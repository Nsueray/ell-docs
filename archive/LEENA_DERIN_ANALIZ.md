> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# LEENA — DERİN ANALİZ (canlı sistem gözüyle)

> **Amaç:** LEENA ŞU AN CANLI KULLANILAN TEK SİSTEM (fuar günleri visitor/badge/check-in,
> leena.app). O yüzden sadece "ne eksik" değil — **ne sağlam, canlıyı bozmadan nasıl üzerine
> inşa edilir, ve diğer ikisindeki güvenlik açığı burada da var mı.**
>
> **Kod:** `~/Desktop/Leena_Projesi/Leena_v401_monorepo` (app: `backend/leena-v401-backend`)
> **Referans:** `~/Downloads/ELAN_EXPO_REQUIREMENTS_v1_0.md` — yalnız 2.4 (Catalogue), 2.5 (Expo Operations), 2.7 (Email)
> **Yöntem:** 3 paralel kod-inceleme ajanı, her iddia `dosya:satır`. Dokümana güvenilmedi. Hiçbir dosya değiştirilmedi. Bulunamayan → "bulamadım".

---

## TL;DR — Alan durumları tek bakışta

| Alan | Durum | Tek cümle |
|---|---|---|
| **A. Güvenlik** | **KISMI** | Auth her endpoint'te var (ELIZA'nın aksine) AMA visitor-data katmanında tenant izolasyonu kırık (LIFFY gibi) + git'e commit'li gerçek JWT/SendGrid secret. |
| **B1. Floor Plan** | **TAM** (KORU) | 18 endpoint, transaction-güvenli, DB-invariant'lı (tek-aktif-versiyon, hücre-tekliği, otomatik m²) + tam Konva.js frontend. |
| **B2. Visitor/Check-in/Badge** | **TAM** (KORU — canlı çekirdek) | Tüm upsert yolları QR'ı korur, terminal check-in duplicate-guard'lı/transactional, email worker FOR UPDATE SKIP LOCKED. |
| **C. Expo Master Record** | **İSKELET** | 10 kolonluk etkinlik stub'ı; edition/sector/venue/buildup/deadline/contacts/partners/cluster hepsi yok. |
| **D. Catalogue Generator** | **YOK** | Sıfır iz — tablo/editör/sayfa yok, PDF kütüphanesi yok, "corel" geçmiyor. |
| **E. Email Altyapısı** | **GENİŞLET** | Queue/worker/3-mode/sequence tabanı sağlam ve üretim-kanıtlı; ama days-before-expo trigger/dil/marketing-flag/sender-mailbox yok. |
| **F. Exhibitor Entegrasyonu** | **İSKELET** | Nullable FK stub'ları var; dış HTTP client yok, ELIZA URL'i yok, company_id/contract_id hiç dolmuyor. |

> **En önemli kıyas:** Güvenlikte LEENA **ELIZA'dan iyi, tenant-izolasyonunda LIFFY ile aynı,
> secret hijyeninde ikisinden de kötü.** Tek-tenant gerçeği (sadece Elan Expo) şu an aktif
> sömürüyü engelleyen TEK şey.

---

## A. GÜVENLİK — KISMI

