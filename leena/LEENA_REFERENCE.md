# Leena EMS — Referans (Dizin / Şema / API)

Bu dosya `CLAUDE.md`den ayrıldı (20 Temmuz 2026). Otomatik yüklenmez; gerektiğinde okuyun.

---

## Dizin Yapısı

```
backend/leena-v401-backend/
├── index.js                    # Ana giriş noktası (CORS, static serve, route mount)
├── initial.sql                 # Temel DB şeması (DİKKAT: production ile tam senkron DEĞİL)
├── migrations/
│   ├── 001_floorplan_tables.sql # Floor Plan Builder tables (expo_halls, expo_floorplan_versions, expo_stands, expo_stand_cells)
│   ├── 002_reactivation_form_id.sql # Adds form_id to reactivation_tokens for design inheritance
│   └── 003_exhibitors_table.sql # Exhibitor registry (expo_exhibitors) + expo_stands.exhibitor_id FK
├── email_worker.js             # Async email kuyruğu işçisi (Render Background Worker)
├── routes/
│   ├── auth.js                 # Login/Register, JWT
│   ├── organizers.js           # Organizer profil (GET /, GET /:id)
│   ├── expos.js                # Expo CRUD + stats
│   ├── visitors.js             # Visitor CRUD, import (upsert), manual registration, badge
│   ├── forms.js                # Form CRUD (9 endpoint, public submit dahil)
│   ├── checkins.js             # Check-in listeleme + stats
│   ├── checkinReports.js       # Check-in rapor verileri (saatlik/günlük)
│   ├── terminalCheckins.js     # Terminal check-in + visitor-by-qr + visitor-by-email + badge-print
│   ├── terminals.js            # Terminal CRUD (5 endpoint)
│   ├── webhook.js              # Zoho form webhook + existing visitor email resend
│   ├── emailSend.js            # Bulk + single email gönderimi
│   ├── emailTemplates.js       # Email template CRUD + defaults
│   ├── emailSegments.js        # Email segment yönetimi (send)
│   ├── emailInbound.js         # Inbound email webhook (POST /inbound)
│   ├── import-checkins.js      # Checkin import (POST /, GET /stats)
│   ├── reports.js              # Raporlama (summary, export, comparison)
│   ├── badgeTemplates.js       # Badge template CRUD + terminal endpoint
│   ├── reactivation.js         # Reactivation campaign API + resend-pending
│   ├── leads.js                # Exhibitor lead scanner API (public, QR auth)
│   ├── conferenceCertificates.js # Conference certificate system (scan, certify, email)
│   └── floorplan.js            # Floor Plan Builder CRUD (halls, versions, stands, cells)
├── middleware/
│   ├── authMiddleware.js       # JWT doğrulama (req.organizer_id atar)
│   ├── auth.js                 # Alternatif JWT middleware (req.user objesi atar — aşağıya bak)
│   └── terminalAuth.js         # Terminal key doğrulama (x-terminal-key header)
├── utils/
│   ├── db.js                   # PostgreSQL bağlantısı (pool)
│   ├── email.js                # processEmailTemplate helper
│   └── qrcode.js               # QR generation helpers
├── public/                     # TÜM frontend dosyaları burada
│   ├── login.html                  # Login sayfası (Gen 4 modern UI, login+register tabs)
│   ├── dashboard_new.html              # Expo seçim sayfası (login sonrası ilk durak)
│   ├── main-panel-v2.html          # Ana dashboard (expo seçildikten sonra)
│   ├── visitorlog-paginated.html   # Visitor listesi + visitor_type filtre
│   ├── qrscanner.html              # Terminal QR tarayıcı + email arama + popup badge
│   ├── badge.html                  # Badge görüntüleme (word-wrap, auto-size)
│   ├── badge-templates.html        # Badge template yönetimi + bulk print
│   ├── form-builder.html
│   ├── form-list.html
│   ├── checkins.html
│   ├── terminals.html
│   ├── email-templates.html
│   ├── email-segments.html
│   ├── email-send.html
│   ├── reactivation-campaign.html  # Campaign yönetimi + resend to pending
│   ├── reactivate.html             # Visitor onay sayfası (public)
│   ├── reports.html                # Genel raporlar
│   ├── checkin-reports.html        # Check-in analytics dashboard (Charts, CSV export)
│   ├── lead-scan.html              # Exhibitor lead scanner (public, mobil, kamera QR)
│   ├── import.html
│   ├── register.html               # Organizer kayıt
│   ├── expo-create.html            # Expo oluşturma
│   ├── form-public.html            # Public form submit sayfası
│   ├── badge-print.html            # Badge print sayfası
│   ├── checkin-import.html         # Checkin import sayfası
│   ├── conference-sessions.html    # Conference topic tracking + targeted email
│   ├── email-history.html          # Email send history log (paginated, filtered)
│   ├── conference-scanner.html    # Hostess conference check-in scanner (mobile, terminal auth)
│   ├── certificate.html           # Public certificate view (print-to-PDF)
│   ├── floorplan-builder.html     # Floor Plan Builder (Konva.js canvas, ES modules)
│   ├── floorplan/                 # Floor Plan Builder JS modules (ES modules)
│   │   ├── api.js                 # API fetch wrapper
│   │   ├── state.js               # Central state + event emitter
│   │   ├── grid.js                # Konva grid rendering, zoom/pan, cell interaction
│   │   ├── stands.js              # Stand CRUD, detail panel, stats
│   │   └── toolbar.js             # Tool selection, hall/version dropdowns
│   └── assets/                     # Logo vb.
# ⚠️ public/ altında *.backup.html ve eski varyantlar (dashboard.html,
#    admin-dashboard.html, main-panel.html) mevcut, aktif olarak kullanılmıyor.
#    login_new.html sadece login.html'e redirect yapar (eski bookmark uyumu).
└── uploads/                    # Kullanıcı yüklemeleri
```

