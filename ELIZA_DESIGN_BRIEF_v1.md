> ⚠️ Sapma (2026-10-22, Sentez UI-05): §8'deki React/Next yönü ERTELENDİ — ui2 düz HTML/JS, derleme
> yok. Yeniden tartı tetiği: Sales alanının (LIFFY) ui2'ye taşınma kararı. Kaynak:
> `ELIZA_UI2_ARAYUZ_KURALLARI_v1.md` UI-05.

# ELIZA — Product Design Brief (for Claude Design) v1

**For:** Claude Design — full creative freedom (visual language, typography, color, logo).
**From:** Elan Expo (Suer Ay, Owner).
**Goal:** Design ELIZA — a unified internal platform — from scratch. Brand identity + design system + the shell + anchor screens. You are free to invent the entire visual direction; there is no existing skin to preserve.

---

## 1. What ELIZA is (one paragraph)

ELIZA is the internal operating platform for **Elan Expo**, an international B2B trade-exhibition organizer headquartered in Istanbul with offices across Morocco, Nigeria, Kenya, China, Algeria and Ghana. Elan Expo finds a sectoral opportunity in an emerging market, sells exhibition space (priced by m²) to international manufacturers, and then operates the physical expo end-to-end. ELIZA replaces a legacy CRM and unifies three jobs into **one product with one login**: selling (finding and closing exhibitors), operating (running the physical event — visitors, floor, badges, catalogue), and the money + intelligence layer (contracts, payments, commissions, executive dashboards). It is a daily-use system of record for ~25 staff — built for heavy, fast, professional work, not a marketing site.

---

## 2. Who uses it

- **~25 internal users** across HQ Istanbul + 6 local offices. Roles: Owner (also acts as CEO), Project Department Lead + staff, Sales Manager, Sales Team Lead, Sales Reps, Local Office staff (sales + project), Finance, Admin.
- **Plus external sales people** (freelancers, agencies) who only sell — and must **never** see finance or other people's data.
- **Two trust rings** (this shapes the whole product, see §4):
  - **Inner ring** = trusted: Project team, Finance, Owner → see Operations + Finance.
  - **Outer ring** = untrusted: sales reps + external freelancers → see **only** Sales.
- **Languages:** internal working language Turkish; cross-office English; outreach content in French/Arabic/others. **The UI itself is in English**; the *content* stored in it is multilingual.
- **Devices:** desktop-primary for office work; **mobile is real and important on-site at expos** — check-in, badge printing, badge/lead scanning happen on phones and handheld terminals at the venue.

---

## 3. Brand & naming (please design the brand)

- **The product brand is ELIZA.** Users see and enter "ELIZA" — one product, one identity. Please **design the ELIZA brand identity**: a wordmark (and an optional compact logomark/icon for the app/nav/mobile), in a couple of variations.
  - *Optional inspiration, not a requirement:* the names ELIZA / LIFFY / LEENA come from family names (Eliz, Elif, Lena) — a warm, human origin. Use it or ignore it.
  - The brand should feel **neutral and international** (works across many countries/languages), **professional**, and **product-like** — it is deliberately *not* tied to the company name "Elan Expo," because the product may one day be sold to others. Avoid anything childish.
- **Navigation labels are functional, not internal code-names:**
  - Top-level domain tabs read: **Sales** · **Operations** · **Finance** (big, functional — what the user does).
  - Small secondary label *under* the tab may show the internal name for continuity: **Sales** (liffy) · **Operations** (leena) · **Finance** (no sub-label).
- **Never show internal/technical names** ("ELL", deployment names, database names) anywhere in the UI.

---

## 4. The shell & navigation model (the spine)

One product, one login, **three functional domains** switched at the top level. The product is **access-gated by role** — this is structural, not cosmetic:

| Role | Sales | Operations | Finance |
|---|:---:|:---:|:---:|
| Owner | ✅ | ✅ | ✅ |
| Project team | ✅ (read, for convert review only) | ✅ | ✅ |
| Sales Manager | ✅ | — | (possibly a thin commission view) |
| Sales rep / freelancer | ✅ | — | — |

