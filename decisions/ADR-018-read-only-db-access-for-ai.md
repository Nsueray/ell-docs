# ADR-018: Read-Only DB Access for AI Agents

## Status
DECIDED (7 May 2026)

## Context
Claude Code assists with Leena EMS development — analyzing bugs, testing hypotheses, writing queries for data investigations, and verifying fixes. Before this decision, all database interactions required the CEO (Suer) to manually copy-paste SQL into Render Shell and relay results back. This was slow (minutes per query round-trip), error-prone (typos in copy-paste), and blocked deep analysis workflows that require dozens of iterative queries.

The email queue bug investigation (ADR-017) was the catalyst: diagnosing 6,159 ghost logs required 15+ diagnostic queries across email_logs, email_queue, and visitors tables. Each round-trip through Suer added 2-5 minutes of latency.

Options considered:
1. **Full read-write access** — AI could run migrations and fixes directly. Rejected: too dangerous for production. One wrong UPDATE could corrupt visitor data during an active fair.
2. **Staging database clone** — Separate DB with periodic sync. Rejected: complex setup, stale data, doesn't help with production debugging.
3. **Read-only user with IP whitelist** — Separate PostgreSQL role with SELECT-only grants. Chosen: minimal risk, immediate value, simple setup.

## Decision
Create a dedicated PostgreSQL user `claude_readonly` with SELECT-only permissions on the Leena production database.

Implementation:
- `CREATE USER claude_readonly WITH PASSWORD '...'`
- `GRANT SELECT ON ALL TABLES IN SCHEMA public TO claude_readonly`
- `ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO claude_readonly` (covers future tables)
- External access via Render PostgreSQL Inbound IP Rules (Suer's current IP)
- Connection string stored in `backend/leena-v401-backend/.env` as `RENDER_DATABASE_READONLY_URL`
- SSL required (Render enforces)

Access boundary:
- **AI can do:** SELECT, COUNT, JOIN, EXPLAIN ANALYZE, aggregate queries, EXISTS checks
- **AI cannot do:** UPDATE, DELETE, INSERT, ALTER, DROP, TRUNCATE, CREATE — all fail with "permission denied"
- **Write operations:** AI prepares SQL, Suer reviews and executes via Render Shell with `$DATABASE_INTERNAL_URL`

## Consequences
- Positive: AI can independently run diagnostic queries, reducing bug investigation time from hours to minutes. The email queue bug (ADR-017) was fully diagnosed with AI-driven queries in one session.
- Positive: Zero risk of accidental data modification. The PostgreSQL permission system enforces this at the database level — no amount of prompt injection or AI error can bypass it.
- Positive: Future tables automatically inherit SELECT grant via ALTER DEFAULT PRIVILEGES.
- Operational: IP whitelist requires manual update when Suer's IP changes (VPN, ISP change). Connection fails with "SSL connection has been closed unexpectedly" — recognizable error, easy fix.
- Security: Plaintext password in .env on Suer's local machine. Accepted risk — the machine is personal, .env is gitignored, and the user has SELECT-only permissions.
- Alternative for write operations preserved: Suer runs via Render Shell. This human-in-the-loop pattern is intentional for all destructive operations.

## Related
- ADR-017: Email queue logging strategy (first use case for read-only access)
- CLAUDE.md "Database Access" section
- Memory file: `reference_db_readonly.md` (Claude Code session persistence)
