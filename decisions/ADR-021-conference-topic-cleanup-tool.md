# ADR-021: Conference Topic Cleanup Tool (Temporary Pattern)

## Status
DECIDED (10 May 2026)

## Context
Mega Clima Nigeria 2026 fair starts 19 May 2026 (8 days away). PDF screenshot from Yaprak showed conference topic data quality issue: UI lists "43 topics" but actual canonical list per organizer is 13 topics.

Investigation revealed deeper problem:
- DB has 55 distinct conference_topic variants in Nigeria expo
- Variants include: apostrophe character mismatches (curly ' vs straight '), "Day 1 |" prefix variants, numbered variants ("3." vs "3)" vs "3 "), semicolon-separated topics (instead of " || "), JSON array string literals (one visitor has '["Day 1 | ...", "Day 2 | ..."]' as conference_topic value)
- 1294 total registered visitors for Nigeria expo, ~30% with non-canonical variants
- Conference certificates table inherits same data quality issues via text-level UNIQUE constraint

Root cause: Conference topics are NOT first-class entities. They exist as free-text strings in two locations:
1. `visitors.custom_fields->>'conference_topic'` (multi-topic via " || " separator)
2. `conference_certificates.conference_topic` column

The canonical source of truth is `forms.fields` JSONB array for the active conference form per expo — but this is a configuration artifact, not an entity. Form changes don't propagate to existing visitors.

## Decision
Build a temporary cleanup tool, NOT an architectural refactor.

### Why temporary?
- Fair starts in 8 days. Conference Entity Migration would affect 8-10 modules (visitors, webhook, certs, scanner, reports, segments, email campaigns, forms) and require multi-table migration during live operation. Risk too high near live event.
- Per existing principle (CLAUDE.md, "Risk-first sequencing near live events"): non-critical architectural changes deferred to post-fair.
- Data quality issue is one-time, not recurring (Zoho form dropdown already constrained to 13 canonical options — webhook not yet validated server-side, but no new bad data flowing).

### What the tool does
Temporary admin UI at `/conference-cleanup.html` and backend at `/api/conference-cleanup/*`. Admin selects expo, sees all conference_topic variants with visitor + cert counts, filters non-canonical, selects visitors, picks target canonical topic from dropdown (dynamically loaded from form.fields), previews impact via dry_run, executes with transaction-wrapped segment-aware rename.

### Key technical decisions

1. **Segment-aware rename, not full-string replace.** Multi-topic visitors (228 in Nigeria, " || " separated) require modifying only the matching segment, preserving other topics. Implemented via JS-level `string_to_array → map replace → join` per visitor (CHUNK_SIZE=100), not single SQL `array_replace`, to handle JSON array edge case and apply defensive trim.

2. **Conflict detection before execute.** `conference_certificates` has UNIQUE (visitor_id, expo_id, conference_topic). Renaming a variant could collide if visitor already has a cert for the target topic. Tool detects conflicts in dry_run, surfaces to admin, deletes old certs on execute (kept newer as canonical).

3. **Dynamic canonical source.** Tool reads `forms.fields[?].options` for each expo's active conference form at runtime. No hardcoded 13-topic list. Adding/removing topics in form auto-updates tool.

4. **Organizer-scoped + expo-scoped.** Every endpoint validates organizer ownership of expo + visitor membership in expo. Cross-organizer leak impossible. Ghana expo (id=5) visible to same organizer, can be cleaned via same tool if needed.

5. **Transaction-wrapped execute.** BEGIN/COMMIT/ROLLBACK at bulk-update level. Any single-visitor failure rolls back entire batch. CHUNK_SIZE=100 for memory bound, all in one transaction.

## Consequences
- Positive: Fair-day-ready in 2-3 days vs. 1-2 weeks for migration. Zero risk to live fair operation.
- Positive: Tool surfaces data quality at variant level — organizer sees exact state and chooses canonical target.
- Positive: Dry-run + conflict-detection prevents UNIQUE constraint violations and accidental data loss.
- Positive: Temporary UI signals one-time use — sidebar link omitted, only accessible via conference-sessions header button + direct URL.
- Trade-off: Underlying anti-pattern (free-text topic in JSONB) remains. Future expos will have same data quality risk unless webhook validation added or full migration executed.
- Trade-off: Tool will be deleted post-fair. ~900 lines of code written for one-time cleanup. Acceptable given the time constraint and risk profile.
- Risk: Webhook still accepts raw conference_topic strings. If Zoho form gets changed or new conference form added without dropdown constraint, bad data flows again. Mitigated by post-fair webhook normalization (todo backlog).

## Alternatives Considered

1. **Conference Entity Migration (full refactor):** Rejected. New tables `expo_conferences` + `visitor_conferences` junction, migrate 1294 visitor JSONB strings to FK rows, refactor 8-10 modules. Estimated 1-2 weeks of work + multi-table live migration. Fair is 8 days away. Too risky.

2. **Manual SQL cleanup by engineer:** Rejected. 30 non-canonical variants x decision per variant = error-prone. Admin (Yaprak) knows canonical mapping; she should drive cleanup, not engineer. Tool surface area lets her decide and execute safely.

3. **Per-visitor edit via existing visitorlog:** Rejected. Existing PUT endpoint does full-replace, not segment-aware. Multi-topic visitors would lose other topics. Also too slow for 30+ variants x 100+ visitors each.

4. **Server-side normalization at write-time only (no historical cleanup):** Rejected. Existing 1294 visitor records remain broken. Fair scanner shows 55 topics in dropdown, hostess confusion at fair-time. Doesn't solve immediate problem.

## Related
- `routes/conferenceCleanup.js` — commit 61db471
- `public/conference-cleanup.html` — commit aa7012f
- Form 39 (Mega Clima Nigeria 2026 Conference Registration) — canonical source, fields JSONB
- conference-sessions.html line 242 orphan link fix — commit 14969f6
- Post-fair backlog: Conference Entity Migration (separate sprint)
- Post-fair backlog: Webhook input validation
- Post-fair backlog: Cleanup tool removal (this ADR's deletion trigger)
- ADR-020 (Shared Frontend Component Pattern) — leena-toast.js reused in cleanup tool
