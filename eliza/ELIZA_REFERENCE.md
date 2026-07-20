# ELIZA — Referans (Zoho Field Mapping / War Room)

Bu dosya `CLAUDE.md`den ayrıldı (20 Temmuz 2026). Otomatik yüklenmez; gerektiğinde okuyun.

---

# 14. Zoho Sales Contracts Field Mapping

Module API name: Sales_Orders

| Field Label              | API Name                  | Data Type              |
|--------------------------|---------------------------|------------------------|
| 1. Date/Amount/Type      | Date_Amount_Type          | Single Line            |
| 2. Date/Amount/Type      | Date_Amount_Type2         | Single Line            |
| 3. Date/Amount/Type      | Date_Amount_Type1         | Single Line            |
| 4. Date/Amount/Type      | Date_Amount_Type4         | Single Line            |
| 5. Date/Amount/Type      | Date_Amount_Type3         | Single Line            |
| 1st Payment              | st_Payment                | Currency               |
| 1st Payment Details      | st_Payment_Details        | Single Line            |
| 2nd Payment              | nd_Payment                | Currency               |
| 2nd Payment Details      | nd_Payment_Details        | Single Line            |
| Adjustment               | Adjustment                | Currency               |
| Advertising              | Advertising               | Pick List              |
| AF Number                | AF_Number                 | Single Line (Unique)   |
| Agent %                  | Agent                     | Percent                |
| Agent Com. Done          | Agent_Com_Done            | Boolean                |
| Agent Commission         | Agent_Comission           | Formula                |
| Agent Commission Paid    | Agent_Comission_Paid      | Currency               |
| Agent Commissions Note   | Agent_Comissions_Note     | Multi Line             |
| Agent Name               | Agent_Name                | Pick List              |
| Agent Registration Fee   | Agent_Registration_Fee    | Currency               |
| Badge                    | Badge                     | Boolean                |
| Balance                  | Balance                   | Formula                |
| Balance Details          | Balance_Details           | Single Line            |
| Balance.                 | Balance1                  | Formula                |
| Billing City             | Billing_City              | Single Line            |
| Billing Code             | Billing_Code              | Single Line            |
| Billing Country          | Billing_Country           | Single Line            |
| Billing State            | Billing_State             | Single Line            |
| Billing Street           | Billing_Street            | Single Line            |
| Boost Mail               | Boost_Mail                | Boolean                |
| BuildUp Rules Email      | BuildUp_Rules_Email       | Boolean                |
| Carrier                  | Carrier                   | Pick List              |
| Catalogue form mail      | Katalog_Formu_Maili       | Boolean                |
| Catalogue Page           | Catalogue_Page            | Lookup                 |
| Company Name             | Account_Name              | Lookup                 |
| Connected To             | Connected_To__s           | MultiModuleLookup      |
| Contact Name             | Contact_Name              | Lookup                 |
| Contract Date            | Contract_Date             | Date                   |
| Country of Company       | Country                   | Pick List              |
| Created By               | Created_By                | Single Line            |
| Currency                 | Currency                  | Pick List              |
| Customer No.             | Customer_No               | Single Line            |
| Description              | Description               | Multi Line             |
| Discount                 | Discount                  | Currency               |
| Due Date                 | Due_Date                  | Date                   |
| Exchange Rate            | Exchange_Rate             | Decimal                |
| Excise Duty              | Excise_Duty               | Currency               |
| Expo Date                | Expo_Date                 | Date                   |
| Expo Name                | Expo_Name                 | Lookup                 |
| Extra Freight Price      | Ektra_Navlun_Fiyati       | Currency               |
| Extra Service Mail       | Ek_Hizmetler_Maili        | Boolean                |
| Free M2                  | Free_M2                   | Number                 |
| Freight                  | Navlun                    | Decimal                |
| Grand Total              | Grand_Total               | Formula                |
| Internal Notification    | Announcement              | Boolean                |
| M2                       | M2                        | Number                 |
| Modified By              | Modified_By               | Single Line            |
| Navlun Hakedisi          | Navlun_Hakedisi           | Number                 |
| Net Total                | Net_Total                 | Formula                |
| Ordered Items            | Ordered_Items             | Subform                |
| Payment Done             | Payment_Done              | Boolean                |
| Payment Method           | Payment_Method            | Multiselect            |
| Payment Reminder         | Payment_Reminder          | Boolean                |
| Pending                  | Pending                   | Single Line            |
| Potential Name           | Deal_Name                 | Lookup                 |
| Purchase Order           | Purchase_Order            | Single Line            |
| Quote Name               | Quote_Name                | Lookup                 |
| Reason for Cancellation  | Reason_for_Cancellation   | Multi Line             |
| Received Payments        | Received_Payment          | Subform                |
| Registration Fee         | Registration_Fee          | Currency               |
| Remaining Payment        | Remaining_Payment         | Formula                |
| Sales Agent              | Sales_Agent               | Lookup                 |
| Sales Commission         | Sales_Commission          | Currency               |
| Sales Contract Owner     | Owner                     | Lookup                 |
| Sales Group              | Sales_Group               | Pick List              |
| Sales Type               | Sales_Type                | Pick List              |
| Scan Link                | Scan_Link                 | URL                    |
| SD %                     | SD                        | Percent                |
| SD Com. Done             | SD_Com_Done               | Boolean                |
| SD Commission            | SD_Comision               | Formula                |
| SD Commission Notes      | SD_Comision_Notes         | Multi Line             |
| SD Commission Paid       | SD_Comision_Paid          | Currency               |
| SD Commission Remaining  | SD_Remaining_Payment      | Formula                |
| Send Them All Now        | Hepsini_Hemen_Gonder      | Boolean                |
| Shipment Deadline        | Shipment_Deadline         | Boolean                |
| Shipment Volume          | Shipment_Volume           | Decimal                |
| Shipping City            | Shipping_City             | Single Line            |
| Shipping Code            | Shipping_Code             | Single Line            |
| Shipping Country         | Shipping_Country          | Single Line            |
| Shipping State           | Shipping_State            | Single Line            |
| Shipping Street          | Shipping_Street           | Single Line            |
| SO Number                | SO_Number                 | Long Integer           |
| SR %                     | SR                        | Percent                |
| SR Com. Done             | SR_Com_Done               | Boolean                |
| SR Commission            | SR_Prim_S                 | Formula                |
| SR Commission Notes      | SR_Comision_Notes         | Multi Line             |
| SR Commission Paid       | Prim                      | Currency               |
| SR Commission Remaining  | Prim_Remaining            | Formula                |
| Stand Design Link        | Stand_Design_Link         | URL                    |
| Stand Design Mail        | Stand_Cizimi_Mali         | Boolean                |
| Stand Type               | Stand_Type                | Pick List              |
| Status                   | Status                    | Pick List              |
| Sub Total                | Sub_Total                 | Formula                |
| Subject                  | Subject                   | Single Line            |
| Tag                      | Tag                       | Single Line            |
| Tax                      | Tax                       | Currency               |
| Terms and Conditions     | Terms_and_Conditions      | Multi Line             |
| Total M2                 | Total_M2                  | Formula                |
| Total Payment            | Total_Payment             | Formula                |
| Transportation           | Transportation            | Pick List              |
| Validity                 | Validity                  | Pick List              |
| Website                  | Website                   | Single Line            |
| Welcome Mail             | Hosgeldiniz_Maili         | Boolean                |

