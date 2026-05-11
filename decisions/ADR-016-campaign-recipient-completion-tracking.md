# ADR-016: Campaign Recipient Completion Tracking

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
DECIDED (5 May 2026)

## Context
Multi-step email campaigns have recipients in `campaign_recipients` table with status field. Before this fix, recipients stayed in 'active' status forever after their final step was sent — `next_step_due_at` was set to NULL but status was not updated.

This caused two cascading issues:
1. `checkCampaignCompletion()` worker query never matched, so campaigns stayed 'active' forever even after all sends completed.
2. UI showed completed campaigns as 'active', confusing operators trying to delete test campaigns.

## Decision
When the worker processes a recipient and finds no next step (`stepsMap[currentStepNum + 1]` is undefined), the recipient's status MUST be set to 'completed' along with `next_step_due_at = NULL`.

This is the single source of truth for "this recipient has finished the campaign flow."

## Consequences
- Positive: campaigns automatically transition to 'completed' once all recipients finish, enabling auto-cleanup, accurate reporting, and operator self-service deletion.
- Positive: status field becomes the canonical "is this still in flight?" check across the codebase.
- Migration burden: Existing stuck recipients (37,574 in active campaigns) required one-time UPDATE on 5 May 2026 to backfill the new convention.
- Edge case: Draft campaigns with recipients (added but never activated) are NOT touched — their `next_step_due_at IS NULL` state is genuine "never started," and they will be set correctly when worker processes them post-activation.

## Related
- `email_worker.js:computeNextDue`
- `email_worker.js:checkCampaignCompletion` (lines 618-624)
- Migration SQL: 5 May 2026 (recipients + campaigns backfill)
- Commit: a449ccb (code fix), 839e3e0 (campaign delete extension)
