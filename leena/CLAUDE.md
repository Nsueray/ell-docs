# CLAUDE.md — Leena EMS

> Bu dosya Claude Code'un her oturumda otomatik okuduğu proje hafızasıdır.
> Son güncelleme: 18 Mayıs 2026 | Versiyon: v4.0.5

---

## ELL Cross-System Rules
Before making architectural decisions, read: `docs/ELL_RULES.md`
If in doubt, mark with 🔶 ELL onayı gerek and ask the user to check with ELIZA chat.

---

## 🔴 ANA KURALLAR (HER ZAMAN GEÇERLİ, İSTİSNASIZ)

### KURAL 1: TAHMİN YÜRÜTME YASAĞI
Tahmin yürüterek kod yazmak veya değişiklik yapmak **kesinlikle yasaktır.**
- Önce analiz yap, ilgili dosyaları oku, veri akışını takip et
- Kesin emin olduktan sonra değişiklik öner
- Emin değilsen → DUR, sor, dosyayı oku
- Asla "muhtemelen böyledir" diye kod yazma
- Fonksiyon isimleri, parametreler, DB kolonları, değişkenler — hepsini dosyadan doğrula

Eksik bilgi varsa:
1. Durmalısın
2. İlgili dosyayı `cat` ile okumalısın
3. Yanıtı bekleyip ondan sonra devam etmelisin

### KURAL 2: MEVCUT SİSTEMİ BOZMA YASAĞI
Leena.app **aktif olarak kullanılmaktadır.** Mevcut sistemi bozacak hiçbir değişiklik yapılamaz.
- Her değişiklik öncesi "bu mevcut işleyişi bozar mı?" sorusu sorulmalı
- Backward compatibility her zaman korunmalı
- Mevcut endpoint'lerin davranışı değiştirilmemeli
- Riskli değişikliklerde detaylı açıklama hazırla ve onay al

### KURAL 3: VERİTABANI DEĞİŞİKLİĞİ KISITLAMASI
DB ve tablolarda değişiklik yapmak **varsayılan olarak yasaktır.**
- Yeni tablo/kolon eklemek nispeten güvenlidir ama yine de onay gerekir
- `DROP`, `DELETE`, `ALTER ... DROP COLUMN` gibi yıkıcı operasyonlar özellikle tehlikelidir
- Detaylı açıklama hazırla (hangi tablo, hangi kolon, neden, ne etkilenir)

### KURAL 4: DEĞİŞİKLİK DÖKÜMANTASYONU ZORUNLULUĞU
Yapılan **her değişiklik** bu CLAUDE.md dosyasına güncellenmelidir.
- **Güncellenmemiş CLAUDE.md = eksik iş**

---

## Proje Nedir?

**Leena EMS**, fuar/kongre yönetimi için geliştirilmiş B2B SaaS platformudur. Organizatörler etkinlik oluşturur, ziyaretçiler kayıt olur, giriş çıkışlar QR kod ile takip edilir, otomatik email'ler gönderilir.

### Temel Tasarım Prensipleri

1. **Tek Sistem, Değişen Fuarlar:** Yeni fuar açmak = yeni sistem kurmak DEĞİL. Fuarlar (expo) sistem içinde değişen varlıklardır.

2. **Tek Kişi Kaynağı (Single Source of Truth):** Sistemde tek bir kişi tablosu vardır (`visitors`). Visitor, Exhibitor, Conference, VIP, Press, Staff, Speaker — hepsi aynı tabloda, farkı `visitor_type` alanı belirler.

3. **Exhibitor = visitor_type, ayrı tablo DEĞİL:** Exhibitor visitors tablosunda `visitor_type='exhibitor'` olarak tutulur. Tek QR, tek badge, tek check-in sistemi.

---

## Ortam Bilgileri

### Lokal Geliştirme
- **Proje Dizini:** `/Users/nsa/Desktop/Leena_v401_monorepo`
- **Backend+Frontend Kökü:** `backend/leena-v401-backend/`
- Backend ve frontend aynı repo, aynı dizin
- `app.use(express.static(path.join(__dirname, 'public')));` (index.js satır 46)

### GitHub
- **Repo:** `https://github.com/Nsueray/Leena_v401_monorepo.git`

### Production
- **Domain:** `https://leena.app`