Primary fields for ELIZA sync:
- AF_Number → contracts.af_number
- Account_Name → contracts.company_name
- Country → contracts.country
- Sales_Agent → contracts.sales_agent
- Expo_Name → contracts.expo_id (lookup)
- Contract_Date → contracts.contract_date
- M2 → contracts.m2
- Grand_Total → contracts.revenue
- Status → contracts.status
- Sales_Type → contracts.sales_type
- Total_M2 → reference for pavilion calculations
---

---

# 15. War Room Dashboard

Location: apps/dashboard (Next.js)
Running on: http://localhost:3000

Pages:
- / → War Room main dashboard
- /expos?year=2026&expo=SIEMA&country=Morocco → Expo Directory (sortable, filterable, export: Copy/CSV/Excel/PDF)
- /expos/detail?name=SIEMA&year=2026 → Expo Detail (agents, companies, countries, monthly trend, export)
- /sales → Fiscal Sales (period filters, KPIs with change%, agent/expo/country tables, trend chart, export)
- /finance → Collections Cockpit (KPI cards, action list, aging chart, upcoming, expo/agent tables, drawer, export)
- /login → Login page (email/phone + password)
- /settings → User settings (change password, logout)

Navigation (all pages — unified via components/Nav.js):
- Order: War Room | Expo Directory | Sales | Finance | Targets | Logs | Intelligence | System | Users | Settings
- Active page highlighted with accent color
- Nav component: components/Nav.js (single source of truth)