---

---

## Veritabanı Şeması

### Ana Tablolar

| Tablo | Amaç |
|-------|------|
| organizers | Hesap sahipleri, auth |
| expos | Etkinlik tanımları (organizer_id) |
| visitors | Kayıt verileri (organizer_id, expo_id, form_id) — TEK kişi kaynağı |
| checkins | Giriş logları (visitor_id, expo_id, terminal, hall, checkin_time) |
| visitor_event_status | Kişi başı event durumu (check-in yapılınca upsert) |
| terminals | Fiziksel tarayıcı tanımları (terminal_key ile auth) |
| forms | Kayıt form yapılandırması (email_template_id) |
| email_templates | HTML email tasarımları (organizer_id) |
| email_queue | Async email görevleri (iki mod: direct HTML veya visitor+template) |
| badge_templates | Badge tasarımları (visitor_type bazlı) |
| email_logs | Email gönderim logları (emailSend + emailSegments tarafından yazılır) |
| reactivation_tokens | Kampanya tokenları (source_expo_id → target_expo_id) |
| exhibitor_leads | Exhibitor lead kayıtları (exhibitor_company bazlı) |
| import_logs | Import operation logs (per-import stats, errors, options) |
| conference_certificates | Conference attendance certificates (visitor_id, expo_id, topic, token) |
| expo_halls | Floor Plan: physical hall definitions (expo_id, grid dimensions) |
| expo_floorplan_versions | Floor Plan: plan versions per hall (draft/active/archived) |
| expo_stands | Floor Plan: stand units (cells-based geometry, commercial status) |
| expo_stand_cells | Floor Plan: individual grid cells per stand (1 row = 1m²) |
| expo_stand_assignments | Floor Plan: assignment history (Phase 2, not used in MVP) |
| expo_exhibitors | Exhibitor registry per expo (name, contact, email, sector, company_id nullable) |

