> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# ELL — GERÇEK DURUM ANALİZİ

> **Yöntem:** Sadece kod, git geçmişi ve DB şeması incelendi. Mevcut dokümantasyona
> (README, CLAUDE.md, `*_STATE.md`, `docs/`) GÜVENİLMEDİ — yalnızca doğrulama için
> referans alındı. Hiçbir dosya değiştirilmedi; tamamen read-only analiz.
> **Tarih:** 2026-06-01
> **Bulunamayan şeyler açıkça "bulamadım" olarak işaretlendi. Spekülasyon yok.**

---

## TL;DR — Yönetici Özeti

| | **LEENA** | **LIFFY** | **ELIZA** |
|---|---|---|---|
| **Ne işe yarar** | Etkinlik/fuar ziyaretçi & badge yönetimi (EMS) | Outbound e-posta + CRM + veri madenciliği | Zoho satış verisi üzerinde finans/risk zekası |
| **Canlı klasör** | `Leena_v401_monorepo` | `liffyv1` (API) + `liffy-ui` (UI) | `~/Projects/eliza` (tek kopya) |
| **Dil / Framework** | Node + Express 5, statik HTML | Node+Express 4 / Next.js 16 | Node+Express 4 / Next.js 16 |
| **DB** | PostgreSQL (kendi) | PostgreSQL (kendi) | PostgreSQL (kendi) |
| **Tenant kolonu** | `organizer_id` ✅ var | `organizer_id` ✅ var | YOK (tek-tenant) |
| **Pratikte** | Tek-tenant (Elan Expo varsayımı) | Tek-tenant (Elan Expo hardcoded) | Tek-tenant |
| **Auth** | Kendi yazılmış (JWT+bcrypt) | Kendi yazılmış (JWT+bcrypt) | Kendi yazılmış (JWT+bcrypt) |
| **Sistemler arası bağlantı** | YOK | YOK (sadece Zoho) | YOK (sadece Zoho) |
| **Zoho bağlantısı** | Sadece gelen webhook | ✅ Aktif (push, OAuth) | ✅ Aktif (sync, OAuth) |

**En kritik bulgu:** Üç sistem **birbirine teknik olarak HİÇ bağlı değil**. Hiçbiri
diğerinin DB'sine veya API'sine bağlanmıyor. Ortak auth/SSO yok — üçü de ayrı login,
ayrı JWT secret. Aralarındaki tek ortak nokta **Zoho CRM** (LIFFY push eder, ELIZA
çeker) ve hardcoded **"Elan Expo"** tek-tenant varsayımı. Dokümanlarda anlatılan
"ELL paylaşımlı DB / sistemler arası entegrasyon" kodda **gerçekleşmemiş** — sadece
TODO ve roadmap olarak duruyor.

---

## 0. HANGİ KLASÖR CANLI?

### LEENA → `~/Desktop/Leena_Projesi/Leena_v401_monorepo`
Uygulama kökü: `backend/leena-v401-backend/`

| Klasör | Son commit | Remote | Durum |
|---|---|---|---|
| **Leena_v401_monorepo** | **2026-05-22** `16adf0c` | `Nsueray/Leena_v401_monorepo.git` | **CANLI** |
| Leena_v401_monorepo copy | 2025-08-28 `2ecccff` | aynı remote | 9 ay eski yedek |
| Leena_v401_online | `.git` yok | — | Atıl kopya |
| leena4-kenya-deploy-full-final | 2025-06-17 `a5be00c` | `Nsueray/leena4-kenya-final-live.git` (FARKLI repo) | Ayrı/eski Kenya deploy |

