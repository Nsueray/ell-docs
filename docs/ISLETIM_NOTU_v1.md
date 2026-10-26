# ELIZA + LIFFY İşletim Notu v1 (TASLAK)

> 26 Ekim 2026, Paket 3 canlıya geçişi. **ell-docs PUBLIC bir repodur.** Bu yüzden bu notta host adı, DB kullanıcı adı, UUID ve
> sır değeri YOK; yalnız adlar ve görevleri var. Ayrıntılı Render envanteri Orchestrator KB'sindedir, repoda değildir
> ([defter:2026-10-08 RENDER ENVANTERİ + FAZ A ROTASYON ÖN-ÖLÇÜMÜ]). Tarih kaydı = o günün ölçümü (YON-01).

## 1. Hangi servis hangi dalı izler

| Sistem | Render servisi | Repo · dal | Adres | Not |
|---|---|---|---|---|
| ELIZA / LEENA | `Leena_v401` (web) | `Leena_v401_monorepo` · `main` | leena.app (ui2: `/ui2/`) | Push = canlı deploy, 20–60 sn kesinti (G43) |
| | `leena-email-worker` | aynı repo · `main`¹ | — | Root `backend/leena-v401-backend` · start `node email_worker.js`: e-posta kuyruğu + kampanya |
| | `leena_v401_db` | — | — | PostgreSQL 17 · PITR 7 gün + export |
| | `leena-staging` (web) | aynı repo · **`eliza-next`** | leena-staging.onrender.com | Worker YOK · ayrı DB (`leena-staging-db`) |
| LIFFY | `liffy-api` | `liffyv1` · `main` | api.liffy.app | |
| | `liffy-worker-docker` | `liffyv1` · `main` | — | Mining / import (Playwright) |
| | `liffy-ui` | `liffy-ui` · `main` | liffy.app | `/api/*` → api.liffy.app (`next.config.ts:8`) |
| | `liffy-redis` · `liffy-db` | — | — | Kuyruk · PostgreSQL 17 |

¹ Render Settings (Suer, 26 Eki): dal `main` · root `backend/leena-v401-backend` · start `node email_worker.js` · auto-deploy
On Commit — yani her LEENA `main` push'u worker'ı da yeniden başlatır. Repoda `render.yaml` / `Procfile` / Dockerfile YOK;
ayar yalnız Render panelinde ([defter:2026-10-26 P3 KAPANIŞ DÜZELTMELERİ CANLIDA]).

- **LIFFY'nin staging'i YOK.** Kurulumu kabul edildi (YON-13 c). O gelene kadar `liffy-api` canlı LEENA'ya bağlı kalır;
  env'i canlı ↔ staging arasında ileri-geri çevirmek **YASAK** (YON-13).
- **Kod canlıya şöyle çıkar:**
  - **LEENA:** iş `eliza-next`'te yapılır → push → staging kendiliğinden deploy olur → Suer kabul eder → CC `main`'e
    `--no-ff` merge eder → Suer sırayla: YON-06 iki ölçüm → export (YON-12) → `main` push → migration → env değişikliği.
  - **LIFFY:** `main`'e push doğrudan canlıdır.
  - Push'u yalnız Suer yapar.

## 2. Env değişkenleri: ad ve görev (değer yok)

**LEENA web (`Leena_v401` / `leena-staging`):**
- `PGHOST` `PGPORT` `PGDATABASE` `PGUSER` `PGPASSWORD`: uygulamanın ve migration koşucusunun DB bağlantısı (`utils/db.js`,
  `scripts/migrate.js`).
- `DATABASE_INTERNAL_URL`: Render Shell'de `psql` için. `DATABASE_URL`: eski betikler.
- `JWT_SECRET`: kullanıcı oturumu (klasik ekranlar + ui2).
- `LIFFY_HMAC_SECRET`: LIFFY servis kimliğinin imza sırrı. Yoksa servis yolu kapalıdır. **Canlı ve staging değerleri
  farklıdır.**
