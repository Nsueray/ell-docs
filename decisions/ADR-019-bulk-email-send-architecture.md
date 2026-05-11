# ADR-019: Bulk Email Send Architecture

> ℹ️ **CONTEXT NOTE — 2026-05-11**
>
> Bu ADR Aşama 1 mimarisi yazılmadan önce karara bağlandı,
> ama içeriği LEENA implementasyonuna özgü ve yeni mimariyle
> uyumlu. Geçerlidir.
>
> **Master karar referansı:**
> [/architecture/ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md]
>
> ---

## Status
DECIDED (7 May 2026)

## Context
Leena's project manager (Yaprak) needed to send badge emails to visitors who never received one — approximately 288 visitors in the Mega Clima Nigeria 2026 expo. The existing email tools didn't fit this workflow:

- **Send Emails page** (`email-send.html`): Requires manual CSV upload or individual entry. No way to filter by "never sent" status. Synchronous SendGrid calls with 100ms delay — timeout risk for large batches.
- **Email Campaigns** (`email-campaigns.html`): Designed for multi-step sequences with conditions (opened/clicked/registered). Overkill for "send one template to a filtered list."
- **Email Segments** (`email-segments.html`): Only filters by check-in status (checked-in vs. not checked-in). No source, type, or email status filters.

The gap: no tool lets Yaprak use the Visitors page's rich filter system (source, type, date, email status) and then send email to the matching results.

## Decision
Add bulk email send capability directly to the Visitors page, reusing the existing filter infrastructure.

### Backend: `POST /api/visitors/bulk-email`
- **Filter reuse:** Extracted `buildVisitorFilter()` helper from inline filter code in `/paginated` and `/export` endpoints. All three endpoints now use the same WHERE clause builder — including the `email_status` filter with historical NULL visitor_id fallback (ADR-017).
- **Mode 2 queue INSERT:** Writes `visitor_id + template_id` to email_queue. Worker fetches template and visitor data at send time, renders HTML, sends via SendGrid. This was chosen over Mode 1 (pre-rendered HTML) because:
  - Template versioning: if template is updated between queue and send, the latest version is used
  - No HTML rendering in the request path — faster API response
  - Worker already handles Mode 2 reliably for webhooks
- **Transaction wrap:** All batch INSERTs (1000 rows per chunk) wrapped in BEGIN/COMMIT/ROLLBACK. If chunk 3 of 5 fails, all chunks roll back — prevents partial queue state.
- **Validation:** Template must belong to organizer AND match expo (or be global with expo_id=NULL). Expo must belong to organizer. Email must not be NULL/empty. Count must be between 1 and 10,000.

### Frontend: Modal in Visitors page
- "Send Email to N visitors" button appears in table header when filter results > 0
- Modal: template dropdown (loaded from `/api/email-templates`), info banner, confirm dialog
- Button disabled during request to prevent double-submit
- Success toast shows queued count

### What was NOT built
- **Schedule for later:** Worker has no `scheduled_at` support for non-campaign emails. Would require new column + WHERE clause change. Deferred to post-fair backlog.
- **Backend duplicate protection:** No check for "this visitor already has a pending email in queue." Frontend confirm dialog is the only guard. If user submits twice quickly, duplicate emails queue. Deferred to post-fair backlog.
- **Progress tracking:** No real-time progress bar. User sees "N queued" immediately, actual delivery happens in background over minutes. Worker logs provide audit trail.

## Consequences
- Positive: Yaprak can filter visitors by any combination (source, type, email status, date, topic) and send email to all matching results in one action.
- Positive: buildVisitorFilter helper eliminates filter logic duplication across 3 endpoints (was copy-pasted, now single source of truth).
- Positive: Mode 2 queue means worker handles all complexity (template rendering, QR code generation, custom fields). Route stays simple.
- Risk: Double-submit sends duplicate emails. Mitigation: frontend button disable + confirm dialog. Backend mitigation deferred.
- Risk: 10K emails queued at once could slow worker for transactional emails. Mitigation: Sprint 7.1 priority queue — transactional emails (registration, badge) always processed before campaign/bulk emails.
- Trade-off: 10K limit is arbitrary. Mega Clima Nigeria has 4,310 visitors — well within limit. If a future expo has 50K visitors, limit can be raised or batching UI added.

## Related
- ADR-017: Email queue logging strategy (worker-only logging pattern used by bulk send)
- ADR-016: Campaign recipient completion tracking (worker architecture context)
- `routes/visitors.js:buildVisitorFilter` — shared filter helper
- `routes/visitors.js:POST /bulk-email` — endpoint implementation
- `email_worker.js:processTask` — Mode 2 processing path
- Post-fair backlog: schedule support, backend duplicate protection
