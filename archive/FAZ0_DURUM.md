> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# FAZ 0a — DURUM NOTU ("nerede kaldık")

> Tek sayfa, madde madde. Gelecek oturum buradan devam eder.

---

## TAMAMLANAN: Faz 0a — Production şema kurtarma (üç sistem de bitti)

- **LEENA:** 8 eksik tablo (terminals, badge_templates, conference_certificates, exhibitor_leads, import_logs, reactivation_tokens, visitor_event_status, exhibitors) + kolon/index drift koda eklendi (migrations `000`, `000a`) + guard'lı `setup-fresh-db.js`. **Commit `9f9e8b9`. Deploy live. Zero-diff doğrulandı.**

- **ELIZA:** 3 tablo (attention_log, expo_metrics, sent_briefings) + 2 view (edition_contracts, fiscal_contracts) + drift koda eklendi (migrations `010`, `025`) + guard'lı `setup-fresh-db.js`. **Commit `a3a80cc`. Zero-diff doğrulandı.**
  - AYRICA: önceden var olan latent build bug düzeltildi — `apps/api/src/routes/auth.js` `require('@eliza/db')` → relative path. **Commit `b2751d9`. Deploy live, /health 200.**

- **LIFFY:** SADECE eksik `mining_results` tablosu eklendi (migration `047`). **Commit `be58541`. Deploy live.** Drift/ordering bilinçli olarak Faz 1'e ertelendi (aşağıda).

---

## DB ERİŞİM DURUMU

- **LEENA:** `claude_readonly` kullanıcısı (gerçek read-only, kanıtlandı)
- **ELIZA:** `eliza_73du_user` (full-write). Render eliza-db, PG18. Bağlantı `.claude/settings.local.json`'da `DATABASE_URL_PROD` anahtarında.
- **LIFFY:** `liffy_user` (full-write).
- ELIZA/LIFFY için read-only kullanıcı **OLUŞTURULMADI** — prompt disipliniyle çalışıldı (kullanıcının kararı). Şema çekimi `pg_dump --schema-only` ile yapıldı (yazmaz).
- Üç şema dökümü: `~/ELL_schema_dumps/{leena,liffy,eliza}_schema_2026-06-02.sql`

---

## AÇIK İŞLER (gelecek fazlar)

### Faz 0b — Secret hijyeni (ACİL, sıradaki oturumun İLK işi)

**LIFFY (en kritik — repo PUBLIC):**
- Repo `github.com/Nsueray/liffyv1` **PUBLIC** ve full-write DB şifresi `CLAUDE_QUICKSTART.md`'de **~60 commit boyunca düz metin sızmış**.
- `liffy-db` Render'da **IP-kısıtsız**: PostgreSQL Inbound = `0.0.0.0/0` (herkese açık).
- `liffy-api` `DATABASE_URL`'i **EXTERNAL form** (`...oregon-postgres.render.com`) ve **LITERAL yapıştırılmış** (linked-to-database referansı DEĞİL) → IP kısıtı eklemek servisi **KOPARIR**; rotation'da env **elle** güncellenmeli.
- `liffy-api` env'inde çok sayıda secret: `ANTHROPIC_API_KEY`, `SENDGRID_API_KEY`, `ZEROBOUNCE_API_KEY`, `JWT_SECRET`, `INBOUND_WEBHOOK_SECRET`, `MANUAL_MINER_TOKEN`, `DATABASE_URL`. **KONTROL EDİLMELİ:** hangileri `CLAUDE_QUICKSTART.md` veya başka tracked dosyada sızmış? (Anthropic/SendGrid key sızmışsa = para riski.)
- **SONRAKİ OTURUM İLK İŞ:** (1) hangi secret'lar git'e sızmış tam tespit, (2) her birini rotate, (3) servis env'lerini güncelle, (4) git geçmişi temizliği (BFG/filter-repo) opsiyonel ama önerilir, (5) `liffy-db`'ye IP kısıtı + servisleri internal'a çevirmeyi değerlendir.

> **⚠️ DB ŞİFRE ROTATION YARIM KALDI — `liffy_user`'ı SİLME!**
> - `liffy-db`'de yeni kullanıcı oluşturuldu: **`liffy_user_v2`** (artık "Default").
> - AMA servisler (`liffy-api`, `liffy-worker`) HÂLÂ eski **`liffy_user`** ile bağlı (env'de `DATABASE_URL` literal, eski şifreyle). Eski `liffy_user` aktif (1 açık bağlantı), **SİLİNMEDİ**.
> - 🛑 **`liffy_user`'ı SİLME!** Servisler hâlâ onu kullanıyor; silinirse LIFFY KOPAR. Önce servis env'leri v2'ye geçmeli.
> - Durum **GÜVENLİ**: LIFFY çalışıyor, bir şey kopmadı. Ama sızıntı KAPANMADI (eski şifre git'te + hâlâ geçerli).
>
> **Tamamlama adımları (zero-downtime):**
> 1. `liffy-api` + `liffy-worker` env'inde `DATABASE_URL` → v2 (tercihen "Add from Database" referansı = otomatik + gelecek-proof; ya da v2 string'i elle yapıştır)
> 2. İki servisi redeploy et
> 3. `liffy_user` bağlantısı 0 olana dek izle: `SELECT count(*) FROM pg_stat_activity WHERE usename='liffy_user'`
> 4. `liffy_user`'ı sil (Render tam silmez, login'ini iptal eder → DB nesneleri korunur, sızıntı kapanır)
> 5. Diğer sızmış secret'lar (ANTHROPIC/SENDGRID/ZEROBOUNCE API key'leri vs.) ayrıca kontrol + rotate
> 6. `liffy-db` IP kısıtı (`0.0.0.0/0` → kendi IP'lerin) ayrıca değerlendir

**Diğer iki sistem:**
- **LEENA:** commit'li secret (`.env.backup`), JWT/SendGrid rotate.
- **ELIZA:** `JWT_SECRET` hardcoded default — `.env`'e taşı.
- **Genel:** üç repoda `.gitignore` `.env*` kapsasın, Zoho webhook token'ları env'e.

### Faz 1'e ertelenen LIFFY temizliği (LIFFY zaten Faz 1'de elden geçecek)
- `mining_jobs` +15 kolon drift, ~15 tabloda index drift
- migration ordering tutarsızlığı (`005` henüz olmayan `007`'ye başvuruyor → sıfırdan rebuild edilemiyor), baz şema yok, runner/guard yok

### Diğer notlar
- **eliza-bot:** apps/api ile aynı build pattern'den (workspace symlink) etkilenebilir — **KONTROL EDİLMEDİ.** Bir gün cache temizlenince patlayabilir. Düşük öncelik.
- **Render:** üç sistem de Auto-Deploy "On Commit". Deploy'da migration **ÇALIŞMAZ** (build=npm install, start=node, pre-deploy boş). Migration'lar elle uygulanıyor.

---

## SONRAKİ ADIM (kullanıcının kararına bağlı)
- **Faz 0b (secret hijyeni)** — özellikle LIFFY sızmış secret
- **VEYA doğrudan Faz 1** (LIFFY güvenlik izolasyonu → quote modülü)
- Kanonik pusula DEĞİŞMEDİ: `ELL_YOL_HARITASI_v4.md` hâlâ geçerli.