- `UNSUBSCRIBE_SECRET`: e-postadaki abonelikten çıkış imzası. Yoksa uygulama açılmaz.
- `SENDGRID_API_KEY` · `SENDER_EMAIL` · `ADMIN_EMAIL`: e-posta gönderimi.
- `BASE_BADGE_URL`: e-postalardaki rozet linklerinin kökü.
- `ZOHO_WEBHOOK_TOKEN`: Zoho form webhook'unun doğrulaması. Yalnız env'den okunur; yoksa webhook 503 döner ve açılış logu
  bunu yazar (LEENA `606d175`; koddaki gömülü yedek kaldırıldı — [defter:2026-10-26 P3 KAPANIŞ DÜZELTMELERİ]).
- `CALLCENTER_KEY` · `CALLCENTER_SUPERVISOR_KEY` · `CALLCENTER_AGENTS` · `CALLCENTER_REPORT_TO`: çağrı merkezi.
- `CORS_EXTRA_ORIGINS`: ek izinli kökenler.
- `EXPECTED_DB_NAME`: bağlanılan DB adı farklıysa uygulama açılmaz; staging koruması.
- `INVITE_ECHO=1`: davet linkini yanıtta gösterir. **Yalnız staging'de kullanılır.**
- `NODE_ENV` · `PORT`.

**`leena-email-worker`** (statik require grafiği 5 dosya: `email_worker.js` + `utils/email.js`, `utils/qrcode.js`,
`utils/trackingPixel.js`, `utils/callCenterReport.js` — ölçüldü 26 Eki):
- `PG*` · `NODE_ENV`: DB bağlantısı.
- `CAMPAIGN_SENDER_NAME` · `CAMPAIGN_SCHEDULER_INTERVAL_SECONDS` · `CAMPAIGN_SCHEDULER_BATCH_LIMIT` · `EMAIL_WORKER_BATCH_SIZE`:
  kampanya ve kuyruk hızı (G8).
- `SENDGRID_API_KEY` · `SENDER_EMAIL`: gönderim. `UNSUBSCRIBE_SECRET`: e-postadaki çıkış/izleme bağlantısı imzası.
- `BASE_BADGE_URL`: rozet linklerinin kökü. `CALLCENTER_REPORT_TO`: çağrı merkezi raporunun alıcısı.
- Bunlar worker servisinde tanımlanır; web servisinde tanımlamak işe yaramaz (G34).

**LIFFY (`liffyv1`; api ile worker aynı kodu çalıştırır):**
- `DATABASE_URL` · `REDIS_URL`: DB ve kuyruk.
- `JWT_SECRET`: LIFFY oturumu. **Yalnız `liffy-api`'de**; worker'dan 26 Eki'de kaldırıldı.
- `UNSUBSCRIBE_SECRET`: abonelikten çıkış imzası, JWT'den bağımsız (SEM-07). api ve worker'da aynı değer.
- `LEENA_API_URL` · `LEENA_HMAC_SECRET` · `LEENA_SERVICE_USER_ID`: ELIZA entegrasyonu.
  - Yalnız `liffy-api`'de tanımlıdır; biri bile eksikse entegrasyon kapanır ve log yalnız eksik adları yazar.
  - `LEENA_HMAC_SECRET`, bağlanılan LEENA ortamındaki `LIFFY_HMAC_SECRET` ile aynı değerdir.
  - `LEENA_SERVICE_USER_ID`, o ortamdaki servis kullanıcısının kimliğidir. Sır değildir ama ortama özeldir: ui2 Admin › Users →
    "LIFFY (service)" satırı, adres çubuğundaki `user=` değeri.
- `DISABLE_CONVERT_OUTBOX`: outbox koşucusunu kapatır (acil durum anahtarı).
- `SENDGRID_API_KEY` · `INBOUND_WEBHOOK_SECRET` · `INBOUND_PARSE_ADDRESS`: e-posta gönderimi ve gelen yanıtlar.
- `ANTHROPIC_API_KEY` · `ZEROBOUNCE_API_KEY` · `MINING_*`: mining ve doğrulama.