Design System:
- CSS: styles/design-system.css (single source for all tokens, classes, responsive)
- No more per-page CSS variable declarations or duplicate styles
- Classes: .page, .page-hdr, .page-brand, .nav-link, .tbl, .summary-row, .summary-card, .btn, .btn-sm, .btn-primary, .btn-danger, .btn-success, .badge, .badge-success, .badge-danger, .input, .input-label, .section-title, .section-hdr, .loading, .export-bar, .export-feedback
- Responsive: @media (max-width: 768px) and @media (max-width: 480px) in design-system.css
- Page-specific styles: kept in <style jsx> blocks (not global)

Auth System:
- Login: /login → POST /api/auth/login → JWT token → localStorage
- Session: Bearer token in Authorization header
- AuthProvider: lib/auth.js wraps _app.js
- AuthGuard: redirects to /login if no token
- Password: bcrypt, min 6 chars
- Remember me: 30 day token vs 24h default
- CEO can set passwords via POST /api/auth/set-password
- Migration: packages/db/migrations/011_user_auth.sql (password_hash, last_login, dashboard_permissions)
- dashboard_permissions JSONB: { war_room, expo_directory, expo_detail, sales, finance, targets, logs, intelligence, system, users, settings }
- Initial CEO password: eliza2026 (change in production)

Expo Directory → Detail:
- Table rows clickable → navigates to /expos/detail?name=X&year=Y
- WhatsApp links can point to /expos/detail?name=X&year=Y

Sales → Expo Detail:
- Expo table rows clickable → navigates to /expos/detail?name=X&year=Y

API endpoints used:
- GET /api/revenue/summary → fiscal KPIs
- GET /api/revenue/edition-summary → edition KPIs (supports ?year=2026)
- GET /api/expos/metrics → upcoming expos (supports ?year=2026)
- GET /api/sales/leaderboard → top agents (always visible)
- GET /api/expos/detail?name=X&year=Y → expo summary (name, country, date, target, sold, revenue, progress, risk)
- GET /api/expos/detail/agents?name=X&year=Y → agent breakdown
- GET /api/expos/detail/companies?name=X&year=Y → company list
- GET /api/expos/detail/countries?name=X&year=Y → country distribution
- GET /api/expos/detail/monthly?name=X&year=Y → monthly sales trend
- GET /api/fiscal/summary?period=year → fiscal KPIs with change% (supports period=today/week/month/year or from+to)
- GET /api/fiscal/by-agent?period=year → agent performance for fiscal period
- GET /api/fiscal/by-expo?period=year → expo breakdown for fiscal period
- GET /api/fiscal/by-country?period=year → country breakdown for fiscal period
- GET /api/fiscal/trend?period=year&granularity=monthly → sales trend (daily/monthly)
- GET /api/finance/summary?mode=edition|fiscal → 8 finance KPIs (contract_value, collected, outstanding, overdue, due_next_30, collection_rate, at_risk, no_payment_count)
- GET /api/finance/action-list?mode&stage&risk&expo&agent&search&sort&order&limit&offset → outstanding_balances rows + suggested_action
- GET /api/finance/aging?mode=edition|fiscal → 6 aging buckets
- GET /api/finance/upcoming?days=30&mode → scheduled payments due within N days
- GET /api/finance/by-expo?mode → expo-level outstanding aggregates
- GET /api/finance/by-agent?mode → agent-level outstanding aggregates
- GET /api/finance/contract/:id/detail → single contract with payment schedule + actual payments
- GET /api/finance/recent-activity?limit=20 → recent payment events

Charts:
- Sales Leaderboard: horizontal bar chart (top 10) — always visible
- Expo Detail Monthly Sales: vertical bar chart (revenue/contracts toggle)
- Fiscal Sales Trend: vertical bar chart (revenue/contracts toggle, daily/monthly auto-select)
- Finance A/R Aging: vertical bar chart (6 color-coded buckets)

Finance Page (/finance):
- Collections Cockpit — default: Edition mode (upcoming expos)
- 8 KPI cards: Contract Value, Collected, Outstanding, Paid This Month, Due Next 30d, Deposit Rate, At-Risk, No Payment
  - KPI cards clickable: Outstanding→reset filters, At-Risk→risk:HIGH, No Payment→stage:no_payment, Due Next 30d→scroll to upcoming, Collected→scroll to recent payments, Paid This Month→scroll to recent payments
  - Paid This Month: SUM(contract_payments.amount_eur) this month, green, shows payment count + vs last month comparison
  - Deposit Rate: paid_eur > 0 contracts / total open contracts * 100, color-coded (green >70%, orange 40-70%, red <40%)
