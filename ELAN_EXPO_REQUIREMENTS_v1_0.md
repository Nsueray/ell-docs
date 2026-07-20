# Elan Expo — System Requirements
## What ELL Must Do (and Do Better Than Zoho)

> **Amendment 2026-07-20:** ELIZA is retired as a separate system/database
> (2026-06-19 decision); ELIZA survives as brand/Finance-tab label within LEENA.
> Single-source-of-truth principle locked: see `decisions/ELL_TEK_KAYNAK_KILIT.md`.
> Where this document references ELIZA as a standalone system, read LEENA Finance.

**Version:** 1.0 (Document complete — all parts filled)
**Date:** 2026-05-06
**Status:** In progress — being filled section by section
**Owner:** Suer Ay
**Purpose:** Canonical requirements document for ELL system design. This is the source of truth for what Elan Expo needs. Existing Zoho usage is reference, not blueprint. ELL must match Zoho's coverage AND exceed it on flexibility, autonomy, speed, usefulness, and adaptability — otherwise the migration has no purpose.

---

## How To Read This Document

> Notes for Suer:
> - **Sections marked [TBD]** = content to be filled in next sessions
> - **Sections marked [PRINCIPLE]** = non-negotiable design rules
> - **Sections marked [FACT]** = current operational reality

---

## Part 1 — Company & Context

### 1.1 What Elan Expo Is

[FACT]

Elan Expo is an international trade exhibition organizer headquartered in Istanbul, Turkey. The company designs, sells, and operates B2B exhibitions across multiple continents — primarily in emerging markets where Western European and Turkish exporters seek to expand. Elan Expo is the bridge: it identifies a sectoral opportunity in a target country, negotiates venue and local partnerships, and sells exhibition space to manufacturers and distributors who want to reach that market.

The company organizes exhibitions in sectors including HVAC, construction, food machinery, water systems, ceramics, decoration/furniture, electricity, agriculture, and information technology. Each expo brings together international exhibitors (the paying customers) and local visitors (the audience). Revenue comes primarily from exhibition space sales (m²-based pricing), supplemented by sponsorships, extra equipment rentals, visa-letter services, and ancillary expo services.

The business is fundamentally **relationship-driven and operations-heavy**. A single expo requires coordination across sales, project management, local logistics, stand contractors, hostess agencies, freight forwarders, travel agencies, visa support, catering, and venue authorities — often across language and time-zone boundaries. The CRM and operational software stack must reflect this reality, not just the sales pipeline.

### 1.2 Operating Footprint

[FACT]

**Offices:**
- **HQ — Istanbul, Turkey** — Owner, Project Department Lead, Sales Manager, Sales Team Lead, plus supporting staff
- **Morocco Office — Casablanca** — local sales and project staff
- **Nigeria Office West Africa** — Country Manager, local sales team, project staff
- **Kenya Office** — local sales and project staff
- **China Office** — local representation
- Smaller presences in Algeria, Ghana

**Active markets:** Nigeria, Morocco, Algeria, Kenya, Ghana, China, Turkey, plus exhibitor sourcing from Western Europe (Germany, Italy, Spain, France), India, and other regions.

**Currencies in regular use:** EUR (default reporting), NGN (Nigeria), MAD (Morocco), TL (Turkey), USD (some contracts), KES (Kenya), DZD (Algeria), GHS (Ghana). Exchange rates are updated when transactions occur, frozen at the rate-of-record once entered, and consolidated to EUR for reporting.

**Languages in daily use:** Turkish (HQ internal), English (primary cross-office), French (Morocco, Algeria), Arabic (Morocco, occasionally), with translated outreach in additional languages depending on target market.

### 1.3 People & Roles

[FACT]

**Hierarchy is mutable.** Roles change. Promotions happen, people leave, new managers come in, team structures evolve. The system must reflect today's structure but allow tomorrow's reorganization without code changes.

**Current structure (May 2026):**

```
Owner
├── Sales Manager (accountable for all sales)
│   ├── Sales Team Lead (recently promoted from sales rep — has reports)
│   │   └── Sales reps reporting to Sales Team Lead
│   ├── Other direct sales reps (no team underneath)
│   └── Local office sales staff (Nigeria, Morocco, Kenya, China)
│
└── Project Department Lead
    ├── Local office project staff
    └── Data entry coordination
```

> The Owner role currently combines what would, in a larger organization, be Owner + CEO. A dedicated CEO may be hired later. Until then, Owner functions as both. The system must support this combined role today and the separation tomorrow.

**Three role categories:**

1. **System users** (~25 people) — staff who log into the platform and use it daily. Salaried employees of Elan Expo or its local subsidiaries.

2. **Sales agents** (~150 entities) — anyone whose sales must be tracked for commission. This includes the system users above, plus:
   - **External agencies** (independent expo-marketing firms in Turkey and partner countries) who sell on commission but do not use the system
   - **Freelancers** brought in for specific expos or campaigns
   - **Inactive past staff** whose historical contracts must remain attributable

3. **Data entry contractors** — temporary, no system login, submit data through public forms.

The distinction between "user" and "sales agent" is structural, not cosmetic. It will be enforced in the schema. (See Part 3.2.)

**Function split — Sales vs Project:**