**`liffy-ui`:** `BACKEND_URL` (login yönlendirmesi, yoksa hata verir) · `NEXT_PUBLIC_API_URL` · `API_BASE_URL`.

## 3. Sırlar nerede (değer yok)

- **Çalışan değer:** ilgili Render servisinin *Environment* sekmesi.
- **Yedek kopya:** parola yöneticisi (LIFFY için "Render env / 1Password", `LIFFY_OPERATIONS.md`). Yeni üretilen bir sır önce
  buraya yazılır, sonra Render'a girilir.
- **Birlikte değişmesi gereken çiftler:**
  - LEENA `LIFFY_HMAC_SECRET` ↔ LIFFY `LEENA_HMAC_SECRET`. Her ortamın çifti ayrıdır.
  - LIFFY `UNSUBSCRIBE_SECRET`: api ve worker'da aynı olmalı.
  - HMAC çifti değişirken aradaki convert'ler *failed* düşebilir. Bitince LIFFY'de **Resend** yapılır.
- **CC'nin erişimi:** yalnız salt okunur canlı DB (yerel `.env` → `RENDER_DATABASE_READONLY_URL`, yalnız SELECT, IP izin
  listesi).
  - Değerler ekrana basılmaz (K4).
  - Kod araması `git grep -l`/`-c` ile ya da sınanmış maskeyle yapılır.
- **Rotasyon:** toplu rotasyon Paket 4 öncesi yapılacak (Faz B kuyruğu).

## 4. Migration nasıl koşulur

Kural: CC migration'ı **yazar ama çalıştırmaz**; Suer koşar. CC canlı DB'ye yazmaz.

**LEENA** (`migrations/NNN_*.sql`; 036 ve sonrası **yalnız koşucuyla**, LED-16):
1. Önce staging: `leena-staging` Shell → `node scripts/migrate.js --dry-run`. NOTICE satırlarını teslim metnindeki beklenenle
   karşılaştır; sonda `DRY-RUN OK: N` görünmeli.
2. Ardından `node scripts/migrate.js` → `COMMIT: N` görünmeli.
3. Kabulden sonra canlı: önce YON-06 iki ölçüm ve export (YON-12), sonra `Leena_v401` Shell'de aynı iki komut.
4. Koşucu yalnız `PG*` ile bağlanır, `.env` okumaz; şu durumlarda hiçbir şey uygulamadan DURUR: kayıtsız dosya, yarım
   uygulanmış dosya, numara boşluğu, sıra dışı dosya, ikinci koşucu.
5. **Deploy sırasında Shell'de iş yapılmaz.** Env değişikliği de yeniden deploy tetikler ve açık işlemi keser (G46). Bu yüzden
   önce migration, sonra env.

**LIFFY** (koşucu yok, `psql` ile):
- Paket 3 dosyaları (054 ve sonrası): `liffy-api` Shell → `bash backend/scripts/migrate_p3.sh`. Betik `DATABASE_URL` ile
  bağlanır, ilk hatada durur ve sonda bir doğrulama satırı basar; ikinci koşuda değişiklik yapmaz.
- Tek dosya: `psql "$DATABASE_URL" -X -v ON_ERROR_STOP=1 -f backend/migrations/NNN_*.sql`.

## 5. Sağlık kontrolü (log satırları)

- **LEENA:**
  - `/health` 200 döner.
  - Log: `✓ LIFFY expo publishing routes loaded`.
  - Sır varsa `✓ Service identity (LIFFY_HMAC_SECRET) enabled — signature v2 · …`, yoksa
    `ℹ Service identity path closed — LIFFY_HMAC_SECRET not set`.
- **LIFFY api:**
  - `[LEENA] integration enabled (expo sync + convert, signature v2)` ya da
    `[LEENA] integration OFF — missing env: <adlar>`.
  - `[convertOutbox] started — every 60 s …`.
