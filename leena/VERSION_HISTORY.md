# Leena EMS — Versiyon Geçmişi

Bu dosya `CLAUDE.md`den ayrıldı (20 Temmuz 2026). Otomatik yüklenmez; gerektiğinde okuyun.

---

## Versiyon Geçmişi

### v4.0.2+ (Şubat 2026 — Mega Horeca Nigeria fuarı)

**Fuar Öncesi (9-10 Şubat):**
- Exhibitor model: visitors.visitor_type kullanımı (ayrı tablo kaldırıldı)
- visitors.booth_number kolonu eklendi
- Badge templates: visitor_type dropdown, booth/phone/sector alanları, bold/italic toggle, bulk print
- QR Scanner: exhibitor modal kaldırıldı, tüm tipler aynı akış
- Visitor log: visitor_type filtre pills + Type kolonu + backend filtre desteği
- Bulk print: Excel → /api/visitors/import API → DB'ye kayıt + QR üretimi
- Import/manual registration upsert: duplicate email → update (QR koru)
- Badge print popup (scanner sayfası açık kalır)
- Badge text wrap (ellipsis kaldırıldı, word-break, auto-size threshold 15/25)
- Test checkin temizliği (37 checkin + 20 visitor_event_status silindi)

**Fuar Sırası (11 Şubat):**
- Reactivation resend-pending endpoint + frontend (farklı template ile pending'lere tekrar gönder)
- Check-in reports sayfası (checkin-reports.html): saatlik/günlük grafik, source/ülke/type dağılımı, dönüşüm analizi, no-show tablosu, CSV export, print, mobil uyumlu
- Exhibitor lead scanner (lead-scan.html + leads.js): kamera QR okuma, firma bazlı lead toplama, vCard export, CSV export
- Terminal visitor-by-email endpoint (email ile visitor arama)
- QR scanner email fallback (input'a email yazılırsa önce email ile arar)
- QR URL parse (kamera URL formatında QR okursa qr parametresini çıkarır)
- Manual registration loading fix (isProcessing/showLoading reset)
- Badge popup boyutu: 450x300 → 600x400

**Post-Fair (23 Feb):**
- Send Email QR fix (emailSend.js: existing visitor QR lookup + BASE_BADGE_URL fallback)
- Check-in report CSV: visitor_type + job_title columns added (10 → 12)
- Check-in backend: visitor_type added to GET /api/checkins SELECT (fixes Type pie chart)
- Email templates expo-based grouping + cross-expo clone
- Forms expo-based grouping + cross-expo clone
- Terminals expo-based grouping + cross-expo clone
- Sidebar standardization: all 15 admin pages unified link list (13 links, 5 sections)
- CLAUDE.md English-only language rule added
- Reports page enhanced for Ghana fair: backend added visitor_type_breakdown, job_title_breakdown, daily_checkin_trend, checkin_by_hall, checkin_by_terminal queries to /summary; frontend added 6 stat cards, overlay line chart (reg+checkin), visitor type doughnut, country horizontal bar, job title horizontal bar, hall bar chart

**Security Hotfix (24 Feb — Sprint 1):**
- POST /api/visitors/manual: authMiddleware added (was open to unauthenticated requests)
- Import route organizer_id: fixed `req.user?.id` → `req.organizer_id` (authMiddleware pattern)
- Zoho webhook token: moved from hardcoded to `process.env.ZOHO_WEBHOOK_TOKEN` with fallback
- QR Scanner localStorage: fixed key mismatch (`organizer_id` → `organizerId` to match login.html)
- Badge endpoint PII: replaced `SELECT *` with explicit column list (email/phone no longer exposed publicly)

**Sprint 2 — UX Consistency (24 Feb):**
- Login redirect unified: all 14 admin pages now redirect to `login.html` (removed 16 `login_new.html` refs across 13 files)
- Active expo indicator: sidebar shows selected expo name (via `selectedExpoName` localStorage) on all 14 admin pages with sidebars. Hidden gracefully when no expo selected. Inserted between sidebar-header and sidebar-nav with inline style + IIFE script.
- Favicon added: `<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96x96.png">` added to all 29 HTML files (admin + public pages). File: `public/assets/favicon-96x96.png`

**Sprint 3 — Login Flow Hotfix (24 Feb):**
- login.html replaced with login_new.html's Gen 4 modern UI (split-panel, Inter font, login+register tabs)
- Added missing `organizerId` to localStorage on login (required by Zoho webhook URL generation)
- Fixed post-login redirect: `main-panel-v2.html` → `dashboard_new.html` (expo selection step was skipped, causing infinite redirect loop)
- Fixed "no expo selected" redirect on 9 admin pages: `main-panel-v2.html` → `dashboard_new.html` (self-redirect loop → proper expo picker)
- login_new.html converted to simple redirect to login.html (old bookmark compatibility)
- dashboard_new.html confirmed as active expo selection page (NOT legacy — Sprint 2 incorrectly labeled it)
- Public form upsert: POST /api/visitors/public now checks email+expo_id before INSERT. Existing visitor → COALESCE UPDATE (QR preserved) + email resend with "(Resent)" subject. New visitor → INSERT as before. Fixes duplicate registration + QR invalidation bug.
- Template placeholder fix: `{{expo_name}}` added to 4 flows missing it (public form, import, reactivation activate badge email); `{{date}}` added to 10 flows missing it (webhook, import, email_worker mode2/3, reactivation create-from-excel/create-from-expo/activate/resend-pending, public form). All 13 email flows now have both placeholders.
- emailSegments.js BASE_BADGE_URL: fixed `http://localhost:3000` fallback → `https://leena.app`
- visitor_type standardized across all frontend: added "conference" type to all 4 pages (form-builder, visitorlog-paginated, badge-templates, import). Standard order: visitor, exhibitor, conference, vip, press, staff, speaker. form-builder.html radio buttons replaced with 7-option select dropdown. visitorlog-paginated.html: new filter pill + CSS badge color (.badge-type-conference orange) + JS color map.
- email_worker transaction fix: `fetchNextTask()` now uses `pool.connect()` + `BEGIN`/`COMMIT`/`ROLLBACK`. Atomic `UPDATE status='processing' WHERE id=(SELECT ... FOR UPDATE SKIP LOCKED)` prevents duplicate email when multiple workers run concurrently.

**Custom Field Email Placeholder Fix (25 Feb):**
- Public form email template: custom_fields (e.g. `conference_topic`) were not available as template placeholders. `{{conference_topic}}` was never replaced because custom_fields was stored as a JSON string in emailData, not spread as top-level keys. Fix: `...(custom_fields || {})` added to emailData spread in `visitors.js` POST /public. Now any form-defined custom field works as `{{field_name}}` in email templates.

**Sprint 4 — Navigation Fix (25 Feb):**
- "All Expos" button fix: `goToDashboard()` in main-panel-v2.html was pointing to `main-panel-v2.html` (self-loop), fixed to `dashboard_new.html`
- Sidebar expo indicator: changed from `<div>` to `<a href="dashboard_new.html">` across all 14 admin pages — expo name is now clickable to switch expo, with `⇄` icon hint
- Webhook custom_fields fix: Zoho webhook now captures all non-standard fields (e.g. `conference_topic`) into `custom_fields` JSONB column. Custom fields are spread into emailData so `{{conference_topic}}` etc. work in email templates. Both INSERT and UPDATE queries updated.
- Webhook visitor_type fix: Zoho webhook now fetches `visitor_type` from forms table when Zoho payload doesn't include it. Priority: Zoho payload → form DB → 'visitor' fallback. Fixes conference form (form_id=31) registrations being saved as 'visitor' instead of 'conference'.

**Sprint 5 — Import Enhancement (26 Feb):**
- Import custom_fields extraction: Excel columns not in `knownColumns` Set are stored as `custom_fields` JSONB (e.g. `conference_topic`). Both UPDATE (merge) and INSERT paths updated.
- Import existing visitor email options: new `existing_email_option` param — `none` (default), `resent` (subject + "(Resent)"), `first_time` (original subject). Each requires explicit template selection via `existing_template_id`.
- Import existing visitor QR options: new `existing_qr_option` param — `keep` (default, preserves QR), `regenerate` (new UUID + badge_id). Warning shown in UI.
- Import email template placeholders: `...customFields` spread into templateData for both UPDATE and INSERT paths. `{{conference_topic}}` and any custom Excel column now works in email templates.
- Import INSERT path fix: `JSON.stringify(row)` → `JSON.stringify(customFields)` — previously stored entire row object including known fields.
- Frontend import.html: new "Existing Visitor Options" card with email/QR dropdowns + conditional template selector. Template required when email option is active.
- Backward compatible: no params sent = old behavior (no email for existing, QR kept).
- Import history log: new `import_logs` table stores per-import stats (new/updated/failed/emails/qr_regen/custom_fields_updated counts, errors array, options used). `GET /api/visitors/import-logs` endpoint with pagination. Frontend "Import History" section with paginated table (20 per page), color-coded stats, expandable error details. Auto-refreshes after each import.
- New counter: `custom_fields_updated_count` tracks how many rows had custom fields (non-standard Excel columns) stored.

**Sprint 6 — Visitors Page Enhancement + Conference Sessions (26 Feb):**
- Visitors page (visitorlog-paginated.html) enhanced with Conference Topic dropdown filter, Job Title and Conference Topic columns in table, active filter count badge on Apply button, and URL param support (?conference_topic=X, ?visitor_type=X pre-apply filters on page load).
- Export fix: `exportData()` changed from `window.location.href` to `fetch()` + blob download pattern — supports auth header for authenticated downloads.
- New backend endpoint: `GET /api/visitors/export` — exports ALL filtered visitors as .xlsx (same filters as /paginated but no pagination limit). Uses XLSX library. Columns: Name, Last Name, Email, Company, Country, Phone, Job Title, Visitor Type, Source, Booth Number, Conference Topic, Registered Date, QR Code.
- New backend endpoint: `GET /api/visitors/conference-topics` — returns conference topics with registered_count and checked_in_count. Groups by `custom_fields->>'conference_topic'`, LEFT JOINs with checkins for check-in data.
- `/paginated` endpoint enhanced: new optional `conference_topic` query param filters by `custom_fields->>'conference_topic'`. New computed column `custom_fields->>'conference_topic' as conference_topic` added to SELECT (single string, NOT whole JSONB blob). Existing consumers unaffected.
- New page: `conference-sessions.html` — Gen 3 design, conference topic tracking dashboard. Stats cards (Total Topics, Total Registrations, Total Checked In), table with Topic/Registered/Checked In/Conversion%/Actions, summary bar. Actions: View Attendees (→ visitorlog with filter), Send Email (→ email-send), Export Topic (→ xlsx download).
- Sidebar updated: "Conferences" link (bi-mortarboard icon) added to all 14 admin page sidebars after "Terminals". Total sidebar links now 14 (was 13).
- email-send.html conference_topic URL param: when navigating from conference-sessions.html "Email" button with `?conference_topic=X`, auto-fetches all matching visitors, switches to bulk mode, pre-fills recipient list, shows conference banner. Save-to-database auto-disabled (already in DB).
- New page: `email-history.html` — Gen 3 design, paginated email send history. Stats cards (Total Emails, Successful, Failed, Delivery Rate %). Filters: Template dropdown, Status (Sent/Failed), Email search. Table: Date & Time, Recipient (email + visitor name), Template, Status (color-coded badge), Details. Pagination with page numbers.
- New endpoint: `GET /api/email-send/history` — paginated email_logs with LEFT JOIN to email_templates and visitors for names. Filters: expo_id (required), template_id, status, search (ILIKE). Includes stats (total_sent, total_failed). Response: `{success, logs[], total, page, totalPages, stats}`.
- email-send.html: "History" button added to header (navigates to email-history.html).

**Conference Certificate System (1 Mar 2026 — Mega Clima Ghana):**
- New table: `conference_certificates` (visitor_id, expo_id, conference_topic, certificate_token UNIQUE, email_sent). UNIQUE constraint on (visitor_id, expo_id, conference_topic) prevents duplicates.
- New route file: `routes/conferenceCertificates.js` — 5 endpoints: POST /checkin-and-certify (terminalAuth), POST /resend (terminalAuth), GET /verify/:token (public), GET /topics (terminalAuth), GET /stats (JWT).
- New page: `conference-scanner.html` — mobile-first hostess QR scanner with topic selector, camera QR (html5-qrcode), result cards, scan log. Terminal auth via URL param.
- New page: `certificate.html` — public certificate view with elegant design (Playfair Display font, gold border, A4 landscape print CSS). "Save as PDF" via window.print().
- Certificate email: inline HTML template with "View Certificate" button linking to certificate.html?token=X. Queued via email_queue Mode 1.
- Conference check-ins stored in standard `checkins` table (source='conference-cert', notes='Conference: TOPIC') — appear in existing reports.
- index.js: route mount added (line 86 load, line 108 mount).

**Conference Certificate Refinements (1-3 Mar 2026):**
- Registration check fix: `isVisitorRegisteredForTopic()` — case-insensitive, splits by `" || "` only (commas are in topic names, not separators)
- Topic append logic: webhook.js + visitors.js /public merge conference_topic with `" || "` separator on re-registration (prevents overwrite, duplicate-safe)
- `splitTopics()` helper: ONLY splits by `" || "` — topic names contain commas (e.g. "Engineering for a Healthy Buildings, Designing for Life")
- Double `client.release()` fix: removed early release calls, only `finally` block releases (fixed ERR_HTTP_HEADERS_SENT on production)
- New endpoint: `POST /api/conference-certificates/resend` — resends existing certificate email using stored token, no new cert created
- Duplicate scan UX: overlay persists with "Resend Certificate" + "Dismiss" buttons (no auto-dismiss)
- Conference topic filters: `/paginated` and `/export` changed from `=` to `ILIKE` for multi-topic support
- `/conference-topics` and `/topics` endpoints unnest `" || "`-separated values into individual topic counts

**Floor Plan Builder — Sprint 1 COMPLETED (30 Mar 2026):**
- New module: Floor Plan Builder (ELL Extension) — spatial CRM layer for expo stand management
- 5 new DB tables: `expo_halls`, `expo_floorplan_versions`, `expo_stands`, `expo_stand_cells`, `expo_stand_assignments` (Phase 2 stub)
- DB features new to codebase: `GENERATED ALWAYS AS` column (total_area_sqm), PostgreSQL trigger (`fn_update_stand_size_m2`), partial unique index (one active version per hall)
- Migration: `migrations/001_floorplan_tables.sql` — run on Render Shell: `psql $DATABASE_INTERNAL_URL -f migrations/001_floorplan_tables.sql`
- New route: `routes/floorplan.js` — 8 endpoints (halls CRUD, versions list+create, stands list+create+delete)
- Stand creation uses transaction (`pool.connect()` + `BEGIN/COMMIT/ROLLBACK`) with batch cell INSERT
- Draft-only enforcement: stand create/delete blocked on active/archived versions
- Optional stand_code: if omitted, auto-generates `S-{id}` after INSERT
- Frontend: `floorplan-builder.html` + 5 ES module files in `public/floorplan/` (state.js, grid.js, stands.js, toolbar.js, api.js)
- Canvas: Konva.js (CDN, v9.3.15) — grid rendering, zoom/pan, rectangular marquee selection, stand boundary rendering
- State: `FloorPlanState` class with event emitter pattern (state.js). `_cellMap` provides O(1) lookup for `getStandAtCell()` and `getOccupiedCells()`
- Stand rendering: no internal cell lines, outer boundary as separate Konva.Line segments. Labels: stand_code bottom-left, m² bottom-right, company name centered (bounding box based)
- Organizer isolation: `expo_halls.organizer_id` direct, sub-tables via JOIN chain (version→hall→organizer)
- Sidebar: standard Leena sidebar + "Floor Plan" link (bi-grid-3x3 icon, under Management section)
- index.js: 2 lines added (require + mount at `/api/floorplan`)
- Spec file: `ELL_FloorPlan_Builder_Spec_v2.md` in repo root
- **Summary:** 5 DB tables, 8 API endpoints, 6 frontend modules (1 HTML + 5 ES modules), Vanilla JS + Konva.js (CDN), no React, no build tools

**Floor Plan Builder — Sprint 2 COMPLETED (30 Mar 2026):**
- Stand update: `PUT /api/floorplan/stands/:id` — general fields (structural changes require draft, commercial fields allowed on active per Invariant #2)
- Commercial status change: `PUT /api/floorplan/stands/:id/status` — quick status dropdown in detail panel, instant save, works on active versions
- Inline editing: detail panel with company name, display label, notes inputs + Save Changes button
- Stand color selection: 10-color pastel palette stored in `metadata.color` JSONB field. Custom color overrides status color in grid rendering (`getStandColor()` checks metadata first). `darkenColor()` generates matching stroke.
- Special area type selector: create dialog shows `special_area_type` dropdown (vip, conference, registration, entrance, exit, technical, other) when `area_kind='special'` selected
- Version activate/archive: `POST /api/floorplan/versions/:id/activate` — draft→active transition, archives current active (transaction). `PUT /api/floorplan/versions/:id` for label/notes update. Activate button (green checkmark) visible only for draft versions.
- Background image overlay: PNG/JPG upload as reference behind grid. Stored in localStorage (base64, per expo+hall). Opacity slider 5%-100%. Grid background rect becomes semi-transparent when image present. New `bgLayer` below `gridLayer`.
- Stats bar live update: `standUpdated` event triggers `updateStats()` + `drawStands()` on every status/field change
- 4 new endpoints: PUT stands/:id, PUT stands/:id/status, POST versions/:id/activate, PUT versions/:id
- **Summary:** Total 12 API endpoints (8 Sprint 1 + 4 Sprint 2)

**Floor Plan Builder — Sprint 3 COMPLETED (31 Mar 2026):**
- Stand split: `POST /api/floorplan/stands/:id/split` — dialog-based horizontal/vertical split at bounding box midpoint. Auto-suggests codes (B3a/B3b). Transaction validates complete cell coverage.
- Stand merge: `POST /api/floorplan/stands/merge` — Shift+click multi-select → merge button → new code prompt. Inherits properties from first stand.
- Version clone: `POST /api/floorplan/versions/:id/clone` — deep copy all stands + cells. Optional `clear_assignments` resets company/status.
- PNG export: client-side `stage.toDataURL({ pixelRatio: 2 })`, auto-download `floorplan-{hall}-v{num}.png`. Includes background image.
- Stand duplicate: copy template (zone, area_kind, metadata) → draw mode → pre-filled create dialog with `{code}-copy` suggestion.
- Stand drag-to-move: `PUT /api/floorplan/stands/:id/move` — ghost overlay (green=valid, red=invalid), grid snap, draft-only. DB uniqueness constraint prevents overlap.
- Multi-stand drag: Shift+click or marquee-select multiple stands → drag all together. Parallel `moveStand()` API calls on commit.
- Select-mode marquee selection: left-drag on empty area → rectangle → selects all stands with cells inside.
- Pan controls: `stage.draggable = false`. Middle mouse button + drag OR Space + left drag = manual pan. Scroll wheel = zoom (unchanged).
- 4 new endpoints: POST stands/:id/split, POST stands/merge, POST versions/:id/clone, PUT stands/:id/move
- **Summary:** Total 16 API endpoints (8 Sprint 1 + 4 Sprint 2 + 4 Sprint 3)

**Floor Plan Builder — Sprint 3.5 Polish (31 Mar 2026):**
- Trackpad pan/zoom: wheel without Ctrl = pan (deltaX/deltaY), Ctrl+wheel or pinch = zoom. Works on MacBook trackpad natively.
- Bulk duplicate: multi-select → "Duplicate All" button. Copies all selected stands offset to the right (or below if no room). Codes get `-c` suffix, commercial_status reset to available.
- Erase mode improved: clicking a stand cell in erase mode → confirm + delete entire stand (not just pending cells)
- Grid rulers: meter markers every 5 cells on top and left edges (9px grey text, cached with grid)
- Selection glow: selected/multi-selected stands get blue shadow rect (4px, opacity 0.3) behind boundary
- Fit to view: already auto-called on hall/version change (verified)

### v4.0.3 (Nisan 2026)

**Form Design Customization (17-20 April):**
- `forms.config` JSONB column activated for style configuration (was unused since initial.sql)
- Style system: headerBanner (image/color/gradient/height), footerBanner (same + text), primaryColor, backgroundColor, fontFamily, buttonText, borderRadius
- Banner images stored as base64 in JSONB (max 500KB, Render ephemeral disk workaround)
- form-builder.html: "Design" tab with color pickers, banner upload, font selection, live preview
- form-public.html: `applyFormStyle(config)` dynamically applies styles. Null config → hardcoded defaults preserved
- reactivate.html: Same style system. form_config from verify endpoint. Null → yellow theme preserved
- `POST /api/forms/upload-banner`: multer memoryStorage, returns base64 data URI
- `migrations/002_reactivation_form_id.sql`: adds `form_id` to `reactivation_tokens`
- body-parser limit: 100KB → 2MB in index.js (`express.json({ limit: '2mb' })`)
- Fix: removed JSON.stringify for JSONB config (was double-encoding), added typeof string parse fallback

**Conference Topic Email Fix (7 April):**
- `formatConferenceTopic()` in utils/email.js — multi-topic → HTML `<ul>` bullet list
- Applied in visitors.js (public form) and email_worker.js (Mode 2 template)
- Single topic: plain text unchanged. Null/empty: empty string

**Import Skip Existing (20 April):**
- `skip_existing` parameter in POST /api/visitors/import
- When true: existing visitors completely skipped (no update, counted in `skipped_count`)
- import.html: radio "Update info (keep QR)" vs "Skip entirely", hides email/QR options when skip selected
- Results display: shows new/updated/skipped/failed/emails counts

**Visitor Detail Panel + Email History (20 April):**
- `GET /api/visitors/:id/emails` — returns email_queue + email_logs history for visitor
- visitorlog-paginated.html: click row → slide-in panel (480px, right side)
- Panel: visitor info grid + email timeline (status icons, subject, date, errors)
- Queries by both visitor_id AND email address (comprehensive history)

**UI Help Info Boxes (20 April):**
- All 20 admin pages have contextual bilingual help boxes (EN main + TR translation)
- Dismissible (X → localStorage per page), re-openable ("ℹ️ Help" toggle)
- Page-specific content: what it does, key info, tips, differences from similar pages

**Floor Plan Builder Fixes (31 Mar - 7 Apr):**
- Zoom: mouse wheel=zoom, trackpad two-finger=pan, Ctrl+wheel/pinch=zoom
- Duplicate: no stand_code → backend auto-assigns S-{id}
- Zoom buttons (+/−) in top bar

**Floor Plan Builder — Sprint 4 Backlog:**
- Background image UX (resize, reposition, alignment)
- Batch stand workflow (draw large area → split into grid)
- PDF export (branded, server-side — Phase 2)
- Connected shape validation (cell adjacency)
- Sidebar link to existing 15 admin pages
- Stand resize (edge drag)

**Yaprak Feedback Sprint A+B (5-6 May 2026):**
- Visitor count display bug fix: `COUNT(*)::int` cast in expos.js (3 endpoints), `parseInt()` defense in dashboard_new.html. Root cause: pg driver serializes bigint as string → JS string concatenation instead of addition.
- Campaign delete extended: new `requireDeletable` helper (draft/completed/paused), `email_queue` pre-cleanup to prevent FK violation, Delete button on list view (non-active only)
- Campaign completion logic fix: `computeNextDue` marks recipient `status='completed'` when no more steps. Previously stayed 'active' forever, blocking `checkCampaignCompletion`. See ADR-016.
- One-time data migration (5 May 2026 Render Shell): 37,574 stuck recipients + 11 campaigns → completed
- `PUT /api/visitors/:id`: authMiddleware, COALESCE(NULLIF()) pattern, email duplicate check (409), qr_code/badge_id route-level protection (never in UPDATE list)
- Inline edit UI in visitor detail panel: Edit button, input form, Save/Cancel, visitor_type dropdown, table auto-refresh
- Toast Bootstrap conflict fix: `.toast` → `.app-toast` (Bootstrap 5 .toast class override caused 0×0 rendering)
- `badge_id` added to `/paginated` SELECT (was missing from detail panel display)

**Yaprak Feedback Sprint C + Email Bug Fix + Madde 10 (7 May 2026):**
- Source filter: replaced 5 fixed pills with searchable text input + datalist, `GET /api/visitors/sources` endpoint, ILIKE partial match
- Conference topic edit: `jsonb_set` for `custom_fields.conference_topic` in PUT endpoint, only shown for `visitor_type='conference'`
- Send Email button in visitor detail panel: template dropdown, `POST /api/email-send/single` integration, double-click protection
- Prev/next visitor navigation: `< >` buttons in panel header, keyboard shortcuts (ArrowLeft/ArrowRight), edit mode confirm dialog
- Email queue bug fix (Fix 1): Mode 1 email_queue INSERTs now include `visitor_id, expo_id, organizer_id, template_id` (3 locations in visitors.js)
- Email queue bug fix (Fix 2): Removed duplicate 'queued' email_logs INSERTs from routes (4 locations). Worker `logToEmailLogs` is now sole log writer.
- Email queue cleanup: 6,396 ghost 'queued' email_logs updated to 'sent' via SQL transaction
- Email status filter: `email_status` query param on `/paginated` and `/export` (never_sent/sent). Uses EXISTS on email_logs with email fallback for historical NULL visitor_id logs (~227ms, acceptable).
- `buildVisitorFilter` helper: extracted shared filter logic from /paginated and /export, also used by /bulk-email
- Bulk email send: `POST /api/visitors/bulk-email` — transaction-wrapped batch INSERT (1K chunks, 10K limit), template+expo ownership check, Mode 2 queue. Frontend modal with template selector and confirm dialog.

**UI Quick Fixes Sprint 1 + Sprint 2 (7 May 2026):**
- Shared toast component (`leena-toast.js`): replaces inline alert()/toast across 21 admin pages. ~73 alert() instances migrated to showToast(). Resolves Bootstrap .toast class conflict in email-campaigns.html. Net -16 lines via DRY.
- Shared fetch wrapper (`leena-fetch.js`): auto-attaches Authorization header, handles 401/403 with auto-logout + redirect, 15s timeout via AbortController, concurrent 401 protection. Migrated in 3 high-traffic pages: visitorlog, email-campaigns, dashboard_new.
- Bulk send filter guard: visitorlog button now requires active filter (prevents accidental send to entire expo).
- Public form error: form-public.html alert() → inline error div for better visitor UX.
- Accessibility: ARIA labels on visitor detail panel buttons (prev/next/edit/close); conference-scanner viewport zoom restored (WCAG 2.1).
- Loading indicator: email-campaigns.html now shows spinner during loadCampaigns().
- Backend COUNT::int cast: reports.js (63 instances) + checkins.js (11 instances). Closes Sprint A gap. Other 11 route files deferred (frontend parseInt() defensive).

### v4.0.4 — Mega Clima Nigeria 2026 Pre-Fair Sprint (15 May 2026)

**Context:** Fuara 4 gün kala (19-21 May, Lagos) toplu UX hardening + 
data quality fixes. 10 production commit, hepsi backward compatible. 
Migration yok (1 webhook auto-split + 1 one-off DB cleanup).

#### Conference Scanner Hardening (commit 27ddae7)
- `public/conference-scanner.html` — pre-display visitor preview + force confirm modal
- Hostess QR scan ettiğinde visitor'ın registered topic'leri ekrana basılır
- "Save & Send Certificate" force butonu artık custom confirm modal'la korunmuş
- Backend untouched
- Audit: CONFERENCE_FORCE_AUDIT_20260514.md

#### qrscanner Country Default (commit d1464b7)
- `public/qrscanner.html:582` — country default `'Morocco' → 'Nigeria'`
- Dropdown options preserved (Morocco still selectable)

#### Hostess Quick Reference Card (commit 7e852ba)
- New page: `public/hostess-guide.html` (10KB, self-contained, no external deps)
- 8 crisis-moment scenarios: force button, not-registered, QR fails, badge redirect, wrong page, cert resend, escalation, offline fallback
- Mobile-first, sticky jump bar, severity color coding
- Production URL: https://leena.app/hostess-guide.html
- Suer needs to fill bookmark URL in Senaryo 5 (placeholder)

#### Terminal Default Visitor Type (commit 86c3738)
- `public/qrscanner.html` — manual registration's visitor_type dropdown defaults to the terminal's badge template visitor_type
- Uses existing `/api/badge-templates/for-terminal/:terminalKey` endpoint (no new endpoint)
- Dropdown remains editable
- Backend/DB unchanged

#### form-public QR Display on Success (commit 9a94447)
- `public/form-public.html` — submit response's `qr_code` rendered as `<img src="/api/qr-image/${qr}">` in success card
- "Show this QR at the entrance" message
- Use case: visitors who don't receive confirmation email can still enter via on-screen QR
- Backend already returned qr_code (no backend change)

#### Manual Registration Reason Field (commit 439eb0e)
- `public/qrscanner.html` — required "Why manual?" dropdown added to manual registration form
- Options: No internet / Did not receive email / Speaker / VIP / Press / Long queue / Other (with conditional text input)
- `routes/visitors.js` `/api/visitors/manual` — accepts manual_reason, merges into custom_fields JSONB
- Backward compatible: missing manual_reason → null, doesn't break existing flow
- Stored as `custom_fields.manual_reason` (string)

#### Badge Preview Type Fix (commit 5606ef6)
- `public/badge.html:295` — preview mode now reflects selected template's visitor_type instead of hardcoded 'VIP'
- Real-print path (else branch) untouched
- Audit: BUG_6_DEEPDIVE_20260515.md (Senaryo 1 — preview-only kozmetik)

#### Smart Capitalize Badge Type (commit d9908d9)
- `public/badge.html` — `formatRole()` helper added: Title Case for normal words, UPPERCASE for known acronyms (vip, ceo, cto, cfo, vp, md)
- Applied at single render site (line 377), affects both preview and real-print paths
- DB unchanged (display-only transformation)
- `esc()` XSS protection preserved (wraps formatRole output)

#### Zoho Day1/Day2 Auto-Split Webhook (commit 6dd34ca)
- `routes/webhook.js` — new `normalizeConferenceTopic()` helper + try-catch guard
- Detects exact MERGED_DAY12 string (Zoho form 39's merged "Day 1 & Day 2" option) and splits into Topic 1 + Topic 5 (canonical form 39 strings)
- Strict exact-match detection (no substring/regex) — zero false-positive risk
- Insertion point: after customFields loop (line ~74), before new/existing visitor branch — covers both INSERT and append-merge paths
- Fail-safe: try-catch pass-through on any error (preserves current behavior)
- Backward compatible: non-matching values byte-identical to current behavior
- Audit: DAY1_DAY2_ISSUE_RESEARCH_20260515.md + WEBHOOK_DAY1_DAY2_FIX_PLAN_20260515.md

#### Day1/Day2 Historical Cleanup (one-off DB, no commit)
- 2 pre-deploy visitors (id 55052, 55909) had merged "Day 1 & Day 2" conference_topic — manually split via Render Shell heredoc, NOT a migration
- Backup table: `conference_topic_backup_20260518` (2 rows, preserved for post-fair drop)
- Pattern: BEGIN; UPDATE ... RETURNING ...; (verify) COMMIT;
- Validated POST-COMMIT: merged_rows_remaining = 0, split_rows_total = 87

#### Post-Fair Backlog (yarın için karar)
- **Request #1**: Token-protected bulk badge print page (HIGH risk, ~yarım-1 gün, security infrastructure)
- **Request #3**: Manual Registration on/off toggle per terminal (LOW-MED risk, migration 008, ~2-3 saat)
- Decisions pending: see REQUESTS_1_AND_3_ANALYSIS_20260515.md

#### Smoke Test Status
- Yaprak confirmed: form-public QR display works ✅
- Yaprak confirmed: badge preview shows SPEAKER (capitalize) ✅
- Other 8 commits: smoke test pending (Yaprak + Suer post-doc-update)

### v4.0.5 — Mega Clima Nigeria 2026 Pre-Fair Sprint Day 2 (18 May 2026)

**Context:** Fuara 1 gün kala (19-21 May, Landmark Centre, Lagos) ikinci pre-fair sprint.
**5 production commit** + 2 migration + 1 DB cleanup/token oluşturma + 1 yeni endpoint.
Hepsi backward compatible. Tüm yeni davranışlar expo-scoped veya additive — mevcut
fuarlar (Ghana expo 5 vb.) etkilenmez.

#### Per-Terminal Manual Registration Toggle (commit 1324296)
- Migration 008: `terminals.allow_manual_registration BOOLEAN DEFAULT TRUE NOT NULL` (production'da uygulandı; 20 terminal default TRUE)
- `POST/PUT /api/terminals` body'de `allow_manual_registration` kabul (snake_case; backward compat: yoksa TRUE / değişmez)
- `GET /api/badge-templates/for-terminal/:key` response'a `allowManualRegistration` (camelCase, terminal objesi konvansiyonu)
- `public/terminals.html`: "Manual Reg" checkbox (Add form + her satır inline toggle, snake_case body)
- `public/qrscanner.html`: `applyTerminalManualRegToggle()` — flag false ise Manual Registration checkbox disabled + not (ayrı fonksiyon; `applyTerminalDefaultType` dokunulmadı)
- Yaprak request #3. Frontend enforcement (`/api/visitors/manual` gate'lenmedi — kapsam dışı)
- Clone bug deferred: `POST /api/terminals/clone/:id` yeni kolonu kopyalamıyor → DB DEFAULT TRUE (post-fair)
- Suer tested ✅

#### Token-Protected Public Bulk Badge Print (commit 5a66070)
- Migration 009: `terminals.kind VARCHAR(20) DEFAULT 'scanner' NOT NULL` + `idx_terminals_kind` (production'da uygulandı; 20 terminal kind=scanner)
- Yeni `middleware/dualAuth.js`: `Authorization: Bearer` → JWT path (authMiddleware ile byte-identical); `x-terminal-key` → kendi terminal SELECT'i + `kind='bulk_print'` gate (403 WRONG_TERMINAL_KIND). `terminalAuth.js` dokunulmadı (scanner/cert/lead route'ları etkilenmez)
- `routes/visitors.js`: `/paginated` + `/import` `authMiddleware` → `dualAuth` swap; token mode'da `expo_id = req.scopedExpoId` (token'dan zorlanır, cross-expo leak yok). JWT path byte-identical
- `public/bulk-badge-print.html` (390 satır, self-contained): `?key=` token, for-terminal `kind` ile gate, Excel upload + DB-from-paginated modu, badge-templates.html modal mantığı port (loadBulkData/executeBulkPrint/generateBulkPrintHTML verbatim), tüm fetch `x-terminal-key`
- `GET /api/badge-templates/for-terminal/:key` response'a `kind` (camelCase, additive — qrscanner #2 etkilenmez)
- Yaprak request #1. Single-organizer sadeleştirme: organizer_id zorlama YOK (sadece Elan Expo; multi-tenant guard post-fair). JWT organizer_id filter zayıflığı (`buildVisitorFilter` sadece expo_id filtreliyor) bilinen, post-fair backlog
- Suer tested ✅ (Mega Clima + Mega Water token'ları)

#### Nigeria Certificate Expo-Gated Branch (commit 9a20641)
- `routes/conferenceCertificates.js`: `/verify/:token` response'a `expo_id` (1 satır additive); yeni `CERT_EMAIL_TEMPLATE_NG` const (yeşil #54AF3A tema, "19–21 May 2026 • Landmark Centre, Lagos", westafricahvacexpo.com asset, Ghana template **yapısıyla birebir** — sadece branding swap). `issueCertificate` + `/resend`: `Number(expoId)===7 ? NG : Ghana`. Ghana `CERT_EMAIL_TEMPLATE` byte-identical (dokunulmadı)
- `public/certificate-ng.html` (yeni): Yaprak `certificate 2.html` markup+CSS **byte-identical** (cp, satır 1-588) + yeni `<script>` (`/verify/:token` → `.field`/`.topic`/`.cert-id` data binding, fetch öncesi gizle, hata overlay)
- `public/certificate.html`: +6 satır JS — `Number(cert.expo_id)===7` → `location.replace('certificate-ng.html'+search)`. Ghana HTML/CSS + DOM-injection **byte-identical**
- Method A2 (ayrı dosya + redirect); Method B (DOM override) reddedildi (Ghana ↔ Yaprak Nigeria template yapısal divergence). cert-id format: `MCN-2026-<token[0:10]>`. "9th International Mega Clima Expo Nigeria 2026" hardcoded (Suer onayı, expo-7'ye özel dosya)
- Forward-only (deploy anında expo 7'de 0 cert). **Test pending** (fuar günü)

#### Cool Plus Topic Block (commit 02e0692)
- Yaprak request: Topics 1, 5, 11 (Cool Plus Limited oturumları) Leena sertifikası ALMAMALI — Cool Plus kendi sertifikasını verir
- `routes/conferenceCertificates.js` helper'ları: `getCoolPlusBlockedTopics(expoId)` (form 39 options [0,4,10] canlı çek; module-level `coolPlusCache` lazy; **fail-OPEN**: DB hatası → boş Set + console.error → sertifika akışı durmaz), `isTopicBlocked` (" || " split + segment normalize + Set.has), `coolPlusBlockResponse` (`code:'COOL_PLUS_BLOCKED'`). `normalizeTopic`: `NFKC + trim + lowercase`
- 3-dokunuş tasarım: `issueCertificate` guard **EN BAŞTA** (blocked → check-in INSERT + visitor_event_status upsert normal akışla **byte-identical SQL**, A1 attendance korunur; cert+email atlanır; `return {blocked,blocked_topic}`) + `checkin-and-certify` caller `if(result.blocked){COMMIT; return coolPlusBlockResponse}` (duplicate branch'ten önce, değişmedi) + `/resend` guard
- `public/conference-scanner.html`: yeni turuncu `blocked-overlay` (success/error/duplicate'ten ayrı; duplicate'in Resend butonu çelişkisi nedeniyle reuse edilmedi), 2sn auto-dismiss (workflow kırılmaz), `confirmAndIssue` + `forceCertify` ikisinde `code==='COOL_PLUS_BLOCKED'` guard (`!success`'ten önce), scan log "Cool Plus". Saf additive
- Rescan dedup (a) kabul: aynı Cool Plus visitor 2 kez taranırsa 2 check-in (cert row yok; sistemde çoklu check-in olağan; post-fair polish)
- Scope: SADECE `expo_id=7`. Forward-only. Diğer expo'lar sıfır davranış değişikliği. **Test pending** (fuar günü)

#### Preemptive Cool Plus Warning + Force Microcopy (commit d858391)
- Yeni `GET /api/conference-certificates/blocked-topics` (terminalAuth, expo-scoped, `getCoolPlusBlockedTopics` reuse, fail-open; **normalize/lowercase string** döner)
- `public/conference-scanner.html`: `loadBlockedTopics()` (sayfa açılışta cache; fail-open boş Set) + `isClientSideBlocked` (backend ile birebir NFKC normalize + " || " split) + dropdown change → selector altı turuncu uyarı + `showVisitorPreview` turuncu banner + Confirm disable + `showUnregCard` Force disable. Saf additive, yeni CSS rule yok (inline + `.pv-match-banner` reuse)
- Defense-in-depth: backend block (02e0692) otoriter — frontend disable bypass edilse bile reject. Fail-safe: endpoint fail → frontend uyarı yok ama backend reddeder
- Mikrokopi: mismatch banner "force will be needed" → "click Confirm to proceed with force certification" (class/yapı dokunulmadı)
- Suer tested ✅ (mobile)

#### Migrations (production'da uygulandı, Render Shell heredoc)
- `008_add_allow_manual_registration_to_terminals.sql` — idempotent IF NOT EXISTS; 20 terminal allow_true
- `009_add_kind_to_terminals.sql` — idempotent; kind=scanner ×20; idx_terminals_kind

#### Tokens / DB ops (no commit, Render Shell)
- Bulk print token — Mega Clima Nigeria (expo 7): `50a9d2a4-76b4-437a-818e-271193777fff`
- Bulk print token — Nigeria Mega Water (expo 8): `77565c52-fee4-40d9-a378-22c5112529a2`
- Conference scanner terminal — Mega Clima Nigeria (expo 7): `7a7537d3-62e5-4ec6-aaca-1d9846e8d16e` (hall='Conference', terminal_no='1', badge_template_id=16, allow_manual_registration=FALSE)

#### Key Decisions / Learnings
- Single-organizer sadeleştirme: bulk-print'te organizer_id enforcement atlandı (sadece Elan Expo; multi-tenant guard deferred)
- JWT organizer_id filter zayıflığı: `/paginated` + `/import` `buildVisitorFilter` sadece expo_id filtreliyor — post-fair backlog
- Certificate redesign Method A2 (ayrı dosya + redirect) > Method B (DOM override): Ghana ve Yaprak Nigeria template yapısal divergence
- Cool Plus block: form 39 canonical string NFKC normalize; defense-in-depth (backend guard + frontend preemptive UI); DB hatasında fail-open
- Conference scanner URL param adı: `terminal_key` (bulk-badge-print.html `key=` kullanır — farklı)

#### Test Status
- Suer tested ✅: 1324296 (manual reg toggle), 5a66070 (bulk print, 2 token), d858391 (preemptive warning, mobile)
- Pending (fuar günü Yaprak/Suer): 9a20641 (Nigeria certificate), 02e0692 (Cool Plus block)

### Shared Frontend Components (public/leena-*.js)

Two shared components reduce duplication across admin pages:

**leena-toast.js** — Notification component
- API: `window.showToast(message, type, duration)`
- Types: success, error, warning, info
- Auto-injects CSS once, container auto-create
- Bootstrap conflict-safe (.app-toast prefix)

**leena-fetch.js** — Authenticated fetch wrapper
- API: `window.leenaFetch(url, options)` — returns Promise<Response>
- Auto-attaches Authorization from localStorage token
- 401/403 → toast + auto-logout + redirect (1500ms delay)
- 15s timeout via AbortController
- All non-auth errors thrown to caller for contextual handling
- Caller catch pattern: `if (err.status === 401 || err.status === 403) return;`

Migration status: 3 pages (visitorlog, email-campaigns, dashboard_new). Remaining 16+ admin pages: post-fair backlog.

### Authentication

- **JWT lifetime:** 30 days (`routes/auth.js:54`, `{ expiresIn: '30d' }`)
- **Storage:** `localStorage.setItem('token', data.token)` in login.html
- **Middleware:** `authMiddleware.js` (JWT_SECRET required, no fallback)
- **Dead middleware:** `middleware/auth.js` exists but unused by any route (has `'your-secret-key'` fallback) — to be deleted in post-fair cleanup
- **Status codes:** 401 = token missing/malformed, 403 = token expired/invalid signature
- **Frontend handling:** leena-fetch.js catches both 401 and 403 as session expiry

**Conference Topic Cleanup Tool (10-12 May 2026):**
- Temporary admin tool to fix conference_topic data quality issues in Mega Clima Nigeria 2026 expo. DB had 55 distinct variants for 13 canonical topics (apostrophe variants, prefix variants, numbered variants, JSON array strings).
- Backend: `routes/conferenceCleanup.js` — 5 endpoints (GET /expos, /canonical-topics, /topic-variants, /visitors, POST /bulk-update). Transaction-wrapped execute, CHUNK_SIZE=100, organizer-scoped, conflict detection (cert UNIQUE constraint).
- Frontend: `public/conference-cleanup.html` — master-detail layout (variants left, visitors right), dry-run preview modal, segment-aware execute. Entry via "Topic Cleanup" button on conference-sessions.html header.
- Canonical source: `forms.fields` JSONB → field with `name='conference_topic'` → `options` array. Dynamic per expo, no hardcoded list.
- conference-sessions.html line 242 orphan sidebar link fix (14969f6).
- Temporary tool — to be removed post Mega Clima Nigeria 2026 fair. See ADR-021.

**Pre-launch Mega Clima Nigeria 70k Reactivation Sprint (13 May 2026):**

Code commits (all deployed to production):
- **BLOCKER-1 fix (3e4b969):** `routes/reactivation.js:589-607` POST /activate template selection corrected. Previously picked first form for expo (often wrong template — e.g. conference template used for visitor activation). New logic: `tokenData.form_id` primary, NULL fallback → `expo_id + visitor_type='visitor' + ORDER BY f.id ASC LIMIT 1`. Added log line: `[reactivation] Activate template selection: form_id=X, template_id=Y`.
- **Async job pattern (094ef99):** New `import_jobs` table (`migrations/005_import_jobs.sql`) with status, total_count, processed_count, skipped_count, failed_count, error_message, target_expo_id, source_expo_id, template_id, form_id. POST /create-from-excel + /create-from-expo refactored: pre-fetch existing emails into Sets (O(1) dedup) → INSERT import_jobs → setImmediate background → 202 response. Helper `processReactivationChunks` with CHUNK_SIZE=1000 and BEGIN/COMMIT/ROLLBACK per chunk. New endpoint: GET /api/reactivation/job/:id polling. Frontend: progress bar + 2s polling loop.
- **File size limit (7d10144):** multer + frontend validation 10MB → 50MB (`routes/reactivation.js:20`, `public/reactivation-campaign.html:431`). 70k Excel ~24MB, headroom retained.
- **email_unsubscribes pre-check (e7d9cf4):** `prefetchEmails()` now returns 3 Sets — existingVisitors, existingTokens, unsubscribed. Filter loop adds `skipped_unsubscribed++` counter, surfaced in UI breakdown.
- **Exhibitor job_title fallback (aff83bc):** `routes/visitors.js:195` — `custom_fields?.job_title || custom_fields?.title || ''`. Exhibitor form (id=35, expo 7) uses field name `title`. Aligns with Excel import path which already uses this OR fallback (visitors.js:612).

DB operations (Render Shell, production):
- **Template 24 unsubscribe footer:** SQL REPLACE inserted standard footer before `</body>` — "You received this email because you registered for or were invited to an Elan Expo event. Elan Expo, Istanbul, Turkey. To unsubscribe from future emails, reply with UNSUBSCRIBE in the subject line." Manual unsubscribe path until automated endpoint is built post-fair.
- **52 exhibitor job_title backfill (expo 7):** `UPDATE visitors SET job_title = custom_fields->>'title' WHERE expo_id=7 AND visitor_type='exhibitor' AND (job_title IS NULL OR job_title='') AND custom_fields->>'title' <> ''`. Backup: `exhibitor_job_title_backup_20260513`. UPDATE 52, visually validated by Yaprak in Visitor Log.
- **76 visitor conference_topic split (expo 7):** "Day 1 & Day 2 | Workforce Development Programme..." segment → Topic 1 + Topic 5 (canonical from form 39). Backup: `conference_topic_backup_20260513`. Method: WITH refs (DB-derived strings) + LATERAL `regexp_split_to_table(...,' \|\| ')` + UNNEST + DISTINCT trim + string_agg. Multi-segment visitors preserved with dedup (e.g. visitor 49864 expanded from 3 to 4 segments). Validation: still_has_day_1_2=0, has_topic_1=76, has_topic_5=76.

Crisis response — test domain SendGrid suppression:
- During async-pattern stress test, 85,000 reactivation tokens were inserted with `test-NNNNN@leena-test.local` (no DNS) recipients. Working assumption "SendGrid skips invalid-domain addresses" was wrong — SendGrid attempts MX lookup, returns deferred, retries 72h, then hard-bounces. 42,924 already submitted to SendGrid; 42,077 pending in queue.
- Action 1: `UPDATE email_queue SET status='cancelled' WHERE status IN ('pending','processing') AND recipient_email LIKE '%@leena-test.local'` → 42,077 cancelled.
- Action 2: 85,000 unique test addresses POSTed to SendGrid Global Suppression List via `/v3/asm/suppressions/global` (85 batches × 1000) → 85/85 success → deferred retries blocked, hard-bounce escalation prevented, sender reputation preserved (~98%).
- Verified: random 10 sent emails confirmed in suppression list.

Infrastructure:
- SendGrid plan upgrade: Pro 100K → Pro 300K ($89.95 → $249/mo). Month-to-date usage already ~84k; 70k reactivation would have exceeded Pro 100K cap.

Smoke test (production validation):
- 5 real recipients (`suer+smoke1@elan-expo.com` … `suer+smoke5`) on Mega Clima Nigeria expo validated full chain. Response 464ms → progress bar → "Completed! 5 tokens created". Reactivation invite used Template 34 ("MC Nigeria Reactive Badge Mailing") with correct {{name}} and {{activation_url}}. Activate flow → reactivate.html → Success. Badge confirmation emitted Template 24 ("QR Code Badge"), proving BLOCKER-1 fix (previously selected Template 29 "Conference QR Badge").

Yaprak's 70k campaign:
- ~12:00 — Yaprak uploaded Excel (41,222 rows, 34,041 unique emails after dedup; header bug `jot_title` corrected by Yaprak before upload). Background drain currently running at ~5 emails/sec (~2-2.5h ETA).

Lessons learned (operational rules):
- **L1 — SendGrid sends to invalid-DNS test domains:** `@leena-test.local`-style fake-domain bulk inserts trigger MX lookup → deferred → 72h retry → hard bounce. Reputation risk. Mitigations: (a) plus-addressing on real mailbox (`suer+test1@elan-expo.com`); (b) pre-add fake domain to SendGrid suppression before bulk send; (c) SendGrid sandbox mode for simulation. *Candidate ELL_RULES.md cross-system rule — pending Suer decision.*
- **L2 — PostgreSQL string match apostrophe types:** `'` (ASCII U+0027) and `'` (typographic U+2019) are distinct codepoints. Form inputs often autocorrect to typographic. SQL hardcoded strings WILL NOT match — derive byte-exact value from DB via subquery (this sprint's 76-visitor split SQL relied on this).
- **L3 — Render Shell vs external DB access:** Render Shell uses `$DATABASE_INTERNAL_URL`. External access requires IP whitelist via Render Dashboard → leena_v401_db → Inbound IP Rules — update when Suer's IP changes.

Open backlog from this sprint (post-fair):
- Generic token-based unsubscribe endpoint (replace manual "reply with UNSUBSCRIBE" instruction).
- SendGrid bounce/complaint webhook integration → automated `email_unsubscribes` population.
- `conferenceCleanup` 1→N split capability (current tool is 1→1 rename only; Day 1 & Day 2 → Topic 1 + Topic 5 done via manual SQL this sprint).
- `email_unsubscribes` per-expo or per-organizer-form scope (currently organizer-level — unsubscribing affects all expos for that organizer).
- Form 39 canonical topic typo cleanup ("Cool Plus Limit" → "Limited", duplicate spaces).
- Existing risks re-flagged for tracking: R5 stale 'processing' email recovery, R8 setImmediate orphan recovery, R9 reactivation_tokens UNIQUE(email,target_expo_id), R14 backend template `{{activation_url}}` placeholder validation.

**Reactivation Monitoring UI Sprint (13 May 2026, afternoon):**

Built on top of the 70k pre-launch sprint above, this pass turned the View Campaigns tab into a live monitoring surface and added a manual close lifecycle. Yaprak's 32k drain ran throughout — frontend deploys never touched the email worker (separate Render service).

Code commits (all deployed):
- **Tier 1 + 2 + Resend safety (`1b9c87e`..`777bb6c`, 7 commits):**
  - `1b9c87e` — Auto-refresh dropdown (Off/10s/30s/60s, default 30s) + "Last updated: X ago" indicator. Scoped to View Campaigns tab; pauses when user switches tabs; `beforeunload` clears intervals.
  - `0978a8c` — Progress bar + ETA per card. Formula: `(total_tokens - pending) / total_tokens` for drain progress; ETA = `pending / 300` minutes (5 email/sec worker throughput). Stalled-history heuristic: same `pending` across 3 consecutive refreshes → yellow fill + "Stalled?" warning.
  - `5d4de9e` — Activation Rate color coding: 0%=red, 1-5%=orange, 5%+=green. Native `title` tooltip "X out of Y activated".
  - `573d182` — Backend `GET /api/reactivation/campaign/:expoId/stats`. Returns per-status email_queue breakdown (count + MIN(created_at) + MAX(sent_at) FILTER `status='sent'`) plus top-level `last_global_sent_at`. SELECT only, organizer-scoped. EXPLAIN ANALYZE in production under 32k live drain: **45ms** (Parallel Seq Scan, expo_id+created_at 24h filter, no index added).
  - `695c28c` — Per-card "Mail Delivery Status" row: `📤 Sent / ⏳ Queued / ⚠️ Failed` + "Last email sent: X ago". 120s+ idle while queue > 0 → yellow "Worker may be stalled". `Promise.allSettled` per-card fetches.
  - `f31a6b1` — Backend `GET /api/reactivation/campaign/:expoId/is-active`. Returns `{ is_active, pending_count, last_queued_at }`. `is_active = (pending+processing in queue > 0) OR (queued in last 10 min)`. Drives resend button enabled state.
  - `777bb6c` — Resend button disabled-while-active + 3-layer confirm: (1) confirm "Resend N emails?" → (2) prompt "Type expo name EXACTLY" (case-sensitive) → (3) confirm "FINAL WARNING". Button carries `data-expo-id`/`data-expo-name`/`data-pending` for the flow.
- **Categorization + sort + test protection (`cdc295a`):**
  - 4 status badges: 🟢 Active, 🟡 Stalled, ⚪ Completed, 🔴 Test (test name prefix `[TEST]` overrides everything).
  - Card sort by `statusOrder = { Active:0, Stalled:1, Completed:2, Test:3 }`, then `last_queued_at` DESC within same status.
  - Test campaigns: permanent resend disable (tooltip "Test campaign — resend disabled to protect from accidental mass send"), `.is-test` opacity 0.55 on stats grid, progress fill gray, caption shows "Test campaign" instead of ETA.
  - Refactor: collapsed previous `loadAllResendButtonStates`/`updateResendButtonState` N+1 fetch pattern into a single batch `Promise.all` of `/is-active` calls that feeds both status computation and resend button state.
  - Empty-active hint: blue info bar above list when no Active/Stalled card exists.
- **Awaiting Activation badge (`0820b00`):**
  - New 🔵 Awaiting badge (`badge-awaiting`, blue). Triggered when `email_queue.pending = 0 AND reactivation_tokens.pending > 0`. Tooltip: "Email delivery complete. Waiting for user activations to come in over time."
  - Stalled redefined: queue still has pending rows AND worker idle 10+ minutes. No longer the catch-all bucket for drained-but-unactivated campaigns.
  - Before this fix, Yaprak's drained-but-pre-activation 32k campaign was wrongly flagged Stalled.
- **Past Campaigns separator + compact view (`384b3fe`):**
  - View Campaigns is now split into two visual sections. Top: full cards for Active/Awaiting/Stalled. Separator (`<hr>` + "PAST CAMPAIGNS" uppercase header). Bottom: compact rows (opacity 0.72, hover→1, single line "[icon] Name • Nk total • N activated (X%) [badge]").
  - Per-card render extracted to `buildFullCardHtml(c)` and new `buildCompactCardHtml(c)`.
  - `loadAllMailDeliveryStatus` and `applyResendButtonState` now iterate only `currentCampaigns` — compact cards skip their mailStatus + resendBtn DOM lookups.
- **Close Campaign + reopen (`4e61c35`) + migration 006:**
  - Migration: `migrations/006_reactivation_closed_at.sql` — `ALTER TABLE expos ADD COLUMN reactivation_closed_at TIMESTAMPTZ NULL, ADD COLUMN reactivation_closed_by INTEGER NULL`. Additive, IF NOT EXISTS, run from Render Shell.
  - Backend: `POST /api/reactivation/campaign/:expoId/close` (idempotent, 409 if already closed, 503 pre-migration), `POST /campaign/:expoId/reopen` (same surface). `GET /campaigns` augmented with `LEFT JOIN organizers o ON o.id = e.reactivation_closed_by` to surface `closed_by_name`, **wrapped in try/catch with legacy-query fallback** so the dashboard never breaks pre-migration.
  - Frontend: 🔒 Closed badge (`badge-closed`, indigo). `computeCampaignStatus` priority: Test > Closed > Active > Awaiting > Stalled > Completed. Full-card header shows a small "🔒 Close" link (current campaigns only). 2-layer confirm: (1) "Close this campaign? Visitors who haven't activated yet will no longer be expected" → (2) "...mark as closed, can reopen later". Closed campaigns render as compact cards in Past Campaigns with `• Closed on DD MMM YYYY by NAME` and a small Reopen link.
  - **Close is a UI/intent signal, not a kill switch** — email_worker keeps draining whatever is already in `email_queue`. Use case: stop expecting more activations from this list.

New endpoints (this sprint):
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/reactivation/campaign/:expoId/stats` | Per-status email_queue breakdown (last 24h), drives Mail Delivery Status row |
| GET | `/api/reactivation/campaign/:expoId/is-active` | Light yes/no for drain state, drives resend button + Active badge |
| POST | `/api/reactivation/campaign/:expoId/close` | Mark campaign as closed (UI/intent only) |
| POST | `/api/reactivation/campaign/:expoId/reopen` | Reverse close |

Schema delta:
- `expos.reactivation_closed_at TIMESTAMPTZ NULL`
- `expos.reactivation_closed_by INTEGER NULL` (soft FK to `organizers.id`, no constraint)

Badge taxonomy reference (6 states, priority order Test > Closed > Active > Awaiting > Stalled > Completed):

| Badge | Trigger | Meaning |
|-------|---------|---------|
| 🔴 Test | `expo_name` starts with `[TEST]` | Test data; resend permanently disabled |
| 🔒 Closed | `reactivation_closed_at IS NOT NULL` | Manually closed by admin; reopen available |
| 🟢 Active | `is_active=true` (queue has pending/processing OR queued in last 10 min) | Worker is sending right now |
| 🔵 Awaiting | `queue_pending=0 AND tokens_pending>0` | Drain done, healthy wait for clicks |
| 🟡 Stalled | `queue_pending>0 AND is_active=false` | Real problem: queue has work but worker idle 10+ min |
| ⚪ Completed | `tokens_pending=0 AND activated>0` | All resolved |

Reactivation monitor open backlog (post-fair):
- "Stalled" 3-fetch heuristic is intentionally short — replace with a smarter detector that considers actual worker `sent_at` cadence.
- Reactivation drop-off analytics: daily activation curve graph (currently only a single percentage).
- Auto-close N days after `expos.end_date` (replace manual close click for routine cases).
- ETA formula currently hardcoded at 300/min (5/sec) — make dynamic from observed throughput.
- Custom modal in place of native `prompt()` for 3-layer resend confirm (some browsers let users mute prompts).
- Bulk-card SendGrid stats endpoint (current per-card fetch is fine at 1-3 expos; revisit if list grows).

**Test Email Cleanup (14 May 2026):**
- 5 internal test email addresses removed from all expos to give Mega Clima Nigeria 2026 (19-21 May) clean baseline metrics:
  - `yaprakguzelcik@gmail.com` (27 visitor rows across expos 1, 3, 5, 7, 9, 10)
  - `suer@elan-expo.com` (3 rows: expos 3, 5, 7)
  - `elan02@elan-expo.com` (7 rows: expos 3, 5, 6, 7, 8, 9, 10)
  - `info@siemamaroc.com` (4 rows: expos 3, 5, 7, 9)
  - `info@moroccofoodexpo.com` (4 rows: expos 3, 5, 6, 7)
- Migration: `migrations/007_test_email_cleanup.sql` (commits `aae78f4` original, `aa7dbcc` post-dry-run fix)
- Backup: `visitors_test_backup_20260514` (46 visitor rows snapshot — DROP after fair end 21 May 2026; see todo.md post-fair backlog)
- Rows affected: 46 visitors + ~389 related rows across 10 tables (campaign_recipients, conference_certificates, exhibitor_leads, reactivation_tokens, visitor_event_status, email_queue, email_logs, email_events via CASCADE, checkins via CASCADE).
- **First cleanup-pattern migration in this repo.** Migrations 001-006 are schema-only; 007 is the first data-only / pre-fair-housekeeping migration. Wrapped in a single transaction with explicit pre-cleanup of all RESTRICT FKs before the visitors DELETE.
- **Audit gap surfaced + caught by dry-run:** initial FK audit (13 May "delete capability" analysis) only mapped FKs pointing TO `visitors.id` and missed inbound FKs on the intermediate tables. Specifically `email_queue.campaign_recipient_id → campaign_recipients(id)` is a RESTRICT FK that blocked the first dry-run. Fix added a new STEP 1 in the migration to clean those email_queue rows before STEP 2 deletes campaign_recipients. No data harmed — transaction rolled back cleanly.
- **Two-phase migration pattern proven and adopted as the template for future cleanup migrations:**
  1. Phase 1 — dry run: `sed 's/^COMMIT;$/ROLLBACK;/' migrations/NNN.sql | psql $DATABASE_INTERNAL_URL` — runs every DELETE, prints row counts, rolls back at end. Any FK violation or syntax error surfaces here, zero risk to production data.
  2. Phase 2 — real run: `psql $DATABASE_INTERNAL_URL -f migrations/NNN.sql` — same file, but COMMIT instead of ROLLBACK at end.
- Apply this template to upcoming post-fair cleanup work: country pollution (44 distinct strings → ~33 canonical, audit 14 May), conference topic variants beyond what `conferenceCleanup.js` can handle (see ADR-021 + post-fair TODO).
- Verification post-execute: `SELECT COUNT(*) FROM visitors_test_backup_20260514` → 46; all four `remaining_*` validation counters → 0.

**Conference Scanner Pre-Display + Force Confirm (14 May 2026):**
- `public/conference-scanner.html` — two UX layers added before fair-day operation:
  - **Change A:** Visitor preview between QR lookup and `/checkin-and-certify` call. Hostess sees visitor's currently-registered sessions (parsed from `custom_fields.conference_topic` via `" || "` split) and a match/mismatch banner for the selected session, then taps "Confirm & Issue Certificate" or "Cancel / Re-scan". New helpers: `showVisitorPreview`, `confirmAndIssue`, `cancelPreview`, `splitTopicsClient`.
  - **Change B:** Custom confirm modal wrapping the "Save & Send Certificate" button in `showUnregCard`. Two-step: hostess must tap "Yes, Issue Certificate" in the modal (danger-red) after reading "this action cannot be undone". New helpers: `confirmForce`, `closeForceConfirm`, `executeForceCertify`.
- Backend untouched. `/checkin-and-certify` POST body shape, response handling, `forceCertify()` body, `showUnregCard` layout — all preserved. Only the call-site wrappers and pre-display layer added.
- Field name compatibility verified: backend response uses `customFields` (camelCase, `terminalCheckins.js:190` transforms snake_case `custom_fields` column).
- Frontend-only deploy (Render web service auto-deploy ~30s); email worker separate service, unaffected.
- Commit: `27ddae7`. Deploy verified 14 May 2026 11:38 UTC.
- Audit reference: `CONFERENCE_FORCE_AUDIT_20260514.md` (Karar Soru 2 + Karar Soru 3).

### Conference Topic Architecture

**Current model (legacy):** Conference topics stored as free-text in `visitors.custom_fields->>'conference_topic'` (multi-topic via `" || "` separator) and `conference_certificates.conference_topic` column. Canonical source: `forms.fields` JSONB array for active conference form per expo.

**Known issue:** No canonical entity model. Renaming requires multi-table updates. Form changes don't propagate to existing visitors. Anti-pattern documented in ell-docs ADR-021.

**Cleanup tool (temporary):** `/api/conference-cleanup` endpoints allow bulk segment-aware rename of variants to canonical topic within an expo. Transaction-wrapped, conflict-detection (cert UNIQUE constraint), CHUNK_SIZE=100.

**Planned refactor (post-fair):** Conference Entity Migration — new tables `expo_conferences` (id, expo_id, name, day, order_no) and `visitor_conferences` (junction). See ADR-021.

### v4.0.2 (6 Şubat 2026)
- Import email QR fix (UUID → img tag)
- Reactivation Campaign modülü
- Email worker iki mod desteği
- Existing visitor re-registration email
- Webhook log formatı iyileştirmesi

### v4.0.1
- Temel EMS sistemi (expo, visitor, checkin, form, email, badge, terminal)
