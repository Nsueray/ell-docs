# ADR-022: Async Job Pattern for Large Bulk Imports

## Status
DECIDED (13 May 2026)

## Context
Leena's reactivation campaign module needs to process 70,000-row Excel uploads in a single admin action. The pre-existing synchronous implementation had three blocking issues:

1. **Browser timeout.** Heroku/Render's default request timeout is 30 seconds. A 70k-row insert with per-row INSERT, email-queue INSERT, and dedup lookup against an existing 80k visitors table runs past 30s — the browser drops the connection and the admin sees a generic 504 with no indication of how far the import actually got.

2. **No progress feedback.** A request that takes 2+ minutes with no UI signal is indistinguishable (to the admin) from a frozen page or a silent crash. Yaprak abandoned and retried a 35k campaign twice in April 2026, creating duplicate token rows that had to be cleaned by SQL.

3. **All-or-nothing transaction risk.** Wrapping 70k inserts in a single transaction holds row locks for minutes and blocks the email_worker. Wrapping them outside a transaction risks partial completion with no rollback path.

This pattern was first prototyped on 30k rows during the 12 May audit, validated on 32k rows in a production smoke run, and locked in for Yaprak's 13 May 70k campaign. Same shape applies to any future ELL bulk operation: LİFFY mining ingestion, LİFFY bulk export, ELIZA report generation, ELIZA migration scripts.

## Decision

Adopt a three-component async job pattern for any bulk operation that may exceed a 30-second HTTP request:

1. **Job state table (`import_jobs`)** — durable record of work, status lifecycle, and progress counters.
2. **Fire-and-forget background processor** — `setImmediate(...)` launches a chunked processor after responding to the client.
3. **Polling endpoint + 202 response** — endpoint returns `202 Accepted` with a `job_id` immediately; frontend polls `GET /api/<module>/job/:id` every 2s to render progress.

### Reference implementation (Leena)

- Migration: `migrations/005_import_jobs.sql` — creates `import_jobs(id, organizer_id, job_type, target_expo_id, source_expo_id, template_id, form_id, total_count, processed_count, skipped_count, failed_count, status, error_message, created_at, updated_at, completed_at)`.
- Backend: `routes/reactivation.js` POST `/create-from-excel` and POST `/create-from-expo` (commit 094ef99).
  - Synchronous phase: parse Excel → pre-fetch existing emails + tokens + unsubscribes into in-memory `Set`s for O(1) dedup → filter valid rows → `INSERT INTO import_jobs (..., status='processing')` → return 202 with job_id.
  - Background phase: `setImmediate(() => processReactivationChunks(jobId, validRows, ctx))` — function loops over rows in `CHUNK_SIZE=1000` slices, each chunk wrapped in `BEGIN/COMMIT/ROLLBACK` via a single `pool.connect()` client. After each chunk: `UPDATE import_jobs SET processed_count=$1, updated_at=NOW() WHERE id=$2`. On chunk failure: rollback, increment `failed_count` by chunk size, continue. On final completion: `UPDATE import_jobs SET status='completed', completed_at=NOW()`. On fatal exception: `UPDATE import_jobs SET status='failed', error_message=$1`.
- Polling endpoint: `GET /api/reactivation/job/:id` — returns full job row (organizer-scoped).
- Frontend: `public/reactivation-campaign.html` — submit button posts, receives 202, opens progress bar; `setInterval` polls every 2s; switches to "Completed" / "Failed" terminal state when `status !== 'processing'`.

### CHUNK_SIZE rationale
1,000 rows × 2 INSERTs/row × ~3KB html_content per row ≈ 6MB per chunk transaction. Holds row locks for ~200-400ms, releases between chunks, lets email_worker and visitor reads through.

## Consequences

**Positive**
- 30-second browser timeout no longer a constraint; arbitrary-size imports work as long as DB has capacity.
- Admin sees real-time progress, can leave the tab open or refresh later (job state is in DB).
- Per-chunk transaction means a single bad row only loses its chunk (max 1000 rows), not the entire 70k import.
- Pattern is module-agnostic — same shape transferable to LİFFY (mining bulk ingestion, bulk export) and ELIZA (data migration, report jobs).

