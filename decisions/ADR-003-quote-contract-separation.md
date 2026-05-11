# ADR-003: Sales Agents Never Create Contracts

> 🔄 **NEEDS REVISION — 2026-05-11**
>
> Bu ADR'nin temel prensibi (sales agent contract yaratmaz)
> korunuyor. Ama Quote→Contract akışı v1.1'de iki birinci
> sınıf akışa genişledi:
>
> - **Akış A:** LIFFY signed quote → Köprü 1 → LEENA pending
>   convert → Project convert (eski ADR-003 akışının yeni
>   adı)
> - **Akış B:** Yaprak LEENA'da signed quote olmadan da
>   doğrudan contract yaratabilir (Project department veya
>   sales agent attribution ile). "Her sözleşmenin quote'u
>   olmaz" prensibi.
>
> Aşama 2 paralelinde revize edilecek.
>
> **Master karar:**
> [/architecture/ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md]
> (Bölüm 6.5, Köprü 1, Köprü 2, A24, A28)
>
> ---

**Status:** DECIDED
**Date:** 2026-04-10
**Decided by:** Suer Ay
**Category:** Business Rule

---

## Context

In Zoho CRM, the real workflow is: sales agent creates a Quote → authorized manager (Yaprak or country manager) reviews and converts it to a Sales Contract. Sales agents never directly create Sales Contracts because the real contract has many fields that agents don't know or understand. This separation of authority is a critical internal control.

ChatGPT's blueprint and Claude's initial proposal both missed this — they assumed sales agents would create contracts directly.

## Decision

The Quote-to-Contract conversion is an **approval workflow**, not a CRUD operation:

1. **Sales agents** create Quotes in LİFFY (company, expo, stand size, proposed price)
2. **Quotes** are submitted to ELIZA's approval queue via API
3. **Authorized managers** (Yaprak, country managers, CEO) review in ELIZA
4. **On approval**, the manager converts the Quote into a Contract — adding fields the agent doesn't see
5. **Sales agents** never see the Contract detail view in ELIZA
6. **Payment recording** is also restricted — sales agents cannot mark payments as received

## Why This Matters

- Agents don't understand many contract fields (payment terms, special conditions, internal notes)
- Without this control, contracts would be inconsistent and unreliable
- This mirrors the existing Zoho workflow — it's not a new restriction
- The audit trail (who created, who approved, who modified) requires this separation

## Permission Model

```
contracts.create       → DENIED for sales agents
contracts.sign         → Yaprak, Country Manager, CEO only
contracts.view_own     → agents see only their own quotes' status
contracts.view_all     → managers, CEO
payments.record        → Finance, Yaprak, CEO only
```

## Consequences

- LİFFY quote form must be simple — agents fill minimal fields
- ELIZA needs an approval queue UI for Yaprak
- Quote → Contract conversion must add/validate additional fields
- Audit trail must capture: who created quote, who approved, who modified contract

## Related Decisions

- ADR-001 (ELIZA as commercial core)
- ADR-006 (Agent firewall)
- ADR-011 (Payment authority — OPEN)

## Implementation Notes

*(Claude Code: add entries here when implementing)*