### Render Servisleri (3 adet — hepsi Oregon region)
| Servis | Tip | Açıklama |
|--------|-----|----------|
| **Leena_v401** | Web Service (Node.js) | Ana uygulama + API + frontend |
| **leena-email-worker** | Background Worker (Node.js) | `node email_worker.js` |
| **leena_v401_db** | PostgreSQL 17 (Managed DB) | Veritabanı |

### DB Bağlantısı
```
psql "postgresql://leena_v401_db_user:xlM5m9TWwT4gXqqiicMA6QjZboJ6njmu@dpg-d2smvl75r7bs73al6scg-a/leena_v401_db"
```

### Database Access

**Read-only (Claude Code, local development):**
- Connection: `process.env.RENDER_DATABASE_READONLY_URL`
- User: `claude_readonly`
- Permission: SELECT only — UPDATE/DELETE/INSERT/ALTER/DROP fail
- Use for: Analysis, hypothesis testing, COUNT/JOIN/EXPLAIN
- Located in: `backend/leena-v401-backend/.env`

**Read-write (Suer, Render Shell only):**
- Connection: `$DATABASE_INTERNAL_URL` from inside Render Shell
- User: `leena_v401_db_user`
- Permission: Full
- Use for: Migrations, cleanup, data fixes — executed by Suer manually

**Rule:** Claude Code uses ONLY read-only for analysis. If a task requires UPDATE/DELETE/INSERT/ALTER/TRUNCATE/CREATE/DROP, prepare the SQL and ask Suer to run it via Render Shell.

**IP Whitelist:** External access requires Suer's current IP in Render's PostgreSQL Inbound IP Rules. If connection fails with "SSL connection has been closed unexpectedly", the IP may have changed — Suer needs to update via Render Dashboard → leena_v401_db → PostgreSQL Inbound IP Rules.

### Deploy Akışı
```
git add . → git commit -m "mesaj" → git push → Render otomatik deploy
```
⚠️ `git push` = production'a deploy. Dikkatli ol.

---

## Teknoloji Stack