**Auth modeli — her endpoint'te uygulanmış (ELIZA'nın aksine).** Global middleware yok; her route kendi auth'unu ekliyor. Üç model:
- **JWT** (`authMiddleware.js:13`, `req.organizer_id` set eder): visitors (çoğu), expos, checkins, forms, reports, terminals, email*, badgeTemplates, campaigns (`router.use` :41), floorplan, exhibitors, reactivation (admin).
- **Terminal key** (`terminalAuth.js:32`, `x-terminal-key`): tüm `terminalCheckins.js` (`router.use` :27), conference-cert check-in/resend, badge `/for-terminal/:key`.
- **Dual** (`dualAuth.js`, JWT VEYA bulk_print terminal key): yalnız `visitors.js /paginated` (:54) + `/import` (:530).
- **Bilinçli public** (tasarımca doğru): login/register, webhook (token'lı), emailInbound, emailTracking, leads (3), reactivation `/verify`+`/activate`, badge `/badge/:qr` (:117), form `/public`, expo `/slug`.

**🔴 Multi-tenant izolasyon — visitor katmanında KIRIK (LIFFY-sınıfı):**
- **`buildVisitorFilter` yalnız `expo_id` ile filtreliyor, ASLA `organizer_id`** (`visitors.js:18`). Bu builder `/paginated` (:54), `/export` (:984), `/bulk-email`'i besliyor. expo_id `req.query`'den, sahiplik kontrolü YOK (`visitors.js:56,981`). Başka org'un expo_id'sini veren herhangi bir authenticated organizer o org'un **tüm visitor PII'sını okur/export eder.** LIFFY açığının aynısı.
- **Doğru scope'lananlar (tutarsızlık):** expos list/detail/delete `organizer_id=$2` (`expos.js:60,85,334`), checkins `e.organizer_id=$1` join (`checkins.js:223`), visitor edit `AND organizer_id=$12` (`visitors.js:176`). Yani izolasyon bazı yerde sağlam, en değerli PII-export endpoint'lerinde yok.
- **Cross-tenant yıkıcı yol:** expo force-delete `expos.js:329-331` önce `DELETE FROM checkins/visitors/forms WHERE expo_id=$1` (organizer kontrolü YOK), sonra organizer-scope'lu `DELETE FROM expos` (:334). Başka org'un expo'sunda son delete 0 satır → ROLLBACK kurtarıyor; ama tek koruma rollback (üstelik shared pool'da `pool.query('BEGIN')` — concurrency-unsafe).

**Tek-tenant ne demek:** Bugün sadece Elan Expo hesabı var, sızacak ikinci tenant yok. AMA kayıt açık (`auth.js:75`) — ikinci organizer kaydolduğu an `/paginated`+`/export`+`/bulk-email` **kod değişmeden** tenant'lar arası sızar. İzolasyon kod ile değil, veri-durumu ile sağlanıyor.

**🔴 Secret hijyeni — git'e commit'li gerçek secret (ikisinden de kötü):**
- **`.env.backup` git-tracked, gerçek değerlerle:** `git ls-files` → `backend/leena-v401-backend/.env.backup` (+`-OLD`/`-backup` kopyaları). İçinde `JWT_SECRET=supersecureleena`, `SENDGRID_API_KEY=SG.EZkZl2...`, `SENDER_EMAIL=suer@elan-expo.com`. `.gitignore` yalnız `.env`'i yok sayıyor, `.env.backup`'ı değil. `supersecureleena` prod JWT secret'ı ise repo erişimi olan herkes admin token üretebilir.
- **JWT fallback — iki middleware'e bölünmüş:** `authMiddleware.js:13` (gerçek kullanılan) fallback YOK — JWT_SECRET yoksa throw. `auth.js:16` ELIZA-tarzı `|| 'your-secret-key'` fallback'i VAR **ama hiçbir route import etmiyor** (ölü kod). Yani tehlikeli fallback canlı yolda değil.
- **Zoho webhook hardcoded fallback hâlâ duruyor:** `webhook.js:8` `ZOHO_WEBHOOK_TOKEN || '98uy237fbiweuhr8h23g9rg239'`. Env set değilse bu public string canlı secret → herhangi biri visitor enjekte edip email tetikler.

**Terminal auth — süresiz, tokensız, DB-backed:** `terminalAuth.js:32` raw `x-terminal-key`'i `terminals.terminal_key`'e (plaintext UUID, expiry yok, rotation yok) eşler; `is_active=false` olana dek geçerli. Sızan key o expo için: QR+email ile visitor lookup (tam PII), check-in, badge-print+auto-checkin, sertifika. Key'ler URL'de geçiyor (`?terminal_key=`) → tarayıcı geçmişi/proxy log'larında.

**Public PII yüzeyi:** `leads.js` (3 endpoint, hepsi PUBLIC, server-session yok) — `exhibitor_company`+`expo_id` bilen herkes `/list` ile her lead'in tam PII'sını okur (`leads.js:174-186`), `/scan` ile lead yazar. Gerçek kimliksiz PII oku/yaz yüzeyi.

