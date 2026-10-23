# ELL FAZ B RUNBOOK v1 — Anthropic API anahtarı + LIFFY JWT_SECRET

> **Kaynak:** Sentez 23 Eki, E bölümü (Faz B başı; KAPI-2 — sır rotasyonu; **Sentez GO var**). Kütük: K-E (LIFFY
> JWT_SECRET: fallback temizliği + "env yoksa başlama", YON-08) · YON-11 · YON-06.
> **Kapsam:** (a) LIFFY'nin Anthropic anahtarının yenilenmesi + eskisinin iptali · (b) LIFFY JWT_SECRET: koddaki sabit
> yedeklerin kaldırılması + açılış koruması + yeni değer.
> **DB export GEREKMEZ** — LIFFY DB'ye dokunuş yok (yalnız Render env + kod).
> **Sır değeri** yalnız Anthropic Console · Render paneli · parola yöneticisinde yaşar. Sohbete, deftere, commit'e,
> ekran görüntüsüne YAZILMAZ.
> **Çelişkide DEFTER kazanır.** Bu belge adım tarifidir; ne yapıldığı defterde [defter:2026-10-23 FAZ B RUNBOOK].

---

## 0. Ölçüm (CC, 2026-10-23, salt-okunur — değer basılmadı; liffyv1 `main` @ `9954054` = origin/main)

### 0.1 Anthropic anahtarını kim tüketiyor
- Env adı: **`ANTHROPIC_API_KEY`** — `backend/services/aiMinerGenerator.js:751`, `:1276`.
- **liffy-api** (`backend/server.js`): `POST /api/admin/ai-miner/generate` (`routes/adminAIMiner.js:68`; mount
  `server.js:93`; JWT ister `:9-23`; anahtar yoksa 400 `:72-73`) → `generateMiner` (`aiMinerGenerator.js:1090`) →
  `callClaudeAPI` (`:750`, istek `:765`) + adım-2 isteği (`:1272`).
- **liffy-worker-docker** (`backend/worker.js`): yalnız madenciler 0 kişi döndürür **ve** `AI_MINER_GENERATOR_ENABLED ===
  'true'` ise (`services/superMiner/services/flowOrchestrator.js:966`); kayıtlı üretilmiş miner yoksa
  `generateMinerWithRetry` (`:1018`) → Claude. Kayıtlı miner'ı çalıştırmak (`runGeneratedMiner` `:1427`) Claude çağırmaz.
- Yerel CLI: `backend/scripts/testAIMinerGenerator.js` (`generateMiner` / `generateMinerV2` → `callClaudeRaw` `:1840`,
  istek `:1846`). `:37`'deki `sk-ant-...` yalnız yardım metni, anahtar değil.