| Katman | Teknoloji |
|--------|-----------|
| Backend | Node.js + Express **5.1.0** (⚠️ Express 5 — v4'ten önemli API farkları var) |
| Veritabanı | PostgreSQL 17 (Render Managed) |
| Frontend | Static HTML/JS (Express static serve, `public/` klasörü) |
| Email | SendGrid (async email_worker ile) |
| QR | Sunucu tarafı QR üretimi (uuid v4) |
| CSS | Sayfa bazlı inline CSS (Inter font, Bootstrap Icons) |
| Auth | JWT (organizer), x-terminal-key (terminal) |
| Hosting | Render.com |

---

## Dizin Yapısı

→ Taşındı: [LEENA_REFERENCE.md](./LEENA_REFERENCE.md)

---

## Veritabanı Şeması

→ Taşındı: [LEENA_REFERENCE.md](./LEENA_REFERENCE.md)

---

## Kimlik Doğrulama

### 1. Organizer Auth (JWT)
- `POST /api/auth/login` → JWT token
- Frontend: `localStorage.getItem('token')`
- Header: `Authorization: Bearer <token>`
- **İki farklı JWT middleware var:**
  - `middleware/authMiddleware.js` — `req.organizer_id` atar. Çoğu route bunu kullanır.
  - `middleware/auth.js` — `req.user` objesi atar (`{id, email, organizer_id}`). Daha esnek payload parsing: `decoded.id || decoded.organizer_id || decoded.userId`. JSON response döner.
- **⚠️ JWT expire olduğunda UI çalışıyor gibi görünür ama veri yazılmaz (sessiz kayıp)**

### 2. Terminal Auth (Key-Based)
- JWT yok, `x-terminal-key` header'ı kullanılır
- `middleware/terminalAuth.js` ile doğrulanır
- **Süresiz** — event admin kapatana kadar açık
- Terminal işlemleri: badge lookup, check-in, email arama

### 3. Public Endpoint'ler (Auth yok)
- `/api/reactivation/verify/:token`, `/api/reactivation/activate`
- `/api/leads/auth`, `/api/leads/scan`, `/api/leads/list`
- Badge görüntüleme, public form submit

---

## Kritik Veri Akışları

### A. Zoho Webhook → Visitor
```
Zoho Form POST → /api/webhook/zoho/:org/:expo/:form
  → x-webhook-token doğrula → badge_id & qr_code üret
  → INSERT visitors (veya UPDATE if existing email — keep QR, resend email)
  → Email gönder (SendGrid via email_queue)
```

### B. Check-in (Terminal)
```
Terminal QR tarar → POST /api/terminal/checkin (x-terminal-key)
  → checkins INSERT + visitor_event_status UPSERT
```

### C. Import (Upsert + Email/QR Options + Custom Fields)
```
Excel upload → POST /api/visitors/import
  → Custom fields extraction: columns NOT in knownColumns → customFields JSONB
  → Per row: email+expo_id check
  → Existing: UPDATE (COALESCE, custom_fields merge) + optional email (resent/first_time) + optional QR regen
  → New: INSERT (new UUID qr_code) + optional email
  → Custom field placeholders (e.g. {{conference_topic}}) work in email templates via ...customFields spread
  → New params: existing_email_option (none|resent|first_time), existing_qr_option (keep|regenerate), existing_template_id
  → Defaults: email=none, qr=keep (backward compatible — no params = old behavior)
```

### D. Manual Registration (Upsert)
```
QR Scanner manual form → POST /api/visitors/manual
  → Aynı upsert mantığı: varsa güncelle (QR koru), yoksa oluştur
```

### E. QR Scanner Email Arama
```
Scanner input'a email yazılırsa (@içeriyorsa):
  → Terminal modda: GET /api/terminal/visitor-by-email?email=X
  → Normal modda: GET /api/visitors/paginated?search=X&limit=1
  → Bulunan visitor'ın qr_code'u ile normal akış devam eder
```

### F. Badge Print
- QR scan / manual registration sonrası `window.open(badge.html?qr=X&terminal_key=Y, popup)`
- Scanner sayfası açık kalır (popup olarak açılır, redirect yok)
- Badge text: word-wrap aktif, auto-size (15/25 karakter threshold)

### G. Email Worker (İki Mod)
```
MODE 1 — Direct HTML: html_content + recipient_email varsa direkt gönder
MODE 2 — Visitor + Template: visitor_id + template_id → bilgi çek → template işle → gönder
```

### H. Reactivation Campaign
```
Admin: Excel veya kaynak expo seç → token üret → email_queue'ya ekle
Visitor: link tıklar → verify → activate → yeni expo'ya kayıt
Resend: POST /api/reactivation/resend-pending → pending olanlara farklı template ile tekrar gönder
```

### I. Exhibitor Lead Scanner
```
Exhibitor: leena.app/lead-scan.html açar
  → Kendi badge QR'ını okutarak giriş (visitor_type=exhibitor kontrolü)
  → Visitor QR'larını okutarak lead kaydeder
  → Firma bazlı: aynı company'deki tüm exhibitor'ların leadleri paylaşılır
  → CSV export + vCard kaydetme
  → QR URL formatı parse edilir (kamera URL döndürürse qr parametresi çıkarılır)
```

### K. Public Form → Visitor Kayıt (Upsert eklendi 24 Şubat 2026)
```
form-public.html → POST /api/visitors/public
  → Backend form_id üzerinden forms tablosundan visitor_type çekiyor (authoritative source)
  → visitor_type ve form_id INSERT'e dahil ediliyor
  → Frontend'den gelen visitor_type'a GÜVENİLMEZ
  → UPSERT: email+expo_id ile mevcut visitor kontrolü (lower(email) + expo_id)
    → Varsa: COALESCE UPDATE (boş alanlar korunur, QR korunur) + email resend "(Resent)"
    → Yoksa: INSERT yeni QR + email gönder
  → Exhibitor formu ile gelen kişi artık visitor_type='exhibitor' olarak kaydediliyor
  → Email template placeholders: custom_fields (e.g. conference_topic) spread into emailData
    → {{conference_topic}}, {{any_custom_field}} etc. work in email templates
```

### J. Email Gönderim Mimarisi

**Queue Kullanan (Doğru):**
- Reactivation campaign emailleri → email_queue → email_worker (Direct HTML modu)

**Queue Bypass Eden (Riskli — Senkron SendGrid):**
- `webhook.js:232` — Zoho form submit → direkt sgMail.send()
- `visitors.js:214` — Public form submit → direkt sgMail.send()
- `visitors.js:505` — Excel import (satır başı) → direkt sgMail.send()
- `emailSend.js:76,178` — Single + bulk send → direkt sgMail.send()
- `emailSegments.js:159` — Segment send (300ms delay) → direkt sgMail.send()

**Etkisi:**
- Büyük import'larda (500+ satır) timeout riski
- SendGrid rate limit'e takılınca email sessizce kaybolur
- Fuar sırasında yaşanan "email gitmiyor" sorununun muhtemel kaynağı

### L. Expo-Based Resource Grouping (23 Şubat 2026)

Email templates, forms, and terminals now support expo-based grouping with cross-expo clone:

| Resource | expo_id Column | Clone Endpoint | Frontend Grouping |
|----------|---------------|----------------|-------------------|
| Email Templates | `email_templates.expo_id` (ALTER ile eklendi) | `POST /api/email-templates/clone/:id` | email-templates.html: current expo cards + other compact list |
| Forms | `forms.expo_id` (zaten vardı) | `POST /api/forms/clone/:id` | form-list.html: current expo cards + other compact list |
| Terminals | `terminals.expo_id` (zaten vardı) | `POST /api/terminals/clone/:id` | terminals.html: current expo table + other compact list |

- Clone always creates with `is_active: false` (safety — admin must manually activate)
- Terminals clone generates a new `terminal_key` (UUID v4)
- Frontend pattern: current expo resources shown as full cards/table, other expo resources as compact single-row list with clone + edit buttons
- Statistics (form-list.html) calculated from current expo forms only

### M. Conference Certificate System (1 Mart 2026, refined 1-3 Mart 2026)

```
Hostess opens conference-scanner.html?terminal_key=X
  → Selects conference topic from dropdown
  → Scans visitor QR code
  → POST /api/conference-certificates/checkin-and-certify
    → Validates registration via isVisitorRegisteredForTopic()
    → If NOT registered and NOT force → returns warning (no action)
    → If force → adds topic to visitor via addTopicToVisitor()
    → Creates checkin record (source='conference-cert')
    → Creates conference_certificates record (UNIQUE per visitor+expo+topic)
    → Queues certificate email via email_queue Mode 1 (pre-processed HTML)
  → Duplicate scan → persistent overlay with "Resend Certificate" button
    → POST /api/conference-certificates/resend (uses existing token, no new cert)
  → Visitor receives email with link to certificate.html?token=X
  → Visitor views/prints certificate (Save as PDF via browser)
```

- Terminal auth (x-terminal-key) — no JWT needed for hostess
- Duplicate prevention: ON CONFLICT (visitor_id, expo_id, conference_topic) DO NOTHING
- Certificate token: crypto.randomBytes(32) hex — used for public URL
- Check-ins appear in existing reports (standard checkins table)

#### conference_topic Separator & Multi-Topic Logic

**Separator: `" || "` (double pipe with spaces).** Commas are NOT separators — topic names themselves contain commas (e.g. "Engineering for a Healthy Buildings, Designing for Life").

**`splitTopics(raw)`** — Helper in conferenceCertificates.js. Splits ONLY by `" || "`. Returns array of trimmed topic strings. Used by isVisitorRegisteredForTopic(), /topics endpoint, addTopicToVisitor().

**`isVisitorRegisteredForTopic(customFields, selectedTopic)`** — Case-insensitive check. Splits both visitor's topics and selected topic by `" || "`, returns true if ANY match found.

**`addTopicToVisitor(client, visitorId, customFields, newTopic)`** — Appends topic with `" || "` separator. Duplicate-safe (case-insensitive check before append). Uses `jsonb_build_object` to update custom_fields.

**Multi-topic append on re-registration:**
- Webhook (webhook.js): reads existing `conference_topic` from DB, appends new with `" || "` if not duplicate
- Public form (visitors.js /public): same merge logic
- Import (visitors.js /import): uses `COALESCE || jsonb` merge (preserves existing custom_fields)
- All three: if topic already exists → keeps existing value unchanged

**Topic unnesting in endpoints:**
- `GET /api/visitors/conference-topics` — splits `" || "` to count individual topics
- `GET /api/conference-certificates/topics` — same unnesting with certificate counts
- `GET /api/visitors/paginated` — `ILIKE %topic%` filter (supports multi-topic values)
- `GET /api/visitors/export` — same ILIKE filter

**Example flow:**
```
1. Visitor registers for "Session A" → DB: "Session A"
2. Same visitor registers for "Session B" → DB: "Session A || Session B"
3. Same visitor registers for "Session A" again → DB unchanged (duplicate prevention)
4. Scanner checks "Session A" → isRegistered = true ✅
```

---

## API Endpoint Özeti

→ Taşındı: [LEENA_REFERENCE.md](./LEENA_REFERENCE.md)

---

## Frontend State Yönetimi

| Key | Set Eden | Kullanan | Risk |
|-----|----------|----------|------|
| token | login.html | Tüm admin sayfalar | Yoksa → login.html |
| selectedExpoId | dashboard_new.html (expo select) | main-panel-v2 + tüm admin sayfalar | Yoksa → dashboard_new.html |
| selectedExpoName | dashboard_new.html (expo select) | All 14 admin sidebar expo indicators | Display only |
| organizerId | login.html | Zoho webhook URL generation | Yoksa webhook URL bozulur |
| organizer | login.html | Profil display | JSON object |
| terminalKey | URL param | QR Scanner | Yoksa terminal auth fail |
| leadScannerAuth | lead-scan.html | lead-scan.html | Exhibitor session |

---

## Bilinen Buglar ve Güvenlik Sorunları

### ✅ FIXED (23 Feb 2026)

- **Public form visitor_type and form_id missing** — `visitors.js` POST /public
  - visitor_type and form_id were missing from INSERT query, all public form records had NULL
  - Fix: visitor_type fetched from forms table via form_id (authoritative source), both columns added to INSERT

- **Send Email QR not showing** — `emailSend.js` single + bulk send
  - emailSend.js never looked up existing visitor's qr_code from DB when save_to_database=false or generate_qr=false
  - Fix: added DB lookup for existing visitor QR when qrCode is null (both single and bulk routes)

- **BASE_BADGE_URL fallback** — `emailSend.js:40,153`
  - Fallback was `http://localhost:3000`, now `https://leena.app`. Uses `baseUrl` const consistently.

- **Check-in report CSV missing columns** — `checkins.js` GET /api/checkins + `checkin-reports.html`
  - visitor_type was missing from backend SELECT (Type pie chart defaulted all to 'visitor')
  - CSV export had 10 columns, now 12 (added Visitor Type + Job Title)
  - Fix: added `COALESCE(v.visitor_type, 'visitor') as visitor_type` to backend query

- **Sidebar inconsistency** — All 15 admin pages
  - 9 pages had wrong Forms link (form-builder.html → form-list.html), 13 missing Send Emails, 8 missing Re-activation, 5 missing Check-in Reports
  - Fix: all 15 admin pages standardized with unified 13-link sidebar

### ✅ FIXED (24 Feb 2026 — Sprint 1 Security Hotfix)

- ~~**Import organizer_id bug**~~ — `visitors.js:333` → Changed `req.user?.id || req.user?.organizer_id || 1` to `req.organizer_id || 1` (authMiddleware sets req.organizer_id)
- ~~**Manual registration auth missing**~~ — `visitors.js:244` → Added `authMiddleware` to `router.post('/manual')`. Frontend already sends Bearer token.
- ~~**localStorage key mismatch**~~ — `qrscanner.html:437` → Changed `localStorage.getItem('organizer_id')` to `localStorage.getItem('organizerId')` to match login.html
- ~~**Hardcoded webhook secret**~~ — `webhook.js:8` → Changed to `process.env.ZOHO_WEBHOOK_TOKEN || 'fallback'`. Env var must be set on Render.
- ~~**Badge endpoint PII leak**~~ — `visitors.js:99` → Replaced `SELECT *` with explicit columns (id, name, last_name, company, country, job_title, visitor_type, badge_id, qr_code, booth_number, badge_url, expo_id). Email and phone no longer exposed.

### ✅ FIXED (24 Feb 2026 — Sprint 3)

- ~~**Public form duplicate registration**~~ — `visitors.js` POST /public had no duplicate check. Same email+expo could create multiple records with different QR codes, invalidating the original. Fix: added upsert pattern (SELECT by lower(email)+expo_id → existing: COALESCE UPDATE + QR preserved + email resent with "(Resent)" suffix; new: INSERT as before).

### ✅ FIXED (1 Mar 2026 — Conference Certificate Fixes)

- ~~**Double client.release() in conferenceCertificates.js**~~ — Early `client.release()` calls before return statements + `finally { client.release() }` caused ERR_HTTP_HEADERS_SENT and "Release called on client already released" on production. Fix: removed all early `client.release()` calls, only `finally` block handles release.
- ~~**Conference topic registration check always failing**~~ — `splitTopics()` was splitting by comma, but topic names contain commas (e.g. "Engineering for a Healthy Buildings, Designing for Life"). Created phantom topics like "Designing for Life". Fix: `splitTopics()` now ONLY splits by `" || "` (double pipe). Comma is never a separator.
- ~~**Conference topic overwritten on re-registration**~~ — Webhook and public form upsert replaced entire `conference_topic` value. Visitor registering for Session B lost Session A. Fix: append logic with `" || "` separator + duplicate prevention in webhook.js, visitors.js /public, and conferenceCertificates.js addTopicToVisitor().

### KRİTİK
(All Sprint 1 items fixed — see above)

### YÜKSEK

6. ~~**email_worker FOR UPDATE transaction'sız**~~ ✅ FIXED 24 Feb — `fetchNextTask()` now uses `pool.connect()` + `BEGIN`/`COMMIT`/`ROLLBACK` transaction. Atomically updates `status = 'processing'` via `UPDATE ... WHERE id = (SELECT ... FOR UPDATE SKIP LOCKED)`. Prevents duplicate email on concurrent workers.

7. ~~**BASE_BADGE_URL fallback yok**~~ ✅ FIXED 23-24 Feb — `emailSend.js` + `emailSegments.js` now use `process.env.BASE_BADGE_URL || 'https://leena.app'` (emailSegments had `http://localhost:3000` fallback, fixed 24 Feb)

8. **Race condition** — `leads.js:99-128`, ~~`visitors.js:248,389`~~ (visitors.js public route fixed 24 Feb, manual+import already had upsert)
   - Check-then-insert pattern, ON CONFLICT kullanılmıyor, eşzamanlı request'te duplicate oluşabilir

### ORTA

9. Hata yanıt formatı tutarsız (5 farklı format: `{error}`, `{success,message}`, `{success,error}`, `{success,error,code}`, `{error,details}`)
10. ~~Sidebar inconsistent~~ ✅ FIXED 23 Feb — All 15 admin pages standardized with unified 13-link sidebar
11. Frontend auth kontrol boşlukları: form-builder, checkin-import, expo-create'te auth check eksik/hatalı
12. ~~Login redirect tutarsız~~ ✅ FIXED 24 Feb — All admin pages redirect to login.html (no token) and dashboard_new.html (no expo). Login → dashboard_new.html → main-panel-v2.html flow restored.
13. ~~Template placeholder uyumsuz~~ ✅ FIXED 24 Feb — `{{date}}` and `{{expo_name}}` added to all 13 email flows (visitors.js import/public, webhook.js, email_worker.js mode2/3, reactivation.js 4 flows)
14. Leads endpoint'te server-side session yok — exhibitor_company bilen herkes lead yazabilir/okuyabilir

---

## Bilinen Sorunlar ve Kısıtlar

1. **CORS:** `https://leena.app` ve `https://www.leena.app` ile sınırlı
2. **initial.sql senkron değil:** Production DB'de olan bazı tablolar initial.sql'de yok
3. **Sidebar links:** ✅ All 15 admin pages standardized (23 Feb 2026). CSS `::before` accent bar also added to all pages.
4. **leena.css merkezi stil dosyası:** CLAUDE.md'de referans verilmiş ama **aslında her sayfa kendi inline CSS'ini taşıyor.** Ortak stil dosyası kullanımı henüz tam uygulanmadı. Yeni sayfa yaparken mevcut sayfaların CSS pattern'ini takip et.
5. **QR kod içeriği:** Badge QR'ların içinde sadece UUID var (URL değil). Telefonla okutunca düz text görünür. lead-scan.html'de kamera scanner ile okunan QR'lar URL formatında gelebilir — parse logic mevcut.
6. **CSS class naming:** Bootstrap CSS loaded on admin pages. Avoid generic class names (.toast, .modal, .alert) — use prefix (.app-toast, .leena-modal) to prevent Bootstrap override conflicts.
7. **PostgreSQL bigint serialization:** `COUNT(*)` returns bigint, pg driver serializes as string. Use `::int` cast in backend or `parseInt()` in frontend for numeric operations.

### Frontend Nesil Haritası
Sayfalar 5 farklı CSS neslinde yazılmış. Yeni geliştirmelerde Gen 3/4 pattern kullanılmalı.

| Nesil | Primary | Sidebar | Sidebar Width | Sayfalar |
|-------|---------|---------|---------------|----------|
| Gen 0 | #e53935 | Yok | - | ~~login.html~~ (replaced with Gen 4) |
| Gen 1 | #0066ff | leena.css (harici) | 240px | dashboard.html, checkin-import.html |
| Gen 2 | #4a6fa5 | Inline CSS + ::before | 256px | terminals, checkins, form-list, email-templates, email-segments, email-send, import, visitorlog-paginated |
| Gen 3 | #4a6fa5 | Inline CSS + ::before | 256px | reports, reactivation-campaign, badge-templates, checkin-reports, form-builder, conference-sessions |
| Gen 4 | #4a6fa5 | Inline CSS + ::before + responsive | 260px | login.html, main-panel-v2, dashboard_new |

### Sidebar Status (Updated 20 Apr 2026)
- ✅ All 20 admin pages sidebar links standardized
- Standard order: Overview → Management → Communication → Settings → Tools
- 16 links: Dashboard, Visitors, Forms, Check-ins, Terminals, **Conferences**, **Floor Plan**, Email Templates, Send Emails, Email Segments, Badge Templates, Re-activation, Check-in Reports, Reports, Import
- ✅ CSS `::before` accent bar added to all 15 pages (Gen 2 pages updated 23 Feb 2026)
- ✅ Active expo indicator added to all 14 admin sidebars (24 Feb 2026) — reads `selectedExpoName` from localStorage, hidden if no expo selected
- ✅ Expo indicator is now a clickable `<a>` link to `dashboard_new.html` (25 Feb 2026) — allows switching expo from any page. Small `⇄` icon on the right as visual hint.
- Mobile sidebar only works on main-panel-v2, other pages sidebar disappears below 768px

### Navigasyon Akışı (Updated 24 Feb 2026)

**Ana akış:**
```
login.html → dashboard_new.html (expo seç) → main-panel-v2.html (expo dashboard)
```

**Sayfa rolleri:**
- `login.html` — Login + Register (Gen 4 modern UI). Token varsa → dashboard_new.html'e auto-redirect
- `dashboard_new.html` — Expo seçim sayfası. selectedExpoId'yi temizler, expo listesi gösterir, seçince main-panel-v2'ye gider
- `main-panel-v2.html` — Ana expo dashboard. selectedExpoId zorunlu, yoksa → dashboard_new.html
- `login_new.html` — Sadece login.html'e redirect (eski bookmark uyumu)

**Redirect kuralları:**
- Token yoksa → `login.html` (tüm admin sayfalar)
- Expo seçili değilse → `dashboard_new.html` (tüm admin sayfalar)
- Logout → `login.html` (localStorage.clear)

**Diğer sayfalar:**
- Forms listesi: form-list.html (form-builder.html DEĞİL)
- Public sayfalar (auth yok): lead-scan.html, reactivate.html, form-public.html, badge.html

---

## Geliştirme Kuralları

### Kod Yazarken
1. Her değişiklikten önce ilgili dosyayı `cat` ile oku — asla tahmin etme
2. Route eklerken `index.js`'e mount etmeyi unutma (try/catch pattern'i ile)
3. Email gönderimi her zaman `email_queue` üzerinden (direkt SendGrid çağrısı yapma)
4. QR kod her zaman `<img>` tag'i olarak email'lerde gönderilmeli, UUID string olarak DEĞİL
5. Import/manual registration'da upsert mantığı kullan (email+expo_id ile kontrol, QR koru)