### visitors Tablosu Önemli Kolonlar
- `id`, `name`, `last_name`, `email` (unique per expo), `phone`
- `company`, `country`, `job_title`
- `visitor_type` — visitor, exhibitor, conference, vip, press, staff, speaker (DEFAULT: visitor) — DB: free TEXT, no constraint
- `booth_number` — exhibitor'lar için stand numarası
- `qr_code` — unique UUID (upsert'te korunur, DEĞİŞMEZ)
- `badge_id` — qr_code'un ilk 8 karakteri
- `source` — manual, form, import, webhook, email
- `origin` — massimport, manual_entry, zoho, manual_email_send
- `expo_id`, `organizer_id`, `form_id`
- `updated_at` — upsert'te güncellenir
- `custom_fields` — JSONB (ek alanlar)

### exhibitor_leads Tablosu (v402+)
```sql
CREATE TABLE exhibitor_leads (
  id SERIAL PRIMARY KEY,
  expo_id INTEGER NOT NULL REFERENCES expos(id),
  exhibitor_visitor_id INTEGER NOT NULL REFERENCES visitors(id),
  exhibitor_company VARCHAR(255) NOT NULL,
  lead_visitor_id INTEGER NOT NULL REFERENCES visitors(id),
  scanned_at TIMESTAMPTZ DEFAULT NOW(),
  notes TEXT
);
```

### email_logs Tablosu
Email gönderim sonuçlarının loglandığı tablo. `emailSend.js` ve `emailSegments.js` tarafından yazılır.
- `id`, `organizer_id`, `expo_id`, `visitor_id`, `template_id`
- `email` — Alıcı email adresi
- `status` — sent, failed
- `message` — Hata/başarı mesajı
- `sent_at` — Gönderim zamanı

### email_queue Ek Kolonlar (v402)
- `recipient_email`, `subject`, `html_content` — Direct HTML modu için
- `sent_at`, `error_message` — Takip için

### conference_certificates Tablosu (v402+)
```sql
CREATE TABLE conference_certificates (
  id SERIAL PRIMARY KEY,
  visitor_id INTEGER NOT NULL REFERENCES visitors(id),
  expo_id INTEGER NOT NULL REFERENCES expos(id),
  organizer_id INTEGER NOT NULL,
  conference_topic TEXT NOT NULL,
  certificate_token VARCHAR(64) NOT NULL UNIQUE,
  email_sent BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(visitor_id, expo_id, conference_topic)
);
```
- One certificate per visitor per topic (UNIQUE constraint)
- `certificate_token` used for public certificate URL
- Written by `conferenceCertificates.js` on conference check-in

### forms.config JSONB Usage (v403)
The `config` column stores style configuration for form design customization:
```
config.style.headerBannerImage (base64 data URI or null)
config.style.headerBannerColor, headerGradientEnd, headerHeight
config.style.footerBannerImage, footerBannerColor, footerGradientEnd, footerHeight, footerText
config.style.primaryColor, backgroundColor, fontFamily, buttonText, borderRadius
```
Default fallback: when config is null, hardcoded CSS defaults apply (backward compatible).

### reactivation_tokens.form_id (v403)
- `ALTER TABLE reactivation_tokens ADD COLUMN form_id INTEGER REFERENCES forms(id)`
- Links reactivation campaigns to a form's design (colors, banners)
- NULL = default yellow theme preserved

### expo_exhibitors (v403)
```sql
CREATE TABLE expo_exhibitors (
  id SERIAL PRIMARY KEY,
  expo_id INTEGER NOT NULL REFERENCES expos(id) ON DELETE CASCADE,
  organizer_id INTEGER NOT NULL REFERENCES organizers(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  contact_person VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(100),
  country VARCHAR(100),
  sector VARCHAR(100),
  company_id INTEGER,  -- LiFFY FK (nullable, no constraint — ADR-014)
  notes TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```
- Basic exhibitor registry per expo
- `expo_stands.exhibitor_id` FK links stands to exhibitors
- `company_id` nullable — will link to LiFFY companies when Phase 2 ready

> **⚠️ Gerçek şemayı görmek için her zaman production DB'yi kontrol et, initial.sql'e güvenme.**

---

---

## API Endpoint Özeti

### Auth
- `POST /api/auth/login` — Giriş, JWT döner
- `POST /api/auth/register` — Kayıt

### Organizers
- `GET /api/organizers` — Organizer listesi
- `GET /api/organizers/:id` — Organizer detay

### Expos
- `GET /api/expos` — Expo listesi
- `GET /api/expos/:id` — Expo detay
- `GET /api/expos/slug/:slug` — Slug ile expo arama
- `POST /api/expos` — Yeni expo oluştur
- `PUT /api/expos/:id` — Expo güncelle
- `DELETE /api/expos/:id` — Expo sil
- `GET /api/expos/:id/stats` — Expo istatistikleri

### Visitors
- `GET /api/visitors/paginated` — Sayfalı listeleme (search, source, origin, visitor_type, conference_topic, date filtreleri + conference_topic computed column)
- `GET /api/visitors/export` — Excel export of ALL filtered visitors (.xlsx download, same filters as /paginated but no pagination)
- `GET /api/visitors/conference-topics` — Conference topic counts with check-in data ({topic, registered_count, checked_in_count})
- `GET /api/visitors/badge/:qr_code` — Badge görüntüleme
- `POST /api/visitors/public` — Public form submit (auth yok)
- `POST /api/visitors/manual` — Manuel kayıt (upsert)
- `POST /api/visitors/import` — Excel import (upsert: varsa güncelle+QR koru, yoksa oluştur)
- `GET /api/visitors/import-logs` — Import history logs (paginated, ?page=1&limit=20&expo_id=)
- `PUT /api/visitors/:id` — Visitor edit (name, email, company, job_title, phone, country, visitor_type, booth_number, conference_topic — qr_code/badge_id protected, auth required)
- `GET /api/visitors/sources` — Distinct source values for filter dropdown (auth required)
- `POST /api/visitors/bulk-email` — Bulk email send to filtered visitors (Mode 2 queue, transaction, 10K limit, auth required)
- `GET /api/visitors/:id/emails` — Visitor email history (email_queue + email_logs, auth required)

### Forms
- `GET /api/forms` — Form listesi
- `GET /api/forms/expo/:expo_id` — Expo'ya ait formlar
- `GET /api/forms/:id` — Form detay
- `GET /api/forms/:id/submissions` — Form submission'ları
- `GET /api/forms/public/:id` — Public form görüntüleme (auth yok)
- `POST /api/forms` — Yeni form oluştur
- `PUT /api/forms/:id` — Form güncelle
- `PATCH /api/forms/:id/toggle` — Form aktif/pasif toggle
- `POST /api/forms/clone/:id` — Form klonla (cross-expo clone)
- `DELETE /api/forms/:id` — Form sil
- `POST /api/forms/upload-banner` — Banner image upload (base64, max 500KB, authMiddleware)

### Terminal
- `GET /api/terminal/visitor-by-qr` — QR ile visitor arama
- `GET /api/terminal/visitor-by-email` — Email ile visitor arama (⚠️ camelCase response: qrCode)
- `POST /api/terminal/checkin` — Check-in (x-terminal-key auth)
- `POST /api/terminal/badge-print` — Badge print kaydı
- `GET /api/terminal/status` — Terminal durum kontrolü

### Terminals (CRUD)
- `GET /api/terminals` — Terminal listesi (expo_id required)
- `GET /api/terminals/all` — Tüm terminaller (expo_name dahil)
- `POST /api/terminals` — Yeni terminal oluştur
- `POST /api/terminals/clone/:id` — Terminal klonla (cross-expo clone, yeni terminal_key)
- `PUT /api/terminals/:id` — Terminal güncelle
- `PATCH /api/terminals/:id/toggle` — Terminal aktif/pasif toggle
- `DELETE /api/terminals/:id` — Terminal sil

### Checkins
- `POST /api/checkins` — Check-in oluştur
- `GET /api/checkins` — Listeleme (pagination, filtreler, visitor detayları dahil)
- `GET /api/checkins/stats/summary` — Özet istatistikler (total, unique, today, by_hall, by_source)
- `GET /api/checkins/stats` — İstatistikler (alternatif)

### Checkin Reports
- `GET /api/checkins/reports` — Check-in rapor verileri (saatlik/günlük dağılım)

### Import Checkins
- `POST /api/import-checkins` — Checkin import
- `GET /api/import-checkins/stats` — Import istatistikleri

### Webhook
- `POST /api/webhook/zoho/:org/:expo/:form` — Zoho form webhook (existing visitor → update+resend)

### Email Templates
- `GET /api/email-templates` — Template listesi (`{success, templates}`)
- `GET /api/email-templates/templates` — Template listesi (alternatif format)
- `GET /api/email-templates/:id` — Template detay
- `POST /api/email-templates` — Yeni template oluştur
- `PUT /api/email-templates/:id` — Template güncelle
- `DELETE /api/email-templates/:id` — Template sil
- `POST /api/email-templates/clone/:id` — Clone template (cross-expo clone)
- `POST /api/email-templates/defaults` — Create default templates

### Email Send
- `POST /api/email-send/single` — Tekli email gönderimi
- `POST /api/email-send/bulk` — Toplu email gönderimi
- `GET /api/email-send/history` — Email send history (paginated, filtered by expo_id, template_id, status, email search)

### Email Segments
- `POST /api/email-segments/send` — Segment bazlı email gönderimi

### Email Inbound
- `POST /api/email/inbound` — Inbound email webhook (SendGrid parse)

### Reports
- `GET /api/reports/summary` — Özet rapor (visitor_type_breakdown, job_title_breakdown, daily_checkin_trend, checkin_by_hall, checkin_by_terminal dahil)
- `GET /api/reports/export` — Rapor export
- `GET /api/reports/comparison` — Karşılaştırma raporu

### Reactivation
- `GET /api/reactivation/campaigns` — Kampanya listesi
- `GET /api/reactivation/campaign/:expoId` — Detay
- `POST /api/reactivation/create-from-excel` — Excel'den kampanya
- `POST /api/reactivation/create-from-expo` — Expo'dan kampanya
- `POST /api/reactivation/resend-pending` — Pending'lere yeni template ile tekrar gönder
- `GET /api/reactivation/verify/:token` — Token doğrula (PUBLIC)
- `POST /api/reactivation/activate` — Aktivasyon (PUBLIC)
- `GET /api/reactivation/stats/:expoId` — İstatistikler

### Leads (Exhibitor Lead Scanner)
- `POST /api/leads/auth` — Exhibitor QR ile giriş (PUBLIC, visitor_type=exhibitor kontrolü)
- `POST /api/leads/scan` — Visitor QR okutarak lead kaydet (duplicate kontrolü)
- `GET /api/leads/list` — Firma bazlı lead listesi (exhibitor_company + expo_id)

### Badge Templates
- `GET /api/badge-templates` — Listeleme
- `GET /api/badge-templates/:id` — Template detay
- `POST /api/badge-templates` — Yeni template oluştur
- `PUT /api/badge-templates/:id` — Template güncelle
- `DELETE /api/badge-templates/:id` — Template sil
- `GET /api/badge-templates/for-terminal/:terminalKey` — Terminal'e atanmış template

### Conference Certificates
- `POST /api/conference-certificates/checkin-and-certify` — Conference check-in + certificate email (terminalAuth). Validates registration via `isVisitorRegisteredForTopic()`. Supports `force: true` to add topic + issue cert for unregistered visitors.
- `POST /api/conference-certificates/resend` — Resend existing certificate email (terminalAuth). Uses existing `certificate_token`, no new cert created. Subject gets "(Resent)" suffix.
- `GET /api/conference-certificates/verify/:token` — Public certificate data (no auth, token-based)
- `GET /api/conference-certificates/topics` — Conference topics for hostess dropdown (terminalAuth). Unnests `" || "`-separated multi-topic values.
- `GET /api/conference-certificates/stats` — Certificate stats per topic (JWT auth)

### Floor Plan Builder
- `GET /api/floorplan/halls?expo_id=X` — Hall list for expo (JWT)
- `POST /api/floorplan/halls` — Create hall (JWT)
- `PUT /api/floorplan/halls/:id` — Update hall (JWT)
- `GET /api/floorplan/halls/:hallId/versions` — Version list for hall (JWT)
- `POST /api/floorplan/halls/:hallId/versions` — Create new draft version (JWT)
- `GET /api/floorplan/versions/:versionId/stands` — All stands + cells for version (JWT)
- `POST /api/floorplan/versions/:versionId/stands` — Create stand with cells (JWT, transaction)
- `PUT /api/floorplan/stands/:id` — Update stand (structural=draft only, commercial=active OK)
- `PUT /api/floorplan/stands/:id/status` — Change commercial status (allowed on active)
- `PUT /api/floorplan/stands/:id/move` — Move stand cells (draft-only, transaction)
- `POST /api/floorplan/stands/:id/split` — Split stand into 2+ stands (draft-only, transaction)
- `POST /api/floorplan/stands/merge` — Merge 2+ stands into one (draft-only, transaction)
- `DELETE /api/floorplan/stands/:id` — Delete stand (JWT, draft-only)
- `POST /api/floorplan/versions/:id/activate` — Activate version (draft→active, archives current)
- `POST /api/floorplan/versions/:id/clone` — Clone version (deep copy stands+cells)
- `PUT /api/floorplan/versions/:id` — Update version label/notes

### Inline Endpoint'ler (index.js)
- `GET /api/templates` — Form-builder dropdown için email template listesi
- `GET /api/qr-image/:qrcode` — Dinamik QR kod resmi (PNG)
- `GET /health` — Health check

---