- **Sızıntı yeri:** `liffyv1/.claude/settings.local.json` (git'te İZLENMİYOR, hiç commitlenmemiş) — anahtar değeri
  **16 satırda** (`:45-60`), **tek** farklı anahtar. Aynı dosyada **31 satırda** şifreli LIFFY DB bağlantı dizesi (ayrı
  madde, bu runbook'ta değil — §3).
- Render'da hangi serviste `ANTHROPIC_API_KEY` ve `AI_MINER_GENERATOR_ENABLED` tanımlı → **ÖLÇÜLMEDİ** (panel; a1).

### 0.2 LIFFY JWT_SECRET yedekleri (sabit değerler basılmadı)
- **30 dosyada** `process.env.JWT_SECRET || '<sabit>'`, **3 farklı sabit:**
  - grup 1 (25 dosya, tek sabit): `routes/` → actions · adminAIMiner (`:7`) · auth (`:8`) · campaignRecipients ·
    campaignSend · campaigns · context · emailLogs · emailTemplates · intents · leads · lists · miningResults · persons ·
    prospects · reports · senders · sequences · settings · stats · timeline · unsubscribes · verification · waiting · zoho.
  - grup 2 (4 dosya, başka sabit): `middleware/auth.js:23` (dışa verir `:79`) · `routes/miningJobs.js:10` ·
    `routes/sourceDiscovery.js:15` · `scripts/test_adr015.js:22`.
  - grup 3: `utils/unsubscribeHelper.js:27` — `UNSUBSCRIBE_SECRET || JWT_SECRET || '<sabit>'`.
- Token ÜRETEN `routes/auth.js:88`, `:151` (grup 1 sabiti), doğrulayan `middleware/auth.js` (grup 2 sabiti) → env yoksa
  giriş zaten kırık olurdu: canlıda `JWT_SECRET`'ın tanımlı olduğuna DOLAYLI işaret (ölçüm değil — b0).
- **Abonelikten çıkma imzası JWT'ye bağlı olabilir:** HMAC (`unsubscribeHelper.js:31-41`) worker (`worker.js:15`),
  `routes/webhooks.js`, `services/sequenceService.js`, `routes/campaignSend.js` tarafından üretilir; `GET
  /api/unsubscribe/:token` (`webhooks.js:934`) doğrular — yalnız onay sayfası gösterir, işlem `POST` (`:959`).
  **`UNSUBSCRIBE_SECRET` tanımlı değilse JWT değişince gönderilmiş tüm e-postalardaki çıkış linkleri "Invalid or
  expired" olur** → b1.
- `backend/.env` git'te izlenmiyor, geçmişte hiç commitlenmemiş (`.gitignore:5`).
- `liffy-ui` (liffy.app): JWT sırrı / doğrulaması YOK; token `localStorage.liffy_token` → rotasyonda kullanıcılar bir kez
  yeniden giriş yapar. `liffy-local-miner`: kullanıcı token'ı `--token` ile (`mine.js:13`, `:30`) → rotasyon sonrası yeni
  token gerekir.
- LEENA'da LIFFY token'ını doğrulayan kod YOK (`routes/contracts.js` yalnız yorum, cross-system fetch yok) → LEENA etkilenmez.
- **Emsal (LEENA):** `utils/bootGuards.js` (saf fonksiyon, fail-closed; `index.js` süreci durdurur) · `routes/auth.js:43`
  (JWT_SECRET yoksa hata, yedek değer YOK).
- Deploy: liffyv1 `main`'e push iki servisi de auto-deploy eder (`LIFFY_OPERATIONS.md:12`; worker ~3-5 dk, api ~2 dk).
  LIFFY'de test zinciri yok (`package.json` yalnız `start`).
- Sağlık (23 Eki 11:3x UTC): `https://api.liffy.app/api/health` **200** (DB `SELECT 1`, `server.js:55`) · `https://liffy.app/` **200**.

---

## 1. Genel kurallar (her adımda)

- **Pencere:** LIFFY'de kampanya gönderimi ve madencilik işi sürmüyorken (worker yeniden başlar; yeniden deploy
  çakışması — LIFFY CLAUDE.md madde 42) + YON-06 (status.render.com).
- **Render env değişikliği:** değişkeni kaydet → deploy başlat ("Save and deploy"; seçenek yoksa Manual Deploy →
  Deploy latest commit). Süre: api ~2 dk, worker ~3-5 dk.
- **Sır üretme/kopyalama:** değer ekrana basılmaz (`… | pbcopy`), doğrudan panele yapıştırılır, parola yöneticisine yazılır.
- Her adım: doğrulama geçmeden sonrakine geçilmez (K1). Başarısızsa o adımın geri alması.

---

## 2A. Anthropic API anahtarı (tek iş — a1 → a6)

| # | ne | nerede | doğrulama | geri alma |
|---|---|---|---|---|
| a1 | **Bakış (yalnız ad):** `ANTHROPIC_API_KEY` hangi serviste tanımlı? `AI_MINER_GENERATOR_ENABLED` değeri ne? | Render → liffy-api → Environment; liffy-worker-docker → Environment | sonucu CC'ye yaz (değer değil, "var/yok" ve bayrak değeri) | — |
| a2 | **Yeni anahtar** oluştur (ad: `liffy-prod-2026-10`), değeri parola yöneticisine | Anthropic Console → API Keys → Create Key | Console'da yeni anahtar listede | anahtarı sil |
| a3 | `ANTHROPIC_API_KEY` = yeni değer → kaydet + deploy | Render liffy-api **ve** liffy-worker-docker → Environment | deploy "Live" | eski değeri geri koy + deploy (a5'ten ÖNCE mümkün) |
| a4 | **Anahtar servisin içinden çalışıyor mu** (DB'ye yazmaz, ücretsiz uç) | Render → liffy-api → Shell, sonra liffy-worker-docker → Shell: komut aşağıda | iki serviste de `anthropic 200` (401 = anahtar yanlış/eksik) | a3 geri alma |
| a5 | **Eski anahtarı iptal et** (yalnız a4 iki serviste 200 iken) | Anthropic Console → API Keys → eski LIFFY anahtarı → Disable / Delete | Console'da eski anahtar devre dışı | **YOK** — iptal geri alınmaz; sorun çıkarsa yeni anahtar (a2) |
| a6 | **Son doğrulama:** a4 komutu tekrar | iki Shell | `anthropic 200` · Console "last used" yeni anahtarda | a3 |

a4 komutu (Render Shell'e yapıştır; değeri basmaz, yalnız HTTP kodunu yazar):
```
node -e "fetch('https://api.anthropic.com/v1/models',{headers:{'x-api-key':process.env.ANTHROPIC_API_KEY,'anthropic-version':'2023-06-01'}}).then(r=>console.log('anthropic',r.status)).catch(e=>console.log('hata',e.message))"
```
a5 için eski anahtarı Console'daki listeyle eşleştirme (Suer'in KENDİ terminalinde; çıktı yalnız ön ek + son 4 karakter,
**sohbete yapıştırılmaz**):
```
grep -oE 'sk-ant-[A-Za-z0-9_-]+' ~/Projects/liffyv1/.claude/settings.local.json | sort -u | sed -E 's/^(sk-ant-[a-z]+[0-9]*-).*(.{4})$/\1…\2/'
```
- **İşlevsel deneme (isteğe bağlı, ÖNERİLMEZ):** `POST https://api.liffy.app/api/admin/ai-miner/generate` (JWT ile,
  gövde `{"url": "…"}`) → 202 — Claude'a ücretli çağrı yapar VE LIFFY DB'ye üretilmiş miner satırı yazar. a4 anahtarı
  aynı ortamda, yazmadan doğrular.
- Bitti mi: a6 geçti → CC deftere "FAZ B (a) KAPANDI". `settings.local.json`'daki 16 satır iptal edilmiş anahtarı taşır →
  temizlik §3.

---

## 2B. LIFFY JWT_SECRET (tek iş — b0 → b4; (a) bittikten sonra)

| # | ne | kim / nerede | doğrulama | geri alma |
|---|---|---|---|---|
| b0 | **Bakış (yalnız ad):** `JWT_SECRET` ve `UNSUBSCRIBE_SECRET` hangi serviste var? | Suer — Render liffy-api + liffy-worker-docker → Environment | sonucu CC'ye yaz ("var/yok"). **DUR:** liffy-api'de `JWT_SECRET` YOKSA b2'den önce b3 yapılır (açılış koruması siteyi durdurur) | — |
| b1 | **Çıkış linklerini koru** (🔶 karar, aşağıda): `UNSUBSCRIBE_SECRET` yoksa iki servise `UNSUBSCRIBE_SECRET` = **bugünkü `JWT_SECRET` değeri** (panelde kopyala-yapıştır) → kaydet + deploy | Suer — Render iki servis | LIFFY'den daha önce gelmiş bir kampanya e-postasındaki "Unsubscribe" linkini tarayıcıda aç → **onay sayfası** (GET yalnız sorar — "Unsubscribe" düğmesine BASMA); "Invalid or expired" DEĞİL | değişkeni sil + deploy |
| b2 | **Kod:** 30 dosyada sabit yedek değer kaldırılır (`process.env.JWT_SECRET` tek kaynak); `unsubscribeHelper.js:27` zinciri yalnız `UNSUBSCRIBE_SECRET` → `JWT_SECRET` (sabit yok); yeni `backend/utils/bootGuards.js` (LEENA emsali, saf fonksiyon) → `server.js` açılışta `JWT_SECRET` yoksa `process.exit(1)`; `worker.js` `UNSUBSCRIBE_SECRET` ve `JWT_SECRET`'ın ikisi de yoksa `process.exit(1)`. **Değer değişmez** → oturumlar düşmez. | CC — liffyv1 `main`, commit (kanıt: kodda sabit yedek 0 · env'siz açılış exit 1 · env'li açılış normal) → **Suer:** `cd ~/Projects/liffyv1 && git push origin main` | `curl -s -o /dev/null -w '%{http_code}\n' https://api.liffy.app/api/health` → 200 · liffy.app açık oturum çalışıyor · Render worker logunda açılış satırı ("Liffy Worker"), boot-guard hatası yok | `git revert <commit>` + push |
| b3 | **Yeni değer:** Suer terminali `openssl rand -hex 32 \| pbcopy` → Render liffy-api `JWT_SECRET` yapıştır → kaydet; **AYNI değer** liffy-worker-docker → kaydet → deploy (ayrı deploy, b2'den sonra). Eski değer parola yöneticisinde kalır (b4 geçene kadar). | Suer — terminal + Render | b4 | eski değeri iki servise geri koy + deploy |
| b4 | **Doğrulama** | Suer + CC | health 200 · liffy.app → mevcut oturum düşer (beklenen; eski token 401) → yeniden giriş → listeler açılıyor · b1'deki eski çıkış linki hâlâ onay sayfası · worker logu temiz · `liffy-local-miner` kullanılıyorsa yeni girişten alınan token ile | b3 geri alma |

**🔶 b1 kararı (Sentez):** `UNSUBSCRIBE_SECRET` = eski JWT değeri → gönderilmiş e-postalardaki çıkış linkleri çalışmaya
devam eder; bedeli: eski değer yalnız çıkış imzasında yaşar (onunla oturum açılamaz, yalnız çıkış linki üretilebilir).
Alternatif: yeni bir değer → eski e-postalardaki çıkış linkleri kırılır (yasal çıkış yükümlülüğü riski). **Öneri: eski
değer.** b0 `UNSUBSCRIBE_SECRET`'ın zaten tanımlı olduğunu gösterirse b1 atlanır.

- **Güncelleme (23 Eki, b2 yazıldı — [defter:2026-10-23 FAZ B (b2)]):** b2 kodu dal `faz-b-jwt` (`532d173`), `main`'e
  doğrudan değil. JWT'ye düşme zinciri KALDIRILDI (SEM-07): worker yalnız `UNSUBSCRIBE_SECRET` ister (JWT okumaz), api ikisini
  de ister. b2 satırındaki "`worker.js` ikisi de yoksa" ve "`git push origin main`" bu notla geçersiz; adımlar CC teslim
  bloğunda. (a) ertelendi.
- Bitti mi: b4 geçti → CC deftere "FAZ B (b) K-E KAPANDI" · parola yöneticisindeki eski JWT değeri silinebilir (b1'de
  çıkış imzası olarak paneldeyse orada kalır).

---

## 3. Bu runbook'ta OLMAYAN (Faz B kuyruğunda kalır)

- `liffyv1/.claude/settings.local.json` temizliği: 16 satırda (iptal edilecek) anahtar + 31 satırda şifreli LIFFY DB
  bağlantı dizesi ("sırlı ölü izin kuralları"); LIFFY DB şifresinin yenilenmesi ayrı karar (Sentez).
- **CC oturum dökümü (23 Eki):** iki ölçüm komutu iki değeri maskesiz yazdırdı — `settings.local.json`'daki LIFFY DB
  bağlantı dizesi (şifreli) ve yerel `liffyv1/backend/.env`'deki `JWT_SECRET`. Sohbete / belgeye / commit'e girmedi; yerel
  oturum dökümünde (`~/.claude/projects/-Users-nsa-Desktop-Leena-Projesi-Leena-v401-monorepo/e184f817-….jsonl`) var. Yerel
  JWT değeri canlıyla aynıysa b3 onu geçersiz kılar; LIFFY DB şifresi yenilenince o satır da geçersiz olur.
- Faz B'nin geri kalanı (deftere bak: 3 izlenen `.env.backup` · staging DB inbound · NOLOGIN roller · Render CLI …).
- **Güncelleme (23 Eki kapanış — [defter:2026-10-23 FAZ B TAMAMLANDI]):** (b) + (c) canlıda, (a) ERTELENDİ ·
  `settings.local.json`'dan 52 sırlı kural silindi (anahtarın 16 kopyası dahil; anahtar iptali ertelendi) · LIFFY DB
  kullanıcısı değişti → yukarıdaki döküm satırındaki dize geçersiz · b4'te otomatik çıkış YOK (Paket 3 notu) · K4 ihlal #3
  [defter:2026-10-23 K4 İHLAL #3].