### Frontend Yazarken
1. Tüm frontend dosyaları `public/` altında
2. `localStorage.getItem('token')` ve `localStorage.getItem('selectedExpoId')` kontrolü yapılmalı
3. Bazı sayfalarda `const token = localStorage.getItem('token')` var, bazılarında inline kullanılıyor — dosyayı kontrol et
4. API base URL: bazı sayfalarda `'/api'`, bazılarında `API_BASE_URL` — dosyaya göre değişir
5. Badge print: `window.open(url, '_blank', 'width=600,height=400')` — popup, redirect değil
6. Font: Inter (Google Fonts), İkonlar: Bootstrap Icons (bi-*)
7. Renkler: Her sayfada CSS variables tanımlı (--primary, --sidebar-bg, vb.)

### Language Rule
- Leena EMS is a global SaaS platform. **Only English** must be used in UI text, log messages, error messages, placeholders, and all user-facing strings.
- Turkish or any other non-English text must never be written in the codebase.
- If existing Turkish text is found in the code, it must be translated to English.
- Code comments and commit messages should also be in English.

### Test Ederken
1. Email testlerinde `email+tag@gmail.com` formatını kullan
2. Terminal endpoint'leri camelCase response döner (qrCode, lastName vs)
3. Paginated endpoint snake_case response döner (qr_code, last_name vs)
4. QR kodun resim olarak göründüğünü kontrol et