- **Sales side** (Sales Manager's organization) is responsible for: lead generation, outreach, qualification, quote creation, closing. Sales reps work in the active phase before signature.
- **Project side** (Project Department Lead's organization) is responsible for: post-signature operations, expo execution, exhibitor onboarding, catalogue production, logistics coordination, expense tracking, and payment collection. The Project department takes over once a quote is signed.
- **Owner** sees everything, approves exceptions (large discounts, unusual commission structures, refunds), and uses the executive dashboard for visibility.

The Quote → Sales Contract conversion is the handoff point between sales and project. Today this happens via a manual "Convert" action by the project team after sales signals "Signed." It is technically a data conversion but functionally a quality gate — the Project department reviews, fills in missing fields, and corrects errors before the contract becomes operational.

### 1.4 Business Volume (Approximate)

[FACT]

**Expos:** 202 expos in the master record (active + archive). Roughly 10–15 expos per active year, depending on market conditions.

**Exhibitors / Customers:** ~18,000 companies in the database, ~17,500 individual contacts. Active paying exhibitors per year are a smaller subset (varies by expo size).

**Leads:** ~587,000 leads accumulated since CRM inception. Channel breakdown approximately:
- Web mining (~344K, the largest channel)
- Web forms ("Contact Us" submissions)
- Excel imports (bulk lists)
- Freelance data entry (public forms)
- Online marketing (Google Ads, Facebook lead ads)
- Expo visitor capture (converted from past attendees)
- Manual entry (sales reps adding contacts they personally meet)

Most of the 587K is dormant or cold. Roughly 75K are considered the active working portfolio.

**Sales agents:** 150 active records (employees + external + freelance).

**Products:** ~242 SKUs in the catalogue, including main exhibition packages (PES, RF, SYK), per-expo equipment (TV, fridges, counters, chairs — often duplicated per market with different pricing), visa letters, sponsorships, and ancillary services.

**Quotes & Sales Contracts:** Thousands of records, with active flow concentrated around expos in the next 6–18 months.

**Revenue records:** ~731 visible payment records in current active view; full historical dataset is larger.

**Catalogue records:** 1,300+ exhibitor catalogue submissions accumulated.

### 1.5 Cultural & Operational Quirks

[FACT]

These are realities that affect how the system must be designed. They are not problems to fix — they are features of the business.

**Multi-currency mixing.** A Nigerian exhibitor may sign a contract in NGN, pay HQ in EUR by international wire, and have local on-site expenses paid in NGN by the Nigeria office. The system must track money in the currency it actually moved, with frozen exchange rates per transaction, and consolidate everything to EUR for executive reporting.

**Cash-from-hand payments.** Not all payments arrive by bank transfer. Local exhibitors sometimes pay in cash to local office staff, who then deposit into the local office account. The system must handle "cash" as a valid payment method without requiring banking integration.

**HQ-supports-local financial flows.** HQ frequently sends operational subsidies to local offices in their local currency. Local offices sometimes remit collected funds back to HQ. The flow goes both ways and varies by expo, season, and cash position. Multi-account ledger must reflect this naturally.

**Motivation-driven commission flexibility.** Commission rates are not contractual fixtures. The CEO and Sales Manager adjust them per contract, per agent, per expo — sometimes to push sales of a slow-selling expo, sometimes as a one-off incentive, sometimes to align with a specific deal's economics. The system must support per-contract overrides on a per-row basis, not require a policy change to deviate.

**Hierarchy fluidity.** Roles change. A sales rep was promoted to Sales Team Lead recently. Tomorrow another rep may be promoted, or restructured into a different team, or a new manager may be hired between the Owner and the Sales Manager. The hierarchy and reporting structure cannot be hardcoded; it must be editable from an admin UI.

**Mixed-language internal communication.** Turkish is the dominant internal language at HQ, but documents (contracts, catalogues, emails to exhibitors) are produced in English, French, Arabic, and other languages depending on the target audience. The system itself can be in English (Suer is comfortable), but content stored in it is multilingual.

**Sales Agent ≠ User reality.** Many sales agents are not employees, are not Elan Expo staff, and have no reason to log into the platform. An external agency closes deals on commission and reports them to Elan Expo by email. The deal must be attributed to that agency in the contract, but the agency does not need a login. The current Zoho approach forced Elan Expo to either give logins (paying per-user license) or fake-attribute to internal users — both unacceptable.

**Project team as quality gate.** The "doğal kontrol kapısı" (natural control point) at Quote → Contract conversion is not a formal approval workflow but is real and valuable. Sales reps focus on closing; the Project department focuses on data integrity and operational readiness. The system should preserve this gate — make it lightweight, not bureaucratic — without forcing it into a formal multi-step approval flow.

**Cancellation favors credit over refund.** When a contract is cancelled, the company prefers to convert the paid amount into a credit balance for a future expo, rather than process a refund. Refunds are the exception, not the default. Commission already paid to the salesperson is deducted from their next commission earnings rather than clawed back.

**Catalogue is a designed publication, not a data export.** Exhibitor catalogues are print-quality publications produced by the Project department, currently in Corel Draw, used for matbaa (printing house) production, digital print, and online distribution per expo. The catalogue is a real deliverable to exhibitors and a marketing artifact of the expo. ELL must replace this manual design work with automated, template-driven generation — this is one of the biggest efficiency wins available.

**One email template, dynamic data per expo.** Communication automation does not maintain separate templates per expo. There is one template per email type (Welcome, Catalogue Form, Stand Design, Boost, Extra Service, BuildUp Rules, Payment Reminder, Badge, etc.), and the expo-specific information (expo name, dates, venue, partners) is pulled dynamically from the Expos module at send time. This keeps template maintenance manageable.

**Tasks/Meetings/Calls adoption failure.** The Owner has tried for years to get the sales team to use Zoho's task and activity tracking. It has never stuck. The system feels disconnected from the actual work. ELL must not repeat this mistake — activity tracking must emerge from work that is already being done (an email is sent, a quote is generated, a reply arrives), not require manual logging in a separate module.

---

## Part 2 — The Eight Core Workflows

[TBD — to be filled in next session]

### 2.1 Lead Acquisition & Distribution

**What a "lead" is at Elan Expo**

A lead is a clue, not a known entity. It is something we found — almost always an email address, sometimes nothing more — that we believe might belong to a company we could turn into an exhibitor. We don't know who they are. We don't know their company name, country, or sector with certainty. We don't even know if there is a real human behind the email.

The work of "leading" is the work of turning that clue into knowledge. We send an email. If we get a reply, we learn who they are. If they're a real person at a real company in a relevant sector, they may become a contact. If they're interested in an expo, they may become a quote. If the quote is signed, they become a customer.

This definition matters because it explains why Elan Expo has 587,000 leads. A lead is not a "qualified prospect" — it is anything we tried to talk to. Most of them never replied. Some replied and turned out to be students, bots, wrong people, or simply not interested in trade exhibitions. A handful turned into real business. The system has to hold all of them, because at the moment of acquisition we cannot tell which is which.

**Channels and approximate volume**

Leads enter Elan Expo from seven channels:

1. **Web mining** — automated scraping of expo websites, exhibitor directories, and industry sources. By far the largest channel: ~344K of ~587K total leads (about 58%). Quality is unknown until contacted; volume is enormous; email verification is mandatory before any outreach.

2. **Web forms** — "Contact Us" submissions on Elan Expo's own websites and per-expo landing pages. Lower volume, higher intent. Unlike mining, the person has already taken an action toward us.

3. **Excel imports** — bulk lists purchased, exchanged with partners, or compiled from past expo attendee lists. Variable quality. Requires deduplication against existing records.

4. **Freelance data entry** — contractors hired to research and enter leads through public forms. No system logins; they submit through a public form that creates lead records directly. Lower volume than mining but typically more context per lead because a human filtered.

5. **Online marketing** — Google Ads, Facebook lead ads, LinkedIn campaigns. Lead is captured by the marketing platform and forwarded into the system.

6. **Expo visitors** — past attendees of Elan Expo's own expos, captured at registration or check-in. These live in the LEENA system, not in the lead database directly. Conversion from visitor → lead is a separate decision.

7. **Manual entry** — sales reps adding contacts they personally meet at conferences, industry events, networking, referrals. Low volume, high context.

The exact percentages between channels 2–7 are not tracked today. Mining dominates by raw count, but the lower-volume channels carry significantly higher per-lead value.

**Lead enrichment — the most under-used capability**

When we send an email to a lead and they reply, we learn things. Their name. Their company. Sometimes their role, country, or sector. We learn whether they're interested in expos at all, in our specific expo, or in nothing.

Today this enrichment is mostly lost. The salesperson reads the reply, mentally notes that "this person isn't interested," and moves on. The lead record stays as it was — just an email — because manually editing the lead to add the new information is friction the salesperson skips.

This is the largest hidden inefficiency in the current lead system. Six months later, when a new expo is launched in a related sector, the same lead surfaces in a campaign and gets a cold email — because nothing in the record says "we already talked to this person." The same anonymous email gets contacted three, four, five times across different expos, even after they've explicitly told us they aren't interested.

ELL must make enrichment automatic or near-automatic:
- When a reply is received, parse it for sender name, company, and signature data; offer to update the lead with one click
- When a lead progresses to a quote or contract, the contact and company information must flow back to enrich the lead record
- When a lead replies "not interested," capture that as a status change automatically, not as a manual action

**Disqualification — the second under-used capability**

Some leads are not real prospects. The reply comes from a student researching a topic, a bot, an unrelated company, or someone who explicitly says "I never attend trade exhibitions." Today these leads are not removed and not flagged. They sit in the database forever, contributing to noise and re-contact.

The fear of deleting is rational. If we delete a lead and discover six months later that it was actually a real prospect, we have lost the channel attribution and the history. The fear of marking-as-disqualified is also rational, but smaller — it preserves the data while signaling "do not contact again."

ELL must make disqualification a low-friction, reversible action:
- Categorized reasons (not an expo audience, wrong region permanently, requested removal, suspected bot, hard-bounce repeated)
- Visible but inactive in working queues
- Easy to reverse if the categorization was wrong
- Automatic, where possible (a hard-bounce on three campaigns auto-flags, etc.)

**Multi-expo candidacy — only after identification**

Because a raw lead is an anonymous clue, there is no meaningful answer to "which expo is this lead a candidate for." We don't know enough about them. The lead is expo-agnostic by nature: it is added to outreach campaigns for whichever expos we are currently selling, and the lead's response (or non-response) gives us our first data.

The question of "which expos" only becomes answerable after the lead is enriched into a contact and a company. At that point we know their sector and country, and we can match them to relevant expos — often more than one. A construction-equipment manufacturer in Italy is naturally a candidate for the Build Expo in Nigeria, the Mega Build Expo in Morocco, and the Algeria Construction Expo simultaneously.

The system must distinguish between these two states cleanly. Leads do not have expo candidates; they have campaign attribution (which campaigns reached out). Contacts and companies do have expo candidates, derived from enrichment.

**Auto-routing and ownership — current rules and current confusion**

Today, the only formal routing rules are at the web form layer in Zoho:

- A web form submission from a country with a local office is auto-assigned to that office's sales staff
- All other web form submissions go to the Sales Manager, who manually distributes them
- Mined leads are added to working lists by the Sales Manager directly; there is no per-lead auto-assignment for mining

This works, but the Owner has noted that lead distribution "is also confusing for me — how should it be?" The honest answer is that no one has formulated a fully satisfying rule, because real-world routing depends on signals that are hard to predict in advance: rep workload, rep specialization, rep availability, expo launch timing, and the Owner's own changing priorities about which expo needs more push.

ELL must support flexible routing without forcing a single rigid rule:
- Default rules per channel (web form by country, mining by sector, etc.)
- Manual override always possible
- Bulk reassignment when team structure changes
- A fallback queue for unassigned leads, monitored by the Sales Manager
- Visibility into routing decisions (why did this lead go to that rep?) so rules can be tuned

**Quality filtering and deduplication**

Duplicates are inevitable across 587K records. The same company appears in mining results, in a freelance submission, and in an expo visitor list — three different events for the same real-world entity. Deduplication must happen at intake, not as periodic cleanup:

- Detect duplicates by email, by company name + country, by domain
- Merge new information into the existing record rather than create a second record
- Preserve channel attribution so the company can be reported as "found via mining and confirmed via web form"
- Handle minor name variations intelligently ("ABC Co.", "ABC Co Ltd", "ABC Limited" — same entity)

Email verification is a separate quality step. Mined emails are unverified; before outreach they pass through verification (current vendor: ZeroBounce). Hard-bounce-likely emails are filtered out before campaign send.

**Response SLA**

There is a real one-week response expectation for web form leads — these are people who actively reached out. Today the SLA is enforced socially, not systemically. The system should make it visible: warn the sales rep when a high-intent web form lead has been waiting, surface aging leads in the daily action queue, and let the Sales Manager see at a glance which reps are responsive to inbound interest.

**Must be better than today**

- **Enrichment must happen.** When a reply teaches us who someone is, the system must capture that — automatically where possible, with one-click confirmation otherwise. The current "the salesperson notices but doesn't update" pattern is the single biggest source of database decay.

- **Disqualification must be normal, not feared.** A lead that is clearly not a prospect must be a single-click action away from being flagged. The fear of deletion must be replaced by a confidence in reversibility and clear categorization.

- **No lost leads.** Web form submissions sometimes fall through cracks today because routing fails, an assigned rep is on leave, or the lead lands in a Zoho view nobody monitors. ELL must guarantee that every captured lead lands in someone's working queue, with a fallback queue for unassigned ones.

- **Channel attribution must be answerable.** The Owner should be able to ask "how many of last quarter's signed contracts started as web form leads vs mined leads" and get an immediate answer. Today the data is in Zoho but the report is hard to assemble.

- **Cross-channel dedup at intake.** A new mining batch must merge with existing freelance and form records, not create duplicates that surface later.

- **Source-driven prioritization.** A web form lead from a known industry player is worth a hundred cold mined leads. The system today treats them with similar priority in the rep's view. ELL must score and surface accordingly.

### 2.2 Sales Cycle (Lead → Signed Contract)

**What this workflow is about**

The sales cycle is the path a lead takes from first contact to a signed contract. It is the work of the sales side of the company: outreach, qualification, quote preparation, negotiation, and closing. Once a contract is signed, the work moves to the project side — see 2.3.

The cycle is not a single linear pipeline. Most leads never respond. Of those who respond, most are not the right fit. Of those who are the right fit, many decline a quote. Of those who accept a quote, some never sign. Each stage filters the funnel, and each transition is also an opportunity to learn — to enrich the lead, qualify the contact, or disqualify with reason.

**The funnel stages**

A record progresses through these stages, but not every record visits every stage:

1. **Lead** — anonymous clue, as defined in 2.1
2. **Contacted** — outreach has been sent (campaign, manual email, or otherwise)
3. **Replied** — the lead has responded; we now know more about them
4. **Qualified Contact + Company** — we have a real person at a real company in a relevant sector; the lead is enriched into a Contact + Company pair
5. **Quote Sent** — a formal quote document has been sent
6. **Quote Signed** — the customer has signed and returned the quote
7. **Sales Contract** (next workflow, 2.3) — the project department has converted the signed quote into an operational contract

Most reporting and rep-level work happens at the boundaries between these stages. The Sales Manager and the Owner watch conversion rates between stages to spot bottlenecks (lots of quotes sent, few signed?), reps in trouble (low reply rate?), and expos in trouble (high quote rate, low close rate?).

**Outreach and qualification**

Outreach today is primarily email. Bulk email campaigns go out per expo, segmented by sector and country. Replies trickle back. The salesperson reads them and decides what to do next: ignore, follow up personally, or move toward a quote. WhatsApp and SMS are planned future channels.

Qualification is informal. There is no formal scoring system in use today. A salesperson reads a reply and forms a judgment: "this person is interested," "this person is asking questions but not buying," "this person is wasting my time." The system does not capture this judgment — it lives in the salesperson's head, or sometimes in a casual note. ELL must make qualification explicit and trackable: a captured intent classification per response, a confidence score, a clear "this contact is qualified" gate.

When a lead replies and is determined to be a real prospect, the salesperson should convert the lead into a Contact + Company pair. This is the moment at which we move from "anonymous email" to "real entity in our database." Today this conversion is manual and skipped often (see 2.1 — enrichment failure). ELL must make it nearly automatic: parse the reply, extract entity information, suggest the Contact and Company creation, ask the salesperson to confirm.

**Quote creation**

A quote is a formal pricing document for a specific exhibitor at a specific expo. It contains:

- **Subject** — an internal identifier, today following a manual pattern of `{Expo}-{Company}-{M²}` (e.g., `BUILDEXPO2026-RAYA ENGR-9SQM`). The subject is visible only inside the company; the customer never sees it. Today this is manually typed and prone to errors. ELL must auto-generate it from the linked records.

- **AF Number** — the unique identifier of the quote/contract. Today this is automatic in Zoho with a single global prefix `A`. ELL adopts a richer schema:
  - `Q{ISO}-{Sequence}` while in Quote stage (e.g., `QNG-811345` for a Nigeria-office quote)
  - `A{ISO}-{Sequence}` after conversion to Sales Contract (e.g., `ANG-811345` — same sequence, prefix changes)
  - Office codes use ISO 3166-1 alpha-2 country codes: TR (Turkey/HQ), NG (Nigeria), MA (Morocco), KE (Kenya), CN (China), DZ (Algeria), GH (Ghana)
  - This makes the AF Number itself a reporting and filtering tool; today the office origin must be derived through joins. New office openings only require adding the ISO code.

- **Customer details** — Company, primary Contact, country, payment terms, payment method.

- **Currency** — selected manually at quote creation. The salesperson chooses based on the customer's preference, the office's normal practice, or the Owner's instruction. A Nigeria-office quote may default to NGN but can be overridden to EUR or USD if the customer requests. The same expo may have quotes in multiple currencies for different customers.

- **Quoted Items** — line items selected from the product catalogue. For an expo-participation quote, this typically includes a main package (PES — Premium Equipped Stand, RF — Registration Fee, or another expo-specific code) priced by m², plus optional extras (extra equipment, sponsorship upgrades, visa letters, transportation services). Discount and tax fields are at the line level.

- **Total amount** — calculated automatically, in the quote currency, with a frozen EUR-equivalent shown alongside.

- **Validity period** — typically until the expo's payment deadline.

**Quote signing — what "signed" means**

In current practice, "signed" means the customer has emailed back a signed copy of the quote document, OR has paid (or partially paid) against the quote. The salesperson updates the quote's stage to `Signed`. This is a manual action with significant operational consequence — it triggers the entire post-signature workflow.

ELL must preserve the manual nature of this action (it is a deliberate signal from the salesperson) but make it more accountable: require a signed-quote scan upload, capture the signing date, and trigger downstream notifications automatically once the salesperson confirms.

**The convert gate — where the project department takes over**

This is the most important transition in the entire sales cycle, and it is built around a deliberate organizational principle: **the project department is the last stop, and the sales side does not see operational details.**

When a quote is marked `Signed`, the system must:

1. Notify the Owner and the Project department (no notification to sales reps — the deal is theirs only until signature)
2. Move the quote into the Project department's review queue
3. Display a clear "Convert to Sales Contract" action available only to the Project department

The Project department then:

1. Opens the quote and reviews every field
2. Compares against the signed contract scan (which is uploaded to Google Drive and linked from the Sales Contract — today via a `Scan Link` URL field)
3. If errors are found — wrong company name, wrong amount, missing detail — the Project department contacts the salesperson directly (call or email), gets clarification, and corrects the quote. Convert does NOT happen until the data is right.
4. When the quote is correct, the Project department clicks Convert. This action:
   - Creates a Sales Contract record
   - Carries forward the AF Number with the prefix changed (Q → A)
   - Copies all quote fields into the contract
   - Leaves operational fields (stand details, payment schedule, commission rates, catalogue page, scan link) blank for the Project department to fill in over time
   - Triggers the post-signature email automation chain (see 2.3 and 2.7)

This convert gate is not a formal multi-step approval workflow — it is a single action by a single team. But it is the boundary between two organizational halves and must be respected as such by the system.

**The privacy boundary between Sales and Project**

This deserves its own explicit statement because it shapes the default permission model:

- Sales reps see what they need to sell: leads, contacts, companies, products, their quotes, their pipeline.
- By default, sales reps do **not** see commission rates of other reps, internal payment notes, refund records, contract cancellation reasons, project-internal communication, or details from other reps' deals. A salesperson can see their own commission on their own contracts (the deal they closed is theirs to understand), but commission detail across the team is restricted.
- The Project department by default sees everything operational: contracts, payments, expenses, commissions, exhibitor logistics, catalogue data, post-signature operations.
- The Owner sees everything.
- The Sales Manager by default sees what is needed to manage sales — full pipeline visibility for the team — with commission and finance details typically remaining Project + Owner.

These are **defaults**, not categorical rules. The Owner must be able to grant or revoke any of these visibilities for any specific user through the per-user permission matrix described in Part 3.1. The system enforces visibility at the field level (not only the module level) so that a salesperson can read a Sales Contract record they are authorized to see while individual sensitive fields remain hidden.

The principle that drives the defaults: organizational discipline benefits from operational opacity in the sales team. Sales reps focus on selling. They do not need to know whether a deal was profitable after commission, or how much commission another rep earned on a similar deal, or what refund history a customer has. Removing this information from their default view reduces noise, prevents internal politics, and protects the company's commercial leverage in negotiations.

**Must be better than today**

- **Quote subject auto-generation.** Manual typing produces inconsistencies. ELL generates the subject deterministically from the linked records and stores both the auto-generated and an optional manual override.

- **AF Number with office prefix.** Encode useful information in the identifier itself. Q→A transition makes the contract status visible from the number alone.

- **Lead → Contact + Company conversion suggested, not manual.** When a reply identifies a real entity, propose the conversion automatically and let the salesperson confirm with one click.

- **Qualification captured explicitly.** Reply intent, confidence, qualification status, and disqualification reason all become structured data, not memory.

- **Convert gate as a clean handoff.** No salesperson can convert. No project person needs the salesperson's permission. The action is structurally separated and visible to both.

- **Privacy boundary as a configurable default.** A salesperson by default does not see commission across the team, refund history, or project-internal notes — but the Owner can grant any visibility per user. The default protects organizational discipline; the configurability accommodates real exceptions.

- **Quote currency intelligence.** Default by office or country, override always available, currency frozen at quote creation, never changes after.

### 2.3 Sales Contract Management

**What this workflow is about**

Once a quote is converted to a Sales Contract, the deal becomes operational. The work shifts from selling to delivering. The Project department now owns the record and is responsible for everything that happens between conversion and the day the customer walks into the expo: completing missing data, collecting payments, sending the announcement email chain, coordinating stand design, gathering catalogue information, issuing badges, and managing changes.

Sales Contract Management is therefore not a single linear flow — it is a long-running operational record that accumulates information over months. The contract is created mostly empty (only the data carried from the quote) and is filled in piece by piece as exhibitors respond to communications, as payments arrive, and as expo logistics are finalized. The record reflects an ongoing relationship, not a closed transaction.

**Status lifecycle**

A Sales Contract has five possible statuses, each representing a real operational reality:

1. **Active** — the default state for a valid, ongoing contract. (Today called `Valid` in Zoho; ELL renames it for clarity.)

2. **On Hold** — the customer has signaled intent to cancel, but is being persuaded to stay. The Sales Manager or Owner is in active negotiation with the customer. The contract is paused but not cancelled. From here it returns to Active or moves to Cancelled / Transferred.

3. **Transferred Out** — the customer agreed to switch to a different expo instead of the original one. The contract is closed at this expo, and a new contract is created at the destination expo (see Transferred In). Payments and commission carry forward to the new contract.

4. **Transferred In** — a contract that exists because a customer transferred from another expo. It is linked to the original contract via `transferred_from_contract_id`. The cloning is structural: the new contract carries the company, the contact, the payment history, and the commission attribution from the original.

5. **Cancelled** — the customer has finally cancelled. Refund or credit balance is processed (credit is preferred — see 2.6). Commission already paid is deducted from the salesperson's next commission payment (see commission section below).

**Status changes are restricted to the Project department.** Sales reps cannot change a Sales Contract's status. This is a deliberate organizational rule — status changes have financial and operational consequences, and they belong to the team that owns post-signature operations.

**Transfer as a first-class action**

Today, transferring a contract from one expo to another is done by manually changing the source contract's status to Transferred Out, then manually creating a clone at the destination expo and setting it to Transferred In. The two records are linked only by the Project department's mental model. There is no system-enforced relationship between them.

ELL must make Transfer a first-class action: a single button on a contract that asks "transfer to which expo?" and creates the destination contract automatically. The two contracts are linked by `transferred_from_contract_id`, payments and commission carry forward, and reporting can naturally answer "how many contracts at Expo X originated as transfers from other expos?"

The alternative path — cancel the old contract and create a fresh new contract — should remain available for the cases where Transfer is not the right model (e.g., the customer wants different products at the new expo, or the financial terms have changed). The system supports both; the Project department chooses based on the situation.

**The structure of a Sales Contract record**

A Sales Contract is a multi-section record. The data fills in over time, in roughly this order:

**At conversion time (carried from quote):**
- AF Number (with prefix change Q→A)
- Subject (auto-generated)
- Contract Date, Expo Date
- Company, Contact, Country
- Sales Type (Exhibition / Sponsorship)
- Currency, Exchange Rate (frozen)
- Quoted Items (line items with prices)
- Sub Total, Discount, Tax, Adjustment, Grand Total

**Filled by the Project department over time:**
- **Stand details** — Stand Type (Equipped, Space Only, etc.), M², Sales Group (which office is operationally responsible), Free M², Total M², Transportation (Excluded / Included)
- **Catalogue Page** — page number assigned in the printed catalogue
- **Stand Design Link** — Drive URL of the approved stand design
- **Scan Link** — Drive URL of the signed contract document
- **Sales Commission** — final commission amounts after all overrides are decided

**Filled as customer responds:**
- Catalogue form data (via the Catalogue automation flow — see 2.4)
- Stand design feedback / approval
- Visa support requests, travel arrangements, special services

**Filled as payments arrive:**
- Payment schedule (planned vade)
- Payments received (actual collection)
- Payment notes (e.g., "Yerel Ofise Ödendi" — paid to local office)

**Three-tier commission**

Commission is structured around three roles, only one or two of which apply to any given contract:

1. **Agent** — an external partner (an independent expo-marketing agency or a freelance individual) who closed the deal on commission. Agents are not employees and do not log into the system. Their commission is the commercial cost of using external sales channels.

2. **SR (Sales Representative)** — the internal employee who closed the deal directly. The salesperson on the company's payroll.

3. **SD (Sales Director)** — the manager who oversees and supports the SR. The person whose team did the deal. Today this is typically the Sales Manager but can be a Sales Team Lead in larger team structures.

**Only one of Agent vs SR is set per contract**, never both. If an external agency closed the deal, the deal is theirs and there is no internal SR. If an internal salesperson closed the deal, there is no external Agent. SD is set only when the deal was internal (there is an SR) and that SR has a manager who shares in the commission.

This structure must be encoded cleanly in ELL:

```
sales_contracts:
  agent_sales_agent_id  (nullable, FK → sales_agents)
  sr_sales_agent_id     (nullable, FK → sales_agents)
  sd_sales_agent_id     (nullable, FK → sales_agents)
  agent_pct             (nullable, override of default)
  sr_pct                (nullable, override of default)
  sd_pct                (nullable, override of default)
```

**Default + per-contract override**

Each sales agent has a default commission percentage stored on their record (set when they are created or updated). Each Sales Contract has nullable override fields. If the override is set, it wins; if not, the default applies.

The defaults exist for convenience — the Project department doesn't have to look up rates every time. The overrides exist because real life is variable: a slow-selling expo might justify a higher percentage to motivate the salesperson; a strategic deal might warrant a different structure; the Owner sometimes adjusts mid-cycle.

There is no formula. There are no rules. The percentage is a number that the authorized person enters, and the system multiplies by the contract amount to compute the commission. The simplicity is the point.

**Commission paid status**

For each commission entry on a contract, the system tracks:
- Amount due (computed from contract amount × percentage)
- Amount paid to date
- Outstanding amount

Commission payments are recorded as Expense records linked to the contract and the agent. The Owner's reports answer "how much commission did we pay agent X this year" and "how much commission do we owe agent Y still" naturally, by aggregating these expense records.

**Cancellation and commission adjustment**

When a contract is cancelled and the customer is refunded or credited, any commission already paid to the salesperson must be reconciled. The current practice is **deduction from next commission payment**, not clawback:

- The system creates a `commission_adjustment` record: agent X owes Elan Expo Y amount because of contract Z's cancellation
- The next time agent X earns commission on a different contract, the adjustment is netted against it
- If the agent leaves or stops earning, the unrecovered adjustment becomes a write-off

This is an accounting reality the system must support. Sales agents (especially externals) will not return paid commission directly; the only practical recovery mechanism is netting against future earnings.

**Payment management**

Customers pay according to their own preference within the agreed terms. The general practice:
- Roughly 40% at signature (sometimes 30%, sometimes 50% — varies by deal)
- Remaining balance approximately one month before the expo
- 4–5 separate payments is typical; exceptions go higher

The system models this with two related concepts:

1. **Payment Schedule** — the planned installments. A list of expected payments with due dates and amounts. This is the "vade plan" — what the customer agreed to pay and when.

2. **Payments Received** — the actual collections. A list of money that arrived, in the currency it arrived in, with the exchange rate frozen at the day of collection. Each received payment links to the payment schedule entry it satisfies (or partially satisfies).

These are kept separate because they don't always match. A customer may pay in three installments instead of two. They may pay early or late. The system must let the Project department record actual payments without forcing them into a planned-payment shape that doesn't match reality.

**Anti-pattern: do not replicate Zoho's bookkeeping fields**

Zoho contracts today contain fields like `Payment Done ✓` (a manual checkbox to filter unpaid contracts) and `Validity 05/26` (a manual month tag to track first-payment month). These were created by the Owner at a time when Zoho's reporting was limited — they are workarounds, not real business concepts. ELL must NOT replicate them. Instead:

- "Unpaid contracts" = `SUM(payment_schedule.amount) > SUM(payments_received.amount)` — computed, not stored
- "First payment month" = `MIN(payments_received.date)` per contract — computed, not stored
- "Contracts with X month commission cycle" = derived from the actual payment month — computed, not stored

This anti-pattern applies broadly, not just to Sales Contract. For every field in current Zoho usage, ELL must ask: "Is this a real business concept, or is this a workaround for limited reporting?" Real concepts stay. Workarounds become computed queries. (See Part 4.)

**Stand details — when and by whom**

Stand details are completed by the Project department over time, not at conversion. The flow:

1. Convert happens; stand details are blank
2. Project department sends Welcome email (workflow rule: convert + 1 day)
3. Project department sends Stand Design email — "we will deliver your stand like this; please confirm or request changes"
4. Customer responds; Project department records Stand Design Link in the contract
5. Project department sends Catalogue email; customer fills out form; Catalogue record is created
6. Project department fills in Catalogue Page when the printed catalogue layout is finalized
7. Project department fills in Sales Commission once final percentages are settled

This is a long flow that may span 3–9 months. The contract is "alive" during this time — it accumulates information. ELL must support this naturally without forcing a single moment-of-completion.

**Email automation triggered by Sales Contract events**

Sales Contracts are the trigger source for the announcement email chain (see 2.7). The triggers fall into two categories:

**Time-relative-to-contract triggers:**
- Welcome email — convert + 1 day
- Stand Design email — convert + N days (per expo)
- Catalogue email — convert + N days (per expo)

**Time-relative-to-expo triggers:**
- Payment Reminder — expo date − 30 days (per expo, configurable)
- BuildUp Rules — expo date − N days (per expo, configurable)
- Badge — expo date − N days (per expo, configurable)
- Boost / Extra Service / Space Only variants — per expo scheduling

**Configurability is mandatory.** The Owner does not want hardcoded "30 days before expo date" rules. Different expos have different rhythms, different customer cultures, different lead times. The Expos module must hold per-expo timing configuration, and the email automation engine reads from there. New expos inherit a default schedule; the Owner adjusts per expo as needed.

**Must be better than today**

- **Status lifecycle as a structured choice.** Five clear statuses with defined transitions. Transfer becomes a first-class action, not a manual two-step.

- **Three-tier commission cleanly modeled.** No more using SR field for external agencies. Agent / SR / SD are separate FK columns. Defaults + overrides without policy rules.

- **No bookkeeping fields.** Payment Done, Validity, and similar Zoho-era workarounds are deleted. Computed queries replace them.

- **Payment Schedule and Payments Received separated.** Plan vs reality. Both supported, neither forced into the other.

- **Commission adjustments tracked.** Cancellation does not silently zero out commission — it creates an adjustment record that lives until reconciled.

- **Per-expo email timing.** All time-relative triggers read from the Expos module. The Owner configures per expo, never per-contract.

- **Long-running operational view.** A Sales Contract is not a closed transaction; it is an active record. The UI must reflect this — show what's been done, what's outstanding, what's coming up.

### 2.4 Catalogue Production

**What this workflow is about**

An expo catalogue is a designed, printed publication that lists every exhibitor at an expo. It includes each exhibitor's logo, contact information, product photos, brands, stand number, and descriptive paragraph — a directory and a marketing document combined. The catalogue is distributed in three forms: a print run produced by a matbaa (printing house), digital prints, and an online file shared via Drive or web link. It is one of the most visible deliverables of any Elan Expo event.

Today, catalogue production is one of the company's biggest manual workloads. The Project Department Lead has been doing it personally for years using Corel Draw. The flow runs roughly like this:

1. Sales Contract is signed and converted
2. The Project department sends a Catalogue email containing a Zoho form link to the customer
3. The customer fills the form (company info, logos, brands, products, contact)
4. The form data lands in Zoho's Catalogues module
5. The Project Department Lead manually compiles all submissions into a Corel Draw layout, expo by expo, exhibitor by exhibitor
6. The final PDF is exported, sent to the matbaa, uploaded to Drive

Step 5 is the bottleneck. It is hours of manual layout work per expo, multiplied across 10–15 expos per year. ELL's mandate is to **eliminate step 5 entirely**: the Project Department Lead must never open Corel Draw to make a catalogue again.

**The data model**

A catalogue is built from three sources of data:

1. **The Expo record** (LEENA) — expo name, dates, venue, sectors, sponsor logos, cover image, organizer info, country/city
2. **The Sales Contract records** (ELIZA) — list of contracted exhibitors with stand numbers, m², stand types
3. **The Catalogue submission** (LEENA) — exhibitor-provided detail: logo, descriptive paragraph, brands, product images, contact info, social media

The system pulls all three together at generation time. The catalogue is never a static document — it is a render of current data. If an exhibitor updates their information before the deadline, the catalogue regenerates with the new data. If a new exhibitor is added late, they appear in the next regeneration.

**Templates — 3 to 4 master designs, configurable per expo**

The Project Department Lead has identified that the catalogue's overall structure is consistent across expos, with variations in color, design, and cover style. ELL takes advantage of this: LEENA holds **3 to 4 master templates** that cover the full design range. For each expo, the Project department:

- Selects which master template to use
- Customizes per-expo elements: cover image, title styling, primary color palette, sponsor logos, sector headers, font choices

Per-expo customization is meaningful but bounded — it does not require Corel Draw skill or a designer's intervention. A template editor inside LEENA lets the Project department adjust these elements through a UI, preview the result, and save the configuration as the expo's catalogue template binding.

**Exhibitor self-service — the biggest workload reduction**

Today, the customer fills a form and the Project department manages everything afterward. ELL inverts this: the customer manages their own catalogue page, and the Project department only reviews and approves.

The flow becomes:

1. Sales Contract Signed → automated email sent to customer with a unique secure link
2. Customer opens the link, sees their own catalogue page in a web editor
3. Customer uploads logo, writes description, adds product images, lists brands, confirms contact info, picks social media links
4. Customer saves; Project department is notified
5. Project department reviews; if changes are needed, sends a comment back; otherwise approves
6. The exhibitor's page is now part of the live catalogue
7. The customer can return to the link and edit until the catalogue deadline (per expo, configurable in the Expos module)
8. After the deadline, the page is locked; only the Project department can make changes

This pattern is known and proven at hundreds of B2B platforms. The customer wants control over their own listing, the company saves enormous coordination cost, and the data is naturally fresher and more accurate than when relayed through email.

**Output formats — PDF and web, from the same source**

ELL produces the catalogue in two forms simultaneously, from the same underlying data:

1. **Print-quality PDF** — for matbaa production, digital printing, and Drive distribution. Generated by the templating engine in print resolution, with proper bleeds, color profiles, and embedded fonts. The Project Department Lead clicks one button; the system produces the file.

2. **Web catalogue** — a public URL per expo (e.g., `catalogue.elan-expo.com/mega-clima-2025`). Mobile-friendly, searchable, scrollable. Each exhibitor has a permalink to their page. Visitors and exhibitors share these links; search engines index them; the catalogue becomes a marketing asset for both Elan Expo and the exhibitors themselves.

The two outputs share a single data source and a single template configuration. The Project department doesn't maintain a print version and a web version separately — they are two renders of the same content.

**The deadline and the lock**

Every expo has a catalogue deadline, configured in the Expos module. The deadline is a real operational concern: the matbaa needs the print file by a specific date, and exhibitors who haven't filled their information by then must either be chased aggressively or excluded.

Before the deadline, exhibitors can edit freely. After the deadline, their pages are locked. The Project department can override the lock for individual exhibitors (a customer who paid late and needs catalogue inclusion despite missing the deadline) but the default is a hard close. The system surfaces the deadline visibly: in the customer's editor, in reminder emails leading up to it, and in the Project department's dashboard ("12 exhibitors haven't completed their catalogue page; deadline in 5 days").

**What's stored, what's regenerated**

The catalogue data lives in LEENA as structured records:

- `expo.catalogue_template_id` — which master template
- `expo.catalogue_customization` — per-expo color/font/cover/sponsor configuration
- `expo.catalogue_deadline` — the lock date
- `catalogue_submission` records — one per exhibitor, with their content and editor history

The PDF and web outputs are **regenerated on demand**, not stored as fixed artifacts (other than the final approved file kept for archive). This means the catalogue is always current, and historical versions are reproducible from the data state at any point in time.

**Must be better than today**

- **No more Corel Draw.** The Project Department Lead never manually composes a catalogue. Template selection + per-expo customization + automatic generation replaces the entire layout workflow.

- **Exhibitor self-service.** Customers manage their own pages. Project department reviews and approves; doesn't do data entry.

- **Web + PDF from one source.** Single data model, two renders. No duplicate maintenance.

- **Per-expo deadline as a system concept.** Not a date in someone's head — a field on the Expo record, surfaced in dashboards and reminder emails.

- **Regeneration on demand.** A new exhibitor signs late; the catalogue updates with one click. An exhibitor fixes a typo; the next regeneration carries the fix. The catalogue is never frozen until the deadline locks the data sources.

- **Searchable, shareable web catalogue.** Becomes a marketing asset, not just a print deliverable. Exhibitors share their permalinks; search engines bring traffic; visitors browse on mobile.

- **Audit trail.** Who edited what, when. The Project department sees the history of every submission. Disputes (a customer claims they uploaded the wrong logo) are resolvable from the audit log.

### 2.5 Expo Operations Management

**What this workflow is about**

An expo at Elan Expo is not a single event — it is a long-running operational project that begins months before the doors open and continues weeks after they close. Expo Operations Management is the workflow that holds everything together: the expo as a master record, the partners contracted to deliver services, the floor plan that organizes physical space, the visitors who attend, the check-in process at the door, and the post-show analytics that close the loop.

This workflow lives almost entirely in LEENA. The Project department is the primary owner. Sales has no role here — once Sales Contracts are converted, the deal is operational and belongs to Project. The system must reflect this organizational reality: LEENA is where Project does its daily work.

Some pieces of this workflow already exist in production today. Floor Plan Builder is operational with 12 endpoints, cell-based stand management, version control, and stand assignment. Visitor management handles registration, QR code generation, badge printing, and check-in via terminal scanning. These are referenced here for completeness, but the focus of this section is on what is missing or must change.

**The expo master record**

An expo is created once, then enriched over months. The master record holds:

**Identity:**
- Expo name (e.g., "Mega Clima Nigeria 2026")
- Edition / year (allows yearly clones — see ELL Glossary)
- Sectors covered (HVAC, Construction, etc. — multi-select)
- Country, city, venue
- Start date, end date

**Build-up & breakdown timing:**
- BuildUp Day 1 (date when special-design stand construction begins)
- BuildUp Day 2 (continuation day)
- Standard stand build-up day
- Show open hours (typically 10:00–17:00 first three days, 10:00–16:00 final day)
- Breakdown date / time

**Deadlines:**
- Catalogue submission deadline
- Stand design confirmation deadline
- Payment final deadline
- Visa support request deadline
- Each deadline is a real date that drives operational pressure and customer-facing communication

**Operation Team contacts (who customers reach):**
- Istanbul HQ contact (FK → users) — the central point of contact
- Local on-site contact (FK → users) — the person at the venue
- These are not internal assignments; they are contact details given to exhibitors so they know who to call

**Online registration & form URLs:**
- Catalogue form URL (where exhibitors submit catalogue content)
- Stand design form URL
- Visitor pre-registration form URL
- Today these live in Zoho Forms; in ELL they will be auto-generated by LEENA per expo

**Partners (see next section)**

The expo record is created when a new edition is opened (could be cloning a previous edition's structure, see Floor Plan Builder's existing clone workflow). The Project department fills in the master fields over weeks, partners are added as agreements are signed, and the record stays alive throughout the operational cycle.

**Co-located expos — the cluster reality**

A frequent operational pattern at Elan Expo is **co-located expos**: two or more expos held in the same venue, on the same dates, sharing operational infrastructure but maintaining separate exhibitor lists and contracts. A typical example: Mega Clima Nigeria 2026 (the main expo) co-located with Water Expo Nigeria 2026 (a smaller satellite expo benefiting from the same visitor profile).

The two expos are operationally one event but commercially two:

- **Operationally one:** Same venue, same hall (often), same build-up dates, same operation team, same partners (stand contractor, hostess agency, catering), same security, same opening hours, often a single visitor entrance with shared check-in.
- **Commercially two:** Separate exhibitor lists, separate Sales Contracts, separate sectors of focus, separate catalogues (or sometimes a combined catalogue — Project department's choice).
- **Financially one for the Owner:** All revenues and expenses pool together in the Owner's view, because operationally it's a single deployment of resources. ELIZA already implements this through the **expo_clusters** concept (auto-detected by country + month, with manual override).

The system must reflect this duality:

- Two expo records exist (Mega Clima Nigeria 2026 and Water Expo Nigeria 2026), each with its own contracts, exhibitors, catalogue settings, and email automation
- A cluster record links them (`expo_clusters` table — already exists in ELIZA)
- Operation team partners can be shared across the cluster: when adding a stand contractor to one expo, the system offers to copy it to the cluster siblings
- Floor plan can be shared (single hall with both expos' stands) or separate (two hall layouts plus a combined view) — the Floor Plan Builder must support both modes
- Financial reporting rolls up at the cluster level by default for the Owner; per-expo detail is available
- Visitor registration is per-expo nominally, but in practice 80% of visitors register only for the main expo and gain access to both. The system must not force a duplicate registration burden on visitors.

**Cluster lifecycle:** A satellite expo (e.g., Water Expo) typically starts as a co-located addition to a larger expo (Mega Clima). Over time, if the satellite reaches its own break-even point — fills its share of the hall, has enough exhibitors to justify its own operation — the Owner separates it: future editions are scheduled at different dates, in their own venue, and the cluster relationship dissolves. The system must support this transition gracefully (a `cluster_id` field that can be null after separation; historical records preserved).



Each expo contracts with several outsourced service providers. The exact partners vary per expo and per country: a Nigeria expo may have a different stand contractor than a Morocco expo, and a small expo may not have a separate hostess agency at all. The system must support this flexibility.

ELL models partners as a separate table linked to expos:

```
expo_partners:
  expo_id           (FK → expos)
  partner_role      ENUM('stand_contractor', 'travel', 'visa', 'forwarder', 
                         'hostess', 'catering', 'security', 'venue_authority', 'other')
  company_name      VARCHAR
  contact_name      VARCHAR
  phone             VARCHAR
  email             VARCHAR
  notes             TEXT
  is_primary        BOOLEAN  -- if multiple partners in same role, which is primary
```

The Project department adds partners to an expo as agreements are made. An expo may have zero, one, or multiple partners in a given role. A primary flag identifies which one to feature in customer-facing communications.

**The purpose of partner data: customer-facing communication.** When a Sales Contract is converted, the exhibitor receives a Welcome email that includes contact details for the partners they may need to work with: stand contractor for special designs, travel agency for hotel/flights, visa company for invitation letters, freight forwarder for shipping. The partner data is pulled into emails dynamically:

```
Stand Contractor: {expo.partners.stand_contractor.company_name}
Contact: {expo.partners.stand_contractor.contact_name}
Phone: {expo.partners.stand_contractor.phone}
Email: {expo.partners.stand_contractor.email}
```

This is the same dynamic-data pattern as everywhere else: one email template, expo-specific data injected at send time. (See 2.7.)

**Visibility:** Partner data is visible to Project + Owner by default, with read access optionally extended to Sales for context. The data is not commercially sensitive — sales reps wouldn't usually need it, but seeing it doesn't harm.

**Floor Plan Builder — current state, future enhancements**

The Floor Plan Builder is operational in LEENA today. It supports:

- Hall-based grid layout (configurable grid dimensions, 1m² cells)
- Cell-based stand creation (rectangular marquee selection)
- Stand attributes: code, m², company, status (available / reserved / sold), color, notes
- Special area types (VIP, conference, registration, entrance, exit, technical)
- Version control: Draft → Active → Archived (only one Active per hall)
- Stand split / merge / clone operations
- Plan cloning for new editions (physical layout copied, assignments cleared)
- Background image overlay (reference architectural drawings)
- 10-color pastel palette, custom colors per stand

**Phase 2 enhancement — Sales Floorplan Templates (per ADR-010):**

The Project department creates a Sales Template from the Master Floor Plan. Sales reps clone this template into their own per-prospect versions, modifying them freely (e.g., placing competitor logos to create urgency, customizing for proposal emails). This dual-layer approach is decided but not yet implemented.

**Phase 2 enhancement — Sales Contract → Stand auto-link:**

When a Sales Contract is signed and stand details are entered (Total M², Stand Type), the system suggests available stands matching the criteria. The Project department confirms the assignment, and the floor plan automatically reflects the new occupant. Today this is manual; in ELL it becomes a coordinated handshake between Sales Contract data and Floor Plan state.

**Phase 2 enhancement — Server-side branded PDF export:**

Today the floor plan renders in-browser via Konva.js. Phase 2 adds server-side PDF generation with Elan Expo branding (logo, color palette, expo metadata). This becomes a print-ready deliverable for venue authorities, marketing, and exhibitor communications.

**Visitor management — current state**

LEENA's visitor management is operational and feature-rich today:

- Single `visitors` table holds visitor, exhibitor, conference attendee, VIP, press, staff, and speaker records (distinguished by `visitor_type`)
- Public registration form with custom fields per expo
- Email confirmation with QR code via SendGrid (handled by background email_worker with FOR UPDATE SKIP LOCKED concurrency safety)
- Manual registration via QR scanner interface
- Excel import with upsert (preserves existing QR codes when updating)
- Conference topic registration with multi-topic support (`||` separator)
- Re-activation campaigns (invite past visitors of one expo to register for another)
- Conference certificate generation and email delivery

**Visitor management — gaps to close**

- **B2B matchmaking:** Match visitor sectoral interests with exhibitor product categories; suggest "visit these stands" pre-show. Requires structured exhibitor catalogue data (see 2.4) and visitor interest tagging at registration.
- **Personalized visitor portal:** A visitor self-service area where they can save favorite exhibitors, build their visit schedule, see appointments, and access their badge.
- **Mobile-friendly badge:** Today badges print from a popup; visitors should also have a mobile-accessible digital badge with the QR code embedded.
- **Pre-show appointment booking:** Visitors book meetings with exhibitors before the expo via the platform. This requires exhibitor availability calendars and matching logic.

These are roadmap items, not Phase 1 requirements. Listed here so the requirements document captures the full long-term picture.

**Check-in operations — current state**

Check-in is operational. Terminal devices at the venue scan visitor QR codes, log entries with timestamps, and trigger badge printing. The system handles:

- Multi-terminal setup per expo
- Email lookup as a fallback (visitor lost their QR / never received it)
- Per-hall and per-terminal check-in tracking
- Real-time check-in dashboard with hourly trends
- Lead scanner mode for exhibitors (exhibitor scans visitor QR to capture leads at their stand)
- CSV export of all check-in data

**Check-in — gaps to close**

- **Push notifications:** Send messages to checked-in visitors during the expo (seminar starts in 10 minutes, VIP lounge open, sponsor message). Could be a sponsorship revenue source.
- **Visitor flow analytics:** Heat-map of which areas of the floor plan have the most visitor flow. Combines floor plan data with check-in zone data.
- **Late-registration handling:** Visitors who arrive without pre-registration should be able to register on-site via tablet/kiosk and receive an instant badge.

**Post-show analytics**

After an expo closes, the data accumulated during the cycle becomes business intelligence. The Project department uses this to evaluate the expo's performance, the Owner uses it for strategic decisions, and exhibitors expect summary reports as part of their participation.

Per-expo analytics required:

**Visitor metrics (LEENA):**
- Total visitors registered, total visitors checked in, conversion ratio
- Visitor breakdown by sector, country, job title, visitor_type
- Daily check-in trend (hourly granularity for opening day)
- Hall-level traffic distribution
- Conference session attendance and certificate issuance rates
- Re-activation campaign effectiveness (past attendees who returned)

**Exhibitor metrics (cross-system):**
- Total exhibitors signed (from ELIZA Sales Contracts)
- Stand occupancy by m² range (small / medium / large)
- Lead capture per exhibitor (from Lead Scanner usage in LEENA)
- Catalogue submission rate (how many exhibitors completed their catalogue page)
- Stand contractor utilization (which exhibitors used the official partner vs. their own)

**Financial metrics (ELIZA):**
- Total expo revenue (Sales Contract amounts)
- Total expo expenses (multi-account ledger filtered by expo_id)
- Net margin per expo
- Commission paid per expo
- Outstanding receivables at expo close

**Operational metrics (cross-system):**
- Pre-show timeline adherence (catalogue deadline met? stand design confirmed on time?)
- Email automation effectiveness (open rates, response rates per email type)
- Customer service load (number of exhibitor inquiries handled, response times)

**Where this lives architecturally:**

- LEENA holds raw operational data (visitors, check-ins, catalogues, floor plan state)
- ELIZA holds raw financial data (Sales Contracts, payments, expenses, commissions)
- ELIZA's Intelligence layer pulls cross-system data via API and presents the integrated post-show report
- The Project department views per-expo summaries in LEENA; the Owner views strategic comparisons across expos in ELIZA's War Room

**Exhibitor data ownership — clarified**

This is a question the requirements document must settle clearly. The reality:

- An "exhibitor" is defined by a signed Sales Contract — Sales Contract → Company → Exhibitor at this expo
- Sales Contract data is owned by ELIZA (per ADR-005)
- Therefore: ELIZA is the source of truth for "who is an exhibitor at expo X"
- LEENA reads this list via API to power: catalogue page generation (2.4), floor plan stand assignment, badge printing for exhibitor staff, lead scanner authorization

The exhibitor record itself does not need to exist as a separate entity. It is a query: "all companies with a non-cancelled Sales Contract for this expo." LEENA caches this list locally and refreshes it via API on relevant events (new contract, contract cancellation, contract transfer).

**Multi-expo coordination**

A single Project department manages multiple expos in parallel. Two patterns are common:

**Pattern 1 — Co-located clusters:** Two or three expos at the same venue on the same dates (see "Co-located expos" section above). Operationally these are managed as one event but tracked as separate commercial records.

**Pattern 2 — Sequential expos in parallel preparation:** A Nigeria expo in build-up phase (3 weeks out), a Morocco expo in announcement phase (8 weeks out), a Kenya expo just starting sales (6 months out). Each is at a different stage of the operational cycle and demands different attention.

The system must support both patterns naturally:

- The Project department's home page shows all active expos with status indicators (sales pace, catalogue completion, payment collection, time-to-show)
- Co-located clusters render as grouped rows so the operational unity is visible at a glance
- Cross-expo navigation is fluid — switching from one expo's catalogue review to another's check-in dashboard requires no context loss
- Filters are sticky per user (the Nigeria local office sees Nigeria expos by default but can switch)
- Notifications include expo context ("Stand design confirmation overdue for [Company] at Mega Clima Nigeria 2026")
- Cluster-level rollups available where they matter: financial summary, operational readiness, visitor totals

**Must be better than today**

- **Expo as a single living record.** Master fields, deadlines, partners, floor plan, visitor data, financial summary — all accessible from one expo page. No more clicking between Zoho modules to assemble the picture.

- **Partner data structured, not freeform.** No more text-field guessing. Partners are typed records with consistent fields, queryable across expos ("which expos use Stand Contractor X?").

- **Email content from expo data, naturally.** No more `${Lookup:Expo Name.Travel Contact}` syntax workarounds — the email template references `expo.partners.travel.contact` directly. The mechanism is the database, not a lookup engine.

- **Floor plan integrated with sales reality.** Sales Contract signed → stand assignment suggested → floor plan updated. No more parallel manual updates in two places.

- **Catalogue and operations linked.** Catalogue submission rate and stand design confirmation rate visible alongside the expo's countdown timer. The Project department sees what's at risk in time to act.

- **Post-show report that writes itself.** Cross-system analytics assembled automatically. The Project department reviews and adds narrative context, but doesn't manually compile data from three places.

- **Multi-expo dashboard.** A working day for the Project Department Lead might touch four expos. The system shows them all at once, prioritized by what needs attention today.

- **Co-located clusters as a first-class concept.** Two expos at the same venue on the same dates are recognized as a cluster — operational data shared by default, commercial data separate. No more managing them as if they were unrelated. ELIZA's existing cluster auto-detection (country + month) extends to LEENA's operational view, with manual override available.

### 2.6 Financial Operations (Multi-Account, Multi-Currency)

**What this workflow is about**

Financial operations is the connective tissue of Elan Expo. Every other workflow eventually expresses itself as money: a Sales Contract becomes Revenue, an expo's logistics become Expenses, a sales agent's deal becomes a Commission, a cancelled contract becomes a Credit Balance, an Owner's intervention becomes a personal-to-company transfer. The financial layer must absorb all of these without flattening them into a single shape, and it must remain comprehensible to a non-accountant Owner who needs to know — at any moment — where money is, where it came from, where it went, and whether the company is on track.

The financial reality of Elan Expo is unusual in several specific ways. The company operates across multiple offices with their own bank accounts in their own currencies. The same expo may have its revenues collected in three currencies and its expenses paid in two more. The Owner sometimes pays for things personally and is owed back by the company. Subsidies move between offices in both directions. Black-market exchange rates differ from official ones in some markets. Cancellations usually become credit balances rather than refunds. Commissions are negotiated per contract, not formula-driven. None of this fits a clean textbook accounting model. The system must reflect operational reality, not impose textbook structure on top of it.

This workflow defines what the financial layer needs to track, how it needs to behave, and how it must be reported — without taking a position on which subsystem owns which table. Implementation arrangement comes later.

**Multi-account ledger**

Elan Expo maintains many accounts. Each office has at least one bank account, often in multiple currencies. There is a cash account at HQ for the Owner's hand-paid expenses. New offices open new accounts; existing offices may add USD or GBP holdings as the business demands. The list is not fixed.

The system must hold an editable list of accounts, where each account has a name, a currency, an office it belongs to (when applicable), and a type that distinguishes bank accounts from cash holdings from any virtual accounts that exist for organizational reasons (a current account against the Owner, for example — see below). The Owner manages this list through an admin UI. There are no hard-coded accounts; if Kenya opens a USD account tomorrow or the Owner needs a GBP holding next year, it is added through the same screen used for any other account.

Each account holds a running balance in its native currency, computed from the transactions associated with it. There is no separate "opening balance" field — historical Zoho transactions are imported in full, and the balance at any point in time is the sum of those transactions to that date. This is the same principle as everywhere else in the document: real business state is a query over real events, not a denormalized field that can drift out of sync.

**Every money movement is two-sided**

This is the central financial principle, and it is the principle most violated by the current Zoho setup.

When HQ sends a subsidy of €5,000 to the Nigeria office, two things happen in reality: HQ's EUR account decreases by €5,000, and Nigeria's account increases by the equivalent in NGN (or in EUR if the office holds a EUR account). Today, Zoho records only one side — usually the receiving side, as a Revenue at the Nigeria office — which is incorrect both as accounting and as reporting. HQ's outflow is invisible. The "where did the money go?" question cannot be answered from the records alone.

ELL must enforce the two-sided principle: every transfer between accounts produces both an outflow and an inflow, linked to each other as one logical event. This applies to:

- HQ subsidising a local office (HQ outflow + local office inflow)
- A local office remitting collected funds back to HQ (local outflow + HQ inflow)
- The Owner paying for something out of personal funds (personal-account outflow + the relevant expense being paid + a corresponding entry on the Owner's current account against the company — the company now owes the Owner)
- The Owner withdrawing from the company to personal funds (company outflow + reduction of the Owner's current-account balance)
- A revenue collected as cash at a local office that later becomes a deposit into the local bank account (cash account outflow + bank account inflow)

The shape of the data is one transfer event with both an `from_account` and a `to_account`, or two linked transactions that the system treats as a single operational event. The implementation choice is not made here. The need is: no money movement is one-sided; every movement appears in both places it touched.

This need has direct consequences for how reporting works. A statement of any account is a complete history of inflows and outflows, with the counterparty visible on each line. A reconciliation between two accounts is a query, not an exercise in finding the matching record.

**The Owner's current account against the company**

The Owner of Elan Expo regularly pays for company expenses out of personal funds. This is not a small or occasional pattern — it is a recurring operational reality. Today these payments largely disappear from the records: the Owner spends the money, the company benefits, and there is no trace except in the Owner's memory. This is a problem of accounting hygiene, but more importantly it is a problem of fairness — the company genuinely owes the Owner for these payments, and the obligation should be visible.

The system must support a dedicated account that represents the Owner's claim on the company (the Owner's current account, in accounting terms). When the Owner pays €1,200 in cash for an expo's local hostess agency, the transaction records an Expense at the expo with payment method "Owner cash" and a corresponding inflow on the Owner's current account — the company now owes the Owner €1,200. When the company later reimburses the Owner from a corporate account, that reimbursement is a transfer from the corporate account out, decrementing the current-account balance toward zero.

The Owner can see at any moment what the company owes them — or what they owe the company, if the balance has gone the other way. This visibility is one of the bigger improvements ELL must deliver over Zoho.

The same pattern can extend to other people who informally lend or owe (a country manager paying out of pocket for an emergency expense, for instance), but the Owner's current account is the primary case.

The exact mechanism by which an Owner-paid expense is recorded — whether the Expense's account directly references the Owner's current account, or whether the Expense uses a designated "Owner cash" payment method that triggers a paired transfer to the current account — is not settled here. Both produce the same end state (the company's debt to the Owner increases by the expense amount). The choice between them is an architectural decision for the implementation phase. The need is that the debt is captured automatically when the expense is recorded, without the Owner or anyone else having to remember to make a separate entry.

**Currencies, exchange rates, and EUR consolidation**

Elan Expo reports its consolidated position in EUR. Individual transactions happen in many currencies. The bridge between the two is the exchange rate, and exchange rates are handled with great care because the alternatives are worse than they appear.

Each non-EUR transaction (Expense, Revenue, or transfer) carries its own exchange rate, entered by the person recording the transaction at the moment of entry. The rate is frozen with the transaction. It is never retroactively changed, even if the official rate or the actual rate moves later. The reasons for this are operational, not theoretical:

- Black-market and parallel-market rates are real in several of Elan Expo's markets. The official rate published by central banks differs from the rate that actually moved the money. The user knows the real rate; the system records what the user knows.
- A retroactively adjusted exchange rate would silently change historical EUR-equivalent figures, which corrupts every financial report ever generated against that data. Audit becomes impossible.
- A daily-rate-table approach was considered and rejected. It cannot account for black-market rates, it can be late or wrong, and it pushes the responsibility for "what rate actually moved this money" away from the human who knew the answer.

The EUR-equivalent of a transaction is a derived value, computed at entry time and stored alongside the original-currency amount, so reports do not need to recompute it on every read. When EUR is the transaction currency, the rate is 1.0 and no conversion happens.

Currency Exchange Gain and Loss are categories that exist in the reference data today, but the company does not currently maintain accounting tight enough to track them as real transactions. They are placeholders for a future capability rather than an active operational concept. The system may record them when the company's financial discipline reaches the point where they can be meaningful; for now, no workflow depends on them.

**Expenses and revenues — the core financial entities**

Every monetary event at Elan Expo is one of two things: an Expense (money the company paid out) or a Revenue (money the company received). The list of categories distinguishes them at a more useful level.

Expenses are categorized in a two-level hierarchy: a Category (Office Expenses, Operation Costs, Pre-Event Costs, Sales Costs, Marketing Costs, Conference Costs) containing many Types (Salaries/Wages, Hall Rent, Stand Construction, Flight Tickets, Catering, and so on — currently 75 types across the six categories). The hierarchy is reference data, editable by the Owner. New types can be added without code changes; obsolete types can be retired. The Categories are stable but not immutable; the Owner can add a new Category if a genuinely new kind of expense appears.

Revenues use a flat list of Categories — Expo Participation, Sponsorship Income, Stand Construction, Extra Stand Materials, Electricity, Ticket Sales, B2B Service Fee, Advertising Fee, Consultancy Income, Local Service Fee, Partner Commission Income, Currency Exchange Gain, Advance from Head Office, Advance from Partners, Other Income — plus an Income Description sub-field for free-text annotation when the category alone does not capture the specific source. Categories are reference data; descriptions are entered case by case.

Each Expense and each Revenue carries the same essential structure: an originating expo (nullable — null means overhead, set means expo-specific), a category and type, an amount in original currency with the frozen exchange rate and the EUR equivalent, the account the money moved through, the payee or payer, the payment date and method, free-text notes, the user who created the record, and — for Revenues attributed to a contract — a contract reference.

A Revenue without a Sales Contract reference is unusual but possible (sponsorship deals not yet structured as contracts, miscellaneous income). A Revenue with a contract reference is the normal case for exhibition fees: the contract sets the obligation, the Revenue records the actual collection.

**Revenue records: one per payment, contract-attributed**

A Sales Contract represents an agreed obligation. Revenue records represent actual collection events. The two are related but distinct, and the relationship is many-to-one: a single contract usually produces multiple Revenue records, one per installment received.

This decision matters because today's practice is inconsistent — sometimes one Revenue with multiple installments inside it, sometimes a separate Revenue per installment. The inconsistency makes reporting unreliable. ELL standardises on one model: **each actual payment event is one Revenue record**, attributed to the originating contract.

When the customer pays the first installment, one Revenue record is created. When the second installment arrives, a second Revenue record is created. The contract's "total received" is the sum of its associated Revenue records, computed on demand — the contract itself does not store a denormalized "received amount" field that could drift out of sync. The contract record carries the planned schedule (the agreed installment plan); the Revenue records carry what actually happened.

This separation matches accounting reality and matches how the company's finances work in practice. Per-payment fields — date, payment method, account that received the payment, exchange rate at the moment of receipt, notes about who paid and how — are natural to capture because each payment is its own record. Reports about "what came in this week" or "which payments are still outstanding" are queries against the Revenue stream, not subform-spelunking inside contracts.

The Sales Contract's installment plan (the agreed vade) is a separate piece of data, distinct from Revenue records. The plan describes intent; Revenue records describe reality. Reports compare the two ("contract X has €40,000 planned by Aug 15, has received €25,000 across two payments — outstanding €15,000"). The comparison is a query, not a stored field.

**Third-party payers**

A real and recurring case: the company that signed the contract is not always the company that pays. An exhibitor in Nigeria may arrange for their Turkish partner company to pay the invoice from Turkey because international transfer is easier from there. Another exhibitor may have an agent who pays on their behalf. The contract belongs to the exhibitor; the money comes from a different entity.

Each Revenue record carries a `payer` field that is independent of the contract's company. By default the payer is the contract's company; when a third party pays, the payer is recorded as that third party (a company that may or may not have its own record in the system). The system supports issuing a proforma invoice to the actual payer when needed, separate from the contract's exhibitor identity.

This separation matters for accounting (the receipt is issued to the payer, not the exhibitor), for audit (the trail of who actually moved the money is preserved), and for relationship continuity (the exhibitor's contract history is not corrupted by who happened to fund a particular installment).

**Budgeted vs actual at the expo level**

The Owner runs the company against budgets, expo by expo. Before an expo's sales open, an expected expense profile is laid out — venue rent estimated, stand construction estimated, marketing budget allocated, conference costs anticipated — and a target revenue level is set. As the expo progresses, actual expenses accumulate against those budgets and actual revenues come in against the target.

The system holds budgeted figures alongside actuals. Each expo has a budget — a list of category/type rows, each with a budgeted amount, currency, and notes. The actuals come from the Expense records linked to the same expo and category/type. The variance is a query: budgeted minus actual, per category, per expo, in EUR.

The budget is not a single number per expo. It is a structured plan that mirrors the expense category structure. "Mega Clima Nigeria 2026 budget" is not "€100,000 total"; it is "€35,000 hall rent, €18,000 stand construction, €12,000 catering, €25,000 marketing breakdown, …". The variance reports become specific: the expo came in €5,000 under on stand construction but €3,000 over on catering. This is the conversation the Owner needs to have, not a single bottom-line number.

Budgeted figures may need to be updated as plans firm up. The system supports edits to the budget but preserves the change history, so a question like "when did the marketing budget for this expo expand?" can be answered.

**Expo attribution — a single expo per transaction**

Every Expense and every Revenue is either expo-specific or general (overhead). The expo attribution field on each record is nullable: when null, the expense is overhead (HQ rent, salaries, general office supplies); when set, the expense belongs to a specific expo and contributes to that expo's profitability calculation.

For co-located clusters, each transaction still attributes to one expo, not to a cluster. The cluster's financial picture is a query that sums across the cluster's member expos. This keeps the data normal and the reporting flexible — the same transaction can roll up to per-expo reports, per-cluster reports, per-country reports, per-office reports, per-year reports, all from the same primary attribution.

When an expense cannot be cleanly attributed to a single expo because it serves several at once (a regional marketing campaign covering Nigeria expos broadly, for instance), the operational practice is to attribute it to the largest beneficiary. This is good enough for the company's needs and avoids the complexity of split-attribution. If a more precise attribution becomes important in the future, it can be added — but it is not a requirement today.

**Sales commission as a financial flow**

Commission is set on the Sales Contract (see 2.3) but only becomes financial reality when it is paid. The payment of a commission is an Expense — category Sales Costs, type Agent Sales Commission or HQ Sales Commission or Local Sales Commission depending on who is being paid. The Expense is linked to the originating Sales Contract via the same contract reference that Revenues use, so the commission is traceable to the deal that produced it.

The commission Expense is a normal Expense in every other respect: it has an account it was paid from, a payment date, a payment method, a currency, an exchange rate. The fact that it originated from a contract's commission calculation is metadata, not a separate accounting concept.

Commission adjustments — the situation where an agent owes the company because a contract was cancelled after commission was paid — are not Expenses. They are a balance carried on the agent's record, deducted from the next commission Expense paid to that agent. The deduction shows on the next commission Expense as a line item: commission earned minus prior adjustment equals net paid. This is the operationally cleanest way to handle the rare but real case where the company is owed money back from an agent.

**Refund and credit balance — flows, not stored fields**

When a contract is cancelled, the customer's already-paid amount has to go somewhere. The Project department's choice — credit toward a future expo, or refund out of the original receiving account — is recorded on the contract, but the financial effect is captured as transactions in the same stream as everything else.

A refund is a real outflow: a negative-direction movement from the account that originally received the payment, in the currency that originally received it (or in another currency the customer prefers, with the appropriate frozen exchange rate). The refund is linked to the originating Revenue records so the path "this money came in, this money went back out" is auditable.

A credit balance is not a stored field on the company record. It is a computed value, derived from the same kind of event stream that account balances use: cancellation events that allocated paid amounts as credit produce credit-allocation entries against the company; future contracts that consumed credit produce credit-consumption entries; the company's current credit balance is the net of those entries on demand. This means a question like "how much credit does this company carry across all expos?" is a query, not a field that someone has to remember to update. It also means that consuming credit on a new contract does not require a manual reconciliation — the new contract's payment schedule simply records that credit-X was applied as the first payment, and the company's outstanding credit decreases accordingly in the next computation.

The same principle applies to commission adjustments described above and to the Owner's current account: real business state is the sum of real events, not a denormalized number.

**Cash flow and account statements**

The Owner needs to be able to look at any account and see its complete history: every movement in, every movement out, the running balance after each. The HQ EUR account, the Nigeria NGN account, the Owner's current account, the cash account — each is a stream of inflows and outflows, and each should be readable as such.

This is what is missing from the current Zoho setup. Reports today are organized around modules (Revenues, Expenses) rather than around accounts. To answer "what happened in the Nigeria account in March?" the Owner has to filter Revenues by country and Expenses by office and try to interleave them mentally. ELL must provide the natural account-statement view, where every account is queryable as a single ordered stream.

Beyond per-account statements, the Owner needs cross-account views: total cash position across all accounts in EUR equivalent, current outstanding receivables from all active contracts, current commissions owed to all agents, current Owner-current-account balance. These are queries, not new tables — but they need to be one click, not assembled by hand.

**Must be better than today**

- **Every money movement is two-sided.** No more silent transfers where the outflow disappears. Every movement between accounts produces matching outflow and inflow records, linked as one logical event. The full path of any euro through the company is visible.

- **The Owner's current account against the company is real.** When the Owner pays for something out of personal funds, the company's debt to the Owner is recorded, visible, and reconciled when reimbursement happens. No more invisible subsidies from the Owner's personal pocket to the company's operations.

- **Account-centric reporting becomes natural.** Statements per account, balances at any historical date, reconciliation between accounts — all queries against a clean transaction stream. Today this requires assembling data from multiple Zoho modules; in ELL it is one screen.

- **Frozen exchange rates with full traceability.** The rate that actually moved the money is captured at entry time and never silently changed. Black-market and parallel rates are first-class. Every EUR-equivalent figure in every report can be traced back to the rate it was computed at and the human who entered it.

- **Budget vs actual per expo, per category.** Variance reports answer real questions ("this expo's stand construction came in 14% under budget; what changed?"). The Owner runs expo profitability against plan, not against memory.

- **One Revenue record per actual payment, contract-linked.** No duplicate sources of payment data, no inconsistency between contracts that record installments inside one Revenue and contracts that record each installment separately. Every payment event is its own record. The contract's outstanding balance is computed from its Revenue records, never maintained as a separate field that can desync.

- **Cancellation, refund, and credit handled as event flows.** Credit balances are not stored fields that drift out of sync — they are computed from the cancellation events that created them and the future contracts that consumed them. Refunds are real outflows linked to the original receiving account. The choice between credit and refund is a Project department decision recorded on the cancelled contract. Both produce auditable money paths.

- **Commission paid is an Expense linked to its contract.** Commission flows are traceable from "this deal closed" to "this agent was paid". Adjustments for cancelled deals are netted on the next payment, not invisibly reconciled.

- **Reference data the Owner controls.** Expense categories, expense types, revenue categories, payment methods, accounts — all editable by the Owner without involving engineering. New offices, new currencies, new expense types are operational changes, not code changes.

- **Historical Zoho data carries forward intact.** Every Expense, Revenue, and (where reconstructable) transfer in Zoho is imported into ELL. Account balances at launch are the sum of historical records, not a separately-entered opening figure. The migration date is invisible in reports — the financial history is continuous.

- **Multi-currency consolidation that respects reality.** The EUR view is the consolidated executive picture; the original currency view is the operational truth. Both are always available, neither obscures the other, and the bridge between them is auditable to the transaction.

### 2.7 Communication Automation

**What this workflow is about**

A trade exhibition is sold once and operated for months. Between the moment a contract is signed and the day the exhibitor walks into the venue, dozens of structured communications need to happen: welcoming the exhibitor, requesting catalogue submissions, confirming stand designs, reminding about payments, sending build-up rules, issuing badges. Multiply this by ten to fifteen expos per year, hundreds of exhibitors per expo, and several languages, and the volume becomes unmanageable by hand.

Communication Automation is the system that handles this volume without sacrificing the personal feel of an organizer who knows their customers. It is also the system that handles the inverse direction — replies coming back from exhibitors — so that the operational team is not chasing scattered Gmail threads to assemble what was said.

This workflow is distinct from the marketing campaigns that the sales side runs to generate leads. Those are bulk outbound campaigns with their own concerns — list segmentation, mining-driven targeting, A/B subject lines. The communication discussed here is **operational**: triggered by contract events, addressed to known exhibitors, governed by per-expo deadlines.

**Two communication tracks**

The system handles two distinct tracks of email communication, with different rules, different ownership, and different compliance posture:

**Operational (transactional) communication.** Triggered by contract events or expo deadlines. Sent to specific known exhibitors. Owned by the Project department. Examples: the eight-email announcement chain after a contract is signed (Welcome, Catalogue Form, Stand Design, Boost, Extra Service, BuildUp Rules, Payment Reminder, Badge), plus expo-deadline triggered messages (catalogue submission deadline, stand design deadline, etc.). These are not marketing. The exhibitor cannot opt out of them — they are necessary to deliver the service the exhibitor paid for. No unsubscribe footer.

**Marketing (campaign) communication.** Sent to leads, contacts, and past exhibitors as outbound prospecting. Owned by the sales side. Subject to opt-out: every marketing message carries an unsubscribe footer, and a recipient who unsubscribes is excluded from future marketing without affecting their operational communications.

The distinction is encoded on every email template: a template is either operational or marketing. The system enforces the unsubscribe rule based on this flag — operational templates ignore unsubscribe state; marketing templates respect it. A recipient who has unsubscribed from marketing still receives their Payment Reminder.

**The eight-email announcement chain (operational)**

When a Sales Contract is signed and converted, an established sequence of communications begins. Each email in the chain has a specific purpose, a specific deadline-relative trigger, and specific data it pulls from the expo and contract records:

- **Welcome** — sent on conversion. Confirms the participation, introduces the operations team, lists the operation team partners (stand contractor, travel, visa, forwarder).
- **Catalogue Form** — sent shortly after Welcome. Contains the secure link the exhibitor uses to submit their catalogue page (logo, description, products). The deadline is computed from the expo's catalogue deadline.
- **Stand Design** — Project sends the proposed stand design and asks for confirmation or revision requests.
- **Boost** — informs about additional visibility opportunities (sponsorship, premium placement, conference inclusion).
- **Extra Service** — informs about ancillary services (extra equipment, special carpet, extra signage, additional badges).
- **BuildUp Rules** — sent close to the expo. Contains build-up day timing, rules about on-site setup, what materials are allowed, what the venue requires.
- **Payment Reminder** — triggered by per-expo configuration (typically 30 days before the expo), sent only if the contract has outstanding balance.
- **Badge** — sent close to the expo. Provides the exhibitor's stand staff badges.

Each of these is one email template that pulls expo-specific data dynamically — expo name, dates, venue, deadline, partner contacts — at send time. There is not one template per expo, nor one template per language-and-expo combination. There is one operational template per email type, in three language versions (English, French, Turkish) that are managed together as one logical template with three variants.

**Per-expo configurable triggers**

The trigger for each email is configurable per expo, not hardcoded into the template. The expo record carries the trigger configuration:

- `payment_reminder_days_before` — how many days before the expo to send the Payment Reminder
- `catalogue_deadline_days_before` — defines when the Catalogue Form mail's stated deadline is
- `stand_design_deadline_days_before`
- `buildup_rules_days_before`
- `badge_send_days_before`

New expos inherit defaults from the system; the Owner or Project Department Lead adjusts these per expo as needed. This is why the trigger is not "fire 30 days before the expo" hardcoded in the email engine — it is "fire `payment_reminder_days_before` days before the expo, where that number lives on the expo record." The same template behaves differently across expos because the expo's deadline configuration drives the timing.

**The "send them all now" case — late-signed contracts**

The standard pattern is: contract signed six months out, email chain triggers spread across those six months. But a different pattern is real and frequent: contract signed one week before the expo. In that case, the spread-out chain is wrong — there is no time for "Catalogue email two months in advance, Stand Design one month in advance." The eight emails need to fire immediately, all of them, so the late-signing exhibitor is brought up to speed in one batch.

The system must support this. The Project department's contract page offers a "Send All Operational Emails Now" action: it queues all eight messages to fire in close succession (with reasonable spacing to avoid spam-detection issues at the receiving end), bypassing the deadline-relative timing. The exhibitor receives the full announcement chain that day and can respond to each within whatever time remains before the expo.

This action is not the default for normal contracts. Default is the deadline-relative schedule. The "send all now" action is invoked manually by Project for contracts where the schedule does not fit reality.

**Manual re-send and individual control**

Beyond the batch action, individual emails must be re-sendable on demand. Common case: the exhibitor reports "I never received the Welcome email" — Project clicks resend on that one email for that one contract. The system records the resend in the email history (the original send is preserved; the resend is logged separately).

Each email type, on each contract, shows its status: scheduled (will fire on date X), sent (fired on date Y), failed (bounced or rejected, with reason), resent (count and dates). The Project department can see at a glance whether the chain is on track or whether a contract has stalled.

**One template, three languages, managed together**

For every operational email type, there are three language variants — English, French, and Turkish. The vast majority of communication is in English (~80% of exhibitors). French is used when both the expo and the exhibitor are local-to-Francophone-context (a Moroccan exhibitor at a Morocco expo, for example). Turkish is used for Turkish exhibitors at any expo and for Turkey-based expos broadly.

The three language variants for one email type are managed together as one logical template. Editing the Welcome template means editing all three language versions in a single editor view, not navigating to three separate template records. They are versioned together, deployed together, and conceptually treated as one template with three rendered outputs.

The selection of which language to send is rule-driven, with a clear precedence:

1. If the exhibitor's contact record has an explicit language preference, that wins.
2. Otherwise, if the expo has been flagged as a "local audience" expo and the exhibitor is from that local country (Morocco expo + Moroccan exhibitor → French; Turkey expo + Turkish exhibitor → Turkish), use the local language.
3. Otherwise, English.

Country-based defaults are reference data — when a new local-language expo is created, the office configures which exhibitor countries get the local language. This is editable, not hardcoded. The Owner can override the language per contact at any time.

**Marketing campaigns and unsubscribe**

Marketing communication — the outreach the sales side runs to leads, past contacts, and prospects — runs on different rules. The sales rep or the campaign manager creates a campaign, selects a list, picks a template (marketing-flagged), schedules or sends.

Every marketing template carries an unsubscribe link in the footer. The link points to a one-click unsubscribe page that records the recipient's unsubscribe state. From that moment forward:

- The recipient is excluded from any future marketing campaign — no list segmentation, no campaign send, no test sends, includes them.
- The recipient continues to receive operational communications if they are an active exhibitor with a contract. The unsubscribe affects marketing only.
- The Owner or Project department can re-subscribe a recipient who explicitly asks to be added back. The audit trail records both events.

This per-recipient marketing-unsubscribe state plus per-template marketing-or-operational classification is enough to handle compliance correctly without forcing an all-or-nothing model that would break operational delivery.

Owners of marketing templates are sales reps and the sales managers. Owners of operational templates are the Project Department Lead and the Owner. The two ownerships do not overlap; the system enforces this through permissions on the template editor.

**Inbound replies — routed by sender mailbox, contract-visible**

Operational emails go out from the appropriate department mailbox — Project's address for most messages, Finance's address for Payment Reminder. Replies from exhibitors come back to whichever mailbox sent the original. This is the correct ownership: an exhibitor responding to a Payment Reminder writes to Finance; an exhibitor responding to a Stand Design email writes to Project. Sales reps stay in the loop on commercial events but are not the primary point of contact for operational matters once a contract is signed.

The reply mechanism today is the recipient department's Gmail inbox. The Project Department Lead reads Project replies; Finance reads Finance replies. If a reply contains information another department needs to know — sales or finance cross-cutting — it is forwarded or mentioned. This division works in practice. The sales side is informed on a need-to-know basis; the operational departments are the frontline for their respective concerns.

ELL must preserve this division while making the communication trail visible inside the system. Replies from exhibitors should appear on the contract record's communication history regardless of which mailbox received them. A new staff member opening a contract page should be able to see "Welcome sent on date X from Project, exhibitor replied on date Y, Payment Reminder sent on date Z from Finance, exhibitor replied on date W with cc to a third-party payer." The full thread, including cc'd parties (third-party payers, partner agencies, internal staff), is preserved as part of the record — the conversation is the relationship.

Whether this is achieved by integrating with the various Gmail inboxes or by routing replies through system mailboxes is an implementation choice. The need is: the contract page tells the story of every conversation across every operational mailbox, and a new staff member taking over the relationship can read that story without needing access to anyone's personal email archive.

**WhatsApp — internal first, external later**

WhatsApp has a clear primary use case at Elan Expo today: internal use by the Owner and sales staff. The Owner uses ELIZA's WhatsApp bot to query data, take notes, get reminders, and stay updated when away from a desk. Sales reps using WhatsApp for similar internal purposes is a natural extension.

External use of WhatsApp — sending operational messages to exhibitors via WhatsApp — is not a current need. It is a vision for after the platform is otherwise complete. When that time comes, the same configuration model used for email (per-expo triggers, per-template language variants, marketing-vs-operational classification, opt-out compliance) extends to WhatsApp as a parallel channel. But it is explicitly out of scope for the initial ELL build. Operational emails carry the operational chain; internal WhatsApp gives the Owner and sales staff a mobile-first window into the system.

**Email history and audit on the contract**

Every email sent in connection with a contract — operational or otherwise — is recorded on the contract. The history is queryable per contract, per expo, per email type, per recipient. For each email entry the system retains, in full:

- Which template was used and which version of that template (templates evolve; the historical version is preserved)
- The exact rendered content the recipient received — body, subject, attachments — stored as an immutable record. A question years later about "what exactly did we tell this exhibitor in 2026" has a precise, auditable answer.
- The sender mailbox (operational emails go from different addresses — Project's address for Welcome/Stand Design/Catalogue, Finance's address for Payment Reminder, etc.)
- The recipient address, plus any cc and bcc recipients
- The send time, the delivery status (delivered / bounced / failed)
- Any open or click tracking events that the email service captured
- Any reply that came back, with the full thread context preserved (replies often involve cc'd parties — third-party payers, partner agencies, internal staff — and the thread context is part of the relationship history)
- Any resend events triggered later

The retention is audit-grade. Storage cost is accepted as the price of evidence. The contract is the company's primary written commitment to its exhibitors, and the system holds the evidence of every commitment made.

**Sender identity — multiple operational mailboxes**

Operational emails do not all come from one mailbox. The Welcome, Catalogue Form, Stand Design, Boost, Extra Service, BuildUp Rules, and Badge emails come from the Project department's address. The Payment Reminder comes from the Finance department's address. The distinction is real and intentional — an exhibitor asked for a payment receipt does not write back to the Project department, they write back to Finance.

Each operational template carries a sender-mailbox configuration. The system supports multiple operational sender identities, configured per template type, with replies routed back to the matching mailbox. New sender identities can be added without code changes when the company structure expands.

**Must be better than today**

- **The eight-email announcement chain works without anyone managing it.** The Project department writes the templates once, configures the per-expo triggers once, and the chain delivers itself. New contracts hit the schedule automatically. Late-signed contracts get the "send all now" action. No spreadsheets tracking who got which email when.

- **One template per email type, three language variants managed together.** No proliferation of per-expo or per-country template copies. The Welcome template is one template, edited in one place, with English / French / Turkish renderings sitting alongside each other.

- **Per-expo trigger configuration replaces hardcoded timing.** Each expo configures its own deadlines and reminder windows. The same email engine sends Mega Clima Nigeria 2026's Payment Reminder 30 days before the expo and Sigma Morocco 2027's Payment Reminder 14 days before — both are correct because the expo records say so.

- **Marketing-vs-operational classification, with per-recipient unsubscribe.** Marketing templates carry unsubscribe; operational templates do not. A recipient who unsubscribes from marketing still gets their Payment Reminder. The compliance posture is correct without breaking exhibitor delivery.

- **Inbound replies live with the contract.** The Project department keeps using Gmail-style inbox workflows where appropriate, but the system's contract page tells the full story of every email and reply. New staff taking over a relationship read the contract, not someone's inbox.

- **Email history as evidence.** Years from now, the question "what exactly did we tell this exhibitor in 2026" has an answer — the rendered content, the date, the recipient, the delivery status — recorded against the contract. Email is the company's primary written commitment to its exhibitors, and the system treats it that way.

- **Resends, schedule visibility, failure handling.** The Project department can see at a glance whether a contract's email chain is on track, can resend a single email to a specific exhibitor in one click, and is alerted when a delivery fails so the exhibitor doesn't quietly fall through.

- **Language selection that respects the relationship.** Default by country, override per contact, expo-aware for local-audience expos. The Moroccan exhibitor at the Moroccan expo gets French; the German exhibitor at the same Moroccan expo gets English; nobody manages this manually past the initial configuration.

- **Marketing campaigns and operational chains are different systems with shared infrastructure.** Sales reps run campaigns; Project runs the announcement chain. They share the templating engine, the send infrastructure, the recipient-state model — but their ownership, their permissions, and their compliance posture are distinct. The system reflects this duality cleanly.

- **WhatsApp internally now, externally later.** The Owner's mobile-first window into the system through WhatsApp is a current need and a current capability. Exhibitor-facing WhatsApp is a future addition, not a Phase 1 commitment. The architecture preserves the option without paying for it now.

### 2.8 Reporting & Intelligence

**What this workflow is about**

Reporting is how Elan Expo sees itself. Every other workflow generates data; this workflow turns that data into the picture the Owner, the Sales Manager, the team leads, and the local offices need to make decisions. It is not a side feature — it is the daily interface the Owner uses to run the company. A dashboard that answers "where are we?" in five seconds is the difference between a company that is run on intuition and a company that is run on facts.

The reporting and intelligence layer covers three distinct surfaces, all driven by the same underlying data: **dashboards** the Owner and managers consume daily, **scheduled push reports** that arrive in inboxes and on phones without anyone pulling them, and **ad-hoc reports** built on demand for one-off questions. AI insights overlay all three — flagging trends, anomalies, and action opportunities the human reader might miss in the raw numbers.

This workflow defines what reporting needs to deliver. The technical question of which data lives where, which subsystem renders which dashboard, and how AI insights are computed belongs to the architecture phase. What matters here is: what answers does Elan Expo need from its data, and how must those answers be delivered?

**The three reports the Owner reads daily**

The Owner has a small set of questions answered every day, often multiple times a day:

1. **Sales pace per expo, by m² and by revenue.** "How are the active expos selling?" The Owner looks at each upcoming expo and sees how much area has been sold (in m²) and how much revenue has been booked. This is checked against the expo's targets and against the same point in the cycle for the previous edition of the same expo.

2. **Data entry activity per person, per office.** "Who is doing the work?" The Owner sees how many leads were added, how many contacts updated, how many emails sent — broken down by individual sales rep and by office. This is a performance signal: low data-entry volume from a particular rep or office is an early warning that something is off.

3. **Outstanding payments per expo.** "How much is owed to us, and against which expos?" The Owner sees, per expo, the total contracted value, the total received, the outstanding balance, and ideally the breakdown of which contracts are overdue. This drives the conversation with Finance about which exhibitors need a phone call before the next expense cycle.

These three views are the Owner's daily home. They must be one click away from any starting point in the system, render in seconds, and stay current — refreshed continuously, not manually rebuilt.

The Project Department Lead has their own daily set of questions which overlap partially with the Owner's: which expos have catalogue submissions outstanding, which have stand designs unconfirmed, which have payment reminders due. The system supports per-role daily dashboards rather than forcing every user through the Owner's view.

**Push reports — automatic, scheduled, by recipient**

Beyond what the Owner pulls, the system pushes reports automatically. The current ELIZA setup sends a morning brief and a weekly summary to the Owner via WhatsApp. This pattern extends:

- **Owner**: morning brief (yesterday's signed contracts, payments received, key alerts), weekly executive summary, monthly per-expo P&L drafts
- **Sales Manager**: weekly team performance summary across the whole sales organization
- **Sales Team Leads**: weekly summary of their team's activity — how many entries each rep made, how many emails sent, how many quotes opened, how many signed
- **Project Department Lead**: weekly operational summary, deadline-warning digest for upcoming expos
- **Local office heads**: weekly office summary, comparison to other offices on relevant metrics

Each scheduled report is configurable — frequency, time, channel (email, WhatsApp, in-app), recipient list. New scheduled reports are added without code changes. Recipients can mute or adjust their personal subscriptions but cannot opt out of reports that the Owner has designated as required (for example, the weekly team report to the team lead).

The push pattern recognizes a reality: people don't pull reports they don't already know exist. A weekly report that arrives in WhatsApp gets read; a weekly report that requires logging in and clicking gets ignored. Push is not a luxury feature — it is the reason intelligence reaches the people who need it.

**Ad-hoc reports — frequent, varied, AI-assisted**

The Owner builds custom reports regularly. The triggers vary: an upcoming commission payment to an external agency requires a report of all that agency's contracts and payments; a question about HVAC sector lead distribution by country requires a query across leads filtered by sector and grouped by country; a budget review requires actual-vs-budget comparison for a specific expo with category breakdown. These are not anticipated reports built in advance — they are situation-driven and structurally diverse.

Today these are built manually in Zoho's report builder, which is functional but slow and limited. ELL must support this in two complementary ways:

**A structured report builder** for users who know what they want and can construct it: select fields, apply filters, group by dimensions, choose visualization. This is the path for repeatable ad-hoc reports — once built, they can be saved, named, and re-run later. The same builder supports promoting a saved ad-hoc report to a scheduled push report or to a permanent dashboard widget.

**Natural-language report requests via AI** for users who know the question but not the data shape. "How many leads in the HVAC sector did we add from Nigeria in the last six months, broken down by sales rep?" produces the answer or produces a draft report that the user can then refine. This lowers the barrier to asking questions of the data — many useful questions go unasked today because building the report is more work than the answer is worth.

The two paths feed each other. AI-generated reports can be saved and become part of the repeatable library. Saved reports can be edited via the natural-language interface ("add a column for total revenue per rep").

**AI insights — four distinct kinds**

Beyond on-demand reports, the system actively surfaces what the human might miss. Four categories of AI-driven insight are valued:

**Trend detection.** Comparing this expo's trajectory to its previous editions, this rep's pace to their historical baseline, this office's conversion rate to its peers. "Mega Clima Nigeria 2026 is selling 15% slower in m² than 2025 was at the same point in the cycle." The system watches for meaningful divergences from established patterns and surfaces them.

**Anomaly detection.** Spotting absences and outliers — events that are notable because they didn't happen. "Morocco office had zero data entry activity this week, where the typical week is 50+." "This expo's catalogue submission rate is 40% with the deadline two weeks away; the typical pace at this stage is 70%." Anomalies are often more valuable than trends because they identify problems before they crystallize into bad outcomes.

**Action suggestions.** Connecting observed state to recommended next steps. "These three contracts have outstanding balance, the Payment Reminder fired two weeks ago, no payment received — does the Owner want to escalate to the Sales Manager?" The action is offered as a suggestion the Owner can accept, refine, or dismiss; the system never executes without confirmation, but it lowers the cognitive load of figuring out what to do next.

**Synthesis.** Combining multiple data sources into a narrative interpretation. "Q4 stand sales for HVAC sector are 20% below budget; the same period saw a slowdown in Nigeria-office data entry; the two are likely related — the office is not generating the leads the budget assumed." Synthesis is the most ambitious tier of insight and the hardest to get right; the system attempts it where the data supports a clear story and stays silent where it doesn't.

All four kinds appear in the Owner's daily dashboard, in the push reports, and in the WhatsApp interface. They are also explorable: clicking on an insight should reveal the underlying data and the reasoning, so the Owner can verify before acting.

**Visibility — who sees whose data**

Reporting carries the same hierarchical visibility model as the rest of the system. The default rule:

- **Project department and Owner see everything.** Operational reports across all expos, all offices, all reps.
- **Managers see their team's data, plus their own.** A Sales Team Lead sees the reps reporting to them and themselves; they do not see other teams. The Sales Manager sees the entire sales organization. The Project Department Lead sees Project staff.
- **Peers do not see each other.** A sales rep does not see another sales rep's pipeline or commission. A local office sales staffer does not see another office's data (unless they have an explicit assignment that crosses offices).
- **Each person sees their own data.** Rep sees their own contracts, their own commission, their own data-entry stats.

This is a default — the Owner can grant exceptions through the per-user permission matrix (a rep being trained to take over another rep's portfolio might temporarily get visibility, for instance). But the default protects organizational discipline: peer comparison is the manager's job, not a self-service feature for the rep to argue about.

Cross-team comparison reports — Nigeria office vs Morocco office vs Kenya office, for example — are visible to whoever has visibility into both sides. The Sales Manager and the Owner see them naturally; a regional team lead sees them only if their scope spans multiple regions.

**Operational vs financial vs data-entry productivity — three reporting axes**

The reporting layer is not one thing. Three distinct axes coexist:

**Operational reporting** — visitor registration funnels, catalogue submission rates, stand design confirmation rates, expo-readiness countdown. The Project Department Lead lives in this view. The data is per-expo, often time-relative ("two weeks before the show"), and oriented around deadlines.

**Financial reporting** — revenue per expo, expense per expo, budget vs actual, account balances, outstanding payments, commission payable. The Owner and Finance live in this view. The data is monetary, aggregated to EUR, often comparing periods.

**Data-entry productivity reporting** — leads added, emails sent, quotes opened, contacts updated, by person and by office. The Owner watches this; team leads watch their own teams. The data is activity-based, used as a leading indicator (low activity now → low contracts later).

These three axes share infrastructure but are conceptually distinct. A unified reporting layer must serve all three without forcing one frame on the others. A dashboard that mixes m² sold (operational) with EUR collected (financial) with leads added (productivity) is correct because the Owner's daily reality mixes all three. But a dedicated visitor-funnel screen serves the Project Department Lead's specific need, and a cash-position screen serves the Finance need, and the system supports both.

**Mobile and WhatsApp interface**

The Owner's primary mobile interface today is the WhatsApp bot connected to ELIZA. This is the right pattern: ask a question in natural language ("Mega Clima Nigeria m² satışı"), receive an answer formatted for a phone screen ("Mega Clima Nigeria 2026: 412 m² sold, target 600 m², 68% achieved, 8 weeks to show"). The full report library is available; the phone interface is just a different surface onto the same data.

This pattern extends to other roles. A sales rep traveling can ask "outstanding from my contracts" and get the answer. A team lead can ask "team activity this week" and get the summary. The interface is the same — natural language in, formatted answer out — with the same hierarchical visibility rules applied automatically.

The desktop dashboard remains the primary surface for deep work; the WhatsApp interface is the always-available companion. Neither replaces the other; they are two faces of the same intelligence layer.

**Evidence and traceability**

When the system reports a number, the Owner must be able to ask "what is this number?" and get a real answer. Every dashboard tile, every report row, every AI insight must be traceable to the underlying records. Clicking on "412 m² sold" produces the list of contracts that summed to 412. Clicking on "this expo is selling 15% slower than 2025" produces the comparison data with the source records. Clicking on "Morocco office had zero data entry this week" produces the filtered query across all data-entry events in that office for the week.

Reporting without traceability is opinion. Reporting with traceability is evidence. The Owner cannot trust insights they cannot verify, and the system must support verification at every level — not as a hidden debug feature, but as a normal one-click-away capability for any number on any screen.

**Must be better than today**

- **The three daily Owner views are one click away.** Sales pace per expo (m² + revenue), data-entry activity per person and office, outstanding payments per expo. These render in seconds and stay current. No more assembling them by filtering modules separately.

- **Push reports reach the people who need them, on the channels they use.** Owner gets WhatsApp morning brief. Team leads get weekly team summaries. Project Lead gets deadline-warning digests. Local office heads get office-comparison summaries. New recipients and new schedules added through configuration, not code.

- **Ad-hoc reports built two ways: structured builder and natural-language AI.** The Owner can drag-drop fields when they know the shape of the answer; they can ask in natural language when they don't. Both paths produce saveable, repeatable, schedulable reports.

- **AI insights surface trends, anomalies, action opportunities, and synthesis.** The system actively watches for what the human reader might miss — selling slower than last year, an office that went quiet, a payment reminder that didn't produce a payment, a budget shortfall with a probable cause. Insights are explorable to their underlying evidence.

- **Hierarchical visibility enforced by default, configurable by exception.** Project and Owner see everything; managers see their teams; peers do not see each other; each person sees themselves. The Owner adjusts per user when the situation requires it.

- **Three reporting axes — operational, financial, productivity — coexist without forcing one frame.** The Project Department Lead has their view, Finance has theirs, the Owner has the integrated view. None of the three is grafted onto a tool designed for the other two.

- **Mobile-first via WhatsApp, desktop for depth.** The Owner asks questions on the phone and gets answers formatted for the phone. The same data, the same visibility rules, the same intelligence — different surface. Sales reps and team leads have the same affordance for their scoped data.

- **Every number is traceable to its source records.** Click any dashboard tile, any report row, any insight — get the underlying data. No opaque numbers. Trust comes from the ability to verify.

- **Custom reports become library reports become dashboard widgets become push reports.** A useful one-off becomes a saved query becomes a tile on the dashboard becomes a scheduled WhatsApp summary, all without rebuilding. The reporting layer is composable, not siloed.

- **Reports the company already uses are migrated, not lost — and curated, not bulk-copied.** Before migration, the Owner and the Project Department Lead review the existing Zoho report library together and mark the reports that genuinely drive daily decisions. Those reports are recreated in ELL. The hayalet raporlar — reports created once for a one-off question and never reopened — are left behind. The exercise is manual and human-judged, not an automated audit, because the question of "which reports do we actually rely on?" is best answered by the people who would notice if a report disappeared.

---

## Part 3 — Cross-Cutting System Requirements

[TBD — to be filled in next session]

### 3.1 Permission & Access Control [PRINCIPLE]

**The principle**

Permissions in ELL are **per-user, configurable, and overridable**. There is no static role hierarchy hardcoded in the system. There are convenient profile templates for fast onboarding, but every user's permission set is independently editable, and the Owner can grant or revoke any specific capability for any specific user without affecting anyone else.

This principle is the operational foundation of the system's flexibility. It accepts that Elan Expo's organizational structure is mutable (people get promoted, teams reorganize, exceptions are needed), that personal trust is granular (a particular rep might be allowed to see something other reps cannot), and that one-size-fits-all role definitions cannot anticipate every legitimate exception. The system supports defaults; the Owner controls exceptions.

**Two layers: profile templates and per-user matrix**

Permissions are constructed in two complementary layers.

**Profile templates** are named permission presets used for fast onboarding. The system ships with the following templates:

1. **Owner** — full visibility and full control across every module, every record, every action.
2. **Project Department Lead** — full operational visibility and control across all expos, plus read access to financial data.
3. **Project Staff** — full operational access; no financial data.
4. **Sales Manager** — visibility across the entire sales organization, write access to commercial records, no operational write access.
5. **Sales Team Lead** — visibility into the team they manage, write access to their own records and read access to their reports.
6. **Sales Rep** — own pipeline, own contracts, own commission, no peer data.
7. **Local Office Sales** — sales scope limited to their office, otherwise mirrors Sales Rep.
8. **Local Office Project** — operational scope limited to their office, otherwise mirrors Project Staff.
9. **Finance** — financial modules in full (Revenue, Expense, accounts, payment side of contracts), no operational details (catalogue, stand design, visitors).
10. **Admin** — system configuration (user creation, reference data, account list, expense category management). May overlap with Owner or be a separate role.

These templates are not exhaustive prescriptions of correct behavior — they are starting points. The list itself is editable by the Owner; new templates can be added when the company grows into new role shapes.

**Per-user matrix** is the actual permission record for each user. The matrix specifies, for each module and each action (View, Create, Edit, Delete, plus module-specific special permissions like "Convert Quote", "Change Contract Status", "Approve Refund"), whether the user can perform it. The matrix also specifies data scope — which records of each module the user sees (their own, their team's, their office's, all).

When a user is created, a profile template is selected and its permissions are copied into the user's matrix. From that moment, the matrix is independent. The Owner can edit any cell of any user's matrix without consulting the template. If the template is later edited, **existing users are not affected** — the template was a snapshot at creation time, not a live binding. This keeps the system predictable: changing a template never silently changes anyone's permissions.

If the Owner wants to apply a template's update to existing users, that is an explicit "re-apply template" action — done deliberately, with awareness that any per-user overrides will be replaced. The default behavior is independence; bulk re-application is opt-in.

**Data scope is separate from action permission**

The matrix distinguishes two questions:

- **Can the user perform the action?** (e.g., can this user create Sales Contracts at all?)
- **On which records can the user perform it?** (e.g., on contracts they own, contracts in their team, contracts at their office, all contracts)

Both are configurable. A user might have full Edit permission on Sales Contracts but only on contracts owned by their team. A different user might have View-only permission but visibility into all offices. The action and the scope are independent dimensions.

Data scope is derived from two inputs: the user's hierarchy position (the `reports_to` chain) and explicit per-user additions. By default, scope follows the hierarchy — a manager sees their reports' data, a team lead sees their team's data, a peer sees only their own. Exceptions are added explicitly: a sales rep being trained to take over a colleague's portfolio gets a temporary scope addition; a senior project staff member helping with a specific local office gets cross-office visibility for that office.

**Configurable defaults, not categorical rules**

A specific anti-pattern this principle rejects: writing rules of the form "Sales reps NEVER see commission of other reps" or "Project staff CANNOT modify financial records." These are sometimes correct as defaults but always wrong as absolutes. Real organizations have real exceptions — a senior sales rep who is being prepared for promotion needs broader visibility temporarily; a Project staff member with finance background gets trusted with a specific module; a country manager covering for an absent team lead needs to see data they normally don't.

The system encodes these as **configurable defaults**. The default for Sales Rep is "no peer commission visibility"; the Owner can grant exceptions per user. The default for Project Staff is "no financial write access"; the Owner can grant exceptions per user. The defaults protect organizational discipline; the exceptions reflect real trust decisions.

This is the same pattern that appears throughout Part 2 — the Quote → Contract conversion gate, the Sales Contract status change restriction, the cluster partner sharing — defaults that are sensible in 95% of cases and overridable in the 5% where the situation demands it.

**Special permissions beyond CRUD**

Some actions are not adequately captured by View/Create/Edit/Delete. The matrix supports module-specific special permissions:

- **Convert Quote to Sales Contract** — restricted to Project department by default (D12)
- **Change Sales Contract Status** — restricted to Project department by default
- **Approve Refund** — Owner by default, optionally Sales Manager + Project Department Lead
- **Edit Operational Email Templates** — Project Department Lead and Owner by default
- **Edit Marketing Email Templates** — Sales Manager and sales reps by default
- **Edit Reference Data** — Owner by default; specific reference types may be delegated
- **Edit Permission Matrix of Other Users** — Owner only, by default
- **View Audit Log** — Owner by default
- **Run Migration / Bulk Operations** — Admin or Owner

The list is extensible. Each module declares the special permissions it supports; the matrix exposes them alongside the standard CRUD permissions for any user.

**Hierarchy as input, not constraint**

Each user has a `reports_to` field pointing to another user. This forms the management hierarchy used for data scope (a manager sees their reports' data). The hierarchy is editable from the admin UI — no code change is needed to promote a sales rep to team lead, to add a layer between the Owner and the Sales Manager, or to restructure local office reporting.

The hierarchy informs default data scope but does not lock it. If a particular reorganization makes the default scope wrong (a newly promoted team lead who should temporarily continue managing their old portfolio plus their team's new portfolio), the matrix accepts an explicit scope addition. The hierarchy is a starting point; the matrix is the final answer.

**Audit and change history**

Permission changes are themselves audited. Every change to a user's matrix — by whom, when, what changed, why if a note was added — is logged and visible in the audit module (see 3.6). A user whose visibility expands or contracts can know when and by whose action. This is not surveillance; it is accountability. The Owner who grants an exception leaves a record; the user who lost access can see when.

**Must be better than today**

- **Per-user permission, not per-role gatekeeping.** Each user's matrix is independently editable. No category-wide "all sales reps see X" forced on everyone in the role; defaults exist as templates, exceptions exist for the cases that need them.

- **Profile templates as fast onboarding, not binding contract.** Apply a template at user creation; from that moment the user's matrix is independent. Template changes do not silently propagate. Re-application is an explicit, deliberate action.

- **Data scope and action permission as separate dimensions.** What a user can do is one question; on whose records they can do it is another. The matrix answers both, and the answers are configurable independently.

- **Hierarchy editable from admin UI.** Promotions, demotions, restructurings, new managers in the chain — all configurable, no code changes. The system supports tomorrow's organization without rewriting today's.

- **Special permissions beyond CRUD.** Convert, status change, refund approval, template editing, reference data editing, audit access — the actions that matter most are explicit toggles, not deduced from generic CRUD assumptions.

- **Permission changes are audited.** Every grant and revocation is logged. The Owner can answer "who has visibility into this expo's contracts and how did they get it?" by reading the audit trail.

- **Compared to Zoho's Profiles + Roles model.** Zoho's two-level abstraction (a Profile defines what actions are allowed; a Role defines what records are visible) is rigid: changing one rep's visibility means creating a new Role, which then becomes a permanent shape in the system. ELL collapses both into the per-user matrix with template starting points, eliminating the rigidity without losing the convenience of defaults.

### 3.2 Identity & User Management [PRINCIPLE]

**The principle**

Three concepts must be cleanly separated in ELL: **users**, **sales agents**, and **data entry contractors**. They overlap operationally (some users are also sales agents; some sales agents do data entry) but they answer different questions and must not be conflated in the schema.

**Users** are the people who log into the system. They have credentials, a per-user permission matrix (3.1), a hierarchy position, and a working surface that depends on their role. Roughly 25 active users today: HQ staff plus local office staff plus the Owner. New users are created and existing ones deactivated through admin UI.

**Sales agents** are the entities to whom commission can be attributed on a Sales Contract. About 150 active records today. The set is much larger than the set of users because it includes external agencies (independent expo-marketing firms in Turkey and partner countries who close deals on commission), freelancers brought in for specific expos, and inactive past staff whose historical contracts must remain attributable. Most sales agents are not users — they have no reason to log into anything; they sell on commission and report deals by email or phone.

**Data entry contractors** are temporary workers brought in to add data (leads, contacts) at scale, often through public forms that don't require authentication. They are not users (no login) and not sales agents (no commission). The system tracks their submissions for productivity attribution but does not give them system access.

The schema must reflect this triple separation. A user record can optionally link to a sales-agent record (when an internal employee earns commission on their own deals). A sales-agent record exists independently and can be referenced from contracts regardless of whether the agent is a user. Data entry contractor identity is a separate, lightweight concept used only for attribution.

**User accounts and lifecycle**

User accounts are created by admins (Owner or designated admin role). At creation, a profile template is selected (3.1) which copies its permissions into the new user's matrix. From there the matrix is independent. The user's hierarchy position (`reports_to`) is set explicitly.

Users can be deactivated rather than deleted. Deactivated users retain their historical record-ownership (the contracts they closed, the leads they added, the audit trail of their actions) but cannot log in and cannot be assigned new work. Reactivation is reversible and restores access. Hard deletion is rare and reserved for cases where the user was created in error.

When a user is deactivated, the records they own do not become orphans. The system supports reassignment — explicit transfer of pipeline ownership from a departing rep to their successor — and falls back to manager ownership when reassignment is not specified. The Owner is responsible for ensuring departing-staff transitions happen cleanly; the system makes the operation easy but does not auto-execute it.

**Sales agent records and lifecycle**

Sales agents are created when needed — either when an external agency starts working with Elan Expo, or when an internal user starts earning commission. Each sales agent record carries: name, type (internal employee / external agency / freelancer), default commission percentage, contact information (for externals), and an optional link to a user record (when the agent is also a system user).

Inactive sales agents are kept as read-only records. An external agency that hasn't closed a deal in two years is still in the system because their historical contracts reference them. The agent's record is preserved; it can be reactivated if the relationship resumes.

Sales agents are not deleted while any contract references them. The system enforces this constraint: a delete request on an agent with attributed contracts produces a clear error explaining what would break. If the relationship truly needs to be erased (a name change, a merger), the operation is a controlled rename plus an audit-logged change, not a hard deletion.

Some sales agents may eventually need a public-facing identity — a name and photo used in customer communications ("your account manager is X"). This is a future concern, not a Phase 1 requirement. For now, sales agent records are internal.

**Identity, audit, and accountability**

Every record creation, modification, and significant action is attributed to the user who performed it. Records carry `created_by`, `created_at`, `modified_by`, `modified_at` consistently. Audit-significant actions (status changes, permission grants, refund approvals, template edits) write to the audit log (3.6) regardless of which module they occurred in. The Owner can always answer "who did this and when" for any data point in the system.

When a user is deactivated, their historical actions remain attributed to them — a contract created by a rep who later left is still recorded as their work. The system does not rewrite history when people leave.

**Must be better than today**

- **Users, sales agents, and data entry contractors are first-class separate concepts.** No more shoe-horning external agencies into fake user accounts. No more confusion about whether the contract "owner" is a system user or a commission target. The schema reflects the three distinct kinds of identity.

- **Per-license cost decoupled from commission attribution.** Adding 50 external agencies to commission tracking does not require 50 user licenses. Sales agents exist as records, not as logins.

- **Hierarchy mutable, history preserved.** Promotions, demotions, departures, restructures — all configurable. Historical attribution is preserved through all of them.

- **Deactivation, not deletion.** Users and sales agents are retired without erasing their footprint. Reversible, accountable, audit-trailed.

- **Reassignment as a deliberate operation.** Departing staff transitions go through an explicit pipeline transfer, not a silent orphan-record state. The departing rep's work has a clear new owner.

### 3.3 Multi-Currency & Multi-Account [PRINCIPLE]

**The principle**

Money in ELL is always **doubly recorded** — in the original currency it actually moved, and in EUR for consolidation. Exchange rates are **frozen at transaction entry time**, never silently recomputed. Every money movement is **two-sided** — an outflow somewhere paired with an inflow elsewhere. Account balances are **derived from transaction streams**, never stored as denormalized fields.

These four mechanics, together, define how ELL handles the operational reality of a multi-currency, multi-office, partially-cash business that sometimes uses parallel-market exchange rates and routinely moves money between offices in both directions.

**Original currency plus EUR equivalent on every transaction**

Every Expense, every Revenue, and every transfer carries: the amount in the currency it actually happened in, the currency code, the exchange rate to EUR captured at entry time, and the EUR-equivalent amount derived from the rate at that moment. The original-currency view is the operational truth — what the local office actually paid, what the customer actually wired. The EUR view is the consolidated executive picture.

When EUR is itself the transaction currency, the rate is 1.0 and no conversion happens. The schema does not distinguish "EUR transactions" as a special case — they are normal transactions with rate 1.0 and amount equal to amount-in-EUR.

**Exchange rates are frozen, not retroactively adjusted**

The rate captured on a transaction is the rate that actually moved that money. Black-market and parallel-market rates differ from official rates in several of Elan Expo's markets. The user entering the transaction enters the rate they actually used. The system records what the user records.

Once a transaction is saved, its exchange rate is immutable for the lifetime of that transaction. It is never recomputed when a new daily rate is published. It is never silently aligned with an official rate. If a correction is genuinely needed (the user entered the wrong rate), the correction is an explicit edit with audit trail, not an automatic adjustment.

A daily rate table may exist as a **suggestion** — the system can pre-fill an exchange rate field with today's central-bank rate as a starting point — but the user always overrides when reality differs from the official figure. The default is convenient; the truth is editable.

**Every money movement is two-sided**

A transfer between accounts produces both an outflow from the source account and an inflow to the destination account. The two sides are linked as one logical event. This applies to:

- HQ subsidising a local office, or a local office remitting to HQ
- The Owner paying for company expenses out of personal funds (paired with an entry on the Owner's current account against the company)
- The Owner withdrawing from the company to personal funds
- A revenue collected as cash that later becomes a deposit into a bank account
- Any other movement of money between accounts the system tracks

Single-sided records — money appearing or disappearing from one account without a counterpart — are an error condition, not an accepted shape. The system enforces the two-sided invariant at the transaction level.

**Account balances are computed, not stored**

The current balance of any account is the sum of all transactions on it, in the account's currency. There is no `accounts.current_balance` field that someone has to remember to update. Querying the balance at any point in time — today, end of last quarter, the morning of an audit — is a query against the transaction stream up to that date.

The same principle extends to the Owner's current account, to credit balances on companies, to commission adjustments owed by sales agents, to outstanding balances on contracts. Real business state is the sum of real events; it is never a separately-maintained number that can drift.

**Editable account list**

The set of accounts is reference data, editable by the Owner. Each account has a name, a currency, an associated office (when applicable), an account type (bank / cash / virtual current account / other), and an active flag. New offices opening accounts, existing offices adding currencies, the Owner needing a new personal-current account — all configured through the admin UI without code changes.

Closed accounts are deactivated, not deleted, when historical transactions reference them. The transaction history remains intact; the account simply stops accepting new transactions.

**EUR as the consolidation reporting currency**

All consolidated reporting is in EUR. Cross-account totals, cross-expo profitability, cross-office summaries, executive dashboards — EUR is the unit. The original-currency amount is always available alongside the EUR equivalent for any line item, but aggregations are EUR-based.

This convention is not architectural; it is commercial. EUR is the currency the Owner thinks in, the currency the company's main accounts hold, and the currency that makes cross-market comparison meaningful for an organization headquartered in Istanbul and operating across Africa.

**Must be better than today**

- **Original currency and EUR equivalent always coexist.** No information is lost in consolidation. The local office sees what they actually paid; the Owner sees the consolidated picture; both views come from the same transaction record.

- **Frozen rates with traceability.** Every EUR figure in every report can be traced back to the rate it was computed at and the user who entered it. Black-market rates are first-class. Retroactive rate adjustments do not silently change historical reports.

- **Two-sided invariant enforced.** No transfer disappears. Every euro's path through the company is auditable from origin to destination.

- **Balances computed from events.** No denormalized balance fields that can desync. Account statements, credit balances, outstanding amounts, commission adjustments — all queries.

- **Account list editable, not coded.** New accounts, new currencies, new offices — operational changes, not engineering tickets.

### 3.4 Hierarchical Visibility & Data Scope

**The principle**

Default data visibility follows the management hierarchy: **managers see down, peers do not see each other, individuals see their own.** Project department and Owner see everything by default. These defaults are configurable per user (3.1) but they protect the organizational discipline that the company has chosen.

**The default visibility rule**

For most modules in the system — leads, contacts, companies, quotes, contracts, revenues, expenses, commissions — the default scope rule is:

- **The Owner** sees everything across every dimension (every expo, every office, every user's records).
- **The Project Department Lead and Project staff** see everything operational across every expo and office. Project has full operational read access by default, plus financial read access at the Project Lead level.
- **Managers** (Sales Manager, Sales Team Lead) see their own records plus the records of everyone reporting to them, transitively. The hierarchy `reports_to` chain is the input; the scope is the union of the chain.
- **Peers** do not see each other's records. A sales rep does not see another sales rep's pipeline. A local office sales staff member does not see another office's sales activity.
- **Individuals** see their own records — what they own, what they created, what is assigned to them.

This is the **default**. Through the per-user permission matrix (3.1), the Owner can grant any user broader scope (a senior rep gets visibility into a colleague's portfolio during transition), narrower scope (a junior rep sees only deals beyond a certain confidence level), or cross-cutting scope (a regional manager spans two offices).

**Scope is composed, not assigned to a single rule**

A user's effective scope on any module is composed from several inputs:

- **Hierarchy-derived scope** — own records plus records of everyone reporting to them through the hierarchy
- **Office-derived scope** — for office-restricted users, records belonging to their office
- **Explicit additions** — specific records, expos, offices, or users added through the matrix
- **Explicit exclusions** — specific records the user is not allowed to see despite default rules including them

The system computes the user's effective scope at query time by combining these inputs. This composition is auditable — for any record a user sees (or does not see), the system can explain why.

**The Sales/Project privacy boundary**

A specific application of hierarchical visibility is the boundary between sales-side data and project-side data. Sales reps see commercial records — their own contacts, their own quotes, their own contracts, their own commission. They do not by default see project-side operational data (catalogue submissions, stand designs, internal project notes), nor do they see other reps' commercial records.

Project staff see operational data across all expos. They do not see other reps' commission breakdowns by default, but they do see the contracts those commissions sit on (because contracts are operational records).

These boundaries reflect organizational discipline: sales reps are evaluated on their own performance and should not have visibility into peer commission to argue from; project staff focus on operations and need contract-level operational data to do their job.

The Owner can grant exceptions through the matrix when they trust a particular user with broader visibility.

**Cross-cutting reports respect scope**

When a user runs a report — a custom report, a saved report, a dashboard widget — the data is filtered to the user's scope automatically. A team lead running "team performance this month" sees their team only. The Sales Manager running the same report sees the entire sales organization. The Owner sees everything.

This is enforced at the query layer, not at the UI layer. A user cannot bypass scope by constructing a query that would include records they should not see — the query engine refuses to return what the user does not have scope for.

**Data scope changes are deliberate, not silent**

Promoting a sales rep to team lead changes their scope. Restructuring a region changes the scope of multiple users. These changes are explicit operations through the admin UI: the hierarchy is edited, the new scope takes effect, the audit log records who made the change and when.

A user whose scope expands does not retroactively see records that were created before the change — or rather, they do, because the scope rule applies at query time to whatever records exist now. There is no "scope at creation" snapshot. This is intentional: when the company restructures, the new visibility reflects the new organization, not a frozen historical reality.

**Must be better than today**

- **Hierarchy-derived scope as the default, configurable per user.** The system computes who-sees-what from the org chart automatically. Exceptions are explicit and audit-trailed.

- **Sales/Project privacy boundary preserved by default.** Sales reps don't drift into operational data they shouldn't see; project staff don't drift into commission politics. The default protects the organizational discipline; exceptions reflect real trust.

- **Scope composition is auditable.** For any record the user sees or doesn't, the system can explain the rule that produced the answer. No mystery permissions.

- **Reports inherit scope automatically.** A team lead's "team performance" report shows their team. The same report run by the Sales Manager shows the whole organization. No per-user report tailoring needed.

- **Restructure once, see the new picture immediately.** Hierarchy edits propagate to scope without code, without bulk re-permissioning. The new team lead sees their new team the moment the org change is saved.

### 3.5 Reference Data Management

**The principle**

Reference data — the controlled lists that other records refer to — is **owned by the Owner** and **editable through admin UI without code changes**. The lists are stable but not immutable; they grow and change as the company evolves.

A reference data change is an operational decision, not an engineering ticket. Adding a new sector, a new expense type, a new account, a new payment method, a new partner role — all happen through the same admin surface, by the same person, in seconds.

**The reference data inventory**

The following are reference data in ELL:

**Geographic and demographic:**
- **Countries** — ISO codes used in AF Number prefixes (D11) and in default-language inference
- **Sectors** — HVAC, Construction, Food Machinery, Water Systems, Ceramics, Decoration/Furniture, Electricity, Agriculture, Information Technology, etc.
- **Languages** — for template variants, contact preferences, country defaults

**Commercial:**
- **Products** — the master pricing catalogue (~242 SKUs today, including PES, RF, SYK, per-expo equipment, visa letters, sponsorships, ancillary services)
- **Currencies** — EUR, NGN, MAD, TL, USD, KES, DZD, GHS, plus any new ones the Owner adds
- **Payment methods** — bank transfer, cash, SWIFT, credit balance, etc.

**Financial:**
- **Expense Categories** — six top-level categories (Office, Operation, Pre-Event, Sales, Marketing, Conference)
- **Expense Types** — ~75 child types under the categories (Salaries/Wages, Hall Rent, Stand Construction, Catering, Flight Tickets, etc.)
- **Revenue Categories** — fifteen flat categories (Expo Participation, Sponsorship Income, Stand Construction, etc.)
- **Accounts** — bank accounts, cash accounts, virtual accounts (3.3)

**Operational:**
- **Stand Types** — Equipped, Space Only, Premium, etc.
- **Sales Groups** — International, Local, country-named groups
- **Partner roles** — Stand Contractor, Travel, Visa, Forwarder, Hostess, Catering, Security, Venue Authority (D25)
- **Email template types** — Welcome, Catalogue Form, Stand Design, Boost, Extra Service, BuildUp Rules, Payment Reminder, Badge, plus marketing campaign templates
- **Sender mailboxes** — Project, Finance, future departments as the company grows

**Permission and role:**
- **Profile templates** — Owner, Project Department Lead, Project Staff, Sales Manager, Sales Team Lead, Sales Rep, Local Office Sales, Local Office Project, Finance, Admin (3.1)
- **Special permissions** — the extensible list of module-specific permissions beyond CRUD

This is not exhaustive — every module that uses controlled vocabulary contributes its lists to the reference data inventory.

**Editing rules**

Reference data is edited through the admin UI by users with the Edit Reference Data special permission, granted by default to the Owner. Specific reference types may be delegated — for example, the Project Department Lead might be given permission to edit Partner roles and Stand Types without being given full reference-data authority.

Edits to reference data take immediate effect everywhere. Adding a new sector immediately makes it selectable on lead forms and contact forms. Renaming a sector updates the display label everywhere the sector appears. Deleting a sector requires that no record currently references it (or an explicit reassignment of dependent records to a different sector).

**Reference data is not deleted while referenced**

The same constraint that applies to sales agents (3.2) applies to all reference data: a value cannot be deleted while records reference it. The system enforces this at the data layer. Attempting to delete an in-use reference value produces a clear error explaining what depends on it.

When a reference value becomes obsolete, the operational practice is to deactivate (set inactive flag), not delete. Inactive values are not offered in new entry but remain valid for historical records. This preserves the integrity of past data while keeping the active list clean.

**Approval workflow — light, not bureaucratic**

For most reference data changes, no approval workflow is needed. The Owner edits, the change takes effect. For high-impact changes (a new top-level expense category, a renamed major sector), the Owner may want a notification trail — the audit log captures every change automatically (3.6), so review-after-the-fact is always possible.

A formal approval workflow (proposed change → review → approve → live) is not a Phase 1 requirement. The Owner is the authority; the audit log is the safeguard. If the company grows to a point where reference-data changes need formal approval, the workflow can be added.

**Reference data and migration**

When ELL launches, reference data is seeded from the existing Zoho configuration. The 6 expense categories and 75 types, the 15 revenue categories, the 8 sectors, the 7 country codes, the multi-language template list — all exported from Zoho and imported into ELL's reference tables.

Migration is a one-time event. After launch, reference data is owned by ELL and managed through the admin UI. Zoho is no longer the source.

**Must be better than today**

- **Reference data managed through admin UI, not engineering tickets.** New sectors, new expense types, new accounts, new partner roles — all configurable in seconds by the Owner or designated admin.

- **Edits take immediate effect across the system.** No deployment cycles for what should be operational changes.

- **Deactivation, not deletion, when values become obsolete.** Historical records remain valid. New entry uses only active values.

- **Audit trail on every reference data change.** The Owner can answer "when did we add this category and who renamed that one?" by reading the audit log.

- **Reference data is the same across all subsystems.** Whatever the architecture phase decides about how reference data is replicated, the user-visible truth is one list per concept — not divergent lists across LIFFY, ELIZA, LEENA.

- **Migration seeds the catalogue once; ELL owns it thereafter.** Zoho's reference configuration is imported at launch. After that, ELL is canonical.

### 3.6 Audit & History

**The principle**

Significant changes to the data are logged, and the log is preserved long enough to support real audit needs. The retention is **24 months rolling**: anything older is archived to cold storage rather than discarded. The audit log is read by **the Owner and the Project Department Lead by default**; broader access can be granted through the permission matrix.

**What is audited**

The audit log captures changes that have organizational, financial, or relationship significance. Not every keystroke — that would be noise — but every change a competent investigator would want to see when answering "what happened?":

- **Status changes** — Sales Contract status changes, Quote conversions, expo activation/archival, user activation/deactivation
- **Permission changes** — every grant, revocation, and template re-application on any user's matrix
- **Reference data changes** — new categories, renamed values, deactivations
- **Financial actions** — refund approvals, commission adjustments, transfer events between accounts, exchange rate corrections
- **Identity changes** — user creation, user deactivation, sales agent creation, sales agent rename
- **Email template edits** — operational and marketing
- **Configuration changes** — per-expo trigger configuration, notification defaults, integration settings
- **Bulk operations** — migrations, mass reassignments, bulk imports

For each entry the log records: who performed the action, when, what was changed (before and after values where applicable), and any note the user added at the time of the change.

Routine record edits — typing a phone number, updating a stand design link, adding a payment record — are captured in the standard `created_by`/`modified_by` fields on the records themselves, not duplicated into the audit log. The audit log is for events that warrant scrutiny; the modification fields are for everyday traceability.

**Retention: 24 months active, archive thereafter**

The audit log is fully queryable for the most recent 24 months. Entries older than 24 months are not deleted — they are moved to archive storage where retrieval is possible but not instant. A specific older entry can be retrieved when needed (an investigation into a deal closed three years ago), but the active interface focuses on the recent window.

This balances two needs: real audit value (which often spans a year or two of activity) against query performance and storage cost (which becomes significant if every entry stays in the hot path forever). The 24-month window covers the typical expo cycle (from sales-open to post-show analysis) plus margin for delayed disputes.

**Access: Owner and Project Department Lead by default**

The audit log is read by the Owner and the Project Department Lead by default. These two roles together cover the organizational vantage points that need accountability visibility: the Owner sees everything, and the Project Department Lead sees the operational integrity questions (who changed a contract status, who edited a template, who reassigned a partner).

Broader access — the Sales Manager reading audit entries on their team's actions, a specific user reading audit entries on their own record — is configurable through the matrix as a special permission. The default is restrictive because audit logs are sensitive; exceptions are explicit.

A user always has access to audit entries about themselves — they can see when their permissions were changed, when their hierarchy position was edited, when their data scope expanded or contracted. Self-audit transparency is a baseline.

**Records cannot be silently rewritten**

Beyond the audit log, the system preserves the principle that significant data is not silently overwritten. Sales contracts that get renegotiated produce new versions (or status changes with audit entries), not silent in-place edits that erase the original terms. Email templates that evolve preserve their historical versions, so an audit question of "what did we send in 2026?" can be answered against the template version that was live at the time. Reference data values that get renamed preserve the rename event in the log.

The combination of audit log plus version-preservation produces a trustworthy historical record. The system can answer "what did this look like at this date?" for any significant data point.

**Must be better than today**

- **Significant changes captured automatically.** The Owner does not have to remember to log changes — the system logs them. Permission grants, refund approvals, status changes, template edits — all in the audit log without anyone writing a note.

- **24-month rolling window with archive beyond.** The recent past is queryable in seconds; the older past is recoverable when needed. Storage cost stays bounded; audit value stays real.

- **Owner and Project Department Lead see the audit log by default; others on permission.** The right people have the right visibility without the audit becoming a cultural surveillance tool.

- **Self-audit is universal.** Every user can see audit entries about themselves. Permission changes, scope changes, hierarchy changes — visible to the person affected, not just the manager who made them.

- **Versions preserved alongside the log.** Templates, contracts, reference values — the audit log says when something changed; the version preservation says what it was. Together they answer "what did this look like at the time?"

### 3.7 Search & Navigation

**The principle**

Search in ELL is **global by default, scopeable on demand**, and respects the user's data scope automatically. Saved filters are **personal**, with optional sharing for managers who want to push a curated view to their team. Navigation is fluid — switching from a contract to its company to that company's other contracts to the expo of one of them happens without context loss.

**Global search across modules**

A search query from the global search bar searches across every module the user has scope on: leads, contacts, companies, contracts, quotes, expos, expenses, revenues, sales agents, partners, products. Results are grouped by module, ranked by relevance, and surfaced in seconds.

The same query string can match: a contact's name, a company's name, a contract's AF Number, an expo's slug, a payment receipt number, a sales agent's name, a product code. The system does not require the user to know which module to look in — the search figures it out.

When the user wants to narrow the search to a specific module ("only contracts", "only expenses"), a single-click filter toggles the scope. The default is global; the narrowed view is on demand.

**Search respects data scope**

Every search query is filtered by the user's effective scope (3.4). A sales rep searching for "Polidoro" finds the Polidoro contract they own; the same search by another rep does not return it (unless the second rep has scope that includes it). The Owner's search returns everything matching across all modules and all scope.

This is enforced at the query layer. A user cannot construct a search that would return records outside their scope — the search engine refuses to surface what the user does not have visibility into.

**Saved filters and shared views**

Frequent search patterns become saved filters. "My Nigeria contracts with outstanding balance", "Mega Clima 2026 exhibitors who haven't submitted catalogue", "All Morocco-based contacts in HVAC sector" — these are constructed once and re-run from a personal saved-filter library.

Saved filters are personal by default — each user maintains their own library, visible only to them. Managers and the Owner can additionally **share** specific saved filters with their team or with named users. A Sales Manager who builds a particularly useful "team pipeline review" filter can push it to their team leads as a shared view; the team leads see it in their saved-filter library and can run it without rebuilding.

Shared filters retain authorship — a recipient can see who shared the filter and can ask for changes — and respect the recipient's data scope. A filter shared with someone whose scope is narrower than the original author's filter scope returns the intersection: the filter's logic applied within the recipient's scope. Sharing a filter does not grant data access.

**Navigation between related records**

Navigation between related records is fluid. From a contract, one click reaches:
- The company the contract belongs to
- The contact who signed it
- The expo it is for (and from there, the expo's other contracts, partners, floor plan)
- The sales agent who closed it (and from there, that agent's other contracts)
- The Revenue records associated with it
- The communication history with the exhibitor
- The catalogue submission for this contract

Each one of those reached records is itself a hub with its own outbound links. The user can move through the data graph naturally without needing to remember which module they came from or how to construct the query that would return the related set.

Navigation history is preserved per user — the system remembers the last several records visited, so the back button works as expected and the user can return to where they were after a detour.

**Recent and pinned**

The user's working set is surfaced through two complementary mechanisms:

**Recent items** — the last several records the user opened, regardless of module, accessible from a persistent menu. This handles the natural pattern of returning to whatever was just being worked on.

**Pinned items** — explicitly bookmarked records, expos, saved filters, or dashboards. A user working intensely on one expo for a month pins it; the pinned items list keeps it one click away regardless of recency. Pins are personal.

**Must be better than today**

- **Global search across every module the user has scope on.** No more guessing which module to search; one query, ranked cross-module results.

- **Saved filters are personal, shareable when useful.** Each user builds their own library; managers can share curated views downward without forcing them.

- **Search and filters respect data scope automatically.** Sharing a filter doesn't grant access; running a search doesn't reveal records outside the user's authority.

- **Fluid navigation between related records.** Contract → company → contact → expo → other contracts at that expo, all without rebuilding queries. The data graph is traversable in clicks.

- **Recent and pinned for the working set.** What the user touched recently and what they care about long-term are both one click away.

### 3.8 Notification System

**The principle**

The notification system is the proactive voice of ELL. It tells users what they need to know without their having to ask. It runs across **three channels** — in-app, email, and WhatsApp — in that priority order. Users **configure their own** notification preferences within the bounds the Owner sets, and they can **mute or snooze** specific notifications when they need quiet time.

**Three channels, in priority order**

Each notification can fire on one or more of three channels:

**In-app notifications** are the primary channel. A bell icon in the system header surfaces unread notifications. They appear in real time when the user is in the system and accumulate when the user is away. This is the default-on channel for every notification — if the user is in the system, they should not need another channel to find out about the event.

**Email notifications** carry the same content to the user's inbox. They are valuable for events the user might miss while away from the system, for events that warrant a written record, and for users whose work day is centered on email rather than on continuous system access. Email is the second priority — important events go here in addition to in-app.

**WhatsApp notifications** are the third channel, reserved for the most time-sensitive or mobile-first events. The Owner already uses WhatsApp as their primary mobile interface (via ELIZA's bot); other users can opt into WhatsApp delivery for specific notification types where mobile responsiveness matters. WhatsApp is selective by default — not everything goes there.

A single notification event can fire on multiple channels simultaneously. A new contract signing might fire in-app + email for the sales rep who closed it, plus WhatsApp for the Owner who wants the morning summary on phone. The same logical event reaches different audiences on the channels that suit them.

**What gets notified**

The notification catalog covers the events users would otherwise have to discover by checking. A non-exhaustive list:

- **Sales-side events** — Quote signed, new lead assigned, lead replied, contract converted, commission paid
- **Project-side events** — Catalogue submission received, stand design approved, payment received against contract, exhibitor reply requiring response
- **Owner-level events** — Daily morning brief, weekly summary, AI-detected anomaly, refund or exception request awaiting approval
- **Operational alerts** — Email send failures, integration errors, expo deadline warnings, contract status anomalies
- **Permission and identity events** — Permission matrix changed by another user, hierarchy position updated
- **Reminders** — Self-set reminders, calendar-based prompts ("expo X is in 30 days")

The catalog is extensible. New modules and new automations contribute their notification events as the system evolves.

**Per-user preference, within Owner-set defaults**

Each user controls their own notification preferences: which events they receive, on which channels. A sales rep who wants in-app for everything plus email only for contract signings configures it that way. A team lead who wants WhatsApp for team-related events but in-app only for everything else sets it accordingly.

The Owner sets system-wide defaults for new users — when a user is created, their notification preferences start at sensible defaults aligned with their profile template. From there the user adjusts as they learn what works for them.

A small set of notifications are **mandatory** — events the Owner has designated as must-receive (a refund request awaiting approval that the user is the approver for, for example). These cannot be muted. The mandatory list is short by design; over-reliance on mandatory notifications produces fatigue and ignored alerts.

**Mute and snooze**

Notifications support temporary silencing. A user heading into a meeting can snooze all notifications for an hour. A user on vacation can snooze for the duration of their leave. A user uninterested in a specific notification type for a project's duration can mute that type for a week.

Snooze and mute are temporary by design — they expire automatically. Permanent silencing of a notification type is done through the preferences (turn it off in the matrix), not through indefinite snoozing. This keeps the user's preference state honest: the matrix reflects what the user wants long-term; snooze reflects what the user wants right now.

Mandatory notifications cannot be muted but can be snoozed for short durations (a few hours) so the user can finish a focused task without losing the alert entirely.

**Notification history and read state**

In-app notifications accumulate in a history that the user can scroll through. Read and unread states are tracked per user per notification. A user who dismissed a notification can recall it from history when needed.

Notification history follows the same retention principle as the audit log (3.6) — recent history is queryable in seconds, older history is archived. The exact window is operational rather than architectural — long enough to support the user's working memory, short enough to keep the interface responsive.

**Must be better than today**

- **Three channels at the user's command.** In-app for system presence, email for inbox-centric workflows, WhatsApp for mobile and high-priority. Each notification can fire on the channels that fit it.

- **Per-user preferences within Owner-set defaults.** Users tailor their own alert mix; new users start with sensible defaults from their profile template.

- **Mute and snooze are temporary by design.** Quiet time is a tactical tool, not a way to permanently disable alerts. Permanent silencing is a preference change with audit trail.

- **Mandatory notifications are short and intentional.** A few must-receive alerts for the right reasons, not a culture of forced noise.

- **Notification history is queryable.** Users recover dismissed alerts from history; the system does not silently drop information that mattered.

### 3.9 Integration Points

**The principle**

ELL is the source of truth for Elan Expo's commercial and operational data. External integrations are **deliberate and bounded** — added when a real operational need is identified, not because integration is fashionable. The current generation of ELL is **standalone** for the most part; key integrations are explicitly Phase 2 or later.

**Online payment collection — Phase 2**

Online payment collection (Stripe, iyzico, or similar) is **out of scope for the initial ELL build**. Today's payment flow — bank transfer, SWIFT, occasional cash — works and is well understood. International exhibitors arrange wire transfers; local exhibitors sometimes pay in cash to local offices; both are captured in the Revenue model (2.6) without needing a payment-gateway integration.

This becomes a Phase 2 priority when the operational benefit is clear. Likely triggers:
- Exhibitor friction with current bank-transfer flow becomes a measurable conversion problem
- The volume of online-prefer customers grows large enough to justify the integration
- A specific market (e.g., European exhibitors expecting card payment) demands it

When the time comes, the integration shape is straightforward: an exhibitor receives a payment link tied to their contract, completes the payment on the gateway, and the system records a Revenue automatically — same shape as a manually-entered Revenue, with the gateway transaction as the source-of-truth reference.

**Accounting software export — to be designed when needed**

Today, the company's accountant does not pull data from Zoho. There is no existing export pipeline to replicate. This means ELL is not under pressure to reproduce a specific output format from day one — there is no "current process" to maintain.

When the accountant's actual needs are scoped — what data, what format, what cadence — the export is designed to fit those needs. Options include direct system access for the accountant (with appropriate read-only permissions), scheduled email-delivered exports in standard formats (Excel, CSV), or eventual integration with specific accounting software the accountant uses. The choice depends on what the accountant actually needs, not on what is technically possible.

This work is deferred until the accountant's requirements are documented. It is a Phase 2 conversation between the Owner, the accountant, and whoever architects the export.

**Turkish e-invoice / e-arşiv — later**

Turkish tax compliance includes e-invoice (e-fatura) and e-archive invoice (e-arşiv) requirements for transactions that fall under specific thresholds and counterparty categories. Today, the company's accountant handles invoice issuance manually, after payments are received.

ELL automating e-invoice issuance is **not a Phase 1 priority**. The current manual flow works, and the integration with Turkish e-invoice systems involves regulated APIs, specific certificate management, and ongoing compliance with evolving tax authority requirements. Building this prematurely creates maintenance burden without solving a current pain.

This becomes relevant when:
- The accountant's manual process becomes a bottleneck
- The volume of invoices grows beyond manual capacity
- Tax authority requirements change in ways that demand automation

When the time comes, ELL's contract and payment data already contains everything needed to produce e-invoices — the integration is a writing layer on top of existing data, not a new data model.

**Email infrastructure**

Outbound email today flows through Zoho's mailing infrastructure (for marketing) and Gmail (for operational, via Yaprak's and Finance's mailboxes). ELL's email subsystem (2.7) replaces both — outbound operational and marketing emails go through ELL's chosen email service provider, with full template rendering, send tracking, and reply capture handled inside ELL.

Inbound email (replies from exhibitors) is captured into the contract's communication history (2.7). The mechanism — direct IMAP integration with the existing Gmail accounts, a forwarding-to-system-mailbox arrangement, or another approach — is an architecture decision. The need is: replies arrive on the contract page regardless of which mailbox they technically landed in.

**Other integrations — explicit non-goals for Phase 1**

The following are explicitly out of scope for the initial ELL build:

- **LinkedIn Sales Navigator or similar prospecting platforms** — sales reps may use these tools manually, but no system-level integration
- **External marketing platforms** (Mailchimp, HubSpot, etc.) — ELL handles its own marketing campaigns
- **Calendar integrations** (Google Calendar, Outlook) — meetings are not tracked in ELL (Tasks/Meetings/Calls were a known Zoho adoption failure; ELL does not repeat the attempt)
- **Voice/telephony integrations** (call logging) — same reasoning
- **Document management beyond Drive links** — uploaded documents in ELL are stored as Drive URLs (signed contract scans, stand designs, catalogue submissions); deeper document management is not a current need
- **HR systems** — user identity is managed inside ELL; payroll integration is not needed because commission is its own flow and salaries are tracked as Expenses without external reconciliation

Each of these can become a Phase 2 priority if a real operational pain emerges. The principle is: integration is added when it solves a known problem, not in anticipation of generic capability needs.

**Internal API surface**

The three subsystems (ELIZA, LIFFY, LEENA) communicate with each other via internal APIs. Reference data is replicated across them; operational data flows according to ownership rules established in earlier sections (2.5 covers exhibitor data flow from contracts in ELIZA to LEENA, for example).

The exact API surface and the eventual question of whether the three-system split should continue, merge, or restructure are architectural decisions for the next phase. The need this section captures is: integration between the subsystems must be reliable, must preserve data integrity, and must not require manual reconciliation by users.

**Must be better than today**

- **Online payment collection as a deliberate Phase 2 addition.** Not built prematurely, but the data model is ready when the trigger comes.

- **Accounting export designed to the accountant's actual needs.** No premature export pipeline reproducing nothing useful; the export is built when the requirements are real.

- **Turkish e-invoice automation when the manual process bottlenecks.** Today's manual flow works; ELL automates when manual capacity becomes the constraint.

- **Email infrastructure inside ELL, not borrowed from Zoho.** Marketing and operational email both run through ELL's send and receive infrastructure, with full audit and history.

- **Explicit non-goals listed.** LinkedIn, calendar, voice, deep document management, HR — all outside Phase 1 by deliberate choice. Integration is added when the pain demands it, not because the capability is fashionable.

- **Three-subsystem internal communication is reliable, not user-visible.** Whatever the architecture phase decides about the split, the user experience is one platform — not three systems the user has to mentally reconcile.

---

## Part 4 — "Better Than Zoho" Targets (Capability Wishlist)

This part synthesizes the "Must be better than today" subsections that closed each Part 2 workflow, plus capabilities that emerged in cross-cutting Part 3 sections. It is the answer to the central question of the project: **if ELL doesn't beat Zoho, why migrate?** Each capability listed here is a measurable improvement over the current state — a concrete way ELL must exceed what Zoho delivers today.

The targets fall into six categories: Automation (work the system does without human prompting), Intelligence (insight the system surfaces), Flexibility (configurability without code), Speed and UX (everyday friction removed), Cost Model (license and per-user economics), and Adaptability (capacity to evolve as the company evolves).

These are not aspirations. They are the success criteria. ELL's launch is judged against this list.

### 4.1 Automation

Today's Zoho leaves substantial repetitive work in human hands. ELL must eliminate this work category by category.

**Catalogue production fully automated.** The Project Department Lead must never open Corel Draw to make a catalogue again. Templates plus exhibitor self-submitted data plus a single click produce print-quality PDF and a public web catalogue. What today takes weeks becomes minutes.

**Eight-email announcement chain runs without supervision.** Once contract triggers and per-expo deadlines are configured, the chain delivers itself. Late-signed contracts trigger the "send all now" action; standard-cycle contracts run on the spread schedule; resends and re-deliveries are one-click; failures surface as alerts, not silent gaps.

**Lead enrichment and disqualification become low-friction.** Reply parsing extracts sender name, company, and signature data automatically; one-click enrichment turns a clue into a Contact + Company. Disqualification is fast and reversible with categorized reasons — lead enrichment stops being the work nobody bothers to do.

**Quote subject auto-generated from linked records.** No more typos in `{ExpoName}-{CompanyName}-{M²}` strings. The system constructs the subject from the data; manual override remains available but is not the default path.

**AF Number auto-assigned with country prefix at the right moment.** Q-prefix on creation, A-prefix on conversion, sequence preserved. No human types these strings.

**Sales Contract status changes propagate consequences automatically.** Cancellation produces credit-balance entries, commission adjustments, and refund or credit decisions. Transfer creates the destination contract with carried-forward payments and commission attribution. Status is one action; consequences follow.

**Floor plan updates from Sales Contract events.** New contract assigns a stand suggestion; cancelled contract releases a stand. The Project department reviews and confirms; the system's first draft is correct most of the time.

**Form URLs auto-generated per expo.** When a new expo is created, the system mints catalogue submission URL, stand design URL, visitor pre-registration URL — no manual field-filling, no per-expo Zoho Forms creation.

**Email replies attached to the contract.** Inbound replies arrive on the contract's communication history regardless of which mailbox technically received them. The relationship's record assembles itself.

**Push reports compiled and delivered on schedule.** Morning brief, weekly summary, deadline-warning digest, team performance roundup — all generated from current data at the configured time, delivered to the configured channel and recipient. Nobody assembles these manually.

**Audit and modification trails captured passively.** Every significant change writes to the audit log; every record edit writes `modified_by` and `modified_at`. The historical record assembles itself as a side effect of work.

### 4.2 Intelligence

Beyond automating the work people do today, ELL surfaces insight people don't know to ask for.

**Trend detection across expo cycles.** The system compares this expo's trajectory to its previous editions, this rep's pace to their historical baseline, this office's conversion rate to its peers. Meaningful divergences from established patterns surface as flagged insights, not as questions someone has to think to ask.

**Anomaly detection on activity and outcomes.** A week with zero data entry from an office that typically produces 50+ entries. A catalogue submission rate of 40% with two weeks to deadline where 70% is normal. A payment reminder that fired but produced no payment. Anomalies are often more valuable than trends — they identify problems before they crystallize.

**Action suggestions linking observation to next step.** "These three contracts have outstanding balance, the Payment Reminder fired two weeks ago, no payment received — escalate to the Sales Manager?" The system offers the next move; the human accepts, refines, or dismisses. Cognitive load drops without surrendering decision authority.

**Synthesis across data sources.** "Q4 stand sales for HVAC are 20% below budget; the same period saw a slowdown in Nigeria-office data entry; the two are likely related." The system attempts narrative interpretation when the data supports a clear story and stays silent when it doesn't.

**Natural-language report requests.** "How many leads in HVAC sector did we add from Nigeria in the last six months, broken down by sales rep?" produces the answer or produces a draft report the user can refine. Ad-hoc questions of the data become conversational, not technical.

**Per-expo profitability with budget variance.** Each expo's actual P&L sits next to its budget plan, with category-level breakdown. The Owner runs the business against plan, not against memory.

**Owner's mobile-first interface via WhatsApp.** Natural-language queries about any data the Owner has scope on, answered with phone-formatted summaries. The same intelligence layer; a different surface.

**Insight traceability — every number explorable to its source records.** Trust comes from verification. Every dashboard tile, every report row, every AI insight clicks through to the underlying records.

### 4.3 Flexibility

Zoho's structural rigidity is one of its most expensive limitations. ELL is built on configurable defaults rather than coded constants.

**Per-user permission matrix replaces fixed Profiles + Roles.** Every cell in every user's matrix is independently editable. Profile templates exist for fast onboarding but do not bind beyond user creation. Exceptions are normal, not workarounds.

**Hierarchy editable from admin UI.** Promotions, demotions, restructures, new layers added — all configurable. The system supports tomorrow's organization without requiring a code change.

**Reference data owned by the Owner.** Sectors, expense categories, expense types, revenue categories, accounts, payment methods, partner roles, profile templates — all editable through admin UI. New configurations are operational decisions, not engineering tickets.

**Per-expo trigger configuration.** Email send timing, catalogue deadline, stand design deadline, payment reminder window — all set per expo on the expo record. The same email engine serves expos with very different operational rhythms.

**Per-contract commission overrides.** Default rates on the sales agent record; per-contract override fields on the contract. No formula, no policy, no approval workflow — the Owner sets the percentage that fits the deal.

**Configurable defaults, overridable exceptions, throughout.** Privacy boundaries, partner-sharing decisions, language selection, notification channels, scope assignments — all defaults plus exceptions. The 95% case is automatic; the 5% case has a clear path.

**Account list dynamic.** New currencies, new offices, new account types added through admin UI. Three years from now's account structure does not require code changes today.

**Cluster vs standalone expo handling.** ELL recognizes co-located clusters as a first-class concept while supporting standalone expos as the default. The lifecycle of an expo — joining a cluster, leaving a cluster — is operational, not architectural.

### 4.4 Speed & UX

Daily friction in Zoho — slow loads, multi-step actions, context loss between modules — adds up to substantial wasted time across the team.

**Daily dashboards render in seconds.** Sales pace per expo, data-entry activity per office, outstanding payments per expo — the Owner's three daily views load instantly and stay current. No assembly from filtered modules.

**Global search across modules in one query.** Any name, any number, any AF Number, any keyword — one search, ranked cross-module results, scope-respecting. No more guessing which module to start in.

**Fluid navigation between related records.** Contract → company → contact → expo → other contracts at that expo, all in clicks. The data graph is traversable; the user is never stuck rebuilding queries to reach related data.

**Recent and pinned items always one click away.** The user's working set — what they touched recently, what they care about long-term — is persistently accessible from any screen.

**Bulk actions where they belong.** Reassign pipeline, send all operational emails, mark a batch of leads disqualified — actions that today require many clicks become one. The system does the loop.

**Visual floor plan editing.** Drag and drop, copy stand block, snap to grid, version control, color coding by status. The Project department interacts with the floor plan visually, not through coordinate fields in a form.

**Catalogue review with inline comments.** Project staff review submissions on the actual rendered catalogue page, leaving comments where the issue is. Exhibitors see the comment, fix the issue, resubmit. No back-and-forth email describing pixel positions.

**Saved filters, sharable views.** Build the search once, save it, run it from a sidebar — share it with the team when it's broadly useful. Repeated questions become saved answers.

**Mobile-first via WhatsApp for the Owner.** Phone-formatted answers to natural-language queries. Always-available companion to the desktop dashboard.

**No more mental reconciliation of three systems.** The user experience is one platform. The architecture phase will decide whether the underlying split persists; the user does not see it either way.

### 4.5 Cost Model

Zoho's per-user pricing is increasingly painful as the company adds external agencies, freelancers, and growing local offices. ELL's cost structure must reflect the reality of the business.

**Sales agents are not licensed users.** External agencies, freelancers, and inactive past staff exist as sales agent records, not as login accounts. Adding 50 commission-attributable agents does not require 50 user licenses.

**Data entry contractors are not licensed users.** Public forms accept their submissions; their attribution is tracked; they have no login.

**Reference data scales without per-record cost.** Adding 100 new expense types, 50 new partner roles, or 30 new accounts is operational configuration, not a billing event.

**Storage cost scales sub-linearly with audit-grade retention.** Email history, audit log, version preservation are accepted as the price of evidence — but archived after 24 months to keep hot-storage cost bounded. The system retains everything; it does not pay hot-storage prices for everything.

**Self-hosted infrastructure removes per-record economics.** Whatever the architecture phase decides about hosting, the cost model is not "$X per active record per month." Storage is bulk, compute is bulk, the marginal record costs effectively nothing.

**One platform replaces multiple Zoho modules and add-ons.** The cost saved is not just license fees on Zoho CRM — it is also Zoho Forms, Zoho Inbox, the various premium-feature surcharges that accumulate, and the time spent maintaining a deeply customized Zoho configuration that drifts from the company's actual needs.

### 4.6 Adaptability

The company three years from now will not be the company today. ELL must absorb that change without rewriting itself.

**New offices added without code changes.** A future Senegal office, a future Egypt office — created in admin UI, given accounts and currencies, given staff, working from day one.

**New currencies added without code changes.** Whatever the next market demands — added to the currency list, used immediately.

**New expense types, new revenue categories, new sectors, new product lines added without code changes.** The reference data inventory grows as the company grows.

**Hierarchy restructures without code changes.** New management layers, merged teams, split teams — handled through admin UI, scope updates immediately.

**New profile templates added when new role shapes emerge.** A future Customer Success role, a future Marketing Director role — defined as templates, applied at creation, available immediately.

**New email template types added without code changes.** A future operational email category — Visa Pre-Approval, Hotel Booking Reminder, Day-of-Show Logistics — added through admin UI, integrated into the per-expo trigger configuration.

**New notification types and channels addable.** When SMS becomes worth the integration, when push notifications matter, when a new internal channel emerges — added through configuration, with per-user preferences attached.

**The three-system architecture is not locked.** ELIZA + LIFFY + LEENA today; some other shape tomorrow if needs evolve. The requirements document does not prescribe the architecture; the architecture phase decides, and re-decides when the needs change.

**Phase 2 capabilities are scaffolded, not prebuilt.** Online payment, accounting export, e-invoice automation, exhibitor portal, B2B matchmaking — the data model anticipates them, the architecture allows them, the implementation arrives when the operational need is clear.

**The Owner controls the rate of change.** New capabilities are deliberate additions, not feature drift. ELL grows when growth is justified and stays stable when stability is the right answer.

---

## Part 5 — Out of Scope (Explicit Non-Goals)

This part lists what ELL is **deliberately not building** in its initial scope. Each item is here for a reason — either it solves no current pain, or the current Zoho behavior is itself the workaround that should not be reproduced, or the capability is genuinely valuable but belongs to a later phase.

The goal of being explicit about non-goals is to protect focus. A requirements document that lists everything as a possibility produces an architecture trying to satisfy everything. The Owner has chosen to carry forward only what serves the company's real operations.

### 5.1 Modules Zoho Has That We Don't Need

Zoho contains modules accumulated over a decade of usage. Several of them are not genuinely used today, and ELL does not reproduce them.

**Tasks, Meetings, Calls.** The Owner pushed adoption of these modules for years; the team did not adopt them. The reasons are real: data entry overhead, low payoff, friction with how sales work actually happens. ELL's Action Engine in LIFFY surfaces what users need to do without asking them to log activities they performed. The Tasks/Meetings/Calls modules are not migrated and not rebuilt.

**SalesInbox.** Replaced by Gmail-centric workflows plus ELL's email infrastructure (2.7). Operational email goes through Project's and Finance's mailboxes; marketing email goes through ELL's send infrastructure; reply capture is handled by integration. SalesInbox itself adds no value and is not migrated.

**Potentials / Deals.** Quote covers what was useful in this module. The pre-quote pipeline-stage abstraction (lead → suspect → prospect → potential → deal) added complexity without operational value at Elan Expo's scale. ELL's pipeline is lead → contact + company → quote → contract, with no intermediate Potentials stage.

**Purchase Orders, Invoices.** Outside ELL's commercial scope. Invoicing for tax purposes is the accountant's manual workflow (3.9); Purchase Orders are not part of how Elan Expo's exhibitor sales work. Both modules are abandoned.

**Feeds.** The internal social-feed module in Zoho was never operationally used. Not rebuilt.

**Cases, Solutions.** Customer-support ticketing is not Elan Expo's business pattern — exhibitor concerns flow through email and direct contact with the Project department, not a ticketing module. Not rebuilt.

**Forecasts.** Zoho's forecast module assumes a sales pipeline structure (deals with probability percentages, revenue forecasts by month) that does not match expo sales cycles (where deal probability is binary up to a deadline). Forecasting in ELL is built into the dashboards (sales pace per expo against target) rather than as a separate forecast module.

**Documents.** Zoho's document management is replaced by Drive links — signed contracts, stand designs, catalogue submissions are stored as URLs to Google Drive. Deeper document management is not a current need.

**Bodies / Expos legacy module.** Earlier organizational structure for expo records. Replaced by the modern Expos record in LEENA.

**LeadChain (Zoho Facebook lead sync).** Set up but never used. Not rebuilt.

**Stand Leads (Plus Design legacy).** Inherited from a prior partnership, not used by current operations. Not migrated.

### 5.2 Features Considered & Rejected

Some capabilities were discussed during requirements gathering and explicitly chosen not to build.

**Mobile native apps.** A native iOS or Android app for sales reps or for exhibitors is not a Phase 1 commitment. The Owner uses ELIZA's WhatsApp bot for mobile interaction; sales reps and the Project department work primarily on desktop. A mobile-responsive web interface (PWA, accessible from a phone browser) is acceptable; native apps are deferred.

**AR navigation, gamification, social features.** Visitor-facing capabilities like augmented-reality stand navigation, gamified visit completion, or social-feed integration with attendee networks were considered and rejected. They are interesting but solve no current problem at Elan Expo's scale.

**External marketplace integrations** for prospecting (LinkedIn Sales Navigator, ZoomInfo, Apollo, etc.). Sales reps may use these tools manually as they do today, but no system-level integration. The mining capability inside LIFFY produces enough leads from Elan Expo's own web sources; external prospecting platforms add cost without proportional return.

**Calendar integrations (Google Calendar, Outlook).** Meetings are not tracked in ELL — the Tasks/Meetings/Calls adoption failure (5.1) demonstrates that calendar-integrated meeting logs are not how this team works.

**Voice/telephony integrations** for call logging. Same reasoning. Sales calls happen; their content lands in email follow-ups, contact notes, or contract data. The call event itself is not separately logged.

**Customer self-service portal beyond Catalogue and Stand Design submission.** Exhibitors will manage their catalogue page and confirm stand design through secure links (2.4, 2.5), but a full exhibitor portal — login, dashboard, multi-expo history, peer messaging — is the future Lead Scanner / Exhibitor Portal vision (D27), not a Phase 1 deliverable.

**Multi-language UI.** The system UI is in English; Suer is comfortable with English and the team's working language already mixes English with Turkish. Translating the UI to Turkish, French, or Arabic is a future consideration if the team's composition changes.

**Bulk import beyond migration.** A persistent self-service bulk-import facility (Excel uploads by users for ongoing data injection) is not a Phase 1 capability. Migration imports are one-time and supervised; ongoing data flows through forms and integrations, not user-uploaded spreadsheets.

**Custom field creation by end users.** Power users in Zoho can sometimes add custom fields to modules; in ELL, schema additions are deliberate engineering decisions, not a self-service capability. Reference data and dropdowns are configurable; structural schema changes are not.

### 5.3 Future Considerations (Not Phase 1)

These are real capabilities the company expects to want, but not in the initial ELL build. They are listed so the architecture phase keeps them accessible without committing to them.

**Online payment collection (Stripe, iyzico, or similar).** Phase 2 priority when bank-transfer friction becomes a measurable conversion problem (3.9).

**Accounting software export.** Designed when the accountant's actual needs are scoped (3.9). Today the accountant pulls nothing from Zoho, so there is no current process to reproduce.

**Turkish e-invoice / e-arşiv automation.** Today's manual flow works; ELL automates when manual capacity becomes the constraint (3.9).

**Exhibitor Portal with login-based services.** Lead Scanner today is a free service to exhibitors via QR scanning; the future portal extends this to login-based multi-expo history, B2B matchmaking, pre-show appointment booking, post-show analytics for the exhibitor (D27).

**B2B Matchmaking between visitors and exhibitors.** Pre-show appointment booking, sectoral matching, on-site recommendations — a substantial Phase 2 capability that builds on Lead Scanner data.

**WhatsApp as an exhibitor-facing channel.** Internal WhatsApp use is current; exhibitor-facing WhatsApp messaging (operational alerts, payment reminders via WhatsApp) is a future addition (2.7).

**SMS notifications.** When the operational benefit emerges in markets where SMS is more reliable than email or WhatsApp.

**Public-facing sales agent profiles.** Names and photos used in customer communications — a future polish, not a Phase 1 need (3.2).

**Currency Exchange Gain/Loss tracking as actual transactions.** Today these are reference data placeholders only; the company does not currently maintain accounting tight enough to track them (2.6, D34). When financial discipline reaches the point where they become meaningful, the system records them.

**Approval workflow for reference data changes.** Today the Owner is the authority and the audit log is the safeguard (3.5). A formal approval workflow can be added if the company grows to a point where reference-data changes need pre-approval.

**Split-attribution for cross-expo expenses.** Today's practice attributes a regional marketing campaign to its largest beneficiary; multi-expo split attribution is added when a more precise attribution becomes operationally important (2.6).

**Federated reporting across separate ELL instances** (if a multi-tenant or multi-company structure ever emerges). Not relevant today.

**The decisions to defer all of these are deliberate.** Each could be built; each is held back because the operational need is either not yet sharp enough or the marginal value does not justify Phase 1 attention. As the business evolves, items move from this list into active scope through the same review process that produced this document.

---

## Part 6 — Appendices

### 6.1 Source Materials

This document was assembled from the following sources, in approximate order of authority:

**Primary — Owner walkthroughs and decisions.** Multi-session interviews with Suer Ay (Owner) covering Zoho usage, operational reality, organizational structure, and explicit decisions on every workflow. The DECISIONS_LOG.md captures 42+ confirmed decisions with the Owner's exact words where relevant. These conversations are the document's primary authority.

**Secondary — ZOHO_USAGE_REFERENCE.md.** A walkthrough of the current Zoho CRM configuration: 13 active modules, ~75 expense types, 15 revenue categories, 8 email automation chains, 587K leads, 18K companies, 202 expos. This document describes what Zoho does today, used as reference for ELL gap analysis but not as a blueprint. ELL is not a Zoho clone.

**Tertiary — Zoho screenshots and email samples.** Specific operational details (the eight-email Announcement chain, the Sales Contract field structure, Quote subject formatting, multi-currency receipt examples, third-party payer email threads) were verified against captured Zoho screens and a real email thread including a third-party payer scenario. These artifacts grounded the requirements in operational reality.

**Quaternary — existing ELL documentation.** Some existing ELL planning documents (ELL_RULES, ADRs, ROADMAP, RFCs in the separate ell-docs repo) were considered as background context but explicitly excluded from this document's project knowledge. Those documents were written before proper requirements gathering and contain solution decisions that may conflict with the needs captured here. They will be revised after this document is finalized.

This document supersedes all prior need-definition material. Architectural and roadmap documents that follow will use this as input.

### 6.2 Glossary

Selected terms used throughout the document:

**ELL** — informal shorthand for ELIZA + LIFFY + LEENA, the three subsystems that together replace Zoho CRM. The name has no marketing meaning.

**ELIZA** — the commercial system of record plus intelligence layer. Hosts financial data, sales contracts, expo financial summary, expense and revenue categorization, the War Room dashboard, the WhatsApp bot for the Owner. Most mature of the three subsystems.

**LIFFY** — the sales action engine and CRM. Hosts leads, contacts, companies, quotes (planned), outreach campaigns, mining results, the Action Screen for sales reps. Phase 1 MVP in progress.

**LEENA** — operations execution. Hosts expos, visitors, floor plans, stands, check-ins, lead scanner data. Catalogue Generator is planned (currently manual in Corel Draw — eliminating this is one of the biggest motivations for ELL).

**Expo** — Elan Expo's term for its specific events. Used consistently in this document. "Trade fair" or "trade exhibition" appear only as generic industry terms.

**Cluster** — two or more co-located expos at the same venue on the same dates, operationally one event but commercially separate. A first-class concept (D28).

**AF Number** — the contract identifier ("Application Form" — origin obscure, retained because it's institutional). Format: `Q{ISO}-{Sequence}` while in Quote stage, `A{ISO}-{Sequence}` after conversion to Sales Contract. Same sequence; prefix flips at Convert.

**Convert** — the Project department's action that turns a signed Quote into a Sales Contract, and turns a Lead into a Contact + Company. The structural boundary between Sales-side and Project-side work (D12).

**Lead** — an anonymous clue, almost always just an email. Most never reply; most who reply are not real prospects. Distinct from a qualified prospect (D7). The system holds 587K leads precisely because they cannot be filtered at acquisition time.

**Sales Agent** — an entity to whom commission can be attributed on a Sales Contract. Includes internal employees, external agencies, freelancers, and inactive past staff. ~150 records. Most sales agents are NOT system users (D41).

**User** — a person with system login credentials. ~25 active users today.

**Owner** — the founder/CEO role at Elan Expo, currently held by Suer Ay. Combines Owner and CEO functions until a dedicated CEO is hired.

**Project Department Lead** — the head of the Project department (post-signature operations). Currently Yaprak.

**Sales Manager** — the head of the sales organization. Currently Elif.

**Sales Team Lead** — a recently emerged middle layer between Sales Manager and individual reps. Currently Bengü.

**HQ** — Istanbul headquarters.

**Local office** — Morocco, Nigeria, Kenya, China, Algeria, Ghana offices.

**Operational email** — Welcome, Catalogue Form, Stand Design, Boost, Extra Service, BuildUp Rules, Payment Reminder, Badge — and other contract-triggered or expo-deadline-triggered communication. Distinct from marketing campaigns (2.7).

**Marketing email / campaign** — outbound prospecting email run by the sales side, subject to opt-out compliance. Distinct from operational email (2.7).

**Two-sided money movement** — the central financial principle: every transfer between accounts produces both an outflow and an inflow, linked as one logical event (3.3).

**Frozen exchange rate** — a rate captured at transaction entry time and never silently recomputed (3.3).

**Owner's current account** — a virtual account representing the Owner's claim on the company (or vice versa). Records the company's debt to the Owner when the Owner pays for company expenses out of personal funds (2.6).

**Computed balance** — account balances, credit balances, outstanding amounts, commission adjustments are all sums over their respective transaction streams, not denormalized stored fields (2.6, 3.3).

**Per-user permission matrix** — the per-user record specifying which actions on which records each user can perform. Profile templates seed it; from creation it is independent (3.1).

**Profile template** — a named permission preset used at user creation. Owner, Project Department Lead, Project Staff, Sales Manager, Sales Team Lead, Sales Rep, Local Office Sales, Local Office Project, Finance, Admin (3.1).

**Hayalet rapor** — Suer's term for a Zoho report that was created for a specific question and then never opened again. Identified during migration review and not carried forward (2.8).

**Anti-pattern: Don't replicate Zoho's bookkeeping fields.** Many Zoho fields exist as workarounds for Zoho's reporting limitations at the time they were created (e.g., Payment Done ✓, Validity 05/26). ELL must NOT replicate them — they become computed queries instead (D2).

### 6.3 Document Maintenance

**Authority.** This document is the canonical source for what Elan Expo needs from ELL. When this document conflicts with any prior ELL planning material — ELL_RULES, ADRs, ROADMAP, RFCs — this document wins. Prior documents will be updated, archived, or rewritten in the architecture phase that follows.

**Updates during the architecture phase.** After this document is finalized, the architecture phase will produce solution-level decisions: which subsystem owns which data, how subsystems communicate, what the database structure looks like, what the API contracts are, what the migration sequence is. Those decisions live in their own documents. This requirements document is updated only when **needs** change, not when solution choices are made.

**Updates as the business evolves.** As Elan Expo grows, opens new offices, adds new sectors, restructures, or changes its operational rhythms, this document is revised to capture the new reality. Each revision increments the version number and adds a Version History entry describing what changed.

**Review cadence.** A full review of this document is recommended annually, or when a significant reorganization or strategic shift makes any current section feel stale. Smaller targeted revisions happen as needs emerge.

**Authorship.** Suer Ay (Owner) is the authority on every claim in this document. Drafting was done collaboratively with AI assistance; final wording reflects the Owner's confirmation. Future revisions follow the same model: the Owner directs; the writing serves the Owner's understanding.

**Distribution.** This document is shared with anyone who will design, build, or operate ELL. A future engineering team reading this should be able to understand not just what the system does, but why it does it that way — and what would make it better.

### 6.4 Version History
- v0.1 (2026-05-06): Skeleton structure proposal
- v0.2 (2026-05-06): Part 1 (Company & Context) filled, structure simplified per Owner feedback (System Layout + Open Decisions removed, Notification System added, email template fact corrected)
- v0.3 (2026-05-06): Part 1 finalized — names replaced with positions, expo count corrected to 10–15/year, Owner role clarified as combined with CEO until separation
- v0.4 (2026-05-08): Part 2.6 (Financial Operations) filled — multi-account ledger, two-sided money movements as central principle, Owner's current account, frozen per-transaction exchange rates, one Revenue per payment, budget vs actual, credit balance as computed value
- v0.5 (2026-05-08): Part 2.7 (Communication Automation) filled — operational vs marketing tracks, eight-email chain with per-expo triggers, "send all now" for late-signed contracts, three-language template variants, unsubscribe scoped to marketing, inbound replies on contract, WhatsApp internal-first
- v0.6 (2026-05-08): Refinements — audit-grade email history (full rendered content stored), multi-mailbox sender identities (Project vs Finance), reply routing by sender mailbox, third-party payer scenario added to Part 2.6 Revenue records
- v0.7 (2026-05-08): Part 2.8 (Reporting & Intelligence) filled — three daily Owner views, push reports per role, ad-hoc reports via builder + natural-language AI, four AI insight categories, hierarchical visibility default, three reporting axes (operational/financial/productivity), mobile-first via WhatsApp, traceability mandatory. Part 2 complete.
- v0.8 (2026-05-08): Part 3.1 (Permission & Access Control), 3.2 (Identity & User Management), 3.3 (Multi-Currency & Multi-Account), 3.4 (Hierarchical Visibility & Data Scope), 3.5 (Reference Data Management) — synthesis of cross-cutting principles from Part 2 plus profile templates list (10 templates), three-identity-concept separation (users/agents/contractors), four multi-currency mechanics, scope composition rules, reference data inventory.
- v0.9 (2026-05-08): Part 3.6 (Audit & History), 3.7 (Search & Navigation), 3.8 (Notification System), 3.9 (Integration Points) — 24-month rolling audit retention with archive, global search respecting scope, three notification channels (in-app/email/WhatsApp) with per-user preferences, online payment + e-invoice + accounting export deferred to Phase 2. Part 3 complete.
- v1.0 (2026-05-08): Part 4 ("Better Than Zoho" Targets), Part 5 (Out of Scope), Part 6 (Appendices) added. Document complete and ready as input for the architecture phase.

---

*This document is the canonical requirements source for ELL system design. When this document conflicts with ELL_RULES, ADRs, or roadmap documents, this document wins — and the others must be updated.*