**Trade-offs / known risks**
- **R5 (existing): Stale `processing` email_queue rows** — unrelated to import_jobs but same conceptual shape: if a worker is mid-transaction during deploy/restart, the row is stranded. Recovery cron is on the post-fair backlog.
- **R8 (new for this pattern): setImmediate orphan on server restart.** `setImmediate` runs inside the same Node.js process that returned the 202. If the web service restarts (Render deploy, OOM, manual restart), the callback is lost; `import_jobs.status='processing'` stays stuck with no further progress. **Mitigation owed (post-fair): boot-time orphan detector** — on web service startup, scan `import_jobs WHERE status='processing' AND updated_at < NOW() - INTERVAL '5 minutes'`, either mark `failed` with `error_message='Server restarted during processing'` or re-enqueue from snapshot.
- **Memory pressure.** Pre-fetching all existing emails into in-memory Sets scales O(n) with organizer's total visitor count, not import size. At ~100k visitors per organizer this is ~10MB per Set — acceptable. Beyond ~1M visitors, switch to per-row indexed DB lookups.
- **No cancel UI.** The 202 → polling pattern has no "cancel job" button. Admin who realizes an Excel was wrong cannot stop the import once running. **Mitigation owed (post-fair): cancel endpoint that sets `import_jobs.status='cancelled'` and a check inside `processChunks` loop that bails on the next chunk.**

## When to use
- Bulk operation processing **1,000+ rows** OR likely to exceed **20 seconds** wall-clock.
- Operation safely chunkable (no global ordering or cross-row dependencies that span chunks).
- Job state worth persisting for audit / retry / debugging.

## When NOT to use
- Sub-1000-row operations where a 1-3 second sync response is acceptable.
- Operations that require synchronous result data in the response (e.g., an UPSERT that must return the new IDs to the caller for next-step logic).
- Operations that can't be safely interrupted between chunks (rare — most chunking is fine if each chunk is its own transaction).
- Lightweight reads or single-row mutations.

## Cross-system applicability

This pattern is the recommended approach for any bulk-write or bulk-compute operation across ELL:

- **LİFFY mining ingestion** — Apify scrape → 10k-100k persons import. Replace any current sync ingestion.
- **LİFFY bulk export** — Excel/CSV export of large persons or affiliations lists.
- **ELIZA historical migration** — Zoho → ELIZA contract/invoice import (estimated 30k+ contracts, 200k+ payments).
- **ELIZA report generation** — multi-table aggregations that take >10s.

Each system implementing this pattern should:
1. Create its own `<module>_jobs` table (or shared `jobs` table if scoping by `job_type`).
2. Use `setImmediate` + chunked transactions in the system's own API service.
3. Polling endpoint follows `/api/<module>/job/:id` convention.
4. Until a boot-time orphan recovery cron is built, expect post-restart job loss and document it for operators.

## Alternatives Considered

1. **Synchronous request with extended timeout.** Rejected. Render and Cloudflare both enforce hard timeouts (30s and 100s respectively); extending application-level only doesn't help. Also leaves browser hanging.

2. **Job queue with separate worker process (BullMQ, pg-boss).** Considered. Cleaner separation: web service ENQUEUES, dedicated worker DEQUEUES. Survives web restart because state is in queue, not in process memory. Rejected for this sprint because: (a) requires new infrastructure (Redis or another long-running worker process); (b) Leena already has a long-running worker (`email_worker.js`) doing different work; layering a second worker just for imports added more deploy/ops surface than the problem warranted at fair-prep time. **Revisit post-fair** — if R8 orphan recovery becomes painful, migrate to pg-boss using existing PostgreSQL.

3. **Synchronous request that returns 202 + later webhook.** Rejected. Requires the admin's machine to be reachable for the webhook, which it never is from a Render service. Polling from the browser is the natural fit.

4. **WebSocket / SSE push for progress.** Considered. Simpler UX (no polling latency), but adds long-lived connection infrastructure to a service that doesn't otherwise need it. Polling every 2s is good enough for a job that runs 30-300 seconds; per-chunk granularity isn't valuable enough to justify the complexity.

## Implementation Notes

- 2026-05-13: Pattern adopted in Leena reactivation module. Commit 094ef99 (backend), migration `005_import_jobs.sql`, frontend polling in `public/reactivation-campaign.html`. Validated on 32k smoke run and 41k production run (Yaprak's Mega Clima Nigeria campaign).

## Related
- `migrations/005_import_jobs.sql` — schema
- `routes/reactivation.js:processReactivationChunks` — reference implementation
- ADR-017 (Email queue logging — worker-only writes) — same single-source-of-truth principle applied to logging
- ADR-019 (Bulk email send architecture) — adjacent pattern: bulk INSERT with chunking, but synchronous because <10k typical
- Post-fair backlog: setImmediate orphan recovery cron (R8 mitigation)
- Post-fair backlog: cancel-job endpoint + chunk-loop bail check
- Leena CLAUDE.md 13 May 2026 sprint entry