### Skills Maintenance Rule

Leena uses 3 custom Claude Skills in `.claude/skills/`:
- `leena-backend` — Route patterns, auth, DB queries, email queue
- `leena-frontend` — Admin page template, sidebar, CSS, API call patterns
- `leena-db-schema` — All tables, FK map, naming conventions, known gaps

**When to update skills:**
- New route added or modified → update `leena-backend` route mount table in `references/route-patterns.md`
- New admin page added → update `leena-frontend` sidebar in `references/sidebar.md`
- New sidebar link added → update sidebar in `references/sidebar.md` AND `templates/admin-page-template.html`
- Schema changed (new table, column, index) → update `leena-db-schema/SKILL.md`
- New environment variable added → update env vars table in `leena-db-schema/SKILL.md`
- Always update "Last verified: vXXX" label in all affected skill files when deploying a new version

**Skills are NOT application code:**
- Files in `.claude/skills/` are documentation/pattern files for Claude, not runtime code
- They do not affect the running application
- They must reflect the CURRENT state of production code
- If a skill contradicts actual code, the actual code is the source of truth — fix the skill

---

## Deploy

- **Platform:** Render.com
- **Web Service:** `node index.js` (auto-deploy on git push)
- **Background Worker:** `node email_worker.js` (Root: `backend/leena-v401-backend`)
- Deploy ~10-20 saniye restart süresi