### VERDICT: LEENA vs LIFFY vs ELIZA
- **ELIZA'dan İYİ:** ELIZA'da hiç auth middleware yoktu + aktif kullanımda hardcoded JWT fallback. LEENA neredeyse her endpoint'e gerçek JWT/terminal auth uyguluyor; tehlikeli fallback yalnız ölü kodda; prod JWT yolu JWT_SECRET istiyor.
- **Tenant izolasyonunda LIFFY ile AYNI:** Birebir aynı "organizer_id yerine sadece expo_id" açığı ana visitor list/export'ta (`buildVisitorFilter`). LEENA expos/checkins/edit'i organizer ile scope'layarak kısmen hafifletiyor ama en değerli endpoint'ler expo_id ile sızıyor.
- **Secret hijyeninde İKİSİNDEN DE KÖTÜ:** Git'e commit'li gerçek JWT + SendGrid key (`.env.backup`) + canlı hardcoded Zoho webhook fallback. **Net: ELIZA'dan iyi, izolasyonda LIFFY ile eşit, secret'ta ikisinden kötü. Tek-tenant gerçeği aktif sömürüyü engelleyen tek şey.**

---

## B1. FLOOR PLAN BUILDER — TAM (KORU)

**18 endpoint** (`routes/floorplan.js`, header yorumu eksik sayıyor — koda güven): Halls (3: `:32,:58,:99`), Versions (5: `:158,:189,:229,:271 activate,:326 clone`), Stands (10: `:420,:487,:636,:715 status,:764 split,:902 merge,:1021 move,:1101 delete`). Hepsi `authMiddleware` (JWT, organizer_id) `:25`.