- Collection Action List: main table with stage/risk filter chips + company search
  - Split table sticky header: fixed header table + scrollable body table (540px max-height), matching colgroup widths, MutationObserver for theme-aware border color
  - Filter summary bar: "SHOWING X of Y | Balance: €X | Value: €X | Paid: €X" — updates on filter change
  - Stage filter chips: [All] [No Payment] [Pre-Event Open] [Partial Paid] — deposit_missing and overdue removed
  - Client-side filtering: stage, risk, multi-field search (company, AF, expo, agent, country)
  - Client-side sorting: all 11 columns sortable via th onClick (Number coercion for numeric cols)
  - Columns: Company, Expo, AF, Agent, Contract, Paid, Balance, Paid%, To Expo, Stage, Risk, Action — Overdue column removed (data always 0)
  - Default sort: total_risk_score DESC, default filter: All (no stage/risk pre-selected)
  - Fetches all records once (limit=500), no server-side filter re-fetch
  - Responsive: AF, Paid% columns hidden on mobile (<768px)
  - All suggested_action text in English
- Company detail drawer: 480px slide-in from right, contract info + payment schedule + received payments
- A/R Aging: shows "Aging requires due dates" placeholder when due_date not set in Zoho; chart renders when due dates available
- Upcoming Collections table (7d/14d/30d/60d toggle) — side by side with aging
- Expected Collections — Next 8 Weeks: weekly cash forecast table from contract_payment_schedule (synthetic 30% deposit + 70% pre-event)
  - Summary line: "Next 8 weeks: €X expected from Y payments"
  - Export: Copy/CSV/Excel
  - Note: "* Based on estimated payment schedule (30% deposit + 70% pre-event)"
- Outstanding by Expo + by Agent tables — side by side, sortable
- Recent Payments table (ORDER BY payment_date DESC — most recent first)
- Export: Copy/CSV/Excel per-table (exports use filtered+sorted data)
- Stage badge colors: no_payment (#C0392B), overdue (#E67E22), pre_event_balance_open (#D4A017), partial_paid (#4A9EBF)
- Risk badge colors: CRITICAL (#C0392B), HIGH (#E67E22), WATCH (#D4A017), OK (#2ECC71)
- Mode filter: edition (expo_start_date within 12 months) vs fiscal (contract_date current year)
- Currency conversion: contract_payments use Contract.Currency + Exchange_Rate to convert local payments to EUR
  - Zoho "X (€Y)" dual format → prefer EUR from parentheses
  - Plain amounts → divide by exchange_rate when currency != EUR
  - contract_payments columns: amount_eur (converted), amount_local (original), currency
  - Dashboard recent payments: dual display "€1.579 (NGN 2.625.000)" for non-EUR
  - Migration 016: amount_local + currency columns on contract_payments
- Collection stages simplified (migration 015): deposit_missing merged into no_payment, overdue kept in SQL but inactive (due_date NULL)
- Known data issue: contracts.due_date is NULL for all 244 open contracts (Zoho Due_Date field not populated)

Design:
- Design system: styles/design-system.css (single source of truth)
- Theme system: data-theme attribute on <html> — "dark" (default) or "light"
  - Dark: #080B10 bg, #0E1318 surface, #141B22 surface-2
  - Light: #F5F5F5 bg, #FFFFFF surface, #FAFAFA surface-2
- Accent color: --accent-color CSS custom property, 6 options (gold/blue/green/purple/red/teal)
- Table density: data-density attribute — "comfortable" (default) or "compact"
- Fonts: var(--font-mono) "DM Mono", var(--font-sans) "DM Sans"
- Animated KPI counters on load
- Risk Radar panel with hover tooltips
- All admin pages now responsive (mobile-friendly)

Settings Page (/settings):
- Profile: name, role, office (read-only cards)
- Appearance: theme toggle (dark/light), accent color (6 swatches), table density (comfortable/compact)
- Language & Region: language + timezone (timezone set via user_country in admin)
- Security: change password + logout
- Settings saved to users.settings JSONB column (migration 012)
- API: PUT /api/auth/settings — debounced save (500ms)
- Applied on login + page load via AuthProvider → applySettings()
- User-bound (not browser-bound) — same settings across all devices

Export:
- Per-table: Each table has own Copy/CSV/Excel buttons (export-btn-sm)
- Page-level: Copy All / CSV All / Excel All (multi-sheet) / PDF (multi-table)
- PDF only at page level (all tables in one document)
- Libraries: npm packages (jspdf, jspdf-autotable, xlsx) with dynamic import() — NO CDN loadScript

Sorting:
- Each table has independent sort state (agentSort, expoSort, countrySort)
- Numeric-safe sort: Number() coercion for PostgreSQL string-typed numbers
- Default: revenue_eur DESC (highest on top)
---