---

## index.js Route Mount Sırası

```javascript
// Route loading (try/catch pattern) — index.js satır 87-105
1.  authRoutes            → app.use('/api/auth', authRoutes)
2.  organizerRoutes       → app.use('/api/organizers', organizerRoutes)
3.  expoRoutes            → app.use('/api/expos', expoRoutes)
4.  visitorRoutes         → app.use('/api/visitors', visitorRoutes)
5.  formRoutes            → app.use('/api/forms', formRoutes)
6.  checkinRoutes         → app.use('/api/checkins', checkinRoutes)
7.  emailTemplateRoutes   → app.use('/api/email-templates', emailTemplateRoutes)
8.  emailSendRoutes       → app.use('/api/email-send', emailSendRoutes)
9.  reportRoutes          → app.use('/api/reports', reportRoutes)
10. webhookRoutes         → app.use('/api/webhook', webhookRoutes)
11. terminalRoutes        → app.use('/api/terminals', terminalRoutes)
12. importCheckinsRoutes  → app.use('/api/import-checkins', importCheckinsRoutes)
13. checkinReportRoutes   → app.use('/api/checkins/reports', checkinReportRoutes)
14. terminalCheckinRoutes → app.use('/api/terminal', terminalCheckinRoutes)
15. emailSegmentRoutes    → app.use('/api/email-segments', emailSegmentRoutes)
16. emailInboundRoutes    → app.use('/api/email', emailInboundRoutes)
17. leadRoutes            → app.use('/api/leads', leadRoutes)
18. reactivationRoutes    → app.use('/api/reactivation', reactivationRoutes)
19. badgeTemplateRoutes   → app.use('/api/badge-templates', badgeTemplateRoutes)
20. conferenceCertRoutes  → app.use('/api/conference-certificates', conferenceCertRoutes)
21. floorplanRoutes       → app.use('/api/floorplan', floorplanRoutes)

// Inline route'lar (index.js satır 107-142):
// GET /api/templates       — form-builder dropdown (authMiddleware)
// GET /api/qr-image/:qrcode — dinamik QR PNG
// GET /health              — health check
```

---

## Versiyon Geçmişi

→ Taşındı: [VERSION_HISTORY.md](./VERSION_HISTORY.md)