- A **freelancer literally never sees a Finance tab** — it does not exist in their shell. Design the nav so domains appear/disappear cleanly by permission.
- **Inner ring = one cohesive experience.** Operations + Finance belong together (trusted team moves between them fluidly).
- **Outer ring = a separate, gated world.** Sales feels like its own focused workspace.
- **Mobile:** the on-site **Scan** action (check-in / badge / lead capture) should be prominent and fast — likely a primary action surfaced on mobile.
- Within a domain, visibility follows the **reporting hierarchy** (a manager sees their reports down the chain) — relevant for how lists/dashboards scope, not a separate nav.

---

## 5. The three domains and their internal structure

This is the information architecture. For each domain: the sections, each section's *shape*, and which screens are the anchors. **Maturity tags** tell you what already exists vs what is brand-new (so you know where the design weight is): 🟢 live today · 🟡 built, not yet in use · 🔴 **brand-new, the centerpiece**.

### 5A. Sales (liffy) — the pre-signature sales workspace 🟡
Audience: sales reps + Sales Manager. Pipeline stages: Lead → Contacted → Replied → Qualified (Contact+Company) → Quote Sent → Quote Signed.

| Section | Contains | Shape |
|---|---|---|
| **My Work** (home) | Today's attention list: incoming replies, follow-ups due, quotes to chase | Prioritized work feed |
| **Prospecting** | Lead lists, mining results, campaigns, sequences, segments | Console + lists + campaign composer |
| **Contacts & Companies** | Qualified real people/companies (CRM core) | List + 360° detail |
| **Pipeline & Quotes** | Deal stages board; create/send/track quotes | Pipeline board + quote editor |

> Principle: activity tracking must **emerge from work already done** (an email sent, a quote made, a reply received) — **not** a separate "tasks/log" module. The home is the Action Screen, not a to-do list.

### 5B. Operations (leena) — running the physical event 🟢 (the live workhorse)
Audience: Project team + on-site staff + Owner. **Everything is scoped to an expo:** pick an expo, then work inside it (plus a cross-expo overview).

| Section | Contains | Shape |
|---|---|---|
| **Expos** | All expos; pick one → its operations dashboard. **Cluster-aware** (see §6) | Portfolio → ops dashboard |
| **Exhibitor & Floor** | Signed-exhibitor onboarding (catalogue, stand design, build-up, exhibitor badges); floor-plan editor; **Catalogue Generator** 🔴; on-site lead scanner | List+detail / visual editor / generator |
| **Visitor & Access** | Registration forms; visitor records + import; check-in; badge templates; terminals | Form builder / **dense data table** / check-in console |
| **Conferences** | Sessions; conference scanner; attendance | List + session detail |
| **Communications** | Email templates / campaigns / segments / sending; re-activation | Template editor / composer |
| **Reports** | Check-in / attendance / operational reports | Dashboard + reports |

> **Critical:** the Operations dashboard must reflect the **whole operation** — exhibitors signed/onboarded, floor occupancy %, visitor registrations + live check-in traffic, conference attendance, pending operational emails, countdown to event — **not just visitors**. Today this product *looks* like a visitor-tracker; it is actually a full event-operations command center. Make that obvious.

### 5C. Finance (the ELIZA domain) — money + intelligence 🔴 (mostly brand-new — the prize)
Audience: Owner, Finance, Project team. **Most of this is being built from scratch** — design it as the modern centerpiece, not a port of an old system.

| Section | Contains | Maturity |
|---|---|---|
| **War Room / Executive** | Owner's daily executive views | 🟡 |
| **Contracts** | Sales Contracts (post-convert), filling operational fields | 🔴 |
| **Money** | Payments/revenue, expenses, multi-account ledger | 🔴 |
| **Commissions & Agents** | Commission calculation + the sales-agent registry | 🔴 |
| **Expo Finance** | Per-expo P&L, budget vs actual | 🔴 |
| **Intelligence** | AI query engine + assistant | 🟡 |

---

## 6. Product concepts the design must respect

These shape real layouts — don't design generic CRM screens:

- **Per-expo context.** Operations is expo-scoped: a clear "which expo am I in" context, easy switching, plus an all-expos view.
- **Cluster.** Two or more co-located expos (same venue + dates) are operationally one event but commercially separate. The Expos list and the ops dashboard must handle **combined vs per-expo** views — don't assume one-expo-at-a-time.
- **Convert gate.** The seam between Sales and the inner ring: when a quote is signed, the Project team reviews it and converts it into a Sales Contract. Design a clean review/convert moment — lightweight, not a heavy multi-step approval.
- **Multi-currency.** Money is tracked in the currency it actually moved (NGN, MAD, EUR, USD, TL, KES…) with a **frozen exchange rate per transaction**, and consolidated to EUR for reporting. Show **transaction currency + EUR equivalent** together. Support "cash" as a payment method.
- **Computed, not stored, totals.** Balances, outstanding amounts, credit balances, commission adjustments are **sums over transaction streams** — present them as live/derived figures, with the ability to drill into the transactions behind a number.
- **Per-row commission overrides.** Commission rates are adjusted per contract / per agent / per expo. The contract/commission UI must make overriding a single line natural.
- **Operational vs marketing email.** Operational mail (badge, payment reminder — must always arrive) is distinct from marketing campaigns (opt-out, bulk). Reflect this distinction where email is composed/sent.
- **Density is a feature.** The daily reality is heavy data work: visitor logs (tens of thousands of rows), lead lists (hundreds of thousands), contracts, payments. Tables must be **scannable, filterable, and fast** — compact rows, sensible sticky headers, a *restrained* filter bar (not a giant filter panel), good empty/loading states.

---

## 7. Creative direction — full freedom

**Invent the visual language. There is no skin to preserve and no palette to match.** We want to see your strongest, most considered direction — including the ELIZA logo. (We have an internal fallback direction in reserve, so explore boldly; if we prefer it we'll say so. Don't hold back.)

**The feel we're after** (interpret freely):
- Professional, calm, confident, **trustworthy** — this holds money and is the system of record.
- **Efficient for heavy daily use** — legible at density, low visual noise, fast to scan.
- Modern and intentional, **not trendy-for-its-own-sake**, not childish, not over-decorated.
- **International / multi-office** — neutral, not culturally narrow.
- Must hold up across three very different contexts: a sales rep's fast list-work, a finance executive dashboard, and an on-site mobile check-in under venue lighting.

**Anti-patterns to avoid** (real problems in the systems we're replacing):
- Big bilingual "help" banners on every page.
- Emoji used as UI icons.
- Inconsistent stat cards (every page styled differently).
- Heavy, cluttered filter panels.
- Double / nested sidebars.
- Long unstructured flat lists with no hierarchy.
- Loud, childish color.

---

## 8. Technical constraints (so it's buildable)

- Target stack: **React / Next.js + Tailwind**. Build a real **design system** (tokens + components), not just mockups.
- **Don't hand-design every screen.** Establish the visual language + a reusable component set + the anchor screens below; the rest of the product is built from that system.
- The **floor-plan editor** is a specialized canvas (existing, complex) — **out of scope** for this design pass; represent it as a placeholder/frame, don't redesign the canvas itself.

---

## 9. Deliverables

1. **ELIZA brand:** wordmark + optional logomark, 1–2 variations, light/dark.
2. **Design system:** color palette, typography scale, spacing, and core components — buttons, inputs/forms, cards, **data tables**, top-nav + domain tabs (with the small sub-labels), badges/status chips, modals/drawers, empty states, loading states.
3. **The shell:** login, the top-level domain switch (Sales/Operations/Finance) with role-gated visibility, and the in-domain navigation pattern.
4. **Anchor screens** (a few per domain — enough to prove the system):
   - **Sales:** My Work (rep home) · Pipeline board · Quote editor · Contact/Company 360.
   - **Operations:** the whole-operation **Expo dashboard** · **Visitor Log** (the dense table) · Exhibitor & Floor view · a public registration form.
   - **Finance:** War Room / Executive dashboard · Contract detail (with money + commission) · a payments/ledger view.
5. **Mobile:** the on-site **Scan** flow + a mobile dashboard and a mobile list view.
6. **States:** empty, loading, and error patterns as reusable parts.

---

## 10. What success looks like

A single, coherent product that:
- Reads instantly as **one platform (ELIZA)** with three clear functional areas, gated by role.
- Makes Operations look like a **full event command center**, not a visitor tracker.
- Makes the new Finance/commercial core feel like a **modern, trustworthy money system**.
- Stays calm and fast under **dense daily data work** — and works **on a phone at the venue**.
- Has a brand identity we'd be proud to put on a login screen — and, one day, to sell.
