# ELL — Belge/Gerçeklik Mutabakat Ölçümü (2026-07-21)

**Kapsam:** `ELL_DURUM_DEFTERI_v2.md` iddiaları vs canlı gerçeklik.
**Yöntem:** Tamamen read-only. Hiçbir INSERT/UPDATE/DELETE/DDL, migration, deploy yapılmadı.
Tüm DB ölçümleri `BEGIN READ ONLY` transaction içinde; LEENA `claude_readonly` kullanıcısıyla.
**Durum:** Faz 3a öncesi karar girdisi.

**Ölçüm turları:** 1. tur (sabah) — LEENA DB IP whitelist nedeniyle erişilemedi, A1-A4 boş kaldı.
**2. tur (öğleden sonra) — IP eklendikten sonra A1-A4 tamamlandı; S2 kapandı.**

---

## 🔴 ÖNCE BUNU OKU — ölçüm sırasında çıkan, göreve dahil olmayan bulgu

**Dört repo da GitHub'da PUBLIC ve içlerinde canlı production kimlik bilgileri var.**

Kanıt (`gh repo view`, 2026-07-21):

| Repo | Görünürlük | İçerdiği sır | Kanıt |
|---|---|---|---|
| `Nsueray/ell-docs` | **PUBLIC** | LEENA DB şifresi | `leena/CLAUDE.md:85` (HEAD'de) |
| `Nsueray/ell-docs` | **PUBLIC** | LIFFY DB şifresi | `liffy/CLAUDE_QUICKSTART.md:56` (HEAD'de) |
| `Nsueray/Leena_v401_monorepo` | **PUBLIC** | PGPASSWORD + JWT_SECRET + SENDGRID_API_KEY | 3 adet commit'li `.env.backup` |
| `Nsueray/liffyv1` | **PUBLIC** | — (env commit'li değil) | — |
| `Nsueray/eliza` | **PUBLIC** | — (env commit'li değil) | — |

Commit'li `.env.backup` dosyaları:
`backend/leena-v401-backend/.env.backup`, `backend/leena-v401-backend-OLD/.env.backup`,
`backend/leena-v401-backend-backup/.env.backup`

**Bu ölçümün kendisi bulgunun kanıtı:** LIFFY DB'sine, sadece public `ell-docs` reposundaki
şifreyle bağlanabildim. Bağlantı için hiçbir özel erişimim gerekmedi.

**Sonuç:** Her iki DB şifresi ve LEENA JWT_SECRET'ı yayında kabul edilmeli. JWT_SECRET
sızıntısı, LEENA için geçerli token üretilebilmesi anlamına gelir — `POST /api/contracts/convert`
dahil tüm authMiddleware korumalı endpoint'ler etkilenir. Ölçüm read-only olduğu için hiçbir şey
döndürülmedi/rotate edilmedi.

> **🔴 bulgu kabul edildi; repolar private yapılıyor, şifre rotasyonu birleşme güvenlik paketine
> eklendi (Suer kararı 2026-07-21).** `ell-docs` private yapıldı; diğer repolar sırada. Şifreler
> sızmış durumda kaldığı için rotasyona kadar geçerli risk sürüyor — private yapmak geçmiş
> klonları ve olası kopyaları geri almaz.

---

## 1) MUTABIK — defter iddiası ölçümle doğrulandı

| # | Defter iddiası | Kanıt |
|---|---|---|
| B6 | Convert endpoint `routes/contracts.js`'te | `routes/contracts.js:64` `router.post('/convert', authMiddleware, ...)` |
| B6 | partners.js atomik tx deseni birebir | `contracts.js:88-135`: `pool.connect()` → `BEGIN`(90) → `COMMIT`(125) → `ROLLBACK`(128) → `finally client.release()`(133-135). Desen kaynağı `partners.js:61-70` ile aynı |
| B6 | 409 idempotency kodda | `contracts.js:31-37` — `err.code==='23505'` + `err.constraint==='idx_contracts_source_quote_id'` → 409 |
| B6 | 401 auth kodda | `contracts.js:64` authMiddleware; `middleware/authMiddleware.js:10` `return res.sendStatus(401)` |
| B6 | 400 guard'ları | `contracts.js:73-83` — quote_id / af_number zorunlu, `status!=='signed'` → 400 |
| B6 | Payload-driven, cross-system fetch yok | `contracts.js:92-123` tek INSERT, dış çağrı yok |
| B6 | Bu dilimde NULL: expo_id, sales_agent_id, audit | `contracts.js:121` yorumu + INSERT kolon listesinde yoklar |
| B7 | Endpoint canlıya deploy edilmiş | `POST https://leena.app/api/contracts/convert` (auth'suz) → **HTTP 401 "Unauthorized"**. Kontrol: `/api/contracts/zzz-yok` → **404**. 401≠404 ayrımı rotanın mount'lu olduğunu kanıtlar (`index.js:134`) |
| B8 | Quotes CRUD yerinde | `liffyv1/backend/routes/quotes.js` — POST `/`(428), GET `/`(579), GET `/:id`(657), PUT `/:id`(689), DELETE `/:id`(771), items CRUD (825/885/932) |
| B8 | Status geçişleri yerinde | `quotes.js:963` send (draft→sent), `:992` decline (sent→declined), `:1021` sign (sent→signed, TERMINAL) |
| B8 | Sign'da scan zorunlu | `quotes.js:1036-1038` — `signed_scan_url` yoksa 400; `:1039-1041` `signed_at` yoksa 400 |
| C9 | prospects ~26.123 | **26.123** — birebir tutuyor |
| C10 | ATR-100000 + QMA-100001 fixture'ları duruyor | ATR-100000 = signed, scan var, 2026-06-12; QMA-100001 = sent. Toplam 2 quote, 1'i signed |
| D11 | convert-core deploy EDİLMEDİ | `eliza` origin/main son commit `cdd8a26` (2026-06-19 11:01). `c2d5621` (convert-core) **main'de değil** (`git merge-base --is-ancestor` → HAYIR). Commit mesajı da "(branch, not deployed)" diyor |
| D11 | eliza'ya en son 19 Haz'da dokunulmuş | Son commit `2026-06-19 13:30:23`; GitHub son push `2026-06-19T10:30:38Z`. 19 Haziran'dan sonra aktivite yok |
| D11 | 026/027/028 mevcut | `eliza/packages/db/migrations/026_convert_slice1_sales_agents.sql`, `027_convert_source_quote_unique.sql`, `028_convert_audit_integer.sql` |
| **A1** | **Migration 012 DB'de UYGULANMIŞ** | `contracts` + `sales_agents` tabloları `information_schema.tables`'ta mevcut (2. tur ölçümü) |
| A1 | contracts integer SERIAL PK | `id integer NOT NULL DEFAULT nextval('contracts_id_seq')`, `contracts_pkey PRIMARY KEY (id)` |
| A1 | frozen-EUR 4 alanı mevcut | `revenue numeric(14,2)`, `currency text`, `exchange_rate numeric(18,8)`, `revenue_eur numeric(14,2)` |
| A1 | `source_quote_id` partial UNIQUE index | `CREATE UNIQUE INDEX idx_contracts_source_quote_id ON contracts (source_quote_id) WHERE (source_quote_id IS NOT NULL)` — **adı `contracts.js:33`'ün beklediğiyle birebir aynı**, 409 yolu gerçekten çalışır |
| A1 | `expos(id)` gerçek FK | `contracts_expo_id_fkey FOREIGN KEY (expo_id) REFERENCES expos(id)`; `expos.id` = integer (tip uyumu tam, ELIZA UUID↔integer çıkmazı yok) |
| A1 | LIFFY soft-ref'ler UUID, FK'siz | `source_quote_id`/`sales_owner_user_id`/`company_id` = uuid, üzerlerinde FK yok |
| A1 | status DEFAULT 'Active', Draft yok | `status text NOT NULL DEFAULT 'Active'::text`; CHECK'te `Draft` yok |
| A1 | `sales_agents` agent_type CHECK | `CHECK (agent_type = ANY (ARRAY['internal','external_agency','external_freelance']))` |
| A1 | `sales_agent_id` kolonu şimdi, doldurma sonra | `sales_agent_id integer` + `contracts_sales_agent_id_fkey → sales_agents(id)`; tüm satırlarda NULL |
| A1 | Audit kolonları iki tipli | `created_by integer`, `converted_by uuid`, `converted_at timestamptz` — hepsi NULL |
| A2 | contracts = 1 satır, test kaydı id=1 duruyor | `SELECT count(*) FROM contracts` → **1**; id=1, status=`Active`, `created_at 2026-06-20 18:07:09+00` |
| A2 | Para no-recompute taşınmış | id=1: revenue `15000.00` USD, exchange_rate `0.92000000`, revenue_eur `13800.00` (15000×0.92=13800 ✓) |
| A2 | Bu dilimde NULL olanlar gerçekten NULL | id=1'de `expo_id`, `sales_agent_id`, `created_by`, `converted_by`, `converted_at` = NULL |
| A4 | expos test kayıtları duruyor | Toplam **16** expo. `id=11` `[TEST] Reactivation Smoke Test Expo`, `id=15` `test`, `id=16` `test` (ikisi 2026-06-18) — üçü de yerinde |
| A4 | Ghana kayıtları duruyor | `id=2` Mega Clima Ghana, `id=4` Mega Clima Ghana 2026 (Test), `id=5` Mega Clima Ghana 2026, `id=6` Ghana Mega Water 2026 |

---

## 2) SAPMA — defter ile gerçek farklı VEYA ölçülemedi

### S1 — Migration 012 dosyası hiç commit edilmemiş, diskte de yok
- **Beklenen:** Defter (satır 23): *"Migration 012 (`012_finance_foundation.sql`) CANLIDA … Son migration 011 → 012"*
- **Bulunan:** `backend/leena-v401-backend/migrations/` içinde **en son dosya `011_seed_reference_data.sql`**. `012*` diye bir dosya yok. Git geçmişinde de yok: `git log --all -- '*012*'` → boş. Convert commit'i `c870c1e` sadece 2 dosya değiştirmiş: `index.js` (+3) ve `routes/contracts.js` (+138) — **migration SQL içermiyor**.
- **Yorum:** SQL Render Shell'den elle çalıştırıldı (belgelenen iş akışı: *"Migrations executed by Suer manually"*, `leena/CLAUDE.md:101`). 2. tur ölçümü **şemanın DB'de gerçekten var olduğunu doğruladı** (bkz. MUTABIK/A1) — yani migration çalışmış, sadece **dosyası versiyon kontrolüne hiç girmemiş.**
- **Ek kanıt (2. tur):** DB'de `schema_migrations` benzeri bir migration kayıt tablosu **yok** (`information_schema.tables`'ta `%migration%` / `%schema_version%` → 0 satır). Yani 012'nin uygulandığına dair ne repoda dosya ne DB'de kayıt var — **tek kanıt tabloların kendisi.** Bu, 000-011 için de geçerli bir yapısal boşluk: migration'ların hangisinin uygulandığı hiçbir yerde izlenmiyor.
- **Faz 3a'yı bloke eder mi:** **EVET (tek kalan blokaj).** Faz 3b `sales_agent_id` doldurmayı, Faz 4 audit kolonlarını gerektiriyor; ikisi de 012'nin kurduğu şemaya yazacak. Şema artık **ölçüldü ve biliniyor** (aşağıdaki Ek A), ama koda yazılı değil — 013 yazmadan önce 012 dosyalanmalı, yoksa sıfırdan kurulacak her ortam (staging, yeni geliştirici) 011'de kalır.

### S2 — LEENA DB ölçülemedi ✅ **KAPANDI (2. tur)**
- **1. turda:** `psql "$RENDER_DATABASE_READONLY_URL"` → `SSL connection has been closed unexpectedly` (3 deneme) — `leena/CLAUDE.md:105`'te belgelenen IP whitelist hatası.
- **Çözüm:** Suer, `78.168.189.35` IP'sini Render Inbound IP Rules'a ekledi (2026-07-21).
- **2. tur sonucu:** `claude_readonly` ile bağlantı kuruldu (`SELECT current_user, current_database()` → `claude_readonly|leena_v401_db`). **A1, A2, A3, A4'ün tamamı ölçüldü.** Sonuçlar MUTABIK tablosunda ve S7/S8/S9'da.
- **Faz 3a'yı bloke eder mi:** **HAYIR — kapandı.**

### S3 — LIFFY sayılarında sapma (küçük ama açıklanmamış)
- **Beklenen:** persons ~80.659, affiliations ~90.722
- **Bulunan:** persons **80.855** (+196), affiliations **90.841** (+119), prospects 26.123 (sapma yok)
- **Yorum:** Yön yukarı ve oran küçük (%0,24 ve %0,13). Mining/import aktivitesiyle uyumlu görünüyor; ama defterdeki sayının hangi tarihe ait olduğu belgede yazmadığı için **artışın kaynağını kanıtlayamadım.** LIFFY'nin "dormant" olduğu varsayımıyla çelişip çelişmediği bu ölçümden çıkmıyor.
- **Faz 3a'yı bloke eder mi:** **HAYIR.** Sapma küçük ve convert yoluna değmiyor.

### S4 — LIFFY hâlâ expo/office/exchange-rate yazabiliyor (kilit belgesiyle çelişki)
- **Beklenen:** `decisions/ELL_TEK_KAYNAK_KILIT.md` §2: *"Expo → LEENA. LIFFY artık bağımsız expo YARATAMAZ — read-only synced görür"*; Currency ve Office owner'ı da LEENA.
- **Bulunan:** LIFFY backend'de yazma endpoint'leri **canlı ve açık**: `quotes.js:231` `POST /expos`, `:251` `PUT /expos/:id`, `:276` `DELETE /expos/:id`, `:172` `PUT /exchange-rates/:currency`, `:136` `PATCH /users/:userId/office`. LIFFY DB'de veri de duruyor: expos=1, offices=7, exchange_rates=1.
- **Yorum:** Kilit belgesi 2026-06-20'de kilitlendi; LIFFY kodu 2026-06-12'den beri dokunulmamış (son push `2026-06-12T11:46Z`). Yani bu bir gerileme değil — **ilke kilitlendi, kod henüz uyarlanmadı.** Defter bu boşluğu "SIRADAKİ/ertelendi" olarak da kaydetmemiş.
- **Faz 3a'yı bloke eder mi:** **HAYIR** (Faz 3a LEENA-içi), ama **Convert-1 için doğrudan önkoşul** — expo bağlama tasarımı LIFFY'nin expo'yu nasıl sahiplendiğine bağlı ve bugünkü cevap "bağımsız yaratabiliyor".

### S5 — LEENA working tree'de 20 takipsiz dosya
- **Bulunan:** `Leena_v401_monorepo` main branch, 20 takipsiz dosya (analiz/rapor .md'leri + `cleanup-day12-commit.sql`, `cleanup-day12-dryrun.sql`). Değiştirilmiş dosya yok, origin ile eşit (`0 0`).
- **`eliza`:** **`convert-core` branch'inde duruyor** (main'de değil) — 1 değişmiş + 1 takipsiz dosya.
- **`liffyv1`:** main, 1 takipsiz dosya. Temiz sayılır.
- **Faz 3a'yı bloke eder mi:** **HAYIR.** Ama `eliza`'nın retired bir branch'te bırakılmış olması, yanlışlıkla o bağlamda çalışma riski taşıyor.

### S6 — Defterin "5-status CHECK" ifadesi yanlış; gerçek 4 ✅ **ÇÖZÜLDÜ (2. tur)**
- **Beklenen:** Defter (satır 27): *"5-status CHECK (`Active`/`On Hold`/`Transferred`/`Cancelled`, default `Active`)"* — cümlenin kendisi "5" diyip **4** eleman sayıyor.
- **Bulunan (DB):** `contracts_status_check` → `CHECK (status = ANY (ARRAY['Active','On Hold','Transferred','Cancelled']))` — **4 eleman.** `contracts.js:27`'deki `CONTRACT_STATUSES` da 4 eleman. **Kod ve DB uyumlu; yanlış olan defterin "5" ifadesi.**
- **Kalan kusur:** `CONTRACT_STATUSES` sabiti `contracts.js`'te tanımlı ama hiç kullanılmıyor (ölü kod); INSERT `'Active'`'i `:117`'de sabit yazıyor.
- **Faz 3a'yı bloke eder mi:** **HAYIR.** Defterdeki "5" tek kelimelik bir düzeltme; ölü kod kozmetik.

### S7 — `sales_agents` locked B3 hedef şeması DEĞİL (2. tur bulgusu)
- **Beklenen (soru A3):** locked B3 = UUID PK + `organization_id` + `user_id` nullable **UNIQUE** + `agent_type`
- **Bulunan (DB):** `id integer` SERIAL PK · `organizer_id integer NOT NULL` · `name text NOT NULL` · `agent_type text NOT NULL` (CHECK ✓) · `user_id integer` nullable · `created_by integer` · `created_at`/`updated_at`. **Satır sayısı: 0.**
  - **UUID değil, integer SERIAL.**
  - **`organization_id` kolonu YOK** — yerine `organizer_id integer` var (LEENA'nın mevcut organizer deseni).
  - **`user_id` üzerinde UNIQUE YOK** — tablodaki tek unique constraint `sales_agents_pkey`.
  - `user_id` tipi **integer** (locked B3'te UUID bekleniyordu).
- **Yorum:** Bu bir gerileme değil — defterin kendi 2026-06-20 bloğu (satır 34-36) `sales_agents`'ı zaten *"integer SERIAL PK … user_id nullable"* diye tarif ediyor, yani **012 ne yaptıysa defter onu doğru yazmış.** Çelişki defterle değil, **locked B2/B3 hedef şemasıyla**: defterin ilerideki satırları (≈1213) locked hedefi *"UUID PK + organization_id"* diye anlatıyor ve o tanım ELIZA Slice 1'e (retired) aitti. **LEENA'da kurulan tablo locked hedeften farklı ve bu fark hiçbir yerde karar olarak kaydedilmemiş.**
- **Faz 3a'yı bloke eder mi:** **HAYIR** (Faz 3a'nın kendisi bu tabloya yazmıyor), ama **Faz 3b'nin (sales_agent doldurma) doğrudan önkoşulu**: doldurmadan önce "hedef şema integer mi UUID mi" kararı verilmeli. Bugün kod ve DB integer; locked belge UUID diyor. **Bu ikisi aynı anda doğru olamaz.**

### S8 — Test kaydı id=1 gerçek LIFFY quote'undan değil, sentetik veriyle üretilmiş (2. tur bulgusu)
- **Beklenen:** Defter (satır 46-47): *"mutlu yol → 201 (id:1, status=Active, para no-recompute taşındı, source_quote_id dolu)"* — LIFFY signed quote → LEENA contract akışının kanıtı gibi okunuyor.
- **Bulunan:** LEENA `contracts` id=1 → `source_quote_id = 11111111-1111-1111-1111-111111111111`, `af_number = A-2026-001`, `company_name = Acme Fuarcilik`, revenue 15000 USD.
  LIFFY'deki **gerçek** signed quote → `id = 99482f19-ac2b-441f-9782-642e2d61a4ad`, af_number `ATR-100000`, company `Halden Nigeria Limited`.
- **Yorum:** Kayıt uydurma bir UUID ve uydurma şirket adıyla oluşturulmuş. **Endpoint'in kendisi doğru çalışıyor** (201/409/400/401 senaryoları geçerli, MUTABIK'ta) — ama **LIFFY→LEENA uçtan uca yolu gerçek quote verisiyle hiç denenmemiş.** Defter bunu "sentetik payload" diye ayırt etmiyor; okuyan kişi entegrasyonun kanıtlandığını sanabilir.
- **Faz 3a'yı bloke eder mi:** **HAYIR**, ama Convert-1 kabul kriterine yazılmalı: gerçek `ATR-100000` payload'ıyla bir convert denemesi (bugün `expo_id` NULL kaldığı için zaten eksik kalır).

### S9 — Migration takip tablosu yok (2. tur bulgusu)
- **Bulunan:** LEENA DB'de `schema_migrations` / `%migration%` / `%schema_version%` adlı hiçbir tablo yok (0 satır).
- **Yorum:** Hangi migration'ın uygulandığı ne repoda ne DB'de izleniyor. S1'in tekil bir hata değil, **yapısal bir boşluğun belirtisi** olduğunu gösteriyor: 012 sessizce kaybolabildi çünkü onu yakalayacak bir mekanizma yok.
- **Faz 3a'yı bloke eder mi:** **HAYIR**, ama 013 yazılırken takip tablosu eklemek ucuz ve aynı hatayı tekrar etmeyi önler.

---

## Ölçülemeyenler (özet)

| Madde | Neden |
|---|---|
| ~~A1-A4~~ | ✅ 2. turda ölçüldü (IP eklendi) |
| D11 Render'da hangi branch canlı | `eliza` reposunda `render.yaml` yok; deploy branch'i Render Dashboard'da. Kod/config'den çıkmıyor. **Dolaylı kanıt:** convert-core main'e merge edilmemiş (`git merge-base --is-ancestor` → HAYIR) |
| S3'teki artışın kaynağı | Defterdeki LIFFY sayılarının hangi tarihe ait olduğu belgede yazmıyor; artış mining/import mı başka bir şey mi ayırt edilemedi |

---

## FAZ 3A HAZIRLIK DEĞERLENDİRMESİ

### Bloke eden: 1 madde kaldı

**S1 — `012_finance_foundation.sql` versiyon kontrolünde yok.**
Şema artık **ölçüldü ve tam olarak biliniyor** (Ek A), ama repoda dosyası yok ve DB'de de
uygulandığına dair kayıt yok (S9). Bu haliyle:
- sıfırdan kurulacak her ortam (staging, yeni geliştirici makinesi) `011`'de kalır — `contracts`
  ve `sales_agents` oluşmaz, `routes/contracts.js` ilk çağrıda patlar;
- 013 yazan kişinin dayanacağı yazılı bir şema yoktur.

**Bloke etmeyen ama Faz 3a/3b'yi doğrudan etkileyen 2 açık karar:**
- **S7** — `sales_agents` integer SERIAL (canlı) vs locked B2/B3 UUID (belge). Faz 3b
  `sales_agent_id`'yi doldurmadan önce hangisinin hedef olduğu kararlaştırılmalı.
- **S4** — LIFFY hâlâ bağımsız expo/office/exchange-rate yazabiliyor; Convert-1'in (expo bağlama)
  tasarımı buna bağlı.

### İlk yapılacak iş

**012'nin DDL'ini canlı DB'den çıkarıp `backend/leena-v401-backend/migrations/012_finance_foundation.sql`
olarak repoya yaz.**

⚠️ **`pg_dump` bu makinede çalışmıyor:** yerel istemci 14.20 (Homebrew), sunucu 17.9 →
`aborting because of server version mismatch`. İki seçenek:
- **(a)** PG17 istemcisi kur (`brew install postgresql@17`), sonra:
  `pg_dump "$RENDER_DATABASE_READONLY_URL" --schema-only --no-owner --no-privileges -t public.contracts -t public.sales_agents`
- **(b)** Kurulum beklemeden **Ek A'daki DDL'i kullan** — bu ölçümün katalog sorgularından
  (`information_schema.columns`, `pg_constraint`, `pg_indexes`) birebir yeniden kuruldu.

Sonra sırasıyla: S9 için basit bir `schema_migrations` tablosu (013 ile birlikte, ucuz) →
S7 kararı (integer mi UUID mi) → Faz 3a migration'ı.

**Faz 3a'ya bugün başlanabilir mi:** 012 dosyalandıktan sonra **evet.** Şema doğrulandı,
endpoint canlı ve çalışıyor, idempotency index'i gerçekten yerinde. Kalan blokaj tek ve
mekanik.

---

## Ek A — 012 şeması (canlı DB'den yeniden kuruldu, 2026-07-21)

> Bu DDL `pg_dump` çıktısı **değildir** — sürüm uyuşmazlığı nedeniyle katalog sorgularından
> yeniden kuruldu. Kolonlar, tipler, NOT NULL/DEFAULT, CHECK, FK ve index tanımları ölçümle
> birebir eşleşir. Orijinal 012 dosyasının yorumlarını ve olası `IF NOT EXISTS` sarmalayıcılarını
> içermez. Repoya almadan önce gözden geçirin.

```sql
CREATE TABLE contracts (
  id                  integer      NOT NULL DEFAULT nextval('contracts_id_seq'::regclass),
  organizer_id        integer      NOT NULL,
  expo_id             integer,
  af_number           text,
  company_name        text,
  contract_date       date,
  revenue             numeric(14,2),
  currency            text,
  exchange_rate       numeric(18,8),
  revenue_eur         numeric(14,2),
  status              text         NOT NULL DEFAULT 'Active'::text,
  source_quote_id     uuid,
  sales_owner_user_id uuid,
  company_id          uuid,
  sales_agent_id      integer,
  created_by          integer,
  converted_by        uuid,
  converted_at        timestamptz,
  created_at          timestamptz  NOT NULL DEFAULT now(),
  updated_at          timestamptz  NOT NULL DEFAULT now(),
  CONSTRAINT contracts_pkey PRIMARY KEY (id),
  CONSTRAINT contracts_status_check CHECK (status = ANY (ARRAY['Active','On Hold','Transferred','Cancelled'])),
  CONSTRAINT contracts_expo_id_fkey FOREIGN KEY (expo_id) REFERENCES expos(id),
  CONSTRAINT contracts_sales_agent_id_fkey FOREIGN KEY (sales_agent_id) REFERENCES sales_agents(id)
);

CREATE INDEX idx_contracts_expo_id      ON contracts USING btree (expo_id);
CREATE INDEX idx_contracts_organizer_id ON contracts USING btree (organizer_id);
-- idempotency anahtarı: contracts.js:33 bu index ADINI bekler
CREATE UNIQUE INDEX idx_contracts_source_quote_id
  ON contracts USING btree (source_quote_id) WHERE (source_quote_id IS NOT NULL);

CREATE TABLE sales_agents (
  id           integer     NOT NULL DEFAULT nextval('sales_agents_id_seq'::regclass),
  organizer_id integer     NOT NULL,
  name         text        NOT NULL,
  agent_type   text        NOT NULL,
  user_id      integer,
  created_by   integer,
  created_at   timestamptz NOT NULL DEFAULT now(),
  updated_at   timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT sales_agents_pkey PRIMARY KEY (id),
  CONSTRAINT sales_agents_agent_type_check CHECK (agent_type = ANY (ARRAY['internal','external_agency','external_freelance']))
);

CREATE INDEX idx_sales_agents_organizer_id ON sales_agents USING btree (organizer_id);
```

**Not:** İki tabloda da trigger yok (`updated_at` otomatik güncellenmiyor — uygulama katmanının
sorumluluğu). `sales_agents.user_id` üzerinde UNIQUE constraint yok (locked B3 bunu bekliyordu — S7).
