# ADR-017: Email Queue Logging Strategy — Worker-Only Writes

## Status
DECIDED (7 May 2026)

## Context
Leena's email system has two tables for tracking email delivery: `email_queue` (pending/processing/sent/failed work items) and `email_logs` (historical record for UI display and audit).

Before this decision, email logging worked as follows:
1. Route handler (visitors.js, webhook.js) INSERTs into `email_queue` with status='pending'
2. Route handler ALSO INSERTs into `email_logs` with status='queued' (immediate log for UI)
3. Worker picks up queue row, sends via SendGrid, then INSERTs a NEW row into `email_logs` with status='sent' or 'failed'
4. The original 'queued' row is never updated

This caused two compounding bugs:

**Bug 1 — Ghost logs:** Every sent email produced TWO `email_logs` rows: one 'queued' (from route) and one 'sent' (from worker). The 'queued' row stayed forever, making the Email History panel show misleading "QUEUED" badges for emails that were actually delivered. 6,159 ghost rows accumulated over 2 months.

**Bug 2 — Missing visitor linkage:** The three Mode 1 email_queue INSERT locations (public form, import existing, import new) omitted `visitor_id`, `expo_id`, `organizer_id`, and `template_id`. When the worker processed these rows, its `logToEmailLogs` function wrote `visitor_id=NULL` — making it impossible to link the 'sent' log back to the visitor. 114,210 of 125,596 sent logs had NULL visitor_id.

These bugs were discovered 12 days before a major fair (Mega Clima Nigeria 2026) when the project manager reported visitors showing "QUEUED" status despite having received their badge emails.

## Decision
1. **Remove route-side email_logs writes.** All four locations where routes wrote 'queued' status to email_logs have been deleted (visitors.js ×3, webhook.js ×1). The worker's `logToEmailLogs` function is now the sole writer of email delivery logs.

2. **Add visitor context to Mode 1 queue INSERTs.** The three Mode 1 INSERT locations now include `visitor_id, expo_id, organizer_id, template_id` alongside `recipient_email, subject, html_content`. Worker Mode 1 priority (html_content check) is preserved — these extra columns are used only for logging, not for email rendering.

3. **Worker is the single source of truth** for email delivery status. A log row appears only after the worker has attempted delivery, with accurate status ('sent' or 'failed').

## Consequences
- Positive: No more ghost 'queued' logs. Email History shows only actual delivery outcomes.
- Positive: Worker logs now include visitor_id, enabling proper linkage in visitor detail panels and email status filters.
- Trade-off: 2-3 second delay before a log appears in Email History (worker polling interval). Accepted because immediate feedback is not critical for email audit logs.
- Migration: 6,396 historical ghost logs cleaned up via SQL transaction (5,086 visitor_id match + 1,310 email match).
- Alternative rejected: Route writes 'queued', worker UPDATEs to 'sent'. This would require the worker to know the original log row's ID — adding coupling between route and worker that doesn't exist today. The simpler "worker writes once" pattern won.

## Related
- ADR-016: Campaign recipient completion tracking (same worker, related timing)
- `email_worker.js:logToEmailLogs` (lines 130-144)
- `email_worker.js:processTask` — Mode 1 vs Mode 2 detection (line 156)
- Fix 1 commit: c3b5df7
- Fix 2 commit: 9a6a0f4