**Nasıl anlaşıldı:** En güncel commit (9 ay farkla), tek aktif çalışma alanı (Mayıs 2026
tarihli dosyalar, `009_` migration'a kadar), git remote'u CLAUDE.md'de "Leena_v401" Render
servisi olarak adı geçen repoyla eşleşiyor.
**UYARI:** Repoda `render.yaml` / Dockerfile **yok** — "Leena_v401" servis adı dosyada
kanıtlanamıyor (Render dashboard'da). Bu kısım: **bulamadım** (dosyada yok). Ancak diğer
kanıtlar canlı klasörü kesin gösteriyor. `.env`'de Render Oregon Postgres host'u
(`dpg-...oregon-postgres.render.com`, db `leena_v401_db`) Render barındırmayı doğruluyor.

### LIFFY → `liffyv1` (backend) + `liffy-ui` (frontend)
Üç klasör = aynı sistemin **üç ayrı bileşeni**, kopya değil:

- **`~/Projects/liffyv1`** — CANLI BACKEND. `package.json` name=`liffy-backend` "Liffy Mining API",
  ~35 router `/api/*`, son commit **2026-05-14** (en yenisi). `Dockerfile` mining worker.
- **`~/Projects/liffy-ui`** — CANLI FRONTEND. Next.js 16, `API_BASE = ... || "https://api.liffy.app"`
  (`app/page.tsx:99` vb.). Son commit 2026-05-12.
- **`~/Projects/liffy-local-miner`** — DEPLOY DEĞİL. Lokal scraper CLI (`mine.js`), server yok,
  canlı API'ye client olarak veri basıyor. Son commit 2026-04-04.

**Deploy manifesti:** `liffy-ui`'de render.yaml/vercel.json yok; prod host `api.liffy.app`
koddan doğrulandı ama deploy platformu dosyada → **bulamadım**.

### ELIZA → `~/Projects/eliza` (tek kopya, başka kopya yok)
Son commit **2026-05-01** `6a7efdd`, branch `main`, 171 commit (ilk: 2026-03-09).
Çalışma ağacı kirli (`021_core_countries.sql` değişik, `ELIZA_CURRENT_STATE.md` untracked).
npm workspaces: `apps/{api,dashboard,whatsapp-bot}` + `packages/{ai,alerts,attention,briefing,db,messages,push,targets,zoho-sync}`.
**Deploy config:** render.yaml/Dockerfile/vercel.json **yok** — CLAUDE.md'nin bahsettiği
`infra/` klasörü **mevcut değil** → **bulamadım** (Render dashboard'da olmalı).

---

## 1. VERİTABANI ŞEMASI (sadece canlı versiyonlar)

### LEENA — PostgreSQL (`initial.sql` + `migrations/001–009` + prod-only tablolar)

> **Önemli:** `initial.sql` prod ile senkron DEĞİL (dosyada belirtilmiş). Bazı canlı
> tablolar hiçbir migration'da yok, Render Shell'de elle yaratılmış; kolonları
> `leena-db-schema/SKILL.md`'den alındı (o da koddan en az bir yerde sapıyor).

**Çekirdek tablolar (`initial.sql`):**
- **organizers** — hesap sahibi / auth principal (= tenant). `id, name, email, password_hash, logo_url`
- **expos** — etkinlik tanımı. `organizer_id FK, name, slug, location, dates`
- **visitors** — TÜM kişiler (ziyaretçi/exhibitor/vip/press/speaker → `visitor_type`). `organizer_id, expo_id, name, email, badge_id, company, qr_code, custom_fields JSONB`
- **forms** — kayıt formu config (JSONB)
- **checkins** — giriş kayıtları. `visitor_id, expo_id, checkin_time, hall`
- **email_templates / email_queue / email_logs** — e-posta tasarım, kuyruk, log

**Floor plan (`migrations/001`):**
- **expo_halls** — fiziksel salon/grid. **expo_floorplan_versions** — taslak/aktif plan versiyonları.
  **expo_stands** — satılabilir stand (içinde *nullable* `company_id`, `contract_id` = LiFFY FK stub'ları, hiç bağlanmamış).
  **expo_stand_cells** — grid hücresi. **expo_stand_assignments** — atama geçmişi (Phase-2 stub).

**Diğer:**
- **expo_exhibitors** (`003`) — fuar başına exhibitor kaydı
- **email_campaigns / campaign_steps / campaign_recipients / email_events / email_unsubscribes** (`004`) — drip e-posta motoru
- **import_jobs** (`005`) — async toplu import takibi
- **Prod-only (migration'sız, elle yaratılmış):** visitor_event_status, terminals, badge_templates, reactivation_tokens, exhibitor_leads, import_logs, conference_certificates

**Aradığınız tablolar:**
- users → **organizers** (auth principal); organizations/tenants → **organizers**
- contracts/revenue/finance → **YOK** (sadece kullanılmayan `expo_stands.contract_id` + `price_per_m2`)
- visitors ✅; badges → `badge_templates` + `visitors.badge_id/qr_code`
- leads → `exhibitor_leads`; companies → **YOK** (sadece nullable `company_id` int → harici LiFFY)

### LIFFY — PostgreSQL (`liffyv1/backend/migrations/` — 47 migration)

- **organizers** (`004`) — tenant/hesap (örn. Elan Expo); Zoho & SendGrid kimlikleri burada
- **users** (`004`) — organizer'a bağlı login kullanıcıları; rol, hiyerarşi (`manager_id`, `reports_to`), `permissions` JSONB
- **sender_identities** — gönderen "From" adresleri
- **email_templates / campaigns / campaign_recipients / campaign_events** — e-posta kampanya & SendGrid event
- **campaign_sequences / sequence_recipients** (`035`) — çoklu-dokunuş drip
- **prospects** (`006`) — ham madenlenen/import kontaklar
- **persons** (`015`) — tekilleştirilmiş kanonik kişi varlığı
- **affiliations** (`016`) — kişi↔şirket istihdam bağı
- **prospect_intents** (`017`) — niyet/etkileşim sinyalleri
- **lists / list_members** — kontak listeleri
- **mining_jobs** (`007`) + mining logs/results — scraping/import işleri
- **generated_miners** (`024`) — AI üretimi scraper kodu (Claude)
- **contact_notes / contact_activities / contact_tasks** (`030`) — CRM not/aktivite/görev
- **pipeline_stages** (`031`) — satış pipeline kolonları
- **action_items** (`037`) — otomatik takip görevleri (P1–P4)
- **discovery_searches** (`043`) — kayıtlı kaynak-keşif aramaları
- **companies** (`046`) — şirket master (dedup, sector, `zoho_account_id`)
- **unsubscribes** (`012`) — opt-out

**Aradığınız tablolar:**
- users ✅, organizations/tenants ✅ (`organizers`), companies ✅
- leads → **tablo YOK** (`leads.js` router `persons`/`affiliations` üzerinde çalışır; "Leads" = Zoho push hedefi)
- contracts/revenue/finance/invoices → **bulamadım** (sadece `can_view_revenue` izin *bayrağı*)
- visitors/badges → **bulamadım** (yok; LIFFY etkinlik sistemi değil, e-posta/CRM aracı)

### ELIZA — PostgreSQL (`packages/db/schema.sql` + migration `004–024`)

> ELIZA'nın **kendi** Postgres'i var (`packages/db/index.js:3-7`).

- **expos** (`schema.sql:5`) — fuar marka/edisyonları (country, edition_year, target_m2, cluster)
- **contracts** (`schema.sql:18`) — **Zoho'dan senkronlanan satış sözleşmeleri** (af_number unique, expo_id, company, revenue, m2); `013` finans alanları ekler (balance_eur, paid_eur, due_date, currency, revenue_eur)
- **contract_payments** (`013`) — Zoho subform'dan gelen tek tek ödemeler
- **contract_payment_schedule** (`013`) — **SENTETİK** ödeme planı (30% depozito + 70% etkinlik öncesi; ELIZA üretir, Zoho'dan değil)
- **exhibitors** (`schema.sql:33`) — büyük ölçüde atıl (sync company_name'i contracts'a yazar)
- **expenses** — fuar başına maliyetler
- **sales_agents** — satıcılar/acenteler
- **alerts** — CEO için risk/olay bildirimleri
- **whatsapp_messages / message_drafts / message_logs** — bot mesajları, onay bekleyen taslaklar, AI sorgu logu
- **sync_log** (`004`) — Zoho sync çalışma takibi
- **users / user_permissions** (`005`) — kullanıcılar + veri kapsamı/WhatsApp izinleri
- **push_log** (`017`) — push dedup (+ twilio_sid)
- **expo_clusters / expo_targets** (`019`) — otomatik gruplama + m²/gelir hedefleri
- **core_countries / core_sectors / core_currencies / core_languages** (`021–024`) — "ELL paylaşımlı" ISO referans tabloları (ama bu repoda başka sistem okumuyor)
- **View'lar:** `outstanding_balances` (finans tahsilat), + `edition_contracts`/`fiscal_contracts`/`expo_metrics` (CREATE'leri migration'da yok → **bulamadım**, başka yerde tanımlı)

**Aradığınız tablolar:** users ✅, contracts ✅, revenue/finance ✅ (contracts+payments+view'lar).
visitors/badges/leads/organizations → **YOK / bulamadım** (CLAUDE.md Zoho modülü olarak listeler ama ELIZA senkronlamaz).

---

## 2. MULTI-TENANCY GERÇEĞİ

### LEENA — `organizer_id` ŞEMADA GERÇEKTEN VAR ✅, ama pratikte tek-tenant
- FK olarak her tabloda: `visitors.organizer_id` (`initial.sql:34`), `expos` (`:19`), forms (`:62`), email_templates (`:88`), expo_halls (`001:24`) vb.
- Auth'ta zorlanıyor: `middleware/authMiddleware.js:18` → `req.organizer_id = decoded.organizer_id`.
- **`tenant_id` / `organization_id` kolonu YOK** — tek eşleşme bir yorum satırı (`middleware/dualAuth.js:15`).

**Tek-tenant varsayımları (dosya:satır):**
- Hardcoded `organizer_id = 1` fallback: `routes/visitors.js:333` (`organizerId || 1`), `routes/visitors.js:552` (`req.organizer_id || 1`), `middleware/dualAuth.js:14`
- Toplu badge-print yolu organizer scope'unu tamamen düşürür, **sadece `expo_id`** ile filtreler — CLAUDE.md'de açıkça "single-organizer simplification (sadece Elan Expo)" gerekçesiyle
- Expo-7'ye özel hardcode: `routes/conferenceCertificates.js:206` `COOL_PLUS_EXPO_ID = 7`

**"Elan Expo" hardcode:** sadece **marka metni/görseli**, tenant ID değil:
`routes/conferenceCertificates.js:66,126` (`alt="Elan Expo"`), `public/certificate.html:423-438`,
`public/form-builder.html:390,959`, `public/reactivate.html:433` ("Powered by Leena EMS · © Elan Expo").

### LIFFY — `organizer_id` ŞEMADA GERÇEKTEN VAR ✅, ama pratikte tek-tenant
- `UUID NOT NULL REFERENCES organizers(id)` neredeyse her tabloda: `migrations/004:23` (`users.organizer_id`), 006, 007, 015–046.
- JWT `organizer_id` taşır, route'lar filtreler: `routes/persons.js:33` (`p.organizer_id = $1`). İsim tutarlı (`tenant_id` yok).

**Tek-tenant (Elan Expo) hardcode (dosya:satır):**
- `scripts/seed_admin.js:23-24` → `ORGANIZER_NAME = 'Elan Expo'`, `ORGANIZER_SLUG = 'elan-expo'`
- Hardcoded kurucu sahip UUID `cfb66f28-54b1-4a82-85d5-616bb6bbd40b` ("Suer") migration'lara gömülü: `032_user_isolation.sql`, `033`, `039` (+ Elif, Bengü UUID'leri)
- `worker.js:674` ve `worker.js:743` → fallback `recipientEmail = 'suer@elan-expo.com'`
- İkinci hardcoded organizer UUID: `scripts/import_zoho_bengu.js:23`

**Verdict (her ikisi):** Şema multi-tenant'a HAZIR, ama deployment tek tenant (Elan Expo) —
sahip user ID, org adı seed script'lerde / migration backfill'lerinde / worker fallback'lerinde hardcoded.

### ELIZA — multi-tenancy YOK (tek-tenant, by design)
`organization_id`/`tenant_id`/`organizer_id` kolonu **yok**. `users`/`user_permissions`
var ama org/tenant ayrımı yok. Tek bir şirket (Elan/Elan Fairs) varsayımıyla çalışıyor.

---

## 3. ELIZA GERÇEKTE NE YAPIYOR?

**Verdict: ELIZA kendi verisini TUTAR + GERÇEK iş mantığı VAR. Salt görüntüleme/cache DEĞİL.**
Bir "sync-ve-analiz" sistemi: Zoho'dan kendi Postgres'ine çeker, sonra kendi
analitik/risk/finans/AI mantığını lokal veri üzerinde çalıştırır.

**Zoho bağlantısı — onaylandı (dosya:satır):**
- OAuth refresh-token: `packages/zoho-sync/zohoAuth.js:7` (`accounts.zoho.com/oauth/v2/token`), `:14-24`
- API fetch: `packages/zoho-sync/syncSalesOrders.js:5` (`zohoapis.com/crm/v2/Sales_Orders`), pagination `:13`, subform `:358`
- Lokal DB'ye yazar: `syncSalesOrders.js:247-284` (`INSERT ... ON CONFLICT (af_number) DO UPDATE`)
- Zoho **read-only kaynak** — kayıtlara POST/PUT/write bulunamadı. ("read-only intelligence layer" iddiası kodda doğru.)
- Ek: `fetchSalesOrders.js`, `syncExpos.js`, `scheduler.js` (cron), `testToken.js`

**Kendi iş mantığı — onaylandı (salt render değil):**
- **Döviz çevrimi:** `syncSalesOrders.js:49-63`, `:121-155` (çift-para regex parse, local→EUR)
- **Sentetik ödeme planı:** `syncSalesOrders.js:173-208` (30% depozito +30g, 70% final etkinlik −30g)
- **Tahsilat staging + çift-eksen risk skoru:** `migrations/014_update_outstanding_view.sql` — `collection_stage`, `collection_risk_score`, `event_risk_score` hesaplayan ciddi SQL
- **Finans API agregasyonu:** `apps/api/src/routes/finance.js:30-90` (collected/outstanding/overdue KPI), `:218-229` (A/R aging 6 kova), `:177-197` (`suggested_action`)
- **Risk/hız motoru:** `packages/ai/riskEngine.js:40-65` (velocity = sold_m2/months, SAFE/OK/WATCH/HIGH)
- **Hedef motoru:** `packages/targets/index.js:45-82` (otomatik hedef = önceki edisyon × (1+%)), cluster tespiti
- **AI sorgu motoru:** `packages/ai/queryEngine.js` (NL→intent→parametreli SQL→Claude yanıtı, SQL whitelist)

→ "Zoho üzerinde ince görüntüleyici" hipotezi **YANLIŞ**.

---

## 4. SİSTEMLER BİRBİRİNE BAĞLI MI?

**HAYIR. Üçü de teknik olarak birbirinden bağımsız.**

| Bağlantı | Durum | Kanıt |
|---|---|---|
| LEENA → LIFFY/ELIZA | **YOK** | LEENA'da hiç outbound HTTP/API yok (`axios/fetch` grep = 0). `liffy`/`eliza` sadece yorumda |
| LIFFY → LEENA/ELIZA | **YOK** | `leena` grep = 0. ELIZA için tek iz: `actionEngine.js:137` `// TODO: Implement when ELIZA shared DB connected` |
| ELIZA → LEENA/LIFFY | **YOK** | leena/liffy URL/IP/API çağrısı = 0; sadece docs/roadmap'te |

- **LiFFY↔LEENA stub'ları:** LEENA'da `expo_stands.company_id`/`contract_id` (`migrations/001:105-106`) ve `expo_exhibitors.company_id` (`003`) "LiFFY FK (nullable, no constraint — ADR-014)" olarak şemada var ama **hiç bağlanmamış**.
- **ELIZA `core_*` tabloları:** "ELL paylaşımlı, LiFFY/LEENA okur" diye dokümante ama bu repolarda **kimse okumuyor**.
- **Ortak nokta = sadece Zoho:** LIFFY Zoho'ya **push** eder (`routes/zoho.js` `POST /api/zoho/push`), ELIZA Zoho'dan **çeker**. Birbirleriyle değil, Zoho ile konuşuyorlar.
- **LEENA & Zoho:** sadece **gelen webhook** (`routes/webhook.js:35` `POST /zoho/:organizer_id/:expo_id/:form_id`); LEENA Zoho'yu çağırmaz.

**Ortak auth/JWT YOK — üçü de AYRI login, AYRI secret:**
- LEENA: `routes/auth.js:48-54` JWT `{organizer_id, email}`, 30 gün, `process.env.JWT_SECRET`
- LIFFY: `routes/auth.js` JWT `{user_id, organizer_id, role, email}`, 7 gün, fallback `"liffy_secret_key_change_me"`
- ELIZA: `apps/api/src/routes/auth.js:230` JWT, fallback `'eliza-dashboard-secret-key-change-in-production'`
- Hiçbir paylaşımlı secret, SSO, federated identity yok. Üç ayrı kullanıcı tablosu, üç ayrı oturum.

---

## 5. TEKNİK TEMEL

| Sistem | Dil / Framework | Auth |
|---|---|---|
| **LEENA** | Node.js + **Express 5.1.0** (CommonJS); frontend statik HTML/JS (`public/`, build yok); `pg`, SendGrid, bcrypt, qrcode | **Kendi yazılmış** — `jsonwebtoken` + `bcrypt` (cost 10). Keycloak/Supabase/Auth0/passport **YOK**. + ayrı terminal-key auth (`terminalAuth.js`, JWT'siz) |
| **LIFFY backend** | Node.js (Docker node:22) + **Express 4** + `pg` + Playwright/Cheerio (mining) + SendGrid | **Kendi yazılmış** — `jsonwebtoken` + `bcrypt`. Library yok. `authRequired` ~10+ route'a kopyala-yapıştır + `middleware/userScope.js` rol bazlı görünürlük |
| **LIFFY frontend** | **Next.js 16 / React 19 / TS**, Tailwind v4, Radix, Recharts | JWT `localStorage` (`liffy_token`), `Bearer` header |
| **ELIZA api** | Node.js (CommonJS JS) + **Express 4** + `pg` + `@anthropic-ai/sdk` + `node-cron` | **Kendi yazılmış** — `jsonwebtoken` + `bcrypt` (SALT=10). NextAuth/Supabase/vb. YOK. Bot ayrı auth (telefon→users lookup) |
| **ELIZA dashboard** | **Next.js 16.1.6 / React 19**, Chart.js, jspdf, xlsx | Bearer / localStorage |
| **ELIZA bot** | Express + Twilio (WhatsApp); DB'ye **doğrudan** sorgu (API'ye HTTP yok) | Telefon bazlı |

**Üçü de:** Node.js, PostgreSQL, hand-rolled JWT+bcrypt auth. Hiçbiri hazır
kimlik sağlayıcı (Keycloak/Supabase/Auth0/passport/NextAuth) kullanmıyor.

---

## EK: Güvenlik & Tutarlılık Notları (kod okumasından, spekülasyon değil)

- **LEENA `.env`** canlı klasörde commit'li: gerçek formatlı SendGrid `SG.` key + JWT secret düz metin. `routes/webhook.js:8` hardcoded Zoho webhook fallback token `'98uy237fbiweuhr8h23g9rg239'`.
- **LIFFY:** `"liffy_secret_key_change_me"` JWT fallback ~10+ dosyada — prod'da `JWT_SECRET` set değilse risk. Migration `038`/`039` "DO NOT RUN AUTOMATICALLY — apply manually" işaretli (ortamlar arası şema farkı olabilir). Çok sayıda `.backup`/`.save` dosyası commit'li.
- **ELIZA:** `auth.js:7` `JWT_SECRET || 'eliza-dashboard-secret-key-change-in-production'` ve `JWT_SECRET` **`.env`'de set DEĞİL** → hardcoded default secret ile çalışıyor.
- **Şema-kod sapmaları:** LEENA `initial.sql` prod ile senkron değil (bazı canlı tablolar elle yaratılmış, migration'sız). ELIZA migration'ları `004`'ten başlıyor (001–003 ve bazı view'ların CREATE'i repoda yok → **bulamadım**). CLAUDE.md'nin bahsettiği ELIZA `infra/` klasörü **mevcut değil**.

## Açıkça BULAMADIĞIM şeyler
- LEENA: repoda `render.yaml` olmadığı için "Leena_v401" Render servis adı dosyadan kanıtlanamadı.
- LIFFY: `liffy-ui` deploy platformu (Vercel/Render) dosyada yok; sadece prod host `api.liffy.app` koddan biliniyor.
- ELIZA: hiç deploy config'i repoda yok; view tanımları (`edition_contracts` vb.) ve migration 001–003 repoda yok.
- Tüm satır sayıları (kayıt adetleri) koddan görülemez — sadece tablo YAPISI çıkarıldı (istendiği gibi).
- Kesin canlı şema yalnızca canlı Render DB'lerine bağlanarak doğrulanabilir; bu read-only dosya analizinin kapsamı dışında.