**Şema (`migrations/001_floorplan_tables.sql`, BEGIN/COMMIT'li):**
- `expo_halls` — `total_area_sqm GENERATED ALWAYS AS (...) STORED` (:29)
- `expo_floorplan_versions` — status draft/active/archived (:53), `UNIQUE(hall_id, version_number)` (:60)
- `expo_stands` — iki-katman status (`area_kind` + `commercial_status`), `UNIQUE(version, stand_code)` (:124)
- `expo_stand_cells` — **çift UNIQUE** (`(stand_id,x,y)` + `(version,x,y)`) = çakışma-yok invariant'ı (:143,:146)
- `expo_stand_assignments` — Phase-2 stub (kullanılmıyor)

**DB-seviye invariant'lar (gerçekten sağlam):** (1) hall başına tek aktif versiyon — partial unique index `idx_one_active_version_per_hall ... WHERE status='active'` (:186) + activate transaction'da öncekini archive eder (:300). (2) versiyon başına hücre tekliği — 409 "cells already occupied" (`:618`, 23505 catch). (3) size_m2 otomatik — trigger `fn_update_stand_size_m2` hücre COUNT'tan hesaplar (:194-211).

**Operasyonlar — hepsi transactional:** create (`:487` pool.connect+BEGIN), split (cell union == orijinal doğrular `:824`), merge (`:902`), clone (deep-copy `:326`), move (cell delete+reinsert, çakışma 409 `:1093`), activate (draft→active, öncekini archive). Draft-only zorlaması tutarlı.

**Frontend:** `public/floorplan-builder.html` (Konva 9.3.15 + pdf.js) + `public/floorplan/{api,state,grid,stands,toolbar}.js` — tam, gerçek.

**KORU sınırı:** `routes/floorplan.js`, `migrations/001` + `003`, `public/floorplan-builder.html` + `public/floorplan/*`, tablolar (expo_halls/versions/stands/cells/assignments/exhibitors), trigger + partial index + çift UNIQUE + GENERATED kolon. Bağımlı: `authMiddleware.js`, `utils/db.js`, `expos`, `routes/exhibitors.js`, Konva/pdf.js CDN, localStorage `token`.

---

## B2. VISITOR / CHECK-IN / BADGE / QR / TERMINAL — TAM (KORU — canlı çekirdek)

**Bu fuarda çalışan kısım. En battle-hardened kod.**

- **Visitor (`routes/visitors.js`):** public reg `/public` (`:197`, upsert `lower(email)+expo_id`, **QR korunur** `ex.qr_code` :259, visitor_type `forms`'tan :232 — client'a güvenmez); manual `/manual` (`:445`, authMiddleware'li, QR korur :489); Excel import `/import` (`:530`, dualAuth, **QR koruma varsayılan** `existing_qr_option='keep'` :545, token modda `expo_id=req.scopedExpoId` :542). PUT `/:id` — qr_code/badge_id UPDATE listesinde YOK (korunur).
- **QR (`utils/qrcode.js`):** değer = `uuidv4()`, `badge_id` = ilk 8 char upper; `/api/qr-image/:qrcode` (index.js:148) UUID'yi PNG'ye render eder.
- **Badge (`routes/badgeTemplates.js`):** CRUD + public `/for-terminal/:key` (:242); visitor_type-bazlı; priority chain terminal→expo→organizer→System Default (:272-309); referans varsa silme engelli (:206). `public/badge.html` + `bulk-badge-print.html` (token-gated).
- **Check-in (`routes/terminalCheckins.js`):** `/checkin` (`:398`, transaction, duplicate-guard `isDuplicateCheckin` threshold 120s :53, **`visitor_event_status` ON CONFLICT(visitor_id,expo_id)** upsert :467); `/badge-print` (:277, opsiyonel auto-checkin); lookup'lar terminal'in expo+organizer'ına scope'lu (:135). Dashboard `routes/checkins.js` + `checkinReports.js`.
- **Email confirmation (`email_worker.js`):** `fetchNextBatch` (:34) `UPDATE ... WHERE id IN (SELECT ... FOR UPDATE SKIP LOCKED)` BEGIN/COMMIT içinde (:40-50) — **concurrency-safe, çift-gönderim önler.** İki-katman priority (transactional önce, campaign sonra), 3 send modu, MAX_RETRIES=5.
- **Komşu özellikler:** reactivation campaigns **TAM** (13 endpoint, async job + email_worker scheduler :270-646), conference certificates **TAM** (6 endpoint, UNIQUE cert, NG/Ghana branch), exhibitor lead-scanner **KISMI** (3 endpoint, hepsi PUBLIC auth'suz — turnstile yolu değil).

**KORU sınırı (canlı fuar akışı):** `routes/{visitors,terminalCheckins,checkins,checkinReports,badgeTemplates,terminals}.js`, `middleware/{terminalAuth,dualAuth,authMiddleware}.js`, `utils/qrcode.js`, `email_worker.js`, `/api/qr-image/:qrcode`, `public/{badge,qrscanner,bulk-badge-print,visitorlog-paginated,checkins,checkin-reports,badge-templates}.html`. Tablolar: visitors (qr_code/badge_id/custom_fields/visitor_type), checkins, visitor_event_status, terminals, badge_templates, email_queue, forms.

**BOZULMAMASI gereken invariant'lar:** (1) QR re-import/re-register/manual-update'te asla değişmez. (2) Check-in duplicate suppression (visitor+terminal, threshold). (3) visitor_event_status `(visitor_id,expo_id)` upsert. (4) Email worker tek-teslimat FOR UPDATE SKIP LOCKED. (5) Terminal scope izolasyonu (expo+organizer). (6) visitor_type server/forms'tan, client'tan değil.

---

## C. EXPO MASTER RECORD — İSKELET

`expos` tam kolon listesi (`initial.sql:17-29`): `id, organizer_id, name, slug, location(tek free-text), description, logo_url, start_date, end_date, created_at, updated_at` + `reactivation_closed_at/by` (migr 006).

**Gerekli alan kontrolü — hepsi YOK:** edition/year, sectors(multi), country, city, venue (hepsi `location` TEXT'ine sıkışmış), build-up/breakdown, deadlines (catalogue/stand-design/payment/visa), operation-team contacts (**users tablosu yok** — yalnız `organizers`), form URLs, `cluster_id`/co-location, `expo_partners` role enum.

CRUD (`routes/expos.js`): POST yalnız `name, location, start_date, end_date, logo_url, description` kabul eder (`:129`); PUT aynı 6 alan (`:200`). **Gap: Part 2.5 master record'unun neredeyse tamamı yok** — üstelik operation-team contacts için önce bir users/staff tablosu gerek (yok).

---

## D. CATALOGUE GENERATOR — YOK

**Exhaustive grep (app root, node_modules hariç):** `catalog`/`catalogue` = **0**, `corel` = **0**, PDF/render lib (`puppeteer|playwright|pdfkit|wkhtmltopdf|pdf-lib|jspdf|pdfmake`) = **0** kodda VE package.json'da. `catalogue_submission` tablosu = YOK (tek "submission" = `forms.submission_count`). Template editor / web catalogue / self-service editor = YOK.

package.json bağımlılıkları (`:13-27`): sendgrid, bcrypt, body-parser, cors, dotenv, express, jsonwebtoken, multer, papaparse, pg, qrcode, uuid, xlsx. **Hiç PDF/HTML-render bağımlılığı yok.** (Sertifikadaki "print-to-PDF" tarayıcı `window.print()`.)

**Gap: uçtan uca sıfırdan** — catalogue_submission modeli, self-service web editör, 3-4 master template/expo, deadline-lock, print-PDF render motoru (kütüphane bile yok — Puppeteer/Playwright net-new), web catalogue sayfası, on-demand regenerate. Genişletilecek temel yok.

---

## E. EMAIL ALTYAPISI — GENİŞLET

**Worker gerçekten çalışıyor ve sağlam (`email_worker.js`):** iki-katman priority fetch (transactional önce, campaign sonra, :34-104), concurrency `FOR UPDATE SKIP LOCKED` BEGIN/COMMIT (:40-66), 3 send modu (direct HTML / visitor+template / fallback, :156-223), reply-to `reply@replies.leena.app` (:239) + inbound parse `emailInbound.js`.

**Var olan özellikler:** bulk+single (`emailSend.js`), template CRUD+default+cross-expo clone (`emailTemplates.js`), segments, reactivation campaigns, **sequence campaigns** (migr 004 + `campaigns.js` + worker scheduler :270-646: çok-adım, per-step `delay_hours`, koşullar all/opened/clicked/registered, tracking pixel, unsubscribe).

**8'li operasyonel zincir + per-expo trigger için gap:**
- **Per-expo days-before-expo trigger: YOK.** Sequence step'leri `delay_hours` = *bir önceki adımdan göreli* (migr 004:55, `computeNextDue` :598-620). Mutlak "expo.start_date'ten X gün önce" scheduling hiçbir yerde yok.
- **"Welcome" tetik event'i: YOK.** Campaign yalnız manuel `POST /campaigns/:id/activate` ile başlar (`:784`); recipient CSV (`:450`) veya expo `visitors`'tan (`:582`) manuel yüklenir. **LEENA'da contracts tablosu yok**, dolayısıyla contract-signing'de Welcome tetikleyecek event yok.
- Multi-language (EN/FR/TR) variant: YOK (language kolonu yok). Marketing-vs-operational flag: YOK. Sender-mailbox-per-template: YOK (tek global sender, reply-to hardcoded).

**Verdict GENİŞLET:** Send altyapısı (queue, SKIP-LOCKED worker, 3 mod, sequence scheduler) güçlü temel. Eklenecek: mutlak days-before-`expo.start_date` scheduler, Welcome için event kaynağı (LEENA'da contract event yok → ELIZA exhibitor-sync gerek, bkz. F), dil variant kolonları, marketing/operational flag, per-template-type sender mailbox.

---

## F. EXHIBITOR ENTEGRASYONU — İSKELET

**Outbound HTTP client (req 882): YOK.** Hiçbir LEENA dosyası `axios/node-fetch/got/request/undici` import etmiyor (grep = 0). `axios` yalnız `@sendgrid/client`'ın transitive bağımlılığı (package-lock.json:34), doğrudan kullanılmıyor. Tek `fetch(` çağrıları frontend'in kendi `/api`'sine. **Hiçbir dış-sistem client'ı yok.**

**`expo_exhibitors` (migr 003):** var (`:6-21`), `company_id` nullable, FK'siz (yorum :16). CRUD (`exhibitors.js`) POST yalnız `name/contact_person/email/phone/country/sector/notes` yazar — **`company_id` hiç yazılmıyor** (grep = 0). Nullable-hiç-dolmayan stub.

**Stands'te `company_id`/`contract_id` (migr 001:105-106):** nullable, constraint'siz; floorplan.js'te yalnız version clone'da **kopyalanıyor** (`:383-384`), create/update request body'den kabul etmiyor. `expo_stand_assignments` Phase-2 stub.

**ELIZA/LiFFY URL:** yalnız SQL yorumlarında (migr 001/003), kod yok, env yok, client yok.

**Verdict İSKELET:** DB kolonları ön-hazır ama **entegrasyon mantığının %100'ü yapılmamış** — outbound HTTP client + ELIZA auth, fetch/cache/refresh servisi, event-driven refresh, company_id/contract_id doldurma mantığı, ve LEENA'da contract entity (yok — bu aynı zamanda E'deki Welcome tetiğini de blokluyor).

**Kritik cross-area bulgu:** LEENA'nın **ne contract entity'si ne de dış API client'ı var** — bu ikisi aynı anda hem E'deki Welcome-email tetiğini hem F'deki ELIZA-exhibitor sync'ini blokluyor.

---

## KORU ADALARI (canlı, dokunulmayacak) — net liste

1. **Floor Plan Builder** — `routes/floorplan.js` (18 endpoint), `migrations/001`+`003`, `public/floorplan/*`, trigger+partial-index+çift-UNIQUE+GENERATED kolon.
2. **Visitor/Check-in/Badge/QR/Terminal çekirdeği** — `routes/{visitors,terminalCheckins,checkins,checkinReports,badgeTemplates,terminals}.js`, `middleware/{terminalAuth,dualAuth,authMiddleware}.js`, `utils/qrcode.js`, `email_worker.js`, ilgili `public/*.html`.
3. **Reactivation campaigns** (TAM) + **Conference certificates** (TAM).
4. **Email gönderim altyapısı** (queue/worker/3-mode/sequence) — KORU ama üzerine operasyonel-zincir GENİŞLET edilecek.

**Şart:** Bu adalara dokunmadan önce iki şey düzeltilmeli (canlıyı bozmadan, ayrı PR): (a) `buildVisitorFilter`'a organizer_id, (b) `.env.backup` git'ten kaldır + secret rotasyonu + webhook hardcoded token.

---

## GÜVENLİK DURUMU: LIFFY/ELIZA İLE KIYAS
- **ELIZA'dan İYİ** — ELIZA'da API auth hiç yoktu; LEENA her endpoint'te var.
- **LIFFY ile AYNI (tenant izolasyonu)** — birebir "expo_id var, organizer_id yok" açığı visitor list/export'ta.
- **İKİSİNDEN KÖTÜ (secret hijyeni)** — git-tracked `.env.backup`'ta gerçek JWT+SendGrid key + canlı hardcoded webhook token.
- **Net:** Üçü de üretim için yetersiz güvenlikte; LEENA ortada — auth katmanı en iyisi, secret hijyeni en kötüsü, tek-tenant gerçeği şu an sömürüyü engelliyor.

---

## EN BÜYÜK 3 RİSK / SÜRPRİZ

1. **🔴 EKSİK MIGRATION MAYINI — ELIZA'dan KÖTÜ.** `initial.sql` yalnız 8 tablo tanımlıyor ve ciddi senkron-dışı; **7 çekirdek üretim tablosu hiçbir CREATE'e sahip değil:** `terminals, badge_templates, conference_certificates, exhibitor_leads, import_logs, reactivation_tokens, visitor_event_status` ("CREATE found in 0 file(s)"). `terminals` tüm check-in/badge akışının belkemiği ve repoda sıfır şema. Üstelik `visitors.qr_code` üzerinde **UNIQUE constraint repoda yok** — QR-koruma invariant'ı prod-only constraint'e bağlı. `initial.sql:4` başta `DROP TABLE CASCADE` yapıyor — prod'a çalıştırmak felaket olur. **Repodan çalışan bir ortam kurulamaz.**
2. **🟠 CANLININ TEK KORUMASI TEK-TENANT GERÇEĞİ.** `buildVisitorFilter` (visitors.js:18) tenant'lar arası PII sızdırmaya kod-olarak açık; sadece ikinci bir organizer olmadığı için patlamıyor. Kayıt açık (`auth.js:75`) — ikinci tenant kaydolduğu an export/paginated/bulk-email kod değişmeden sızar. Zaman bombası.
3. **🟡 STAGING YOK + SESSİZ DEPLOY HATASI.** Deploy = `git push` → Render auto-deploy, **staging yok** (`render.yaml` yok, gerçek test script yok). `index.js` route'ları try/catch ile yüklüyor — bozuk bir route dosyası **çökmek yerine sessizce mount olmuyor** (`✗ Failed to load` log'lar) → regresyon fark edilmeden canlıya çıkabilir.
   **Bonus sürpriz (pozitif):** Canlı operasyon çekirdeği (floor plan + terminal check-in + email worker) gerçekten **üretim-kalitesinde** — transaction'lar, FOR UPDATE SKIP LOCKED, duplicate-guard, DB-invariant'lar, QR-koruma. Diğer iki sistemin aksine LEENA'nın çekirdeği sağlam; sorun çevrede (master record, catalogue, entegrasyon) ve güvenlik hijyeninde.

---

## "CANLIYI BOZMADAN ÜZERİNE İNŞA" — DİKKAT EDİLECEK 3 NOKTA

1. **QR'ı asla yeniden üretme.** Dört upsert yolu da mevcut email+expo'da QR'ı korur (webhook.js:174, visitors.js public/manual/import). Repoda `qr_code` UNIQUE constraint'i YOK — kararlılığı DB değil app sağlıyor. Update'te yeni UUID basan bir yeni yol, basılmış/gönderilmiş badge'leri fuar ortasında sessizce geçersizleştirir.
2. **Shared pool'da ad-hoc transaction çalıştırma, email_worker claim sorgusuna dokunma.** Çok-statement yazma için `pool.connect()`+dedicated client kullan (terminalCheckins.js'i kopyala, expos.js delete'ini DEĞİL). `UPDATE ... FOR UPDATE SKIP LOCKED` (email_worker.js:41-47) aynen kalsın — çift-gönderimin tek koruması ve worker ayrı bir Render servisi (web deploy'da restart olduğunu görmezsin).
3. **Her yeni visitor-data endpoint'i organizer_id ile filtrelemeli (expo_id yetmez) + her yeni tablo gerçek migration almalı.** `buildVisitorFilter` yanlış emsal (expo_id-only) — kopyalamak sızıntıyı yayar. `initial.sql`'in prod'u yansıttığını ASLA varsayma (7 tablo + qr UNIQUE yalnız canlı DB'de); migration'ı staging-yokluğunda iki-fazlı dry-run (COMMIT→ROLLBACK) ile test et.

---

## METODOLOJİ & SINIRLAR
- 3 paralel ajan: (A+G güvenlik/live-build), (B1+B2 KORU), (C+D+E+F gap). Her bulgu `dosya:satır`. node_modules taranmadı.
- Olgunluk: TAM/KISMI/İSKELET/BOZUK/YOK. LEENA'da çekirdek operasyon TAM (canlı-kanıtlı), çevre İSKELET/YOK.
- **Bulamadım:** 7 üretim tablosunun CREATE'i (terminals/badge_templates/conference_certificates/exhibitor_leads/import_logs/reactivation_tokens/visitor_event_status); `visitors.qr_code` UNIQUE; herhangi bir catalogue kodu; days-before-expo email trigger; multi-language template; outbound HTTP client; contract entity — hiçbiri repoda yok.
- "Var" denen her şey kanıtlı; kanıtlanamayan "bulamadım" dendi. Hiçbir dosya değiştirilmedi.
