# ELL — Durum Defteri (Tek Yaşayan Belge) — v2

> ## 🔴 2026-06-19 — MİMARİ KARAR DEĞİŞİKLİĞİ (HER ŞEYDEN ÖNCE OKU)
>
> **ELIZA ayrı sistem/database olarak terk edildi.** Eski ELIZA backend/DB disposable Zoho
> mirror + raporlama prototipidir; verisi LEENA'ya migrate edilmeyecek. `eliza_73du` üstündeki
> convert çalışması (migration 026/027/028 + POST /api/contracts/convert) **legacy/retired**
> kabul edilir, **deploy edilmeyecek**.
> - **LIFFY** = dış halka / satış / freelancer izolasyonu. Ayrı DB + ayrı servis.
> - **LEENA** = iç halka / operations + **finance + contracts + payments + commissions + ledger + reporting**.
> - **ELIZA** = kullanıcıya görünen ürün / **Finance tab** / brand adı; fiziksel backend/DB **DEĞİL**.
> - **Tek cross-DB sınır: LIFFY ↔ LEENA.** ELIZA↔LEENA bridge yoktur.
> - Convert core **LEENA'da yeniden kurulacak**; `contract.expo_id` → **LEENA canonical `expos.id` gerçek FK**.
> - Tarihsel Zoho expo/contract migration ileride **Zoho → LEENA** kapsamında ele alınacak (eski ELIZA mirror değil).
>
> *(Bu yaşayan defterde aşağıdaki bazı eski kayıtlar bu karara aykırıdır; SİLİNMEDİ, **SUPERSEDED**
> işaretlendi ve yeni karara göre düzeltildi. Çelişki görürsen bu blok kazanır.)*

> ## ✅ 2026-06-20 — LEENA FİNANS ÇEKİRDEĞİ CANLIDA (012 + CONVERT)
>
> 2026-06-19 kararı **inşa edildi ve CANLI**. Artık "yeniden kurulacak" değil — **kuruldu**:
>
> **1. Migration 012 (`012_finance_foundation.sql`) CANLIDA** (leena_v401_db). Dry-run
> (ROLLBACK) → COMMIT, `\d contracts` doğrulandı. İki yeni tablo, tamamen additive — canlı
> LEENA operasyonu (visitor/badge/check-in/floor plan) ETKİLENMEDİ. Son migration **011 → 012**.
> - **`contracts`**: integer SERIAL PK; `expo_id` integer **nullable FK → expos(id)** (aynı-DB
>   GERÇEK FK — 2026-06-19 kararının ödülü somut, ELIZA UUID↔integer çıkmazı YOK); 4-status (Draft yok) CHECK
>   (`Active`/`On Hold`/`Transferred`/`Cancelled`, default `Active` — **'Draft' bilinçli DIŞARIDA**:
>   contract signed quote'tan doğar, doğduğu an Active); para 4 alan (`revenue`/`currency`/
>   `exchange_rate`/`revenue_eur` — frozen-EUR, bilgi kaybını önler); LIFFY soft-ref'ler UUID
>   nullable FK'siz (`source_quote_id`/`sales_owner_user_id`/`company_id` — 028 dersi: kaynak
>   sistemin tipinde); `sales_agent_id` integer nullable FK (kolon şimdi, doldurma Faz 3b — 027/028
>   dersi: ikinci ALTER'dan kaçın); audit nullable FK'siz (`created_by` integer / `converted_by`
>   uuid — bilinçli iki tip, iki kaynak; Faz 4 kimlik); `source_quote_id` partial UNIQUE index.
> - **`sales_agents`**: integer SERIAL PK; `agent_type` CHECK (`internal`/`external_agency`/
>   `external_freelance`); `user_id` nullable (çoğu agent login değil); audit nullable.
>
> **2. Convert endpoint (Slice 2) CANLIDA** — `routes/contracts.js`, `POST /api/contracts/convert`,
> partners.js deseni (express.Router, pool.connect/BEGIN atomik tx, mapWriteError 23505). **4 senaryo
> test geçti** (leena.app): mutlu yol → 201 (id:1, status=Active, para no-recompute taşındı,
> source_quote_id dolu); idempotency → 409 (partial unique çalıştı, ikinci contract YOK — 027 dersi
> canlı doğrulandı); guard status≠signed → 400; auth token yok → 401. **Payload-driven** (cross-system
> fetch YOK — transport LIFFY aktivasyonuna ertelendi; convert eden quote verisini body'de gönderir).
> Bu dilimde NULL: `expo_id` (Convert-1), `sales_agent_id` (Faz 3b), audit (Faz 4).
> - **Auth kararı (A):** role-gate Faz 4'e ertelendi (LEENA JWT'sinde role YOK — ölçümle doğrulandı,
>   authMiddleware sadece organizer_id veriyor). **Güvenlik açığı DEĞİL, sıralama:** yetki sistemi
>   PLANLI+kilitli (B21-B42 user_permissions matrisi), Faz 4'te users+roller ile kurulur. Bugün
>   organizer-scope + geçerli JWT + idempotency yeterli (single-tenant, sadece iç ekip, dışarıdan
>   kimse LEENA'da değil). Endpoint'te yer işareti yorumu var: `// FAZ 4: convert-permission buraya`.
>
> **3. Eski ELIZA convert-core → RETIRED EXPERIMENT** (kayıt). `eliza_73du` üstündeki 026/027/028 +
> `convert-core` branch + `POST /api/contracts/convert` **deploy EDİLMEYECEK, LEENA'ya birebir port
> EDİLMEYECEK**. Sadece DERSLERİ referans alındı (alan eşleme, idempotency, atomik tx, audit/028,
> 8 test senaryosu) — ve bu derslerle LEENA-native sıfırdan yazıldı (yukarıda). 3-DB yönünün ürünü.
>
> **2026-07-21 amendment — SIRADAKİ değişti:** Aşağıdaki "SIRADAKİ" maddesi artık geçerli
> değil. **Convert-1 (expo bağlama + transport + review-queue UI) bilinçli olarak LIFFY
> aktivasyonuna ertelendi** — sıradaki iş değil, bekleyen iş. Altındaki açık karar (UUID↔integer
> eşleme) ve LIFFY ölçümü ihtiyacı geçerliliğini koruyor, sadece zamanlaması LIFFY aktivasyonuna
> bağlandı. (012 + convert endpoint durumu değişmedi: canlıda.)
>
> **2026-07-21 mutabakat ölçümü sonrası eklenen notlar** (kanıt:
> `ELL_MUTABAKAT_2026-07-21.md`):
>
> - **S7 KAPANDI (2026-07-21):** integer kalır, B3 v1.1 amend edildi, invariant'lar 014 ile
>   dosyalandı. Faz 4 geldiğinde tip kararı kuyruktan düşecek.
>   *(Hüküm: Mimari + Sentez onaylı, kilitli. Fiziksel tip barındıran sistemin native tipini
>   izler — LEENA döneminde integer SERIAL. Kilitli semantik invariant'lar: agent_type üçlüsü;
>   `user_id` nullable + UNIQUE; CHECK internal→`user_id` NOT NULL, external→NULL; bir user en
>   fazla bir agent. Migration: `014_sales_agents_invariants.sql`.)*
> - **Convert-1 kabul kriteri:** gerçek ATR-100000 payload'ıyla uçtan uca convert (bugüne
>   kadarki tek test sentetik veriydi — LEENA contract id=1'in `source_quote_id`'si
>   `1111...1111`, gerçek LIFFY quote'u değil).
> - **Convert-1 önkoşulu:** LIFFY'nin expo/office/exchange-rate yazma endpoint'leri
>   kapatılacak/read-only'ye çevrilecek (tek-kaynak kilidi gereği; kod henüz uyarlanmadı).
>
> **SIRADAKİ (2026-06-20 — bkz. üstteki amendment):** Convert-1 (expo bağlama) — açık karar: LIFFY quote expo'yu nasıl seçiyor (UUID),
> LEENA canonical expo (integer) ile nasıl eşleşecek? **LIFFY ölçümü gerekiyor** (2026-06-20 başladı).
> İki yol: (a) quote oluşturulurken LEENA expo_id zaten seçili → payload doğrudan taşır (köprü yok);
> (b) convert anında UUID→integer eşleme (köprü kurulur). Ölçüm bunu KANITLAYACAK. Sonraki dilimler:
> sales_agent doldurma (Faz 3b), audit (Faz 4), transport (LIFFY aktivasyonu). **Test contract id:1
> canlıda duruyor — demo/temizlikte silinecek** (silinirse SERIAL 2'den devam eder).

> ## ✅ 2026-07-21 — MUTABAKAT PARANTEZİ KAPANDI
>
> Ölçüm raporu: `ELL_MUTABAKAT_2026-07-21.md`.
>
> **Sonuçlar:** S1 kapandı (012 dosyalandı, 013 schema_migrations + 014 invariants canlıda),
> S2 kapandı (IP), S6 düzeltildi (4-status), S7 KAPANDI (integer kalır, B3 v1.1 amend),
> S9 kapandı (takip tablosu canlıda).
>
> **Kuyruğa taşınan:** S3 (LIFFY sayı artışı kaynağı belirsiz), S4 (LIFFY yazma endpoint'leri
> → Convert-1 önkoşulu), S8 (gerçek ATR-100000 E2E testi → Convert-1 kabul kriteri),
> güvenlik rotasyonu (birleşme paketi).
>
> **015 normalize canlıda; takip tablosu tam dosya adlarıyla, 000a dahil, 17 kayıt.
> Faz 3a migration'ları 016'dan başlar.**
>
> **SIRADAKİ:** Faz 3a — contracts operasyonel kolonlar + payment-create + Finance liste UI.

> ## ✅ 2026-07-21 — FAZ 3a-1 TAMAM (contracts görünür)
>
> **Migration 016 canlıda:** 9 operasyonel kolon (`scan_link`, `stand_design_link`,
> `catalogue_page`, `stand_type`, `sqm`, `free_sqm`, `sales_group`, `transportation`,
> `transferred_from_contract_id`) + `contracts_transportation_check` +
> `contracts_no_self_transfer_check` + self-FK `contracts(id)`. `schema_migrations` **18 kayıt**.
>
> **Endpoint'ler canlı:** `GET /api/contracts` (liste, organizer scope, `?expo_id=`/`?status=`),
> `GET /api/contracts/:id` (detay, 31 alan), `PUT /api/contracts/:id/status` (4 durum arası
> serbest, geçiş matrisi yok). Commit'ler: `cfeeced`, `8e9baf6`, `040f10e`.
>
> **UI canlı:** `public/contract-list.html` + `main-panel-v2.html`'e "Finance" nav bölümü.
> **Görsel kontrol Suer tarafından GEÇTİ** (liste + nav ekran görüntülü).
>
> **Notlar:**
> 1. `no_self_transfer` yalnız A→A engeller; **A→B→A döngüsü Transfer aksiyonu diliminde
>    uygulama katmanında** çözülecek.
> 2. **Route sırası:** ileride `GET /contracts/convert` eklenirse `/:id`'den **ÖNCE**
>    tanımlanmalı (yoksa `:id='convert'` olarak yakalanır).
> 3. `CONTRACT_STATUSES` artık kullanılıyor — **S6 "ölü kod" kaydı düştü.**
> 4. `schema_migrations` 000/001/002 `applied_at` NULL — tarihsel, dokunulmadı.
> 5. **Komisyon dilimi ölçüm maddesi:** tekil `sales_agent_id` ↔ requirements üçlü modeli
>    (agent/sr/sd) reconcile edilecek + **LEENA'da `users` tablosu YOK** (kimlik Faz 4).
> 6. `contracts` id=1 (Acme, sentetik) **S8'e kadar kalır.**
> 7. Finance nav'ı **Yaprak'a da görünür**, sayfa **rol-kapısız** (Faz 4) — bilinçli kabul;
>    Suer Yaprak'ı sözlü bilgilendirecek.
> 8. `contracts` **`updated_at` trigger'sız** — UPDATE'lerde elle `NOW()` (expos deseni).
>
> **SIRADAKİ ADAYLAR (3a-2, karar Suer'de):** payment-create + computed paid/balance ·
> contract detay sayfası · Transfer aksiyonu.

> ## ✅ 2026-07-22 — FAZ 3a-2 TAMAM (ödeme girişi + hesaplanan paid/balance)
>
> **Migration 017 canlıda:** `payments` tablosu, **12 kolon**. Dry-run → ROLLBACK → COMMIT
> ritüeliyle uygulandı. `schema_migrations` kaydı **UZANTISIZ** (`017_payments`) — 015
> normalizasyonuna uyum. *(Ölçüm 2026-07-22: 12 kolon, kayıt `017_payments`
> `2026-07-22 08:17:19+00`, tabloda toplam 19 kayıt.)*
>
> **Endpoint'ler canlı:** `POST /api/contracts/:id/payments` + `GET /api/contracts/:id/payments`.
> `GET /api/contracts` (liste) ve `GET /api/contracts/:id` (detay) artık `paid_eur` +
> `balance_eur` döndürüyor (LEFT JOIN LATERAL, D2 — hiçbir yere yazılmaz). **37/37 test geçti.**
> Commit'ler: `270f3e8`, `c1c3543`, `d3d1989`.
>
> **UI canlı:** `contract-list.html` — Paid/Balance kolonları + satır altına açılan inline
> add-payment formu + currency select (EUR/USD/TRY/MAD/NGN/KES, default EUR + rate kilidi).
> Commit'ler: `f97c893`, `462de94`. Submit-sonrası reset hatası ("EUR ama kilit açık" hâli)
> yakalanıp düzeltildi.
>
> **GÖRSEL ONAY ALINDI (2026-07-22):** canlıda ilk ödeme girildi — contract id=1'e
> **100 USD × 0.9 → 90.00 EUR**; ekranda Paid `90.00 EUR` / Balance `13,710.00 EUR`
> doğrulandı. Server hata metni toast'ta aynen görünüyor (client-side doğrulama bilinçli yok).
>
> **Hesaplama:** `amount_eur = round2(amount × exchange_rate)` — **server hesaplar**,
> client'tan geleni yok sayar. `currency = EUR` ise `exchange_rate` 1.0 zorunlu (aksi hâlde 400).
>
> **KİLİTLİ KARARLAR (3a-2):**
> 1. `payment_method` CHECK listesi: `bank_transfer` / `cash` / `cheque` / `credit_card` / `other`.
> 2. `account_id` + `payer` bu dilimde **YOK** → **ledger fazında additive** eklenecek.
> 3. **`payments` immutable event:** `updated_at` yok, UPDATE/DELETE endpoint yok — düzeltme
>    akışı ledger fazının konusu.
> 4. **Contract status'u ödeme girişini KISITLAMAZ** — `Cancelled`'a da ödeme girilebilir
>    (bilinçli: geçmiş tahsilat her hâlükârda kaydedilebilmeli).
> 5. **Currency whitelist yalnız UI'da** (select: EUR/USD/TRY/MAD/NGN/KES — İstanbul merkez +
>    Fas/Nijerya/Kenya ofis birimleri). Server 3-harf format kontrolüyle kalır; ledger fazında
>    referans tabloya bağlanabilir.
> 6. **EUR dışına geçişte `exchange_rate` alanı BOŞALTILIR** (1 bırakılmaz): kuru güncellemeyi
>    unutmanın sessizce yanlış `amount_eur` üretmesi yerine görünür 400 hatası — bilinçli UX kararı.
> 7. **MODEL NOTU:** `payments` = Revenue record'un (req `:1002`) contract'a demirli minimal
>    öncüsü; ledger fazında evrim/bağlanma **iki yol da açık**.
>
> **FAZ 4 / İLERİYE NOTLAR:**
> 1. `payments.created_by` **NULL** yazılıyor (LEENA JWT'sinde user id yok) — `converted_by`
>    ile birlikte **Faz 4 identity işi**.
> 2. **Currency normalizasyon tutarsızlığı:** `payments` normalize ediyor (uppercase),
>    `convert` **etmiyor** → Faz 4'te convert'e de eklenecek (`contracts.js:337-339` yorumu).
> 3. `payment_date` **TZ davranışı** `contract_date` ile aynı (DATE → yerel TZ'li JS Date):
>    farklı TZ'de gün kayması olası — bilinen davranış, mevcut desen.
> 4. `schema_migrations`: `012_finance_foundation` kaydının `applied_at`'i **boş** (013 öncesi
>    geriye dönük kayıt) — tarihsel not.
>
> **CANLI VERİ NOTU:** `contracts` id=1 (Acme, sentetik) üzerinde **canlı test ödemesi var**
> (id=1: 100 USD × 0.9 = 90.00 EUR, `bank_transfer`, 2026-07-22). **S8 E2E'ye kadar contract'la
> birlikte kalır — SİLME.** *(2026-07-22 ölçümünde tabloda tek ödeme kaydı görüldü.)*
>
> **SIRADAKİ ADAYLAR (3a-3, karar Suer'de):** contract detay sayfası · Transfer aksiyonu ·
> payment schedule.

> ## ✅ 2026-07-22 — FAZ 3a-3 TAMAM (contract detay sayfası)
>
> **Migration GEREKMEDİ** — sıradaki numara **018** olarak duruyor (son kayıt `017_payments`).
> **Backend'e dokunulmadı:** ölçüm, `GET /api/contracts/:id`'nin zaten `c.*` (016'nın 9 kolonu
> dahil **33 alan**) + `expo_name` + `sales_agent_name` + `paid_eur`/`balance_eur` döndürdüğünü
> gösterdi — yeni endpoint'e gerek kalmadı.
>
> **`public/contract-detail.html` (YENİ) canlıda:** künye (status **PUT ile değiştirilebilir**) ·
> para özeti · 016 operasyonel alanları (link alanları **yalnız `http(s)` ise tıklanabilir** —
> `javascript:` koruması) · ödeme listesi · liste sayfasıyla **aynı** inline add-payment formu.
> İki fetch: `GET /:id` + `GET /:id/payments`.
>
> **`contract-list.html`:** satır tıklaması + **AF No linki** ile detaya geçiş
> (`contract-detail.html?id=N`, `expo-list.html:276` `openExpo` deseni). **Tıklama muafiyeti tek
> yerde hedef kontrolüyle** — buton/select/form/link satır navigasyonunu tetiklemez.
>
> **GÖRSEL ONAY ALINDI (2026-07-22):** satır→detay geçişi, tıklama muafiyeti, detaydan status
> değişiminin listeye yansıması, detaydan ödeme girişinin tablo + para özetini güncellemesi —
> hepsi ekranda doğrulandı.
>
> **Commit:** `ef0ff6f` (detay sayfası + navigasyon).
>
> **FAZ 4 / İLERİYE NOTLAR (3a-3 eki):**
> 1. `paid_eur`/`balance_eur` **iki endpoint'te iki farklı yolla** üretiliyor: detayda SQL
>    LATERAL (`contracts.js:196-206`), payments'ta JS aritmetiği (`:418-428`). Değer aynı;
>    **Faz 4 temizliğinde tek yönteme indirgenebilir.**
> 2. `transferred_from_contract_id` detayda **ham id** gösteriliyor (`af_number` join'i yok) —
>    Transfer dilimi geldiğinde join'lenecek.
>
> **SIRADAKİ ADAYLAR (3a-4, karar Suer'de):** ödeme düzeltme/reversal (**#1, ihtiyaç
> doğrulandı**) · Transfer aksiyonu · payment schedule.

> ## ✅ 2026-07-22 — FAZ 3a-4 TAMAM (ödeme düzeltme / reversal)
>
> **Migration 018 canlıda** (`018_payment_reversal`, dry-run → ROLLBACK → COMMIT ritüeliyle;
> kayıt **uzantısız**, `2026-07-22 10:52:45+00`):
> - `reverses_payment_id` integer **self-FK** `payments(id)`
> - `uq_payments_reverses_payment_id` **partial UNIQUE** (027 deseni — çifte-reversal engeli
>   DB seviyesinde, race-proof)
> - `payments_amount_check` **revizyonu**: normal kayıt `reverses NULL + amount > 0`;
>   reversal `reverses NOT NULL + amount < 0`. **Normal kayıt kuralı değişmedi** → mevcut POST
>   davranışı bozulmadı.
>
> **`POST /api/contracts/:id/payments/:paymentId/reverse` canlıda.** **32/32 backend + 10/10 UI
> testi** geçti. Hata yolları: **404** (contract / ödeme yok, başka contract'ın ödemesi) ·
> **400** (reversal-of-reversal) · **409** (çifte reversal — garanti partial UNIQUE'ten,
> constraint-map üzerinden).
>
> **`contract-detail.html`:** Reverse aksiyonu (native `confirm`) + **Reversed** /
> **Reversal of #N** rozetleri. `contract-list.html`'e **dokunulmadı** (Reverse yalnız detayda).
>
> **E2E KABUL GEÇTİ (2026-07-22)** — Suer senaryodan geniş test etti:
> - Her iki orijinal ödeme de terslendi (**doğru girilmiş USD dahil** → reversal genel çalışıyor,
>   yalnız hatalı kayda özgü değil).
> - **Tam-sıfır ara durum ekranda doğrulandı:** Paid `0.00` / Balance `13.800,00`.
> - Sonra doğru kurla `500 TRY × 0.0196` girildi → final **Paid 9.80 / Balance 13.790,20**,
>   detay **ve** listede doğrulandı.
> - İşaret çevrimi **kuruşu kuruşuna** (−90.00 / −25.500,00); rozet ve buton görünürlükleri doğru.
>
> **Commit'ler:** `41d45d7` (migration 018) + `c180295` (endpoint + UI).
>
> **KİLİTLİ KARARLAR (3a-4):**
> 1. **Reversal = storno.** Orijinal satır **immutable**; ters kayıt `currency` / `exchange_rate` /
>    `payment_method` / `amount_eur`'u **AYNEN kopyalar**, işaret çevrimi **SQL'de**
>    (`INSERT..SELECT`, `-amount` / `-amount_eur`). **`round2` çağrılmaz** — negatif yuvarlama
>    asimetrisi (`round2(-x) ≠ -round2(x)`) riski böylece hiç doğmaz.
> 2. `payment_date` = **reversal günü** (orijinalin tarihi değil) — "açık düzeltme + audit"
>    (req `:1525`).
> 3. `notes`'u **server yazar**: `Reversal of payment #N (X.XX CUR)`; client body'si yok sayılır.
> 4. **Reversal'ın reversal'ı yasak** → uygulama katmanında **400**. (DB CHECK başka satıra
>    bakamaz; trigger over-engineering olurdu.)
> 5. **Çifte-reversal garantisi DB'de** (partial UNIQUE → 409), uygulama katmanında değil.
> 6. **paid/balance koduna dokunulmadı** — SUM negatifi kendiliğinden netler (D2). Tam-sıfır
>    durumda `paid_eur` **`0.00`** döner (COALESCE), `—` değil.
> 7. **Edit/Delete endpoint'i HÂLÂ YOK** — immutability korundu.
> 8. **Reverse aksiyonu yalnız detay sayfasında** (listede yok).
>
> **SIRADAKİ ADAYLAR (3a-5, karar Suer'de):** Transfer aksiyonu · payment schedule.

> ## ✅ 2026-07-22 — FAZ 3a-5 TAMAM (contract transfer / devir)
>
> **Migration 019 canlıda** (`019_transfer_guards`, dry-run → ROLLBACK → COMMIT ritüeliyle;
> kayıt **uzantısız**, `2026-07-22 18:17:21+00`). **Yeni kolon YOK**, iki partial UNIQUE:
> - `uq_contracts_transferred_from` — **one-child**: bir contract'ın en fazla bir devamı olur.
>   Race-proof, DB seviyesinde (027 deseni).
> - `uq_contracts_af_number` — server-üretimi af emniyeti (012'de af_number kısıtsızdı).
>
> **`POST /api/contracts/:id/transfer` canlıda.** **49/49 backend + 11/11 UI testi** geçti.
> Klon `INSERT..SELECT` + storno-taşıma + kaynak `status='Transferred'` — **TEK ATOMİK TX**
> *(canlı kanıt: id=1 ve id=3'ün `updated_at`'i aynı — `18:43:59.017131`)*.
> Hata yolları: **400** (`expo_id` eksik/geçersiz, kaynak status uygun değil) · **404** ·
> **409** (çifte transfer + af çakışması, **DB garantili**).
>
> **`PUT /:id/status`:** elle `'Transferred'` → **400**. `:229`'daki "geçiş matrisi yok" yorumu
> güncellendi. **Transferred'DAN çıkış serbest.**
>
> **`GET /:id`:** `transferred_from_af` + `transferred_to_id`/`transferred_to_af` join'leri
> → **3a-3 defter borcu KAPANDI** (ham id gösterimi kalktı).
>
> **`contract-detail.html`:** Transfer butonu (yalnız Active/On Hold **ve** `transferred_to`
> yokken) + inline expo-select formu + from/to **af linkleri**. `contract-list.html`'e
> dokunulmadı. **Commit'ler:** `11c397b` (019) + `63631de` (endpoint + UI).
>
> **E2E KABUL GEÇTİ (2026-07-22):** Acme → **[TEST] Reactivation Smoke Test Expo**.
> - Yeni contract **id=3** (`A-2026-001-T`): Active, bugünün tarihi, expo dolu, kopyalar birebir,
>   **Paid 9.80 / Balance 13.790,20**, taşınan ödeme orijinal tarihiyle.
> - Kaynak **id=1**: Transferred, **Paid 0.00 / Balance 13.800,00**, kapama satırı + terslenmiş
>   çiftler yerinde.
> - Liste 2 contract, rakamlar doğru.
>
> **KİLİTLİ KARARLAR (3a-5):**
> 1. **Transfer = YENİ contract yaratır** (klon; req 2.3 first-class action) — var olan iki kaydı
>    **bağlamaz**.
> 2. **Klon:** organizer / company / agent / frozen-para / `company_id` **kopya**; `expo_id`
>    seçilen hedef; `status` Active; `contract_date` transfer günü; operasyonel + convert alanları
>    **boş**. 4-status modelinde **"Transferred In" = `transferred_from` NOT NULL** (S6 ile uyumlu
>    — beşinci bir status eklenmedi).
> 3. **AF sonek kuralı:** `X → X-T → X-T2 → X-T3` (server üretir); `af` NULL ise NULL.
> 4. **Ödeme taşıma = STORNO-TAŞIMA.** Terslenmemiş ödeme başına: kaynakta **kapama**
>    (`reverses` set, bugün, `Transferred to <af> (payment #N)`) + yenide **pozitif kopya**
>    (**ORİJİNAL tarih**, `Transferred from <af> (payment #N)`). Terslenmiş çiftler ve reversal
>    satırları **yerinde kalır**. Sistem toplamı değişmez; paid/balance koduna dokunulmadı (D2).
>    *Semantik not:* kapama satırları **yapısal olarak reversal**'dır — UI rozeti "Reversal of #N"
>    gösterir, ayrımı `notes` yapar.
> 5. **A→B→A DÖNGÜ BORCU TASARIMLA KAPANDI:** yaratım-temelli transferde zincir **append-only**,
>    döngü yapısal olarak imkânsız. Kalan tek risk (çifte transfer) DB'de partial UNIQUE ile
>    çözüldü — trigger/CHECK gerekmedi.
> 6. **Elle `PUT → Transferred` kapalı; Transferred'dan çıkış serbest.**
>    **TEORİK NOT (yaşanmış vaka DEĞİL):** kaçış kapısı **tek yönlü** — Transferred'dan çıkılırsa
>    elle geri dönüş yok, psql gerekir; ikinci transfer her durumda DB'den **409** alır.
>    Kalıcı çözüm adayı: **Faz 4 permission** (Owner'a elle geçiş yetkisi).

> ## ⚠️ CANLI TEST VERİSİ — contract id=1 (Acme, sentetik)
>
> *(3a-4 E2E sonrası, 2026-07-22 ölçümü, `claude_readonly`. Bu blok önceki "2 ödeme kaydı"
> envanterinin yerine geçer.)*
>
> **İKİ contract var** (transfer sonrası):
>
> | id | af_number | status | expo | contract_date | paid_eur | balance_eur |
> |---|---|---|---|---|---|---|
> | 1 | `A-2026-001` | **Transferred** | — | 2026-06-20 | **0,00** | 13.800,00 |
> | 3 | `A-2026-001-T` | Active | **[TEST] Reactivation Smoke Test Expo** (id 11) | 2026-07-22 | **9,80** | 13.790,20 |
>
> **`id=2` YOK** — SERIAL sequence test akışında tüketildi. **Bilinen davranış, boşluk normaldir**
> (sequence rollback'te numara yakar).
>
> **7 ödeme kaydı** — id=1'de **6 satır**, id=3'te **1 satır**:
>
> | id | contract | tutar | kur | EUR | reverses | notes | durum |
> |---|---|---|---|---|---|---|---|
> | 1 | 1 | 100.00 USD | 0.90000000 | 90.00 | — | `test` | **TERSLENDİ** (#3) |
> | 2 | 1 | 500.00 TRY | 51.00000000 | 25.500,00 | — | — | **TERSLENDİ** (#4), hatalı kur |
> | 3 | 1 | −100.00 USD | 0.90000000 | −90.00 | **1** | `Reversal of payment #1 (100.00 USD)` | reversal |
> | 4 | 1 | −500.00 TRY | 51.00000000 | −25.500,00 | **2** | `Reversal of payment #2 (500.00 TRY)` | reversal |
> | 5 | 1 | 500.00 TRY | **0.01960000** | 9.80 | — | — | **TAŞINDI** (#6 ile kapandı) |
> | 6 | 1 | −500.00 TRY | 0.01960000 | −9.80 | **5** | `Transferred to A-2026-001-T (payment #5)` | transfer kapaması |
> | 7 | **3** | 500.00 TRY | 0.01960000 | 9.80 | — | `Transferred from A-2026-001 (payment #5)` | taşınan kopya |
>
> Tüm yöntemler `bank_transfer`, tüm tarihler 2026-07-22. *(Envanter ölçümle doğrulandı —
> varsayım değil.)*
>
> **Üç desenin canlı örneği bir arada:**
> - **id=2 + id=4** — reversal (hatalı kur düzeltmesi; hata veri girişinde, hesaplamada değil:
>   balance eksiye düşmüş ve hesap zinciri negatifi doğru göstermişti).
> - **id=1 + id=3** — reversal'ın doğru-kayıt üzerinde de çalıştığının kanıtı.
> - **id=5 + id=6 + id=7** — storno-taşıma: kaynakta kapama, hedefte pozitif kopya.
>
> ⚠️ **Ölçüm notu:** "taşınan kopya orijinal tarihini korur" kuralı bu canlı veriyle
> **ayırt edilemiyor** — orijinal (id=5) de kopya (id=7) da 2026-07-22. Kural yerel testte
> farklı tarihle (2026-07-10) doğrulandı; canlı veri onu çürütmüyor ama kanıtlamıyor da.
>
> **S8 E2E'ye kadar SİLİNMEZ; S8 öncesi temizlenir.**
>
> **sales_agents (3b-1 sonrası, 2026-07-23 ölçümü):** **151 kayıt** = 150 Zoho-import
> (`zoho_record_id` dolu) **+ 1 LEENA-doğumlu** (elle create; `zoho_record_id` NULL, UI testinden).
> Kırılım: `internal` **127** (126 import + 1 elle) / `external_freelance` 19 / `external_agency` 5;
> aktif **27** (26 import + 1 elle) / pasif 124. *(Import 150'sinin kendi kırılımı: internal 126 /
> freelance 19 / agency 5; aktif 26 / pasif 124 — probe'la birebir.)*
> `contracts` 2 / `payments` 7 **değişmedi**. **Atanmış agent'ı olan contract YOK** (E2E ataması
> temizlendi).

> ## ★★ FAZ 3A KAPANDI (2026-07-22) — TİCARİ ÇEKİRDEK LEENA-NATIVE CANLIDA
>
> **Uçtan uca zincir çalışıyor:**
> `quote → convert → contract → payment → reversal → transfer → hesaplanan paid/balance`
>
> | Dilim | Ne geldi | Migration |
> |---|---|---|
> | **3a-1** | contracts görünür (liste + operasyonel kolonlar + status geçişi) | 016 |
> | **3a-2** | payment girişi + **hesaplanan** paid/balance (D2) | 017 |
> | **3a-3** | contract detay sayfası | — (gerekmedi) |
> | **3a-4** | ödeme düzeltme / **reversal** (storno) | 018 |
> | **3a-5** | contract **transfer** (klon + storno-taşıma) | 019 |
>
> Migration'lar **016–019**, hepsi **dry-run → ROLLBACK → COMMIT ritüeliyle** uygulandı ve
> `schema_migrations`'a uzantısız kayıtla işlendi. **Tüm dilimler görsel onay / E2E kabul ile
> kapandı** — hiçbiri "test geçti" ile bırakılmadı.
>
> Taşınan mimari ilkeler: **payments immutable event** · **D2 (hesaplanır, saklanmaz)** ·
> **frozen-EUR** · teklik/idempotency garantileri **DB'de** (partial UNIQUE, 027 deseni) ·
> `round2` yalnız ilk girişte, kopya/işaret çevriminde asla.

> ## ✅ FAZ 3B-1 TAMAM (2026-07-23) — KOMİSYON RECONCILE + AGENT ALTYAPISI + ZOHO IMPORT
>
> **Ölçüm + reconcile:** "tekil `sales_agent_id` ↔ req üçlü modeli" çelişkisi **GERÇEKti**;
> **requirements kazandı** — Zoho'da üçlü model (Agent/SR/SD) fiilen yaşıyor (ELIZA ölçümü:
> alanlar Zoho'da VAR, `syncSalesOrders` map etmiyordu — yalnız tek `Sales_Agent.name` lookup).
>
> **Migration'lar (016-022 serisine 020-022 eklendi; hepsi `\i` ritüeliyle):**
> - **020 `commission_agents`:** `sales_agents.default_commission_pct` + contracts'a **agent/sr/sd
>   FK + 3 override pct** (K1a, req `:461-469` şeması) + **dışlayıcılık CHECK'leri** (K3a: Agent XOR
>   SR; SD yalnız SR varken) + pct-requires-fk + 0-100 range (B18). **EXPAND** adımı.
> - **021 `import_prep`:** **S7 v1.2 amendment** (aşağıda) + 6 kolon (`email` / `sales_group` /
>   `agent_company` / `commission_currency` / `is_active` / `zoho_record_id` + partial UNIQUE).
> - **022 `import_prep2`:** probe sonrası delta — `default_director_pct` (+0-100 CHECK) /
>   `sales_team` / `country`. **021'e DOKUNULMADI** (uygulanmış migration değişmez — delta ayrı dosya).
>
> **ZOHO IMPORT MÜHÜRLÜ (2026-07-23):** probe → seal → dry-run → import akışı; `MAPPING_SEALED`
> guard'ı (alan-adı **tahminiyle import imkânsız**). **150 kayıt import edildi:** internal **126**
> / external_freelance **19** / external_agency **5**; aktif **26** / pasif **124** (canlı kırılım
> probe'la birebir). İdempotent (**D4:** `ON CONFLICT (zoho_record_id) DO NOTHING` — asla UPDATE
> etmez). Script: `scripts/import-zoho-agents.js` (**tek seferlik, sync DEĞİL**; Render Shell notu:
> `export DATABASE_URL="$DATABASE_INTERNAL_URL"`).
>
> **Agent atama canlıda:** `PUT /api/contracts/:id/assignment` (TAM SET semantiği; dışlayıcılık
> 400'leri **CHECK'e düşmeden**) + `contract-detail` **Commission kartı** (dropdown + pct
> **placeholder = default**, OTOMATİK YAZILMAZ — override bilinçli). Kod eski `sales_agent_id`'den
> **TAMAMEN çıktı** (word-boundary grep 0) → **DROP artık güvenli**.
>
> **Agent UI canlıda:** `sales-agents.html` (liste + "Show inactive" + create/edit + Active toggle)
> + `GET` default **yalnız aktifler** (B6 davranışı) + POST/PUT. Nav 3 sayfaya + yeni sayfaya eklendi.
>
> **Commit'ler:** `70e5654` (020) · `0ee0ea1` (atama+geçiş) · `443fdea` (021) · `f159067` (script)
> · `f77d4aa` (022+mühür) · `79047c7` (UI).
>
> **E2E / GÖRSEL ONAY (2026-07-23, Suer):** agent liste (aktif-default + Show inactive soluk
> satırlar) + New agent / Edit / deactivate + assignment dropdown gerçek veriyle **GEÇTİ** (ekran
> kanıtlı). ⚠️ *(Ölçüm notu: E2E'de yapılan agent ataması **kalıcı bırakılmadı** — 2026-07-23
> ölçümünde `contracts`'ta agent/sr/sd atfı olan satır YOK; atama akışı test edildi, sonra
> temizlendi.)*
>
> **S7 v1.2 AMENDMENT (kilitli, BELGELİ BORÇ):** `"internal → user_id NOT NULL"` **ASKIYA ALINDI**
> — dayandığı `users` tablosu LEENA'da yok, uygulanabilir değildi (internal agent hiç girilemiyordu).
> Korunan yön: `external_* → user_id NULL` (`sales_agents_external_user_null_check`). Faz 4'te
> `users` doğunca internal'lara `user_id` backfill + eski sıkılık geri gelir. **NOT:** `archive` B3
> v1.0/v1.1 metni hâlâ eski hâli anlatıyor — **belge güncelleme borcu** (ayrı belge dilimi).
>
> **KİLİTLİ KARARLAR (3b-1):**
> - **K1a:** atama düz 3 FK + 3 pct override contracts üzerinde (req `:461-469`).
> - **K2a:** tekil `sales_agent_id` DROP edilecek — sıralı (expand→contract), **023'te**.
> - **K3a:** dışlayıcılık DB CHECK'te.
> - **K4:** `default_commission_pct` agent kaydında.
> - **K5 GÜNCELLENDİ:** elle seed **İPTAL** → Zoho import (gerçek kaynak) + kalıcı create/edit UI
>   (Yaprak'ın yüzeyi).
> - **K6:** `sales_owner_user_id` komisyon atıf kaynağı **DEĞİL** — LIFFY provenance metadata'sı,
>   Faz 4 identity'de çözülür.
> - **D1:** `is_active` sales_agents'ın **kendi kolonu** (B6 taşıyıcısı); Faz 4'te internal'lar
>   user-deaktivasyonuyla senkron. Deactivate reason-log Faz 4 audit'e ertelendi.
> - **D2:** `commission_currency` taşındı, **motor dilimine kadar KULLANILMAZ**.
> - **D3 — ZOHO-CANONICAL KURALININ İLK BELGELİ İSTİSNASI:** agent modülü bugünden
>   **LEENA-canonical**; Zoho agent modülü DONUK. Genel kural (expo/sector/country vb.) DEĞİŞMEDİ.
> - **D4:** import idempotent DO NOTHING; sync değil.
> - **Currency:** create/edit **normalize** eder (`eur→EUR`; `euro→400`) — payments deseniyle tutarlı.
> - **SUER İLKESİ (genel, kilitli):** veri sistemde varsa elle girilmez — kaynağından otomatik
>   alınır; kaçınılmaz elle giriş **serbest metin değil SEÇMELİ** (select/datalist).
>
> ---
>
> **★ K7 — KOMİSYON MOTOR KURALLARI (Suer, kilitli — motor dilimi bunlarla açılır):**
> - **(a)** Hak ediş **TAHSİLATA bağlı ve ORANSAL** — kısmi ödeme = kısmi komisyon.
> - **(b) MATRAH = `contract_line_items`'tan FORMÜLLE türetilir, SAKLANMAZ (D2):**
>   `Σ (quantity × unit_price × (1 − discount_percent/100))` — **`is_registration_fee = false`**
>   satırlar; **vergi yapısal olarak dışarıda** (tax ayrı katman), **RF bayrakla dışarıda**. Satır
>   yoksa komisyon **HESAPLANMAZ** + "kalem dökümü eksik" raporlanır.
>   **SAHA KANITI (Zoho canlı contract, 2026-07-23):** 18.600 MAD − 1.500 RF = 17.100 × SR %5 =
>   **855** — formül Zoho pratiğiyle **birebir**.
> - **(c) ÖDEME TAKVİMİ:** ayda **İKİ kesim** — ayın **15'i** ve **ay sonu**; ödeme, girildiği
>   tarihten **SONRAKİ İLK kesimde** ödenir. Cycle SAKLANMAZ — `payment_date`'ten türetilir (D2).
> - **(d)** Reversal/transfer edilen ödemeler matrahtan **otomatik düşer** (SUM netler — özel kod
>   yok, doğrulama testi yeter).
> - **(e) SD mekanizması:** `default_director_pct` (Zoho `Director_Comm_Rate`) — canlı örnek SR %5
>   + SD %2. "Contract amount"ın vergi-dahilliği belirsizliği **L kararlarıyla KAPANDI** (matrah
>   artık satırlardan türer); `contracts.revenue`'nun vergi-dahilliği transport'a kadar **kanıtsız**
>   (dürüst not).
>
> **L KARARLARI (satır kalemleri — inşa sonraki dilimde):**
> - **L1** `contract_line_items` (quote satırlarının **convert anında donmuş kopyası**; satır
>   toplamı saklanmaz).
> - **L2a** `product_code` donmuş + **`is_registration_fee` bayrak**.
> - **L3** convert payload **ŞİMDİ genişler** (opsiyonel `line_items[]`); elle-giriş UI YOK.
>   ⚠️ **LIFFY AKTİVASYON ÖNKOŞUL LİSTESİNE EKLE:** "convert payload'ında `line_items` **ZORUNLU**
>   olur".
> - **L4** satırlar geldiyse `grand_total(hesap) ↔ revenue ±0.01` değilse **400**; satırlar
>   **immutable**.
> - **L5** sıra.

> ## ✅ 2026-07-24 — FAZ 3b-2 TAMAM (023 DROP + 024 line items + convert L3/L4 + commissionable_base K7b + UI)
>
> **Migration 023 (`023_drop_contracts_sales_agent_id`) canlıda** *(Suer teyidi 2026-07-24:
> `information_schema`'da `sales_agent_id` 0 satır; kayıt `@ 10:07:33+00`)*. **K2a'nın CONTRACT
> adımı kapandı** — 020'de açılan expand→contract döngüsü tamam. Kolonla birlikte
> `contracts_sales_agent_id_fkey` FK'si de düştü; **üçlü agent/sr/sd FK + pct + CHECK'ler eksiksiz
> duruyor** (`\d` ile doğrulandı).
>
> **Migration 024 (`024_contract_line_items`) canlıda** *(Suer teyidi: 11 kolon, 6 kısıt —
> 3 check + fk + pk + unique, `pg_get_constraintdef` ile doğrulandı; kayıt `@ 10:13:14+00`)*.
> **Şema kararları:**
> - `quantity numeric(10,2)` — **⚠️ İŞARETLİ SAPMA (kabul):** taslak `(12,2)` diyordu; `sqm`
>   emsali ölçümü (016) taslağı yendi, m² hassasiyeti sqm ile birebir.
> - `unit_price numeric(14,2)` (`revenue` emsali) · `discount_percent` CHECK **iki sınırlı** 0-100.
> - `UNIQUE(contract_id, line_no)` FK araması için index görevini de görür → **ayrı index bilinçli YOK**.
> - `currency` CHECK **bilinçli YOK** (contracts.currency'de de yok — koşullu dal) · `product_code`
>   nullable · `created_at` var / **`updated_at` bilinçli YOK** (tablo immutable) · **satır toplamı
>   kolonu YOK** (D2).
> - **017 payments'ın isimsiz-kısıt emsalinden BİLİNÇLİ ayrılık:** tüm kısıtlar **açık adlı**
>   (017 dersi).
>
> **Backend (commit `bd47d99`):** convert **L3** opsiyonel `line_items[]` — yoksa/boş dizide eski
> davranış **birebir** (4 senaryo değişmedi). `line_no`'yu **SERVER** atar (dizi sırası, 1'den);
> `currency`'yi **SERVER** contract'tan kopyalar (payload satır currency'si yok sayılır).
> **SPESİFİKASYON-DIŞI GUARD (onaylı):** satır varsa contract `currency` zorunlu → 400. **L4:**
> `grand_total` (RF **DAHİL**) ↔ `revenue` `±0.01` → 400 (mesajda iki değer). Atomik **tek tx**
> contract + satırlar; `23514 → 400` mapWriteError'da.
>
> **GET `/:id`:** `line_items[]` (ORDER BY line_no) + `commissionable_base =
> SUM(ROUND(q×p×(1−d/100),2)) FILTER (RF=false)` — **D2, saklanmaz**. **⚠️ İŞARETLİ SAPMA (kabul):**
> "üçüncü lateral" yerine **AYRI SQL** — `CONTRACT_DETAIL_SQL` PUT assignment ile paylaşımlı, lateral
> onu kırardı; hesap yine SQL'de. Satır yokken `base null` + `reason "line items missing"`;
> **YALNIZ-RF edge:** base `"0.00"` (kalem var, komisyona konu tutar 0 — reason yok).
>
> **Testler:** backend **27/27** (regresyon 4 senaryo + satırsız/boş + Zoho saha kanıtı fixture'ı
> `18.600→17.100→855` + L4 sınır tam/`+0.01`→201, `+0.02`→400 + şekil + atomiklik/idempotency-temiz
> + satırsız reason) · UI DOM stub **11/11**.
>
> **UI (commit `94ff3e5`):** `contract-detail` **Line Items kartı** (Payments öncesi, aynı iskelet;
> `money`/`dash`/`escapeHtml` yeniden kullanıldı; RF rozeti `.tag`; Line Total **UI-hesap, D2**; sıra
> server'dan).
>
> **CANLI CURL + GÖRSEL ONAY (Suer teyidi 2026-07-24, ekran kanıtlı):** curl → **201, contract id=4**,
> `AF-TEST-LINES-001`, `quote_id e72b38fd-…-078df138868c`, EUR / rate 1.0 / revenue 18.600,00, 2 satır
> (Stand 100×171,00; Registration Fee 1×1.500,00 RF). Ekranda **id=4** → 2 satır, RF rozeti, Line
> Total 17.100,00 / 1.500,00, **Commissionable Base 17.100,00 EUR**; **id=3** → "No line items" +
> "— (line items missing)"; diğer kartlar bozulmadı. Canlı sayım: **3 contract / 2 line_item / 8+ ödeme**.
>
> **Commit'ler:** `5a6e355` (023+024 dosyaları) · `bd47d99` (convert+GET+testler) · `94ff3e5` (UI).
>
> **Test verisi zinciri:** `id=4` (`AF-TEST-LINES-001`) **SENTETİK** — `id=1`/`id=3` gibi
> **S8 E2E'ye kadar SİLİNMEZ**.
>
> **⚠️ LIFFY AKTİVASYON ÖNKOŞULU (L3 somutlaştı):** convert payload'ı **`line_items[]` göndermeli**;
> **satır varken `currency` zorunlu** (server 400). Göndermezse contract **satırsız doğar** →
> `commissionable_base` **hesaplanamaz** (komisyon motoru çalışmaz). Bu, LIFFY aktivasyon
> önkoşullarına eklenen kalıcı maddedir.

> ## ✅ 2026-07-25 — FAZ 3b-3 TAMAM (komisyon motoru: M1 çekirdek + FIX + M2 kesim raporu — MIGRATION'SIZ, tamamen türetilmiş/D2)
>
> **Komisyon motoru üç commit'te canlı, SIFIR migration** — tüm hesap `contract_line_items` +
> `payments` üstünde SQL'de türetilir, hiçbir komisyon değeri saklanmaz (D2). Commit zinciri
> (`git log` ile doğrulandı): **M1 `5c7ccfd` · M1-FIX `320f00f` · M2 `f28e6a6`**.
>
> **KİLİTLİ HÜKÜMLER (bu dilimde verildi — artık defter kaydı):**
> - **SD HÜKMÜ (a):** SD **bağımsız**, SR ile **AYNI matraha** — `sd_pot = sd_pct/100 × base`.
>   Kademeli "SR'ın içinden" modeli **REDDEDİLDİ**. Saha kanıtı: SD %2 = **342,00 MAD** =
>   17.100 × %2. Mühür: M1-T7/T8.
> - **CANCELLED HÜKMÜ (a):** tahsil edilmiş ödemeler komisyon doğurmaya **devam eder** (K7a);
>   motor/rapor **status filtresi YOK**; iade yalnız **reversal**'la, `SUM` netler. Mühür
>   testleri: **M1-T12 + M2-T-G**.
> - **Sentez M-a..M-e:** iki katman (potansiyel/hak ediş) · oran = `paid_eur/revenue_eur` ·
>   ödeme-başına dilim, kesim ödemenin `payment_date`'inden · tavan `LEAST(...,1)` · yuvarlama
>   **yalnız gösterilen toplamlarda** (ara yuvarlama YOK).
> - **U1a** tavan **kümülatif-marjinal** dilimlere yansır ("(cap)" notu) · **U2a** kesim
>   **takvim günü** (`payment_date` DATE, TZ yok) · **U3a** rapor **yalnız hak edilmişi** gösterir,
>   potansiyel detayda kalır.
> - **Sınır günü:** gün ≤15 → ayın **15'i** kesimi; ≥16 → **ay sonu**; kesim günü **DAHİL**.
> - **Penny-tavan:** overpayment notu **yalnız** `paid_eur − revenue_eur > 0.01` ise (L4 toleransı).
> - **Reversal'ın kesim dönemi** = reverse edildiği gün (`payment_date = CURRENT_DATE`) — M-c ile
>   tutarlı, **M2 T-C** ile mühürlü.
>
> **M1 — komisyon çekirdeği (`5c7ccfd`):** `routes/contracts.js`'e `computeCommission()` (`:318`) +
> `GET /:id`'de `contract.commission` (`:465`). Nesne: `base, ratio,
> roles[{pct_used, pct_source, full/full_eur, earned/earned_eur, reason?}]`. Oran çözümü
> **override > default**. Ölçülen default kolonlar: `default_commission_pct`
> (**agent + SR ORTAK — ⚠️ İŞARETLİ SAPMA**, mevcut şema gerçeği) + `default_director_pct` (SD).
> **Tüm aritmetik SQL**; JS `round2` komisyonda **hiç yok**. Koruma durumları: `line items missing`
> / `roles []` / `revenue missing` / `rate missing`. **Testler 29/29** (bu oturumda yeniden
> ölçüldü) + UI stub 15/15 — sayı zinciri 855 / 342 / 641.25 / tavan / SD 342-136.80 / T12.
>
> **M1-FIX (`320f00f`):** assignment-save sonrası **Commission + Line Items kartlarının kaybolması**.
> Kök neden: `submitAssignment`'ın `render(data.contract)` kullanması — PUT paylaşımlı
> `CONTRACT_DETAIL_SQL`'den döner, `line_items`/`commission` **taşımaz** (onlar yalnız `GET /:id`'de
> ayrı sorgularla eklenir). **Tek satır → `loadContract()`** (add-payment deseni). Stub **7/7**.
> *(Suer teyidi 2026-07-24/25, ekran kanıtlı: fix sonrası tekrarda kartlar KALDI, "Assignment saved"
> toast'ıyla.)* **Görsel tur bug'ı yakaladı → görsel-onay-şart kuralının değeri kanıtlandı.**
>
> **M2 — kesim raporu (`f28e6a6`):** `routes/commissions.js` (YENİ) + `GET /api/commissions`
> (`index.js` mount) + `public/commissions.html` (YENİ) + nav linki (`main-panel-v2.html`).
> `from/to` **cut_date** filtresi; **⚠️ İŞARETLİ SAPMA (kabul):** default `to` = **içinde bulunulan
> dönemin cut_date'i** ("bugün" literal'i mevcut dönemi dışlardı → G5a çelişkisi). Kümülatif-marjinal
> dilim SQL'i: `cum_after = SUM(amount_eur) OVER(PARTITION BY contract ORDER BY payment_date,id)` →
> `effective_pay = LEAST(cum_after,rev) − LEAST(cum_before,rev)` → `slice_raw = pot_eur ×
> effective_pay / rev` + `capped` işareti; **tek final ROUND** (M-e). **Tek-kaynak fiilen
> `COMMISSIONABLE_BASE_EXPR`** (contracts.js'ten export) + **İNVARYANT testi** (Σ ham dilim ≡ M1
> `earned`; telescoping, ham + ROUND sonrası). **⚠️ İŞARETLİ SAPMA (kabul):** `SLICE_EUR_EXPR`
> literal `amount_eur` taşıdığından M2 pencereli `effective_pay` için **referans/belge** olarak
> export edildi, birebir kullanılmadı. **Testler 30/30 + stub 16/16** — 30.78 / 26.93 /
> 61.56-15.39-0.00+cap / T-C negatif dönem toplamı olduğu gibi kalır.
>
> **GÖRSEL ONAY (Suer teyidi 2026-07-25, ekran kanıtlı):** `commissions.html` default aralıkta
> **"Jul 16–31, 2026 (cut Jul 31)"** → **BENGU DOGRUER** · Slice **342.00** · Period Total
> **342.00 EUR** · dipnot görünür; **01-31 Ocak** aralığında **"No commission slices in this
> period."**; nav linki çalışıyor; `contract-list` (3 kayıt) bozulmadı. M1 kartı ayrıca: id=4
> atamasızken "No commission roles assigned"; SR %5 override sonrası **sr · BENGU DOGRUER ·
> 5.00% (override) · Full 855.00 EUR · Earned 342.00 EUR · Collection 40%** (7.440 ödeme sonrası);
> id=3 "— (line items missing)".
>
> **Kozmetik not (bilinçli, aksiyon YOK):** EUR kontratta çift gösterim "855.00 EUR (855.00 EUR)".
>
> **Test verisi zinciri GENİŞLEDİ:** `id=4` + **BENGU DOGRUER** SR %5 override + **7.440,00 EUR**
> ödeme (2026-07-24) — **S8 E2E'ye kadar SİLİNMEZ**.

> ## ✅ 2026-07-27 — GOVERNING-DOC ROL DARALTMASI (ell-docs `55c07ff`)
>
> - **Belge rolleri kilitlendi.** `ELL_YOL_HARITASI_v5` = yalnız **PUSULA** (faz sırası +
>   her fazda geçerli ilkeler). `ELL_BILGI_MIMARISI_v3` = yalnız **BİLGİ MİMARİSİ** (hangi
>   varlık hangi sistemde/DB'de, sahiplik kimde). **Durum/ilerleme/sıradaki adım = yalnız
>   bu defter.** Her iki belgeye deftere işaretçi kondu (YOL 6 yer, BILGI 1 yer).
> - **11 cerrahi düzenleme, içerik SİLİNMEDİ** — eski metinler üstü çizili + ⛔ SUPERSEDED
>   olarak duruyor (defter deseninin aynısı). Diff: +35 / −10, 2 dosya.
> - **ÖLÇÜM BULGUSU (borç yanlış tanımlanmıştı):** "DURAN BORÇ" iki belgenin 2026-06-19
>   LEENA-native kararına göre güncellenmediğini varsayıyordu. Ölçüm bunu ÇÜRÜTTÜ: mimari
>   düzeltme her iki belgede ZATEN uygulanmıştı (SINIF C = boş; kanıt `YOL:58,59,65` ·
>   `BILGI:36,38`). Gerçek borç yalnız **durum/ilerleme cümlelerinin ayıklanması**ydı.
> - **Öz-çelişki giderildi** (`YOL:30`): belge hem "defter kazanır" hem "bu belge kazanır"
>   diyordu. Yeni hüküm: **faz/ilke çelişkisinde yol haritası, durum çelişkisinde defter kazanır.**
> - **UUID gün-1 kuralı S7 v1.2 ile uyumlandı** (`YOL:133` + `YOL:359`): PK tipi
>   **barındıran sistemin native tipini** izler — **LEENA = integer SERIAL, LIFFY = UUID**.
>   Cross-system soft-ref **kaynak sistemin tipinde** tutulur (`source_quote_id`,
>   `sales_owner_user_id` UUID kalır). **`organizer_id` + audit gün-1 kuralı DEĞİŞMEDEN
>   geçerli.** Tip Faz 4 kimlik birleşmesinde yeniden ele alınır.
> - **KALAN (ikinci pas adayı, bu dilimde bilinçle yapılmadı):** YOL faz gövdelerindeki
>   dağınık "bugün YOK / şu an" ifadeleri ve BILGI tablolarındaki 🟢/🟡/🔴 olgunluk
>   sütunları tek tek temizlenmedi; bölüm-seviyesi ⛔ işaretçisiyle nötralize edildi
>   (YOL BÖLÜM 3 başı, BILGI rol sınırı bloğu). Gerekirse ayrı dilim.
> - Commit: **`55c07ff`** (ell-docs). LEENA koduna/DB'ye dokunulmadı.
> - **Devir brief'i ELL_GLOSSARY.md için dayanaksız bir değişiklik iddiası taşıyordu** —
>   2026-07-27 ölçümü dosyayı **TEMİZ** buldu (son dokunuş `a416fa9`). İddia metni bilerek
>   aktarılmadı: alıntı sonraki oturumlarda canlı iddia olarak yeniden doğuyor (2026-07-29
>   tekrarı ölçüldü). Madde kapandı, aksiyon gerekmiyor.

> ## ✅ 2026-07-27 — PAYOUT P1 CANLIDA (migration 025 + agent cari hesap)
>
> - **Migration `025_commission_payouts` CANLI** (leena_v401_db). Dry-run (ROLLBACK) →
>   COMMIT, `\d` doğrulandı. Son migration **024 → 025**. Tamamen additive; canlı LEENA
>   operasyonu etkilenmedi. Kod commit: **`3ab2dac`** (leena-v401).
> - **MODEL = CARİ HESAP (S-1 kilitli).** Payout kaydında **dönem/kesim kolonu YOKTUR** —
>   bilinçli. Bakiye = Σ earned (türetilmiş) − Σ payout `amount_eur`, **her okumada hesaplanır**.
>   İleride "eksik" sanılıp dönem kolonu EKLENMEYECEK.
> - **D2 KORUNDU.** Tablo komisyonu değil **ÖDEMEYİ** saklar. `earned_eur` / `balance` /
>   `cut_date` gibi hiçbir türetilmiş değer saklanmaz. ("Payout olayında dondurulur"
>   önerisi ölçüm turunda REDDEDİLDİ.)
> - **Tablo şekli** (payments deseni birebir): `id serial PK` · `organizer_id int NOT NULL`
>   (FK yok) · `sales_agent_id → sales_agents(id)` · frozen-EUR dörtlüsü
>   (`amount`/`currency` DEFAULT 'EUR'/`exchange_rate`/`amount_eur`) · `payout_date DATE` ·
>   `notes` · `reverses_payout_id` self-FK · `created_by` · `created_at`.
>   **`updated_at` YOK** (immutable olay). **`payment_method` YOK** (spekülatif açılmadı).
> - **Kısıtlar:** `commission_payouts_amount_check` (reversal yoksa amount>0, varsa amount<0) ·
>   `commission_payouts_exchange_rate_check` (>0) · `uq_commission_payouts_reverses`
>   (partial UNIQUE — bir payout yalnız bir kez ters alınır) · `ix_commission_payouts_agent`.
> - **S-3: CLAWBACK AYRI MEKANİZMA DEĞİL.** Fazla ödeme → bakiye negatif → sonraki ödemede
>   mahsuplaşır. Ayrı clawback tablosu/alanı/akışı KURULMAYACAK. Negatif bakiye engellenmez.
> - **S-4: IMMUTABLE.** UPDATE/DELETE yok; düzeltme = negatif tutarlı yeni satır +
>   `reverses_payout_id`.
> - **S-8: TEK KAYNAK.** M2'nin dilim CTE'leri (`pay`/`eff`/`sliced`) `commissions.js`'ten
>   **`utils/commissionSlices.js` → `SLICE_CTES`**'e çıkarıldı (salt extract). Hem M2 hem
>   agent statement AYNI ifadeyi kullanır; ikinci komisyon formülü YOK.
>   **M2 regresyonu 30/30 birebir geçti** — çıktı değişmedi.
> - **Endpoint'ler** (`routes/payouts.js`, mount `/api/agents`):
>   `POST /:id/payouts` (amount_eur sunucuda hesaplanır; 23505→409, 23514→400) ·
>   `GET /:id/statement` (earned/paid/balance + payout listesi, hepsi türetilmiş;
>   status filtresi YOK — K7a).
> - **CANLI E2E DOĞRULANDI (agent 47 BENGU DOGRUER, earned 342.00):**
>   K-1 paid 0.00 / balance 342.00 → K-2 (id=1, 100 EUR) → K-3 (id=2, 300 EUR)
>   paid 400.00 / **balance −58.00** → K-4 (id=3, −100, reverses id=1) paid 300.00 /
>   balance 42.00 → K-6 (id=4, 1000 MAD @0.09 → **amount_eur 90.00**) paid 390.00 /
>   **balance −48.00**, 4 satır. Görsel onay alındı.
> - **KALICI TEST VERİSİ:** `commission_payouts` id=1,2,3,4 (agent 47) — immutable,
>   **SİLİNMEZ**; sentetik zincirin parçası (id=4 contract zinciriyle birlikte S8 E2E'ye kadar).
> - **Bilinen küçük (aksiyonsuz):** `payout_date` JSON'da ISO timestamp olarak dönüyor
>   (`...T00:00:00.000Z`) — kolon DATE, kozmetik; P2 UI'da formatlanacak.
>   `created_by` NULL — Faz 4 kimlik/yetkiye ertelendi (`// TODO Faz 4` yer işareti kodda).
> - **Ölçüm kaydı:** 2026-07-27 itibarıyla çift-rollü agent sayısı = **0** →
>   `sales_agents.default_commission_pct` agent+SR ORTAK kolon sapması bugün zararsız.
>   **TETİK: ilk çift-rollü agent doğduğunda kolon ayrılır.**

> ## ✅ 2026-07-27 — PAYOUT P2 CANLIDA (agent statement UI iskeleti)
>
> - **`public/agent-statement.html` CANLI.** Kod commit: **`ab8a6d9`** (leena-v401).
>   MIGRATION YOK, yeni backend endpoint YOK — P1'in iki endpoint'i kullanıldı.
>   `commissions.html` iskeleti/auth deseni birebir izlendi (leenaFetch, 401/403 auto-logout).
> - **D2'nin UI karşılığı korundu:** `earned_eur`/`paid_eur`/`balance_eur` sunucudan
>   geldiği gibi basılır; istemcide toplama/çıkarma/yuvarlama YOK. `amount_eur` istemcide
>   hesaplanmaz, gönderilmez — sunucu hesaplar.
> - **Ekran:** üç kutu (Earned/Paid/Balance, negatif kırmızı) · payouts tablosu
>   (sunucu sırası korunur; `payout_date` ISO→`YYYY-MM-DD` kırpılır; negatif satır kırmızı;
>   REVERSES kolonu) · Record payout formu (EUR→rate 1 disabled) · hata satırı.
> - **Reverse akışı:** buton YALNIZCA `amount > 0` VE satır henüz ters alınmamışsa görünür;
>   aksi halde "reversed". Tıklanınca `confirm()` → negatif satır + `reverses_payout_id`.
>   Çift-reverse UI'dan yapısal olarak imkânsız (buton gizlenir); DB tarafı ayrıca
>   partial UNIQUE ile korunuyor (P1 T-4).
> - **Erişim:** yeni sayfa kendi Finance nav'ını taşır (ortak partial YOK — nav her sayfada
>   inline). `public/sales-agents.html` satır başına TEK additive "Statement" butonu eklendi
>   (kolon sayısı değişmedi). **Canlı ops sayfalarına (visitor/badge/floorplan/check-in/
>   terminal) DOKUNULMADI.** `commissions.html`/`contract-list.html` nav'ları değişmedi.
> - **`agent_id` yoksa:** `/api/sales-agents` listesinden basit `<select>` (yeni endpoint
>   yazılmadı; `/api/agents` liste endpoint'i YOK — bilinen durum).
> - **Regresyon:** M1 29/29 · M2 30/30 · payout 26/26 — P1'le birebir, sapma yok.
> - **GÖRSEL TUR 5/5 GEÇTİ (agent 47, canlı):**
>   T1 Earned 342.00 / Paid 390.00 / Balance −48.00 kırmızı, 4 satır ·
>   T2 id=1 "reversed", buton gizli · T3 +10 EUR → Paid 400.00 / Balance −58.00, 5 satır ·
>   T4 storno → Paid 390.00 / Balance −48.00, 6 satır (net sıfır, "Reversal of #5", REVERSES #5) ·
>   T5 `-5` denemesi → ekranda "amount must be greater than 0 for a payout.", satır
>   eklenmedi, rakamlar değişmedi (sessiz yutma yok).
> - **KALICI TEST VERİSİ (eklendi):** `commission_payouts` id=5 ("P2 UI test", 10 EUR) ve
>   id=6 ("Reversal of #5", −10 EUR) — immutable, **SİLİNMEZ**. Toplam 6 satır, net etki 0.
> - **Faz 4 borcu (kabul edilmiş):** Finance ekranları rol-gate'siz görünüyor;
>   `<!-- TODO Faz 4: role gate (B21-B42) -->` yer işareti sayfada duruyor.
> - **KALAN (P3 adayı, bu dilimde bilinçle yapılmadı):** toplu ödeme ekranı · PDF/makbuz ·
>   banka entegrasyonu · agent'a bildirim · nav birleştirme (ortak partial) · tasarım cilası.

> ## ✅ 2026-07-28 — PAYMENT SCHEDULE PS1 CANLIDA (migration 026 + vade planı)
>
> - **Migration `026_payment_schedule` CANLI** (leena_v401_db). Dry-run (ROLLBACK) → COMMIT,
>   `\d` doğrulandı. Son migration **025 → 026**. Additive; canlı ops etkilenmedi.
>   Kod commit: **`fa7f288`** (leena-v401).
> - **PLAN ≠ GERÇEK (kilitli).** `payment_schedule_items` PLANDIR, `payments` OLAYDIR.
>   Eşleştirme ZORLANMAZ, uyarı üretilmez. Müşteri "Kenya'ya ödeyeceğim" deyip Türkiye'ye
>   öderse: plan satırı olduğu gibi kalır, ödeme kendi ofisiyle kaydedilir (S-13r).
> - **KUR DONDURULMAZ (S-4).** Plan para hareketi değildir → `exchange_rate`/`amount_eur`
>   kolonu YOK. Tutar kontrat para biriminde tutulur, `currency` kontrattan kopyalanır.
> - **REVİZYON DESENİ (S-5) — repoda ilk.** Tutar/tarih ASLA UPDATE edilmez; revizyonda eski
>   satırlar `superseded_at` damgalanır, yeni satırlar `revision = max+1` ile eklenir.
>   Aktif plan = `superseded_at IS NULL`. "Müşteri 3 kez vade erteledi" bilgisi kaybolmaz.
> - **DURUM SAKLANMAZ (S-7).** Zoho'nun `Payment Done ✓` / `Validity 05/26` deseni
>   KOPYALANMADI. "Ödenmemiş" = Σ schedule > Σ payments, TÜRETİLİR, kontrat seviyesinde.
>   `matches_revenue` yanıtta hesaplanır, saklanmaz.
> - **Yeni tablo `offices`** — sade referans: `id serial` · `name` · `country_code char(2)`
>   → **FK `core_countries(code)`** (⚠️ `core_countries` PK'sı CHAR(2) koddur, integer id
>   YOKTUR — `country_id` varsayımı ölçümle çürütüldü) · `is_active` · UNIQUE(name).
>   **TAM 5 satır tohum:** Turkey/TR · Morocco/MA · Nigeria/NG · Kenya/KE · China/CN.
>   Ofis × para birimi × tahsilat şekli **çarpım tablosu KURULMADI** — kombinasyon seçilir,
>   saklanmaz (S-11r).
> - **OFİS LİSTESİ KODA GÖMÜLMEZ (S-16r).** Enum yok, CHECK yok, frontend sabiti yok;
>   tüketici `GET /api/offices`'ten okur. K-12r testi ispatladı: yeni ofis TEK INSERT ile
>   eklenir, deploysuz görünür. `payment_method` bu kuralın DIŞINDA (kapalı küme, CHECK kalır).
> - **TEK SÖZLÜK (H7).** `expected_method` CHECK'i `payments.payment_method` ile AYNI beş
>   değeri kullanır (`bank_transfer`,`cash`,`cheque`,`credit_card`,`other`). 'bank'/'cash'
>   kısa sözlüğü AÇILMADI (iki sözlük = eşleme borcu). **`payments.payment_method`'a
>   DOKUNULMADI** (NOT NULL, canlıda 8/8 `bank_transfer`).
> - **`payments`'a iki nullable kolon** (tek ALTER — 027/028 dersi): `schedule_item_id`
>   (FK; **mantık bilinçli olarak YOK**, eşleştirme PS2+ işi — S-6) · `received_office_id` (FK).
> - **`payment_schedule_items` kısıtları:** partial UNIQUE `(contract_id, item_no) WHERE
>   superseded_at IS NULL` (027-deseni) · `ix_payment_schedule_items_contract` ·
>   4 ADLI CHECK (amount>0 · percent 0-100 · source 3-değer · expected_method 5-değer).
> - **DEFAULT ÜRETİCİ (Suer kuralı):** `d1 = contract_date + 7`, `d2 = expo.start_date − 30`.
>   `d2 <= d1` → **TEK kalem %100 @ d1** (S-2 çekme+birleştirme tek ifadede).
>   Değilse → %40 @ d1 + kalan @ d2. Yuvarlama: item1 ROUND(revenue×0.40,2), item2 = kalan
>   (Σ ≡ revenue TAM — S-3).
> - **YARIM PLAN YASAK (S-1).** `contract_date` / `expo_id` / `expo.start_date` / `revenue`
>   birinden biri NULL → **400 + 0 satır**, ayırt edici İngilizce mesaj. Canlıda doğrulandı.
> - **İMZA TARİHİ = `contracts.contract_date` (Suer kararı 2026-07-28).** Ayrı `signed_date`
>   AÇILMADI — convert zaten LIFFY `signed_at`'i buraya yazıyor; ikinci kolon iki kaynak
>   doğururdu. Ölçüm: canlı 3 kontratın 3'ünde de dolu, backfill gerekmedi.
> - **Σ ≠ revenue ENGELLENMEZ (S-9).** Elle tutar girişinde uyuşmazlık kabul edilir,
>   yanıtta `warning` döner. Gerçek plana zorlanmaz.
> - **KOMİSYONA DOKUNULMADI (S-8).** Komisyon tahsilat-oranlıdır (`paid_eur/revenue_eur`),
>   plana DEĞİL. Regresyon: **M1 29/29 · M2 30/30 · payout 26/26** sapmasız.
> - **Endpoint'ler:** `GET /api/offices` (routes/offices.js) · `GET /api/contracts/:id/schedule`
>   (active + history + türetilmiş totals) · `POST /api/contracts/:id/schedule` (elle,
>   yüzde XOR tutar) · `POST /api/contracts/:id/schedule/default`. Ofis yönetim endpoint'i
>   (POST/PUT) **bilinçle yazılmadı** — PS2.
> - **Testler: PS1 29/29** (yerel scratch DB). Kritik: **K-4 birleşme dalı** (fuara 32 gün)
>   canlıda test EDİLEMEZ, yalnız burada doğrulandı. K-7 revizyon invaryantı: eski satırların
>   `amount`/`due_date` değerleri değişmemiş.
> - **CANLI GÖRSEL TUR 5/5 (contract id=3, 15.000,00 USD, imza 2026-07-22, fuar 2027-01-01):**
>   V1 5 ofis · V2 default 201 · V3 **6.000,00 @ 2026-07-29 (%40) + 9.000,00 @ 2026-12-02
>   (%60)**, Σ 15.000,00 ≡ revenue, `matches_revenue true` · V4 revizyon → aktif **rev 2**,
>   history 2 satır superseded, tutarlar değişmemiş · V5 contract 4 (expo_id NULL) →
>   **400 "expo required", 0 satır**.
> - **KALICI TEST VERİSİ:** contract id=3'te schedule revision 1 (superseded) + revision 2
>   (aktif), toplam 4 satır — S8 E2E'ye kadar **SİLİNMEZ**.
> - **Bilinen küçük (aksiyonsuz):** `GET /schedule` `due_date`'i ham Date döndürüyor →
>   JSON'da TZ-kaymış ISO (`payout_date` ile aynı sınıf, DB değeri doğru). PS2 UI'da
>   formatlanacak.
> - **Ölçüm notları (kayda geçsin):** `expos` initial.sql'de (migration'larda değil);
>   16 expo'nun 1'inde `start_date` NULL → S-1 guard'ı teorik değil. Para birimi referans
>   tablosu ve merkezi FX tablosu **YOK** (kur her satırda inline/frozen); `currency`
>   hiçbir tabloda CHECK'siz, sözlük yalnız UI'da. Yönetim UI'ı olmayan referans tablolar:
>   `core_countries`, `core_sectors`, `offices` (PS2 "Reference Data" adayı).

> ## ✅ 2026-07-28 — PS2 CANLIDA (ofis boyutu + tek ödeme formu; 027 + 028)
>
> - **Migration'lar CANLI:** `027_payout_office_method` (commission_payouts +
>   `paid_office_id` FK offices, + `payout_method` ADLI CHECK beş değer) ·
>   `028_agent_office` (sales_agents + `office_id` FK offices + 3 kademeli backfill).
>   Son migration **026 → 028**. Kod commit'leri: **`dc00354`** (PS2-A) · **`e2db297`** (B1) ·
>   **`e289c7d`** (B2) · **`fd516e4`** (C).
> - **NAKİT YÖNÜ ARTIK ÇİFT TARAFLI.** `payments.received_office_id` = para NEREYE GELDİ
>   (giriş, 026) · `commission_payouts.paid_office_id` = para NEREDEN ÇIKTI (çıkış, 027).
>   Tek yönlü kayıt ofis bakiyesini yanlış gösteriyordu; PS3 nakit öngörüsünün ön koşulu.
>   ⚠️ AD FARKI KASITLI: `received_office_id` (payments) ≠ `paid_office_id` (payouts).
> - **TEK SÖZLÜK (H7).** `payout_method` CHECK'i `payments.payment_method` ile AYNI beş
>   değer (`bank_transfer`,`cash`,`cheque`,`credit_card`,`other`). Kısa 'bank'/'cash'
>   sözlüğü AÇILMADI. `payments.payment_method`'a DOKUNULMADI.
> - **REVERSAL OFİSİ SUNUCUDA DEVRALIR (W-8).** İstemciden gelen ofis/method reversal
>   satırında **YOK SAYILIR** — para geldiği yere döner, kullanıcıya sorulmaz. ÜÇ nokta:
>   payment reverse (`contracts.js:737`, INSERT...SELECT) · payout reverse
>   (`payouts.js:114/132`, istemci-gönderme modelinden **sunucu-kopyalama**ya çevrildi) ·
>   transfer'in İKİ INSERT'i (negatif kapama + pozitif kopya, `contracts.js:932/947`).
>   Üçüncüsü ölçümde çıktı: transfer klonunda ofis kopyalanmasaydı sessizce kaybolurdu.
> - **ZORUNLULUK KATMANI AYRIŞTIRILDI (W-6).**
>   DB: `received_office_id` / `paid_office_id` / `office_id` **NULLABLE KALIR** —
>   NOT NULL constraint YOK (canlı ofissiz satırlar var, eski kayıtlar hatasız görünür).
>   FORM + API: **yeni** payment/payout kaydında ofis ZORUNLU (400 "office required").
>   **MUAF:** reversal ve transfer dalları — ofisi orijinalden devralıyorlar, istemciden
>   ofis beklemezler. Ayrışma yapısal (ayrı endpoint / `!isReversal` guard).
> - **⛔ SÜPERSE EDİLEN İKİ KABUL KRİTERİ (Suer onaylı, 2026-07-28):**
>   `PS2-A test (i)` ve `PS1 K-10r` "ofissiz ödeme KABUL (201)" diyordu → artık
>   **"ofissiz → 400 office required"**. Testler SİLİNMEDİ, çevrildi. Gerekçe: "para
>   geldiğini onaylıyorsak nereye geldiğini de biliyoruzdur" (Suer). Muafiyet testleri
>   (reversal/transfer) ofis göndermeden bırakıldı — asıl invaryant onlar.
> - **AGENT → OFİS BACKFILL (Suer kuralı).** 3 kademeli, SIRAYLA: (1) `sales_team`
>   ofis adı içeriyorsa → o ofis · (2) yoksa `sales_group` · (3) yoksa `country` beş ofis
>   ülkesinden biriyse → o ofis · (4) hiçbiri → **Turkey**. Takım etiketi country'den
>   önce gelir (Nigeria Office 12 vs country Nigeria 7). UPDATE **idempotent**
>   (`WHERE office_id IS NULL`), ofis id'leri alt sorguyla (sayısal id gömülmedi).
>   **SONUÇ (canlı, dry-run ile birebir): Turkey 122 · Nigeria 12 · Morocco 10 ·
>   Kenya 5 · China 2 = 151, NULL 0.**
>   Kaynak alanlar Zoho'dan **serbest metin** (021:56, 022:28-29) — FK/CHECK yok, ILIKE ile eşlendi.
> - **AÇIK MADDE — IRAQ VE OFİSSİZ ÜLKELER:** veride `Iraq Office` etiketi var (sales_team 3,
>   country 3) ama `offices` tohumunda YOK. Iraq + Italy/India/Ghana/Spain/Algeria/Malaysia/
>   Lebanon/Egypt/Germany/Iran (~18 agent) kural (4) ile **Turkey**'e bağlandı.
>   Iraq ofis olarak açılacak mı — **KARAR VERİLMEDİ**, Suer'e ait. Açılırsa tek INSERT +
>   ilgili agent'ların office_id güncellemesi yeter (kod değişikliği YOK, S-16r sayesinde).
> - **ÖN-DOLDURMA (W-7, kilit değil — kullanıcı ezebilir):** payment formu → kontratın
>   `agent` rolündeki agent'ın ofisi, yoksa `sr`'ninki, yoksa boş. Payout formu → agent'ın
>   ofisi (statement yanıtına `agent_office_id` eklendi; ek endpoint AÇILMADI).
>   `sales_agents` `SELECT_COLS` sabitine (salesAgents.js:17) `office_id` eklendi — tek yer,
>   GET/POST/PUT üçünü kapsar. Agent formunda ofis DÜZENLEME kapsam dışı (okuma amaçlı).
> - **TARİH DEFAULT'U (W-9):** add-payment tarihi artık BUGÜN ön-dolu. Record-payout zaten
>   bugünle geliyordu, dokunulmadı. Sunucuda tarih zorlaması YOK.
> - **TEK ÖDEME FORMU (W-10).** `contract-list.html` satır içi hızlı ödeme formu KALDIRILDI
>   (payForm/togglePayForm/lockRateIfEur/submitPayment). "+ Payment" artık
>   `contract-detail.html?id=` adresine götürür. Gerekçe: aynı form iki yerde = her alan
>   iki kez bakım. **Yan kazanç: `CURRENCIES` kopyası 3 → 2 düştü** (H-4 borcu küçüldü;
>   kalan: contract-detail.html, sales-agents.html).
> - **OFİS LİSTESİ KODA GÖMÜLMEZ (S-16r) — korundu.** Dropdown'lar `GET /api/offices`'ten;
>   frontend'de ofis sabiti/dizisi/enum YOK. Yeni ofis tek INSERT ile deploy'suz görünür.
> - **Testler:** PS2-A 5/5 · PS2-B1 10/10 · PS2-C 18/18. Regresyon **M1 29/29 · M2 30/30 ·
>   payout 26/26 · PS1 29/29** — sapmasız. Komisyon motoruna (commissions.js,
>   utils/commissionSlices.js) DOKUNULMADI.
> - **GÖRSEL TUR — EKRANDA DOĞRULANANLAR (G1-G6):**
>   G1/G2 contract 4'teki iki test ödemesi reverse edildi → **reversal of #10 = Kenya
>   (devraldı), reversal of #9 = "—"**; PAID 7.440,00 EUR, COLLECTION 40%, **earned 342.00'a
>   döndü** (taban restore) · G3 payment formu: tarih bugün + Office **Turkey** ön-dolu
>   (SR→agent 47) · G4 contract 3'te ofissiz Save → kırmızı **"Office is required"**, satır
>   yazılmadı · G5 Morocco ile 5,00 EUR kaydedildi, listede Morocco · G6 agent 47:
>   Earned 342.00 / Paid 390.00 / Balance −48.00, payout formunda Office **Turkey** ön-dolu.
> - **⚠️ GÖRSEL ONAY EKSİĞİ (bilinçli, Suer kararı):** G7 (ofissiz payout → uyarı) ·
>   G8 (Kenya+cash payout) · G9 (payout reversal devralma) **ekranda koşulmadı**.
>   Testlerle kapsanıyor (U4, U6, PS2-B1 T5) ama **görsel onay alınmadı**. PS3 turunda
>   ilk fırsatta bakılacak.
> - **KALICI TEST VERİSİ (eklendi, SİLİNMEZ):** contract 4'te 2 reversal satırı (net 0) ·
>   contract 3'te "PS2-C office required" 5,00 EUR / Morocco ödemesi.
> - **Bilinen küçükler (aksiyonsuz):** `contract-list.html`'de `.pay-row`/`.pay-form` CSS
>   kuralları artık ölü (zararsız) · `CURRENCIES` hâlâ 2 dosyada kopya · scratch test
>   ortamındaki `expos` stub'ına `organizer_id` eklendi (yalnız test kurulumu; prod
>   `expos`'ta kolon zaten vardı, ürün kodu etkilenmedi).

> ## ✅ 2026-07-28 — PS3-A CANLIDA (schedule UI kartı + default ofis ön-doldurma)
>
> - **Commit `87d162d`** (2 dosya: routes/contracts.js · public/contract-detail.html).
>   Migration YOK — şemaya dokunulmadı. PS1'in görünür karşılığı bu dilimde doğdu.
> - **KART YERİ:** contract-detail.html'de LINE ITEMS ile PAYMENTS **arasında** (:158).
>   Aktif tablo + totals + `<details>` history + [Generate default] / [Add manually].
> - **D-1 — DEFAULT ÜRETİCİ ARTIK OFİS ÖN-DOLDURUYOR** (contracts.js:1318-1329,
>   1346-1354): LEFT JOIN sales_agents ag/sr + COALESCE(ag.office_id, sr.office_id).
>   Çözülemezse NULL, hata dönmez.
>   **⚠️ AYNI KURAL İKİ KATMANDA:** PS2'nin W-7 çözücüsü FRONTEND'dedir
>   (contract-detail.html:284-290, payment formu için); default üretici SUNUCUDA
>   çalıştığı için aynı kuralı SQL ile AYRICA uygular. **Ortak kod YOKTUR** — kural
>   (agent → sr → NULL) değişirse **İKİ YER de** güncellenmelidir.
>   **Gerekçe kayda geçsin:** bu alan boş kalsaydı PS3-B nakit öngörüsü geçmişi
>   gösterir, GELECEĞİ göstermezdi — dilimin varlık sebebi ölürdü.
>   `applyScheduleRevision` ve manuel POST /schedule DOKUNULMADI (ofis istemciden gelir).
> - **PLAN OFİSİ ZORUNLU DEĞİL (U-10) — payments'tan KASITLI FARK.** Ödemede ofis
>   zorunlu ("para geldiyse nereye geldiğini biliriz" — Suer); plan bir TAHMİNDİR,
>   ön-doldurulur, ezilebilir, boş bırakılabilir. Bu tutarsızlık DEĞİL, ayrımdır.
> - **⚠️ KASITLI ASİMETRİ — İLERİDE "HATA" SANILMASIN:** default üretici İNAKTİF ofisi
>   kabul eder, manuel POST REDDEDER (400). Aynı alan, iki kural. Gerekçe: plan bir
>   tahmindir; agent gerçekten o ofise bağlıdır. Bugün oluşamaz (beş ofis de aktif,
>   kapatma UI'ı yok). Düzeltilecek bir şey YOK.
> - **Payout'ta ofis ZORUNLU, method OPSİYONEL** — ölçüldü ve doğrulandı (G8: method
>   boş bırakılarak kayıt geçti). Kasıtlı.
> - **Testler:** PS3-A 8/8 (S1 agent ofisi · S1b SR fallback · S2 NULL ofis 201 ·
>   S3 inaktif ofis plan tahmini · S4 manuel istemci ofisi agent'ı ezmez · S5 revizyon).
>   Regresyon **M1 29/29 · M2 30/30 · payout 26/26 · PS1 29/29 · PS2-A 5/5 ·
>   PS2-B1 10/10 · PS2-C 18/18** — sapmasız. Komisyon motoruna (commissions.js,
>   utils/commissionSlices.js) DOKUNULMADI.
> - **GÖRSEL TUR — EKRANDA DOĞRULANDI (9/9):**
>   V-1 contract 3 kartı: rev 2, Jul 29 6.000,00 (%40) + Dec 2 9.000,00 (%60), USD,
>   15.000,00/15.000,00 matches revenue, Expected office "—" ·
>   V-2 history: rev 1'in satırları superseded, tutarlar DEĞİŞMEMİŞ ·
>   V-3 contract 4 [Generate default] → **"expo required"** (ayırt edici mesaj), satır
>   yazılmadı ·
>   V-4 onay uyarısı ekranda: "This will replace the active plan (revision 2 → 3).
>   The previous plan is kept in history." ·
>   V-5 manuel %30/%30/%40 → 4.500,00 / 4.500,00 / 6.000,00, Σ ≡ 15.000,00 TAM ·
>   V-6+V-7 tek kalem 1.000,00 + ofis boş → KAYIT GEÇTİ, kırmızı **"does not match
>   revenue"** göründü, ofissiz kalem kabul edildi ·
>   V-8 satırlarda edit/delete/"paid" işareti YOK ·
>   G7 ofissiz payout → **"Office is required"**, Paid 390,00 SABİT (kayıt yok) ·
>   G8 Kenya payout → Paid 405,00 / Balance −63,00, satırda Kenya ·
>   G9 Reverse → reversal satırı da **Kenya** (sorulmadan), Paid 390,00 / Balance −48,00
>   → **agent 47 net SIFIRA döndü, earned 342,00 tabanı temiz**.
>   PS2'den devreden G7-G9 görsel borcu **KAPANDI**.
> - **Tur sapmaları (defect DEĞİL):** revision 3 yerine 4 çıktı — [Generate default] iki
>   kez basıldı; her çağrı yeni revizyon üretir, immutable modelde NORMAL ·
>   G8'de 10 yerine 15 EUR + method boş; aritmetik doğru (390+15=405, 342−405=−63).
> - **⚠️ AÇIK GÖRSEL BORÇ — DARALTILDI:** D-1'in **schedule-default** ofis
>   ön-doldurması ekranda görülemedi: contract 3'te agent/SR rolü YOK (ofis NULL),
>   contract 4'te expo YOK (400). **AMA W-7 payment-form ön-doldurması GÖRÜLDÜ** —
>   contract 4'ün ADD PAYMENT formunda OFFICE = **Turkey** ön-dolu geldi (SR BENGU
>   DOGRUER → agent 47 → Turkey). Yani borç yalnız schedule-default dalı.
>   Testlerle kapsanıyor (S1/S1b/S2). Kapanma koşulu: **agent rolü VE expo'su olan**
>   gerçek bir kontrat doğduğunda. En ucuz yol contract 4'e expo bağlamak olurdu —
>   expo_id komisyon formülüne girmez, 342,00 tabanını bozmaz — ama Suer (b) dedi,
>   canlı komisyon verisine dokunulmadı. KARAR VERİLMEDİ, kuyrukta.
> - **KALICI TEST VERİSİ (SİLİNMEZ):** contract 3 schedule **revision 6** — tek kalem
>   1.000,00 USD @ Sep 10, ofissiz, "does not match revenue" (V-6/V-7'nin canlı kanıtı),
>   history 11 satır · agent 47'de 15 EUR Kenya payout + reversal'ı (net 0).
> - **Revizyon birikimi normal:** her [Generate default] ve her manuel kayıt yeni revizyon
>   üretir; satırlar UPDATE/DELETE edilmez (H3/S-5). Rev 6'ya çıkmış olması sağlıklı
>   davranıştır.

> ## ✅ 2026-07-28 — BELGE KONSOLİDASYONU (tek ev = repo; BE1+BE2+BE3)
>
> - **Commit'ler: `4278bc8` (BE2) · `1f53fb6` (BE3).** Kod/DB'ye dokunulmadı.
> - **KİLİTLİ İLKE — TEK EV = REPO.** Her ELL belgesi `~/Projects/ell-docs`'ta yaşar;
>   Claude KB'si bunun bir ALT KÜMESİNİN kopyasıdır. **Repo'da olmayan belge YOKTUR.**
>   Bu ilkeden önce belgeler üç yere dağılmıştı (repo · KB · Desktop/Downloads).
> - **BE1 ÖLÇÜMÜ (12 kök belge sınıflandırıldı):** CANLI **4** (durum defteri = tek durum
>   kaydı · yol haritası = pusula/faz-ilke · bilgi mimarisi = IA/sahiplik · glossary =
>   kanonik terim) · REFERANS 5 · ARŞİV 3 · **⛔ÖLÜ 0**. **ROL ÇAKIŞMASI YOK** —
>   2026-07-27 rol daraltması tutmuş. Suer'in "6 canlı" tahmini ölçümle çürütüldü.
> - **ARŞİVE TAŞINANLAR (git mv, R099 — SİLME YOK):** `ELL_RULES.md` ·
>   `ELL_ROADMAP.md` · `ELL_MUTABAKAT_2026-07-21.md` → `archive/`. Her birinin başına
>   ⛔ ARŞİV banner'ı kondu (güncel durum → defter, faz/ilke → yol haritası).
> - **⚠️ ELL_RULES.md — SINIRDA DOSYA, KARAR VERİLMEDİ:** 365 satırın **13'ü** 2026-06-19
>   kararına aykırı (":44 three systems" · ":46 ELIZA commercial system of record" ·
>   ":69/:78 all three databases" · ":80 eliza-db source of truth" · ":134/:138/:217
>   ELIZA authority writes"). Dosya kendini zaten superseded ilan ediyor (:2), o yüzden
>   ⛔ÖLÜ değil ARŞİV. **13 satır TEK TEK işaretlenmedi — Sentez kararı: dosya arşivde,
>   banner yeter, emeğe değmez.** Banner'ı atlayıp ortadan okuyan yanılır; ⛔ÖLÜ'ye
>   çekilsin mi, açık soru.
> - **REPO'YA ALINAN İKİ YETİM (kök dizin):** `ELL_LOCKED_KARARLAR_OZET.md` (75 satır,
>   kilitli mimari kararlar B1-B20+, "uyum kontrol listesi" — defter buna **3 yerde**
>   referans veriyordu ama dosya repoda YOKTU, ~/Downloads'ta duruyordu) ·
>   `ELL_TEK_KAYNAK_KILIT.md` (147 satır, tek-kaynak ilkesi, kilitli 2026-06-20).
>   Kaynak kopyalar yerinde bırakıldı.
> - **MİMARİ FAZ KANIT BELGELERİ ARŞİVE ALINDI (8 dosya, 📌 banner):** üç derin analiz
>   (LEENA/LIFFY/ELIZA) · gap analizi · cross-DB ölçümü · gerçek durum analizi · oturum
>   özeti · FAZ0 durum. Kaynaklar (`~/Projects`, `~/Downloads`, `~/ELL_schema_dumps`)
>   SİLİNMEDİ. **Bunlar ARŞİV ama ÖLÜ DEĞİL:** yol haritası `:50` kanıt olarak bunlara
>   dayanıyor ("gap analizi (35 ihtiyaç), üç derin analiz") — ama **isim vermeden**.
>   Artık repoda oldukları için zincir kapatılabilir; yol haritasına dosya adı ekleme
>   işi YAPILMADI, açık.
> - **archive/ = 15 dosya** (4 legacy mimari + 3 ⛔ARŞİV + 8 📌kanıt). Kök = **11 .md**.
> - ~~**⚠️ KAYIP BELGE — AKSİYON GEREKTİRİR:** `FAZ1a_DURUM.md` (LIFFY güvenlik izolasyonu,
>   ~120 satır) diskte **hiçbir yerde bulunamadı**; yalnız Claude KB'sinde var. KB
>   yenilenirse kaybolur. Suer KB'den indirip `archive/`'a koymalı.~~
>   → ⛔ **SUPERSEDED — KURTARILDI** (`efbc500`, `archive/`'a alındı). Bkz. 2026-07-29 kaydı.
> - ~~**⚠️ KB BAYAT — ÖLÇÜLDÜ:** Claude KB'si **c44ffeb**'de donmuş. Satır matematiği
>   kanıtladı (defter 1996 = 1965+35−4 ✓ · yol haritası 391 = 371+29−9 ✓ · bilgi
>   mimarisi 248 = 243+6−1 ✓). Yani **PS1 · PS2 · PS3-A kayıtlarının hiçbiri KB'de
>   YOK**. KB okuyan her oturum eksik bilgiyle başlar. **KB yeniden yüklenmeli.**~~
>   → ⛔ **SUPERSEDED — KB TAZELENDİ** (ölçüm 2026-07-29: KB defteri 2355 satır,
>   PS1 + PS2 + PS3-A kayıtlarını İÇERİYOR).
> - **README yeniden kuruldu:** CANLI 4 belge + rolleri · referans belgeler · archive/
>   açıklaması · tek satırlık öncelik kuralı (durum/ilerleme → defter, faz/ilke → yol
>   haritası). Repoya ilk bakan hangisini okuyacağını görür.

> ## ✅ 2026-07-29 — KURAL KÜTÜĞÜ (KK1) + DOC-TAIL BORCU KAPANDI
>
> - **Kod/DB'ye DOKUNULMADI.** Migration yok, endpoint yok. Yalnız belge.
> - **`ELL_LOCKED_KARARLAR_OZET.md` 75 → 146 satır:** sonuna **"İŞ KURALLARI (build fazı)"**
>   bölümü eklendi. Defterdeki **27 iş kuralı** `GRUP-NN` formatında indekslendi —
>   MOT 5 · TAH 4 · ODE 3 · PLN 8 · OFS 5 · SEM 2 · YON 0. Kütük İNDEKSTİR: gerekçe defterde
>   kalır, **çelişkide defter kazanır**. ID tahsisi YALNIZ kütükte, numara asla yeniden kullanılmaz.
> - **ESKİ S- ADLARI BENZERSİZ DEĞİLMİŞ (ölçümle bulundu, varsayım değil):** PS1 (payout) ve
>   PS3 (plan) dilimleri S- numaralarını sıfırdan başlatmış. `S-1` · `S-3` · `S-4` · `S-8`
>   iki AYRI hükümde kullanılıyor → her biri İKİ yeni ID aldı:
>   S-1 → ODE-01 (:642) + PLN-01 (:755) · S-3 → ODE-02 (:656) + PLN-03 (:754) ·
>   S-4 → ODE-03 (:658) + PLN-04 (:725) · S-8 → MOT-01 (:660) + MOT-02 (:762).
>   Tek ID verilseydi kütük iki hükmü birleştirir, indeks olarak doğduğu gün bozulurdu.
> - **AYNA DA ÖLÇÜLDÜ (aynı hüküm, iki ad):** `H3` ≡ `S-5` — defter zaten "(H3/S-5)" diye
>   çift yazıyor (:929) → **PLN-05** tek ID. `W-7` ≡ `D-1` — defter :875'te "AYNI KURAL İKİ
>   KATMANDA" diyor, fark katman (frontend/SQL), hüküm değil → **OFS-05** tek ID, iki-katman
>   bakım uyarısı satıra taşındı. Diğer adaylar ölçüldü, **AYRI çıktı**, birleştirilmedi:
>   W-6 (zorunluluk katmanı) ↔ U-10 (planda ofis opsiyonel) ↔ S-13r (plan/ödeme ofisi farklı
>   olabilir) · H7 (ikinci sözlük açılmaz, kural) ↔ H-4 (CURRENCIES kopyası, borç).
> - **TİRESİZ HÜKÜMLER HASADA ALINDI (elle sayılarak, desen genişletilmeden):** `H7` · `H3` ·
>   `U1a` · `U2a` · `U3a`. İlk tarama `S-[0-9]` deseniyle yapıldığı için tire olmayanlar kaçmıştı.
> - **KÜTÜK DIŞI — KAYDA GEÇSİN, YENİDEN TARTIŞILMASIN:** `K`/`V`/`T` = test ve görsel-tur
>   ID'leri. Tiresiz `S1..S9` (:88-93 açık soru takibi) · `D1..D4` (:445-450 import kararı) ·
>   `D2` (mimari ilke, ~30 geçiş) AYRI namespace'lerdir. **Arama deseni tire'yi zorunlu tutmalı**
>   — gevşetilirse bu üç namespace çöp olarak girer.
> - **B1 + B19 ETİKETLENDİ, METNİ DEĞİŞTİRİLMEDİ:** `[HEDEF — birleşme sonrası]`. Bugün geçerli
>   LEENA gerçeği `organizer_id` + integer PK (S7 v1.2); `organization_id` + UUID birleşme
>   hedefidir. Zaman ekseni farkı, çelişki değil. Kalan B maddelerine etiket KONMADI.
> - **DOC-TAIL BORCU KAPANDI (ölçüldü — üçü de defterde yoktu):** `cd1b2fd` (belge
>   konsolidasyonu defter kapanışı) · `efbc500` (FAZ1a_DURUM.md kurtarıldı, archive'a alındı) ·
>   `95a324a` (ZOHO_USAGE + SECTION_3_2 arşive). **Güncel sayım: kök 11 .md · archive/ 18.**
>   (2026-07-28 kaydındaki "archive/ = 15" yazıldığı gün DOĞRUYDU — dokunulmadı.)
> - **KÖK NEDEN DÜZELTİLDİ:** belgenin kendi tarifi "en üstte en güncel" diyordu; defter
>   ASLINDA kronolojik-artan. Bu bayat cümle KK1'i yanlış yönlendirmişti — düzeltildi.
>   Yeni kayıt `★ SIRADAKİ ADAYLAR`'dan ÖNCE, dizinin sonuna girer.
> - **KAPANAN AÇIK KALEMLER:** KAYIP BELGE (FAZ1a) · KB BAYAT · KB yeniden yükleme ·
>   KK1 kural kütüğü. Hepsi ⛔ SUPERSEDED / üstü çizili işaretlendi. Tarihsel ifadelere
>   DOKUNULMADI — yalnız açık iş kalemleri kapatıldı.
>

> ## ✅ 2026-07-29 — PS3-B ÖNKOŞUL GATE (expo_id komisyon yolunda yok)
>
> PS3-B gate: expo_id komisyon yolunda YOK. Dayanak = statik analiz (grep boş,
> dört yüzey file:line ile çivili) + K0 kalibrasyonu (koddan çıkarılan SQL ekran
> sayılarını yeniden üretti) + B1 (DB-tarafı mekanizma yok).
> Sayısal önce/sonra testi KOŞULMADI: test SQL'i expos'a hiç bakmadığı için
> sonucu koşmadan belliydi — döngüseldi. "Ampirik olarak test edildi" DEĞİLDİR.

> ## ✅ 2026-07-29 — CONTRACT 4 EXPO BAĞLANDI (expo 15) + D-1 GÖRSEL BORCU KAPANDI
>
> - **Yazma:** `UPDATE contracts SET expo_id = 15 WHERE id = 4` — dry-run (ROLLBACK,
>   teyitli) → BEGIN/COMMIT, Suer'in Render Shell'inden. Migration YOK, kod değişikliği YOK.
>   Organizer eşleşmesi önceden doğrulandı (c_org = e_org = 1).
> - **NEDEN UPDATE:** `expo_id`'yi yerinde güncelleyen endpoint YOK. Tek yazma yolu
>   transfer (`contracts.js:853-914`) ve o append-only klon üretir — contract 4'ü bağlamaz,
>   yeni contract doğurur. Bağlama bu yüzden elle yapıldı.
> - **EXPO SEÇİMİ = 15 ("test", start_date 2026-11-18).** Ölçümle seçildi: 4 test fuarı
>   adayından 16 elendi (start_date NULL → plan üretilemez), 4 elendi (2026-03-03, geçmiş →
>   nakit öngörüsü geleceği göstermez), 11 elendi (contract 3 orada + reactivation smoke
>   test fixture'ı). 15'te sıfır visitor/checkin/contract vardı.
>   **⚠️ EXPO 15 ARTIK CONTRACT TAŞIYOR — SİLİNMEZ** (contract 4 zincirinin parçası,
>   S8 E2E'ye kadar).
> - **GATE'İN AMPİRİK KARŞILIĞI (ekranda, bağlama SONRASI):** contract 4 sr earned
>   **342.00** · commissions.html cut Jul 31 Period Total **342.00** (5 satır birebir aynı) ·
>   agent 47 statement earned **342.00**. Üçü de gerçek endpoint'ten, app pool'undan.
>   PS3-B gate'te koşulamayan sayısal doğrulama BUDUR — döngüsellik yok.
> - **D-1 GÖRSEL BORCU KAPANDI.** [Generate default] → Revision 1, 2 satır:
>   Jul 31 7.440,00 EUR (%40) + Oct 19 11.160,00 EUR (%60), Σ 18.600,00 ≡ revenue
>   ("matches revenue"). **Her iki satırda Expected office = Turkey** (SR BENGU DOGRUER →
>   agent 47 → Turkey, SUNUCUDA çözüldü). Oct 19 = expo start_date 2026-11-18 eksi
>   `payment_deadline_days_before` 30. Agent rolü VE expo'su olan kontrat ilk kez doğdu.
> - **KALICI TEST VERİSİ (eklendi, SİLİNMEZ):** contract 4 schedule Revision 1 (2 satır).

> ## ✅ 2026-07-30 — PS3-B CANLIDA (nakit öngörü raporu: ofis × vade, EUR, tamamen türetilmiş)
>
> - **Üç commit canlıda:** `4362054` (çekirdek rapor) · `ca6fb3c` (K14 overdue +
>   K15 on hold) · `430e08d` (K16 planlanmamış gelir sayaçları + etiket hijyeni).
>   **MIGRATION YOK · ŞEMA DEĞİŞİKLİĞİ YOK · SAKLAMA YOK** — her sayı okuma anında
>   türetilir (D2/S-11r). Dört dosya: `routes/cashForecast.js` (YENİ) · `index.js`
>   (mount) · `public/cash-forecast.html` (YENİ) · `main-panel-v2.html` (nav).
>   Komisyon motoruna (contracts.js computeCommission, commissions.js,
>   utils/commissionSlices.js, payouts.js) **DOKUNULMADI**.
>
> - **⚠️ K1-K16 GEÇİCİ ETİKETLERDİR — KALICI ID KÜTÜKTE VERİLECEK.**
>   Buradaki **K4** (Σplan≠revenue işareti) ve **K7** (EUR çevrimi) defterdeki
>   kilitli **K4** (`default_commission_pct`, defter:440) ve **K7** (komisyon motor
>   kuralları, defter:457) **DEĞİLDİR**. İsim-alanı çakışması Sentez bloklarında
>   doğdu, kodda değil. Kütük turunda PLN-NN tahsis edilecek, eski ad parantezde
>   korunacak. Aynı uyarı `cashForecast.js` başında da duruyor, silinmez.
>
> - **MODEL (kilitli hükümler):**
>   **K7** plan satırı EUR'ya rapor anında çevrilir: `amount × contracts.exchange_rate`
>   — kontratın KENDİ kilitli kuru. Yeni kur icat edilmez, "bugünkü kur" kullanılmaz.
>   Plana kur kolonu EKLENMEDİ (S-4 korundu).
>   **K8** tahsilat düşümü: `Σpayments.amount_eur` (reversal'lar dahil NET, status
>   filtresi YOK) aktif plan satırlarına **due_date ASC, eşitlikte item_no ASC**
>   sırasıyla düşülür. Formül komisyon motorunun `effective_pay` teleskop deseniyle
>   BİREBİR AYNI: `LEAST(paid, cum_after) − LEAST(paid, cum_before)`. İkinci formül
>   YAZILMADI. `remaining` yapısal olarak 0'ın altına inmez; fazla tahsilat ayrı
>   sütunda (`excess_eur`), gizlenmez.
>   **⚠️ K8 BİR VARSAYIMDIR, EKRANDA YAZAR:** hangi taksitin kapandığı sistemde
>   KAYITLI DEĞİL (S-6; ölçüm: `payments.schedule_item_id` **0/13 dolu**).
>   Toplam kalan DOĞRUDUR, **ay dağılımı varsayıma dayalıdır**. Gerçek çözüm =
>   satır eşleştirme, AYRI DİLİM.
>   **K9** eksen = **OFİS × VADE**, toplamlar EUR. Para birimi toplama ekseni DEĞİL,
>   satır bilgisi (orijinal tutar + currency satırda görünür). Özgün "ofis × para
>   birimi × vade" tarifi Suer'in iş kuralıyla bu yönde daraldı: **tüm raporlama
>   EUR'dadır, giriş anındaki kilitli kurdan çevrilir** (Zoho'daki yerleşik davranış).
>   **K10 KARA LİSTE (beyaz liste DEĞİL), İKİ KATMANDA:** plan CTE'de
>   `Transferred`+`Cancelled` (tamamen dışarıda) · gruplamada `On Hold` (dışarıda
>   ama K15'te sayılır — CTE'de atılsaydı kalanı hesaplanamazdı).
>   **⚠️ 5. bir statü eklenirse hangi katmana yazılacağı AÇIK KARAR GEREKTİRİR;**
>   yanlış katman sessizce "on hold" muamelesi görür. (D-1'in "AYNI KURAL İKİ
>   KATMANDA" uyarısıyla aynı sınıf.)
>   **On Hold dışlama gerekçesi (Suer):** beklemedeki kontrat ödeme yapmaz — ya
>   iptal edilir ya müşteri başka fuara ikna edilip sözleşme aktarılır.
>   **K14 OVERDUE** = `due_date < CURRENT_DATE AND remaining > 0`. Satır bayrağı +
>   ofis içi alt toplam — AYRI ÜST GRUP DEĞİL (eksen ofis, gecikmiş satırın hangi
>   ofise ait olduğu kaybolmasın). `remaining = 0` olan geçmiş satır OVERDUE değildir
>   ama rapordan da gizlenmez.
>   **K16** planlanmamış gelir sayaçları: `Y` = plansız kontratların Σrevenue_eur ·
>   `X` = planlı ama eksik planlı kontratların Σ(revenue_eur − plan_total_eur).
>   **NETLEŞME YASAK (E1):** yalnız `revenue_eur > plan_total_eur` toplanır; fazla
>   planlanmış kontrat X'i AZALTMAZ (5.000 eksik + 5.000 fazla = 0 sessiz gizleme
>   olurdu). **AYRIKLIK (E2):** her kontrat TEK sayaçta, Y ∩ X = ∅.
>   **K1** NULL ofis GİZLENMEZ — "(No office)" kovası, rapor anında ofis
>   tahmin/çıkarım YAPILMAZ. **K13** plansız kontrat sayacı · **K11** `to_char` ·
>   **K12** organizer scope.
>
> - **VARLIK SEBEBİ — BANNER TOPLAM ALACAK DEĞİLDİR.** Canlı ölçüm: banner
>   **12.065,20 €**, gerçek toplam bakiye **24.945,20 €** (c4 11.160,00 + c3
>   13.785,20). Fark **12.880,00 €** = contract 3'ün planlanmamış geliri.
>   Banner *tarihli planlanmış nakdi* gösterir; toplam alacak AYRI bir rapordur,
>   tek sayıda birleştirilmez (Sentez hükmü). K16 sayaçları farkı görünür kılar.
>
> - **BU DİLİMDE ÖLÇÜLENLER (kayda geçsin, sonraki dilimlerin girdisi):**
>   `payment_schedule_items` (026): `due_date` DATE (TZ yok) · `amount` +
>   `currency` (CHECK YOK) · `percent` · `source` · `expected_office_id` nullable ·
>   `superseded_at`. **`exchange_rate`/`amount_eur` YOK** (S-4: plan bir para
>   hareketi değildir).
>   **Aktif revizyon = `superseded_at IS NULL`** (contracts.js:1162), bayrak kolonu
>   YOK, `MAX(revision)` yalnız sonraki numarayı üretir (:1111) — aktif seçmez.
>   `contracts_status_check` = **Active · On Hold · Transferred · Cancelled**
>   (012:88 + contracts.js:28).
>   `contracts.exchange_rate` numeric(18,8) **NULLABLE, CHECK YOK** (012:74).
>   `contracts.revenue_eur` numeric(14,2) **NULLABLE, CHECK YOK** (012:75).
>   `payments.schedule_item_id` FK var ama **ÖLÜ** — dolduran/okuyan kod YOK
>   (grep BULAMADIM), canlıda 0/13.
>   **E1b — ÖDEME PARA BİRİMİ KONTRATTAN FARKLI OLABİLİR:** 13 ödemenin **10'u**
>   uyumsuz (c1 USD/TRY · c3 USD kontrat, hiç USD ödeme yok · c4 EUR/USD). Ortak
>   payda yalnız `amount_eur`. K8'in EUR üzerinden çalışmasının sebebi budur.
>   `GET /:id/schedule` `SELECT *` ile ham DATE döndürüyor (:1162) → TZ kayması
>   riski. **Ekranda kayma GÖZLENMEDİ** (sunucu muhtemelen UTC) ama sebep
>   ölçülmedi; forecast kendi okumasında `to_char` kullanır (K11). GET düzeltmesi
>   **KUYRUKTA**.
>
> - **Testler:** cash forecast **41/41** (T1-T24). Regresyon **8/8 suite sapmasız**:
>   M1 29/29 · M2 30/30 · payout 26/26 · PS1 29/29 · PS2-A 5/5 · PS2-B1 10/10 ·
>   PS2-C 18/18 · PS3-A 8/8. **Taban contract 4 sr earned 342.00 KAYMADI.**
>   **⚠️ TEST İZOLASYON BORCU (ürün regresyonu DEĞİL, harness kusuru):** suitler
>   TOPLU koşulamıyor — `commission_payouts` FK'si sonraki suitin
>   `DELETE sales_agents` temizliğini bloke ediyor. **Her suite TAZE DB ile koşulur.**
>   Kaydedilmezse sonraki dilimde "regresyon kırıldı" sanılır.
>
> - **GÖRSEL TUR — EKRANDA DOĞRULANDI (8/8):** nav linki · banner 12.065,20
>   (Overdue 0,00 · Upcoming 12.065,20) · Turkey 11.160,00 (c4 Jul 31 Outstanding
>   **0,00** = K8 teleskopun canlı kanıtı; Oct 19 11.160,00) · **(No office)**
>   905,20 (c3 1.000,00 USD → 920,00 EUR = K7 canlı kanıtı, Collected 14,80) ·
>   Contracts'ta c3 kırmızı ⚠ (920 ≠ 13.800), c4 temiz · sayaç satırı
>   `0 without schedule 0,00 · 1 incomplete 12.880,00 · 0 on hold 0,00 ·
>   0 no EUR revenue value` · K8 dipnotu görünür.
>
> - **BİLİNÇLİ ASİMETRİLER (ileride "hata" sanılmasın):**
>   (a) Eksik planlamanın EUR karşılığı var (K16/X), **fazla planlamanın YOK** —
>   dördüncü sayaç açılmadı. Gerekçe: canlıda örnek yok + fazla planlama
>   "planlanmamış gelir" değil, farklı bir anomali; aynı sayaca konursa ikisi de
>   bulanır. `matches_revenue` ⚠ kontrat bazında görünür kılıyor.
>   (b) `exchange_rate` NULL olan planlı kontrat K16/X'e **giremez**
>   (`revenue_eur > NULL` = unknown) — kabul edilmiş davranış, çünkü
>   `contracts_unconvertible`'da görünür.
>   (c) X/Y bir **BÖLÜNMEDİR** (her kontrat tekinde); `contracts_unconvertible` ve
>   `contracts_missing_revenue_eur` ise **TEŞHİS EKSENİDİR** — X/Y ile örtüşebilirler.
>   Bu çifte sayım DEĞİL, tasarım gereğidir.
>
> - **KOZMETİK BORÇ (aksiyonsuz):** sayaç satırında `"1 contracts have incomplete
>   schedules"` — tekil/çoğul uyumsuz, `"1 contract has"` olmalı ·
>   `contracts_unconvertible` sayaç satırında **koşullu görünüyor**, diğer dört
>   sayaç sıfırken bile duruyor (desen tutarsızlığı) ·
>   `excess_eur` `GREATEST(numeric,0)` sıfırken integer `"0"` döndürüyordu →
>   `::numeric(14,2)` ile düzeltildi (test yakaladı).
>
> - **KALICI TEST VERİSİ (SİLİNMEZ):** contract 3 (expo 11, schedule rev 6, tek
>   satır 1.000 USD @ Sep 10, ofissiz) · contract 4 (expo 15, schedule rev 1, iki
>   satır, ofis Turkey). İkisi de PS3-B'nin canlı kabul verisidir; değişirse
>   ekran sayıları kayar.
>   ⚠️ GÜNCELLEME 2026-08-03: contract 4'e payment #14 (10,00 EUR eşleşmiş) +
>   reversal'ı eklendi (TAH-04 görsel turu); ödeme listesi bu blokta yazıldığı
>   günkü haliyle kalmıştır (YON-01).
>
> - **KUYRUKTA (bu dilimde bilinçle yapılmadı):** `GET /:id/schedule` TZ düzeltmesi ·
>   `schedule_item_id` satır eşleştirme mantığı (K8'i varsayımdan çıkarır) ·
>   K1-K16 → PLN-NN kalıcı ID tahsisi (kütük turu) · test harness izolasyonu ·
>   ofis yönetim ekranı · Reference Data admin sayfası · agent formunda ofis düzenleme.

> ## ✅ 2026-07-31 — KK2: PS3-B kural tahsisi + kod etiket sed'i
>
> - **Ne yapıldı:** PS3-B'nin geçici `K1..K16` etiketleri kalıcı kütük ID'lerine tahsis
>   edildi. **Yeni ID:** RAP grubu (RAP-01 EUR-raporlama · RAP-02 sessiz-kaybolmama
>   sayaçları · RAP-03 kara-liste kapsamı) · PLN-09 (rapor EUR çevrimi) · PLN-10 (satır
>   teleskop düşüm) · PLN-11 (overdue) · OFS-06 (NULL ofis gizlenmez) · YON-01..04 (süreç).
>   **Genişletme (yeni ID YOK):** PLN-04/05/06/07 · OFS-01 · TAH-04 çapraz referans.
>   **ID ALMAYAN:** K2→D2 mimari ilkesi · K6/K9-axis/K11 (tasarım-teknik) · K12 (mimari
>   çok-kiracı invaryantı).
>
> - **RAP grubu DAR tutuldu:** yalnız ALAN-BAĞIMSIZ raporlama ilkeleri girer; bir hüküm
>   tek bir alanı (plan/ofis/komisyon/payout) ilgilendiriyorsa o grubun içine yazılır.
>   Emsal: komisyon raporlaması MOT-05'te yaşıyor. Bu yüzden PS3-B raporlama hükümlerinin
>   çoğu PLN'e/OFS'e dağıtıldı; yalnız global EUR-raporlama (RAP-01) ve sessiz-kaybolmama
>   (RAP-02) + kara-liste (RAP-03) RAP'a girdi.
>
> - **KK1 simetri kuralı uygulandı:** K13 (plansız sayaç) + K15 (On Hold dışlanır-ama-sayılır)
>   + K16 (planlanmamış gelir sayaçları) tek bir hükmün üç tezahürüydü → **TEK parent RAP-02**;
>   E1 (netleşme yasak) ve E2 (ayrıklık) alt madde olarak yazıldı.
>
> - **⚠️ AÇIK SORU (bu dilimde ÇÖZÜLMEDİ):** RAP-03'te 5. bir kontrat statüsü eklenirse
>   hangi katmana (plan CTE tam-dışlama vs gruplama-dışlama-ama-sayma) yazılacağı açık karar
>   gerektirir; yanlış katman sessizce "on hold" muamelesi görür.
>
> - **Defter :633 sertleştirildi:** ELL_GLOSSARY.md için devir brief'indeki dayanaksız
>   değişiklik iddiasının TIRNAKLI çekirdek metni kaldırıldı, iddia tarif edildi (alıntı
>   sonraki oturumlarda canlı iddia olarak yeniden doğuyordu). "Kök neden düzeltildi"
>   YAZILMADI — nedensellik kanıtlanmadı, yalnız sertleştirme.
>
> - **Kod sed'i (`55729d6`):** geçici `K` etiketleri kalıcı ID'lere çevrildi (yalnız
>   yorum/etiket satırları; kod/SQL mantığı değişmedi). `K[0-9]` deseni cashForecast.js ·
>   cash-forecast.html · test dosyasında SIFIR (grep doğrulandı). Cash forecast **41/41**.
>   `cashForecast.js` başlığındaki isim-alanı uyarısı kalıcı ID'lere göre yeniden yazıldı.
>
> - **Commit'ler:** `72ff64b` (kütük tahsisi + defter hijyeni, 2026-07-30) · `55729d6`
>   (kod sed'i, LEENA) · bu KK2 kaydı (ell-docs). PUSH YOK — Suer atar.
>
> - **KB yeniden yüklendi (YON-03 kapanış şartı, Suer dolduracak):** KB @ aad1773
>   *(push + KB yükleme sonrası hash yazılınca dilim KAPANIR; teyit yoksa AÇIK.)*

> ## ✅ 2026-08-03 — TAH-04 CANLIDA (ödeme↔taksit eşleştirme: öneri + kullanıcı onayı)
>
> - **Commit'ler:** `e83b805` (kod) · `3d0caef` (regresyon kaydı, boş commit) ·
>   `32131d1` (sayaç kusuru fix). **MIGRATION YOK** — `payments.schedule_item_id`
>   026'da zaten vardı (nullable, UNIQUE/CHECK/ON DELETE yok), kolon eklenmedi.
>   Dört dosya: `routes/contracts.js` · `routes/cashForecast.js` ·
>   `public/cash-forecast.html` · `public/contract-detail.html`.
>   Komisyon motoruna DOKUNULMADI.
>
> - **İŞ KURALI (Suer, kilitli):** eşleştirme = OTOMATİK ÖNERİ + KULLANICI ONAYI.
>   Ödeme formunda taksit alanı en eski açık taksitle ön-doldurulur; kullanıcı
>   ezebilir veya boşaltabilir. Kilit DEĞİLDİR (OFS-05 deseni). Boş eşleştirme
>   geçerli bir durumdur.
>   Önerinin sırası PLN-10 teleskobuyla AYNI: `due_date ASC, item_no ASC`.
>   Ayrışırsa form ile rapor birbirinden kopar — kullanıcı önerileri onayladıkça
>   rapor "düzelirken" bozulurdu.
>
> - **FORMÜL (tek kaynak, ikinci formül yazılmadı — MOT-01):**
>   `matched_i` = o kaleme eşleşmiş `payments.amount_eur` (NET)
>   `cap_i` = **LEAST( GREATEST(plan_eur_i − matched_i, 0), plan_eur_i )**
>   `U` = eşleşmemiş + düşmüş ödemeler (NET)
>   `covered_i` = U'nun cap üzerinde teleskopu · `remaining_i` = cap_i − covered_i
>   `excess_i` = GREATEST(matched_i − plan_eur_i, 0)
>   **⚠️ ÜST KIRPMA NEDEN GEREKLİ:** reversal orijinalin `schedule_item_id`'sini
>   devralır → bir kaleme eşleşmiş toplam NEGATİF olabilir → `plan − matched > plan`
>   olurdu, kalem kendi tutarından fazla borç gösterirdi. T29 bunu kanıtlıyor.
>   **CEBİR (C3'ün yapısal kanıtı):** Σremaining = Σplan − Σmatched − U =
>   Σplan − paid_net → eşleştirme TOPLAMI DEĞİŞTİRMEZ, yalnız AY DAĞILIMINI
>   düzeltir. Testle değil cebirle garanti.
>   **⚠️ ÇİFTE SAYIM YASAĞI:** U yalnız eşleşmemiş ödemeleri içerir. Eşleşmiş
>   ödeme hem kendi kalemine hem U'ya sayılırsa toplam bozulur.
>
> - **⚠️ Ö0a — C8 × C4 ÇAKIŞMASI VE ÇÖZÜMÜ (kalıcı davranış, "bug" sanılmasın):**
>   C8 revizyonda eşleşmelerin düşmesini, C4 ödemenin UPDATE edilmemesini istiyordu.
>   Boşaltma bilgiyi yok ederdi: "hiç eşleşmemiş" ile "revizyonda düştü" ayırt
>   edilemez olurdu (RAP-02 ihlali).
>   ÖLÇÜM: `applyScheduleRevision` superseded satırı **UPDATE ile damgalıyor,
>   SİLMİYOR** → FK hedefi duruyor, referans bütünlüğü kırılmıyor.
>   **KARAR: BOŞALTMA YOK.** "düşmüş" = FK'nın gösterdiği satırın
>   `superseded_at IS NOT NULL` olması. TÜRETİLİR, saklanmaz (D2). Migration yok,
>   ödemeye dokunulmuyor (C4), bilgi kaybolmuyor.
>   **⚠️ KALICI SONUÇ: `schedule_item_id` ASLA kendiliğinden temizlenmez.**
>   Superseded bir satırı göstermeye devam eder — BU NORMALDİR. Kullanıcı yeniden
>   eşleştirene kadar sayaçta görünür. "Temizlenmemiş veri" DEĞİLDİR.
>
> - **REVERSAL / TRANSFER TAŞIMA:**
>   Reversal orijinalin `schedule_item_id`'sini DEVRALIR (TAH-01 deseni) — net
>   sıfırlama taksidin İÇİNDE gerçekleşsin.
>   Transfer: kaynaktaki kapama satırı kaynağın item'ını devralır; **klondaki
>   kopya NULL kalır** — klonun planı YOK (ölçüldü: transfer `payment_schedule_items`'a
>   hiç dokunmuyor, klon plansız doğar). KAÇINILMAZ NULL; klonun planı sonradan
>   üretilince kullanıcı elle eşleştirir.
>   **⚠️ OFS-05 SINIFI BORÇ:** aynı devralma kuralı reversal ve transfer bloklarında
>   AYRI yazılıyor, ortak kod yok — kural değişirse İKİ yer de güncellenir.
>
> - **C9 — GERİYE DÖNÜK GÖÇ YAPILMADI.** Mevcut ödemeler eşleşmemiş başladı.
>   Gerekçe: otomatik doldurma teleskop varsayımını veriye KALICI yazar ve geri
>   alınamaz — kullanıcının bilinçli seçimi ile göç ürünü veride AYIRT EDİLEMEZ olur.
>   **⚠️ Contract 1'in 3 ödemesi (Transferred, plansız) HİÇBİR ZAMAN eşleşemez →
>   %100 kapsama yapısal olarak imkânsız. Karma mod (C1) KALICI gerçektir,
>   geçiş durumu değil.**
>
> - **GÖRSEL TUR — BİR KUSUR YAKALADI, DÜZELTİLDİ (`32131d1`):**
>   Reversal sonrası sayaç `1 payments matched — 10.00 EUR` gösteriyordu; satır
>   ve banner ise doğru (net 0) idi.
>   **KÖK NEDEN (ölçüldü):** `paystat` sorgusu reversal'ı (`reverses_payment_id
>   IS NULL` ile) eliyordu ama **TERSLENMİŞ ORİJİNALİ elemiyordu**. Sayaç ile
>   satır/banner FARKLI KAYNAKTAN besleniyordu (paystat vs matched CTE).
>   **AYNI KUSURUN İKİNCİ UCU:** `unmatched` EUR'u BRÜT idi (33.063,80), oysa
>   net 7.454,80. Aynı düzeltmeyle net oldu.
>   **KARAR:** `matched` = `schedule_item_id` dolu VE `reverses_payment_id IS NULL`
>   VE kendisi terslenmemiş. Sayı ve EUR TEK KAYNAKTAN. Sayaç · satır · banner
>   üçü aynı tanımı kullanır (RAP-02: sayaç panonun doğruluk göstergesidir,
>   tabloyla çelişemez).
>   **⚠️ Danışmanın "2 bekleniyordu" hipotezi ÖLÇÜMLE ÇÜRÜDÜ** — sayı 1'di çünkü
>   reversal zaten eleniyordu; hata terslenmiş orijinaldeydi. Ölçüm hipotezden önce.
>
> - **Ekranda doğrulandı (deploy sonrası):** gün-1 değişmezlik (banner 12.065,20 ·
>   Turkey 11.160,00 · (No office) 905,20 · c3 kırmızı ⚠) · Matched sütunu render
>   ediliyor, Collected'dan görsel ayrı (C1) · 10 EUR eşleştirme → Matched 10,00,
>   Outstanding 11.150,00, banner 12.055,20 · reversal → ofis (Turkey) ve item
>   devralındı, banner 12.065,20'ye döndü · fix sonrası sayaç
>   `0 matched — 0,00 · 3 unmatched — 7.454,80 (net)`.
>   **TABAN contract 4 sr earned 342.00 KAYMADI.**
>
> - **⚠️ REGRESYON — DÜRÜST BEYAN, "8/8" DEĞİLDİR:**
>   8 eski suite dosyası (M1/M2/payout/PS1/PS2-A/PS2-B1/PS2-C/PS3-A)
>   **`/private/tmp` scratchpad'inden OS temizliğiyle SİLİNMİŞTİ** — koşulamadılar.
>   Yerine dokunulan dört yol için assertion'lar YENİDEN YAZILDI (R1-R8, kütükten
>   okundu, uydurulmadı): OFS-03 ofissiz ödeme → 400 · TAH-01 reversal devralma ·
>   SEM-01 method sözlüğü · PLN-05 revizyon damgalama · PLN-01 yarım plan → 400 ·
>   A4 transfer klon plansız · PLN-10 gün-1 birebir · OFS-06 NULL ofis kovası.
>   Suite 67/67 (41 PS3-B + T25-T38 + R1-R8).
>   **⚠️ TEST BORCU: suitler `/private/tmp`'de yaşıyor, OS temizliği bir kez sildi.
>   İkinci kez olursa yine ölçüm kaybı olur. Repoya alınması AYRI DİLİM**
>   (hardcoded `/Users/nsa` yolları + `ell_comm_test` bağımlılığı temizlenmeli).
>
> - **KALICI TEST VERİSİ (eklendi, SİLİNMEZ):** contract 4'e 2026-08-03'te
>   payment #14 (10,00 EUR, ofis Turkey, Oct 19 taksitine eşleşmiş) + reversal'ı
>   girildi. Görsel turun eşleştirme/reversal kanıtıdır; silinirse o kanıt kaybolur.
>
> - **KUYRUKTA (bu dilimde bilinçle yapılmadı):** test suitlerinin repoya alınması ·
>   `GET /:id/schedule` TZ düzeltmesi · RAP-03 5. statü açık sorusu · ofis yönetim
>   ekranı · Reference Data admin · Faz 4 rol/yetki.
>
> - **KB yeniden yüklendi (YON-03 kapanış şartı, Suer dolduracak):** KB @ 42b3a6b

> ## ✅ 2026-08-04 — TEST ALTYAPISI REPOYA ALINDI (`tests/`, setup yeniden kuruldu)
>
> - **Commit `0542fc2`.** Ürün koduna DOKUNULMADI; `package.json`'da yalnız
>   `scripts.test` + `scripts.test:setup` eklendi (bağımlılık DEĞİŞMEDİ,
>   framework EKLENMEDİ). Migration yazılmadı.
>
> - **SORUN:** test suitleri `/private/tmp` scratchpad'inde yaşıyordu; OS
>   temizliği **9 dosyayı sildi** — 8 suite (M1/M2/payout/PS1/PS2-A/PS2-B1/
>   PS2-C/PS3-A) **ve `setup_comm_db.js`**. Hiçbiri commit edilmemişti, tek kopya
>   oradaydı. Arama: `/private/tmp` · `/tmp` · `~/Desktop` · `~/Projects` ·
>   git geçmişi → **BULAMADIM**. `ell_comm_test` yalnız postgres onu tuttuğu için
>   yaşıyordu; düşseydi kimse yeniden kuramazdı.
>
> - **YENİ YAPI:** `tests/test_cash_forecast.js` (taşındı) ·
>   `tests/setup_test_db.js` (YENİ) · `tests/README.md` (koşum talimatı).
>   Taşınan testte YALNIZ İKİ SATIR değişti: mutlak `BE` yolu →
>   `path.join(__dirname,'..')` · `new Pool({host:'localhost',...})` →
>   `process.env.TEST_DATABASE_URL || 'postgresql://postgres@localhost:5432/ell_comm_test'`.
>   **Test mantığı/assertion/fixture DEĞİŞMEDİ** — T3 ancak böyle ölçülebilirdi.
>
> - **⚠️ SETUP HATIRADAN DEĞİL ÖLÇÜMDEN YAZILDI (YON-01):** silinmiş dosyanın
>   hatırlanan hali yeniden yazılmadı. Ayakta duran `ell_comm_test` şeması
>   ölçüldü: **canlı 10 tablo − migration'ın ürettiği 8 = 2 STUB**
>   (`expos`, `core_countries` — 012-028 aralığında yok, FK hedefi).
>   Stub şemaları `\d` ile çıkarıldı: `expos` (id serial PK, name, start_date,
>   end_date, organizer_id) seed id 1-5 org=1 · `core_countries` (code char(2) PK,
>   name varchar(100) NOT NULL) seed TR/MA/NG/KE/CN.
>   **FK sırası ölçüldü:** `expos` → 012'den ÖNCE (`contracts.expo_id`) ·
>   `core_countries` → 026'dan ÖNCE (`offices.country_code`).
>   Migration 012→028, 17 dosya, atlanan yok. `offices` (+5 seed) 026'dan gelir,
>   stub DEĞİL.
>
> - **T3 KANITI — iki değişken AYRI ayrı izole edildi:**
>   (1) referans koşusu, taşımadan önce, eski DB → **67/67**
>   (2) taşınmış test, ESKİ DB'de (tek değişken = taşıma) → 67/67 BİREBİR
>   (3) taşınmış test, YENİ setup'la sıfırdan → 67/67 BİREBİR
>   (4) ikinci `test:setup && test` → 67/67 BİREBİR (**setup IDEMPOTENT**)
>   Test adları da birebir karşılaştırıldı, yalnız sayı değil.
>   **TABAN contract 4 sr earned 342.00 (T35) geçti.**
>
> - **T2 — SIR TARAMASI:** `tests/` altında connection string/şifre/token YOK.
>   `JWT_SECRET = 'test-only-secret-not-production'` literal duruyor — açıkça
>   non-production test imza anahtarı, gerçek credential değil.
>
> - **⚠️ AÇIKTA KALAN TEST KAPSAMI (bu dilimde bilinçle yapılmadı — T4):**
>   Silinen 8 suite YENİDEN YAZILMADI; altyapı önce, kapsam sonra.
>   Bugün **test edilmeyen** alanlar (Ö5'te kütükten türetildi, defterdeki test
>   sayıları TARİHSEL ve doğrulanamaz):
>   M2 kesim raporu (MOT-01/03/04/05) · payout cari hesap (ODE-01/02/03) ·
>   PLN-02/03/06/07/08 default-gen matematiği · OFS-04/05 · PS2-C agent office.
>   R1-R8 + T35'in kapsadıkları AYRI: OFS-03 · TAH-01 · SEM-01 · PLN-05 ·
>   PLN-01 · A4 transfer · PLN-10 gün-1 · OFS-06.
>   **Yeniden yazım AYRI DİLİM; kapsam listesi budur.**
>
> - **ÖLÇÜLMEDİ:** `ell_comm_test` şemasının canlı LEENA şemasıyla birebir
>   aynılığı (canlıya dokunulmadı) · CI'da koşum (CI yok) · başka host/OS'ta
>   koşum (yalnız bu makinede doğrulandı) · `.gitignore` (repoda yok, bu
>   dilimde açılmadı — yanlış desen dosya yutabilir).
> - **KB yeniden yüklendi: `1b181d1`** (YON-03). Yüklenen belgeler:
>   `ELL_DURUM_DEFTERI_v2.md` + `ELL_LOCKED_KARARLAR_OZET.md` (son 10 commit'te
>   değişen tek iki dosya, `git log --name-only` ile ölçüldü).

> ## ✅ 2026-08-04 — AGENT FORMUNDA OFİS DÜZENLEME (create/edit)
>
> - **Commit `ff080fb`.** MIGRATION YOK — `sales_agents.office_id` 028'de zaten vardı.
>   Komisyon/ödeme/payout/schedule yollarına DOKUNULMADI.
>
> - **KUSUR (tam hali):** kolon 028'de vardı, `salesAgents.js` GET **okuyordu**
>   (SELECT_COLS), ama INSERT ve UPDATE **yazmıyordu**, `sales-agents.html`'de
>   ofis alanı **yoktu** → elle eklenen agent ofissiz doğuyor ve UI'dan düzeltilemiyordu.
>
> - **⚠️ ETKİ (doğru hali):** ofissiz agent bir ödemeyi **DOĞRUDAN REDDETTİRMEZ** —
>   OFS-03 zorunluluğu `payments.received_office_id` üzerindedir, `sales_agents.office_id`
>   üzerinde DEĞİL. Gerçek sonuç: OFS-05 ön-doldurma zincirinin (`agent → sr → NULL`)
>   `agent` adımı boş dönüyordu → ofis alanı sessizce boş geliyor, kullanıcı fark
>   etmeden devam edebiliyordu. **Sessiz eksiklik.**
>
> - **Yapılan:** POST INSERT + PUT UPDATE'e `office_id` (nullable); `officeExists`
>   DB varlık kontrolü (is_active şartı YOK — düzenlemede pasifleşmiş ofis korunur);
>   geçersiz → 400. Form Office `<select>` **`GET /api/offices`'ten** (OFS-01: koda
>   gömülmedi; boş = "— No office —"). Liste Office sütunu (client-side ad çözümü).
>   **OFS-05 zinciri DEĞİŞMEDİ** — yalnız `agent` adımının kaynağı UI'dan doldurulabilir oldu.
>
> - **Ofis ZORUNLU DEĞİL** (NULL kabul, OFS-04 ruhu).
>
> - **⛔ 151 KAYDA DOKUNULMADI:** ölçüm 151 dolu / 0 NULL (Zoho import'undan geldi) →
>   **backfill/veri düzeltme YAPILMADI**, gerek yoktu.
>
> - **Testler:** `tests/test_agent_office.js` (YENİ, ayrı dosya) A1-A6 → 6/6; `npm test`
>   zincirledi. Regresyon cash-forecast **67/67**, **TABAN contract 4 sr earned 342.00
>   (T35) geçti**. Toplam 73.
>
> - **⚠️ ÖLÇÜLMEDİ:** görsel tur (Suer ekranda doğrulayacak) · pasif ofisli agent'ın
>   edit'te ofisinin korunup korunmadığı canlıda (yalnız kod: is_active şartsız varlık).

> ## ✅ 2026-08-04 — M4 TEST KAPSAMI: ODE + MOT (kütükten yeniden yazım)
>
> - **AMAÇ:** OS temizliğinin sildiği 8 suite'in yerine, **KÜTÜKTEN** yazılmış test
>   seti. Kaynak kütük; eski dosyalar yok, **kopya değil, sayı hedefi yok** (defterdeki
>   29/30/26… TARİHSEL, doğrulanamaz). Ürün koduna DOKUNULMADI — ikisinde de FAIL yok.
>
> - **ODE turu (commit `b5b6384`):** `tests/test_payouts.js`, **12 test / 3 kural**.
>   ODE-01 cari hesap (earned/paid/balance türetilir) · ODE-02 fazla ödeme negatife
>   düşer + reversal mahsup · ODE-03 immutable (düzeltme=negatif reversal).
>   ⚠️ **O1b deseni** (kayda değer): bir kolonun **YOKLUĞUNU şema üzerinden** kanıtlar
>   (commission_payouts'ta dönem/kesim kolonu yok) — modelin sessizce bozulmasını engeller.
>   ⚠️ **O3d:** cross-agent reversal koruması **kütükte YAZMIYOR, koddan ölçüldü**
>   (payouts.js:151).
>
> - **MOT turu (commit `32717fe`):** `tests/test_commissions.js`, **12 test / 5 kural**.
>   MOT-01 tek kaynak · MOT-02 tahsilat oranı (plan değil) · MOT-03 tavan/(cap) ·
>   MOT-04 kesim (gün≤15→15, ≥16→son) · MOT-05 rapor yalnız hak edilmiş.
>   ⚠️ **M01a 3-AYAK (döngüsellik önlemi):** M1 computeCommission == statement (SLICE_CTES)
>   == **EL HESABI literal 342.00** (base 17.100 × %5 = 855; 855 × 0,40 = 342). İki yol
>   aynı yanlış formülü kullansa eşit çıkardı → üçüncü ayak (sabit sayı) bunu yakalar.
>   ⚠️ **MOT-02 eski M2 listesinde YOKTU** (tarihsel eksik) → bu turda yazıldı, eksiklik
>   devralınmadı.
>   ⚠️ Ölçüm: `computeCommission` SLICE_CTES kullanmıyor (AYRI M1 yolu); MOT-01'in
>   "tek kaynak" iddiası dilim CTE'leri içindir, (a)/(b) farklı yollar → eşitlikleri anlamlı.
>
> - **Toplam test: 97** — `test_cash_forecast.js` 67 · `test_agent_office.js` 6 ·
>   `test_payouts.js` 12 · `test_commissions.js` 12. `npm test` dördünü zincirler,
>   idempotent, **TABAN 342.00** (T35 + M01a el-hesabı) korunuyor.
>
> - **⚠️ AÇIKTA KALAN KAPSAM (HÂLÂ test edilmiyor):** PLN-02/03/06/07/08 (default-gen
>   matematiği/revizyon/plan) · OFS-04/05 · PS2-C agent office backfill · **tüm kenar
>   durumlar** (sıfır bakiye, kesim sınırı çoklu dönem, EUR-dışı, reversal ofis devralma
>   W-3). M4 sürüyor; sıradaki turlar bu listeden seçilir.
>
> - **⚠️ ÖLÇÜLMEDİ:** eski 8 suite'in bu 24 testle örtüşme oranı (dosyalar yok) ·
>   kenar durumların riski (bu turların testlerinden çıkacak) · canlı doğrulama (test turu).

> ## ✅ 2026-08-04 — M4 TEST KAPSAMI: PLN (plan üretimi, kütükten)
>
> - **PLN turu (commit `84135a7`):** `tests/test_schedule.js`, **15 test / 7 kural**,
>   **FAIL yok** — plan üretim kodu doğru (son turlarda sessiz kalmış olsa da).
>   PLN-01 yarım plan yasak (4 önkoşul NULL→400+0) · PLN-02 %40/%60 (d2>d1: 400/600;
>   d2≤d1: tek %100) · PLN-03 · PLN-04 (planda kur yok, şema) · PLN-05 immutable/revizyon ·
>   PLN-06 (ödeme durumu saklanmaz, şema) · PLN-07 (Σ≠revenue→warning).
>   Ürün koduna DOKUNULMADI.
>
> - **⚠️ PLN-03 tam davranışı (kütükten, doğrulandı):** yuvarlama artığı **İKİNCİ
>   kaleme** yazılır (default üretici: `a1=round2(revenue×0,40)`, `a2=revenue−a1` →
>   artığı a2 emer), Σ kalem ≡ revenue TAM. El hesabı: 100,01 × %40 = 40,004 → 40,00 (ilk);
>   100,01 − 40,00 = **60,01** (ikinci); Σ = 100,01. "Son" değil, "ikinci" — kütük kazandı.
>
> - **Ö3 KARARI — FRONTEND KATMANI TEST EDİLMEDİ, BORÇ DEĞİL:** ölçüldü ki
>   `contract-detail.html generateDefault()` yalnız `POST /schedule/default` çağırıyor;
>   **client-side %40/%60 matematiği YOK** (grep boş) → plan üretim matematiği SERVER-ONLY,
>   frontend duplikasyonu yok → sunucu-testi PLN'i TAM kapsar. (OFS-05 iki-katman borcu
>   ödeme-formu ofis ön-doldurmasıdır, PLN dışı — o borç ayrı, hâlâ açık.)
>
> - **PLN-09/10/11 çift yazılMADI** — cash-forecast suite'inde zaten test ediliyor.
>
> - **Toplam test: 112** — cash-forecast 67 · agent 6 · payouts 12 · commissions 12 ·
>   schedule 15. `npm test` beşini zincirler, idempotent, **TABAN 342.00** korunuyor.
>
> - **⚠️ AÇIKTA KALAN KAPSAM (M4 sürüyor):** PLN-08 (plan≠ödeme ofisi zorlanmaz) ·
>   OFS-04/05 (+ OFS-05 frontend/SQL iki-katman borcu) · PS2-C agent office backfill ·
>   **tüm kenar durumlar** (sıfır bakiye, kesim sınırı çoklu dönem, EUR-dışı, W-3 reversal
>   ofis devralma). Yazıldı: ODE(3) + MOT(5) + PLN-01..07.
>
> - **⚠️ ÖLÇÜLMEDİ:** eski PS1 suite'inin bu 15 testle örtüşmesi (dosya yok) ·
>   kenar durumların riski · frontend office-prefill katmanı (OFS-05, ayrı borç) · canlı doğrulama.

> ## ✅ 2026-08-04 — OFİS YÖNETİM EKRANI + kapalı-ofis ad çözümü (M2)
>
> - **Commit `3ebe8b5`.** `routes/offices.js` (GET param + POST + PUT) · `offices.html`
>   (YENİ ekran) · üç ekran ad-çözümü düzeltmesi · `main-panel-v2` nav · `tests/test_offices.js`.
>
> - **Migration YAZILMADI:** `is_active boolean NOT NULL DEFAULT true` 026'da zaten
>   vardı (ölçüldü). Kapatma = `is_active=false`.
>
> - **⛔ DELETE endpoint'i YAZILMADI (gerekçe ölçümle):** canlıda 5 ofisin **hepsinin
>   bağlı kaydı var** (Turkey 122 agent + payments/sched; Morocco/Nigeria/Kenya/China
>   agent'lar) — 4 FK hepsi RESTRICT → bugün **tek ofis bile silinemez**; DELETE yazılsa
>   ilk günden ölü kod olurdu. Ofis geçmiş kayıtlarda referanstır.
>
> - **AD ÇÖZÜMÜ ÇAKIŞMASI M2 tarafından YARATILDI → aynı dilimde KAPATILDI:** ekran ilk
>   ofisi kapattığı an, `officeName` GET /api/offices (aktif-only) besleniyorsa geçmiş
>   kayıtların ofis adı `#id`'ye dönerdi (RAP-02 sınıfı: aynı bilgi iki kaynaktan çelişir).
>   **Desen:** ad çözümü **tüm ofislerden** (`?include_inactive=1`), dropdown **yalnız aktiften**.
>   Düzeltilen 3 ekran: `contract-detail.html` (payments/schedule ofis sütunu + ödeme
>   dropdown) · `sales-agents.html` (liste + form) · `agent-statement.html` (payout sütunu +
>   record-payout dropdown). **`cash-forecast.html` DOKUNULMADI** — backend LEFT JOIN, bağışık.
>
> - **⚠️ İKİ DESEN YAN YANA (açık borç):** ad çözümü artık iki farklı desende —
>   **backend-JOIN** (cash-forecast) vs **client-side eşleme** (diğer üç ekran). Hangi
>   desende birleşileceği KARAR gerektirir, bu dilimde çözülmedi.
>
> - **⚠️ ROL GATE YOK:** yazma endpoint'leri (POST/PUT) bugün **her kimliği doğrulanmış
>   kullanıcıya** açık (`offices.js` TODO Faz 4). **BİLİNÇLİ**, unutulmuş değil — kod
>   yorumunda da yazılı.
>
> - **Kapatma ONAY adımı:** ekranda `is_active` aktif→kapalı geçişinde `confirm()`
>   ("Close office 'X'? … Existing records keep their office."). Engelleme değil, onay.
>
> - **Iraq:** ofis VERİSİ girilmedi (kod turu) — Iraq/ofissiz ülkeler kararı (defter:827)
>   AYRI, hâlâ açık.
>
> - **Testler:** `tests/test_offices.js` (YENİ) **F1-F8 / 8 test**, FAIL yok. Toplam
>   **120** (cash-forecast 67 · agent 6 · payouts 12 · commissions 12 · schedule 15 ·
>   offices 8). İdempotent, **TABAN 342.00** korunuyor, mevcut testler bozulmadı.
>
> - **⚠️ ÖLÇÜLMEDİ:** görsel tur (Suer) · iki-desen birleşme kararı · kapalı ofisli
>   canlı senaryo (bugün kapalı ofis yok) · ad-çözümü düzeltilen 3 ekran dışında başka
>   gösterim yeri olup olmadığı (tam repo taranmadı).

> ## 📋 2026-08-04 — HEDEFE MESAFE ÖLÇÜMÜ (envanter turu; kayıt 2026-09-09'da yazıldı)
>
> ⚠️ **GECİKMİŞ KAYIT.** Ölçüm 2026-08-04'te yapıldı, deftere o gün yazılmadı;
> bulgular bir ay boyunca yalnız sohbet geçmişinde durdu. Aradaki sürede ELL'e
> hiç dokunulmadı (ell-docs `e911166`'da sabit; LEENA finans motoru —
> contracts/commissions/payouts/cashForecast/commissionSlices — `3ebe8b5..HEAD`
> aralığında HİÇ değişmedi, ölçüldü). Sayılar ölçüm günündendir.
>
> - **AMAÇ:** kuyruk organik büyümüş bir listeydi, HEDEFE giden yol haritası
>   değildi. Bu tur "satışçıya açılma" eşiğine ne kaldığını ÖLÇTÜ.
>
> - **⚠️ ÜÇ VARSAYIM ÇÜRÜDÜ:**
>   1. **LEENA'da `users` TABLOSU YOK.** Kolon değil, TABLO. `migrations` +
>      `initial.sql` grep BOŞ. Daha önce "users.office_id kaç kullanıcıda dolu"
>      diye sorulmuştu — kolon da yok, tablo da. JWT yalnız `organizer_id` taşıyor.
>   2. **LIFFY "read-only seed, aktif geliştirilmiyor" DEĞİL.** Kod
>      `~/Projects/liffyv1/backend/` altında: **154 .js dosyası**, migrations
>      001-052, ~40 route. Modüller: mining/prospecting · campaigns · leads ·
>      pipeline · quotes · companies/persons · userManagement · zoho.js ·
>      verification. Tam bir prospecting/CRM/campaign/quote platformu.
>      Son commit **2026-06-12**. (Önceki "liffyv1 kökü boş" ölçümü YANLIŞ
>      DİZİNE bakmıştı — kök .md ağırlıklı, kod `backend/`'de.)
>   3. **Rol/yetki gate YOK.** `authMiddleware.js:13-18` yalnız KİMLİK doğruluyor
>      (JWT verify → `req.organizer_id`). Yetki kontrolü yok → geçerli JWT'si olan
>      **altı Finance sayfasının hepsini** (Contracts · Sales Agents · Commissions ·
>      Cash Forecast · Offices · Agent Statement) görür VE değiştirir.
>
> - **⚠️ KİLİTLİ HÜKÜMLE ÇELİŞKİ (karar Suer'de, bu turda çözülmedi):**
>   Faz 4 (rol/yetki) "EN SONA" diye kilitliydi. Ölçüm gösteriyor ki
>   **satışçıya açılmak rol gate olmadan mümkün değil** — bir satışçı bugün
>   giriş yapsa tüm finans verisini görür ve değiştirir. Sıralama kararı
>   Suer'in; ama kilitli hüküm ile ölçüm çelişiyor, kayda geçer.
>
> - **CONVERT KÖPRÜSÜ YARI KURULU:** LEENA `routes/contracts.js:2-10` —
>   "LIFFY signed quote (payload) → LEENA contract INSERT" endpoint'i VAR,
>   ama **PAYLOAD-DRIVEN**: cross-system fetch YOK. Convert eden, quote verisini
>   body'de elle gönderir. Canlı LIFFY→LEENA otomatik aktarım YOK.
>   (Transport, LIFFY aktivasyonuna ertelenmişti.)
>
> - **KATALOG LIFFY'DE, LEENA'DA DEĞİL:** `products` (LIFFY 050:132) ·
>   `product_prices` (050:180) · `exchange_rates` (050:227) · `quotes` (051:31) ·
>   `quote_line_items` (051:112). **242 SKU import'u bu yüzden LIFFY işidir.**
>
> - **İKİ SİSTEM AYRI DB:** LEENA `leena_v401` (PGDATABASE) · LIFFY
>   `process.env.DATABASE_URL`. Paylaşımlı DB YOK, canlı API çağrısı YOK.
>   `canonical_expo_id` LIFFY `expos`'ta VAR (050:90) ama **soft UUID ref, FK YOK**
>   ("cross-system integration key, no FK"). Doluluk ÖLÇÜLMEDİ.
>
> - **İKİ SİSTEMDE DE VAR OLAN KAVRAMLAR (birleşme envanteri, tasarım YAPILMADI):**
>   `offices` (LEENA 026 + LIFFY 050) · `expos` (ikisinde de) ·
>   `companies` (LIFFY 046; LEENA'da kontratta `company_name`) ·
>   `users` (LIFFY VAR, LEENA YOK) · agents (LEENA `sales_agents`;
>   LIFFY `sales_owner_user_id` 048).
>
> - **8 CORE WORKFLOW (gereksinim belgesi Part 2) — bugün nerede:**
>   2.1 Lead Acquisition → LIFFY · 2.2 Sales Cycle → LIFFY quotes + convert
>   yarı-kurulu · 2.3 Contract Management → LEENA ✓ · 2.4 Catalogue Production →
>   LIFFY (tablolar var, akış ölçülmedi) · 2.5 Expo Operations → LEENA EMS ✓ ·
>   2.6 Financial Operations → LEENA finance ✓ · 2.7 Communication → LEENA emails
>   + LIFFY campaigns · 2.8 Reporting → ELIZA + LEENA reports.
>
> - **LIFFY DB'YE BAĞLANILAMADI:** `backend/.env` var ama DB/DATABASE/PG anahtarı
>   İÇERMİYOR; `db.js:20` `process.env.DATABASE_URL` istiyor; shell'de UNSET.
>   → Bağlantı yalnız Render runtime env'inde. Katalog doluluğu, quote sayısı,
>   `canonical_expo_id` doluluğu, LIFFY users sayısı **ÖLÇÜLEMEDİ** — Render
>   Shell'den Suer koşabilir.
>
> - **SATIŞÇI EŞİĞİ — ölçülmüş engel listesi (üçü birbirine bağlı):**
>   1. per-user hesap: LEENA'da `users` tablosu YOK
>   2. rol/yetki matrisi: YOK (`authMiddleware` yalnız kimlik)
>   3. user → agent/office bağı: tablo olmadığı için yok
>   ⚠️ Zincir: rol gate user olmadan yazılamaz; convert'in kimin adına yapıldığı
>   user olmadan bilinemez. **İlk halka `users`.**
>
> - **ÖLÇÜLMEDİ (bu turda bilinçle, zaman sınırı):** LIFFY deploy durumu ·
>   convert'in fiili kullanımı (kaç kontrat convert'ten doğdu) · Katalog Production
>   ve Reporting akışlarının işlevselliği (dosya varlığı ölçüldü, çalışması değil) ·
>   ELIZA'nın bugünkü durumu · birleşme TASARIMI (nasıl birleşecekler — ayrı iş) ·
>   gereksinim belgesi Part 3/4.

> ## ✅ 2026-09-09 — ui2 KABUK DİLİMİ: yeni arayüz iskeleti (nav + kimlik + yetki kancası)
>
> **Ne:** Yeni ELIZA arayüzünün ilk taşı — `public/ui2/` altında **KABUK**. Bu bir
> deneme/atılacak UI DEĞİL: zamanla **ASIL sistem** olacak (eski taraf en sona kapanır).
> Bu dilim **YALNIZ KABUK** — ekran içeriği yok, Finance dahil hepsi placeholder.
>
> **Üç katman bilinçle ayrıldı (dilimin çekirdek kararı):**
> 1. **İSKELET** (kabuk/nav/auth/veri-katmanı/yetki-kancası) = GERÇEK, şimdi kuruldu.
> 2. **KAPSAM** (ekranlar) = artımlı, dilim dilim gelecek (bugün boş).
> 3. **BACKEND YETENEĞİ** (rol motoru) = **Faz 4, TAKLİT EDİLMEZ.** Sahte "yetki
>    gerekli" ekranı YOK; yetki kancası bugün gerçek veri-modelini (users yokluğunu)
>    yansıtır, uydurmaz.
>
> **Kabuk deseni — vanilla `shell.js` include (emsal: `leena-fetch.js`/`leena-toast.js`):**
> framework/npm bağımlılığı YOK. Nav içeriği **TEK KAYNAK** `public/ui2/shell.js`'te
> yaşar; sayfalar yalnız `<div id="ui2-nav">` mount + `<script src="shell.js">` taşır,
> nav HTML TAŞIMAZ (30 dosyada menü tekrarı hatasını yapısal önler).
> - **KİMLİK tek nokta** `ui2CurrentUser()` — bugün tek kişi (users YOK); Faz 4 users okur.
> - **YETKİ tek nokta** `ui2CanSee()` — bugün **HER ZAMAN TRUE** (rol motoru YOK);
>   Faz 4 `user_permissions` okur, **ekran kodu DEĞİŞMEZ**.
> - **AUTH** mevcut desenle: token `localStorage['token']` → yoksa `/login.html`;
>   `/leena-fetch.js` include (aynı origin, ui2 ayrı giriş istemez).
> - **Nav** (brief :32-34): **Sales**(alt: liffy) · **Operations**(alt: leena) ·
>   **Finance**(alt yok) — üçü de görünür. Tasarım `signal.css`+`themes.css`
>   `public/ui2/styles/`'a kopyalandı (`.topnav`/`.domain-tab` emsal sınıfları).
>
> **Dosyalar (hepsi YENİ, `public/ui2/`):** `shell.js` · `index.html` ·
> `sales.html`/`operations.html`/`finance.html` (placeholder) · `styles/signal.css`+
> `styles/themes.css`. `express.static` public kökünden servis ettiği için `/ui2/...`
> otomatik erişilir (SPA/catch-all YOK — ölçüldü `index.js:46`).
>
> **SINIR (bu dilim, bilinçle):** mevcut `public/*.html`'e sıfır dokunuş · yeni endpoint
> YOK (kapsam sınırı — "endpoint yasak" değil, **ayrı dilim**) · client-side hesap YOK
> (RAP-02) · migration YOK · routes/utils/index.js'e dokunulmadı · rol motoru simüle
> edilmedi. **Sales boş kabuk** (liffy ayrı platform, ayrı DB).
>
> **YON-05 (ölçüm dersi):** 5/5 Finance mockup'ı (Commissions/Expo-Finance[Line/Budget/
> Actual/Variance]/War-Room[KPI]/Ledger/Reports) mevcut endpoint'ten **ZENGİN** — mockup
> ≠ mevcut kabiliyet. Önceki "Finance-Commissions.html birebir şu veriye karşılık gelir"
> ölçülmemiş varsayımdı; çürütüldü. Ekranlar geldikçe her biri ayrı ölçülecek.
>
> **BACKEND İŞ KUYRUĞU (kabuğun açığa çıkardığı, sıra Suer'de):** `users` tablosu (satışçı
> eşiği #1) · rol/yetki matrisi (`ui2CanSee` gerçek cevabı) · ekran-başı endpoint dilimleri.
>
> **Regresyon:** `npm test` **120/120** (67+6+12+12+15+8) · **T35 TABAN 342.00 KAYMADI** ·
> M01a 342.00 sağlam. ui2 salt `public/` — backend'e sıfır dokunuş kanıtlandı.
>
> **Commit'ler (push YOK):** LEENA `ui2 shell (nav + auth + permission hook)` + `ui2 kabuk
> dilimi`; ell-docs bu kayıt.

> ## ✅ 2026-09-09 — ui2 İLK GERÇEK FINANCE EKRANI: Contract (kapsama ölçümüyle seçildi)
>
> **Ne:** ui2 kabuğuna ilk gerçek ekran — **Contract detail** (`finance-contract.html`),
> gerçek veri `leenaFetch` ile. "Hangi ekran" tahminle değil **kapsama oranıyla** seçildi.
>
> **KAPSAMA ORANI (endpoint alanı DOĞRUDAN döndürüyor / mockup alanı; türetilebilir SAYILMAZ, RAP-02):**
> | Ekran | Oran | ~% | En iyi endpoint |
> |---|---|---|---|
> | **Contract** ✅ | **8/14** | **~57%** | GET `/api/contracts/:id` + `/:id/payments` (+header alanları ayrıca kapalı) |
> | Commissions | 4/12 | ~33% | GET `/api/commissions` (statement eklenirse ~50%, ama liste endpoint'i yok) |
> | Expo Finance | 0/8 | 0% | YOK (cash-forecast = ofis×vade nakit; Budget/Actual/Variance/Costs kaynağı yok) |
> | Ledger | 0/10 | 0% | YOK (ledger/journal endpoint'i yok; yürüyen Balance zaten client-hesap, RAP-02) |
> | War Room | 0/10 | 0% | YOK (FY hedef, cash position, AR yaşlandırma, aylık trend — hiçbiri yok) |
>
> Contract en yüksek **ve %50 eşiğinin üstünde** → seçildi (DUR-ve-SOR tetiklenmedi).
> ⚠️ cash-forecast HİÇBİR mockup'a karşılık gelmiyor (ölçüldü, varsayılmadı) — ayrı ekran.
>
> **Kurulan ekran (gösterilemeyen SİLİNDİ, boş sütun/placeholder YOK):**
> header (company/af/expo/tarih/status) · metrik şeridi Revenue/Paid/Balance (üçü de
> doğrudan) · **Line items** (Description/Qty/Unit) · **Commission** (Role/Agent/Rate/
> Earned-EUR — per-rol, hepsi `commission.roles[]`'ten doğrudan) · **Payments**
> (Date/Method/Amount/FX/EUR-booked). Görsel sistem signal.css; düzen veriye uyarlandı.
>
> **BACKEND İŞ KUYRUĞU (silinen alanlar = kusur DEĞİL, iş listesi):**
> - Line items **Amount** (satır toplamı) → `/api/contracts/:id` line_items'a `amount`
>   eklenmeli. Bugün yok: hesap var, alan döndürülmüyor (RAP-02 → client türetemez).
> - Line items **EUR equiv** → satır EUR karşılığı (amount×exchange_rate). Kur var, alan yok.
> - Line items **Comm % / Commission** (per-satır) → model komisyonu **per-ROL** veriyor,
>   per-satır YOK. Mockup per-satır gösteriyor — model farkı (LEENA: komisyon satır değil
>   sözleşme-rol seviyesinde). Karar gerektirir, otomatik iş değil.
> - Payments **Type** → payments'ta `payment_type` kolonu yok.
> - Payments **Status** → payments'ta `status` kolonu yok (reversal negatif satırla; ekranda
>   `reverses_payment_id` → "reversal" etiketiyle gösterildi, tam Status değil).
> - Metrik **Commission total** → endpoint per-rol `earned_eur` veriyor, TOPLAM döndürmüyor;
>   client toplayamaz (RAP-02) → metrik konmadı. Endpoint contract-level toplam döndürmeli.
>
> **SUBNAV KARARI (kural #1'in ikinci uygulaması):** tasarımda her Finance mockup'ı AYNI
> subnav'ı (War Room·Expos·Ledger·Contracts·Commissions·Reports) **kendi içine kopyalıyor** —
> kaçındığımız tekrar. → `shell.js`'e `UI2_SUBNAV` (domain→öğe) + `ui2RenderSubnav()` **tek
> kaynak** eklendi; sayfa yalnız `UI2_SUBACTIVE` bildirir. Yalnız GERÇEK ekranı olan öğe
> listelenir (bugün Finance=1: Contracts). Yapı ikinci ekranı bir satırla taşır.
>
> **Ö1 (nav'da iki "NI") sonucu — KUSUR DEĞİL:** `shell.js` avatarı **tam bir kez** üretir
> (satır 82); metin üreten CSS pseudo-element yok. İki-öğe **tasarım mockup artefaktı** —
> mockup nav-right'ında search-ikonu+bell-ikonu+avatar var (`Finance - Commissions.html:94-98`);
> ui2 zaten tek avatara indirgenmiş. Düzeltilecek çoğaltma yok. **Ö2 CSS sızıntısı:**
> `grep -l signal.css/themes.css public/*.html` → ui2 DIŞINDA isabet YOK (sızıntı yok).
> **Ö3 incognito:** token yoksa `shell.js:43-47` **koşulsuz** `/login.html` (mutlak, doğru).
> ⚠️ Ek gözlem: leena-fetch 401 yolunda `logout()` **göreli** `login.html`'e gider (/ui2'den
> yanlış çözülür) — paylaşılan dosyaya dokunmadan sayfa catch'inde mutlakla önceledim.
>
> ⚠️ Kabuk dilimi görsel turu KISMİ geçti (Suer): nav/etiket/aktif vurgu doğrulandı; incognito
> yönlendirme + CSS sızıntısı canlıda tam doğrulanmadı — kod kanıtı var, görsel teyit Suer'de.
>
> **Regresyon:** `npm test` **120/120** · **T35 342.00 KAYMADI** · M01a 342.00. Ürün koduna
> (routes/utils/index.js) sıfır dokunuş — testler etkilenmedi. Ekran testi yazılmadı (harness
> DOM koşmuyor); doğrulama görsel turda. **Commit (push YOK):** LEENA `ui2 first finance
> screen` (finance.html→finance-contract.html) + ell-docs bu kayıt.

> ## 📋 2026-09-09 — SUER HÜKÜMLERİ: adlandırma + Faz 4 kilidi + ui2 hattı (gecikmiş kayıt, yazım 2026-09-13)
>
> ⚠️ **GECİKMİŞ KAYIT.** Hükümler 9 Eyl Sentez oturumunda Suer tarafından sözlü verildi, deftere o
> gün DÜŞMEDİ; kütüğe 13 Eyl'de ID aldı (AD-01, YON-05), defter hikâyesi bugün yazıldı.
>
> - **ADLANDIRMA (→ kütük AD-01):** ELIZA = ürün/marka adı (kullanıcının gördüğü) · ELL = iç kod
>   adı (repo/dosya) · eski bağımsız sistem = **"eliza-legacy"** · LEENA Finance sekmesi yalnız
>   "Finance" · nav'da `liffy`/`leena` küçük etiket. ⚠️ **CUTOFF: Bu kayıttan ÖNCEKİ tüm defter/kod
>   kayıtlarında ELIZA = eliza-legacy.**
> - **YON-05 önerisi** (bir ölçüm turu bir varsayımı çürütürse bulgusu aynı turda deftere kayıt
>   girer) — kütükte ID aldı 13 Eyl.
> - **FAZ 4 KİLİDİ KALDIRILDI.** Ertelemenin dayanağı ("dışarıdan kimse LEENA'da değil") ekibe açma
>   kararıyla ORTADAN KALKTI. ⚠️ Ama bugün hâlâ tek kullanıcı Suer → gate ACİL DEĞİL.
> - **ui2 HATTI AÇILDI.** Suer: "ilerlemeyi göremediğim için iş kararlarına katkı veremiyorum" —
>   konfor talebi değil, KARAR KALİTESİ sorunu.

> ## 📋 2026-09-10 — WEB KESİNTİSİ: Render deploy katmanı (gecikmiş kayıt, yazım 2026-09-13)
>
> ⚠️ **GECİKMİŞ KAYIT.** Kesinti gece yaşandı; SIEMA kendi repo'suna yazdı (LEENA monorepo
> `docs/sessions/SIEMA_OPS_20260909.md`), ELL defterine DÜŞMEDİ. Kural (YON-06) doğdu ama hikâyesi
> kayıt dışı kaldı.
>
> **Zaman çizelgesi (UTC, ölçülmüş):** 20:52 `493ad39` auto-deploy · 21:08 **Timed Out** (build
> BAŞARILI, uygulama çıktısı YOK) · 21:08–21:33 `leena.app` **502** · 21:23 restart → 21:27 boot
> (⚠️ 4 dk ERKEN bakıldı) · 21:30 `4be38ed` specific-commit deploy → 21:31 **Live**.
> **Render Status:** "Degraded Build and Deploy Times, Oregon" — Investigating **21:26 UTC**, bizim
> timeout'tan **18 DK SONRA** → platform sorunu bizde göründüğünde henüz ilan edilmemişti.
>
> **ÖLÇÜLENLER:** Worker HİÇ düşmedi (`493ad39`) · DB Available · bellek %20, CPU ~0 · **kod hatası
> YOK** (iki boot da temiz) → arıza **Render deploy katmanında**.
> **KAYIP (SIEMA ölçümü):** ~45-55 açılma/tıklama · Zoho ~5-6 kayıt (retry ~8-9 kurtardı) · 1 public
> form. **Aktivasyon kaybı 0. A2 güvende.**
> **SONUÇ:** **YON-06** (push öncesi platform durumu ölçülür) · restart boot'a **~4-5 dk** ister ·
> harici uptime monitörü todo (fuar sonrası).

> ## 📋 2026-09-13 — FAZ 4 PLANLAMA TURU (kimlik+yetki; salt ölçüm, kod yok)
>
> **Faz 4 KİLİDİ KALKTI (Suer, 9 Eyl).** Ertelemenin eski gerekçesi ("dışarıdan kimse
> LEENA'da değil") 3-sistem yön değişikliğiyle geçersizleşti. ⚠️ AMA bugün hâlâ **tek
> kullanıcı Suer** → enforcement/gate **ACİL DEĞİL**; kimlik altyapısı (users+köprü) önceliği.
>
> **ÖLÇÜMLER (salt okuma, file:line):**
> - **Ö1 — sales_agents.user_id VAR.** `012_finance_foundation.sql:36` (`user_id integer`,
>   nullable) + `UNIQUE(user_id)` `014:33` (`sales_agents_user_id_key`). **FK YOK** (users
>   tablosu yok → FK olamaz). `021` internal→user_id kuralını askıya aldı (users doğunca geri
>   gelir). → **Köprünün yarısı hazır; 3. dilim küçülür.**
> - **Ö2 — LIFFY users** (`004_create_organizers_users…:21-28`): PK **UUID**, organizer_id UUID
>   FK, email/password_hash NOT NULL, role VARCHAR(20) ('owner'/'admin'/'user'), is_active.
>   `reports_to` UUID FK `039:14`; motor `middleware/userScope.js:105-226` (recursive CTE).
>   Kayıt sayısı DB'ye bağlanılamadı (DATABASE_URL Render'da) → psql bloğu üretildi (aşağıda).
> - **Ö3 — LEENA login** `routes/auth.js:21`: `organizers` tablosu (users DEĞİL), bcrypt
>   `password_hash:38`, JWT `sign:48` payload `{organizer_id, email}`, secret `JWT_SECRET:53`.
>   organizer_id DB'den (organizers.id).
> - **Ö4 — LIFFY permissions JSONB** `039:24` (DEFAULT `'{}'`). **Enforcement kodu YOK** —
>   kolon var, hiçbir yerde okunmuyor. (matrix emsali var ama LIFFY'de bile gate yok.)
> - **Ö5 — JWT secret:** iki sistem de `process.env.JWT_SECRET`, HS256 (varsayılan). ⚠️ **Aynı
>   env ADI ≠ aynı değer** (ayrı deploy, ayrı Render servisi). SSO zemini var (algoritma+ad deseni
>   aynı); kalan = değer paylaşımı + user eşleme. LIFFY'de fallback default string var (auth.js:8).
> - **Ö6 — "eski yol kırılmaz" DOĞRULANDI:** payload'da `user_id` YOK, `exp=30d` (uzun geçiş),
>   `req.organizer_id` 26 dosyada, middleware YALNIZ `decoded.organizer_id` okuyor
>   (`authMiddleware.js:17`). → user_id eklemek **additive**; eski token'da user_id yok ama kimse
>   okumadığı için umursanmaz; yeni okuyucu `decoded.user_id ?? null` yazarsa kırılmaz.
> - **Ö7 — ui2 shell imzaları:** `ui2CurrentUser()` argümansız→`{name,id}` (`shell.js:40`),
>   `ui2CanSee(domainKey)`→bool (`:52`). **İmza KORUNABİLİR** koşuluyla: kimlik+yetki ya JWT
>   payload'ında taşınır (senkron decode) ya da shell.js DOMContentLoaded'da (zaten async bağlam)
>   **init-once** ile /api/me çeker, cache'ler; iki fonksiyon senkron o cache'i okur. ⚠️ RİSK: biri
>   bunları Promise-döndürür yaparsa çağıranlar kırılır → **Faz 4 senkron sözleşmeyi korumalı**.
>   Sağlanırsa SAYFA (ekran) kodu değişmez — kabuk vaadi tutar.
>
> **DİLİM SIRASI (Sentez iskeletinden SAPMA ölçümle):**
> 1. **users + ilk Owner + sales_agents FK** ← *genişledi:* Ö1 kolon+UNIQUE zaten var, yalnız FK
>    users'a bağlı → FK'yi dilim 1'e aldım (ayrı dilim gereksiz).
> 2. JWT'ye **user_id + name** ← *name eklendi:* Ö7, ui2CurrentUser senkron kalsın diye kimlik
>    payload'da taşınmalı (yalnız user_id değil).
> 3. ~~sales_agents.user_id köprüsü~~ → *küçüldü:* FK dilim 1'e taşındı; kalan = internal agent
>    user_id **backfill** (küçük, ayrı).
> 4. permission matrix (enforcement YOK) · 5. gate (ACİL DEĞİL — tek kullanıcı) · 6. SSO (zemin
>    var: Ö5).
>
> **İLK DİLİM TANIMI:**
> - **Migration** `032_users_and_first_owner.sql` (sıradaki no ölçüldü: 031 dolu) — YAZILIR,
>   ÇALIŞTIRILMAZ (Suer Render Shell'de dry-run→commit).
>   - `CREATE TABLE users` (B2 LEENA kendi kimlik tablosu): **id serial PK** (sales_agents.user_id
>     integer + organizers integer ile uyumlu — Ö1) · organizer_id integer FK organizers · email
>     UNIQUE · password_hash · **is_owner** bool (B10: aktif Owner<1 olamaz — partial index/CHECK) ·
>     **display_role** (B9: yetki DEĞİL) · **password_must_change** (B7) · is_active · created_at.
>   - `ALTER TABLE sales_agents ADD CONSTRAINT … FOREIGN KEY (user_id) REFERENCES users(id)`
>     (kolon+UNIQUE zaten var, Ö1).
>   - **İlk Owner = Suer** INSERT, `password_must_change=true` (B7). Şifre hash migration'a GÖMÜLMEZ
>     (değer yazılmaz) — geçici hash + must_change, ilk girişte değişir.
> - **Dosyalar:** yalnız migration. **Kod YOK** (login users'ı bu dilimde okumaz — o dilim 2).
> - **NE KIRILMAZ:** mevcut giriş `organizers` üstünden çalışır (auth.js users'a dokunmaz); JWT
>   payload değişmez; FK eklenmesi mevcut sales_agents satırlarını etkilemez (hepsi user_id NULL —
>   ⚠️ ÖN-DOĞRULAMA psql: `SELECT COUNT(*) FILTER (WHERE user_id IS NOT NULL) FROM sales_agents;`
>   0 değilse o id'ler users'a önce girmeli, yoksa FK patlar).
> - **NASIL DOĞRULANIR:** dry-run BEGIN…ROLLBACK · `\d users` + `\d sales_agents` (FK görünür) ·
>   ilk Owner SELECT · mevcut organizer login hâlâ token alıyor · `npm test` **120** bozulmaz
>   (users additive, testler değmez) · TABAN 342.00.
>
> **psql blokları (Suer, Render Shell, salt okuma):**
> - LIFFY sayım: `SELECT COUNT(*) AS users, COUNT(*) FILTER(WHERE is_active) AS active,
>   COUNT(DISTINCT organizer_id) AS orgs, COUNT(*) FILTER(WHERE role='owner') AS owners,
>   COUNT(*) FILTER(WHERE reports_to IS NOT NULL) AS with_mgr,
>   COUNT(*) FILTER(WHERE permissions <> '{}'::jsonb) AS custom_perms FROM users;`
> - LEENA FK ön-kontrol: `SELECT COUNT(*) FILTER (WHERE user_id IS NOT NULL) AS agents_with_user
>   FROM sales_agents;`
>
> **⚠️ YON-05 (varsayım çürüdü):** ui2 ilk ekranda hem Sentez hem Orchestrator **Commissions**
> önermişti; oran ölçümü ikisini de çürüttü (Commissions 4/12 ~%33 · **Contract 8/14 ~%57**).
> Ölçüm olmasa yarısı silinmiş ekran kurulacaktı. Ayrıca `cash-forecast` (canlıdaki en olgun
> rapor, 67 test) **hiçbir mockup'a karşılık gelmiyor** — tasarım tarafında boşluk.
>
> **⚠️ AÇIK BORÇ — logout() göreli yönlendirme:** `leena-fetch` 401 yolu göreli `login.html`'e
> gidiyor → `/ui2/`'den `/ui2/login.html` çözülür (404). CC sayfa catch'inde mutlakla aştı
> (paylaşılan dosyaya dokunmamak doğruydu) ama **HER YENİ ui2 SAYFASINDA TEKRAR EDER.** Çözüm
> adayı: `shell.js`'e taşımak (kabuk zaten tek kaynak, kural #1) — ölçülmedi.
>
> **ui2 finance-contract görsel turu 6/6 GEÇTİ** (canlı, `696568a`): TABAN 342.00 ekranda ·
> 999999→"not found" · CSS sızıntısı YOK (contract-list + cash-forecast temiz, banner 12.065,20 durdu).
>
> **Çalışma kuralları K1/K2/K3 CLAUDE.md'ye eklendi** (LEENA repo, additive; ölçüm turu "commit
> yok" istisnası — Sentez açıkça istedi). **Commit:** LEENA `CLAUDE.md` + ell-docs bu kayıt. PUSH YOK.

> ## ✅ 2026-09-13 — FAZ 4 DİLİM 1: users tablosu + ilk Owner + sales_agents FK (migration yazıldı, KOŞULMADI)
>
> Migration `032_users_and_first_owner.sql` YAZILDI, ÇALIŞTIRILMADI (Suer Render Shell'de
> koşar). Login akışı (`routes/auth.js`), JWT payload, `organizers` DEĞİŞMEDİ. Commit var, PUSH YOK.
>
> **⚠️ 1 — TEST DB'Sİ CANLIDAN ÜÇ MIGRATION GERİDE (YALANCI YEŞİL, YON-05):** `setup_test_db.js`
> yalnız **012→028** kuruyor (ölçüldü `:19-24`; önceki tur "031" tahmini YANLIŞTI). **029/030/031
> test DB'sine HİÇ girmiyor** → geçen 117 test artık var olmayan bir şemayı doğruluyor. 032 dördüncü
> açık. Bu, 3 tarih-fail'inden **BÜYÜK** kusur ve **sıradaki dilimin ana işi**. İlk raporda "borç"
> diye yan not geçilmişti — yalancı yeşil olduğu görülmemişti.
> **⚠️ 2 — tarih-bağımlı 3 fail:** T1/T4/T7 cash-forecast. Fixture `test_cash_forecast.js:82`
> `due_date:'2026-09-10'`, assert `is_overdue===false` (`:98`). Bugün 2026-09-13 → backend DOĞRU
> (`is_overdue=TRUE`); TEST sabit-tarih fixture'ıyla kırılıyor. Dilim-DIŞI (032 test'e girmiyor).
> **⚠️ 3 — sessiz çürüme:** 9 Eyl 120/120'di; 4 gün kimse koşmadı, kırmızıya döndü, kimse bilmedi.
> Suite yalnız dilim koşarken çalışıyor (CI/otomatik koşum yok).
> **⚠️ 4 — borç boyutu ÖLÇÜLMEDİ:** kaç sabit tarih daha kırılacak (test fixture'larında)?
> **⚠️ 5 — düzeltmenin tuzağı:** hepsi `CURRENT_DATE + 30` yapılırsa OVERDUE senaryosu hiç test
> edilmez. Fixture düzeltilirken hem geçmiş hem gelecek kalem NİYETİ korunmalı.
> **6 — password_hash NULL kararı (Suer):** kolon `NOT NULL` DEĞİL, sentinel YOK. NULL = "henüz
> şifre yok". Gerekçe: hash kolonuna hash-olmayan değer yazmak veride yalandır, o kolonu okuyan her
> kod yolu için kalıcı mayın — NULL dürüst. İlk Owner: `password_hash NULL + password_must_change=true`.
> Migration koşulmadı → değişim bugün bedava (koştuktan sonra ikinci migration gerekirdi).
> **7 — B10 + Ö2 (doğru):** B10 kütük "1'in ALTINA inemez" = **en az 1** → partial unique index
> elendi (en-fazla-1 verir); **statement-level trigger** `enforce_min_one_active_owner` (AFTER
> UPDATE/DELETE, INSERT'te değil). Self-grant yarısı app-layer (dilim 4). Ö2: `sales_agents_user_id_key`
> CONSTRAINT (index değil), `ALTER COLUMN TYPE` otomatik rebuild; 0 satır → `USING` no-op.
>
> **auth.js NULL-şifre ÖLÇÜMÜ (düzeltilmedi, dilim 2'nin işi):** `auth.js:25-27` boş kontrolü yalnız
> istek gövdesi için; DB `password_hash` NULL kontrolü YOK (`:38` öncesi). Login bugün `organizers`
> okuyor (`:30`), users DEĞİL → NULL yolu bugün tetiklenmez. ⚠️ Dilim 2 users okuyunca NULL-hash'li
> Owner girişi → `bcrypt.compare(plain,null)` throw → catch(`:65`) → **500 (401 değil)**. Dilim 2
> guard'ı: users'tan önce `if(!user.password_hash) return 401`.
>
> **PG SÜRÜMÜ ÖLÇÜLDÜ (Suer, Render dashboard 10 Eyl):** `leena_v401_db` = **PostgreSQL 17** →
> `gen_random_uuid()` çekirdekte, `CREATE EXTENSION` GEREKMEZ. Migration olduğu gibi. BLOK 1 teyit
> olarak Suer listesinde kalıyor (kuşak değil, doğrulama).
>
> **Önceki kararlar (korunuyor):** `users.id`=**UUID** (LEENA'nın kendi ihtiyacı: sayım sızıntısı ·
> kayıt-öncesi ID · birleştirme çakışması; "LIFFY UUID olduğu için" DEĞİL — LEENA çekirdek, taviz
> vermez). `organizers.id` **SERIAL kaldı** (26 dosya + JWT bağlı; `users.organizer_id` integer FK,
> iki-tip kasıtlı). Ö3 ön koşul: `sales_agents` user_id dolu **0** beklenir (BLOK 2, Suer). İlk Owner
> e-posta `suer@elan-expo.com` BLOK 3 ile doğrulanır.
>
> **⚠️ KUYRUĞA (Sentez, bugün çözülmedi):** `organizers` bugün HEM kiracı HEM giriş kimliği; SaaS'ta
> ayrılır (tenant ≠ user). users geldiğinde giriş users üzerinden, organizers saf kiracı olmalı —
> PK tipinden BÜYÜK konu. Multi-tenant güvenliği UUID ile GELMEZ, her sorgunun kiracıya göre
> filtrelenmesiyle gelir (ÖLÇÜLMEDİ). Dilim 2: `ui2CurrentUser()` **SENKRON KALMALI** (init-once
> async çek → senkron cache); Promise'e çevrilirse kabuk vaadi bozulur.
>
> **Doğrulama:** `npm test` bugün **117/120** (3 tarih-fail dilim-dışı) · **TABAN 342.00 KAYMADI**
> (T35) · M01a 342.00. Migration test DB'sine girmiyor (setup 012→028). **Commit:** LEENA migration
> `032` + ell-docs bu kayıt. Sonra **DUR** — Suer BLOK 1-8'i koşacak.

> ## ✅ 2026-09-13 — FAZ 4 DİLİM 1 CANLIDA: `users` tablosu + ilk Owner + `sales_agents` FK
>
> - **Migration `032_users_and_first_owner.sql` canlıda KOŞTU** (Suer, Render Shell,
>   `BEGIN … \i … COMMIT` tek oturum). Kod commit'i `bbc69ff` (monorepo).
>   ⚠️ Faz 4 kilidi 9 Eylül'de kalktı; ertelemenin eski gerekçesi ("dışarıdan kimse
>   LEENA'da değil") yön değişikliğiyle geçersizleşti. Bugün hâlâ tek kullanıcı
>   Suer → **gate ACİL DEĞİL**, sıra buna göre kuruldu.
>
> - **ÖN ÖLÇÜMLER (Suer, canlı DB):** PG **17.9** → `gen_random_uuid()` çekirdekte,
>   `CREATE EXTENSION` gerekmedi · `sales_agents` **152 satır, `user_id` dolu 0** →
>   tip değişimi no-op · `organizers` **TEK SATIR**, id=1, suer@elan-expo.com.
>
> - **⚠️ BLOKE EDİCİ ÖLÇÜM — Render'da otomatik migration YOK.**
>   Repo: `package.json` start/prestart/postinstall YOK · `render.yaml` /
>   `Procfile` / `Dockerfile` YOK · `index.js` yalnız `app.listen`.
>   Dashboard (Suer): Build=`npm install` · **Pre-Deploy Command BOŞ** ·
>   Start=`node index.js`.
>   ⚠️ Pre-Deploy tam migration'ın koşacağı yerdir — boş.
>   **Bu ölçülmeseydi push migration'ı SESSİZCE koşturabilirdi** ve
>   "yazılır-çalıştırılmaz" kuralı farkında olmadan çiğnenirdi.
>   Ayrıca ölçüldü: Root Directory = `backend/leena-v401-backend` → Render Shell
>   orada açılıyor, `\i migrations/...` göreli yolu doğru çözülüyor.
>
> - **ŞEMA:** `users.id` **uuid**, DEFAULT `gen_random_uuid()` ·
>   `organizer_id` **integer** FK → `organizers(id)` (organizers serial KALDI) ·
>   `email` UNIQUE · `password_hash` **NULLABLE** · `is_owner` (B10) ·
>   `display_role` (B9, **yetki DEĞİL**) · `password_must_change` (B7) · `is_active`.
>   `sales_agents.user_id` **integer → uuid**, UNIQUE korundu, FK eklendi.
>
> - **UUID GEREKÇESİ — LEENA'nın KENDİ ihtiyacı:**
>   1. Sıralı ID sayım sızdırır (`users/47` → kaç kullanıcı var, `users/46` denenebilir).
>   2. ID kayıt atmadan üretilebilir (toplu içe aktarma, kuyruk, çevrimdışı).
>   3. İçe aktarma/birleştirmede çakışmaz.
>   ⚠️ "LIFFY UUID olduğu için" gerekçesi **İPTAL** — LEENA çekirdektir; LIFFY'yi
>   değiştirmemek için LEENA'da taviz verilmez (Suer hükmü).
>
> - **⚠️ `password_hash` NULLABLE — sentinel REDDEDİLDİ.**
>   `'!PENDING_FIRST_LOGIN'` gibi bir değer yazılması önerilmişti; reddedildi:
>   **hash kolonuna hash olmayan yazmak veride yalandır**, o kolonu okuyan her
>   kod yolu için kalıcı mayın. NULL = "henüz şifre yok", dürüst.
>   Migration koşulmadan önce düzeltildi → bedava.
>
> - **B10 = statement-level trigger** `enforce_min_one_active_owner`
>   (AFTER DELETE OR UPDATE, FOR EACH STATEMENT).
>   Kütükten okundu: "1'in ALTINA inemez" = **en az 1** → partial unique index
>   ELENDİ (o en-fazla-1 yapar). Self-grant yarısı app-layer'a (dilim 4).
>
> - **⚠️ ÖLÇÜMDE ÇIKAN, PLANDA OLMAYAN:** `sales_agents_external_user_null_check`
>   (021) — "agent_type internal değilse `user_id` NULL olmalı". `users` tablosu
>   olmadığı için ASKIDA duruyormuş; şimdi **ANLAM KAZANDI**: dış ajans/freelance
>   agent **DB seviyesinde** `users` kaydı ALAMAZ.
>   "Freelance satışçılar LIFFY'de kalır, çapraz erişim yalnız iç ekip" hükmüyle
>   örtüşüyor — 021'de bilinçle konmuş.
>
> - **DOĞRULAMA — DRY-RUN ÖNCE, GERÇEK KOŞUM SONRA:**
>   Dry-run (`BEGIN … ROLLBACK`) temiz geçti; ROLLBACK sonrası `users` YOK,
>   `sales_agents.user_id` **integer**'a geri döndü (canlıda iz yok, teyitli).
>   Gerçek koşum sonrası: Owner satırı
>   `ae219804-f737-46ed-b9b3-74e4105d90a4` · `password_hash` NULL ·
>   `is_owner` t · `password_must_change` t · `user_id` **uuid** kalıcı.
>   **⚠️ HÜKMÜN SINAVI GEÇTİ:** `leena.app` çıkış→giriş ÇALIŞTI, ayrıca
>   **incognito'da eski şifreyle giriş yapıldı** — önbelleğe alınmış oturum değil,
>   gerçek kimlik doğrulama turu. "Okuyan kod yok" iddiası canlıda kanıtlandı.
>
> - **GERİ ALMA BLOĞU HAZIR, KOŞULMADI.** Migration dosyasından okunarak üretildi
>   (nesne adları `032:31/59/69/82/86` ile eşleşiyor), ters sıra: FK drop →
>   `user_id` uuid→integer → trigger drop → fonksiyon drop → `users` drop.
>   Başında dolu-satır koruması (`RAISE EXCEPTION`). Sözdizimi denetlendi,
>   runtime test EDİLEMEDİ — kabul.
>
> - **⚠️ SIRA HÜKMÜ — (a) ŞİMDİ KOŞ, gerekçesi DEĞİŞKEN İZOLASYONU:**
>   "Migration ve kod aynı anda canlıya çıksın" seçeneği ÇÜRÜDÜ — migration elle
>   koşuluyor, kod push ile gidiyor, **her hâlükârda iki ayrı eylem**.
>   Migration tek başına koşunca `ALTER TYPE` + FK + trigger **izole** doğrulandı.
>   Dilim 2 koduyla birlikte koşsaydı, sorun çıktığında sebep ayırt edilemezdi.
>   **Bir tur = bir değişken.**
>
> - **⚠️ DİLİM 2 KAPSAMI BÜYÜDÜ — BOOTSTRAP AÇIĞI:**
>   İlk Owner `password_hash` NULL. `auth.js` ölçüldü: `:25-27` boş kontrolü
>   yalnız istek gövdesi için, DB NULL kontrolü YOK. Login bugün `organizers`
>   okuyor → NULL yolu bugün TETİKLENMİYOR.
>   Dilim 2'de giriş `users`'a taşındığı an: kayıt var, şifre yok, şifre belirleme
>   akışı da yok → **KİMSE GİREMEZ**. 401 guard 500'ü önler ama **giriş yolu değildir**.
>   → Dilim 2 yalnız "JWT'ye `user_id` ekle" DEĞİL; **şifre belirleme akışını da
>   içermeli**. Guard: `if (!user.password_hash) return 401`.
>
> - **`organizers` HEDEF/YOL HÜKMÜ (Sentez):** (a) ve (b) alternatif DEĞİL —
>   (a) hedef, (b) ona giden yol.
>   **HEDEF:** `organizers` SAF KİRACI olur, giriş `users`'a **TAŞINIR** (kopyalanmaz).
>   Bugün `organizers` içindeki e-posta/şifre giriş verisidir; kiracı tablosunda
>   durması tek-kaynak ilkesinin ihlalidir.
>   **YOL:** JWT geçiş boyunca HER İKİSİNİ taşır; `organizer_id` çalışmaya devam
>   eder → 26 dosya + middleware dokunulmaz, eldeki token'lar geçerli kalır.
>   ⚠️ **ÖLÇÜLMÜŞ KISIT: `exp = 30d`** → eski yol en erken dilim 2'den **30 GÜN
>   SONRA** emekli edilebilir. **Takvimdir, tercih değil.**
>
> - **`ui2CurrentUser()` SENKRON KALACAK** (dilim 2 notu). Promise'e çevrilirse
>   çağıran her ekran kırılır ve kabuğun "ekran kodu DEĞİŞMEZ" vaadi bozulur.
>   Çözüm: init-once async çek → senkron cache.
>
> - **⚠️ AÇIK BORÇ — 1. MADDE: TEST DB'Sİ CANLIDAN 4 MIGRATION GERİDE.**
>   `setup_test_db.js` 012→028 kuruyor; **029/030/031/032 test DB'sine HİÇ
>   GİRMİYOR** → geçen 117 test **artık var olmayan bir şemayı doğruluyor:
>   YALANCI YEŞİL.** Her yeni migration açığı büyütüyor.
>   **Sıradaki dilimin ana işi.**
>
> - **⚠️ AÇIK BORÇ — 2. madde: tarih-bağımlı 3 fail** (fixture `due_date`
>   `'2026-09-10'` < bugün). Backend doğru, test kırılgan. Boyutu ÖLÇÜLMEDİ
>   (kaç sabit tarih daha kırılacak).
>   **3. madde — SESSİZ ÇÜRÜME:** 9 Eylül'de 120/120 idi; 4 gün kimse `npm test`
>   koşmadı, suite kırmızıya döndü, kimse bilmedi. Suite yalnız dilim koşarken
>   çalışıyor, aralarda çürüyor.
>   **4. madde — DÜZELTMENİN TUZAĞI:** tarihleri `CURRENT_DATE`-göreli yapmak
>   kolay, ama hepsi `+30` olursa OVERDUE senaryosu HİÇ test edilmez. Niyet
>   korunmalı: bazı satırlar geçmişte, bazıları gelecekte.
>
> - **⚠️ KUYRUĞA (Sentez açtı, bugün çözülmedi):**
>   "`organizers` bugün HEM kiracı HEM giriş kimliği. SaaS'ta bu ikisi ayrılır
>   (tenant ≠ user). PK tipinden BÜYÜK konu."
>   "Multi-tenant güvenliği UUID ile GELMEZ — her sorgunun kiracıya göre
>   filtrelenmesiyle gelir. ÖLÇÜLMEDİ."
>
> - **SUER GENEL KURALI (kütüğe girecek, ayrı iş):** "ELIZA anlık iş çözsün diye
>   değil, multi-tenant SaaS hassasiyetinde kurulur. Hızlı çözüm tercih edilmez.
>   En kaliteli seçenek kurulumu aşırı uzatmıyorsa, her zaman en doğru yol seçilir."

> ## ✅ 2026-09-13 — TEST DB SENKRONU: yalancı yeşilden çıkış + setup GUARD
>
> - **⚠️ YENİ İLKE (Sentez):** "Test DB'si tüm veritabanının aynası değil, **TEST EDİLEN
>   KODUN aynasıdır**." Finans testleri → finans şeması (012+) + bağlı olduğu OMURGA
>   (`organizers`). Sentez'in ilk "dizini oku ne varsa koş" kriteri ölçümle çürüdü:
>   `organizers` test DB'de yoktu · 029/031 email altyapısına (`email_campaigns`/`email_queue`)
>   bağımlı · 031 `CREATE INDEX CONCURRENTLY` transaction içinde çalışmıyor (PG kısıtı, tercih değil).
>
> - **YALANCI YEŞİL KAPANDI:** `setup_test_db.js` artık `migrations/` dizinini OKUYOR
>   (sabit dizi KALDIRILDI), 012'den **sayısal** sıralı koşar. → **033+ finans migration'ı
>   OTOMATİK girer**, borç yeniden açılmaz. Kanıt: setup 18 migration koştu (012→028 + **032**),
>   test DB'de `users` VAR (id uuid, `password_hash` nullable), `sales_agents.user_id` **uuid** +
>   FK→users(id), UNIQUE korundu.
>
> - **DIŞLA-LİSTESİ** (kod içinde, her satır tek-cümle gerekçe): 029 (email evreni) · 030
>   (callcenter, bağımsız olsa da finans-dışı tutarlılık) · 031 (email_queue yok + CONCURRENTLY).
>   ⚠️ **SINAVLA KANITLANDI:** 029 listeden çıkarılınca setup **GÜRÜLTÜYLE patladı**
>   (`relation "email_campaigns" does not exist`, exit 1) — sessiz yalancı-yeşil DEĞİL. Sabit-aralıktan
>   farkı: aralık her migration'da güncellenmeli; dışla-listesi yalnız yeni bir email/callcenter
>   migration'ında (nadir), unutulursa gürültülü arıza.
>
> - **`organizers` stub — OMURGA** (authMiddleware okur; 032 `users.organizer_id` FK + ilk Owner
>   seed). MINIMUM: id (FK hedefi) + email (DO bloğu eşleşmesi). Canlı ölçüm (defter 13 Eyl:
>   TEK SATIR id=1 suer@elan-expo.com) + 032'nin canlı koşumu (id integer olduğunu kanıtladı).
>
> - **Yerel PG 14.18** (Homebrew) → PG13+, `gen_random_uuid()` çekirdekte, sorun yok.
>
> - **⚠️ setup GUARD eklendi** (whitelist): hedef DB adı TAM `ell_comm_test` değilse script
>   **hiçbir şey yapmadan çıkar** (DB adı `URL` API ile ayrıştırılır, elle string kesme yok;
>   ayrıştırma başarısız = ret). Kontrol `DROP DATABASE`'den ÖNCE, çıkış non-zero, bağlantı
>   string'i gösterilmez (şifre). Gerekçe: `DROP DATABASE` prod'a karşı bugüne dek YALNIZ
>   TESADÜFEN korunuyordu (Render'da `TEST_DATABASE_URL` tanımsız). Tesadüf güvenlik değildir.
>   ⚠️ KANITLANDI: sahte ad (`ell_comm_tset`) → reddedildi, exit **1**, sahte DB **yaratılmadı**
>   (`pg_database` 0 satır); doğru ad → exit 0; env tanımsız (varsayılan) → çalışır.
>
> - **DOĞRULAMA:** her suite AYRI koşuldu → **117/120** (cash_forecast 64/3 · agent_office 6 ·
>   payouts 12 · commissions 12 · schedule 15 · offices 8), aynı 3 tarih-fail, **YENİSİ YOK** ·
>   **TABAN 342.00** (T35 + M01a). İdempotent: ikinci `setup+test` aynı sonuç.
>
> - **⚠️ YENİ KEŞİF — AÇIK BORÇ: `npm test` zinciri ilk fail'de DURUYOR.** `package.json`
>   `test` script'i `&&` ile bağlı → cash_forecast 3-fail'de exit 1 verip zinciri kesiyor;
>   kalan 5 suite (53 test) **HİÇ KOŞMUYOR**, `npm test` yalnız 64/3 gösteriyor. Bu, tarih-fail'in
>   gizlediği İKİNCİ yalancı-durum katmanı: `npm test` çağıran biri diğer 53 testin durumunu görmez.
>   Ürün kodu değil (script). ⚠️ `package.json` **SIEMA DONDURMA LİSTESİNDE (3 Ekim'e kadar)** →
>   düzeltme (`&&`→`;` veya suite-runner) **3 Ekim sonrası ilk iş**. O tarihe kadar doğrulama
>   yöntemi: **6 suite AYRI koşulur** (bu turda yapıldı; şema-sonrası kanıt: `user_id` uuid üstünde
>   64/3+6+12+12+15+8=117/120, aynı 3 tarih-fail). Sonraki promptlarda "npm test" değil "6 suite
>   ayrı" yazılır.
> - **⚠️ İŞLEM HATASI (ders):** dışla-listesi sınavında 029'u geri koymak için `git checkout`
>   kullanıldı → commit'siz yeni `setup_test_db.js` silindi, yeniden yazıldı (sınav sonucu geçerli).
>   **Ders: commit'siz dosya varken `git checkout` geri-alma aracı DEĞİL** — working-tree'yi
>   committed hale döndürür, yeni yazımı yok eder. Tekrarlanmasın (geçici düzenlemeyi geri almak
>   için: yeniden Write veya `git stash`, checkout değil).
>
> - **⚠️ AÇIK BORÇ: 029/030/031 test DB'sinde YOK ve TEST EDİLMİYOR** (şema senkron, kapsam değil).
>   032 girdi ama `users` testleri dilim 2'nin işi.
>
> - **⚠️ AÇIK BORÇ — TARİH (ayrı dilim):** **115 sabit tarih, 7 dosyada** (biri npm test kapsamı
>   dışı). "3 fail" bugünün sayısıydı, borcun boyutu değil. Çoğu SABİT KALMALI (kontrat imza
>   tarihi bugüne göre kaymaz — göreli yapmak YANLIŞ). Yalnız kodun bugünle karşılaştırdıkları
>   çürür: `due_date` · `cut_date` · forecast penceresi. "Hepsi +30" tuzağı: OVERDUE senaryosu
>   hiç test edilmez. Sıra: şema senkronundan SONRA, dilim 2'den ÖNCE. **Bu dilimde tarihlere
>   DOKUNULMADI** (bir dilim bir değişken).
>
> - **Commit:** LEENA `setup_test_db.js` + ell-docs bu kayıt. PUSH YOK.

> ## ✅ 2026-09-13 — TARİH BORCU DÜZELTİLDİ: cash_forecast is_overdue fixture'ları göreli
>
> - **⚠️ BORÇ 141 TARİHTEN 2 SATIRA İNDİ** (ölçüm turu daralttı): 5 suite × `is_overdue`/
>   `CURRENT_DATE` **0 isabet** → schedule(37)+commissions(21)+payouts(5)+offices(2) **B sınıfı,
>   dokunulmadı**. Tek çürüme noktası `cashForecast.js:143` (`due_date < CURRENT_DATE AND
>   remaining>0`). ⚠️ **"115 sabit tarih" borcun boyutu SANILMIŞTI — sayı ≠ borç**; çoğu sabit
>   kalmalı (kontrat/ödeme/expo tarihi bugüne göre kaymaz).
>
> - **DEĞİŞEN: SADECE 2 tarih** (ikisi upcoming, cash_forecast T1/T4/T7): eski `2026-09-10`
>   (bugün kırıktı) + `2026-10-19` (19 Ekim'de kırılacaktı) → `daysAhead(30)`/`daysAhead(60)`.
>   Helper `_ymd`/`daysAhead`/`daysAgo` (aynı dosyada). ⚠️ **YEREL bileşen**, `toISOString`
>   DEĞİL: DB CURRENT_DATE `Europe/Istanbul` = yerel makine TZ (ölçüldü); toISOString UTC'ye
>   çevirip gece yarısı 00:00-03:00 gün kaydırırdı.
>
> - **⚠️ C SINIFI KAPATILDI (kod izlendi):** `2026-08-01`/`09-01` çiftleri (T5 revizyon · T18
>   incomplete · T25/T26 ödeme↔kalem · T2 excess · T3 statü) **HİÇBİRİ is_overdue kullanmıyor**
>   → B, çürümüyor. Ölçüm turundaki "yeşil ama anlamsız" endişesi bu çiftler için **GEÇERSİZ**
>   çıktı (is_overdue assertion'ı yok). Gerçek gizli çürüme yalnız `2026-10-19` (gelecek-tarama).
>
> - **⚠️ PENCERE UYUMU:** `WIDE=?from=2026-01-01&to=2026-12-31` sabit üst sınırı `daysAhead`'i
>   Aralık'ta taşırırdı (satır düşer → yanlış-sebeple geç/kal). T1 çağrısı `T1WIN=daysAgo(400)..
>   daysAhead(400)` göreli pencereye çevrildi. Diğer testlerin WIDE'ına dokunulmadı (B tarihleri,
>   is_overdue yok).
>
> - **NİYET KORUNDU** (overdue + upcoming İKİSİ de test ediliyor):
>   | senaryo | test | tarih | çürür mü |
>   |---|---|---|---|
>   | overdue | T10, T13 | `2020-01-01` (SABİT, uzak-geçmiş) | hayır |
>   | upcoming | T1, T4/T7 | `daysAhead(60/30)` (GÖRELİ) | hayır |
>   | upcoming | T13 | `2030-01-01` (SABİT, uzak-gelecek) | hayır |
>   | remaining=0 (tarih-duyarsız) | T1 Jul31, T11 | `2026-07-31`/`2020` (SABİT) | hayır |
>   ⚠️ TUZAKTAN KAÇINILDI: hepsi `daysAhead` OLMADI — overdue tarafı 2020 sabit kaldı, yoksa
>   overdue senaryosu hiç test edilmezdi (yalancı yeşilin üçüncü biçimi).
>
> - **DOĞRULAMA:** 6 suite ayrı → **120/120** (cash_forecast **67/67** — 3 fail gitti; diğer 5
>   değişmedi 6+12+12+15+8) · **TABAN 342.00** (T35 + M01a). setup 032/uuid şeması üstünde.
>
> - **ZAMAN YOLCULUĞU SINAVI — kısmi:** sahte bugün 2026-11-20'de (eski 09-10/10-19 ikisi geçmiş
>   olurdu) helper `daysAhead(30/60)` hâlâ GELECEK üretti (12-20, 2027-01-19) + pencere kapsadı →
>   göreli mantık kanıtlandı. ⚠️ **Uçtan-uca DB-kaydırma YAPILAMADI:** `faketime` yok + DB
>   `CURRENT_DATE` built-in (ürün kodu mock yasak, sistem saati kapsam dışı). Helper-mantık +
>   JS-sahte-bugün kanıtı verildi; DB-seviyesi zaman-yolculuğu ÖLÇÜLEMEDİ.
>
> - **AÇIK:** `test_wizard_silent.js` (1 tarih `2026-09-30`) — npm test kapsamı dışı,
>   sınıflandırılmadı, dokunulmadı.
>
> - **Commit:** LEENA `test_cash_forecast.js` + ell-docs bu kayıt. PUSH YOK. Ürün koduna, diğer
>   5 suite'e, setup'a, package.json'a (SIEMA dondurması) DOKUNULMADI.
>
> **Kütük yazımı (2026-09-13):** A-J hükümleri işlendi → AD-01 (A, yeni grup) · YON-05 (B) · YON-06 (C) · YON-07 (D) · YON-08 (E) · SEM-03 (F) · SEM-04 (G) · SEM-05 (H) · YON-09 (I) · YON-10 (J).

> ## ✅ 2026-09-14 — users TABLOSU TESTLERİ: B10 trigger İLK KEZ tetiklendi (ÇALIŞTI)
>
> - **`tests/test_users.js` yazıldı, 12 test** (endpoint yok — users route dilim 2; test doğrudan
>   `pool.query` + hata yakalama, `expectReject`/`expectPass`). Her kural pozitif+negatif.
> - **⚠️ B10 trigger `enforce_min_one_active_owner` İLK KEZ TETİKLENDİ.** Dilim 1'de yazılmış ama
>   canlıda HİÇ çalıştırılmamıştı (dilim 1 raporu). **Sonuç: ÇALIŞTI, kusur YOK.** U5 (tek Owner
>   is_active=false) · U6 (tek Owner DELETE) · U7 (tek Owner is_owner=false) — üçü de **REDDEDİLDİ**
>   (trigger RAISE). U8 (2 Owner varken birini pasife çek) → GEÇER. ⚠️ Ö2: trigger `AFTER UPDATE OR
>   DELETE FOR EACH STATEMENT` — **INSERT kapsamda DEĞİL** (doğru: Owner eklemek invariant'ı ihlal
>   etmez; son-Owner UPDATE/DELETE ile korunuyor). Açık: TRUNCATE trigger'ı atlar (nadir/admin,
>   test edilmedi).
> - **021 `external_user_null_check` İLK KEZ test edildi** (032'yle anlam kazanmıştı): U10
>   (external_freelance + user_id dolu → REDDEDİLDİ, CHECK) · U11 (internal + geçerli user_id →
>   GEÇER). Kütük ölçümü doğrulandı: `CHECK (agent_type='internal' OR user_id IS NULL)`.
> - Diğer kurallar: SEM-03 (id uuid default, U1) · SEM-04 (password_hash NULL, U2/U2b — seed Owner
>   NULL canlıda) · FK sales_agents.user_id→users(id) (U9, olmayan uuid reddedildi) · email UNIQUE
>   (U3) · organizer_id FK (U4).
> - **RESET stratejisi:** seed Suer = TEK aktif Owner korunur; negatif B10 testleri onu düşürmeye
>   çalışır → trigger RAISE query'yi geri alır, state bozulmaz. Reset: sales_agents sil (user_id FK
>   önce) → extra users sil (Suer koru) → Suer aktif+owner garanti.
> - **⚠️ Yeni suite `npm test` ZİNCİRİNDE DEĞİL** — `package.json` SIEMA dondurmasında (3 Ekim).
>   Ayrı koşuluyor (`node tests/test_users.js`). **3 Ekim sonrası zincire eklenecek — borç.**
> - **DOĞRULAMA:** 7 suite ayrı → cash_forecast **67** · agent_office **6** · payouts **12** ·
>   commissions **12** · schedule **15** · offices **8** · users **12/12**. İlk 6 DEĞİŞMEDİ ·
>   TABAN **342.00** (T35+M01a) · idempotent (2. koşum aynı) · package.json diff boş.
> - **`CLAUDE.md` (monorepo):** "ELIZA EMEKLİ" → "eliza-legacy EMEKLİ (AD-01). ELIZA = ürünün adı."
>   (tek satır, parantez korundu). AD-01 ile hizalandı.
> - **Commit:** LEENA `tests/test_users.js` + `CLAUDE.md` (tek commit) + ell-docs bu kayıt. PUSH YOK.
>   Ürün koduna / migration'a / package.json'a / auth.js'e DOKUNULMADI.

> ## ✅ 2026-10-08 — FUAR SONRASI ÖLÇÜM + KARARLAR
>
> - **Ne yapıldı:** 14 Eyl – 8 Eki aralığı salt-okunur ölçüldü (iki repo, CC); üretim DB
>   sayımı Suer tarafından Render Shell'de koşuldu (yalnız SELECT). Kararlar Suer'den.
> - **ELL tarafı 14 Eyl – 8 Eki SIFIR hareket** (ell-docs'ta commit yok).
> - **LEENA:** 25 EMS/fuar commit'i (3'ü merge) + main dışı 1 dal. İkisi ortak boot dosyalarına
>   dokundu: `index.js` (qr-image ucu; boot mantığı değişmedi) · `email_worker.js` (nightly
>   rapor). Finans davranışı ETKİLENMEDİ; package.json / finans / ui2 / auth / migration / tests
>   temiz.
> - **14 Eyl kuyruğu 5/5 BEKLİYOR:** em-dash atıf biçimi · test kapsamı (test_users zincirde
>   değil) · TRUNCATE açığı · package.json zinciri · Faz 4 dilim 2.
> - **Üretim DB sayımı (8 Eki, Render Shell, yalnız SELECT — Suer koştu, CC görmedi):**
>   users 1 · sales_agents 152 · contracts 3 · payments 15, net 7.454,80 EUR ·
>   commission_payouts 8, net 390,00 EUR · ledger tablosu 0 · schema_migrations 028'de
>   duruyor, 032 şema izi canlı · terminals 50 anahtarlı / 20 aktif · "TEST OFFICE" ofisli
>   1 agent.
> - **Render oturumu read-only bayrağı OFF ile açıldı;** set yalnız SELECT'ti, yazma olmadı.
> - **İki repo PUBLIC** — bilinçli kabul edilmiş risk, sahibi Suer (K1).
> - **Sır envanteri çıkarıldı;** konum listesi repo public olduğu için deftere YAZILMAZ,
>   Orchestrator sohbetinde tutulur.
> - **Sınır kayması:** ölçüm sırasında CC bir token değerini tool çıktısında gördü; rapora
>   yazmadı.
> - **Kararlar (Suer, 8 Eki):**
>   - **K1** — repolar public kalır.
>   - **K2** — DB şifresi + JWT + ilk yedek + eliza-api askıya → **16 Eki+**; Kenya öncesi
>     restart yok.
>   - **K3** — Operations ekranlarının evi **ui2**; v402 yalnız çıkarma/temizlik.
>   - **Sıra:** Faz 4 dilim 2 → LEDGER → katalog/quote.
> - **Hız:** güvenlik, sistem bitince kapsamlı auditin konusu; tek istisna K2 (Faz A). Faz B
>   kuyrukta, tetik Suer.
> - **Kenya kilidi (13-15 Eki) DAR:** yasak = canlı LEENA'ya dokunan iş; serbest = LIFFY,
>   ui2'de yeni GET-only dosya (deploy kapı saatleri dışında), belge/plan.
> - **Çalışma ritmi:** her dilim bir ui2 ekranıyla kapanır; Suer görsel onayı şart. Haftada
>   tek hedef.
> - **v402 sayım uyuşmazlığı** (8≠9, 2≠3, 37≠16); kanıt dosyası repoda yok; mutabakat sonra.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** DB sayımları CC tarafından gözlenmedi (Suer'in aktarımı) ·
>   Render panel ayarları (auto-deploy dalı) ölçülmedi.
> - **Bilinçle yapılmayanlar:** sır temizliği/rotasyon (K2 → 16 Eki+) · em-dash · test zinciri ·
>   TRUNCATE · Faz 4 dilim 2.
> - **Commit:** yalnız bu defter (ell-docs). PUSH YOK.

> ## ✅ 2026-10-08 — ui2 FINANCE CONTRACT LİSTE EKRANI (yazıldı)
>
> - **Ne yapıldı:** ui2'de ilk gezilebilir finans akışı: ui2 girişi → contract listesi →
>   mevcut ui2 contract detayı. Yalnız okuma.
> - **Dosyalar (LEENA):** YENİ `public/ui2/finance-contracts.html` · DEĞİŞEN `public/ui2/index.html`
>   (yalnız tek link).
> - **Commit:** LEENA `8798dc6` "ui2: finance contract liste ekranı (read-only)".
> - **Veri kaynağı:** tek GET `/api/contracts` (mevcut uç, authMiddleware, organizer scope).
>   paid_eur / balance_eur SUNUCUDA hesaplanıyor (D2); ekran yeniden hesaplamaz, yalnız
>   biçimler. Satır → `finance-contract.html?contract=<id>`.
> - **EKSİK ALAN:** yok — 7 kolonun 7'si uçta mevcut (fuar ADI `expo_name` olarak geliyor).
> - **Ölçülenler:** `git diff --stat` = 2 dosya · tek fetch (GET) · paid/balance üzerinde
>   aritmetik yok · sahte veriyle Node harness: render + satır tıklaması doğru, HTML kaçışlı.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** gerçek tarayıcıda sunucu + test DB ile açılış (yerelde
>   `.env` canlı bilgi taşıyor, sunucu kaldırılmadı; headless Chrome bu ortamda yanıt vermedi).
>   Görsel kabul deploy sonrası Suer'de. Subnav "Contracts" sekmesi hâlâ detay sayfasına
>   gidiyor (shell.js kapsam dışı).
> - **Bilinçle yapılmayanlar:** shell.js / stil / backend / eski sayfalar / filtre / buton yok.
> - **Durum:** PUSH EDİLMEDİ. Push (SIEMA penceresi + status.render.com, 12 Eki öncesi) ve Suer
>   görsel onayı bekliyor. Dilim onayla kapanır; teyit sonraki dilimin kaydına düşer.

> ## ✅ 2026-10-08 — KENYA ÖLÇÜM PAKETİ + ui2 LİSTE KAPANIŞI
>
> - **ui2 liste ekranı KAPANDI:** Suer görsel onayı (canlı, 3 satır, paid/balance eski ekranla
>   birebir, satır→detay çalışıyor). Push: LEENA `02d8908..ae3cd4f` (merge, SIEMA PR #22
>   üstüne; mesajdaki ":wq" kozmetik, kalır), ell-docs `16868f1..bb51e55`. Render web + worker
>   Live. **Auto-Deploy main'de açık** (E6 kapandı) — Suer gözlemi, CC panelden görmedi.
> - **Ne yapıldı:** Kenya haftası kâğıt işlerinin girdisi ölçüldü (CC, LEENA salt-okunur,
>   DB bağlantısı YOK, setup script'i koşulmadı).
> - **0 — Durum:** iki repo yerelde zaten origin ile eşit (LEENA `ae3cd4f`, ell-docs `bb51e55`),
>   ff gerekmedi. `8895919..ae3cd4f` (8798dc6 hariç): `708daee` feat(footer) + `02d8908` PR #22
>   merge + `ae3cd4f` merge → üçü de YALNIZ `utils/trackingPixel.js` (e-posta footer'ı).
>   auth / middleware / migrations / tests / package.json / index.js / email_worker.js /
>   ui2 / finans route'larına dokunan YOK.
> - **1 — Migration + test DB (2c):**
>   - 030 = `callcenter_leads` tablosu + 4 index · 031 = `email_queue` üstünde 2 index
>     (`CREATE INDEX CONCURRENTLY`) · 032 = `users` + B10 trigger + `sales_agents.user_id`
>     uuid/FK + ilk Owner seed. **Üçü de (ve 029) `schema_migrations`'a kendini YAZMIYOR.**
>   - Kayıt mekanizması: runner YOK. 013 tabloyu kurar ve 000–012'yi toplu işler; 013–028
>     dosyaların her biri kendi INSERT'ünü taşır. `migrate.js` yalnız `initial.sql` koşar,
>     `schema_migrations`'a dokunmaz. Canlıda "028'de duruyor" bu yüzden — 029–032 uygulanmış
>     ama kayıtsız.
>   - Test DB setup: dizini okur, ≥012, DIŞLA-listesi 029/030/031 (gerekçeli), sayısal sıra →
>     **18 migration: 012–028 + 032. Sentez beyanı DOĞRU; 030/031 GİRMİYOR (bilinçli).**
>   - 030/031 şemasına dayanan finans testi YOK. Email smoke'ları `email_queue`'yu test DB'den
>     değil canlı/salt-okunur URL'den okur (test DB kapsamı dışında).
>   - Defter 2030 (TEST DB SENKRONU kapanışı) bugünkü kodla UYUŞUYOR. ⚠️ ★SIRADAKİ içindeki eski
>     "★★ TEST DB SENKRONU (ACİL)" maddesi BAYAT (2030 kaydıyla kapanmış).
> - **2 — Dilim 2 auth tabanı (bugünkü kod):**
>   - Login `POST /api/auth/login` → **`organizers`** tablosundan okur, bcrypt karşılaştırır;
>     token alanları **`organizer_id`, `email`**; süre **30 gün**. `POST /api/auth/register` da
>     `organizers`'a yazar.
>   - `authMiddleware` token doğrular, `req.organizer_id` yazar (eksik → 401, geçersiz → 403);
>     32 dosya require eder, ~116 route tanımında kullanılır. `dualAuth` yalnız
>     `routes/visitors.js`: `/paginated`, `/import` (bulk_print) + `/manual` (`forKinds(['scanner'])`);
>     JWT yolunda `req.organizer_id` + `authMode`, terminal yolunda `req.terminal`,
>     `scopedExpoId`.
>   - `middleware/auth.js` (req.user, gömülü fallback'li) **ÖLÜ:** hiçbir .js require etmiyor
>     (grep 0, OLD/backup dahil).
>   - `users` (032, sonrası değişiklik yok): id uuid · organizer_id FK · email UNIQUE ·
>     password_hash nullable · is_owner · display_role (yetkide kullanılmaz) ·
>     password_must_change · is_active · created_at. Trigger `trg_min_one_active_owner`
>     AFTER UPDATE OR DELETE, statement — TRUNCATE kapsamda değil. `sales_agents.user_id` uuid,
>     FK→users, UNIQUE (014), external için NULL zorunlu (021 CHECK).
>   - `users`'a giden route/middleware/utils kodu: **YOK** (grep 0).
> - **3 — B3:** `contracts.status` izinli değerler Active / On Hold / Transferred / Cancelled
>   (012 CHECK + kod sabiti). Transfer aksiyonu: kaynak `Transferred`'a çekilir, devam YENİ satır
>   (`Active`) ve yön `transferred_from_contract_id` ile tutulur (016 kolon, 019 tek-devam
>   index'i); "Transferred to" ters join'le türetilir; elle `Transferred`'a geçiş kapalı.
>   **Hüküm koda/şemaya UYUYOR** → kütüğe SEM-06 işlendi.
> - **4 — TEST OFFICE + TABAN:**
>   - "TEST OFFICE" repoda seed/migration/script olarak YOK; 026 seed'i yalnız 5 ofis. Aynı adı
>     yaratan tek kod `tests/test_offices.js` — ama hedefi test DB (`ell_comm_test`). Canlı
>     satırın kaynağı repodan BULUNAMADI (UI'dan elle açılmış olabilir — ölçülmedi).
>   - TABAN 342.00: monorepo CLAUDE.md "contract 4 sr earned = 342.00" der; defterde canlı
>     contract 4 doğrulamaları (ör. ui2 görsel turu). **Testler contract 4'e bağlı DEĞİL** —
>     T35 ve M01a kendi fixture'ını kurar (base 17.100 × %5 × 0,4). ui2 detay ekranı `?contract`
>     yoksa varsayılan 4'ü açar. → contract 4 silinirse testler kırılmaz; canlı çapa ve ui2
>     varsayılanı kırılır.
> - **5 — ell-docs `leena/CLAUDE.md` farkı:** çalışma kopyası (2369 satır) = LEENA `72a6d56`
>   (2026-09-07) sürümünün BİREBİR kopyası; LEENA HEAD (2899 satır) değil. Eksik bölümler:
>   v4.0.12–v4.0.21 + "Çalışma kuralları (Suer, 13 Eyl)". `leena/todo.md` çalışma kopyası
>   LEENA geçmişindeki hiçbir sürümle eşleşmiyor. Sır taşıyan satır sayıları ölçüldü (CLAUDE.md
>   ve todo.md'de var); içerik/konum burada YOK. Dosyalara dokunulmadı.
> - **Çalışma düzeni:** yalnız Orchestrator ↔ Suer ↔ Sentez. Eliza Audit ve v402 kapandı;
>   işleri Orchestrator kuyruğunda.
> - **Render bakımı 14 Eki 04:00 İstanbul** — o gece LEENA push'u yok.
> - **RTM nihai (Sentez hükümlü):**
>   - **B2:** contract_line_items UPDATE/DELETE engelleyen trigger — migration 16 Eki+ YAZILIR,
>     dilim 2 migration'ıyla aynı gece, AYRI dosya; test: UPDATE/DELETE reddi, INSERT serbest.
>   - **B3:** kütüğe işlendi (SEM-06).
>   - **B4 ve 4a-3:** aksiyon yok — password_hash NULL bilinçli, ilk-şifre akışı dilim 2'nin
>     parçası.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** DB (canlı/test) — bağlanılmadı · Render Auto-Deploy ve
>   Live durumu (Suer gözlemi) · TEST OFFICE canlı satırının kaynağı · route kullanım sayısı
>   (~116) satır-grep'idir, `router.use` düzeyi ayrıca sayılmadı.
> - **Bilinçle yapılmayanlar:** LEENA'da değişiklik · rotasyon runbook'u · dilim 2 tasarımı ·
>   migration yazımı (B2 dahil) · ledger ön-ölçümü · v402 sayımı · em-dash · test zinciri ·
>   ★SIRADAKİ'deki bayat ACİL maddesinin silinmesi.
> - **Commit:** ell-docs defter + kütük (tek commit). PUSH YOK.

> ## ✅ 2026-10-08 — RENDER ENVANTERİ + FAZ A ROTASYON ÖN-ÖLÇÜMÜ
>
> - **Render envanteri çıkarıldı** (Suer: panel + Shell, salt okuma): 19 servis (16 aktif,
>   3 askıda). Ayrıntılı envanter ve rotasyon runbook taslağı Orchestrator proje KB'sinde
>   (RENDER_ENVANTER, RUNBOOK_FAZ_A) — repo public olduğu için repoda DEĞİL.
> - **LEENA (Suer gözlemi):** web + worker Auto-Deploy On Commit · env group yok · health check
>   path boş. DB: Basic-1gb, PostgreSQL 17, PITR 7 gün + export var. Tüm tablolar uygulama
>   rolüne ait.
> - **Shell'den DB girişi:** `psql "$DATABASE_INTERNAL_URL"` veya argümansız `psql` çalışıyor.
>   Web'deki `DATABASE_URL` harici adresi gösteriyor ve Render içinden bağlanmıyor (neden
>   ölçülmedi).
> - **DÜZELTME (8 Eki ölçüm raporu):** "DATABASE_INTERNAL_URL Render ortamında tanımlı" —
>   çalışan uygulamanın env'inde YOK; yalnız Render Shell oturumunda var.
> - **LIFFY (Suer, SQL salt okuma):** DB'de Render credential rotasyonu YARIM (yeni default
>   kullanıcı var, servisler eski kullanıcıda). Yeni default kullanıcı eski sahibin rolüne üye,
>   tüm tablolarda okuma + yazma yetkili.
> - **Teknik karar (Orchestrator):** LEENA DB rotasyonu Render'ın "New default credential"
>   yoluyla, geçişten önce yetki kontrolüyle. Render desteğine soru gönderildi; cevap
>   bekleniyor, artık bloke etmiyor.
> - **Sentez'e açık:** konfeti / konfeti-db nedir · eliza-legacy'nin diğer 3 parçası
>   (dashboard, bot, db) hâlâ çalışıyor, karar yalnız eliza-api · LIFFY JWT_SECRET Faz A
>   kapsamında mı.
> - **B-4 bulguları (CC, kod salt-okuma; LEENA `ae3cd4f`, LIFFY `9954054`, ikisi origin'le eşit):**
>   - **1 — LEENA JWT:** `JWT_SECRET` okuyan çalışan kod yalnız `routes/auth.js` (sign),
>     `middleware/authMiddleware.js`, `middleware/dualAuth.js` (verify) — 8 Eki listesi
>     TAM, ek YOK. Ayrıca `middleware/auth.js` (gömülü fallback'li) okuyor ama hâlâ hiçbir
>     yerden require EDİLMİYOR (ölü). Testler kendi test-secret'ını kurar.
>   - **2 — JWT'siz yollar:** `terminalAuth` (yalnız `x-terminal-key` + DB lookup) ve iki
>     callcenter middleware'i (`x-callcenter-key` / `x-callcenter-supervisor-key` +
>     `CALLCENTER_*` env) JWT kullanmıyor → JWT rotasyonu terminal ve call-center
>     oturumlarını düşürmez; yalnız admin/organizer oturumları yeniden giriş ister.
>   - **3 — LEENA DB okuyucuları:** çalışan zincirde YALNIZ iki yer: `utils/db.js` (web,
>     `index.js`'ten erişilir) ve `email_worker.js` (worker, kendi Pool'u); ikisi de `PG*`
>     okur, SSL açık (worker yalnız production'da). `DATABASE_URL` / `DATABASE_INTERNAL_URL`
>     çalışan uygulamada OKUNMUYOR — yalnız tek başına script'lerde (migrate, setup-fresh-db,
>     debug/native-db, import-zoho-agents). `import-zoho-agents` önce `DATABASE_URL`'e bakar,
>     sonra `DATABASE_INTERNAL_URL`'e → Render Shell'de web'in harici `DATABASE_URL`'i önce
>     seçilir (Shell'de koşulursa bağlanamayabilir — ölçülmedi). `config/database.js`,
>     `public/utils/db.js`, `deep-debug.js`, `email_worker_backup.js` erişilmeyen ölü kopyalar;
>     `deep-debug.js`'de koda gömülü harici DB host fallback'i var (sır değil, temizlik adayı).
>   - **4 — eliza / konfeti:** LEENA kodunda eliza-api'ye ya da eliza host'una çağrı YOK
>     ("eliza" yalnız ui2 marka/tema ve yorumlarda). "konfeti" LEENA'da ve LIFFY'de (izlenen +
>     izlenmeyen) HİÇ geçmiyor.
>   - **5 — Mac'teki yerel sır dosyaları:** repo dışı/izlenmeyen **5 yerel dosyada** DB/JWT
>     değişkeni ya da bağlantı dizesi var (LEENA 2, LIFFY 1, CC proje ayarları 2 — ayarlar
>     ignore'lu, hiç commit edilmemiş). Ayrıca repoda izlenen 3 `.env.backup` (bilinen). CC'nin
>     LEENA salt-okunur bağlantısı (`claude_readonly`) LEENA backend'in yerel env dosyasında;
>     **CC'nin LIFFY bağlantısı LIFFY uygulama rolüyle** (salt-okunur rol değil) ve CC proje
>     ayarlarında duruyor; CC'nin LEENA proje ayarlarında da 1 uygulama-rolü bağlantısı var →
>     Faz A rotasyonu bu yerel girdileri de bozar, runbook'a "yerel güncelleme" adımı gerekir.
>   - **6 — LIFFY kodu:** `DATABASE_URL` 5 yerde (uygulama: `config.js`, `db.js`; 3 script).
>     `JWT_SECRET` 30 dosyada okunuyor ve **30 dosyanın 30'unda koda gömülü fallback** var
>     (3 farklı literal). LIFFY repo da PUBLIC → env'de `JWT_SECRET` tanımsız kalırsa token
>     sahtelenebilir. Faz A kapsam kararına girdi.
> - **YON-05 notu:** bu oturumda Orchestrator, defterde yazılı Shell komutunu aramadan yanlış
>   komut verdi ve `env` çıktısından değişkenin yokluğuna hükmetti. Ders: Shell komutu
>   vermeden önce defter/KB aranır.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** Render panel/Shell bulguları (Suer gözlemi) · LIFFY DB yetki
>   durumu (Suer SQL'i) · üretimde `JWT_SECRET`'ın LEENA/LIFFY env'inde tanımlı olup olmadığı ·
>   web `DATABASE_URL`'in neden bağlanmadığı · require grafiği statik (göreli `require`),
>   dinamik yükleme taranmadı.
> - **Bilinçle yapılmayanlar:** rotasyon · runbook yazımı · LEENA/LIFFY'de değişiklik · DB
>   bağlantısı · Render API.
> - **Commit:** yalnız bu defter (ell-docs). PUSH YOK.

> ## ✅ 2026-10-08 — FAZ 4 DİLİM 2 YAZILDI (dal, push yok)
>
> - **Sentez kararları:**
>   - **K-A token:** mevcut JWT + `uid`; AYNI secret, AYNI süre (30 gün), AYNI middleware
>     (`authMiddleware` `organizer_id` okur → mevcut route'lar yeni token'la değişmeden çalışır).
>   - **K-B ilk şifre:** Render Shell script'i; yalnız Owner hash'i NULL iken yazar, EZME YOK.
>   - **K-C:** Kenya'da ayrı dal; Faz A ile aynı gece DEĞİL, Faz A önce.
>   - **033 şartı:** 029–032 için geriye dönük `schema_migrations` kaydı YALNIZ şema izi
>     kanıtlıysa (izi olmayan eklenmez; `applied_at` NULL — kayıt uygulama kanıtı değildir).
> - **Suer onayı (8 Eki):** K2 aynen kalır — şifre/anahtar değişimi 16 Eki+.
> - **Dal:** LEENA `faz4-dilim2` (main `ae3cd4f`'den) · commit **`49fa217`**. main'e DOKUNULMADI,
>   PUSH YOK.
> - **Eklenen dosyalar:** `routes/userAuth.js` (login · me · change-password) ·
>   `migrations/033_users_truncate_guard.sql` · `scripts/set-first-owner-password.js` ·
>   `public/ui2/login.html` · `public/ui2/whoami.html`. **Değişen:** `index.js` (tek mount satırı) ·
>   `package.json` (test zincirine `test_users.js`) · `public/ui2/index.html` (link) ·
>   `tests/test_users.js` (+18 test).
> - **Ölçümler (yazmadan önce):** çalışan uygulama `contract_line_items`'a UPDATE/DELETE yapmıyor ·
>   B10 fonksiyonu TG_OP'a bakmıyor → AFTER TRUNCATE'te aynen çalışır · `authMiddleware` fazla
>   claim'i reddetmiyor, yalnız `organizer_id`'yi req'e koyuyor → `me` için ayrı küçük middleware
>   (route dosyasında) · token anahtarı tek: `token` · bcrypt 10, JWT 30 gün, register uzunluk
>   kuralı ≥6 · `schema_migrations(version PK, applied_at)` · 033/034 numaraları boştu.
> - **Testler (yerel test DB):** önce **132** (finans 120 + users 12) → sonra **150/150**
>   (finans 120 + users 30), ikinci koşu aynı (idempotent). **TABAN 342.00 KAYMADI** (T35 + M01a).
>   Setup 033'ü otomatik aldı (19 migration). Test DB'de 033 yalnız 032 kaydını ekledi; izi
>   olmayan 029/030/031 eklenmedi (R1 testi). TRUNCATE users (CASCADE dahil) reddedildi (T1).
> - **034 BLOKE (yazılmadı):** `contract_line_items` UPDATE/DELETE reddi trigger'ı mevcut altı
>   finans suite'ini kırar — reset'leri `DELETE FROM contract_line_items` yapıyor. Testler
>   sessizce değiştirilmedi. → **Sentez kararı:** test reset yolu (ör. test-only bypass /
>   TRUNCATE / şema yeniden kurma) ya da trigger kapsamı.
> - **Orchestrator / CC varsayılanları (Sentez onayı bekliyor):**
>   - Uç yolu `/api/user-auth/*`.
>   - Eski-login token'ı `me`'de **409 `NOT_USER_SESSION`** (401/403 değil — leena-fetch 401/403'te
>     oturumu siler).
>   - Yanlış mevcut şifre **400** (aynı neden).
>   - Şifre uzunluğu ≥6 (register kuralı; 10 varsayılanı KULLANILMADI çünkü kural mevcuttu).
>   - Kullanıcı yokken de bcrypt karşılaştırması (zamanlama eşitliği).
>   - Script: birden fazla şifresiz aktif Owner varsa yazmaz ("ambiguous").
>   - ui2 login yalnız `token` anahtarını yazar (`organizer` / `organizerId` yazmaz).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** canlı DB (bağlanılmadı; 033'ün canlıda hangi geriye dönük
>   kayıtları ekleyeceği canlı şemaya bağlı) · script'in etkileşimli CLI kısmı (gizli giriş,
>   onay) — yalnız mantık fonksiyonu test edildi · ui2 login/panel gerçek tarayıcıda açılmadı ·
>   `index.js` uygulama olarak ayağa kaldırılmadı (yalnız sözdizimi kontrolü).
> - **Bilinçle yapılmayanlar:** eski login/register · authMiddleware · dualAuth · shell.js ·
>   leena-fetch · rol/yetki matrisi · organizers taşıması · ikinci kullanıcı · sıfırlama e-postası
>   · rate limit · 034.
> - **Kapanış (Faz A gecesinden SONRAKİ pencerede):** merge + push + 033 (Suer koşar; 034
>   kararından sonra) + ilk şifre (Suer, script) + ui2 görsel onay.
> - **Commit:** yalnız bu defter (ell-docs). PUSH YOK.

> ## ✅ 2026-10-08 — SENTEZ KAPANIŞ KARARLARI + 034 (dal)
>
> - **K-D — 034 kontrat kalemi değiştirilemez:** trigger `contract_line_items` üzerinde UPDATE +
>   DELETE + TRUNCATE'i reddeder (statement-level BEFORE), INSERT serbest. Açık adlı oturum
>   anahtarı `ell.allow_line_item_reset`, varsayılan KAPALI (tanımsız/boş/'on' dışı = kapalı);
>   yalnız test kurulumu/temizliği açar (`SET LOCAL`, transaction süresince). Ürün kodunda anahtar
>   YOK — kaynak taraması testi bunu bekçiler.
>   - Ölçüm (yazmadan önce): ürün kodunda bu tabloya UPDATE/DELETE yok · FK ON DELETE CASCADE
>     yok · ürün kodunda contracts silme yok → durma koşulu tetiklenmedi. Kodda önceden
>     `current_setting` ile okunan özel ayar yoktu → `ell.` öneki ilk kez kullanıldı.
>   - Test: altı finans suite'inin tek satırlık kalem temizliği ortak yardımcıya geçti
>     (assertion'lara dokunulmadı). `test_users` T1 (TRUNCATE users CASCADE) artık kalemlere de
>     iner; B10'u ölçmeye devam etsin diye anahtar yalnız o geri alınan transaction'da açılır.
>     Yeni suite 11 test.
>   - **Dal `faz4-dilim2` commit `3d9896a`** (dilim 2 = `49fa217` + `3d9896a`). Test **150 → 161/161**
>     (finans 120 + users 30 + line-item 11), iki koşu aynı. **TABAN 342.00 KAYMADI.**
>   - Kapanış: dilim 2 ile aynı pencerede (merge + push + 033 + 034 Suer koşar), Faz A gecesinden
>     SONRA. main'e kod girmedi, PUSH YOK.
> - **K-E — LIFFY JWT_SECRET Faz B'de;** fallback temizliği + "env yoksa başlama" koruması ile
>   (YON-08).
> - **konfeti / konfeti-db:** Suer'in kişisel servisi (davetiye), ELL dışı, DOKUNULMAZ.
> - **eliza-legacy (api, dashboard, bot, db) KALIR:** Suer WhatsApp botunu ve dashboard'u
>   kullanıyor (Zoho salt-okunur ayna). Kapatma birleşme sonrası, yeni sistem aynı cevapları
>   verince. **Faz A'dan A4 düştü.** Zoho/Twilio anahtarları Faz B kuyruğunda.
> - **`/me`'de eski token → 409:** geçici köprü (leena-fetch 401/403'te oturumu siliyor);
>   rol/yetki diliminde yeniden ele alınır.
> - **Şifre ≥ 6:** bugün tek kullanıcı Suer; yetki diliminde SaaS ölçüsüne çekilir (YON-07) —
>   kuyruk.
> - **033 geriye dönük kayıtlar `applied_at` NULL:** doğru, tarih uydurulmadı.
> - **Kullanıcı başına mail limiti:** LIFFY Faz 1b'de mevcut (worker günlük limit, kullanıcı
>   bazlı); gereksinime "mevcut davranış" olarak yazılması belge borcu — Kenya kâğıt listesi.
> - **Kenya sırası:** 2d ledger ön-ölçümü → v402 temizlik sayımı.
> - **Kütük:** AD-01'e not eklendi (eliza-legacy emekli = üzerine inşa edilmez; birleşmeye kadar
>   okuma aracı olarak serviste).
> - **★SIRADAKİ:** "eliza-api askıya" maddesi ★SIRADAKİ'de YOKTU (yalnız 8 Eki K2 tarihsel
>   kaydında geçiyor — tarihsel kayıt değiştirilmedi); kuyruk maddeleri ve belge borcu eklendi.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** canlı DB (034'ün canlı tabloda reddettiği bir iş akışı
>   olup olmadığı yalnız koddan ölçüldü) · `index.js` ayağa kaldırılmadı · ui2 sayfaları
>   tarayıcıda açılmadı.
> - **Bilinçle yapılmayanlar:** main'de kod · push · merge · canlı DB · rol/yetki · LIFFY.
> - **Commit:** defter + kütük (ell-docs, tek commit). PUSH YOK.

> ## ✅ 2026-10-08 — 2d LEDGER ÖN-ÖLÇÜMÜ
>
> - **Ne yapıldı:** ledger (hesaplar · transfer · bütçe · gider · gelir) için salt-okunur ön-ölçüm;
>   öneri/tasarım/karar YOK. Çıktı: **`LEDGER_ON_OLCUM_2026-10-08.md`** (kök — README'de belge türü
>   klasörü tanımlı değil).
> - **Sayılar:** gereksinim maddesi **21** (REQ §2.6 + 3.1/3.3/3.4/3.5/3.6/3.9 + 1.2/1.5 + Part 5) ·
>   boş/TBD **17** (en önemlileri: transferin veri şekli, sahip-ödemeli gider mekanizması, gider
>   onayı, gider belgesi/makbuz, bütçe yetkisi, gelir hedefi yapısı, dönem tanımı) · belgeler arası
>   çelişki **9** (biri belge↔kod farkı olarak işaretli: komisyon ödemesi REQ'de gider kaydı,
>   LEENA'da ayrı payout tablosu).
> - **LEENA bugün:** ledger tablosu YOK (migrations + initial.sql grep 0); ledger'a değen yapılar
>   `contracts` kur/EUR kolonları · `payments` (+ters kayıt, ofis, vade bağı) · `payment_schedule_items` ·
>   `commission_payouts` · `offices` · nakit öngörü / agent ekstresi / komisyon uçları. `payments`'ta
>   `account_id` + `payer` bilinçli olarak ledger fazına bırakılmış.
> - **Sentez kriter turuna girdi.**
> - **KB @ 5e8b193** — Orchestrator KB yenilendi (8 Eki 21:50); Sentez KB: ölçülmedi.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** DB (canlı/test) · Zoho'nun kendisi ve ZOHO_USAGE_REFERENCE ·
>   LIFFY · Sentez KB · `ELL_MIMARI_v1.0_KONSOLIDE.md`, `HANDOVER_BRIEF.md`,
>   `ELL_FEATURE_INSPIRATION.md`, `archive/` taranmadı.
> - **Bilinçle yapılmayanlar:** öneri · tasarım · karar · LEENA'da değişiklik · dal değişikliği.
> - **Commit:** yeni dosya + bu defter (ell-docs). PUSH YOK.

> ## ✅ 2026-10-08 — LEDGER KRİTER HÜKÜMLERİ
>
> - **Ne:** Sentez'in 8 Eki ledger kriter hükümleri + Suer kararları kanonik belgelere işlendi
>   (kütük LED grubu, REQ ve glossary amendment'ları). Girdi: `LEDGER_ON_OLCUM_2026-10-08.md`
>   (Ç1–Ç9, boşluk 1–17). Kod / migration / tasarım YOK.
> - **Çelişki hükümleri:**
>   - **Ç1** — REQ v1.0 tamamdır, amendment'lıdır; "In progress" künyesi tarihsel; Part 2/3
>     başlarındaki `[TBD]` işaretleri kaldırıldı (altları dolu).
>   - **Ç2** — defter/kütük kazanır: ödeme değiştirilemez, düzeltme ters kayıt (TAH-01, ODE-03).
>     ADR-011'in düzenle/sil satırlarına SUPERSEDED notu; rol/kapsam kısmı (yerel ofis kısıtlı
>     form, kendi ülkesi) Faz 4 yetki girdisi olarak geçerli kalır.
>   - **Ç3** — ödeme yöntemi SEM-01'in 5 değeri; SWIFT = `bank_transfer`; kredi bakiyesi ledger olayı → **LED-01**.
>   - **Ç4** — para birimleri referans tablosu (8 birim, ISO, TL→TRY), arayüz tablodan okur → **LED-02**.
>   - **Ç5** — "account" = para hesabı; Zoho Account = company → **LED-03**.
>   - **Ç6** — "Transferred In/Out" = SEM-06'dan türetilmiş gösterim (REQ + glossary notu;
>     ADR-012'ye de aynı not).
>   - **Ç7** — tek kaynak: tutar bir kez saklanır, ledger hareketi payout/payment'a FK ile
>     bağlanır, gelir `payments`'tan türetilir (D2) → **LED-04**.
>   - **Ç8** — kur satırda değişmez; kur düzeltmesi = ters kayıt + yeni kayıt → **LED-05**.
>   - **Ç9** — `payer` alanı ledger v1'de VAR (R7). Proforma = belge üretimi, ledger dışı; fatura
>     kapsamıyla birlikte sonraki faz.
> - **Boşluk hükümleri:**
>   - **1** (Sentez kriteri) — transfer: tek mantıksal olay, iki bağlı hareket, tek atomik yazım → **LED-06**.
>   - **2** (Sentez kriteri) — sahibin cari hesabı "owner" tipinde sanal hesap → **LED-07**.
>   - **3** (Suer kararı) — gider onayı YOK; düzeltme ters kayıt; "kim girer" Faz 4 → **LED-08**.
>   - **4** (Suer kararı) — makbuz: v1'de gider kaydında nullable belge bağlantısı alanı (Drive URL
>     deseni); dosya yükleme kurulmaz.
>   - **5** (Suer kararı) — bütçe: Owner kilitler; kilit sonrası yalnız revizyon; kilidi Owner açar → **LED-09**.
>   - **6** (Suer kararı) — gelir hedefi expo başına TEK EUR rakamı; gider bütçesi kategori/tip satırlı.
>   - **7** — kur farkı kâr/zarar: v1 dışı.
>   - **8** — bölünmüş atıf: yok (REQ 1034).
>   - **9 / 10 / 11** — muhasebe aktarımı, e-fatura, online tahsilat: sonraki faz.
>   - **12** — yerel ofis gider yetkisi: Faz 4 yetki matrisi; şema `office_id` taşır.
>   - **13** — banka mutabakatı: v1 dışı.
>   - **14** — dönem: raporlar tarih aralığıyla; sabit mali yıl kavramı YOK; expo ekseni `expo_id`
>     ile (ADR-012: mali yıl ≠ edisyon).
>   - **15** — tarihsel transfer aktarımı: Faz 6 göç ölçütü.
>   - **16** — hesap türleri: banka · kasa · sanal (owner dahil). Şema kişiye cari hesap açmaya izin
>     verir (hesap ↔ kişi bağı nullable), UI'da yalnız owner.
>   - **17** — `[TBD]` işaretleri: Ç1 ile kapandı.
> - **Kesit sırası (dilim 2 kapanışından SONRA, her biri bir ui2 ekranıyla):**
>   - **L-1** hesaplar + referans veri (para birimleri, gider/gelir kategorileri — Zoho tohumlu) +
>     hesap ekstresi ekranı
>   - **L-2** transferler (iki hareket) + owner hesabı
>   - **L-3** giderler (belge bağlantısı alanı dahil)
>   - **L-4** `payments`'a `account_id` + `payer`; payout ↔ ledger bağı; gelir görünümü
>   - **L-5** expo bütçesi (revizyon + kilit) vs gerçekleşen
>   - **L-6** nakit / alacak / komisyon özet raporu (R12, R15)
>   - Migration'lar yazılır, Suer koşar; canlı LEENA'ya dokunan her kesit fuar takvimine göre
>     pencereye girer.
> - **Ortak kurallar (tüm kesitler):** tutar değiştirilemez (düzeltme ters kayıt) · EUR karşılığı
>   girişte donar (R4, RAP-01) · hiçbir bakiye saklanmaz (R13/D2) · TABAN 342.00 korunur.
> - **Eklenen kütük ID'leri:** LED-01 · LED-02 · LED-03 · LED-04 · LED-05 · LED-06 · LED-07 ·
>   LED-08 · LED-09 (yeni grup "LED — ledger").
> - **REQ amendment (2026-10-08):** üstte tarihli amendment bloğu (07-20 amendment'ının biçimi) +
>   ilgili satırlarda kısa işaret: künye, iki `[TBD]`, para birimi (1.2 ve 3.5), ödeme yöntemi,
>   Transferred Out/In, kur düzeltmesi (3.6), mail limiti (2.7) + §6.4 sürüm geçmişine bir satır.
>   **Mail limiti:** LIFFY'de mevcut davranış bulundu ve REQ'e kanıtıyla "mevcut davranış" olarak
>   yazıldı (kullanıcı başına günlük limit, varsayılan 500, takvim günü, kampanya sahibi bazlı;
>   worker batch'i kalan hakka kırpar). Kenya kâğıt listesindeki belge borcu KAPANDI.
> - **Glossary amendment:** "account" satırı (LED-03), Zoho eşleme maddesi, kontrat statüleri (Ç6).
> - **ADR notları:** ADR-011 (Ç2, düzenle/sil SUPERSEDED; rol/kapsam Faz 4 girdisi) ve ADR-012
>   (Ç6, In/Out türetilmiş gösterim) mevcut tarihli-blockquote biçimiyle notlandı; metin silinmedi.
> - **16 Eki+ sonrasına kalanlar:** ADR-011/012 LEENA'da DEĞİL, ell-docs'ta → Kenya kilidine
>   takılmadı, aynı gün notlandı. LED-02'nin kod
>   karşılığı (para birimi tablosu + arayüz listelerinin tablodan okuması) LEENA işi → Kenya
>   kilidi, 16 Eki+; ledger kesitleriyle planlanır.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** LIFFY mail limiti canlıda hangi değerlerle çalışıyor (DB
>   ölçülmedi) · LEENA'da değişiklik yok · Sentez'in kaynak metni CC tarafından görülmedi
>   (Orchestrator brief'inden aynen aktarıldı).
> - **Bilinçle yapılmayanlar:** LEENA / LIFFY değişikliği · DB · ledger tasarımı · yeni belge.
> - **Commit:** kütük + REQ + glossary + bu defter (ell-docs, `900ec25`); tamamlama + ADR notları
>   ayrı commit. PUSH YOK.
> - **Tamamlama:** Orchestrator brief'i ilk turda eksikti; metinler aynı gün eklendi.

> ## ✅ 2026-10-08 — DİLİM 2 SEM-05 HİZALAMA (dal)
>
> - **Ne uyuşmuyordu:** kütük SEM-05 (Sentez 13 Eyl, dilim 2 öncesi BAĞLAYICI) dilim 2 için
>   JWT'de `user_id` + `name` ve `ui2CurrentUser()`'ın SENKRON kalmasını ister. Dal `3d9896a`
>   token'a `uid` koymuştu, `name` yoktu; yeni ui2 login yalnız `token` yazdığı için
>   `ui2CurrentUser()` ya boş (`{name:'User', id:null}`) ya da önceki klasik oturumdan kalma
>   organizer'ı (yanlış kişi) döndürüyordu.
> - **Ne değişti (dal `faz4-dilim2`, commit `a67ab0f`):**
>   - Claim `uid` → **`user_id`**; tüm okuyucular güncellendi (`/me` artık `user_id` döner).
>   - `ui2CurrentUser()` senkron kaldı, fetch eklenmedi: ui2 login, yanıttaki kimliği YENİ
>     `ui2User` anahtarına token'a bağlı olarak (son 16 karakter) yazar; kabuk bu kaydı yalnız
>     o token hâlâ geçerliyse okur, aksi hâlde klasik davranış (`organizer` / `organizerId`)
>     birebir sürer. Eski login'in anahtarlarına dokunulmadı.
>   - Yeni test `test_ui2_current_user.js` (8): gerçek `shell.js` sahte depolamayla koşulur;
>     senkron dönüş, doğru kullanıcı, bayat kayıt yok sayılır, klasik/boş davranış değişmedi.
> - **`name` durumu: Sentez kararı bekliyor (EKLENMEDİ).** Kanıtlı tek kaynak yok: `users`'ta ad
>   kolonu yok (032); `organizers.name` kiracının adı (SEM-05: organizers saf kiracı);
>   `sales_agents.name` yalnız isteğe bağlı `user_id` bağıyla (canlıda dolu 0). Şema değişikliği
>   gerekeceği için yazılmadı. Kabuk gösterim için geçici olarak e-postayı kullanıyor (CC varsayılanı).
> - **Testler:** 161 → **169/169** (finans 120 + users 30 + line-item 11 + ui2-current-user 8),
>   iki koşu aynı. **TABAN 342.00 KAYMADI.**
> - **ADR INDEX:** ADR-011 satırı ve özet maddesi "PARTIALLY SUPERSEDED 2026-10-08" notu aldı.
> - **YON-05 notu:** Orchestrator dilim 2 brief'ini yazmadan önce kütüğü taramadı; SEM-05 atlandı.
>   **Ders:** dilim brief'inden önce kütükte ilgili grup aranır.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** ui2 login → kabuk akışı gerçek tarayıcıda denenmedi
>   (`ui2CurrentUser` birim testi gerçek `shell.js` ile; `login.html`'in yazımı kaynak kontrolü
>   + testte aynı biçimle kuruldu) · canlı DB.
> - **Bilinçle yapılmayanlar:** `name` · main'de kod · push · merge · eski login · authMiddleware ·
>   dualAuth · leena-fetch · migration.
> - **Commit:** LEENA dal `a67ab0f` · ell-docs defter + INDEX. PUSH YOK.

> ## ✅ 2026-10-19 — YENİDEN BAŞLAMA: KİLİT KALKTI, TEK YOL HARİTASI
>
> - **Kilit kalktı (Suer, 19 Eki):** Kenya bitti; uzun süre fuar yok. Fuar pencereleri, Kenya
>   kilidi ve SIEMA koordinasyonu KALKTI. Tek kontrol: **status.render.com**. Suer bir sonraki
>   fuar takvimini bildirince kilit yeniden tanımlanır.
> - **Chat düzeni:** yalnız Orchestrator ↔ Suer ↔ Sentez. Eski Orchestrator sohbeti kapandı;
>   yeni sohbet bu kayıtla açılır.
> - **Ölçüm 1 — repolar (CC, 19 Eki; fetch sonrası):**
>   - LEENA yerel `main` = `ae3cd4f` (8 Eki ile aynı); `origin/main` = `08f76cb` → yerel 0 ileri,
>     **2 geri**. Çalışma kopyası 8 Eki ile aynı: 1 M (`backend/leena-v401-backend/.DS_Store`) +
>     22 izlenmeyen. Stash 2 (eski filter-branch kayıtları).
>   - `ae3cd4f..origin/main`: `48c12e1` (12 Eki, Kenya konferans sertifikası) + `08f76cb` (PR #23
>     merge). Dosyalar: `public/certificate-ke.html` (A), `public/certificate.html` (M),
>     `routes/conferenceCertificates.js` (M). auth / userAuth / middleware / migrations / tests /
>     package.json / index.js / email_worker.js / ui2 / finans: **hiçbirine dokunulmadı** →
>     **"dilim 2 tabanı değişmedi" DOĞRULANDI.**
>   - Dal `faz4-dilim2` HEAD `a67ab0f` (yalnız yerel; origin'de yok), merge-base `ae3cd4f`.
>     origin/main'e göre 2 geri / 3 ileri. Merge dry-run (yerel main'e `--no-commit --no-ff`):
>     **çakışma YOK**, 20 dosya; `--abort` sonrası HEAD `ae3cd4f` ve `status` önceki ile birebir.
>     `origin/main`'e karşı `git merge-tree`: **çakışma YOK** (iki tarafın ortak dosyası 0).
>   - Migrations: `ae3cd4f`'ten sonra main'e yeni dosya YOK (son `032`). `033`/`034` tüm
>     ref'lerde yalnız `faz4-dilim2`'de → **numara çakışması YOK**, yeniden numaralama gerekmez.
>   - `package.json` test zinciri: main 6 dosya (`test_users` zincirde DEĞİL); dal 9 dosya
>     (`test_users` + `test_line_item_immutable` + `test_ui2_current_user` eklendi).
>   - ell-docs: `main` origin'den 1 ileri (`2ad238a` push edilmedi). `leena/CLAUDE.md` ve
>     `leena/todo.md` commit'lenmemiş farkı **hâlâ VAR**. Sır taraması (değer basılmadan, satır
>     sayısı): CLAUDE.md'de koda gömülü JWT fallback literal'i geçen 2 eklenen satır; şifre /
>     bağlantı dizesi / anahtar biçimli satır bu kalıplarla 0. 8 Eki'deki sayımın kalıbı defterde
>     yok → birebir karşılaştırma ÖLÇÜLMEDİ. Dosyalara dokunulmadı.
> - **Ölçüm 2 — testler (yerel `ell_comm_test`):** main zinciri **120/120** + `test_users` ayrıca
>   **12/12** = **132** (8 Eki referansı ile aynı). Dal, ayrı worktree'de: **169/169** (finans 120 +
>   users 30 + line-item 11 + ui2-current-user 8); **T35 TABAN sr earned 342.00 KAYMADI**.
>   Worktree kaldırıldı (`git worktree list` yalnız ana kopya + başka oturumdan kalma `om19`).
> - **Ölçüm 3 — Faz A girdileri:**
>   - LEENA `JWT_SECRET`/`PG*`/`DATABASE_URL`/`DATABASE_INTERNAL_URL` okuyan dosyalar: main
>     `ae3cd4f` ile `origin/main` AYNI (48 dosya) → 8 Eki E4 listesine fark YOK. Dal +2:
>     `routes/userAuth.js` (`JWT_SECRET` verify :39, yoksa reddet :57, sign :77) ve
>     `scripts/set-first-owner-password.js` (yalnız `PG*`). → Merge sonrası rotasyonda JWT
>     okuyan çalışan kod listesine `routes/userAuth.js` girer.
>   - LIFFY `liffyv1` `9954054` (= origin, 8 Eki ile aynı): DB yalnız `DATABASE_URL` —
>     `backend/config.js:5`, `backend/db.js:20` + 3 script; `PG*`/`DATABASE_INTERNAL_URL` yok.
>     Süreçler: `npm start` = `node backend/server.js`; sequence ve action worker aynı süreçte
>     (`server.js:122-133`); ayrı `backend/worker.js` de `./db` → aynı `DATABASE_URL`. Render'da
>     worker.js'i hangi servisin koştuğu ÖLÇÜLMEDİ (repoda render.yaml/Procfile yok).
>     `liffy-ui` `7b15ced`: DB/JWT env okumuyor.
>   - İlk-şifre script'i: dal `scripts/set-first-owner-password.js` (111 satır). Bağlantı yalnız
>     ortamdaki `PG*`, dotenv yüklemez (:9); `PGHOST`/`PGDATABASE` yoksa çıkar (:75). Hash
>     doluysa yazmaz ("hash dolu, değişiklik yok", ROLLBACK) — ama bu kontrol "evet" onayı ve
>     şifre sorulduktan SONRA yapılır (:86-93). **Ad SORMUYOR** (K-F henüz uygulanmadı).
> - **K-F (Sentez 19 Eki):** `users`'a nullable ad kolonu, dilim 2 penceresinde AYRI migration;
>   Owner adı ilk-şifre script'inde alınır; token `name` doluysa taşır, boşsa e-posta.
> - **K-G (Sentez 19 Eki):** `shell.js` sapması kabul. Kriter: "eski davranış değişmez; ekleme
>   geriye uyumlu ve testli olmak şartıyla serbest".
> - **TEK YOL HARİTASI** (★SIRADAKİ'ye taşındı; eski sıralar tarihsel):
>   1) **Faz A** — export + DB şifresi + LIFFY DB + JWT (A4 yok).
>   2) **Dilim 2** — merge, push, 033 + 034 + ad kolonu (üç dosya, Suer koşar); ilk-şifre
>      script'i; ui2 login / "kim girdi" görsel onay. **İş 1 ve İş 2 aynı gün, arka arkaya; İş 1 önce.**
>   3) Faz 4 kalan: kullanıcı yönetimi ekranı (davet, aktif/pasif, yetki matrisi çekirdeği).
>   4) Ledger L-1…L-6.
>   5) Katalog/quote (LIFFY aktivasyon paketi).
>   6) Zoho göçü + raporlama.
>   Paralel/sonda: v402 temizlik sayımı (L-1 sonrası) · Faz B · em-dash · test zinciri.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** canlı DB (bağlanılmadı) · Render servis/env durumu ve
>   status.render.com · LIFFY'de `worker.js`'i koşan Render servisi · 8 Eki sır-satırı sayımıyla
>   birebir karşılaştırma · dalın `origin/main` üstünde test koşusu (yerel main 2 geri; aradaki
>   commit'ler test zincirine dokunmuyor) · ui2 login gerçek tarayıcıda.
> - **Bilinçle yapılmayanlar:** LEENA'da commit/merge/checkout/pull · migration · push ·
>   ell-docs `leena/*` farkı.
> - **Commit:** ell-docs yalnız defter. PUSH YOK (Suer).

> ## ✅ 2026-10-21 — FAZ A / A0: EXPORT + RESTORE KANITLANDI
>
> - **Üç export (Suer, Render paneli, 19 Eki):** LEENA `2026-10-19T15_00Z.dir.tar.gz`
>   (1.421.091.698 B) · LIFFY `2026-10-19T15_29Z.dir.tar.gz` (164.612.955 B) · eliza-db
>   `2026-10-19T15_33Z.dir.tar.gz` (1.365.677 B). Yalnız LEENA'nınki açıldı; `~/Downloads`'taki
>   üç dosyaya dokunulmadı.
> - **Export anı:** dosya adı `15_00Z`; arşiv başlığı "Archive created at 2026-10-19 15:02:12 +03".
>   Veriden ölçülen pencere: staging'deki en geç satır `email_events.created_at` **14:54:15 UTC**;
>   canlıda olup staging'de olmayan ilk satır **15:02:58 UTC** → dump anı 14:54:15–15:02:58 UTC
>   arasında. "+03" büyük olasılıkla saat dilimi etiketi, saat UTC (15:02 UTC) — **doğrulanmadı**;
>   "12:02 UTC" okunuşu veriyle ÇÜRÜDÜ.
> - **Staging DB:** `leena-staging-db` (Render, Oregon), db `leena_staging_db`, user
>   `leena_staging_db_user`, **PostgreSQL 17.11**. Kalıcı staging. URL repo dışında, 600 izinli
>   yerel dosyada; hiçbir yere basılmadı. Plan: ÖLÇÜLMEDİ (panel görülmedi).
> - **Adım 1 — ölçüm:** PATH'teki `pg_restore`/`psql` 14.20 → kurulu `postgresql@17` (17.10)
>   kullanıldı, yeni kurulum yok. Dump: DIRECTORY formatı, `toc.dat` var, sıkıştırmasız, 17.11'den
>   alınmış; 544 TOC girdisi: **75 TABLE** (+75 TABLE DATA) · 39 SEQUENCE · 69 INDEX · 61
>   CONSTRAINT · 84 FK · 3 FUNCTION · 2 TRIGGER · 3 EXTENSION (`pg_stat_statements`, `pgcrypto`,
>   `uuid-ossp`). Sahip rolü `leena_v401_db_user` 533 girdide. Açık boyut 16,39 GB (15,94 GB'ı
>   `email_queue` veri dosyası). Staging restore öncesi boş (public 0 tablo).
> - **Adım 2 — restore:** `pg_restore --no-owner --no-privileges --jobs 4`.
>   - Deneme 1 (19 Eki 16:01:48 UTC) WARP kapatılırken ağ değişince koptu (16:04:50, "Operation
>     timed out" + "worker process died", rc=1) → staging yarım kaldı; CC'nin sıfırlama komutu izin
>     sınıflandırıcısınca engellendi, **Suer sıfırladı**; boşluk yeniden doğrulandı (0 tablo).
>   - Deneme 2: **19 Eki 16:21:10 → 22:48:26 UTC (6 sa 27 dk), rc=0, hata satırı 0, "errors
>     ignored" YOK**, extension hatası yok. Süreyi `email_queue` COPY'si belirledi (~0,1 MB/sn
>     sunucu tarafı). Mac uykusu `caffeinate -i -w <pg_restore pid>` ile engellendi.
> - **Adım 3 — kanıt (21 Eki 09:35 UTC; canlı `claude_readonly` + read-only):**
>   - Tablo **75 / 75**. Index 130/130 · trigger 2/2 · sequence 39/39 · `pg_proc` 52/52 aynı
>     isimler · extension aynı. (`information_schema.routines` canlı 51 / staging 52: fark
>     `pg_stat_statements_reset` — `claude_readonly` EXECUTE yetkisi olmadığı için göremiyor;
>     nesne farkı değil.)
>   - Satır: **75 tablonun 70'i birebir eşit; staging > canlı hiçbir tabloda YOK (ANORMAL 0).**
>     Fark yalnız 5 tabloda, hepsi export'tan sonra canlıya eklenen satır: `email_events` +673 ·
>     `email_unsubscribes` +23 · `email_logs` +14 · `email_queue` +14 · `visitors` +2.
>   - Kesim filtresi (canlıda `< 2026-10-19 15:00 UTC`): `created_at`/`updated_at` kolonlu
>     **48 tablonun 48'i staging ile eşit** (farklı beş tablonun dördü dahil); `email_logs`'ta bu kolonlar yok,
>     `sent_at` ile 733.754 = 733.754.
>   - İstenen tablolar (canlı / staging): `users` 1/1 · `expos` 23/23 · `contracts` 3/3 ·
>     `contract_line_items` 2/2 · `payments` 15/15 · `commission_payouts` 8/8. `line_items`,
>     `payouts`, `commissions` adıyla tablo BULAMADIM (karşılıkları yukarıdakiler).
>   - En büyük 10 (canlı bayt; canlı / staging satır): `email_queue` 570.825/570.811 ·
>     `campaign_recipients` 250.963/250.963 · `email_events` 749.592/748.919 · `email_logs`
>     733.768/733.754 · `reactivation_tokens` 207.994/207.994 · `visitors` 112.834/112.832 ·
>     `callcenter_leads` 41.396/41.396 · `visitor_event_status` 51.207/51.207 · `visitors_backup`
>     22.542/22.542 · `email_campaigns` 30/30. Toplam boyut canlı 4,09 GB / staging 3,65 GB
>     (restore şişkinliksiz yazar; satır farkı değil).
>   - **TABAN contract 4 sr earned: canlı 342.00 (7 dilim) = staging 342.00 (7 dilim).** Sorgu
>     koddaki `utils/commissionSlices.js` SLICE_CTES metninden üretildi (ikinci formül yok).
>   - `schema_migrations` son kayıt iki tarafta **`028_agent_office`** (2026-07-28 13:33:03 UTC),
>     30/30 kayıt. (029–032'nin canlı kaydı yok — bilinen açık, 8 Eki kuyruğu.)
> - **Hüküm:** LEENA export'u staging'e eksiksiz geri yüklenebiliyor → **geri dönüş iddiası
>   kanıtlanmış restore'a dayanıyor** (YON-11). Faz A rotasyon adımları (A1+) bu kanıtla açılabilir.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** staging planı (panel) · dump'ın kesin anı (pencere ölçüldü,
>   an değil) · satır İÇERİĞİ eşitliği (yalnız sayı; checksum yok) · LIFFY ve eliza-db export'larının
>   restore'u (kapsam dışı) · staging'e uygulama bağlayıp çalıştırma · zaman kolonsuz 26 tablonun
>   kesim filtreli sayımı (bunlar zaten tam sayıda eşit).
> - **Bilinçle yapılmayanlar:** canlıda yazma · credential rotasyonu · staging web servisi ·
>   dilim 2 dalı · LIFFY/eliza restore. Açılmış geçici arşiv klasörü silindi.
> - **Kütük:** YON-11 eklendi (Sentez madde 8). **Commit:** ell-docs defter + kütük. PUSH YOK.

> ## ✅ 2026-10-21 — FAZ A TAMAMLANDI
>
> - **Panel tarafı (Suer, 21 Eki):** LEENA DB giriş kullanıcısı `leena_app_2026` (eski
>   `leena_v401_db_user` girişi kaldırıldı) · LIFFY `liffy_app_2026` (`liffy_user` ve
>   `liffy_user_v2` girişleri kaldırıldı) · `claude_readonly` şifresi yenilendi · LEENA `JWT_SECRET`
>   yenilendi. Suer kanıtları: `pg_stat_activity` yalnız `leena_app_2026`; ui2 contract 4 → €342.00
>   eski kullanıcı kaldırıldıktan sonra da açık; liffy.app açık, `liffy_app_2026` 2 bağlantı. A4 yok.
>   Geri dönüş dayanağı: A0 restore kanıtı (YON-11).
> - **A6 — yerel değerler (CC; değer YOK):**
>   - Ölçüm (adlar, `git ls-files`): LEENA `backend/leena-v401-backend/.env` (izlenmiyor, ignore'lu;
>     `PGUSER PGHOST PGDATABASE PGPASSWORD PGPORT JWT_SECRET SENDGRID_API_KEY SENDER_EMAIL BASE_URL
>     RENDER_DATABASE_READONLY_URL`) · LEENA `frontend/leena-v401-clean/.env` (izlenmiyor; aynı adlar,
>     READONLY_URL yok) · LEENA `.claude/settings.local.json` (izlenmiyor; bağlantılar izin
>     kuralı: 4 `claude_readonly` + 1 `leena_v401_db_user`) · LIFFY `.claude/settings.local.json`
>     (izlenmiyor; 31 `liffy_user` izin kuralı).
>   - ⚠️ **Varsayım ÇÜRÜDÜ:** iki `.env`'deki `PG*` canlıyı değil **yerel geliştirme DB'sini**
>     gösteriyor (`postgres@localhost/leena_v401`); `DATABASE_URL` satırı yok. Suer kararı:
>     `PG*` ve `JWT_SECRET` yerelde DEĞİŞMEDİ (canlı DB şifresi ve canlı JWT sırrı Mac'e yazılmadı);
>     `settings.local.json` izin kurallarına DOKUNULMADI (eski şifreler geçersiz).
>   - Yazılan tek yerel satır: `backend/leena-v401-backend/.env:10` `RENDER_DATABASE_READONLY_URL`
>     (izlenmeyen dosya; satır sayısı değişmedi). İzlenen dosyaya sır yazılmadı.
> - **⚠️ `claude_readonly` şifresi 21 Eki'de İKİ KEZ yenilendi; ilk değer sohbete düştü.** Suer
>   kararıyla CC, sohbetteki değerle bir defalık bağlanıp `ALTER ROLE claude_readonly PASSWORD`
>   ile yeni değeri atadı (48 hex, `secrets.token_hex(24)`; SCRAM-SHA-256 doğrulayıcı olarak
>   gönderildi — düz şifre sorgu metnine / `pg_stat_statements`'a girmedi). Yeni değer `.env:10`'da
>   ve repo dışı 600 izinli yerel dosyada.
> - **⚠️ CC ölçüm hatası (A6 Adım 1):** LIFFY `settings.local.json` taramasında maskeleme kalıbı
>   eksikti → CC oturum çıktısına `ANTHROPIC_API_KEY`'in büyük kısmı, LIFFY `JWT_SECRET` başı ve
>   bir JWT token başı düştü (dosya satırları 45–60, 158, 176, 182). Değerler hiçbir dosyaya
>   yazılmadı. **Anthropic API anahtarı iptal/yenilenmeli (Suer)**; LIFFY JWT Faz B'de zaten yenileniyor.
>   **Ders:** sır dosyası taramasında değer değil yalnız ad + satır no basılır.
> - **Adım 3 — doğrulama (CC, 21 Eki):**
>   - LEENA `claude_readonly` yeni şifreyle: `current_user = claude_readonly`, read-only `on`.
>     Sohbetteki (ilk) değer: **REDDEDİLDİ** ("password authentication failed"; rastgele yanlış
>     şifreyle aynı mesaj). Panel öncesi değer de REDDEDİLDİ.
>   - LIFFY `liffy_app_2026`: `session_user = liffy_app_2026`, **`current_user = liffy_user`** —
>     rolde `role=liffy_user` ayarı var. `liffy_user` rolü DURUYOR ama `rolcanlogin = f`; `liffy_user_v2` yok.
>   - Eski LEENA kimliği (`leena_v401_db_user`, `settings.local.json:70`): **REDDEDİLDİ** — "role
>     is not permitted to log in".
>   - `pg_roles`: `leena_v401_db_user` **VAR, NOLOGIN**; `leena_app_2026` onun üyesi ve
>     `role=leena_v401_db_user` ayarlı → uygulama oturumu eski rolün kimliğiyle çalışır.
>     **75 tablonun 75'inin `tableowner`'ı `leena_v401_db_user`.** (`leena_v401_db_user`
>     `claude_readonly`'nin üyesi — önceden kalma; raporlandı, dokunulmadı.)
>   - `pg_stat_activity` (LEENA): `leena_app_2026` 1 + `claude_readonly` 1 (CC).
>   - `git status --porcelain`: LEENA ve LIFFY Adım 1 kaydıyla **birebir aynı**.
> - **Faz B notları:** staging DB inbound `0.0.0.0/0` → daraltılmalı · 3 izlenen `.env.backup` ·
>   LIFFY `JWT_SECRET` (K-E) · iki `settings.local.json`'daki ölü sırlı izin kuralları temizliği
>   (Anthropic anahtarı dahil) · "silinen" rollerin NOLOGIN olarak durması bilinçli mi (sahiplik
>   için gerekli görünüyor) — Sentez.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** Render Shell'deki `psql`'in eski kullanıcıyla girip girmediği ·
>   canlı LEENA `JWT_SECRET` yenilemesinin eski token'ları reddettiği (CC denemedi) · LIFFY'de
>   eski `liffy_user` şifresiyle bağlantı denemesi (rol NOLOGIN, giriş zaten kapalı) · Render paneli.
> - **Commit:** ell-docs defter. PUSH YOK.

> ## ✅ 2026-10-21 — DİLİM 2: MERGE HAZIR
>
> - **Uygulanan hükümler:** B7 · B9 · B10 (033 TRUNCATE) · B32 (`display_name` adı) · SEM-03 ·
>   SEM-04 · SEM-05 (JWT `user_id`+`name`, `ui2CurrentUser` senkron) · MOT-01 (TABAN) · K-A · K-B ·
>   K-D (034) · K-F (035) · K-G · 033 şartı (029–032 kaydı yalnız şema iziyle) · YON-01 · YON-05 ·
>   YON-06 · YON-07 · YON-09 · YON-10 · YON-11. LED-01..09 bu pakete DEĞMEZ (ledger kapsam dışı).
>   Kapılar (YON-11): merge = deploy → KAPI-1 (Suer); 033/034 trigger + 035 kolon + auth →
>   KAPI-2, kararları mevcut (033 şartı, K-D, K-F, K-A/SEM-05).
> - **Ölçüm 1a:** yerel `main` `ae3cd4f` · `origin/main` `08f76cb` · `faz4-dilim2` `a67ab0f`
>   (origin'de yok). Çalışma kopyası 1 M (`.DS_Store`) + 22 izlenmeyen (önceki ile aynı).
>   `om19` worktree (başka oturum, `08f76cb`) HÂLÂ VAR — dokunulmadı.
> - **Ölçüm 1b — 029–032 canlıda:** dördü de **UYGULANMIŞ-KAYITSIZ** (kısmi/uygulanmamış YOK → DUR
>   tetiklenmedi). İz: 029 `email_campaigns.delivered_count` + yorum · 030 `callcenter_leads`
>   (21 kolon) + 4 index · 031 iki `email_queue` index'i `indisvalid = true` · 032 `users` +
>   `trg_min_one_active_owner` + fonksiyon + `sales_agents.user_id` uuid + FK + Owner satırı
>   (hash NULL, must_change true). `schema_migrations` 30 kayıt, son `028_agent_office`;
>   `version` PK, `applied_at` nullable → 033'ün geriye dönük kayıtları yazılabilir. 033/034 izi yok.
> - **Ölçüm 1c:** dalda 033 + 034 vardı, ikisi idempotent (DROP…IF EXISTS / CREATE OR REPLACE /
>   ON CONFLICT DO NOTHING), BEGIN/COMMIT içermiyor. K-F ad kolonu dosyası **YOKTU → yazıldı (035)**.
> - **Ölçüm 1d:** dal kodu 033/034'e bağlı DEĞİL (yalnız trigger + kayıt). 035 kolonu kod
>   `to_jsonb(u)->>'display_name'` ile okur → kolon yokken login + `/me` çalışır, ad = e-posta
>   (test N4). → **Sıra: push/deploy ÖNCE, migration'lar SONRA tek tek** (Shell'de dosyalar da
>   ancak deploy sonrası var).
> - **İnşa (dal):** `origin/main` (Kenya sertifikası) dala merge (`171feb6`, çakışma yok) ·
>   `931e709`: `035_users_display_name.sql` (nullable `display_name` + boş-metin CHECK,
>   idempotent) · `userAuth.js` token/yanıt `name` = ad || e-posta, `/me` `name` + `display_name` ·
>   ilk-şifre script'i: salt-okunur ön kontrol "evet"ten ÖNCE (hash dolu / Owner yok / belirsiz /
>   035 yok → soru sormadan çıkar; kilitli kontrol yazımda aynen), Owner adı sorulur (boş = NULL),
>   hedef satırı `session_user` + `current_user` · ui2: login kayda ad yazar, `ui2CurrentUser()`
>   adı döner (adsız eski kayıt → e-posta, K-G), whoami "Name" satırı.
> - **Testler (yerel test DB):** 169 → **181/181**, iki koşu + `main` üzerinde üçüncü koşu aynı
>   (finans 120 · users 39 · line-item 11 · ui2-current-user 11). Yeni: S0/S2b ön kontrol · N1 ad
>   yok → e-posta · N2 ad yazımı + token + `/me` · N3a/b boş ad NULL / CHECK reddi · N4/N4b kolon
>   yokken login · N5 035 iki kez koşum · C9–C11. **TABAN T35 342.00 KAYMADI.**
> - **ui2 yerel deneme:** test DB + Chrome (headless, Playwright): `ui2/login.html` → `whoami.html`;
>   Name "Suer Ay" · Owner · Session User · must change No; `ui2CurrentUser()` = {name, id, email,
>   session:'user'}; sayfa hatası 0. Yerel koşum için repo dışı sarmalayıcı: SSL'siz test pool'u +
>   CORS yerelde açık (`index.js` izin listesi yalnız leena.app) — kod değişmedi.
> - **main:** `ae3cd4f` → **`931e709`** (fast-forward; origin/main'in 5 önünde). COMMIT VAR, PUSH YOK.
> - **Suer bloğu:** push (YON-06 ön kontrolü) → deploy doğrulama (login.html 200, API 401) →
>   Shell kimlik + dosya kontrolü → 033/034/035 her biri dry-run (`BEGIN … ROLLBACK`) sonra gerçek
>   (`-1`) → `schema_migrations` 029–035 (7 satır) → ilk-şifre script'i → leena.app/ui2 görsel onay
>   (+ contract 4 €342.00, klasik login). Her adımda DUR koşulu ve geri dönüş satırı teslim metninde.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** Render Shell'in çalışma dizini ve `psql`'in Faz A sonrası
>   kullanıcısı (blokta 2.0/2.0b kontrolü) · ilk-şifre CLI'sinin uçtan uca koşumu (yerel Postgres
>   SSL'siz, script SSL zorunlu; mantık birim testli) · canlıda deploy/migration · canlı tarayıcı
>   akışı · klasik `/login.html` ile yeni kodun canlıda yan yana çalışması (yerel testte L7 kapsar).
> - **Commit:** LEENA `main` `931e709` (yerel) · ell-docs defter. PUSH YOK (ikisi de).

> ## ✅ 2026-10-21 — DİLİM 2 CANLIDA (KAPI-1 geçti)
>
> - **Suer koşumu (21 Eki):** `git push` `08f76cb..931e709` → web + worker **Live**;
>   `ui2/login.html` 200. Render Shell: `session_user = leena_app_2026`, `current_user =
>   leena_v401_db_user`. 033 / 034 / 035 her biri dry-run + gerçek, **hatasız**. İlk-şifre script'i:
>   "Owner password set; password_must_change = false" (ad girildi). **Görsel onay (Suer):**
>   ui2/whoami Name / Owner / Yes / User / No; ui2 contract 4 → €342.00 migration'lardan sonra da aynı.
> - **CC salt-okunur teyit (21 Eki, `claude_readonly`):** `schema_migrations` 029–035 = 7 satır
>   (029–032 `applied_at` NULL — 033 geriye dönük kaydı, şema iziyle; 033 11:17 · 034 11:18 ·
>   035 11:19 UTC), toplam 37 · trigger'lar `trg_min_one_active_owner` + `_truncate` +
>   `trg_contract_line_items_immutable` · `users_display_name_not_blank` VAR · Owner: aktif,
>   hash dolu, must_change false, `display_name` dolu · **TABAN contract 4 sr earned 342.00
>   (7 dilim)** · `origin/main` = `931e709` · `leena.app/ui2/login.html` 200.
> - **Takvim (SEM-05):** token süresi 30 gün → eski `/login.html` yolu en erken **2026-11-20**'de
>   emekli edilebilir (karar ayrı; otomatik değil).
> - **⚠️ ÖLÇÜLMEDİ:** klasik `/login.html` girişinin dilim 2 sonrası canlıda denenmesi (Suer
>   raporunda yok) · worker loglarında hata taraması · eski token'ların JWT_SECRET rotasyonu
>   sonrası reddi.
> - **Kapanış (YON-03):** push → KB yeniden yükleme → `KB @ <hash>` satırı Suer teyidiyle girer;
>   o satıra kadar paket belge tarafında AÇIK.

> ## ✅ 2026-10-21 — STAGING HAZIRLIK
>
> - **Karar (Sentez 9 + 7b, Suer):** Render'da ikinci LEENA web servisi `leena-staging`, dal
>   `eliza-next`'ten auto-deploy, env'i `leena-staging-db`'ye bakar. Koda "staging ise" dalı YOK;
>   fark yalnız env. **Maliyet onaylandı:** web $7/ay + DB $8,70/ay. Worker servisi YOK (staging'de
>   kuyruk/kampanya gönderimi olmaz).
> - **Dal:** `eliza-next` = `main` `931e709` + `fab377d`. Yalnız yerel; push Suer
>   (`git push -u origin eliza-next`). Kütükte "staging" geçen hüküm YOK.
> - **Ölçüm — env (çalışan kod; dosya:satır):**
>   - Boot'ta ÇÖKEN: yalnız `UNSUBSCRIBE_SECRET` (`routes/emailTracking.js:20-22`, exit 1).
>   - Çökmez ama işlevsiz: `PG*` (`utils/db.js:6-10`, yoksa localhost → her sorgu hata) ·
>     `JWT_SECRET` (login 500 `routes/userAuth.js:65`, korumalı uçlar 403 `authMiddleware.js:13`).
>   - Opsiyonel, yoksa: SendGrid üçlüsü → gönderim atlanır, `sendEmail` **true döner**
>     (`utils/email.js:34-37`; çağıran "gönderildi" sanır — davranış bilgisi, değiştirilmedi) ·
>     `CALLCENTER_KEY`/`_SUPERVISOR_KEY` → 503 fail-closed (`middleware/callCenter*Auth.js:17`) ·
>     `CALLCENTER_AGENTS`/`_REPORT_TO` → boş liste · `BASE_BADGE_URL` → **`https://leena.app`
>     yedeği** (19 yer; staging linkleri canlıyı gösterir) · ⚠️ `ZOHO_WEBHOOK_TOKEN` → **koda gömülü
>     yedek token** (`routes/webhook.js:8`; repo public → Faz B) · `NODE_ENV` yalnız log/stack.
>     Worker değişkenleri yalnız `email_worker.js` (ayrı süreç; staging'de yok). Terminal: env yok
>     (DB anahtarı). Twilio/Anthropic: LEENA backend okumuyor. Frontend API'yi göreli yolla çağırır
>     (mutlak leena.app yalnız `register.backup.html`) → staging UI canlıya gitmez.
>   - ⚠️ **Varsayım ÇÜRÜDÜ (YON-05):** "fark yalnız env" bugünkü kodla mümkün değildi — CORS izin
>     listesi koda gömülü (`index.js:21`, yalnız leena.app); tarayıcı aynı-origin POST'ta da `Origin`
>     gönderir → staging'de login 500 "CORS not allowed" (21 Eki yerel denemede gözlendi).
> - **Kod (`fab377d`, eliza-next; canlıya `main` merge'üyle aynen gider):**
>   `utils/bootGuards.js` + `index.js`: (1) **DB-adı koruması** — boot'ta `current_database`
>   loglanır; `EXPECTED_DB_NAME` varsa doğrulanmadan dinlenmez, eşleşmezse/okunamazsa exit 1.
>   (2) **`CORS_EXTRA_ORIGINS`** — izin listesine env'den tam origin ekler. İki değişken de canlı env'de
>   YOK → canlı davranış aynı (yalnız ad logu). KAPI-2 (boot): (1) Sentez kararı; (2) ölçüm sonucu
>   eklendi → **Sentez teyidi istenir**.
> - **Testler:** 181 → **197/197**, iki koşu aynı. Yeni `test_boot_guards.js` (16): birim G1–G7 +
>   index.js GERÇEK süreçte anahtarsız env'le (B1 yanlış DB → exit 1, hiç dinlemedi · B2 doğru DB →
>   dinler · B3 login.html 200 · B4 ek origin'den POST geçer · B4b Owner login 200 + `/me` 200 ·
>   B5 callcenter 503 · B6 SendGrid yok → gönderim atlanır · B7/B8 canlı şekli: dinler, yabancı
>   origin hâlâ reddedilir). **TABAN T35 342.00 KAYMADI.**
> - **Staging DB durumu (CC, salt SELECT):** son migration `028_agent_office` (30), Owner hash
>   NULL, 033/034/035 YOK (19 Eki kopyası, dilim 2 öncesi) → staging'de login için Shell'de
>   033/034/035 + ilk-şifre script'i gerekir (panel bloğunda).
> - **Suer panel bloğu:** teslim metninde (form alanları · env listesi kaynaklarıyla · doğrulama).
>   URL deftere YAZILMAZ.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** canlı servisin build/start komutları ve Node sürümü (repoda
>   yok — panelden kopyalanacak) · canlı env'de `NODE_ENV` değeri · Render'da staging deploy'u ·
>   register akışı (test DB'de `organizers.name` yok, YON-09) · webhook ucu anahtarsız.
> - **Commit:** LEENA `eliza-next` `fab377d` (yerel) · ell-docs defter. PUSH YOK.

> **Meta not (2026-10-21, defter kaydı değil):** LEENA `CLAUDE.md` 217,581 → 84,841 karakter (Claude Code dosya başı eşiği 150k) — versiyon geçmişi + 4 "✅ FIXED" bloğu `docs/CLAUDE_ARCHIVE.md`'ye AYNEN taşındı; kural metinleri yerinde, değişmedi · LEENA `eliza-next` `ee13814` · PUSH YOK.

> ## ✅ 2026-10-21 — STAGING CANLI
>
> - **Ne:** Render'da `leena-staging` web servisi açıldı (Suer, panel): **leena-staging.onrender.com**, dal
>   `eliza-next` auto-deploy, DB `leena-staging-db`. Staging DB'de 033–035 uygulandı + Owner şifresi
>   verildi (Suer, Shell). Env'de `CORS_EXTRA_ORIGINS` · `EXPECTED_DB_NAME` · `BASE_BADGE_URL` (Suer
>   beyanı; değerler deftere YAZILMAZ). Worker servisi yok (karar 21 Eki).
> - **Ölçülenler (CC, 21 Eki; staging salt-okunur oturum, `default_transaction_read_only=on`):**
>   - curl: `/login.html` 200 · `/ui2/login.html` 200 · `/health` 200.
>   - `schema_migrations` **37** kayıt, son `035_users_display_name`; 033/034/035 `applied_at` 12:22:32 UTC
>     (üçü aynı saniye). Trigger'lar `trg_min_one_active_owner` + `_truncate` + `trg_contract_line_items_immutable` VAR.
>   - Owner: aktif 1 · hash dolu · `password_must_change = false` · `display_name` dolu (değer basılmadı).
>   - **CORS_EXTRA_ORIGINS etkili:** staging origin'iyle `POST /api/user-auth/login` (sahte e-posta) → **401**
>     (CORS geçti, kimlik reddi); yabancı origin → **500 "CORS not allowed"** (canlı davranışı korunuyor).
>   - Sunucu: PostgreSQL **17.11** (canlı **17.9** — iki ortam aynı majör, farklı minör).
>   - TABAN contract 4 sr earned **342.00** (7 dilim) — SLICE_CTES'ten.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** `EXPECTED_DB_NAME`'in boot logundaki etkisi ve `BASE_BADGE_URL`'in link
>   üretimindeki etkisi (Render logu / e-posta yok) · staging'de gerçek tarayıcı oturumu · Render paneli.
> - **Bilinçle yapılmayanlar:** staging DB'ye yazma · env değerlerini okuma/yazma.
> - **Commit:** ell-docs defter. PUSH YOK.

> ## ✅ 2026-10-21 — PAKET 1: STAGING'E HAZIR
>
> - **Ne yapıldı (dal `eliza-next`, tek merge / tek revert):** ledger L-1…L-6 + migration runner.
>   - **Ön iş (ayrı commit `37d6f9a`):** `docs/CLAUDE_ARCHIVE.md`'den 4 kural notu (Two-phase migration ·
>     42703 fallback · EXPLAIN before optimizing · Attribution honesty) CLAUDE.md "Versiyon Geçmişinden
>     Ayrılıp Burada Kalanlar"a AYNEN taşındı; arşivde `↪` işaret satırı (ee13814 deseni). Metin
>     karşılaştırması: 4/4 birebir, arşivde kalan 0.
>   - **P1-0 runner** `scripts/migrate.js`: kayıtsız dosyaları TEK transaction'da uygular + kaydeder;
>     `--dry-run` = uygula + ROLLBACK + liste; yalnız PG* env (URL argümanı reddedilir); `EXPECTED_DB_NAME`
>     varsa uyuşmazlıkta DUR; DUR koşulları LED-16. `*_rollback.sql` atlanır (013 notu).
>   - **Migration'lar (yazıldı, ÇALIŞTIRILMADI):** 036 hesaplar + para birimleri + gider kategori/tip + gelir
>     kategorisi · 037 tohum (ayrı dosya) · 038 `payments.account_id` + `payer` (KAPI-2) · 039 transfers +
>     expenses + ledger_entries + `ledger_lines` view + değişmezlik/iki-bacak/tutarlılık trigger'ları ·
>     040 expo bütçesi. Hepsi `ell.migration_runner` korumalı, kendi kaydını yazmaz.
>   - **API** `/api/ledger/*` (para birimi, referans, hesap, ekstre, transfer, gider, bütçe, özet) ·
>     ödeme/payout/ters kayıt/kontrat devri ledger'a bağlandı (`utils/ledger.js` tek kural) · migration
>     ÖNCESİ şemada kod eski davranışla çalışır (ledger uçları 503, para birimi listesi eski 6'ya düşer).
>   - **Ekran (iskelet):** ui2 Summary · Accounts · hesap ekstresi · Transfers · Expenses · Expo budget
>     (subnav'a 5 öğe) · klasik `contract-detail.html` ödeme formuna Account + Payer + Account kolonu ·
>     `agent-statement.html` payout formuna Account · sabit para birimi listeleri (3 kopya) tablodan okur.
> - **Commit:** LEENA `eliza-next` `37d6f9a` (ön iş) + **`c15ac1f`** (paket). PUSH YOK.
> - **Kütük taraması (pakete değen):** LED-01…09 · D2 · SEM-01/02/05 · TAH-01/03/04 · ODE-01/03 · MOT-01 ·
>   PLN-05 · OFS-01 (S-16r)/03/05 · RAP-01/02/03 · YON-01/05/06/07/09/11 · B9 · B10 · B25 · AD-01.
>   **Yeni:** LED-10…LED-17 (🔶 olanlar Sentez teyidinde).
> - **Ölçülenler:**
>   - **ADIM 0 (canlı `claude_readonly` + staging salt-okunur):** şema kataloğu iki tarafta 1.328 satır; fark
>     YALNIZ 7 satırda ve hepsi aynı ifadenin farklı yazımı (varchar ARRAY cast deparse: 6 CHECK —
>     callcenter_leads ×3, expo_partners ×1, expos ×2 — + `idx_callcenter_leads_pool` yüklemi) → anlamsal
>     fark 0. `schema_migrations` iki tarafta 37 = 37 dosya (kayıtlı-dosyasız 0, kayıtsız dosya 0). 029–035
>     iki tarafta kayıtlı. Ledger tablosu iki tarafta 0. `payments` 14 kolon / 15 satır (6 ters) ·
>     `commission_payouts` 14 kolon / 8 satır (3 ters) · contracts 3 · offices 6 (TEST OFFICE pasif) ·
>     organizers 2 (org 2: 1 expo, finans 0) · users 1. Kullanılan para birimleri: ödeme EUR/TRY/USD ·
>     payout EUR/MAD · kontrat EUR/USD (hepsi REQ'nin 8'i içinde).
>   - Dilim 2 ÖLÇÜLMEDİ üçlüsü: klasik `leena.app/login.html` **200** (+ `/ui2/login.html` 200, `/health` 200) ·
>     **eski JWT:** yerel/test sırrıyla imzalı token canlıda ve staging'de **403** (contracts + `/me`), token'sız 401 ·
>     **worker logları: ÖLÇÜLEMEDİ** — Render CLI kurulu ama oturum belirteci **2026-06-17'de süresi dolmuş**
>     (`render login` etkileşimli, Suer).
>   - **Testler:** taban **197/197** (CLAUDE.md "67/67" bayattı — YON-05) → **269/269** (+ledger 43 ·
>     premig 7 · runner 16 · ui2 pages 6). PG 14.18'de 3 koşu + PG **17.10** geçici kümede 2 koşu, hepsi aynı.
>     **TABAN 342.00 KAYMADI** (T35 + ledger üzerinden ödemeyle I5).
>   - **Prova (CC, yerel PG17, staging şeması):** staging'den `pg_dump --schema-only` + finans tabloları
>     (salt-okunur; organizers/users SENTETİK — kişisel veri alınmadı) → gerçek CLI: `--dry-run` "DRY-RUN OK:
>     5" · uygula "COMMIT: 5" · tekrar "Nothing to apply". NOTICE: `037: organizer 1 → currencies +8 (REQ)
>     +0 (in use) · expense categories +6 · expense types +4 · income categories +4` · `038: payments 15 rows`.
>     Uygulama sonrası app: eski form gövdesi hesap/varsayılan yokken **201 + uyarı**, varsayılan hesapla 201 +
>     hareket · TABAN 342.00 (SQL + API) · özet komisyonu = 152 agent ekstresinin toplamı (ödenecek 0.00 ·
>     bize borçlu 1 agent 48.00) · ledger dışı 16 ödeme (15 + prova) / 8 payout. Prova DB'si silindi.
>   - **Tarayıcı (Playwright, yerel test DB):** ui2 login (Owner) → 6 ekran + klasik ödeme formu; sayfa hatası 0;
>     konsoldaki 5 adet 500'ün HEPSİ `/api/expos` (test DB'deki `expos` stub'ında `country_code` yok — EMS
>     route'u, YON-09); ledger sayfaları boş expo listesine düşer. Owner kilidi UI'dan atıldı; klasik formda
>     kasa hesabı seçilip ödeme girildi → `account_id` + 'in' hareketi.
> - **YON-05 (çürüyen varsayımlar):** (1) CLAUDE.md test beklentisi 67/67 değil 197 idi (düzeltildi → 269).
>   (2) "Her migration kendi kaydını yazar" — 010/011/012/016/029–032 YAZMAZ; canlıda 016 yine kayıtlı (elle),
>   test DB'sinde kayıtsız → test DB kaydı canlıdan farklıdır; runner testi canlı şeklini (37) kurar.
>   (3) leena-fetch 401 **ve 403**'te oturumu siler → yetki reddi 403 olamaz (Owner reddi 409, LED-15).
>   (4) Test sunucusu PG 14.18, canlı 17.9 / staging 17.11 → suite PG17'de de koşuldu.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** migration'ların staging/canlı DB'de koşumu (Suer) · staging deploy'u ve
>   staging tarayıcı oturumu · worker logları · eski (rotasyon öncesi) canlı JWT sırrıyla imzalı token'ın reddi
>   (o sır CC'de yok; ölçülen: yabancı sırla imzalı token reddi) · `EXPECTED_DB_NAME`/`BASE_BADGE_URL` etkisi ·
>   `/api/expos`'un canlıda ledger açılır listeleri için maliyeti · gerçek Zoho referans listesinin tamamı.
> - **Bilinçle yapılmayanlar:** push / merge · canlı ve staging DB'ye yazma · migration koşumu · ledger öncesi
>   satırlara geriye dönük hareket · `payments.currency`'ye FK/doğrulama (davranış değişikliği) ·
>   `commission_payouts`'a hesap kolonu (hesap hareket satırında) · gelir kategorisinin ödemeye bağlanması ·
>   iade (`refund`) akışı (tür CHECK'te var, yazan uç yok) · rol/yetki gate (Faz 4) · cila / tasarım.
> - **🔶 Sentez'e açık sorular:** LED-10…17 teyidi · gelir kategorisi nereye bağlanır (LED-04: ayrı gelir
>   tablosu yok) · iade + kredi bakiyesi dilimi · yeni ödemede para birimi tablo doğrulaması · kontrat
>   devrinin ekstrede net-sıfır iki satır görünmesi kabul mü · `PRE_MIGRATION_CURRENCIES` yedeğinin
>   kaldırılma anı (040 canlıda uygulanınca).
> - **Teslim (Suer):** push → staging Shell `node scripts/migrate.js --dry-run` → `node scripts/migrate.js` →
>   6 ekran görsel onayı → "merge" → canlı sırası (export → push main → canlı Shell dry-run → migrate → ui2
>   contract 4 €342.00 + özet). Ayrıntı teslim metninde.

> ## ✅ 2026-10-21 — PAKET 1: MAIN'E MERGE (canlı sırası Suer'de)
>
> - **Ne yapıldı:** Suer "merge" dedi → yerel `main`'e `git merge --no-ff eliza-next` → **`35cad76`**
>   (ebeveynler `931e709` = origin/main · `c15ac1f`). Gelenler: `fab377d` (boot korumaları, yalnız env) ·
>   `ee13814` + `37d6f9a` (CLAUDE.md bölme / 4 kural notu) · `c15ac1f` (ledger 036–040 + runner + API + ekranlar).
>   **Tek revert:** `git revert -m 1 35cad76`. Merge ağacı = `c15ac1f` ağacı (birebir, `rev-parse ^{tree}`).
> - **Commit:** LEENA `main` **`35cad76`** (yerel; origin/main'in 5 önünde). **PUSH YOK.**
> - **Ölçülenler (CC, bu tur; DB'ler salt-okunur):**
>   - `origin/eliza-next` = `c15ac1f` (push reflog 2026-10-21 16:56 +0300) · `origin/main` = `931e709`.
>   - **Staging:** `schema_migrations` **42**, son `040_expo_budgets`; 036–040 `applied_at` hepsi
>     **14:02:12.42 UTC** (tek transaction) · `ledger_entries` / `accounts` / `expo_budgets` VAR ·
>     `payments.account_id` + `payer` VAR. Tohum: currencies 8 · gider kategori 6 · gider tipi 4 · gelir
>     kategorisi 4 (= provadaki NOTICE). Suer'in deneme izi: 1 hesap (EUR banka, ofis 1 varsayılanı,
>     14:13 UTC) · 1 gider + 1 'out' hareketi (14:25 UTC) · transfer 0 · bütçe 0 · hesaplı ödeme 0.
>     `ui2/finance-summary.html` **200**, `/api/ledger/summary` token'sız **401** (route bağlı).
>   - **Canlı:** `schema_migrations` **37**, son `035_users_display_name`; ledger tablosu YOK, `payments`'ta
>     yeni kolon YOK (beklenen) · `leena.app/ui2/finance-summary.html` **404** (beklenen: push öncesi) ·
>     `/health` 200.
>   - **TABAN contract 4 sr earned = 342.00 (7 dilim)** staging (migration SONRASI) ve canlıda, SLICE_CTES ile.
>   - **Testler `main` üzerinde:** **269/269**, ❌ 0 (tek koşu; T35 + M01a + I5 342.00).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** Suer'in staging görsel onay raporu (yalnız "merge" geldi) — DB izi
>   yalnız Accounts + Expenses ekranlarının kullanıldığını gösteriyor; Summary / ekstre / Transfers / Budget /
>   klasik formun Account alanı açıldı mı bilinmiyor · canlı env'de `EXPECTED_DB_NAME` / `CORS_EXTRA_ORIGINS`
>   yokluğu bu tur yeniden ölçülmedi (21 Eki STAGING HAZIRLIK ölçümü) · canlı deploy + migration · worker logları.
> - **Bilinçle yapılmayanlar:** push (`main` ve ell-docs) · canlı DB'ye yazma / migration koşumu · staging
>   deneme verisinin (1 hesap, 1 gider) silinmesi — ledger silmeyi reddeder, ters kayıt + pasifleme Suer'in
>   kararı · `eliza-next`'in `main`'e eşitlenmesi (bir sonraki dal işinin ilk adımı: `git merge --ff-only main`).
> - **Teslim (Suer, canlı sırası):** export (Render panel) → YON-06 (status.render.com + takvim) →
>   `git push origin main` → Live (~60 sn, G43; arada eski form çalışır, ledger ekranları "not migrated yet") →
>   canlı Shell `node scripts/migrate.js --dry-run` (DUR: `database` ≠ `leena_v401_db` / "DUR —" / FAILED) →
>   `node scripts/migrate.js` → "COMMIT: 5" → tekrar koşum "Nothing to apply" → ui2 contract 4 €342.00 +
>   `finance-summary.html` açılıyor. Shell açıkken deploy yok (G46).
> - **Kapanış (YON-03):** canlı koşum sonrası CC salt-okunur teyit kaydı (`schema_migrations` 42, TABAN, sayfa 200) ayrı
>   kayıt olarak girer; o kayda kadar Paket 1 AÇIK.

> ## ✅ 2026-10-21 — PAKET 1 CANLIDA (KAPI-1 geçti)
>
> - **Ne yapıldı (Suer, 21 Eki):** `git push origin main` (`931e709..35cad76`, 18:22 +0300) → auto-deploy
>   **tetiklenmedi**, Render **Manual Deploy** ile alındı. Canlı Shell `node scripts/migrate.js --dry-run` +
>   gerçek: **5/5 (036–040)**. **Görsel onay (Suer):** ui2 contract 4 → **€342.00** · `finance-summary.html` açık.
> - **Commit:** LEENA'da yeni commit YOK (`main` = `origin/main` = `35cad76`) · ell-docs bu kayıt.
> - **Ölçülenler (CC salt-okunur teyit, 21 Eki 15:33 UTC, `claude_readonly`):**
>   - `schema_migrations` **42**, son `040_expo_budgets`; 036–040 `applied_at` hepsi **15:29:59.51 UTC**
>     (tek transaction; 035 11:19 UTC).
>   - Ledger nesneleri VAR: `ledger_entries` · `ledger_lines` view · `expo_budget_lines` · 6 tabloda 11 trigger
>     (staging'le aynı sayı) · `payments.account_id` + `payer`.
>   - Tohum: org 1 → para birimi 8 (DZD, EUR, GHS, KES, MAD, NGN, TRY, USD) · gider kategorisi 6 · gider tipi 4 ·
>     gelir kategorisi 4. Org 2 → 0 (aktif Owner yok; LED-17 kuralı).
>   - Veri: hesap **0** · hareket 0 · transfer 0 · gider 0 · bütçe 0 · ödeme 15 (account_id/payer dolu 0) ·
>     payout 8 → hepsi ledger dışı (LED-14).
>   - **TABAN contract 4 sr earned = 342.00 (7 dilim)**, SLICE_CTES ile.
>   - HTTP: `ui2/finance-summary.html` · `finance-accounts.html` · `finance-contract.html` · `/login.html` ·
>     `ui2/login.html` · `/health` **200** · `/api/ledger/summary` ve `/currencies` token'sız **401**.
> - **Açık nokta (ölçülen + kod):** canlıda hesap 0 → bundan sonra girilen her ödeme/payout hesapsız kaydedilir;
>   form "Payment added" + uyarı tostu gösterir (`contract-detail.html:1059`, metin `utils/ledger.js:92`), ledger
>   dışı sayacı büyür. Ofis varsayılan hesapları açılınca yeni ödemeler kendiliğinden ledger'a girer (LED-12);
>   öncekiler geriye dönük girmez (LED-14).
> - **Suer notları (Sentez'e — karar orada):** (1) gider "karşı taraf" düz metin olmamalı → tedarikçi/venue
>   kaydı + ödeme geçmişi ekranı; Paket 1b mi, Paket 3 mü? (2) gider tipleri eksik → Zoho'nun tam listesi gerekli
>   (LED-17: belgede BULAMADIM).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** auto-deploy'un `35cad76` için tetiklenmeme sebebi · export'un push öncesi
>   tamamlandığı (Suer raporunda yok) · dry-run çıktısının metni (Target satırı / NOTICE'ler; rapor "5/5", tohum
>   sayıları DB'den ölçüldü) · worker logları · canlı tarayıcıda Accounts / Transfers / Expenses / Budget /
>   ekstre ekranları ve klasik formun Account alanı · canlı env'de `EXPECTED_DB_NAME` / `CORS_EXTRA_ORIGINS`.
> - **Bilinçle yapılmayanlar:** canlıda hesap açma / veri girişi (Suer) · `PRE_MIGRATION_CURRENCIES` yedeğinin
>   kaldırılması (koşulu oluştu: 040 canlıda; ayrı dilim) · `eliza-next`'in `main`'e eşitlenmesi.
> - **Geri dönüş (YON-11):** `git revert -m 1 35cad76` yalnız kodu geri alır; 036–040 şeması kalır. Restore
>   kanıtlanmadı.
> - **Kapanış (YON-03):** ell-docs push → KB yeniden yükleme (Sentez + Orchestrator) → `KB @ <hash>` satırı Suer
>   teyidiyle girer; o satıra kadar Paket 1 belge tarafında AÇIK.

> ## ✅ 2026-10-21 — TEKNOLOJİ GÜNCELLEME TURU (Sentez + Suer, asistan incelemeli)
>
> - **Ne yapıldı (belge dilimi; kod/DB YOK):** Sentez direktifi "Teknoloji güncelleme turu kapanışı" + Sentez →
>   Orchestrator EK "YZ/SAT Paket 1b ve 2'ye işlendi" uygulandı. **İŞ A:** REQ başına, 2026-10-08 bloğunun altına
>   "Amendment 2026-10-21" AYNEN + §6.4'e satır. **İŞ B:** kütük — yeni gruplar YZ-01..03 ve SAT-01..04, LED-19,
>   çapraz referans notları ODE-02 / LED-04 / YON-05 (AD-01 "Not" deseniyle satır sonuna). **İŞ C:** bu kayıt +
>   ★ SIRADAKİ (Paket 1 KAPALI · Paket 1b = P1b-1..3 · Paket 2 eklemeleri · Paket 3 amendment girdisi ·
>   madde 6'ya rapor modülü + genel arama).
> - **Commit:** ell-docs — İŞ A/B uygulandı, **bu kayıtla aynı tek commit** (REQ + kütük + defter); hash teslim
>   metninde (commit kendi hash'ini taşıyamaz). PUSH YOK (Suer).
> - **HÜKÜMLER (Sentez bölüm 1 — Suer kararları + Sentez; asistan incelemesi işlendi):**
>   - **İLKE**
>     - YZ-01: Çalışma anındaki yapay zeka iş verisi YAZMAZ, yalnız okur; ürettiği her şey insan onayıyla girer;
>       yapay zekasız yapılabilen yapay zekasız yapılır. (Claude Code'un zincir içinde kod/migration yazması bu
>       kuralın DIŞINDADIR — kütüğe bu ayrımla.)
>     - YZ-02: Şirket verisi yapay zekaya yalnız şirket kontrolündeki entegre hesap (API) üzerinden;
>       şifre/anahtar/bağlantı dizesi ASLA; çalışanların kişisel hesaplarına şirket verisi girmez; ajan, isteyen
>       kullanıcının görebildiğinden fazlasını görmez (Faz 4 kapsamı). Sağlayıcının "eğitimde kullanmama" şartı
>       hesap açılışında teyit edilir (ölçülmedi). Suer: D5 = b, 3 şart.
>     - YZ-03: Her yapay zeka yüzeyi (rapor asistanı, WhatsApp botu) mevcut API'lerin istemcisi, ayrı sistem
>       değil (2026-07-21 UI-bağımsız API kararının uzantısı). Bot yazması = onay diyaloğu sonrası deterministik
>       kayıt.
>   - **DÜŞEN (yazılmaz):** Yeni veri bulma motoru/robotu (mevcut LIFFY robotu olduğu gibi kalır, geliştirilmez;
>     verimi ölçülür) · sürükle-bırak "kendi tasarımımız" rapor ekranı (Zoho tarzı rapor modülü KALIR) · anlatı
>     üreten içgörü/sentez modülü (sayısal eşikli uyarılar KALIR) · katalog dizgi motoru (şablon editörü, matbaa
>     PDF üretici, satır içi yorum) ELL içinde · kullanıcı başına bildirim tercih matrisi, sustur/ertele, zorunlu
>     liste, bildirim geçmişi · kayıtlı filtre / paylaşılan görünüm / son açılanlar-sabitlenenler · üç dil
>     varyantı için özel yan yana editör (metinler saklanır).
>   - **KALAN / EKLENEN**
>     - SAT-01 e-posta kuralı (Suer, 16:51): lead / kontak / katılımcı KAYDI e-posta ister. E-postasız bulgular
>       ayrı "ikincil kayıt" tablosunda ("doğrudan e-posta yok" etiketi) durur, kampanyaya giremez, lead/kontak
>       sayılmaz; yanında "e-postalarını bul" aksiyonu (yapay zeka ya da servis, takılabilir); e-posta bulununca
>       insan onayıyla asıl tabloya geçer. Mükerrer eşleme ikincil tabloda ad+şirket+ülke(+LinkedIn URL).
>     - SAT-02 kazanım boru hattı sabit, bulucu değiştirilebilir: istek ekranı → çıktı şablonu → bekleme masası
>       (doğrulama + mükerrer birleştirme + kaynak etiketi) → tek tuş içeri al. Bulucu = mevcut robot / yapay
>       zeka ajanı / e-posta servisi; ELL içinde bulucu yazılmaz; dış araçla sistem entegrasyonu şart değil
>       (içe aktarma yeter).
>     - SAT-03 sahiplik ve havuz tablodan: ayrılan kullanıcı → havuz; N gün iletişimsiz → uyarı → havuz →
>       yeniden dağıtım; info@/web form → ülke→ofis tablosu. Eşik/tablo Owner'da; kod yok. Önkoşul: olay kaydı
>       (kim ne zaman ne gönderdi). N ve tablolar dilim gelince Suer'den.
>     - SAT-04 bölge yasağı tablodan: ofis/kullanıcı → satabileceği ülkeler (yerel ofisli ülkeye HQ satamaz).
>       Hem atama kuralı hem yetki girdisi (Faz 4). Owner değiştirir.
>     - Katalog (Suer: a): şablonlar tasarımcıyla BAŞTAN birkaç adet hazırlanır; her fuarda sistem verisinden
>       dış araçta OTOMATİK üretim; elle sayfa dizme YOK — "Corel açılmaz" vaadi korunur, motor dışarıda.
>       Sistemde kalan: katılımcı formu, onay, son tarih kilidi, eksik sayacı, temiz dışa aktarım (tablo +
>       görseller), web kataloğu, audit. Kabul: bir fuarla pilot; pilot düşerse madde geri gelir.
>     - Raporlama iki katman: sabit ekranlar (Owner 3 günlük görünüm, nakit öngörü, komisyon kesimi, agent
>       ekstresi, bütçe/gerçekleşen, fuar başına alacak) + Zoho tarzı rapor modülü (modül→alan→süzgeç→grupla→
>       sırala→kaydet→Excel); yapay zeka rapor TANIMINI taslak kurar, sistem koşar. Modülün yeri yol haritası 6
>       (Zoho göçü + raporlama). O güne kadar özel sorular salt-okunur bağlantıyla yapay zekaya (bugünkü yol) —
>       GEÇİCİ, kütüğe yazılır.
>     - Genel arama (tek kutu, iki veritabanı) KALIR; rapor modülüyle birlikte (ortak dizin).
>     - WhatsApp botu KALIR, ileri faz: okur + onay diyaloğuyla yazar (örn. gider girişi); eliza-legacy botu o
>       güne kadar okuma aracı. ⚠️ PAKET 1 L-3 KRİTERİ (ŞİMDİ): gider giriş API'si bot-yazılabilir tasarlanır
>       (alanlar eksik/dolu ayrımı, firma eşleme, onay adımı).
>     - Yetki: önce modül + kapsam (kendi/ekibi/ofisi/hepsi), 4–5 profil; alan gizleme yalnız komisyon, sonra.
>     - Cevap e-postası okuma: yapay zeka önerir (isim/şirket/ilgi), insan onaylar — YZ-01'in tek istisnası
>       (serbest metin). Kendi kural seti yazılmaz.
>     - Olay kaydı (B6) önemi arttı: SAT-03, eşikli uyarılar ve Owner aktivite ekranı buna bağlı. Sıra sorusu
>       (Faz 4 kalan mı, ayrı paket mi) kuyruğa.
>     - Girişte süzgeç (doğrulama + mükerrer: e-posta + şirket adı + alan adı) Paket 3 SONRASI, boru hattıyla
>       birlikte (Suer teyidi bekleniyor; Sentez önerisi).
>   - **BELGE HİJYENİ:** REQ §2.3 "commission_adjustment kaydı" → SUPERSEDED (ODE-02 cari hesap) · REQ §2.3
>     "komisyon ödemesi = gider kaydı" → SUPERSEDED (commission_payouts + LED-04) · REQ §5.2: yalnız "LIFFY
>     mining yeter / orantısız maliyet" cümlesi SUPERSEDED; "no system-level integration" KALIR.
> - **EK (Sentez → Orchestrator, 21 Eki):** Paket 1 KAPALI kalır; yeni kriter Paket 1b'ye girer → P1b-3 gider
>   taslağı (★ SIRADAKİ'de AYNEN) + **LED-19** · Paket 2 eklemeleri (★ SIRADAKİ'de). Sentez amendment metnini
>   henüz okumadı; ell-docs push gelince KB çekilir, çelişki çıkarsa ayrı tur.
> - **⚠️ Çelişki notu (Sentez çelişki turuna):** REQ 2.8 "Ledger L-3 expense API is designed bot-writable from
>   day one (**Package 1 criterion**)" · YZ-03 "L-3 gider API'si gün-1 bot-yazılabilir" · bölüm 1 "PAKET 1 L-3
>   KRİTERİ (ŞİMDİ)" ↔ EK "Paket 1 KAPALI kalır; yeni kriter Paket 1b'ye" (P1b-3, LED-19). Metinler AYNEN
>   bırakıldı; ★ SIRADAKİ EK'i izler. İkincil: bölüm 1 / REQ 3.1 "4–5 profil" ↔ EK "5 profil".
> - **YON-05 kaydı:** varsayılan (Sentez) — "yapay zeka mining'in yerini aldı" · ölçülen (Suer) — 261 kişi /
>   5 e-posta · kanıt: Suer ölçümü (ham çıktı bu defterde YOK; CC ölçmedi) → SAT-01/02.
> - **Ölçülenler (CC, bu tur):**
>   - **ID kontrolü:** kütük + defterde `YZ-[0-9]` · `SAT-[0-9]` · `LED-18` · `LED-19` = 0 eşleşme → önerilen
>     ID'ler çakışmasız, AYNEN tahsis. LED-18 tahsis EDİLMEDİ (kütük kuralı: numaralar süreksiz, kovalanmaz).
>   - **P1b-3 tabanı — bugünkü gider ucu (LEENA `35cad76`):**
>     1. `POST /api/ledger/expenses` (`routes/ledger.js:541`) tek transaction'da `expenses` satırı + ledger 'out'
>        hareketi yazar → 201 `{expense, ledger_entry_id}`. Yetki `authMiddleware` (`:128`) — geçerli her token;
>        `created_by` = token'daki `user_id`, eski organizer token'ında NULL (`utils/ledger.js:38-48`).
>     2. Zorunlu: `expense_type_id` (aktif tip + aktif kategori) · `account_id` (aktif hesap) · `expense_date`
>        (YYYY-MM-DD) · `payment_method` (SEM-01'in 5 değeri) · `amount` > 0 · `exchange_rate` > 0, EUR'da = 1
>        (`:543-546`, `:78-88`). Opsiyonel: `currency` (yoksa hesabınki, varsa eşit — LED-11, `:556-560`) ·
>        `expo_id` · `counterparty` · `notes` · `document_url` (http/https). `amount_eur` sunucuda hesaplanır.
>     3. Karşı taraf: `expenses.counterparty text` nullable düz metin (`039_ledger_core.sql:67`), `trimOrNull`
>        ile yazılır (`:580`), listede metin döner (`:603`); tedarikçi tablosu / FK / eşleme YOK.
>     4. Hata biçimi: ilk eksik/yanlış alanda tek mesajlı 400 `{error}` — eksik alan LİSTESİ dönmez, kısmi /
>        taslak kayıt yok (bot için "eksik/dolu ayrımı" yok).
>     5. Onay adımı YOK (LED-08): satır doğduğu an hareket yazılır; UPDATE/DELETE trigger'la reddedilir
>        (`trg_expenses_immutable`, `039:291`); düzeltme yalnız `POST /expenses/:id/reverse` (`:627`). Canlıda
>        gider 0 satır (21 Eki 15:33 UTC ölçümü). P1b-3 bu ucun ÖNÜNE taslak katmanı koyar; "kabul" bu ucu aynı
>        doğrulamayla çağırır (EK metni).
> - **ÖLÇÜLECEK (karar öncesi, bu dilimde değil — Sentez listesi):** Robot: Render'da hangi servis koşuyor
>   (worker.js dahil), çalışıyor mu, günlük doğrulanmış e-posta, aylık maliyet · firma kayıtlarında sektör alanı
>   doluluğu (LIFFY DB) · hangi yapay zeka sağlayıcısı şirket hesabında veritabanı bağlantısı + eğitimde
>   kullanmama veriyor · Zoho'da fiilen kullanılan rapor listesi (ZOHO_USAGE_REFERENCE'tan) — rapor modülünü
>   boyutlar · katalog pilotu.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** yukarıdaki ölçülecek listesi · Suer'in 261 / 5 ölçümünün ham verisi ·
>   P1b-1/P1b-2 metni (Sentez önceki bloğu, Orchestrator'da yok) · P1b-3'ün FK verdiği `suppliers` tablosunun
>   tanımı (Orchestrator'daki hiçbir metinde yok) · Sentez'in amendment metnini okuması (EK'te kendisi söylüyor).
> - **Bilinçle yapılmayanlar:** kod / DB / LIFFY / LEENA'ya dokunma · REQ "Version" satırındaki "(amended
>   2026-10-08 — see top)" ibaresinin güncellenmesi (istenmedi) · çelişkili "Package 1 criterion" ifadelerinin
>   düzeltilmesi (AYNEN kuralı; Sentez turuna) · LED-18 boşluğunun doldurulması · ell-docs'taki önceden değişmiş
>   `leena/CLAUDE.md` + `leena/todo.md` (commit'e girmedi).
> - **KB @ ca2bd5b (Orchestrator + Sentez, Suer teyidi; YON-03).** Bu satır Paket 1 CANLIDA kaydının belge
>   kapanışını da karşılar.

> ## ✅ 2026-10-21 — PAKET 1 BELGE KAPANIŞI (KB @ ca2bd5b) + SENTEZ CEVAPLARI
>
> - **Ne yapıldı:** (1) YON-03 kapanışı: **KB @ ca2bd5b** (Orchestrator + Sentez, Suer teyidi) → teknoloji
>   turu + Paket 1 belge tarafı KAPALI. (2) Kütük: LED-10 / 11 / 12 / 13 / 15 / 17 🔶 işaretleri kaldırıldı →
>   "Sentez teyitli 21 Eki". (3) Sentez'in Paket 1 kapanış brief'ine cevapları (aşağıda).
> - **Sentez hükümleri (21 Eki):**
>   - Gelir kategorisi ledger'daki **income** satırına bağlanır; tek kategori **"Contract revenue"** yeter.
>   - İade + kredi bakiyesi: **R11, Paket 3 sonrası**.
>   - Ödeme para birimi ≠ `contract.currency` **serbest** (LED-11: eşitlik hesap ile hareket arasındadır).
>   - Kontrat devrinin ekstrede **net-sıfır iki satırı kabul**.
>   - Sapma (e) **kabul**: payout'un hesabı `commission_payouts`'ta değil ledger hareket satırında.
>   - Faz B'ye: auto-deploy'un `35cad76`'da tetiklenmeme sebebi (**Render event log**) · **Render CLI yenileme**.
> - **Commit:** ell-docs bu kayıt (Paket 1b ön işi; ayrı küçük commit). PUSH YOK.
> - **Ölçülenler:** `origin/main` = `ca2bd5b` (`git fetch`; `merge-base --is-ancestor` ✓) · kütükte 🔶 kalan **0**.
> - **⚠️ ÖLÇÜLMEDİ:** KB yüklemesinin kendisi (Suer teyidi) · gelir kategorisinin bağlanacağı paket (hüküm var,
>   uygulama yeri belirtilmedi).
> - **Bilinçle yapılmayanlar:** gelir kategorisi bağlantısının kodu (Paket 1b kapsamında değil) · 037'nin 4 gelir
>   kategorisine dokunma (hüküm "tek kategori yeter" der, mevcutları silmeyi söylemez).

> ## ✅ 2026-10-21 — PAKET 1b: STAGING'E HAZIR
>
> - **Ne yapıldı (dal `eliza-next`, SERBEST bölge, tek merge / tek revert):** Sentez Paket 1b (P1b-1..3).
>   - **Dal hazırlığı:** `eliza-next` → `main`'e fast-forward (`35cad76`), üzerine tek commit.
>   - **P1b-1 tedarikçi kaydı — 041:** `suppliers` (tür supplier/venue/contractor/other · ülke `core_countries` FK ·
>     ofis + vergi no isteğe bağlı · silinmez, pasiflenir · ad tekliği kiracı × normalize ad × ülke) +
>     `expenses.supplier_id` (nullable, bileşik FK; mevcut satırlar NULL, counterparty metni kalır).
>     API `/api/ledger/suppliers` (liste + ad araması · seçenekler · ekle · düzenle/pasifle · ödeme geçmişi —
>     ledger'dan türetilir, tarih aralığı). Gider listesi/ekstre tedarikçi adını taşır; ters gider tedarikçiyi devralır.
>   - **P1b-2 referans tohumu: BULAMADIM → migration YOK** (aşağıda ölçüm). Zoho dışa aktarım talimatı teslim
>     metninde (Suer); liste gelince ayrı tohum dilimi (runner ile, ON CONFLICT DO NOTHING, mevcut 6/4/4 korunur).
>   - **P1b-3 gider taslağı — 042:** `expense_drafts` (expenses alanları + source ai/import/manual + confidence notu +
>     eksik alan listesi + tedarikçi önerisi + karar). API `/api/expense-drafts` (POST · GET liste eksik/tam süzgeci ·
>     GET /:id · POST /:id/accept · POST /:id/reject). Kabul = `utils/ledger.js createExpense` — `POST
>     /api/ledger/expenses` ile TEK doğrulama yolu (gider ucu bu fonksiyona taşındı, davranış ve mesajlar aynı).
>   - **Ekran (iskelet):** gider formunda karşı taraf artık SEÇMELİ (datalist + "New supplier" kısayolu; listede
>     olmayan metin reddedilir) · ui2 Suppliers listesi + tedarikçi detayı (geçmiş, tarih süzgeci, kayıt düzenleme) ·
>     ui2 "Expense drafts" (eksik alanlar kırmızı, öneri seçili ama atanmış değil, Accept/Reject, elle taslak).
>     Yeni ekranlar Finance > Expenses altında; oraya sayfa içi bağlantıyla gidilir (subnav'a öğe EKLENMEDİ —
>     Paket 1'in 6'lı subnav testi aynen geçsin diye; subnav'a eklemek ayrı karar).
> - **Commit:** LEENA `eliza-next` **`8119683`**. PUSH YOK.
> - **Kütük taraması (pakete değen):** Suer ilkesi (defter, kilitli) · LED-03 · LED-08 · LED-11 · LED-16 · LED-17 ·
>   LED-19 · YZ-01/02/03 · OFS-05 · OFS-01 (S-16r) · D2 · SEM-01 · RAP-01 · YON-07 · YON-11 (SERBEST) · TABAN.
>   **Yeni:** LED-18 · LED-20 · LED-21 (🔶 Sentez teyidinde) · LED-16'ya not.
> - **Ölçülenler:**
>   - **P1b-2 ön ölçümü:** LIFFY / LEENA ayar dosyalarındaki DB bağlantıları yalnız `liffy` · `leena_v401_db` ·
>     `leena_staging_db`'ye gider — eliza-db'ye salt-okunur yol **BULAMADIM**. eliza-legacy şema dökümü
>     (`~/ELL_schema_dumps/eliza_schema_2026-06-02.sql`, tarihsel — YON-01): yalnız `expenses(category text, …)`
>     — tek seviyeli serbest metin, gider tipi / gelir kategorisi tablosu YOK. eliza kodu: Zoho sync yalnız
>     `fetchSalesOrders.js`; `ELIZA_CURRENT_STATE.md` "Expense Tracking: Not started … no active writer". → liste
>     eliza-legacy'de olsa bile tek seviyeli olurdu; kaynak Zoho'nun kendisi. (eliza reposunun kendi `.env`'inde
>     `DATABASE_URL` adı var — LIFFY/LEENA kapsamı dışında, KULLANILMADI.)
>   - **Runner planı canlı + staging (salt-okunur oturum, `plan()` yalnız SELECT):** iki tarafta kayıt **42**, bekleyen
>     TAM `041_suppliers`, `042_expense_drafts`, DUR koşulu **0**.
>   - **Prova (yerel PG 17.10, staging şeması):** `pg_dump --schema-only` + az veri (schema_migrations, core_countries,
>     offices, currencies, accounts, expense_categories/types, expenses, ledger_entries; organizers SENTETİK) →
>     gerçek CLI: "DRY-RUN OK: 2" · "COMMIT: 2" · tekrar "Nothing to apply"; NOTICE `041: expenses 1 rows — supplier_id
>     NULL on all`. Prova DB'si + dökümler silindi. ⚠️ İlk veri dökümüne `organizers` tablosu girmişti — dosya
>     açılmadan silindi, `organizers`'sız yeniden alındı.
>   - **Testler:** **269 → 316/316** — PG 14.18'de 3 koşu + PG 17.10 geçici kümede 1 koşu, hepsi aynı. Yeni:
>     `test_ledger_p1b` 31 · `test_ledger_p1b_premig` 6 (yeni kod + ≤ 040 şema: gider formu 201, tedarikçi/taslak
>     uçları 503) · `test_ui2_p1b_pages` 7 · `test_migrate` 16 → 19 (R15-R17 Paket 1b). **TABAN 342.00 KAYMADI**
>     (T35 + I5 + P1b T35). Test DB'si üçüncü kopya `ell_comm_test_p1` (≤ 040) eklendi.
>   - **Tarayıcı (Playwright, yerel test DB):** gider formunda listeden tedarikçi → `supplier_id` dolu gider · listede
>     olmayan metin istemcide reddedildi · "New supplier" kısayolu yazılanı ad olarak aldı, kaydetti, seçti · tedarikçi
>     listesi/detayı (€120.00, ödeyen hesap) · yapay zeka taslağı: 5 eksik alan kırmızı (renk `--dang`), öneri "Expo
>     Stand Builders (TR)" seçili → kabul: gider 230.00 + `out` hareketi, taslak accepted · elle taslak → ret ·
>     ekstrede tedarikçi adı. Sayfa hatası 0; konsoldaki 6 adet 500'ün hepsi `/api/expos` (test DB stub'ı, YON-09).
> - **YON-05 (çürüyen varsayım):** "Var olan view 036+ dosyasında `CREATE OR REPLACE` ile genişletilebilir" — runner'ın
>   yarım-iz denetimi (`scripts/migrate.js:95-96`) adı geçen VAR OLAN view'ı iz sayar → staging/canlıda DUR olurdu.
>   041 view'a dokunmadan yazıldı (join), LED-16'ya not.
> - **Test kuralı notu:** `test_migrate` R9/R12/R13 Paket 1 dosya kümesini sabit sınıyordu (036-040, "5", 42); 041-042
>   eklenince kırıldı. Beklentiler DEĞİŞMEDİ — prova girdisi o pakete donduruldu (gerçek dosyaların ≤ 040 kopyası +
>   runner'ın kopyası); Paket 1b geçişi YENİ testlerde (R15-R17).
> - **⚠️ Sır olayı (bu oturum, değer YAZILMAZ):** P1b-2 için ayar dosyası taramasında maskeleme LIFFY
>   `.claude/settings.local.json` satırlarını tam kapsamadı; oturum çıktısına Anthropic API anahtarının ve LIFFY
>   `JWT_SECRET`'ın birer PARÇASI düştü. İkisi zaten Faz B'de (iptal/yenileme) — öncelik yükselir. Ders (yeniden):
>   sır dosyasında yalnız `grep -l` / `-c` / ad + satır no; içerik satırı hiç basılmaz.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** staging/canlı deploy + migration · staging tarayıcı oturumu · eliza-db içeriği
>   (bağlantı yok) · Zoho'daki gerçek kategori/tip listesi · aksan duyarsız eşleşme (`unaccent` yok: "Société" ↔
>   "societe" eşleşmez — basit normalize kabul) · worker logları.
> - **Bilinçle yapılmayanlar:** P1b-2 tohum migration'ı (veri yok) · `expo_partners` bağı · eski `counterparty`
>   metinlerinin tedarikçiye eşlenmesi · API'de counterparty metninin reddi (mevcut davranış) · taslak düzenleme
>   (içerik değişmez; düzeltme kabulde) · `requirePermission` / servis kullanıcısı / `is_ai` (Paket 2) · subnav öğesi ·
>   gelir kategorisi bağlantısı · staging DB tazeleme — **Sentez şartı "her kapı öncesi taze kopya"; bu paket yalnız
>   ekleme (yeni tablo + nullable kolon), tazeleme GEREKMEZ; Paket 2 öncesi tazelenir.**
> - **🔶 Sentez'e:** LED-18/20/21 teyidi · Zoho adları ("OFFICE EXPENCES", "SALES COSTS") REQ'nin 6 kategorisine mi
>   eşlenecek, yoksa Zoho adıyla mı tohumlanacak · gelir hükmü "tek kategori Contract revenue" varken Revenues
>   modülünün Income Category listesi hâlâ istenecek mi · yeni ekranlar subnav'a eklensin mi (U1 testi 6'lı).
> - **Teslim (Suer):** push → staging Shell `node scripts/migrate.js --dry-run` → `node scripts/migrate.js` → ekranlar →
>   "merge" → canlı sırası (export → push main → canlı Shell dry-run → migrate). Ayrıntı teslim metninde.

> ## ✅ 2026-10-22 — PAKET 1b: MAIN'E MERGE (canlı sırası Suer'de)
>
> - **Ne yapıldı:** Suer "merge" dedi → yerel `main`'e `git merge --no-ff eliza-next` → **`613ce8e`**
>   (ebeveynler `35cad76` = origin/main · `8119683`). Gelen yalnız `8119683` (041–042 + tedarikçi / taslak API +
>   seçmeli tedarikçi + 3 ui2 ekranı). **Tek revert:** `git revert -m 1 613ce8e`. Merge ağacı = `8119683` ağacı
>   (birebir, `rev-parse ^{tree}` = `b02e501`).
> - **Commit:** LEENA `main` **`613ce8e`** (yerel; origin/main'in 2 önünde). **PUSH YOK.**
> - **Ölçülenler (CC, bu tur; DB'ler salt-okunur oturum):**
>   - `origin/eliza-next` = `8119683` (Suer push etti) · `origin/main` = `35cad76`.
>   - **Staging:** runner `plan()` kayıt **44**, bekleyen 0, DUR 0 · 041–042 `applied_at` ikisi de
>     **2026-10-22 07:49:23 UTC** (tek transaction). Suer'in deneme izi: 1 tedarikçi (venue, NG, 07:51 UTC) ·
>     1 tedarikçili gider + `out` hareketi (07:52) · 1 elle taslak (07:55, 2 eksik alan) **pending** — kabul 0, ret 0 ·
>     21 Eki'deki eski gider `supplier_id` NULL (beklenen). `ui2/finance-drafts|suppliers|supplier.html` **200** ·
>     `/api/expense-drafts` ve `/api/ledger/suppliers` token'sız **401** (route bağlı) · `finance-expenses.html`
>     `sup-list` taşıyor (yeni kod servis ediliyor).
>   - **Canlı:** runner `plan()` kayıt **42**, bekleyen TAM `041_suppliers`, `042_expense_drafts`, DUR 0 ·
>     `expenses` 0 · `accounts` 0 · `ledger_entries` 0 · `leena.app/ui2/finance-drafts.html` **404**,
>     `finance-expenses.html` 200 ama `sup-list` YOK (beklenen: push öncesi) · `/health` 200.
>   - **TABAN contract 4 sr earned = 342.00 (7 dilim)** staging (041–042 SONRASI) ve canlıda, SLICE_CTES ile.
>   - **Testler `main` üzerinde:** **316/316**, ❌ 0 (tek koşu; T35 + M01a + I5 342.00).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** Suer'in staging görsel onay raporu (yalnız "merge" geldi) · **staging'de taslak
>   Kabul ve Ret akışı** — DB izi yalnız oluşturmayı gösteriyor; kabul denenip 400 aldıysa taslak tasarım gereği
>   pending kalır, DB'den ayırt edilemez (yerelde tarayıcıyla geçti, 21 Eki kaydı) · tedarikçi detay ekranının ve
>   "+ New supplier" kısayolunun açıldığı · canlı deploy + migration · worker logları.
> - **Bilinçle yapılmayanlar:** push (`main` ve ell-docs) · canlı DB'ye yazma / migration koşumu · staging deneme
>   verisinin silinmesi (tedarikçi silinmez, pasiflenir; taslak silinmez, reddedilir — Suer'in kararı) ·
>   `eliza-next`'in `main`'e eşitlenmesi (sonraki dal işinin ilk adımı: `git merge --ff-only main`) · P1b-2 tohumu
>   (Zoho dışa aktarımı bekleniyor).
> - **Teslim (Suer, canlı sırası):** export (Render panel) → YON-06 (status.render.com + takvim) →
>   `git push origin main` → Live (~60 sn, G43; auto-deploy tetiklenmezse Manual Deploy — `35cad76`'da öyle oldu;
>   arada gider formu tedarikçisiz çalışır, tedarikçi / taslak uçları 503 "not migrated yet" — `test_ledger_p1b_premig`) →
>   canlı Shell `node scripts/migrate.js --dry-run` (DUR: `database` ≠ `leena_v401_db` / "DUR —" / FAILED; beklenen
>   NOTICE `041: expenses 0 rows`, "DRY-RUN OK: 2") → `node scripts/migrate.js` → "COMMIT: 2" → tekrar "Nothing to
>   apply" → ui2 contract 4 €342.00 + `finance-drafts.html` açılıyor. Shell açıkken deploy yok (G46).
> - **Kapanış (YON-03):** canlı koşum sonrası CC salt-okunur teyit kaydı (`schema_migrations` 44, TABAN, sayfa 200)
>   ayrı kayıt olarak girer; o kayda kadar Paket 1b AÇIK. P1b-2 ayrıca AÇIK.

> ## ✅ 2026-10-22 — PAKET 1b CANLIDA (KAPI-1 geçti)
>
> - **Ne yapıldı (Suer, 22 Eki):** `git push origin main` (`35cad76..613ce8e`) → auto-deploy **tetiklendi**
>   (`35cad76`'nın aksine), `finance-drafts.html` 200. Canlı Shell `node scripts/migrate.js --dry-run` + gerçek:
>   **2/2 (041, 042)**. Staging'de taslak **Kabul** → gider #3 doğdu (Suer gördü). **Export ATLANDI — Suer kararı:**
>   21 Eki 17:54 export + PITR 7 gün var; migration yalnız ekleme (yeni tablo + nullable kolon).
> - **Commit:** LEENA'da yeni commit YOK (`main` = `origin/main` = `613ce8e`) · ell-docs bu kayıt.
> - **Ölçülenler (CC salt-okunur teyit, 22 Eki; canlı `claude_readonly`, staging salt-okunur oturum):**
>   - `origin/main` = `613ce8e` (yerel reflog: push 2026-10-22 11:16:41 +0300).
>   - **Canlı:** runner `plan()` kayıt **44**, bekleyen 0, DUR 0 · 041–042 `applied_at` ikisi de **08:19:31 UTC**
>     (tek transaction). Nesneler staging'le aynı: `suppliers` + `expense_drafts` üzerinde 4 trigger ·
>     `expenses.supplier_id` VAR · 4 indeks · `core_countries` 230.
>   - Canlı veri: tedarikçi 0 · gider 0 · taslak 0 · hareket 0 · hesap 0 (canlıda deneme girişi yok).
>   - **TABAN contract 4 sr earned = 342.00 (7 dilim)** canlı + staging, SLICE_CTES ile.
>   - HTTP (leena.app): `ui2/finance-drafts.html` · `finance-suppliers.html` · `finance-supplier.html` ·
>     `finance-expenses.html` (`sup-list` VAR — seçmeli form servis ediliyor) · `finance-summary.html` · `/health`
>     **200** · `/api/expense-drafts` ve `/api/ledger/suppliers` token'sız **401**.
>   - **Staging Kabul izi:** taslak 1 (manual) `accepted`, `expense_id` = 3, `reviewed_at` 08:12 UTC → gider 3
>     tedarikçili + `out` hareketi (aynı dakika). Staging toplam: tedarikçi 1 · gider 3 (2'si tedarikçili) · hareket 3.
> - **🔶 Export kuralı önerisi (Suer → Sentez; KURAL DEĞİL, karar bekliyor):** canlı push öncesi yeni export yalnız
>   (a) veri değiştiren / silen migration varsa ya da (b) son export 24 saatten eskiyse. Bugüne kadarki teslim
>   metni "DUR: export bitmeden push yok" diyordu. Bu tur öneriye uyuyor: 041–042 yalnız ekleme; 21 Eki 17:54
>   → 22 Eki 11:16 +0300 push arası 24 saatten kısa (17:54 hangi saat diliminde olursa olsun).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** export zamanı ve PITR süresi (Suer beyanı; Render paneli CC'ye kapalı) ·
>   canlı dry-run çıktısının metni (rapor "2/2"; Target satırı / NOTICE görülmedi) · auto-deploy'un bu kez
>   tetiklenip `35cad76`'da tetiklenmeme sebebi (Faz B, Render event log) · staging'de taslak **Ret** akışı
>   (rejected 0; yerelde tarayıcıyla geçti, 21 Eki kaydı) · canlı tarayıcıda yeni ekranlar ve ui2 contract 4
>   €342.00 görünümü (TABAN DB'den ölçüldü) · worker logları.
> - **Bilinçle yapılmayanlar:** canlıda tedarikçi / gider / taslak girişi (Suer) · staging deneme verisinin
>   temizliği (tedarikçi pasiflenir, taslak reddedilir — silinmez) · `eliza-next`'in `main`'e eşitlenmesi (sonraki
>   dal işinin ilk adımı: `git merge --ff-only main`) · P1b-2 tohumu (Zoho CSV bekleniyor).
> - **Geri dönüş (YON-11):** `git revert -m 1 613ce8e` yalnız kodu geri alır; 041–042 şeması kalır. Restore
>   kanıtlanmadı.
> - **Kapanış (YON-03):** ell-docs push → KB yeniden yükleme (Sentez + Orchestrator) → `KB @ <hash>` satırı Suer
>   teyidiyle girer; o satıra kadar Paket 1b belge tarafında AÇIK. **P1b-2 AÇIK** (Zoho CSV → ayrı tohum dilimi) ·
>   LED-18 / LED-20 / LED-21 🔶 Sentez teyidinde.

> ## ✅ 2026-10-22 — PAKET 1b BELGE KAPANIŞI (KB @ d638987) + SENTEZ KARARLARI
>
> - **Ne yapıldı:** (1) YON-03 kapanışı: **KB @ d638987** (Orchestrator + Sentez) → Paket 1b belge tarafı KAPALI.
>   (2) Kütük: LED-18 / LED-20 / LED-21 🔶 kaldırıldı → "Sentez teyitli 22 Eki". (3) Sentez'in Paket 1b kapanış
>   brief'ine kararları (aşağıda); export kuralı kütüğe **YON-12**; LED-17'ye not. (4) ★SIRADAKİ güncellendi.
> - **Sentez kararları (22 Eki):**
>   - **P1b-2 tohumu ZOHO ADIYLA:** büyük harf normalize edilir, yazım hatası düzeltilir ("EXPENCES" → "EXPENSES");
>     çakışmada Zoho kazanır; mevcut 6 kategori Zoho adlarıyla eşleştirilir, **ID korunur**.
>   - **Gelir kategorisi tohumlanır (15):** ödemede zorunlu DEĞİL, varsayılan "Contract revenue". (21 Eki'deki
>     "tek kategori yeter" hükmünü genişletir.)
>   - **Suppliers + Drafts Finance alt menüsüne girer** — K-G kuralıyla (Sentez 19 Eki: eski davranış değişmez,
>     ekleme geriye uyumlu ve testli); Paket 2'de aynı dalda (4c).
>   - **Export kuralı → YON-12:** canlı push öncesi yeni export (a) veri değiştiren/silen migration · (b) son export
>     >24 saat · (c) KAPI-2 paketlerinde HER ZAMAN; PITR yedek değildir, kanıtlı restore yedektir.
>   - **Faz B önceliği kabul:** Paket 2 SONRASI, Paket 3 ÖNCESİ.
>   - **Tasarım fazı kuyruğu:** UI düzeni (sayfa içi bağlantılar menüye — iskelet sonrası) · sayfa geçiş yavaşlığı
>     (ölçülecek).
>   - **P1b-2 tohum dilimi** Suer CSV'yi getirince sıraya ARAYA GİRER.
> - **Commit:** ell-docs bu kayıt (Paket 2 ön işi; ayrı küçük commit). PUSH YOK.
> - **Ölçülenler:** `origin/main` = `d638987` (`git fetch`) · kütükte 🔶 kalan **0** · YON'da son numara YON-11 → yeni
>   YON-12.
> - **⚠️ ÖLÇÜLMEDİ:** KB yüklemesinin kendisi (Suer/Orchestrator beyanı) · Zoho'daki 15 gelir kategorisinin adları
>   (CSV bekleniyor).
> - **Bilinçle yapılmayanlar:** tohum migration'ı (CSV yok) · mevcut 6 kategorinin yeniden adlandırılması (tohum
>   dilimiyle; mevcut satır güncellemesi → YON-11'e göre KAPI-2 değerlendirmesi o dilimde).

> ## ✅ 2026-10-22 — PAKET 2: STAGING'E HAZIR
>
> - **Ne yapıldı (dal `eliza-next`, KAPI-2, tek merge / tek revert):** Sentez Paket 2 (P2-1..P2-4) + Suppliers/Drafts
>   alt menüye (4c, K-G kuralıyla). Dal hazırlığı: `eliza-next` → `main`'e fast-forward (`613ce8e`), üzerine tek commit.
>   - **P2-1 (043 + `/api/users` + davet):** `users.office_id` · `user_invites` (token SHA-256, 72 saat, tek kullanım,
>     yeniden davet/pasifleştirme iptal eder) · internal temsilci bağı backfill (tek e-posta eşleşmesi; çoklu boş) ·
>     liste / davet / yeniden davet / profil (ad · ofis · temsilci bağı) / aktif-pasif (sebep zorunlu) ·
>     `/api/user-auth/invite/check|accept` (kimlik doğrulamasız, token POST gövdesinde) · e-posta `email_queue`
>     transactional (campaign_id NULL) · `INVITE_ECHO=1` yalnız staging.
>   - **P2-2 (044 + `utils/permissions.js`):** kayıt defteri 18 kod · 5 sistem şablonu (Owner 0 · Finance 12 · Project 3 ·
>     Office Manager 12 · Sales 3 satır; değişmez, DB trigger) · `user_permissions` (grant + kapsam | revoke) ·
>     `users.role_id` (Owner'lar Owner şablonunda) · tek çözümleme yeri + kapsam + boş `regionFilter` yuvası (SAT-04).
>   - **P2-3 (KAPI):** `requirePermission` — ledger yazma (referans veri, hesap, transfer, gider, tedarikçi, bütçe
>     revizyonu) · gider taslakları (okuma/yazma/kabul-ret) · payout yazma · `/api/users`. EMS / contracts / payments
>     DOKUNULMADI. `authMiddleware`: user_id taşıyan token'da `is_active` denetimi (klasik token DB'ye gitmez).
>     `/me` etkin yetki özetini döner; `ui2CanSee` / `ui2RenderSubnav` onu okur (menü UX).
>   - **P2-4 (045):** `audit_log` yalnız eklenir; davet / kabul / aktif-pasif / profil / şablon / kişi başı yetki /
>     bütçe kilidi (LED-15) yazılır.
>   - **Ekran (iskelet):** ui2 Admin > Users (liste + davet; e-posta eşleşen temsilci önerilir) · kullanıcı detayı
>     (profil · durum · davet · şablon + kişi başı ezme tablosu · geçmiş [Owner]) · `ui2/invite.html` (şifre belirleme) ·
>     ui2 login davetten dönüşte e-posta dolu · "Who is signed in" Role/Office/Access · Finance subnav'a Suppliers + Drafts.
> - **Commit:** LEENA `eliza-next` **`ce670ab`**. PUSH YOK.
> - **Kütük taraması (pakete değen):** B9 · B10 · B12 · B20 · B21 · B22/B23 · B24 · B25 · B27/B28 · B30 · B32 · B33
>   (reports_to — bu pakette YOK) · B40 · B42 (alan kapısı — bu pakette YOK) · SEM-03/04/05 · K-A · K-G · LED-09/15 ·
>   OFS-05 · YZ-02 (servis kullanıcısı — karar yok) · SAT-04 · YON-07/09/11/12 · G45 · TABAN. **Yeni:** YET-01..09
>   (🔶 Sentez teyidinde).
> - **Ölçülenler (ADIM 0, salt-okunur):**
>   - `authMiddleware` bugün yalnız `decoded.organizer_id` okur (`middleware/authMiddleware.js:17`, eski hali); require
>     eden: **33 route dosyası + `index.js`** (inline `/api/templates`). `dualAuth` / `terminalAuth` DOKUNULMADI.
>     Eski `/login.html` organizers'ta kalır (SEM-05 takvimi, en erken 20 Kas).
>   - **sales_agents ↔ users (canlı):** users 1 · temsilci 152 (internal 128 — e-postalı 126; external_freelance 19;
>     external_agency 5) · e-postası users'la eşleşen internal **1** (Suer) · aynı e-postayı paylaşan internal grup **11**
>     (bunlara sahip kullanıcı olursa bağ boş kalır) · kiracı 1. → 043 canlıda beklenen: **bağ 1, belirsiz 0, eşsiz 0**.
>   - **SendGrid transactional yolu:** `email_queue.campaign_id` nullable; canlıda campaign_id NULL satırlar var (sent);
>     worker 1. öncelik kuyruğu `campaign_id IS NULL` (`email_worker.js:60`), Mode 1 = `html_content` + `recipient_email`
>     (`:212`); `organizer_id` / `expo_id` / `visitor_id` nullable → davet satırı bu yoldan gider.
>   - **TTFB (3 ölçüm medyanı, s):** canlı contract 0.40 · expenses 0.39 · summary 0.28 — staging 0.29 · 0.28 · 0.28.
>   - **Runner `plan()` canlı + staging (salt-okunur):** iki tarafta kayıt **44**, bekleyen TAM 043–045, DUR **0**.
>     Canlıda `organizers` **2** satır; aktif Owner yalnız kiracı 1'de → şablon tohumu yalnız kiracı 1'e (LED-17 deseni).
>   - **Prova (yerel PG 17.10, staging ŞEMASI — `pg_dump --schema-only`, veri YOK; schema_migrations / offices /
>     core_countries verisi + SENTETİK organizer/user/temsilci):** gerçek CLI "DRY-RUN OK: 3" · "COMMIT: 3" · tekrar
>     "Nothing to apply"; NOTICE `043: … users 1, linked 1, ambiguous 0, no match 0` · `044: permissions 18, roles 5,
>     role_permissions 30, users with role 1`. Küme + dökümler silindi.
>   - **Testler:** **316 → 379/379** — PG 14.18'de 4 koşu (ilk ikisi A3 testi eklenmeden 378/378, son ikisi 379/379) +
>     PG 17.10 geçici kümede 1 koşu (379/379). Yeni: `test_users_admin` 39 · `test_users_premig` 6 (yeni kod + ≤ 042 şema: kapılar eski davranış, users/davet
>     503, /me eski şekil) · `test_ui2_p2_pages` 14 · `test_migrate` 19 → 23 (R18–R21; R21 043'ün veri değiştiren bağ
>     adımı: tek eşleşme bağlanır, çoklu boş, external yok). **TABAN 342.00 KAYMADI** (T35 + I5 + P1b T35 + P2 T35).
>     Test DB'si dördüncü kopya `ell_comm_test_p1b` (≤ 042) + `email_queue` stub'ı (YON-09: test edilen kod yazar).
>   - **Tarayıcı (Playwright, yerel test DB, `INVITE_ECHO=1`):** Owner 4 sekme (Admin dahil) → davet (Finance, Turkey) →
>     link ekranda + sunucu logunda → ayrı oturumda link → şifre → login'e e-posta dolu döner → Finance girişi: tek sekme
>     (Finance), subnav 8 öğe, `admin-users.html` "You do not have permission (users.read)" · Owner detayda 12 etkin yetki →
>     sebepsiz pasifleştirme engellendi → sebepli pasif → davetlinin eldeki oturumu sonraki sayfada 401 → çıkış → giriş
>     "Invalid email or password" · denetim: invite → invite_accept → deactivate. Sayfa hatası 0 (konsoldaki 409/401'ler
>     reddedilmesi beklenen istekler).
> - **Test kuralı notu (assertion değişimleri — gerekçeli):**
>   - `test_ui2_ledger_pages` U1/U4 (subnav 6 → 8) ve `test_ui2_p1b_pages` P1 (aktif öğe `expenses` → `suppliers`/`drafts`):
>     Sentez 22 Eki kararı (Suppliers + Drafts alt menüye) bu beklentileri doğrudan değiştirir; U1 artık Paket 1'in 6
>     öğesinin AYNI sırada yerinde olduğunu da ölçer (K-G: eski davranış değişmez, ekleme sonda).
>   - **Fixture (assertion aynı):** kapılı uçlarda eski token 409 köprüsü aldığı için `test_ledger` / `test_ledger_p1b` /
>     `test_payouts`'un varsayılan aktörü Owner kullanıcı oturumu; `test_ledger` klasik oturum kilit satırı (B2) açıkça
>     klasik token'la koşar, STAFF'a Finance şablonu verildi (B3 OWNER_REQUIRED'ı ölçmeye devam etsin).
>   - `test_users` T1: geri alınan transaction'a `ell.allow_user_admin_reset` (034 / Paket 1 emsali; CASCADE yeni
>     tablolara iner). `test_migrate` R15–R17 girdisi ≤ 042'ye donduruldu (R9–R14 emsali), beklentiler aynı.
> - **🔶 Sentez'e (karar / teyit):**
>   - **`authMiddleware`'e dokunuldu (KAPI-2):** yalnız user token'ında tek PK sorgusu, klasik token birebir (A3 testi: 0
>     sorgu). Alternatifi (kontrol yalnız kapılı uçlarda) pasif kullanıcıya 30 gün EMS/contracts/payments erişimi bırakırdı.
>   - **Açık kalan:** `dualAuth` JWT yolu (toplu yaka kartı) DOKUNULMAZ olduğu için pasif kullanıcının token'ı orada
>     çalışmaya devam eder.
>   - **Davet linki `email_queue.html_content`'te düz metin** (worker Mode 1 gereği): DB okuyabilen görür; tek kullanımlık
>     + 72 saat. Worker değişikliği (KAPI-2) olmadan kapanmaz.
>   - **Şablon içerikleri** (Finance / Project / Office Manager / Sales — 044) varsayılandır; özellikle Project'e
>     `budget.write`, Office Manager'a `office` kapsamı, `reference.write`'ın hiçbir şablonda olmaması (REQ: Owner).
>   - **Şablon canlı bağ** (YET-04) · **yetki verme tavanı** (YET-07) · **kayıt defterinde `organizer_id` yok** (YET-01).
>   - **"commission yazma":** `routes/commissions.js`'te yazma ucu YOK (ölçüldü) → kapı payout'a; `/api/sales-agents`
>     yazmaları (B11) kapısız kaldı.
>   - **Şifre ≥ 6** korundu ("yetki diliminde SaaS ölçüsü" kuyruğu bu pakette yapılmadı) · davet e-postası küçük harfle
>     saklanır, login büyük/küçük harf duyarlı (mevcut davranış).
>   - **Merge sonrası:** klasik `/login.html` oturumuyla ledger yazma / payout (agent-statement) 409 + "ui2 ile giriş yap"
>     mesajı alır — finans yazmaları için ui2 girişi gerekir.
>   - Her ui2 sayfası açılışta bir kez `/me` çağırır (menü tazeleme; çizimi bekletmez) — "sayfa geçiş yavaşlığı" kuyruğuna not.
> - **Staging DB tazeleme (Sentez şartı: KAPI-2 öncesi taze kopya) — ÖLÇÜM + ÖNERİ, karar Suer'in:** canlı ↔ staging (salt-
>   okunur, sayı + parmak izi): fark YALNIZ Paket 1/1b deneme verisi (hesap 1 · gider 3 · hareket 3 · tedarikçi 1 ·
>   taslak 1). `users` · `sales_agents` · `organizers` · `offices` · `contracts` · `payments` parmak izleri ve
>   `schema_migrations` 44, `commission_payouts` 8, `payment_schedule_items` 14 AYNI. Paket 2'nin yazdığı/okuduğu
>   tablolar canlıyla birebir → **tazeleme atlanabilir (öneri)**. EMS tabloları karşılaştırılmadı (Paket 2 dokunmaz).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** staging/canlı deploy + migration · staging'de `INVITE_ECHO` · staging'de e-posta
>   worker'ı ve SendGrid gönderimi (davet satırı kuyrukta kalır mı, gider mi) · staging tarayıcı oturumu (P2-5) · EMS
>   ekranlarının user token'ıyla canlı davranışı (test DB'de EMS tabloları yok; yalnız middleware birim testi) ·
>   kiracı 2'nin kim olduğu (şablon almaz) · worker logları.
> - **Bilinçle yapılmayanlar:** organizers → users taşıma (20 Kas+) · şifre sıfırlama e-postası · rate limit · LIFFY↔LEENA
>   tek giriş · genel audit · alan gizleme (B42) · `reports_to` hiyerarşisi (team = own) · özel şablon ekranı/API'si ·
>   `is_owner` verme/alma · servis kullanıcısı (YZ-02) · `dualAuth` · sales-agents kapısı · şifre kuralı · P1b-2 tohumu.
> - **Teslim (Suer):** push → staging Shell migrate (dry-run → gerçek) → staging env `INVITE_ECHO=1` + deploy → P2-5
>   kapanış ekranı → "merge" → canlı sırası (**export ZORUNLU, YON-12 (c)**). Ayrıntı teslim metninde.

> ## ✅ 2026-10-22 — SAYFA ENVANTERİ (teslimat ölçümü, salt-okunur; Sentez 22 Eki, YON-11 istisnası)
>
> - **Ne yapıldı:** LEENA `public/` altındaki tüm HTML'in sayfa başı envanteri — alan · fuar yüzeyi · menü/link/akış izi ·
>   son commit · ui2 ikizi · API uçları · fuar no gömülü · ölü aday — + ui2 sayfa geçişi canlı ölçümü (TTFB, yükleme
>   sırası, istek sayısı). Taban `origin/main` = `613ce8e` (canlı); ölçüm ayrı worktree'de (`/tmp/ell-envanter`, ölçüm
>   sonrası kaldırıldı). `eliza-next` çalışma kopyasına (paralel Paket 2 oturumu) dokunulmadı, stash yok.
> - **Commit:** LEENA dal `audit/sayfa-envanteri` (main'den) **`9e17f69`** — tek dosya
>   `docs/audits/SAYFA_ENVANTERI_2026-10-22.md` (918 satır). PUSH YOK. Kod/DB değişmedi.
> - **Ölçülenler:**
>   - **Toplam 81** HTML (kök 61 · ui2 16 · callcenter 3 · email_templates 1; 7'si `*.backup.html`). Alan: EMS 49 ·
>     finance 18 (eski 7 + ui2 11) · auth 6 · ops 4 · ui2 kabuk 3 · admin 1 · **sales 0** (`ui2/sales.html` boş kabuk).
>   - **Ulaşılamayan 22** (kökler: `login.html` zinciri / backend'in ürettiği URL / `/ui2/` girişi; yorum dışı link):
>     **ölü aday 14** (7 yedek + admin-dashboard · checkin-import · dashboard · main-panel · login_new · register ·
>     email_templates/modern-default) · İZSİZ-FUAR 7 (bulk-badge-print · conference-scanner · lead-scan · hostess-guide ·
>     callcenter ×3 — kod linki yok, URL yalnız belge izinde) · İZSİZ-YENİ 1 (expo-create, son commit 2026-09-09).
>     Hüküm "kod izinde kullanıcı yok"; KALSIN/TAŞI/SİL Sentez'de, Suer onayıyla.
>   - **Fuar yüzeyi 18.** **Fuar no gömülü:** sayısal expo id 2 sayfa (`certificate.html:523-541` expo 7/13/9/10
>     yönlendirmesi · `lead-scan.html:185` `EXPO_ID = 3`) · tek-fuar içeriği 9 · yerel varsayılan 3 (Nigeria/Lagos).
>   - **ui2 ikizi:** var 0 · kısmi 3 (contract-list, contract-detail, login) · EMS'in 49 sayfasının hiçbirinin ui2
>     karşılığı yok. **ui2 adası:** eski arayüzden ui2'ye kod içi link 0; giriş yalnız `/ui2/` URL'i.
>   - **ui2 geçiş (canlı, curl, oturumsuz, 3 örnek medyanı):** tam sayfa yükleme; statik istek 3/5/7 + on-load API 0–6
>     (kod sayımı; en çok expenses 13) · TTFB HTML 0.234–0.323 s, varlık 0.230–0.249 s · `Cache-Control: public,
>     max-age=0` + ETag. 16/16 ui2 HTML'in canlı sha256'sı = `613ce8e`.
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** canlı kullanım (log/analytics — kural gereği) · DB'deki e-posta şablonlarının taşıdığı
>   sayfa URL'leri · elden dağıtılan URL'ler · uçların backend'de varlığı / HTTP metodu · ui2 on-load API'nin canlı sayısı,
>   Google Fonts, tarayıcı render süresi · Paket 2 sayfaları (`ce670ab`: +3 ui2 sayfası → merge sonrası 84) · v402
>   "fuar numarası gömülü 10 dosya" (`:3557`) kaynak listesi **BULAMADIM** → karşılaştırılamadı · backend'de gömülü
>   expo/form id'leri.
> - **Bilinçle yapılmayanlar:** KALSIN/TAŞI/SİL hükmü · kod/DB/CLAUDE.md değişikliği · push · `eliza-next`'e ve çalışma
>   kopyasındaki değişikliklere dokunma · belgelerdeki terminal anahtarlı URL'leri rapora kopyalama · SIRADAKİ bloğu
>   güncellenmedi (tek ekleme kuralı).

> ## ✅ 2026-10-22 — PAKET 2: MAIN'E MERGE (canlı sırası Suer'de)
>
> - **Ne yapıldı:** Suer "merge" dedi → yerel `main`'e `git merge --no-ff eliza-next` → **`b75c87b`**
>   (ebeveynler `613ce8e` = origin/main · `ce670ab`). Gelen yalnız `ce670ab` (043–045 + `/api/users` + davet +
>   `requirePermission` kapıları + audit + 3 yeni ui2 ekranı). **Tek revert:** `git revert -m 1 b75c87b`. Merge ağacı =
>   `ce670ab` ağacı (birebir, `rev-parse ^{tree}` = `ca652e2`). İlk deneme (`git merge -F -`) "could not read file '-'"
>   ile merge YAPMADAN durdu (main `613ce8e`'de kaldı); mesaj dosyayla verilip tekrarlandı. Çalışma kopyası ardından
>   `eliza-next`'e geri alındı (ağaç aynı → dosya değişmedi).
> - **Commit:** LEENA `main` **`b75c87b`** (yerel; origin/main'in 2 önünde). **PUSH YOK.**
> - **Ölçülenler (CC, bu tur; DB'ler salt-okunur oturum):**
>   - `origin/eliza-next` = `ce670ab` (Suer push etti) · `origin/main` = `613ce8e`.
>   - **Staging:** runner `plan()` kayıt **47**, bekleyen 0, DUR 0 · 043–045 `applied_at` üçü de **2026-10-22 09:57:55 UTC**
>     (tek transaction) · permissions 18 · roles 5 · role_permissions 30 · users 2 (ikisi de şablonlu) · bağlı internal
>     temsilci 1 · `user_permissions` 0 · `ui2/admin-users.html` + `invite.html` **200** · `/api/users` token'sız **401**.
>   - **P2-5 izi (staging `audit_log`, 3 satır, aynı hedef, aktörlü):** `user.invite` 10:02:14 → `user.invite_accept`
>     10:03:06 → `user.deactivate` 10:04:46 (sebepli; diff `is_active` + `invites_revoked`). Davetli kullanıcı: Finance ·
>     Turkey · şifreli · **pasif**. Davet satırı: kullanılmış, iptal yok, son geçerlilik 25 Eki 10:02 (72 saat).
>   - **Staging davet e-postası `email_queue`'da `pending`** (10:02:14'ten beri; 10:21 UTC'de hâlâ, `sent_at` boş) → e-posta
>     gitmedi; link ekrandan/logdan (INVITE_ECHO) alınmış. Staging'de kuyruğu tüketen worker yok ya da çalışmıyor —
>     hangisi ÖLÇÜLMEDİ. Satırdaki link kullanılmış token taşır (açılırsa genel hata).
>   - **Canlı:** runner `plan()` kayıt **44**, bekleyen TAM `043_user_invites`, `044_permissions`, `045_audit_log`, DUR 0 ·
>     users 1 (aktif Owner 1) · tek internal e-posta eşleşmesi 1, çoklu 0 → beklenen NOTICE `043: … linked 1 …` ·
>     `leena.app/ui2/admin-users.html` ve `/api/users` **404** (beklenen: push öncesi) · `ui2/finance-drafts.html` 200 ·
>     `/health` 200.
>   - **EMS tabanı (push öncesi; canlı sonrası aynı ölçüm tekrarlanır):** canlıda servis edilen 8 dosyanın sha256'sı =
>     `main` blob'u (8/8 AYNI): `login.html` · `dashboard_new.html` · `main-panel-v2.html` · `visitorlog-paginated.html` ·
>     `qrscanner.html` · `checkins.html` · `terminals.html` · `leena-fetch.js`. Merge'ün `public/` değişikliği YALNIZ
>     `ui2/` (4 yeni + 6 değişen); `dualAuth` · `terminalAuth` · EMS route'ları · `contracts` · `payments` · `routes/auth.js`
>     değişmedi (git diff). EMS'in yoluna giren tek dosya `middleware/authMiddleware.js` (klasik token DB'ye gitmez — test).
>   - **TABAN contract 4 sr earned = 342.00 (7 dilim)** staging (043–045 SONRASI) ve canlıda, SLICE_CTES ile.
>   - **Testler `main` üzerinde:** **379/379**, ❌ 0 (tek koşu, 20 suite; T35 ×2 + M01a + I5 342.00).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** Suer'in P2-5 ekran gözlemleri (yalnız "merge" geldi) — Finance'ta yalnız Finance
>   sekmesi, Admin'de "no permission", pasif sonrası oturumun düşmesi ve girişin reddi: DB'de giriş izi tutulmaz
>   (`users`'ta son giriş kolonu yok), audit yalnız 3 olayı gösterir · staging `INVITE_ECHO` env değeri (panel) · staging
>   worker durumu · canlı deploy + migration · Yaprak'ın eski girişi (canlı sonrası) · worker logları.
> - **Bilinçle yapılmayanlar:** push (`main` ve ell-docs) · canlı DB'ye yazma / migration koşumu · staging deneme izinin
>   (pasif Finance kullanıcısı, `pending` e-posta satırı) temizlenmesi — Suer'in kararı · `eliza-next`'in `main`'e
>   eşitlenmesi (sonraki dal işinin ilk adımı: `git merge --ff-only main`) · `audit/sayfa-envanteri` dalı (paralel oturum;
>   dokunulmadı).
> - **Teslim (Suer, canlı sırası):** **export (Render panel) — ZORUNLU, YON-12 (c)** (DUR: export bitmeden push yok) →
>   YON-06 (status.render.com + takvim) → `git push origin main` → Live (~60 sn, G43; auto-deploy tetiklenmezse Manual
>   Deploy). Arada (deploy → migrate penceresi) kapılar eski davranışta, `/api/users` + davet uçları 503 "not migrated",
>   `/me` eski şekil (`test_users_premig`) → canlı Shell `node scripts/migrate.js --dry-run` (DUR: `database` ≠
>   `leena_v401_db` / "DUR —" / FAILED / NOTICE farklı; beklenen `043: … users 1, linked 1, ambiguous … 0, no match 0` ·
>   `044: permissions 18, roles 5, role_permissions 30, users with role 1 …` · "DRY-RUN OK: 3") → `node scripts/migrate.js`
>   → "COMMIT: 3" → tekrar "Nothing to apply". Shell açıkken deploy yok (G46). Sonra **CC ölçer** (plan 47/0 · TABAN ·
>   EMS 8 dosya sha256 = `main` · `/api/users` 401 · ui2 sayfaları 200) + **Suer bakar** (Yaprak'ın eski `/login.html`
>   girişi · ziyaretçi listesi · check-in) → **KAPI-2**. Canlıda `INVITE_ECHO` YOK → davet e-postası canlı worker'la gider.
>   Merge sonrası finans yazmaları (ledger, payout) ui2 girişi ister.

> ## ✅ 2026-10-22 — PAKET 2 CANLIDA (KAPI-1 geçti)
>
> - **Ne yapıldı (Suer, rapor 22 Eki 14:01):** export 13:37 ✓ (YON-12 c) · `git push origin main` `613ce8e..b75c87b`,
>   auto-deploy tetiklendi ✓ · canlı Shell migrate dry-run + gerçek **3/3** (043–045; NOTICE `linked 1`, `18 / 5 / 30`) ·
>   `admin-users` 200. **Staging P2-5 akışının tamamı Suer tarafından görüldü:** davet → link → şifre → Finance girişi
>   (yalnız Finance sekmesi) → Admin "no permission" → Deactivate → giriş reddi. KAPI-2 (auth, YON-11) Sentez 22 Eki
>   GO'suyla açılmıştı; KAPI-1 (merge = deploy) bu push'la geçti.
> - **Commit:** LEENA canlı = `main` **`b75c87b`** (`origin/main` = `b75c87b`, ölçüldü). Bu kayıt: ell-docs.
> - **Ölçülenler (CC, 22 Eki 11:06 UTC; DB salt-okunur oturum, HTTP oturumsuz):**
>   - **Canlı DB:** runner `plan()` kayıt **47**, bekleyen 0, DUR 0 · 043–045 `applied_at` üçü de **11:01:14 UTC** (tek
>     transaction) · permissions 18 · roles 5 (Owner 0 · Finance 12 · Office Manager 12 · Project 3 · Sales 3 satır;
>     hepsi sistem, Owner şablonu tek) · role_permissions 30 · users 1, şablonu Owner · bağlı internal temsilci 1 ·
>     `user_invites` 0 · `user_permissions` 0 · `audit_log` 0 · davet e-postası 0 · ofisli kullanıcı 0 · ledger tarafı
>     değişmedi (expenses / accounts / ledger_entries / suppliers / expense_drafts hepsi 0).
>   - **TABAN contract 4 sr earned = 342.00 (7 dilim)** canlı (043–045 SONRASI) ve staging, SLICE_CTES ile.
>   - **EMS 8 dosya:** canlıda servis edilen sha256 = `main` blob'u **8/8 AYNI** ve merge öncesi tabanla aynı
>     (`login.html` · `dashboard_new.html` · `main-panel-v2.html` · `visitorlog-paginated.html` · `qrscanner.html` ·
>     `checkins.html` · `terminals.html` · `leena-fetch.js`), hepsi 200.
>   - **Paket 2 ui2 dosyaları:** `admin-users` · `admin-user` · `invite` · `admin-ui.js` · `shell.js` · `login` · `whoami` ·
>     `finance-drafts` → 200, sha256 = `main` **8/8** (yeni kod servis ediliyor).
>   - **Uçlar:** `/api/users` ve `/api/users/options` token'sız **401** · `/api/user-auth/invite/check` sahte token'la **400**
>     genel mesaj ("This invitation link is invalid or has expired…") · `/health` 200 · `ui2/finance-accounts.html` TTFB
>     0.30 / 0.27 / 0.27 s (merge öncesi ADIM 0 medyanı 0.28–0.40).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** **Yaprak'ın eski `/login.html` girişi ve EMS ekranlarının oturumlu davranışı** — Suer'in
>   raporunda yok; CC'de organizer kimliği yok (yalnız dosya + oturumsuz uç ölçüldü; klasik token'ın DB'ye gitmediği
>   testte) · canlıda davet / Finance kullanıcısıyla uçtan uca akış (yalnız staging'de) · canlı worker'ın davet e-postasını
>   gönderdiği (canlıda henüz davet yok) · staging worker durumu (davet satırı `pending`) · deploy ve worker logları.
> - **Bilinçle yapılmayanlar:** canlıya yazma · deneme daveti · staging deneme izinin temizlenmesi · `eliza-next`'in
>   `main`'e eşitlenmesi (sonraki dalın ilk adımı) · `audit/sayfa-envanteri` (`9e17f69`, origin'de YOK — push Suer'de).

> ## ✅ 2026-10-22 — PAKET 2 BELGE KAPANIŞI (KB @ 7a2d9fd) + UI-0 KRİTERLERİ (Sentez)
>
> - **Ne yapıldı (UI-0 ÖN İŞ A — belge, ayrı commit; inşadan ÖNCE):**
>   (1) YON-03 kapanışı: **KB @ 7a2d9fd** → Paket 2 belge tarafı KAPALI (Sentez UI-0 paketinin bildirimi).
>   (2) Kütük: **YET-01..09 🔶 KALIR** — Sentez teyidi gelmedi.
>   (3) Kütük yeni grup **UI — arayüz: UI-01..06** + "AÇIK SORULAR — KAPANDI" satırı; metin Sentez hükümlerinden
>   AYNEN (satır kırılımları birleştirildi, kelime değişmedi).
>   (4) Yeni belge **`ELIZA_UI2_ARAYUZ_KURALLARI_v1.md`**: UI-01..06 + UI-0 kapsamı (İNŞA / KAPSAM DIŞI / ORTAK) +
>   8 kabul ölçütü (Sentez metni aynen) + brief sapma notunun metni (§4).
>   (5) **`ELL_BILGI_MIMARISI_v4.md`** (v3 KALIR, değiştirilmedi): yalnız §4'e **§4.1 ui2 alt menü eşlemesi** —
>   Executive · Contracts (kontratlar, komisyonlar, agent'lar) · Money (… gider taslakları dahil) · Expo Finance;
>   Intelligence ui2'de YOK; Commissions & Agents Contracts grubunda. Başına v4 yama notu. README canlı belge
>   satırı v3 → v4; referans listesine arayüz kuralları belgesi.
>   (6) **`ELIZA_DESIGN_BRIEF_v1.md` ell-docs'ta BULAMADIM** (`grep -rln "DESIGN_BRIEF"` + dosya adı araması: 0)
>   → sapma notu brief'e yazılamadı; metni arayüz kuralları §4'te bekliyor. **Suer'den istenir; UI-0 onsuz
>   devam.** Repo DIŞINDA ölçülen 4 kopya (sha256 dördü de `b61895f9f841…`): `~/Downloads/` ·
>   `~/Desktop/UX_KB/` · `~/Desktop/Eliza_Audit_KB/` · `~/Downloads/Eliza Platform new ui design/uploads/` —
>   ell-docs'a ALINMADI (talimat yok); §8 başlığı "Technical constraints" (`:139`).
>   (7) Bu kayıt + ★SIRADAKİ'de UI-0 satırı (kriterler geldi) ve Paket 2 satırı (KB).
> - **Commit:** ell-docs (bu kayıt). PUSH YOK.
> - **Ölçülenler:** ell-docs `origin/main` = `7a2d9fd` = HEAD (`git fetch`, bu tur) · kütükte 🔶 satırı **9**
>   (YET-01..09; değişmedi) · kütükte `UI-0x` deseni önce **0** → **6** + kapanış satırı · BM v3 ↔ v4 farkı yalnız
>   başlık + yama notu + §4.1 (`diff`).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** KB yüklemesinin kendisi (Sentez/Orchestrator beyanı) · repo dışı brief
>   kopyalarından hangisinin Sentez'in kastettiği sürüm olduğu (dördü aynı içerik).
> - **Bilinçle yapılmayanlar:** brief'in ell-docs'a kopyalanması · v3 dosyasına dokunma · YET 🔶'larının kaldırılması ·
>   çalışma kopyasındaki `leena/CLAUDE.md` + `leena/todo.md` değişikliklerine dokunma (bu turun değil, commit'e girmedi).

> ## ✅ 2026-10-22 — PAKET UI-0: STAGING'E HAZIR
>
> - **Ne yapıldı (dal `eliza-next`, SERBEST, tek merge / tek revert; Sentez 22 Eki UI-0, kütük UI-01..06):** dal hazırlığı
>   `eliza-next` → `main`'e fast-forward (`b75c87b`), üzerine tek commit.
>   - **tokens.css** (UI-04): tek token dosyası — renk · yazı (font + ölçek) · boşluk · köşe/gölge; tema `html[data-theme]`
>     (vermillion varsayılan = `:root` · cobalt · eski `:root` paleti `signal` adıyla korundu — K-G). Kaynak: tasarım setinin
>     `styles/signal.css` + `themes.css`'i (repo kopyasıyla sha256 AYNI). signal.css'teki 4 sabit renk (#fff ×2, hover, çerçeve)
>     token oldu. **ui2'de tokens.css dışında sabit renk 0.**
>   - **components.js** (UI-03): Liste (her hücre `data-label`, satır → detay) · Detay (başlık + bölüm + anahtar/değer) · Form
>     (satır içi / yığılı; eksik alan kırmızı) · Özet kartı (tek stat-card; `href` → kayda iner, D2) · **para çifti**
>     (işlem birimi + sunucunun EUR'u; EUR yoksa "—") · boş / yükleniyor / hata. Sayfa işaretleme YAZMAZ.
>   - **nav.json** (UI-02): tek kaynak; `shell.js` yalnız okur (`/ui2/nav.json`), `ui2CanSee` aynen (Paket 2 /me özeti).
>     Finance alt menüsü 4 grup (UI-01): Executive (Summary) · Contracts (Contracts · Commissions · Agents) · Money (Accounts
>     [+ ekstre alt sayfa] · Transfers · Expenses · Suppliers [+ detay] · Drafts) · Expo Finance (Expo budget). Commissions /
>     Agents **yer-tutucu** ("soon" → `placeholder.html`, bugünkü klasik ekrana bağlantı: `/commissions.html`,
>     `/sales-agents.html`). Intelligence yok.
>   - **Giriş → Finance özet** (UI-06): Finance sekmesi `finance-summary.html`; `/ui2/` ve ui2 login sonrası nav.json `landing`'e
>     gider (Finance'ı göremeyen kullanıcı ilk görünen alanına). **Sales / Operations:** boş-durum ekranı (ölü link değil).
>   - **/ui2/_sablon/**: dizin + 4 şablon (list · detail · form · summary), sahte veri, `?state=empty|loading|error`.
>   - **Taşıma:** mevcut 19 ui2 sayfasının HEPSİ (Paket 2'ninkiler dahil) şablon + tokens'a; API çağrıları ve iş kodu aynen,
>     yalnız işaretleme bileşenden. ledger-ui.js / admin-ui.js veri yardımcısına indi (görsel kod components.js'e).
> - **Commit:** LEENA `eliza-next` **`1ad8456`** (üstünde `b75c87b` ff). ell-docs: `92bb1c9` (ön iş A) + bu kayıt. PUSH YOK.
> - **Ölçülenler:**
>   - **ÖN İŞ B:** "45 HTML tasarım seti" repoda ve ell-docs'ta **YOK**; repo DIŞINDA `~/Downloads/Eliza Platform new ui design/`:
>     45 HTML (kök 30 · `themes/` 12 · `warm/` 3) + 4 CSS; `var(--` kullanımı **3268**, sabit hex 802 (çoğu tema/palet tanımı:
>     `themes/` 12×34, Directions 126, Settings-Appearance 72). Setin `styles/signal.css` + `themes.css`'i = repo `ui2/styles`
>     kopyaları (sha256 aynı) → tokens.css oradan türetildi (elle çıkarma gerekmedi).
>   - **Sabit hex (aynı grep, dosya başına):** önce (`ce670ab`) **103** = signal.css 39 · themes.css 64 · sayfalar 0 →
>     sonra tokens.css **100**, tokens.css dışı **0** (32 dosya).
>   - **ui2 sayfa:** önce 19 HTML (Paket 2 dahil) / 25 dosya → sonra 25 HTML / 32 dosya (+ placeholder · `_sablon/` 5 ·
>     components.js · nav.json · tokens.css; − themes.css · ledger.css).
>   - **Eski nav yapısı (önce):** `shell.js` içinde sabit `UI2_DOMAINS` (4 sekme, Admin `userOnly`) + `UI2_SUBNAV.finance` düz
>     8 öğe (Contracts → `finance-contract.html` = c4 detayı; liste menüde yoktu); sales/operations boş. signal.css 251 satır
>     (39 hex `:root` + bileşenler; ui2'de kullanımı 0 ölçülen yardımcılar — row/col/gap/divider/kbd/live-dot/bar/delta/
>     input-group/stat/btn-lg/btn-icon/chip-outline — taşınmadı) · themes.css 80 satır · ledger.css 27 satır (`lg-*` düzen → `ui-*`).
>   - **Backend / API:** `git diff ce670ab 1ad8456` yalnız `public/ui2` + `tests` + `package.json` (test zinciri) — route,
>     middleware, migration, EMS sayfası DEĞİŞMEDİ.
>   - **Testler (PG 14.18, 2 koşu):** **379 → 416/416**, ❌ 0. Yeni: `test_ui2_ui0` 21 (N1–N8 nav + iki yönlü · G1–G2 giriş /
>     boş-durum · K1–K7 **bileşen-kopya** + para çifti + özet kartı + durumlar + liste · H1–H3 hex / token · T1 şablonlar) ·
>     `test_ui2_ui0_render` 16 (gerçek uçlar + tohum → 14 ekran tarayıcısız çizildi → API'nin her rakamı ekranda AYNEN;
>     **R1 sr earned €342.00 ekranda**). Mutasyon denemesi: sayfaya `<table>` / sabit hex / nav dışı sayfa / ölü nav yolu →
>     ilgili test KIRMIZI, geri alındı. **TABAN 342.00 KAYMADI** (T35 ×3 + M01a + I5 + ekranda R1/R4).
>   - **Tarayıcı karşılaştırması** (`tests/ui0_compare.js`, Playwright 1.63 + Chrome for Testing 145, aynı tohum, `1ad8456`
>     üstünde): 18 sayfa taşıma öncesi (`ce670ab` ağacı) / sonrası — `<main>` ondalıklı sayılar **eksik 0**, ek 4 (kontrat
>     listesinde gelirin EUR'u ×3 — API'de vardı, ekranda yoktu · eşit EUR bacağının tekrarı ×1); TABAN kontratında €342.00
>     önce ✓ sonra ✓ · 390 px'te yatay taşma **0** (18 sayfa + `_sablon` 4 şablon × 4 durum + dizin + yer-tutucu = 36) · sayfa
>     hatası 0 · **kabul 1 uçtan uca:** şifreli Finance kullanıcısı `/ui2/login.html` → `finance-summary.html`, sekme yalnız
>     Finance, gruplar Executive · Contracts · Money · Expo Finance; `/ui2/` → `finance-summary.html`. 79 ekran görüntüsü
>     (repoya konmadı, oturum karalamasında).
> - **Test kuralı notu (assertion değişimleri — gerekçeli, Sentez UI-02 "sayı testi silinir" + UI-03 taşıma):**
>   - `test_ui2_ledger_pages` U1: 8-öğe sayı/sıra testi SİLİNDİ → yerine 4 grup sırası + Paket 1 ekranlarının grubunda olması +
>     aktif öğe; U4: `keys.length === 8` sayı parçası silindi (bağlantı varlığı U2'de, iki yönlü test yeni suite'te).
>   - `test_ui2_p2_pages` S1–S3: sabit 8 → nav.json'dan türetilen Finance menü sayısı; S4: sabit 7 → türetilmiş + yer-tutucuların
>     izinsiz gizlendiği (commissions.read yok). Mantık aynı (klasik: hepsi · izin: süzülür).
>   - `test_ui2_p1b_pages` P5: `styles/ledger.css` → `signal.css` (birleşti); `lg-miss/lg-missing` → `C.missing()` + `missing:`
>     seçeneği (`ui-miss/ui-missing`, `--dang`) — ölçülen şey aynı (eksik alan kırmızı).
>   - **Fixture (assertion aynı):** vm'de koşan shell.js'e nav.json verisi hazır verilir (`ui2NavData`) — tarayıcıda fetch eder.
> - **Davranış farkları (Sentez kriteri gereği; K-G "eski davranış değişmez" değerlendirmesi için liste):** Finance sekmesi c4
>   detayı → özet · alt menü düz → 4 grup, "Contracts" → liste · ui2 login sonrası whoami → giriş (özet) · `/ui2/` bağlantı
>   sayfası → yönlendirme · avatar → whoami, marka → giriş · ayrı "EUR" sütunları → para çifti · dar ekranda liste kart olur, alt
>   menü kendi içinde kayar · negatif tutar tablo hücresinde kırmızı (önce `.table .num` eziyordu — hata düzeltmesi) ·
>   Sales/Operations metni İngilizce (dil kuralı) · kontrat "not found" metni listeye bağlantı verir.
> - **🔶 Sentez'e:** (1) yer-tutucu → klasik ekran bağlantısı ui2'den eski arayüze İLK kod içi köprü (envanter "ui2 adası": 0) —
>   kabul mü · (2) para çifti istisnaları (EUR'u API'de olmayan: kalem birim fiyatı · ekstre giriş/çıkış toplamı · taslak) ·
>   (3) nav.json alan adları İngilizce + ek alanlar (parent · legacy · landing · userOnly) · (4) `signal` teması korunsun mu ·
>   (5) ui2 bağlantı rengi vermillion (tasarım fazı).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** staging (push yok) ve 8 kabul maddesinin staging'de görünümü · staging/canlı GERÇEK
>   verisiyle ekran (yalnız test DB; contract 4 kimliği değil TABAN kurgusu) · Safari / Firefox / gerçek telefon (yalnız
>   Chromium 390×844 emülasyonu) · nav.json'un sayfa başına +1 isteğinin geçiş süresine etkisi (tasarım kuyruğu "sayfa geçiş
>   yavaşlığı") · Google Fonts'un tokens.css'ten yüklenmesi (aynı URL) · cobalt / signal temalarının görünümü (yalnız token
>   tutarlılığı H2) · erişilebilirlik (kontrast, klavye) · test DB'de tarih alanları ISO zaman damgası görünüyor
>   (`2025-12-31T21:00:00.000Z`, yerel TZ) — önce/sonra aynı, canlıdaki görünümü bu turda ölçülmedi.
> - **Bilinçle yapılmayanlar:** tema değiştirici · yeni Finance ekranı (Commissions/Agents yalnız yer-tutucu) · organizer paneli
>   (UI-06 → UI-1) · rol/yetki mantığı · EMS · backend / migration · `ui0_compare.js`'in npm zincirine alınması (tarayıcı
>   bağımlılığı repoda yok) · ekran görüntülerinin repoya konması · brief'in ell-docs'a alınması · main'e merge · push.
> - **Teslim (Suer):** `git push origin eliza-next` (LEENA, `ce670ab..1ad8456`) → staging auto-deploy (~60 sn, G43; migration
>   YOK) → 8 kabul maddesi `leena-staging.onrender.com` üzerinde (adresler teslim metninde) → "merge" → main'e tek merge.
>   ell-docs push ayrıca. Geri dönüş: merge sonrası `git revert -m 1 <merge>` (yalnız statik dosya + test; şema yok).

> ## ✅ 2026-10-23 — PAKET UI-0: MAIN'E MERGE (canlı sırası Suer'de)
>
> - **Ne yapıldı:** Suer "merge" dedi → önce `eliza-next`'e **`48789c5`** (yalnız CLAUDE.md: beklenen test sayısı
>   379 → 416; `1ad8456` bu satırı güncellememişti — Paket 1b/2'de inşa commit'i güncelliyordu) → yerel `main`'e
>   `git merge --no-ff eliza-next` → **`cb37f24`** (ebeveynler `b75c87b` = origin/main · `48789c5`). Gelen: `1ad8456` +
>   `48789c5`. **Tek revert:** `git revert -m 1 cb37f24`. Merge ağacı = `eliza-next` ağacı (birebir, `rev-parse ^{tree}` =
>   `1946d09`). `b75c87b..cb37f24` farkı: 45 dosya; `public/ui2/` ve `tests/` dışında yalnız `package.json` (test zinciri) +
>   `CLAUDE.md`. Backend route / migration / EMS sayfası YOK. Çalışma kopyası ardından `eliza-next`'e geri alındı.
> - **Commit:** LEENA `main` **`cb37f24`** (yerel; origin/main'in 3 önünde) · `eliza-next` **`48789c5`** (origin'in 1 önünde).
>   **PUSH YOK.**
> - **Ölçülenler (CC, 23 Eki 09:28–09:45 UTC; DB'ler salt-okunur oturum, `transaction_read_only=on`; HTTP oturumsuz):**
>   - `origin/eliza-next` = `1ad8456` (Suer push etti) · `origin/main` = `b75c87b` · ell-docs `origin/main` = `7a2d9fd`
>     (UI-0 belge commit'leri `92bb1c9` + `bc28b11` henüz push EDİLMEDİ).
>   - **Staging (`leena-staging.onrender.com`):** `1ad8456`'daki 32 ui2 dosyasının **32/32**'si 200 ve sha256 = git blob
>     (nav.json, tokens.css, components.js, `_sablon/` dahil) · klasik köprüler `/commissions.html` + `/sales-agents.html`
>     200 · `/health` 200.
>   - **Canlı (`leena.app`, push öncesi taban):** `b75c87b`'deki 25 ui2 dosyası **25/25** = blob · EMS 8 dosya
>     (`login.html` · `dashboard_new.html` · `main-panel-v2.html` · `visitorlog-paginated.html` · `qrscanner.html` ·
>     `checkins.html` · `terminals.html` · `leena-fetch.js`) **8/8** = `main` blob'u · `ui2/nav.json` ve
>     `ui2/styles/tokens.css` **404** (beklenen: push öncesi) · `/health` 200.
>   - **EMS'ten ui2'ye kod içi referans** (`1ad8456`, `public/` ui2 dışı + `index.js` + `routes/`): **0** → silinen
>     `themes.css` / `ledger.css`'i ui2 dışında yükleyen yok.
>   - **DB (her iki tarafta `schema_migrations` 47, son `045_audit_log`; UI-0 migration getirmez):** **TABAN contract 4 sr
>     earned = 342.00 (7 dilim)** canlı (`leena_v401_db`, `claude_readonly`) ve staging (`leena_staging_db`), SLICE_CTES ile.
>   - **Testler `main` üzerinde:** **416/416**, ❌ 0 (tek koşu; T35 ×3 + M01a + I5 + R1 342.00, R4 özet birebir).
> - **⚠️ ÖLÇÜLMEDİ / GÖZLENEMEDİ:** Suer'in staging'deki 8 kabul maddesi gözlemi (yalnız "merge" geldi) — giriş → Finance
>   özeti, alt menü tıklamaları, şablonların üç durumu, telefonda 390 px, Sales/Operations ekranı oturumlu olarak CC'de
>   görülmedi (staging için CC'de kullanıcı kimliği yok; dosya eşliği ve sayfaların 200 dönmesi ölçüldü) · staging'in gerçek
>   verisiyle ekran rakamları (yalnız test DB'de ölçüldü, `1ad8456` kaydı) · canlı deploy · Render event log.
> - **Bilinçle yapılmayanlar:** push (`main`, `eliza-next`, ell-docs) · canlıya yazma · `ui0_compare.js`'in staging'e karşı
>   koşulması (oturum gerekir) · Sentez 🔶 soruları (klasik köprü · tek birimli tutar istisnaları · nav.json ek alanları) —
>   açık kalır.
> - **Teslim (Suer, canlı sırası):** migration YOK, KAPI-2 değil (SERBEST) → **YON-12:** (a) yok · (c) yok · (b) son export
>   22 Eki 13:37 (+03) → push **23 Eki 13:37 (+03)'ten sonraysa YENİ export ZORUNLU** → YON-06 (status.render.com +
>   kampanya/fuar takvimi; G42) → `git push origin main` (`b75c87b..cb37f24`) → Live (~60 sn, G43; auto-deploy tetiklenmezse
>   Manual Deploy). Render Shell'de iş yok. Sonra **CC ölçer** (canlı ui2 32 dosya sha256 = `main` · eski `themes.css` /
>   `ledger.css` 404 · EMS 8 dosya = `main` ve push öncesiyle aynı · TABAN · `/health`) + **Suer bakar** (`leena.app/ui2/` →
>   giriş → Finance özeti; gerçek veriyle rakamlar). `eliza-next` push'u (`48789c5`, yalnız CLAUDE.md) staging'i yeniden
>   deploy eder, ekranı değiştirmez. Geri dönüş: `git revert -m 1 cb37f24` + push (şema yok).

> ## ★ SIRADAKİ ADAYLAR (Faz 3b-3 sonrası — karar Suer'de, seçim yapılmadı)
>
> - **★ SIRADAKİ (2026-10-22 — bu kazanır; aşağıdakiler tarihsel):**
>   1) ~~**Staging web servisi kurulumu**~~ → ✅ **STAGING CANLI (21 Eki)** →
>   2) ~~**Paket 1 — Ledger**~~ → ✅ **CANLIDA (21 Eki 18:30, `35cad76`, KAPI-1 geçti)** — **KAPALI kalır**
>   (yeni kriterler Paket 1b'ye — Sentez EK 21 Eki); ✅ belge kapanışı **KB @ ca2bd5b** →
>   **Sıra (Sentez EK 21 Eki, değişmedi):** Paket 1b (P1b-1..3) → Paket 2 → Paket 3 (amendment girdi).
>   3) ~~**Paket 1b — P1b-1..3**~~ (Sentez paketi 21 Eki, SERBEST bölge; dal `eliza-next`) — ✅ STAGING'E HAZIR
>   (21 Eki, `8119683`) → ✅ STAGING'DE (22 Eki 07:49 UTC) → ✅ MAIN'E MERGE (`613ce8e`) → ✅ **CANLIDA (22 Eki
>   11:19, KAPI-1 geçti)** — P1b-1 + P1b-3 **KAPALI**; ✅ belge kapanışı **KB @ d638987**.
>   **P1b-2 AÇIK:** eliza-db'de liste YOK (BULAMADIM) → Zoho CSV (Suer) → ayrı tohum dilimi (runner ile); **Suer
>   CSV'yi getirince sıraya ARAYA GİRER** (Sentez 22 Eki); tohum ZOHO ADIYLA, mevcut 6 kategori ID'si korunur, gelir
>   kategorisi 15 — [defter:2026-10-22 PAKET 1b BELGE KAPANIŞI].
>   - **P1b-1 tedarikçi kaydı** (`suppliers` + `expenses.supplier_id`; Suer notu 1 → Paket 1b) · **P1b-2 referans
>     tohumu** (eliza-legacy Zoho aynası ölçülür; Suer notu 2) · **P1b-3 gider taslağı** (aşağıdaki EK metni).
>   - **P1b-3 GİDER TASLAĞI (bot-yazılabilir giriş) — Sentez EK metni AYNEN:**
>     - LED-08 DEĞİŞMEZ: gider (expenses) değiştirilemez olaydır, onay statüsü taşımaz. YZ-01 gereği
>       yapay zeka iş verisi YAZMAZ → yapay zeka yalnız TASLAK yazar: expense_drafts (ayrı tablo):
>       alanlar expenses ile aynı + source (ai|import|manual) + confidence notu + eksik alan listesi
>       (JSON) + supplier_match (suppliers'a FK nullable + eşleşme skoru/aday adı) + status
>       (pending|accepted|rejected) + reviewed_by/at. İnsan "kabul" deyince expenses satırı doğar
>       (mevcut POST yolu, aynı doğrulama), taslak accepted olur, FK ile bağlanır; ret → rejected,
>       silinmez. Taslak ledger'a HİÇ yazmaz.
>     - API: POST /api/expense-drafts (yazar: yapay zeka istemcisi dahil, YZ-03 — mevcut uçların
>       istemcisi, ayrı yol yok) · GET liste (eksik alanlı/tam ayrımı filtre) · POST /:id/accept ·
>       POST /:id/reject. Yetki: şimdilik oturum sahibi; Paket 2'de requirePermission takılır.
>     - Firma eşleme: suppliers üzerinden ad benzerliği (basit normalize + ILIKE), otomatik atama
>       YOK, öneri + insan seçer (OFS-05 deseni: öneri kilit değildir).
>     - YZ-02: yapay zeka istemcisi yalnız şirket hesabının kimliğiyle (users satırı, is_ai bayrağı
>       YOK — Paket 2'de ayrı "servis kullanıcısı" kararı; şimdilik Owner token'ı).
>     - Ekran: ui2 "Bekleyen gider taslakları" — eksik alanlar kırmızı, tedarikçi önerisi seçmeli,
>       Kabul/Ret.
>     - Kütük: LED-19 "yapay zeka giderde yalnız taslak yazar; gider insan kabulüyle doğar (YZ-01 +
>       LED-08 birlikte)".
>   - **P1b-3 tabanı (ölçüldü):** [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU] → "P1b-3 tabanı" (5 madde).
>   4) ~~**Paket 2 — kullanıcı yönetimi**~~ (davet, aktif/pasif, yetki matrisi çekirdeği) — **KAPI-2** (auth);
>   kriterler (Sentez 21 Eki + EK 21 Eki + 22 Eki GO) → ✅ STAGING'E HAZIR (`ce670ab`) → ✅ staging 043–045 + P2-5 →
>   ✅ MAIN'E MERGE (`b75c87b`) → ✅ **CANLIDA (22 Eki 14:01, KAPI-1 geçti)**; aynı dalda Suppliers + Drafts alt menüye
>   (K-G kuralıyla); ✅ belge kapanışı **KB @ 7a2d9fd**. **Açık:** YET-01..09 🔶 Sentez teyidi (kapanış brief'i 22 Eki) ·
>   Yaprak'ın eski girişi ölçülmedi.
>   **★ SIRA (Suer 22 Eki — bu kazanır):** **UI-0** (✅ STAGING'E HAZIR — LEENA `1ad8456`, [defter:2026-10-22 PAKET UI-0] → ✅ **MAIN'E MERGE** (`cb37f24`,
>   canlı sırası Suer'de) — [defter:2026-10-23 PAKET UI-0 MERGE];
>   ✅ kriterler geldi — Sentez 22 Eki, SERBEST, dal `eliza-next`;
>   kütük UI-01..06 + `ELIZA_UI2_ARAYUZ_KURALLARI_v1.md` — [defter:2026-10-22 UI-0 KRİTERLERİ]; girdi: SAYFA ENVANTERİ
>   [defter:2026-10-22 SAYFA ENVANTERİ] + UX çıktısı) → **Faz B başı** (Anthropic API anahtarı iptal/yenileme + LIFFY `JWT_SECRET`, K-E) →
>   **Paket 3**. P1b-2 Zoho CSV gelince araya girer (değişmedi). **Eklemeler (Sentez EK 21 Eki — tarihsel):**
>   - P2-2 sırası: ÖNCE modül + kapsam (own/team/office/all), 5 profil; ALAN gizleme bu pakette YOK — tek
>     istisna sonraki dilim: komisyon alanları (oran/hak ediş), Sales profili görmez; şimdi yalnız kaydı:
>     permissions'a "field" eylemi eklenmez, tablo genişletilebilir kalır.
>   - SAT-04 yuvası: bölge yasağı yetki çözümlemesine GİRDİ — scope=office/team çözülürken bölge tablosu okunur,
>     koda bölge gömülmez (S-16r); tablo Paket 3'te (LIFFY tarafı); Paket 2'de `utils/permissions.js`'de
>     "bölge filtresi" yuvası boş ama tanımlı (ikinci yeniden yazım gerekmesin).
>   - YZ-03 bot notu: eliza-legacy botu bugün Zoho aynasını doğrudan okuyor; yeniden yazıldığında API
>     istemcisi olur — Paket 4/5, şimdi aksiyon yok.
>   5) **Paket 3** — REQ amendment 2026-10-21'i GİRDİ alır (2.1 kazanım hattı + SAT-01..04, 2.4 katalog);
>   SAT-04 tablosu burada (LIFFY tarafı). Girişte süzgeç (doğrulama + mükerrer) Paket 3 SONRASI, boru hattıyla
>   (Suer teyidi bekleniyor). Önceki ★ satırındaki "katalog/quote (LIFFY aktivasyon)" ile ilişkisi Sentez'de.
>   6) **Zoho göçü + raporlama** + **rapor modülü (Zoho tarzı) + genel arama** (REQ 2.8 / 3.7, amendment
>   2026-10-21).
>   **Sentez kuyruğu:** olay kaydı (B6) sırası — Faz 4 kalan mı, ayrı paket mi (SAT-03, eşikli uyarılar, Owner
>   aktivite ekranı buna bağlı) · REQ/YZ-03 "Package 1 criterion" ↔ EK çelişkisi (KB okununca) · gelir
>   kategorisi → ledger income bağlantısının paketi (hüküm 21 Eki: tek kategori "Contract revenue") · iade +
>   kredi bakiyesi R11 Paket 3 sonrası · ~~Paket 1b soruları (22 Eki)~~ → ✅ cevaplandı 22 Eki (LED-18/20/21
>   teyitli · tohum Zoho adıyla · gelir 15 · alt menü (K-G kuralıyla) · export → YON-12) — [defter:2026-10-22 PAKET 1b BELGE
>   KAPANIŞI].
>   **Tasarım fazı kuyruğu (Sentez 22 Eki):** UI düzeni (sayfa içi bağlantılar menüye — iskelet sonrası) · sayfa
>   geçiş yavaşlığı (ölçülecek).
>   Paralel/sonda: v402 temizlik sayımı (L-1 sonrası) · em-dash · test zinciri · `PRE_MIGRATION_CURRENCIES`
>   yedeğinin kaldırılması (040 canlıda).
>   **Faz B kuyruğu (zaman: Paket 2 SONRASI, Paket 3 ÖNCESİ — Sentez 22 Eki):** **ÖNCELİKLİ (21 Eki oturumunda
>   parçaları çıktıya düştü):** Anthropic API anahtarı
>   iptal/yenileme (LIFFY `settings.local.json`'dan sızdı) · LIFFY `JWT_SECRET` (K-E) → sonra: 3 izlenen
>   `.env.backup` · staging DB inbound
>   `0.0.0.0/0` daraltma · sırlı ölü izin kuralları · NOLOGIN kalan eski roller + tablo sahipliği (Sentez sorusu) ·
>   auto-deploy'un `35cad76`'da tetiklenmeme sebebi (Render event log'dan ölçülecek; Sentez 21 Eki; `613ce8e`'de
>   tetiklendi, 22 Eki) ·
>   Render CLI yenileme (oturum 2026-06-17'de düştü; worker logları okunamıyor; Sentez 21 Eki).
>   Takvim: eski `/login.html` emekliliği en erken 2026-11-20 (SEM-05).
> - **TEK YOL HARİTASI (2026-10-19) — TARİHSEL:** 1) Faz A ✅ (21 Eki) · 2) dilim 2 ✅ (21 Eki CANLIDA).
>   1) Faz A (export + DB şifresi + LIFFY DB + JWT; A4 yok) → 2) dilim 2 (merge, push, 033 + 034 +
>   ad kolonu — üç dosya, Suer koşar; ilk-şifre script'i; ui2 login / "kim girdi" görsel onay) —
>   **1 ve 2 aynı gün, arka arkaya; 1 önce** → 3) Faz 4 kalan: kullanıcı yönetimi ekranı (davet,
>   aktif/pasif, yetki matrisi çekirdeği) → 4) Ledger L-1…L-6 → 5) katalog/quote (LIFFY
>   aktivasyon paketi) → 6) Zoho göçü + raporlama. Paralel/sonda: v402 temizlik sayımı (L-1
>   sonrası) · Faz B · em-dash · test zinciri. Fuar kilidi yok (19 Eki); tek kontrol status.render.com.
> - **GÜNCEL SIRA (2026-10-08) — TARİHSEL (2026-10-19 yol haritası önceliklidir):**
>   1) ~~ui2 liste ekranı: push + Suer görsel onayı.~~ → ✅ KAPANDI (2026-10-08).
>   2) Kenya haftası (kâğıt, LEENA'ya dokunmadan): rotasyon runbook'u Faz A · Faz 4 dilim 2
>      tasarımı · ölçümler (TEST OFFICE, schema_migrations 030-032 planı, ell-docs
>      leena/CLAUDE.md farkı) · ledger ön-ölçümü. **Sıra (8 Eki): ~~2d ledger ön-ölçümü~~ ✅
>      (+ LEDGER KRİTER HÜKÜMLERİ işlendi) → v402 temizlik sayımı.** ~~Mail limiti belge borcu~~ ✅.
>      Faz 4 dilim 2 dalda YAZILDI (`faz4-dilim2`: `49fa217` + `3d9896a` + `a67ab0f` SEM-05 hizalama; `name` Sentez kararı bekliyor).
>   3) 16 Eki+: Faz A rotasyonu (A4 düştü — eliza-legacy kalır) → Faz 4 dilim 2 kapanışı
>      (merge + push + 033 + 034 + ilk şifre + ui2 görsel onay) → **Ledger L-1…L-6 (dilim 2
>      sonrası, her biri ui2 ekranıyla)** → katalog/quote.
>   Bekleyen: em-dash · test kapsamı · package.json zinciri · Faz B.
> - **Açık kuyruklar (2026-10-08 eklendi):**
>   - Temizlik listesi: TEST OFFICE (+1 agent) · contracts 1/3/4 birleşme. ⚠️ TABAN 342.00
>     contract 4'e bağlı (canlı çapa + ui2 detay varsayılanı; testler bağlı değil): yeni TABAN
>     çapası Sentez kararıyla belirlenmeden contract 4 silinmez/değişmez.
>   - v402'den devralınan temizlik (yalnız çıkarma, yeni ekran yok; Kenya sonrası, SIEMA
>     penceresi): kopya mail kapıları, ölü kampanya sayfası, fuar numarası gömülü 10 dosya.
>     Önce Orchestrator sayımıyla kapsam → Sentez onayı → dilimler.
>   - 030/031 test DB durumu: **KAPALI (bilinçli dışlama)** — setup 012–028 + 032 koşar,
>     030/031 DIŞLA-listesinde, bunlara dayanan finans testi yok. Açık kalan ayrı konu:
>     029–032'nin canlı `schema_migrations` kaydı (plan Kenya haftası kâğıdı).
> - **Açık kuyruklar (2026-10-08 Sentez kapanışı):**
>   - Faz B: LIFFY `JWT_SECRET` (K-E — fallback temizliği + env yoksa başlama, YON-08) ·
>     Zoho/Twilio anahtarları.
>   - eliza-legacy kapatma: birleşme sonrası, yeni sistem aynı cevapları verince.
>   - Rol/yetki dilimi: `/me` eski-token 409 köprüsü yeniden ele alınır · şifre ≥6 → SaaS
>     ölçüsü (YON-07).
>   - ~~Belge borcu (Kenya kâğıt listesi): LIFFY kullanıcı başına mail limiti gereksinime
>     "mevcut davranış" olarak yazılır.~~ → ✅ REQ amendment 2026-10-08.
>
> *(Aşağıdakiler önceki adaylar — tarihsel, 2026-10-19 tek yol haritası önceliklidir.)*
>
>   - **★★ TEST DB SENKRONU (ACİL):** `setup_test_db.js` 012→028 kuruyor,
>     029/030/031/032 girmiyor → 117 test var olmayan şemayı doğruluyor.
>     Yalancı yeşil. Faz 4 dilim 2'den ÖNCE çözülmeli.
>   - **FAZ 4 DİLİM 2:** JWT'ye `user_id` + `name` · **şifre belirleme akışı**
>     ⛔ **4 EKİM'E KADAR KİLİTLİ** (fuar: Siema 22-24 Eyl, Madesign 1-3 Eki). Açılış: ölçüm + inşa AYNI TURDA, önceki ölçüm bayat sayılır.
>     (bootstrap açığı) · `ui2CurrentUser()` senkron kalacak.
> - **★ ui2 SONRAKİ FINANCE EKRANI (Contract kuruldu 2026-09-09):** oran tablosuna göre 2.
>   en yüksek Commissions (~33%, statement'la ~50%) — ama önce **backend iş kuyruğu** (contract-level
>   commission total · line-item amount/EUR · payments type/status) hangi ekranı açar? Her ekran
>   ayrı ölçülür (mockup ≠ endpoint, YON-05). Backend önkoşulu sürüyor: `users` + rol matrisi
>   (`ui2CanSee`/`ui2RenderSubnav` bugün TRUE; gerçek cevap Faz 4).
> - **★ SATIŞÇI EŞİĞİ (ölçüldü 2026-08-04):** LEENA `users` tablosu ·
>   rol/yetki gate · user→agent/office bağı. Üçü zincir, ilk halka `users`.
>   ⚠️ Faz 4 "en sona" kilidiyle ÇELİŞİYOR — karar Suer'de.
> - **CONVERT canlı transport** (LIFFY→LEENA otomatik): bugün payload-driven.
> - **LIFFY DB ölçümleri** (katalog/quote/canonical_expo_id/users doluluğu):
>   Render Shell'den koşulacak, psql blokları hazır.
> - ~~**★ PAYOUT dilimi** (ayrı, gelecek): fiilî agent ödemesi bir **OLAYDIR** — kaydı/ledger'ı bu
>   dilimin işi; **`commissions` tablosu ancak o zaman doğar** (Sentez-1). Clawback/adjustment
>   semantiği de payout masasında. *(Komisyon motoru M1/M2 tamam — `5c7ccfd`/`320f00f`/`f28e6a6`;
>   hesap türetiliyor, ödeme henüz kaydedilmiyor.)*~~ → ✅ **P1 KAPANDI (2026-07-27, 025 +
>   `3ab2dac`).** KALAN: **P2 — payout UI iskeleti** (agent statement ekranı, İngilizce, cila yok).
>   → ✅ **P2 de KAPANDI (2026-07-27, `ab8a6d9`).**
> - ~~**payment schedule** — 3a kuyruğundan kalan (plan ≠ gerçekleşen; req `:509-511`, `:564`).~~
>   → ✅ **PS1 KAPANDI (2026-07-28, 026 + `fa7f288`).** KALAN: **PS2** — schedule UI kartı
>   (contract-detail) · ofis yönetim ekranı · "Reference Data" sayfası · nakit öngörü raporu
>   (ofis × para birimi × vade) · ödeme↔kalem eşleştirme.
>   → ✅ **PS2 KAPANDI (2026-07-28, 027+028; `dc00354`/`e2db297`/`e289c7d`/`fd516e4`).**
>   KALAN: **PS3 — nakit öngörü raporu (ofis × para birimi × vade kırılımı — ASIL ÖDÜL)** ·
>   ofis yönetim ekranı (ekle/kapat, Iraq kararı) · Reference Data admin sayfası ·
>   ödeme↔kalem eşleştirme (S-6) · schedule UI kartı (contract-detail) · agent formunda
>   ofis düzenleme.
>   → ✅ **PS3-A KAPANDI (2026-07-28, `87d162d`).** KALAN: ~~**PS3-B — nakit öngörü raporu
>   (ofis × para birimi × vade kırılımı — ASIL ÖDÜL; iki yön de artık kayıtlı, önkoşul
>   tamam)**~~ → ✅ **PS3-B CANLIDA (2026-07-30, `4362054`/`ca6fb3c`/`430e08d`).** · ~~ofis yönetim ekranı (ekle/kapat)~~ → ✅ **CANLIDA (2026-08-04, `3ebe8b5`; Iraq veri girişi ayrı, açık)** · Reference Data admin sayfası ·
>   ~~**kural kütüğü (ELL_LOCKED_KARARLAR_OZET'e iş kuralları bölümü — S/H/W/U/D hükümleri
>   indekssiz birikiyor)**~~ → ✅ **KK1, 2026-07-29** · ~~ödeme↔kalem eşleştirme (S-6)~~ → ✅ **TAH-04 CANLIDA (2026-08-03, `e83b805`/`3d0caef`/`32131d1`)** · ~~agent formunda ofis düzenleme~~ → ✅ **CANLIDA (2026-08-04, `ff080fb`)** ·
>   ~~**D-1 schedule-default ön-doldurma görsel borcu**~~ → ✅ **contract 4 expo bağlama, 2026-07-29**.
>   → ✅ **BELGE KONSOLİDASYONU KAPANDI (2026-07-28, `4278bc8` + `1f53fb6`).**
>   AÇIK: ~~**KB yeniden yükleme (c44ffeb'de donmuş)**~~ · ~~**FAZ1a_DURUM.md KB'den indirilecek**~~ ·
>   ELL_RULES ⛔ÖLÜ'ye çekilsin mi · yol haritası :50 kanıt zincirine dosya adları eklensin mi ·
>   ~~**KK1 kural kütüğü (evi artık belli: ELL_LOCKED_KARARLAR_OZET.md repoda)**~~ → ✅ **2026-07-29**.
> - **Belge güncelleme borcu:** `archive` B3 v1.0/v1.1 → S7 v1.2 (belge dilimi).
> - ~~**⚠️ DURAN BORÇ (KORUNUYOR):** `ELL_YOL_HARITASI_v5` + `ELL_BILGI_MIMARISI` hâlâ LEENA-native
>   karara (finans/komisyon LEENA'da; ELIZA marka/Finance-tab) göre **güncellenmedi**.~~ → ✅
>   **KAPANDI (2026-07-27, `55c07ff`):** rol daraltması yapıldı; borcun "mimari dil güncellenmedi"
>   varsayımı ölçümle çürütüldü (zaten güncelmiş). Bkz. 2026-07-27 kaydı.
> - **Ucuz iyileştirme kuyruğu — kur-yönü ipucu (DURUYOR, ihtiyaç 2 kez doğrulandı):**
>   add-payment formunda `exchange_rate` alanına yön ipucu. Bir sonraki UI dokunuşunda yapılır.

> ---
>
> **Bu nedir:** ELL projesinde yapılan her şeyin, karşılaşılan sorunların ve açık
> kuyrukların tek kaydı. Faz başına ayrı belge YOK — her şey burada.
> **KAYIT SIRASI = KRONOLOJİK-ARTAN:** en YENİ kayıt, `★ SIRADAKİ ADAYLAR` bloğundan ÖNCE,
> dizinin SONUNA girer. (Eski "en üstte en güncel" ifadesi YANLIŞTI — düzeltildi 2026-07-29;
> KK1'i yanlış yönlendirmişti.) Durumu buradan gör.
>
> **Pusula:** `ELL_YOL_HARITASI_v5.md` (canonical roadmap — çelişkide o kazanır; v4 superseded).
> **Kontrol listeleri:** `ELAN_EXPO_REQUIREMENTS_v1_0.md` (ne lazım) +
> `ELL_LOCKED_KARARLAR_OZET.md` (mimari uyum). Öneri üretmeden önce bu ikisi okunur.

Son güncelleme: **2026-06-19 (MİMARİ KARAR DEĞİŞİKLİĞİ):** ELIZA ayrı sistem/database olarak
**terk edildi**. `eliza_73du` üstündeki 026/027/028 convert çalışması **legacy/retired** — deploy
edilmeyecek. **Convert core LEENA'da yeniden kurulacak.** Expo eşleme artık "ELIZA 1227 vs LEENA 16"
problemi DEĞİLDİR; current convert için **LEENA canonical expo gerçek FK** kullanılacak. Tarihsel
Zoho expo/contract migration ileride **Zoho → LEENA** migration kapsamında ele alınacak.
*(Önceki "CONVERT ÇEKİRDEK bitti [eliza 026/027/028] / üç expos kopuk / eşleme LIFFY-aktivasyon önkoşulu"
notu SUPERSEDED — aşağıdaki CONVERT GATE bölümü yeni karara göre düzeltildi.)*

---

## NEREDE KALDIK — TEK CÜMLE

**Ticari çekirdek + KOMİSYON MOTORU canlıda (2026-07-25):** quote → convert (+`line_items`) →
contract → payment → reversal → transfer → hesaplanan paid/balance + `commissionable_base`
**+ komisyon motoru** (M1 contract görünümü `earned/full` + M2 kesim-dönemi raporu
`/api/commissions` — tavan + reversal + cancelled mühürlü). **FAZ 3A + 3B TAMAM** (migration
**016-024** + komisyon motoru **M1/M2 canlı, migration'sız** — tamamen türetilmiş/D2; hepsi E2E
kabul aldı). **Sıradaki: ~~PAYOUT dilimi~~ → ✅ P1+P2 KAPANDI (2026-07-27); kuyrukta değildir.** (fiilî agent ödemesi = olay; `commissions` tablosu ancak
o zaman doğar — Sentez-1) ~~**+ governing doc borcu** (`ELL_YOL_HARITASI_v5` + `ELL_BILGI_MIMARISI`
hâlâ LEENA-native karara göre güncellenmedi)~~ → ✅ governing-doc borcu **KAPANDI (2026-07-27,
`55c07ff`)**; kuyrukta değildir (bkz. 2026-07-27 kaydı). **Convert-1 + LIFFY aktivasyonu ertelendi** (L3:
`line_items` + satır-varken-currency LIFFY önkoşulu). Sonraki: audit/kimlik (Faz 4), transport
(LIFFY aktivasyonu). Birleşme bitene kadar sistemleri kimse kullanmıyor (tek kullanıcı Suer).

*(Önceki hâli — 2026-07-24, "Sıradaki: KOMİSYON MOTORU" — motor M1/M2 canlılaştığı için geçersiz;
blok kayıtları yukarıda duruyor. Ondan önceki 2026-06-20 "Convert-1" hâli de superseded.)*

*(Aşağıdaki tarihsel notlar — "Convert gate tasarımı kilitlendi", eski Faz 2 ölçümü — bu oturumda
İNŞAYA döküldü ve canlılaştı; tasarım kayıtları referans olarak korunuyor.)*

**CONVERT GATE TASARIMI KİLİTLENDİ (2026-06-18).** 6 karar locked-uyumlu kilitlendi (yetki =
ayarlanabilir permission, sabit rol değil; contract tek tablo LEENA DB'sinde, handoff Akış A
LINK/CREATE, review-queue türetilmiş liste state'siz, cross-DB tek sınır LIFFY↔LEENA, expo
seçimi LEENA aynı-DB FK). **KRİTİK kilitli gerçek: ELIZA ayrı sistem/DB DEĞİLDİR; ELIZA tab =
LEENA Finance. Contract fiziksel olarak LEENA DB'dedir.** Tek cross-DB sınır LIFFY↔LEENA. Ertelendi (bilinçli):
#5 transport mekanizması, Akış B (signed-quote'suz contract + fuzzy-match linkage), Zoho migration
(EN SON). Detay + bu oturumun dersi (locked/req > canlı ölçüm > eski belge, 4 kez düzeltildi) aşağıda
"CONVERT GATE TASARIMI". **Sıradaki: Convert inşa dilimleri** (Expo'daki dilim-dilim disiplini) —
ilk muhtemelen contract tablosu + locked sales_agents + leads/contacts/companies. İnşa sırası sıralı
modda konuşulacak. Test fixture hazır: ATR-100000 (signed quote).

**Test kayıtları — canlıda BİLİNÇLİ bırakıldı (demo/deneme için):** Smoke test sırasında
oluşan test expo'ları (id 15 `test`, id 16 `test` klonu, id 11 `[TEST] Reactivation Smoke
Test Expo`, `Mega Clima Ghana 2026 (Test)`) ŞİMDİLİK SİLİNMİYOR — Suer hem Yaprak'a modülü
gösterirken hem kendi denemeleri için bunları kullanıyor. Demo/deneme aşaması bitince
silinecek (DELETE Suer'in terminalinden, Claude Code'a canlı read-only). Silmeden önce id 11
+ Ghana kaydı doğrulanmalı (created_at + bağlı veri — gerçek fuar olabilir, körlemesine
silinmeyecek); id 15 + 16 kesin test.

---

## ★ STRATEJİK ÇERÇEVE (2026-06-15 netleşti) — "BİRLEŞMEYE KADAR KİMSE KULLANMAZ"

Suer'in net kararı: **LIFFY ve LEENA Finance/ELL birleşimi, ELL birleşmesi tamamlanana kadar
canlı kullanıma AÇILMAYACAK.** Tek kullanıcı Suer (+ asistanı). Sonuçlar:

1. **"LIFFY satışçıya açılma" = birleşme.** Eskiden defterde "freelancer'a açmadan önce"
   diye geçen her önkoşul, aslında BİRLEŞME anına bağlı. Öncesinde acil değil.
2. **Tüm güvenlik kalemleri → "birleşme güvenlik paketi"** (aşağıda tek liste). Bugün
   kurulumu/işleyişi ENGELLEMEYEN hiçbir güvenlik işine takılmıyoruz; basit/anlık
   çalışma hızlandırıyor. Birleşmede topluca: şifre rotation + güvenlik geçişi.
3. **242 SKU catalog import'u → birleşmeye ertelendi.** Fiyatlar bayatlamasın diye tek
   seferde, birleşmede aktarılacak. (Eskiden "quote'u açmanın ön şartı"ydı; artık değil.)
4. **Env/secret değerlerini Suer kendi terminalinden/panelinden girer**, chat'e yazılmaz.
   Bugün ELIZA env'leri (JWT_SECRET, CORS_ORIGINS, TWILIO_AUTH_TOKEN) böyle girildi.

### ▼ BİRLEŞME GÜVENLİK PAKETİ (tek liste — birleşmede topluca yapılacak)
Aşağıdakilerin hiçbiri bugün kurulumu/işleyişi engellemiyor; birleşme anında tek
oturumda toplanacak. (Detaylı gerekçeler ilgili faz bölümlerinde.)
- [ ] **LIFFY:** JWT dev-fallback `liffy_secret_key_change_me` (31 dosya) → boot-guard
      (ELIZA'da yapıldı, LIFFY'de yapılacak); CORS daralt; secret rotation.
- [ ] **LIFFY DB:** `liffy_user`→`liffy_user_v2` rotation tamamla (servisler v2'ye
      geçmeden eski'yi SİLME); IP kısıtı `0.0.0.0/0` daralt; oturum çıktılarında görünen
      şifreler değişecek.
- [ ] **LIFFY DELETE eşitleme:** campaigns/lists/mining jobs/results tekil DELETE'lerine
      1a deseni (rol-kapısı + reason + audit + scope) ekle. (Ölçüm: bugün eksik, baypas
      riski yok ama açılmadan eşitlensin.)
- [ ] **Eski ELIZA (terk edildi — 2026-06-19):** erişilebilir kalacaksa minimum auth korunur
      (create-user/set-password rol-gate); **kapatılacaksa launch blocker DEĞİL**. Repo
      private/archive olabilir; DB read-only backup/dump. **Yeni launch güvenliği = LEENA
      Finance permissions + LIFFY izolasyonu.**
- [ ] **GitHub:** repo public/private kontrolü (LIFFY/ELIZA). Secret repoda yok (.env
      hiç commit'lenmemiş), public kalmasının bugünkü maliyeti sadece iş-mantığı
      görünürlüğü; yine de açılmadan private yapılacak.
- [ ] **Kullanıcı-ofis atamaları:** 25 kullanıcıya `users.office_id` (UI'da Products &
      Pricing → Users & Offices).
- [ ] **242 SKU catalog import** (birleşmede tek seferde — fiyat bayatlamasın).
- [ ] **Test fixture temizliği:** ATR-100000 + QMA-100001 raporlama canlıya çıkmadan SQL
      ile silinecek (signed API'den silinemez; sequence SIFIRLANMAZ).
- [ ] **Audit log** = sistem geneli "kim/ne/ne zaman" = **LIFFY + LEENA** (iki sistem tek arayüz);
      **Finance audit LEENA içinde yüksek öncelik**. *(eski "üç sistem" ifadesi düzeltildi.)*

---

## ★ UI/TASARIM STRATEJİSİ (2026-07-21, Suer kararı)

Mevcut LEENA/ELIZA arayüzleri **GEÇİCİ İSKELEDİR** — nihai ürün bu görünüm ve kullanımla
**YAYINLANMAYACAK.** Teknik/backend inşa bittikten sonra ayrı ve ciddi bir UI/UX + tasarım
fazı yapılacak (Claude Design'da ilk denemeler mevcut). Sonuçlar:

1. **İnşa dilimlerinde UI minimum iskelettir** — liste/form çalışsın yeter, cila ve görsel
   iyileştirme **YAPILMAZ**, buna harcanan efor israftır.
2. **UI eleştirisi inşa dilimi konusu değildir.**
3. **Backend/API'ler UI-bağımsız tasarlanır** ki tasarım fazında arayüz komple değişebilsin.
4. **Tasarım fazı roadmap'e ayrı faz olarak girecek** (yeri birleşme sonrası netleşir).

**NAVİGASYON BORCU (2026-07-23, Suer):** LEENA'nın "login → önce expo seç" akışı yaka-kartı
geçmişinin kalıntısı — ELL'in nihai akışı **DEĞİL**. Nihai akış: login → **organizer-level ana
panel** (finans, contracts, agents, raporlar — expo'suz) → expo-level işlere oradan dalınır.
Veri modeli ve API'ler **zaten organizer-level** (contracts/payments/agents expo'suz çalışıyor,
ölçülü) — değişecek olan yalnız **kabuk/navigasyon**. Tasarım fazının **İLK maddesi**. İnşa
dilimlerinde bu akışa uygun API tasarımına devam (**expo_id opsiyonel kalır, zorunlulaştırılmaz**).

---

## ★ EXPO OPERATIONS MODÜLÜ — TAMAMLANDI + CANLIDA ✅ (2026-06-18, smoke test geçti)

> **İNŞA İLERLEME:**
> - ✅ ADIM 1 READ-ONLY ölçüm bitti (2026-06-16). Bulgular: expos tablosu var (id int,
>   16 kolon, 14 satır), tasarım alanlarının çoğu eksik. expo_clusters LEENA'da YOK /
>   ELIZA'da VAR. expo_partners YOK. users tablosu YOK (tek kimlik organizers) → operation
>   team kararı bu yüzden değişti (aşağıda). Floor plan clone: routes/floorplan.js:326
>   (version-level). Son migration 009 → yeni 010.
> - ✅ ADIM 2 migration 010 **CANLIYA UYGULANDI** (2026-06-16). Dry-run + idempotency +
>   FK/CHECK doğrulaması geçti, sonra Suer canlıya uyguladı. expos 16→43 kolon (+27),
>   expo_clusters + expo_partners + **core_countries + core_sectors + expo_sectors
>   junction** yaratıldı. Dosya: migrations/010_expo_operations.sql.
> - ✅ Seed 011 **CANLIYA UYGULANDI** (2026-06-16): migrations/011_seed_reference_data.sql
>   — 230 ISO ülke + 26 sektör. (Ayrı dosya — bkz. aşağıdaki içerik-filtresi notu.)
>   - **Teknik karar (a) DÜZELTİLDİ — sectors/country REFERANS TABLOSU (TEXT[] DEĞİL):**
>     country_code → core_countries(code) FK; sektör → expo_sectors junction (array
>     DEĞİL — array-element FK yok, referans bütünlüğü için junction ŞART). city/venue
>     serbest text (açık küme). Currency LEENA expo'da YOK (LIFFY'nin konusu). [Önceki
>     "TEXT[]/serbest text" kararı referans bütünlüğünü kaçırmıştı; bu daha doğru.]
>   - Teknik karar (b): 8 deadline = NULLable DATE + COALESCE(override, start_date−offset)
>     deseni (NULL=hesapla, dolu=Yaprak override). İki-seviyeli override tek desende.
>   - created_at = TIMESTAMPTZ (LEENA konvansiyonu; ELIZA düz TIMESTAMP ama LEENA içi
>     tutarlılık > iki-DB eşleşme, zaten senkron yok).
>   - Dokunulmadı: location (legacy kaldı, zero-data-loss), actual_visitors (kolon yok,
>     COUNT'tan), users FK yok.
> - ⚠️ **İÇERİK-FİLTRESİ NOTU (önemli, tekrar olabilir):** Uzun ISO ülke listesini (~230
>   isim) Claude Code'a yazdırırken "API Error: Output blocked by content filtering policy"
>   alındı — uzun ülke/bölge ismi listesi Anthropic içerik filtresini YANLIŞ tetikledi
>   (false positive), "tekrar dene" de aynı hatayı verdi (bağlama gömülüydü). ÇÖZÜM: yapı
>   migration'da (boş tablo), uzun seed AYRI dosyada hazır SQL olarak elle uygulandı.
>   KURAL: Claude Code'a uzun isim/veri listesi YAZDIRMA → ayrı seed dosyasında ver.
> - ✅ ADIM 3 ÖLÇÜM bitti (2026-06-16, tek seferde tüm dilimler, file:line kanıtlı).
>   Bulgular: routes/expos.js (424 satır) zaten var — GET list/:id/slug, POST/PUT/DELETE,
>   /:id/stats. Auth: middleware/authMiddleware → req.organizer_id, her endpoint WHERE
>   organizer_id scope'lu. DB: pg Pool, pool.query, ORM yok. Clone transaction deseni:
>   floorplan.js:327 pool.connect()+BEGIN+finally{release()}. En temiz CRUD örneği:
>   routes/exhibitors.js. Frontend: public/*.html vanilla JS (fetch+Bearer token);
>   en temiz form expo-create.html (380 satır), en temiz liste dashboard_new.html.
>   Mevcut UI'da AZ Türkçe var (expo-create.html:147 "Fuar" vb) → yeni ekranlar tam
>   İngilizce, mevcuda dokunma. Seed canlıda: core_countries=230, core_sectors=26.
>   - **KARAR (tarih otomasyonu yeri): SQL SELECT'te COALESCE** — actual_visitors COUNT
>     deseniyle birebir tutarlı (LEENA'da türetilmiş alan SELECT'te response'a eklenir).
>     Her GET: `COALESCE(payment_deadline, (start_date − payment_deadline_days_before *
>     INTERVAL '1 day')::date) AS payment_deadline_effective` — 8 deadline için. NULL
>     override→offset'ten hesapla, dolu→onu kullan. `_effective` suffix ayrımı görünür.
>   - **KARAR (clone floor plan version): sadece AKTİF version → yeni draft** (clear_
>     assignments=true, boş satış başlar). Tüm version geçmişi kopyalanmaz.
>   - **KARAR (clone cluster_id): NULL başlat** (tasarımla aynı — eski cluster eski
>     tarihli, yeni edition bağımsız başlar, Yaprak gerekirse yeni cluster'a bağlar).
>   - **KARAR (dropdown endpoint yolu): `/api/reference/countries` + `/api/reference/
>     sectors`** — global referans (expo'ya özel değil, organizer filtresi yok); expo
>     altına gömülmez (ülke listesi expo'nun alt-kaynağı değil; LIFFY de kullanabilir).
>   - NOT: core_sectors 26 satır (tasarımdaki "8 sektör" örnekti); dropdown tabloyu okur,
>     26 gösterir. Sektör listesi sonra gözden geçirilebilir, inşayı bloklamaz.
> - ✅ **DİLİM 1-2-3 İNŞA + LOKAL TEST BİTTİ (2026-06-16). PROD'A PUSH YOK (biriktiriliyor).**
>   - **Suer kararı (deploy stratejisi):** Görsel/screenshot onay adımı ATLANDI (UI sistem
>     bütünüyle bitince komple değişecek, ekran-ekran onay oyalanma). Claude Code lokal
>     yazılabilir test DB'ye karşı gerçek route kodunu test eder (endpoint JSON doğru mu,
>     _effective matematiği doğru mu, sözdizimi temiz mi), geçince dilim tamam sayılır.
>     Her dilim AYRI deploy EDİLMEZ — kod commit edilebilir ama prod push'u 4 dilim
>     bütünüyle bitince TEK seferde. Gerekçe: sadece-ekleme (yeni dosyalar/endpoint'ler),
>     mevcut LEENA'ya/Yaprak akışına dokunulmuyor → biriktirmek güvenli. Tek istisna: bir
>     dilim mevcut LEENA'yı etkileyecek olursa (mevcut tablo/endpoint değişimi) DUR ve SOR.
>   - **Dilim 1 (Okuma) ✅:** routes/expos.js GET / genişletildi (27 kolon + country join +
>     opsiyonel filtreler role/status/country/year, organizer_id scope korundu). GET /:id
>     genişletildi (8 deadline _effective COALESCE + sectors json + cluster/country join).
>     routes/reference.js YENİ (GET /api/reference/countries 230 + /sectors 26, global,
>     organizer scope yok). public/expo-list.html YENİ (İngilizce, filtre barı, tablo,
>     status renkli badge). **Geriye-uyumluluk KANITLANDI:** minimal 4-alanlı POST hâlâ
>     default'larla çalışır, response sadece alan EKLENDİ (çıkarılmadı/yeniden adlandırılmadı)
>     → mevcut tüketiciler kırılmaz. NOT: POST artık `RETURNING *` ham satır dönüyor (43
>     kolon) — bugün tüketici yok, sorun değil; ileride gizli tutulması gereken bir kolon
>     eklenirse otomatik sızar (bilgi notu, aksiyon değil).
>   - **Dilim 2 (Yazma+otomasyon) ✅:** POST/PUT genişletildi (WRITABLE_FIELDS + sectors
>     junction + transaction + enum/FK validation + nn() empty→null + mapWriteError; PUT
>     dinamik update + override temizleme). public/expo-form.html YENİ (İngilizce create/edit,
>     Identity · Sectors multi-select · canlı deadline otomasyonu start/end+8 offset → 8 auto
>     tarih override edilebilir · Form URLs · actual_visitors read-only). expo-list.html New
>     Expo + satır-tıkla → forma bağlandı. **Bulunan+düzeltilen bug:** form'un ilk halinde TZ
>     off-by-one (toISOString/slice UTC'ye çevirip +03'te tarihi bir gün kaydırıyordu);
>     backend doğruydu (SQL _effective kanıtlı), sadece client-side JS; lokal-bileşen tabanlı
>     TZ-güvenli helper'larla (fmtLocal/computeDate/dateOnly) düzeltildi. Lokal test: POST tam
>     expo+sectors+custom offset→201, GET _effective doğru (offset 45→Apr4, override korunuyor),
>     PUT offset değişti→yeniden hesap + override null→offset'e döndü, backward-compat minimal
>     POST→default'lar, validation bad status/country→400, cross-org PUT→404 (scope korundu) ✓
>   - **Dilim 3 (Clone) ✅:** POST /api/expos/:id/clone (transaction, pool.connect/BEGIN/
>     finally release) + bumpExpoName/yearOf helper. expo-list.html cloneExpo() bağlandı
>     (confirm → clone → yeni expo id ile forma yönlendir). expo-form.html boş-tarih amber
>     ipucu (clone-mode doğal boş-tarih durumundan algılanır, ekstra state YOK).
>     **Clone tarih kararı DÜZELTİLDİ:** edition_year +1 ve isimdeki yıl +1 (akıllı regex
>     replace) AMA start_date/end_date BOŞ gelir (kaynak +1 yıl DEĞİL — fuar tarihi yıldan
>     yıla öngörülemez kayar, "kaynak+365" yanlış varsayım; Yaprak gerçek tarihi girer). 8
>     deadline override de BOŞ (offset'ler kopyalanır dolu; Yaprak start/end girince 8
>     deadline o anda otomatik hesaplanır — "fuar tarihini gir gerisi kayar"ın clone hali).
>     Üç kategori: KOPYALANIR (organizer_role, sectors, country/city/venue, location/desc/logo,
>     8 offset, show_open_hours, partners, floor plan aktif version→draft atamalar sıfır);
>     BUMP (edition+1, isim regex+1, slug); SIFIRLANIR (start/end NULL, 8 deadline NULL, 3
>     form_url NULL, cluster_id NULL, status→announcement, stand commercial_status→available).
>     Lokal test (zengin kaynak: sectors+partners+cluster+floor plan): expo satırı tüm
>     kategoriler doğru, sectors+partners kopyalandı, floor plan yeni hall + sadece aktif
>     version→draft (archived atlandı) + cloned_from + stand'ler available + size_m2 trigger
>     yeniden hesap + cell kopyalandı, cross-org clone→404, form clone açılınca start/end boş
>     + amber ipucu + deadline'lar gri ✓
>   - **⚠️ BİLİNÇLİ TEKNİK BORÇ — Floor plan clone kopya-kodu (Dilim 3'te doğdu):** Floor
>     plan version-clone mantığı artık İKİ yerde: `floorplan.js` (inline, kendi route
>     handler'ında, floor plan'ın kendi version clone'u, export edilmemiş — floorplan.js:1135
>     sadece router export ediyor) + `routes/expos.js` (expo clone'un parçası). Dilim 3
>     ölçümünde floorplan.js'te yeniden kullanılabilir clone helper'ı BULUNAMADI → expo clone
>     zinciri (halls→aktif version→stands→cells) için mantık expos.js'te yeniden yazıldı.
>     **Bakım kuralı:** floor plan clone kuralı değişirse (cell kopyalama, "aktif version"
>     tanımı, stand status sıfırlama) İKİ yeri de güncelle; biri unutulursa floor plan clone
>     ile expo clone farklı davranır. **Neden şimdi çözülmüyor (Suer kararı):** ortak helper'a
>     (utils/) çıkarmak Yaprak'ın AKTİF kullandığı çalışan floorplan.js'e dokunmayı gerektirir
>     = "sadece-ekleme, mevcut LEENA'yı bozma" kuralını çiğner; kozmetik temizlik için canlı
>     floor plan'ı riske atmaya değmez. Borç gerçek ama küçük, kurallar sık değişmiyor, 25
>     kullanıcı/tek-tenant'ta kabul edilebilir. **Ne zaman:** ÜÇÜNCÜ bir tüketici çıkarsa
>     ortak helper'a çıkar — şimdi değil.
>   - **NOT (küçük, aksiyon değil):** Clone confirm'i tarayıcı native confirm() kullanıyor;
>     "yanlışlıkla klonladım"da geri dönüş yok (yeni boş expo oluşur) ama DELETE zaten var,
>     silinebilir. İleride UI komple yenilenince confirm akışı da düzelir.
> - ✅ **DİLİM 4 (Partner + Cluster CRUD) TAMAMLANDI + req 727 bağlandı (2026-06-18):**
>   - **Bölüm A (partners):** routes/partners.js YENİ — /api/partners?expo_id=X (flat +
>     query param, exhibitors.js deseniyle; nested DEĞİL — exhibitors flat kullanıyor).
>     GET/POST/PUT/DELETE. Scope expo üzerinden (expo_partners'ta organizer_id YOK → her
>     sorgu expos JOIN + organizer_id kontrolü). 11 rol enum validation, is_primary.
>     public/expo-partners.html YENİ (İngilizce, 11 rol dropdown, op-team istanbul_hq/
>     local_onsite turuncu badge — ayrı ekran YOK, rol seçimiyle).
>   - **Bölüm B (clusters):** routes/clusters.js YENİ — /api/clusters GET(expo_count'lu)/
>     POST/PUT/DELETE + GET /:id/expos (kardeşler). expos.js'e PUT /:id/cluster (bağla/ayır,
>     cluster_id NULL=ayır, organizer scope). cluster-delete önce expo'ları ayırır sonra
>     siler (expo'lar korunur). public/expo-clusters.html YENİ. expo-form.html'e Partners
>     butonu + Cluster bölümü (bağla/ayır + kardeş listesi).
>   - **req 727 (copy-to-siblings) — KARAR VERİLDİ + bağlandı:** Partner add formunda
>     "Copy to cluster siblings?" checkbox. Üç karar (Suer): (1) tetikleme = add-anında
>     checkbox, varsayılan İŞARETSİZ (bilinçli işaretlensin, otomatik saçılmasın); SADECE
>     cluster'lı expo'da görünür. (2) roller = SADECE stand_contractor/hostess/catering/
>     security (req 719'un birebir saydıkları); venue_authority HARİÇ (mekanın sahibi, Elan'ın
>     tuttuğu tedarikçi değil, kardeşler aynı venue'da zaten ortak); istanbul_hq/local_onsite
>     hariç (expo'ya özel). (3) çakışma = ROL BAZINDA atla (kardeşte o rolde herhangi partner
>     varsa o rolü hiç ekleme — rol+company değil rol bazında). Backend transaction'lı, kopya
>     is_primary=false. Lokal test 7 senaryo geçti (kopyalama/filtre/çakışma/copy=false/
>     cluster'sız/is_primary hepsi ✓).
>   - **DEPLOY (2026-06-18) — TEK PUSH, 4 dilim + 727 birlikte:** commit 335dacd (modül, 10
>     dosya: index.js + routes/{expos,reference,partners,clusters}.js + migrations/010 +
>     public/{expo-list,expo-form,expo-partners,expo-clusters}.html). git add . DEĞİL — sadece
>     bu modülün dosyaları (untracked .md analizleri + cleanup SQL'leri + seed 011 dışarıda
>     bırakıldı). **Push öncesi sadece-ekleme teyidi yapıldı (git diff):** index.js sadece 3
>     register ekledi (mevcut register'lar değişmedi); expos.js'teki "silinen" satırlar
>     GET/POST/PUT'un genişletilen eski gövdeleri (alan silinmedi/yeniden adlandırılmadı, POST
>     yanıtı superset'e büyüdü); DELETE/slug/stats dokunulmadı. Mevcut endpoint davranışı
>     değişmedi → push güvenli. Render otomatik deploy tetiklendi.
>   - **Seed 011 commit (2026-06-18):** commit 46a066f — migrations/011_seed_reference_data.sql
>     repo'da yoktu (canlıda elle uygulanmıştı), eklendi. Commit öncesi iki teyit: (1) 011
>     idempotent — 2 INSERT'in ikisi de ON CONFLICT DO NOTHING (countries→code, sectors→slug),
>     "safe to re-run". (2) Otomatik migration runner YOK — package.json'da migrate/build/start
>     script yok, migrate.js sadece initial.sql çalıştırıyor, render.yaml yok, index.js boot'ta
>     .sql çalıştırmıyor; numaralı migration'lar elle psql'den uygulanıyor. → "otomatik runner +
>     idempotent değil" riskli ikilisi yok, commit deploy'u kırmaz. Migration zinciri artık
>     repo'da tam (010 + 011).
>   - **✅ SMOKE TEST GEÇTİ (2026-06-18, Suer canlıda gerçek-veriyle):** Expo List 15 expo
>     kirli veriyle (country boş, status announcement) açılıyor, ÇÖKMÜYOR (en kritik test).
>     Filtreler çalışıyor (Year=2027 → 15'ten 2'ye düştü). Tarih otomasyonu DOĞRU (start
>     18.11.2026 → 8 deadline doğru offset'lerle, TZ kayması YOK canlıda da). Clone çalıştı
>     (id 16, edition+1, tarihler boş, amber ipucu, status announcement, offset'ler kopyalı).
>     Country dropdown 230 ülke + sektör 26 dolu (/api/reference/ canlıda çalışıyor). Partner/
>     cluster ekranları + form cluster bölümü çalışıyor. **Mevcut LEENA BOZULMADI** —
>     dashboard_new.html hâlâ çalışıyor, yeni form'la oluşturulan expo'yu okuyor (aynı tabloyu
>     paylaşıyorlar, sadece-ekleme kanıtlandı). Country listede "—" = bug değil (14 expo'ya
>     henüz country girilmemiş, yeni alan; form'dan seçilince dolacak).
>   - **TEST KAYITLARI — canlıda BİLİNÇLİ bırakıldı (demo/deneme):** id 15 (`test`) + id 16
>     (`test` klonu) KESİN test (Suer bu oturumda yarattı); id 11 (`[TEST] Reactivation Smoke
>     Test Expo`) + `Mega Clima Ghana 2026 (Test)` doğrulanacak (id 11 clone'dan önce vardı,
>     Ghana ismi gerçek fuara benziyor — created_at + bağlı veri kontrolü). ŞİMDİLİK SİLİNMİYOR
>     — Suer Yaprak'a gösterirken + kendi denemelerinde kullanıyor; demo bitince silinecek
>     (DELETE Suer'in terminalinden, Claude Code'a canlı read-only).
>   - **NOT (bug değil, ileride):** (a) Clone confirm hâlâ native confirm() — UI birleşmesinde
>     düzelir. (b) Yeni ekranlar mevcut LEENA ana menüsüne bağlı değil (sadece-ekleme gereği);
>     Expo List kendi sidebar'ı var (Expo List/Clusters/My Expos); Yaprak'ın erişim yolu UI
>     birleşmesinde netleşecek. (c) Floor plan clone kopya-kod borcu (aşağıda, bilinçli).
>
> ───────────────────────────────────────────────────────────────────────────────────
> **AŞAĞISI: İNŞA SÜRECİNİN DETAY KAYDI (tamamlandı, referans için korunuyor)**
> ───────────────────────────────────────────────────────────────────────────────────
>
> **Tasarım:** kağıt üstünde TAMAM (iskelet + alan yerleşimi + tarih otomasyonu + clone +
> üç yardımcı ekran). **Yer:** LEENA (roadmap Faz 4-5). Convert'in önkoşulu.
> **Ölçüm dayanağı:** requirements 667-766 (expo record + cluster + partner), 711
> (clone = floor plan clone expo-level), 833-913 (post-show analytics).

### Neden şimdi
- Convert gate'in önkoşulu: fuar sayfası convert'ten önce gelmeli (katı blok değil
  artık — defter "fuar sayfası convert ön şartıydı, artık değil" — ama tasarım sırası
  doğru).
- "Her şey expo-scoped" merkezi ihtiyaç; bu UI o mimarinin görsel kapısı.
- Quote (Faz 1f) bitti+canlıda (migration 050/051/052, 2026-06-12, gözle doğrulandı),
  yani sıra doğru.

### Üç ekran

**1. Expo List — giriş kapısı**
- Tüm fuarlar tek tabloda: ad · ülke · tarih(ler) · durum (announcement / sales-open /
  build-up / live / accomplished).
- Satıra tıkla → fuar detayına gir. Sistemin ana navigasyon ekseni burası.
- Üstte tek buton: **+ New Expo** (sıfırdan; sade/ikincil stil — nadir yol).
- Her satırda: **Clone** (öne çıkan/davetkâr stil — ASIL yol).
- Görsel öncelik: liste ekranına girince göz önce Clone'a düşmeli, New Expo'ya değil.
- Cluster'lar gruplu satır olarak render (requirements 895 — operasyonel birlik görünsün).

**2. Expo Form — TEK form, ÜÇ giriş yolu (create/edit ayrımı YOK)**
Aynı form + aynı backend endpoint; fark sadece "hangi veriyle pre-fill edildiği":

| Giriş | Form açılışı |
|-------|--------------|
| **Clone** (asıl) | Kaynak fuarın TÜM alanları + partner bağları + floor plan layout DOLU gelir. Yaprak sadece değişeni düzeltir (ad/tarih + gerekirse partner/layout). |
| **New Expo** (nadir) | Boş; sadece core alanlar görünür. |
| **Edit** (mevcut) | Tüm alanlar açık+dolu; partner ekle, tarih güncelle, durumu accomplished yap. |

- `actual_visitors`: formda **READ-ONLY**, LEENA'dan hesaplanan (COUNT), dokunulmaz.
  reported/şişirme alanı YOK (bkz. aşağıda "Bilinçli dışarıda").

**3. Partner Page — AYRI sayfa, AYRI tablo**
- requirements 738-766 + operation team. `expo_partners` tablosu: expo_id · partner_role
  ENUM (11 değer: stand_contractor/travel/visa/forwarder/hostess/catering/security/
  venue_authority/**istanbul_hq**/**local_onsite**/other) · company_name · contact_name ·
  phone · email · notes · is_primary.
- **istanbul_hq + local_onsite operation team rolleri (2026-06-15 kararı):** Operation
  team contact'ları AYRI expo alanı DEĞİL — partner tablosundan bu iki rolle gelir.
  Gerekçe: operation team her zaman Elan çalışanı değil, bazen operasyon freelancer'ı
  tutuluyor → stand_contractor gibi fuara-özel kişi/kurum, partner mantığına oturuyor.
  company_name: freelancer'sa o kişi/şirket, Elan çalışanıysa "Elan Expo"/boş. İsim/
  telefon/mail zaten partner tablosunda ayrı alan. requirements 698-701 "iç atama değil,
  iletişim bilgisi" niyetiyle tam uyumlu.
- Fuara buradan bağlanır/seçilir. Bir fuarda bir rolde 0/1/çok partner olabilir;
  is_primary = customer-facing iletişimde öne çıkan.
- **Çift amaç:** (a) welcome/operasyon maili partner bilgisini buradan OTOMATİK çeker
  (forwarder, stand contractor, local ofis — requirements 755-764 dinamik veri deseni),
  (b) ayrı tablo clone'u temiz tutar.
- Görünürlük: Project + Owner default; Sales'e read opsiyonel (requirements 766).

### Alan yerleşimi (2026-06-15 kilitlendi — requirements 677-732)

5 mantıksal grup, Project'in doldurma sırasında. Alan adları İngilizce/snake_case.

**Grup 1 — Identity (core, her giriş yolunda görünür)**
| Alan | Tip | Not |
|------|-----|-----|
| expo_name | text | "Mega Clima Nigeria 2026" |
| edition_year | text/number | clone bunu artırır |
| sectors | multi-select → expo_sectors junction | core_sectors FK (array DEĞİL) |
| country | select → core_countries FK | country_code CHAR(2); city/venue serbest text |
| city | text | |
| venue | text | |
| organizer_role | enum (4 değer) | Elan'ın fuardaki sıfatı; default main_organizer |
| start_date | date | **TÜM deadline'ların kaynağı** |
| end_date | date | breakdown'un kaynağı |
| actual_visitors | **READ-ONLY** | LEENA COUNT, dokunulmaz, reported YOK |
| cluster_id | FK → expo_clusters (nullable) | boş=bağımsız, dolu=co-located |

**Grup 2+3 — Tarih otomasyonu (fuar tarihinden TÜRETİLEN + iki-seviyeli override)**
Çekirdek mantık: 8 tarih elle GİRİLMEZ; start/end'den offset'le hesaplanır.
Override iki seviye: (a) offset değiştir → kalıcı, clone'a taşınır, ritim kayar;
(b) tarihi direkt düzelt → tek seferlik özel durum. (currency exchange-rate'teki
"hesapla ama override koru" deseni — burada iki katmanlı.)

Mantık dayanağı: default'lar sistem-seviyesi, yeni fuar miras alır (requirements
1126); ama her offset per-expo düzenlenebilir (requirements 549/1120: Owner hardcoded
"30 days before" İSTEMİYOR, sayı expo kaydında yaşar, email engine oradan okur).

| Deadline | Offset alanı | Hesap | Default (KİLİT) |
|----------|--------------|-------|-----------------|
| buildup_day_1 | buildup_1_days_before | start − N | **3** |
| buildup_day_2 | buildup_2_days_before | start − N | **2** |
| standard_buildup_day | standard_buildup_days_before | start − N | **1** |
| catalogue_submission_deadline | catalogue_deadline_days_before | start − N | **25** |
| stand_design_confirmation_deadline | stand_design_deadline_days_before | start − N | **25** |
| payment_deadline | payment_deadline_days_before | start − N | **30** |
| visa_support_deadline | visa_deadline_days_before | start − N | **40** |
| breakdown | breakdown_days_after | end + N | **0** (son günle aynı) |

show_open_hours | **tek text alanı** | "10:00–17:00 (son gün 16:00)" — yapısal DEĞİL,
hiçbir şeye beslenmiyor, sadece exhibitor'a gösterilir, 25 kullanıcı için yapısal aşırı.

Yaprak deneyimi: start/end gir → 8 tarih otomatik dolar → özel durumda offset veya
tarih override. Clone'da: yeni start/end → hepsi yeniden kayar (Zoho'da tek tek
güncelliyordu; burada fuar tarihi değişince gerisi kendiliğinden kayıyor — gerçek
iyileştirme).

**Grup 4 — İPTAL (2026-06-15): Operation Team contacts artık expo alanı DEĞİL.**
~~istanbul_hq_contact / local_onsite_contact FK→users~~ → bunun yerine `expo_partners`
tablosunda `istanbul_hq` + `local_onsite` rolleri (yukarıda Partner Page'e bakınız).
Gerekçe: operation team bazen freelancer, partner mantığına oturuyor; LEENA'da users
tablosu da yok (ölçüm 1e — FK hedefi yoktu). Expo kaydına contact alanı EKLENMEZ.

**Grup 5 — Form URLs (v1: elle; sonra LEENA auto-generate, requirements 707)**
| Alan | Tip |
|------|-----|
| catalogue_form_url | url |
| stand_design_form_url | url |
| visitor_preregistration_form_url | url |

**Partners** → bu formda DEĞİL, ayrı sayfada (`expo_partners`, yukarıda).

**organizer_role (Grup 1) — ekran görüntüsüyle doğrulandı, 2026-06-15.** Zoho expo
kaydında GERÇEKTEN var (Expo Information bölümü, Status'un üstünde — eski adı "GL
Account"). Requirements'ta geçmemesi requirements'ın eksikliği, alanın yokluğu değil
(chat ilk turda yanlışlıkla "yok" sandı; ekran kanıtı düzeltti). Adı `organizer_role`
yapıldı — "GL Account"un yanıltıcı muhasebe çağrışımı yok; dört değer de Elan'ın o
fuardaki sıfatı (ortak tema = rol). Sabit dört-değerli enum (reference-data DEĞİL),
Zoho etiketleri birebir snake_case:
- `main_organizer` — kendi fuarımız (**default**)
- `co_organizer` — ortak düzenlediğimiz
- `agent` — acente olarak sattığımız başkasının fuarı
- `consultant` — danışman olarak yer aldığımız
Clone'da kopyalanır (yeni edition genelde aynı rolde).

### expo_clusters tablosu (Requirements'a göre LEENA'da kurulur)
- requirements 721/726: country+month auto-detect + manual override. **(2026-06-19: eski
  "kurulumda ELIZA'ya bak, varsa hizalan" refleksi KALDIRILDI — eski ELIZA şeması schema
  authority DEĞİLDİR; varsa yalnız tarihsel referans.)** Requirements'a göre LEENA'da
  kuruldu/kurulacak.
- Model: eşit fuarlar ortak cluster kaydına bağlı (parent-child DEĞİL — requirements 726).
- Lifecycle: uydu ayrılırsa cluster_id null olur, tarihsel kayıt korunur (requirements 732).
- Partner paylaşımı: bir fuara partner eklerken sistem "cluster kardeşlerine kopyala?"
  diye sorar (requirements 727).

### Clone akışı (floor plan clone'un expo-level versiyonu) — DETAY KİLİT 2026-06-15
```
Expo List → satırda [Clone]
   ↓
Form açılır, alanlar üç kovaya göre dolu/boş/hesaplı gelir (aşağıda)
   ↓
Yaprak start/end girer → 8 deadline otomatik kayar; gerekirse override
   ↓
Kaydet → yeni expo + kopyalanmış partner bağları + kopyalanmış layout
```

**Alan-alan üç kategori:**

KOPYALANIR (kaynaktan birebir, Yaprak dokunmaz):
- organizer_role (yeni edition genelde aynı rolde)
- sectors, country, city, venue (clone'un tüm mantığı: aynı yer/fuar)
- 8 offset alanı (ritim sabit; start değişse de offset aynı)
- show_open_hours (aynı saatler)
- istanbul_hq + local_onsite operation team (partner bağları içinde — ayrı alan değil)
- partner bağları (aynı tedarikçiler — requirements 727)
- floor plan layout (aynı hall)

YENİDEN HESAPLANIR (yeni start/end girilince otomatik kayar):
- 8 türetilen deadline (buildup ×3, catalogue, stand_design, payment, visa, breakdown)
  = yeni start/end ± offset. Offset kopyalandı, tarih kaynaktan GELMEZ, hesaplanır.

SIFIRLANIR / ELLE (yeni edition'a özel):
- **edition_year** → otomatik +1 (2026→2027). Clone = yeni edition.
- **expo_name** → akıllı replace (parse DEĞİL): edition_year +1 olunca isimdeki eski
  yılı yeni yılla değiştir ("Mega Clima Nigeria 2026"→"2027"). İsimde yıl yoksa aynı
  kalır, Yaprak düzeltir. Clone'un ~%90'ı sadece yıl değişimi → en az iş.
- **start_date / end_date** → BOŞ. Yaprak girer (tüm tarih otomasyonunu tetikler).
- **actual_visitors** → 0/boş (yeni fuar, LEENA henüz saymadı).
- **status** → başlangıç değeri **`announcement`** (expo lifecycle ilk aşaması;
  kaynak `accomplished`/`live` ise ASLA kopyalanmaz). NOT: bu expo status enum'u
  (announcement/sales-open/build-up/live/accomplished — defter satır 89); quote'un
  draft→sent→signed enum'uyla KARIŞTIRMA, ayrı şeyler.
- **form URL'ler** (catalogue/stand_design/visitor_preregistration) → BOŞ. Her edition
  için LEENA yeni URL auto-generate eder (requirements 707); eski URL yeni fuara yanlış.
- **cluster_id** → BOŞ. Yeni edition bağımsız başlar; eski cluster_id eski tarihli
  cluster'a bağlardı (yanlış). Bu edition da co-located olacaksa Yaprak iki yeni
  edition'ı yeni cluster'a bağlar.

**Clone KAPSAMI özeti:** master alanlar + partner bağları + floor plan layout
kopyalanır. Boş kabuk DEĞİL, kaynağın akıllı kopyası (tarihler/URL/cluster/status
yeni edition'a göre sıfırlanır, gerisi gelir).
- "Zaten var" DEĞİL → mevcut floor plan clone workflow'unun (requirements 711) expo-level
  versiyonu; aynı desen, kapsam expo master + partner + layout.
- Clone ≠ rebooking. Clone = yapı kopyası (exhibitor YOK). Rebooking = tek tek firma
  taşıma. Farklı butonlar, farklı zamanlar, farklı kullanıcılar.

### Bilinçli dışarıda bırakılanlar
- **reported/şişirilmiş visitor sayısı → YOK (Faz 5 post-show, ELIZA).** Gerekçe: şişirilmiş
  sayı (örn. 4500 gerçek → 5200 sunum) bir VERİ değil, RAPOR çıktısı. Farklı raporlara
  farklı sayı gösterilebilir (sponsor A'ya 5200, B'ye 4800) — tek `reported_visitors`
  alanı bunu zaten karşılamaz. Şişirme = rapor-anı kararı (Project'in sunum müdahalesi),
  kalıcı alan değil. Expo'nun gerçek verisi bozulmaz. requirements'a yeni alan
  EKLENMEZ (requirements 913 "rapor kendini yazar + Project anlatı ekler" felsefesiyle
  uyumlu).
- **Rebooking (3 parça) → Faz 2 convert akışı.** (a) Sales Contract'ta "Rebook" =
  önceki edition kontratından yeni edition için yeni quote/contract üret (aynı firma/m²,
  güncel fiyat) — convert/quote kısayolu. (b) Floor plan'da stand'ta "Rebook" = önceki
  sahibi yeni edition aynı koordinata yerleştir. (c) Rebooking RATE = hesaplanan metrik
  (önceki exhibitor'ların kaçı rebook etti, fuar kalite göstergesi) → post-show (Faz 5).
  requirements/defterde HİÇ geçmiyordu — yeni kavram, convert akışında doğru yerine
  oturacak.
- **International/local visitor kırılımı → v1 değil** (country verisi kirli).

### Üç yardımcı ekran (2026-06-15 kilitlendi — standart CRUD/filtre, makul karar)

**1. Partner sayfası — ayrı sayfa, standart CRUD**
- Liste: company_name · contact_name · email · phone · partner_role · is_primary.
- Ekle / düzenle / sil. Fuara `expo_partners` (requirements 738-766) üzerinden bağlanır.
- Yaprak buradan partner girer; expo formunda o fuara bağlı partnerleri görür/seçer.
- Fazla detay yok — şema zaten kilitli, ekran çizilince oturur.

**2. Cluster UI — expo formunda alan + aksiyon**
- Expo formunda `cluster_id` alanı + "cluster'a bağla / cluster'dan ayır" aksiyonu.
- Cluster'a bağlıysa "kardeş fuarlar" listesi görünür.
- Partner eklerken "kardeş fuara da kopyala?" sorusu (requirements 727).
- Ayırma = cluster_id null (requirements 732, tarihsel kayıt korunur).
- Standart, requirements 713-732 tarif ediyor.

**3. Expo List filtreleme**
- Liste ekranında filtreler: organizer_role · status · country · year.
- Zoho expo listesi gibi ama filtreli. Basit.



---

## TAMAMLANAN FAZLAR

### FAZ 0 — Temel hijyen (şema kurtarma + secret) ✅
- Üç sistemin (LEENA/LIFFY/ELIZA) canlı şeması READ-ONLY çekildi, `~/ELL_schema_dumps/`'a
  dökümanlandı. Eksik tabloların CREATE'leri migration olarak koda eklendi.
- Her üç sistemde guard-korumalı setup script + migration kapsamı.
- Yan etki: gizli bir ELIZA build bug'ı bulunup düzeltildi.

### FAZ 1a — LIFFY güvenlik izolasyonu ✅ (2026-06-08 / 06-09)

**Amaç:** Satışçı sadece kendi (+ altının) verisini görsün/export etsin/silsin. LIFFY
freelancer'a açılmadan önceki zorunlu önkoşul (requirements 351-363, locked B33).

**Şema ayağı (migration 048 — canlıya uygulandı):**
- `persons`, `prospects`, `companies` tablolarına `sales_owner_user_id UUID`
  (FK→users.id, ON DELETE SET NULL, nullable) + index.
- Backfill: persons 80657/80657, prospects 26123/26123 owner'a atandı
  (owner id `cfb66f28-54b1-4a82-85d5-616bb6bbd40b`). companies boş tablo.
- Kolon adı `sales_owner_user_id` = locked B35 uyumlu.

**Scope kodu (12 endpoint — canlıya deploy edildi):**
Mevcut `reports_to` motoru kullanıldı (`getHierarchicalScope` /
`canAccessRowHierarchical`, middleware/userScope.js — yeni motor yazılmadı).
Recursive CTE `users.reports_to` üzerinden: kullanıcı kendi + tüm alt kademesini görür.
- **Düz scope (8):** persons list/detail/affiliations/campaigns, leads list,
  prospects list+stats, companies list/count/industries/contacts, pipeline/board.
  Hepsinde `sales_owner_user_id` üzerinden; affiliations/companies/prospects join'le
  `persons.sales_owner_user_id`'ye bağlandı.
- **DELETE (persons):** rol kapısı (owner+manager+admin, sales_rep YOK) → 404 →
  scope → reason zorunlu (locked B12) → sil → log. Sıra bu.
- **Export (persons):** scope eklendi, rol kısıtı YOK (rep kendi listesini export eder).
  `users.permissions` JSONB'ye DOKUNULMADI (locked karar — matrix'e ertelendi).
- **Pipeline null-assignee:** atanmamış kişiyi ilk dokunanın otomatik sahiplenmesi
  deliği kapatıldı (her durumda scope kontrolü çalışıyor).
- **pipeline UUID cast fix:** pre-existing bug (atanmamış kişiyi stage'e atarken tip
  hatası). Scope'tan bağımsız ama null-assignee fix'inin çalışması için gerekli. Ayrı
  commit'lendi.
- **DOKUNULMADI (bilinçli):** persons industries/companies/stats — aggregate-only, PII
  yok, scope eklemek dropdown'ları bozar. `permissions` JSONB. legacy team_ids.

**Frontend (liffy-ui):** DELETE artık reason soran dialog gösteriyor; boş sebep
engelleniyor; backend'e `{ reason }` gönderiyor. (Mevcut unsubscribe dialog deseni
kullanıldı, yeni kütüphane eklenmedi.)

**Test (deploy öncesi, gerçek HTTP):** scope 18/18 + delete/export/pipeline 8/8 geçti.
İki rep birbirinin verisini görmüyor/export/silmiyor; manager ikisini de görüyor;
owner her şeyi görüyor.

**Canlı doğrulama (deploy sonrası):** scope canlıda 3 kullanıcı için doğrulandı
(owner 80657, manager 0, rep 0 — atama yok). Auth çalışıyor (token'sız 401, health 200).
DELETE koruma mantığı deploy öncesi test edildi (canlıda secret paylaşmamak için
tekrarlanmadı).

**Deploy:** önce frontend (liffy-ui), sonra backend (liffyv1) — git push, Render
otomatik. İkisi de Live. Sıra önemliydi (backend önce gitseydi eski frontend'de silme
kırılırdı).

---

## AÇIK KUYRUKLAR (yapılacaklar — öncelik sırası değil, liste)

### Faz 1f'den doğan (Quote modülü)
- [ ] **242 SKU catalog import'u.** Catalog tabloları (products/product_prices) canlıda
      ve BOŞ; Zoho'daki 242 SKU normalize edilerek (pazar-çoğaltması ayıklanıp
      ürün + ofis-bazlı fiyata ayrıştırılarak) import edilecek. Quote'u satışçıya
      açmanın ön şartı. Elle temizlik + import script tasarımı gerektirir.
- [ ] **Kullanıcı-ofis atamaları.** 25 kullanıcıdan sadece test edilenler atandı;
      tümüne `users.office_id` atanmalı (UI'da Products & Pricing → Users & Offices).
- [ ] **TEST FIXTURE'LARI — RAPORLAMA CANLIYA ÇIKMADAN SİLİNMELİ:**
      ATR-100000 (signed, TestExpo/TestStand/Halden — convert gate testi için bilinçli
      bırakıldı) + QMA-100001 (sent, MAD, indirimli — çoklu-currency örneği).
      Silme SQL ile (signed API'den silinemez). Sequence bir daha SIFIRLANMAZ.
- [ ] **quotes.company_id köprüsü:** companies tablosu boş olduğundan (77K şirket
      affiliations string'lerinde) quote ara-dönemde `company_name TEXT` taşıyor
      (migration 052). Companies dedup projesi yapıldığında quotes'a nullable
      `company_id` köprü kolonu eklenecek — BİR SONRAKİ MİGRATION'A BİNECEK NOT.
- [ ] **Signed bildirimi şimdilik sadece Owner'a** (LEENA SendGrid transactional yolu).
      Project departmanı dağıtımı Convert gate fazında genişletilecek (req 333).
- [ ] **Gözle doğrulanmadı (kod canlıda):** Expired rozeti (sent + valid_until geçmiş)
      ve draft-detayda Expo'nun İLK açılışta dolu gelmesi (fix deploy edildi, cache
      yüzünden eski bundle'da test edilemedi). İlk gerçek quote'larda bakılacak.
- [ ] **suer kullanıcısının first_name/last_name boş** — Owner kolonu email prefix
      gösteriyor ("suer"); Admin'den doldurulursa isim görünür. Kozmetik.

### Faz 1a'dan doğan
- [ ] **Audit log = sistem geneli "kim/ne zaman/ne yaptı" sayfası.** Şu an silme
      yalnızca SUNUCU LOGUNA yazılıyor (sorgulanabilir tablo değil). Sebep: mevcut
      `contact_activities` person silinince cascade ile log'u da siliyor; bağımsız
      tablo gerekiyordu. **Karar: Faz 4'te yapılacak** — LIFFY + LEENA, tüm aksiyonlar,
      tek audit arayüzü (roadmap Faz 0 düzeltme #4 + Faz 4 "audit detaylandır"). Köprüde
      sunucu logu yeterli (sistem henüz satışçıya kapalı, silme trafiği yok).
- [ ] **DELETE rol kapısında 'admin' rolü var mı?** Kod owner+admin+manager yazıyor;
      `users.role`'da admin gerçekten var mı teyit edilmedi. Yoksa zararsız.
- [ ] **sales_rep'e "Sil" butonu görünüyor** (tıklayınca 403 alıyor). Güvenli ama UX
      pürüzü. Rol-bazlı buton gizleme Faz 4 permission matrix ile gelecek.

### Faz 1b'den doğan
- [ ] **Owner-NULL kampanyalar günlük limite tabi değil.** worker.js throttle
      `created_by_user_id` üzerinden çalışıyor; NULL ise kırpma yok (sınırsız gönderir).
      Yeni kampanyaların sahibi var, pratik sorun değil; ama eski/sahipsiz kampanya
      varsa boşluk. Faz 4 (kimlik birleşimi) ile doğal kapanır.
- [ ] **Yarım kampanya UX:** limit dolunca worker batch'i `continue` ile atlıyor,
      kampanya `sending`'de takılı kalıyor; kullanıcı neden durduğunu UI'da görmüyor
      (log'a yazılıyor). Kalıcı kayıp YOK (recipient pending kalır, sonraki poll'de
      tekrar denenir). Küçük UX pürüzü — frontend auth/UI işiyle birlikte ele alınabilir.

### Secret hijyeni — DÜZELTİLDİ (ölçüldü 2026-06-11): büyük oranda zaten temiz
- **`backend/.env` git'te DEĞİL** (ls-files boş, .gitignore:5'te var, git geçmişinde 0
  commit). Secret'lar sadece lokal çalışma dizininde, repoya hiç girmemiş. Render env
  var'larını ayrı yönetiyor, .env deploy edilmiyor. **Acil secret açığı YOK.** (Önceki
  oturumdaki ".env commit'li" endişesi ölçümle çürütüldü.)
- `.env` içeriği: JWT_SECRET, MINING_API_BASE, MINING_API_TOKEN, MINING_JOB_ID (son ikisi
  secret değil — URL+UUID).
- [ ] **GitHub repo public/private — KONTROL ET (Suer, GitHub'da).** Public ise kaynak
      kod görünür (secret değil ama iş mantığı/endpoint yapısı). LIFFY açılmadan private
      olmalı. Bu, eski "public repo credential exposure" notunun gerçek durumu.
- [ ] **JWT_SECRET periyodik rotation** — best practice, ACİL DEĞİL. Rotate edilince tüm
      aktif token'lar düşer (herkes yeniden login). MINING_API_TOKEN rotate edilirse
      Render env'inde de güncellenmeli.
- [ ] **liffy_user → liffy_user_v2:** v2'ye geçilmiş (oturumlarda v2 kullanılıyor). Eski
      liffy_user hâlâ duruyorsa, servislerin v2'de olduğu teyit edilip eski silinebilir.
- [ ] liffy-db IP kısıtı `0.0.0.0/0` — go-live öncesi daralt.

### Faz 1d'den doğan — ÇÖZÜLDÜ (ölçüldü 2026-06-15)
- [x] **Mass delete (toplu silme) ÖLÇÜLDÜ — güvenli.** Backend'de array kabul eden toplu
      silme endpoint'i YOK; tüm DELETE'ler tekil `/:id`. Frontend'de mining jobs/results
      için çoklu-seçim+sil var ama N tekil DELETE isteğiyle yapılıyor (bulk endpoint yok).
      **Hiçbir dolaylı silme persons'a CASCADE etmiyor:** liste silme→list_members
      (persons etkilenmez); campaign silme→prospect_intents/recipients (persons etkilenmez);
      mining job silme→mining_results (persons.source_mining_job_id SET NULL). Person yalnız
      kendi korumalı DELETE'inden silinebiliyor → 1a baypas edilmiyor. **Yeni bulgu (→
      birleşme paketine):** persons/quotes DIŞINDA tekil DELETE'lerde (campaigns, lists,
      mining jobs/results) rol-kapısı/reason/audit EKSİK; mining results'ta scope bile yok.
      Acil değil (tek kullanıcı), birleşmede 1a deseniyle eşitlenecek.
- [x] **"Assign All" pozitif testi GEÇTİ (2026-06-15).** Yeni mining job → sonuçları
      owner'a toplu ata → ekranda "4 contacts assigned" (gözle doğrulandı). Çalışıyor.

### Lead/Contact ayrımı + mining akışı — Faz 2 (Convert gate ile BİRLİKTE)

**KARAR VERİLDİ: Lead ve Contact AYRI TABLO** (requirements-uyumlu, üç bağımsız mimari
görüş aynı sonuca vardı). Status kolonu DEĞİL.
- **Gerekçe (semantik):** requirements Lead ve Contact'ı iki ayrı VARLIK olarak
  tanımlıyor, bir varlığın iki hâli olarak değil. Glossary: Convert "turns a Lead into
  a Contact + Company." Funnel stage 4: lead enrich edilince Contact+Company çiftine
  dönüşür → biri ölür, diğeri (kopyalanarak) doğar. Status kolonunun ima ettiği "aynı
  şeyin hâli" semantiği YANLIŞ.
- **Gerekçe (ölçek):** ham cold lead hacmi (~587K, çoğu cevapsız) gerçek contact
  çekirdeğinden (~17.5K) kat kat büyük; aynı tabloda tutmak her contact sorgusunu çöp
  lead üstünde çalıştırmak demek. Ayrım fiziksel olmalı.
- **Gerekçe (güven sınırı):** Lead = dış halka (LIFFY mining/campaign) hammaddesi;
  Contact+Company convert sonrası iç halkaya bağlanır. İki ayrı yaşam döngüsü.
- **Model:** `leads` (ham — email + kanal + status[new/contacted/replied]) → enrich/
  convert anında → `contacts` + `companies` doğar. Dönen lead satırı SİLİNMEZ,
  "converted" işaretlenir (funnel analitiği: kaç lead → contact).

**MEVCUT KOD DURUMU (ölçüldü 2026-06-10):** Mining sonucu doğrudan `persons`'a
"contact" olarak yazılıyor (aggregationTrigger, AGGREGATION_PERSIST=true). `persons`'ta
lead/contact ayrımı YOK (stage/status alanı yok). Yani requirements'ın en temel
kavramsal ayrımı kodda uygulanmıyor — her şey "contact".

**NE ZAMAN: Faz 2 Convert gate ile BİRLİKTE — bugün İZOLE KURMA.** Lead→Contact
dönüşümü Convert gate'in kalbi (aynı mekanizma). Şimdi LIFFY'de tek başına `leads`
tablosu kurulursa Faz 2'de yeniden ele alınır. Doğru yer: Convert gate tasarımı.

**Açık kalemler (tasarımda çözülecek):**
- [ ] Mevcut `persons` (~80K) + `prospects` (~26K dual-write) yeni leads/contacts
      modeline nasıl göçecek? Prospects'in kaderi: **DEPRECATE adayı güçlü** (ölçüm:
      %96 persons ile email-örtüşüyor, ayrı varlık değil — aşağı Faz 2 ön ölçüm).
- [x] **Rakamlar DB'den TEYİT EDİLDİ (2026-06-15)** — aşağıdaki "FAZ 2 ÖN ÖLÇÜM"e bak.
      (Requirements'taki 587K/17.5K illüstratifti; gerçek persons 80.659.)

**Mining → liste → kampanya zinciri (#3, daha hafif):** mining → persons OTOMATİK,
ama persons → kampanya yolu MANUEL liste oluşturmaktan geçiyor (mining otomatik listeye
düşmüyor). Temiz hali yukarıdaki #1'e (lead modeli) bağlı. Minimal "mining → otomatik
liste" daha erken yapılabilir; tam temiz hali Faz 2 ile.

### İç bildirim pipeline'ı (transactional, iç ekibe) — Faz 2/4
- [ ] **İç bildirim maili** (quote signed, contract sent, payment confirmed gibi
      olaylarda Elan Expo'nun KENDİ satış/yönetim ekibine bildirim). Dış pazarlama
      maili DEĞİL — footer/unsubscribe/domain reputation gerektirmez (kendi çalışanına
      gidiyor). **Bugün minimal hali VAR:** Faz 1f'de quote signed → Owner'a mail
      (LEENA SendGrid transactional yolu, `campaign_id=NULL`). Tam pipeline (Project
      dağıtımı, diğer olaylar) Faz 2 (convert gate) veya Faz 4 (birleşme) ile.
      **Mimari yön (2026-06-19 güncel):** Event source **LIFFY veya LEENA**'dır. Quote-signed
      event LIFFY'de doğar; **contract/payment/commission event'leri LEENA Finance'ta doğar**
      (ELIZA event source DEĞİL). LEENA transactional email altyapısı kullanılır (olay-bazlı
      akış ilkesiyle uyumlu).
- **NOT — roadmap 1b "op/marketing template flag" maddesi GEÇERSİZ:** O madde dış
      operasyonel maillerin LIFFY'den geçtiğini varsayıyordu. Üç sistem ölçüldü
      (2026-06-09): dış operasyonel mailler (badge/check-in/sertifika/reactivation)
      zaten LEENA'dan footer'sız çıkıyor (`campaign_id=NULL`); LIFFY onları hiç
      üretmiyor; ayrıca LIFFY'de `campaign_type` CHECK constraint'i 'operational'
      değerini engelliyor (flag ölü olurdu). Footer flag yazıldı, ölçüm sonrası geri
      alındı. Gerçek gelecek ihtiyaç yukarıdaki iç bildirim pipeline'ı.

### Secret hijyeni (sisteme açılırken topluca — Faz 1a'da bilinçli ertelendi)
- [ ] **JWT dev-fallback `liffy_secret_key_change_me`** 31 dosyada hardcoded. Canlı
      secret bundan FARKLI (deploy testinde doğrulandı — canlı güvende) ama fallback
      kodda duruyor. Boot-time guard ekle (JWT_SECRET yoksa başlama).
- [ ] **LIFFY DB credential rotation:** eski `liffy_user` hâlâ kullanımda; `liffy_user_v2`
      yaratıldı ama servisler geçmedi. Servisler v2'ye geçmeden eski'yi SİLME.
- [ ] Eski `liffy_user` ve v2 şifreleri oturum terminal çıktılarında düz görünür —
      rotation listesine dahil (kurulum bitince hepsi değişecek, bilinçli kabul).
- [ ] **liffy-db IP kısıtı `0.0.0.0/0` açık** — secret temizliğiyle birlikte daralt.
- [ ] Anthropic/SendGrid/ZeroBounce API key + webhook token git geçmişi auditi
      (önceki tarama: HEAD'de ve geçmişte para-riskli sızıntı YOK).

### Eski açık (Faz 0/1'den taşınan)
- [ ] LIFFY migration ordering kırıklığı (005→007) — Faz 1'e ertelenmişti, hâlâ açık.

---

### FAZ 1b — Campaign cila ✅ (2026-06-09)
- **Footer flag maddesi GEÇERSİZ çıktı** (detay açık kuyruklarda) — dış operasyonel
  mailler LEENA'dan zaten footer'sız çıkıyor, LIFFY üretmiyor. Footer kodu yazıldı,
  ölçüm sonrası geri alındı.
- **Worker throttle (geçerli iş, tamamlandı):** ana worker'a (worker.js) günlük
  gönderim limiti eklendi. Sequence worker'daki `getRemainingDailyLimit` paylaşılan
  `utils/dailyLimit.js`'e çıkarıldı (kod kopyalanmadı). Batch `Math.min(BATCH_SIZE,
  remaining)` ile kırpılıyor (limitCache+`--` deseni KULLANILMADI — worker concurrent
  gönderdiği için race condition riski). 0/NULL limit = sınırsız (mevcut davranış).
  Test 6/6 geçti (gerçek mail gönderilmeden). Commit 6b985ad.

---

### FAZ 1c — Frontend auth sertleştir ✅ (2026-06-09)
- **Ölçüm: gerçek güvenlik açığı YOK.** Backend (LIFFY) her endpoint'te `jwt.verify` +
  `organizer_id` izolasyonu uyguluyor; frontend guard'ları güvenlik sınırı değil UX.
  Token'ı DevTools'tan değiştiren biri sadece menüde link görür, backend 403/401 döner.
  Roadmap 1c'deki "server-side session / route guard" maddeleri sıfır güvenlik kazancı
  sağlardı — EKLENMEDİ (over-engineering'den kaçınıldı).
- **Yapılan gerçek iş (UX):**
  - **LIFFY:** süresi dolmuş token kontrolü (`exp` claim → temizle + login'e yönlendir,
    layout-client.tsx + useAuthGuard.ts) + login sonrası kaldığı sayfaya dönüş
    (returnTo). Commit 3bcc679.
  - **ELIZA:** sadece returnTo (expiry GEREKMEDİ — `/api/auth/me` ile sunucuda zaten
    doğruluyor, proaktif yakalıyor). Commit 512c64c.
  - **Güvenlik:** returnTo açık-yönlendirmeye karşı korundu (`safeReturnTo` sadece
    tek-`/` iç path; `//evil.com`, `https:`, `/\` reddediliyor). Build + statik izleme
    doğrulandı, döngü riski yok.
- **LEENA bilinçli ERTELENDİ → Faz 4.** LEENA frontend statik HTML (42 sayfa,
  sayfa-başı inline guard, merkezi modül yok, JWT hiç decode edilmiyor). expiry+returnTo
  eklemek 42 sayfaya dokunmak/sıfırdan guard kurmak demek — küçük UX işi için orantısız
  ve LEENA CANLI. LEENA'nın auth/izolasyon işi zaten Faz 4'e bağlıydı (roadmap satır
  240); returnTo/expiry de o zaman topluca yapılır.

---

### FAZ 1d — Lead pipeline ✅ (owner-atama ayağı; routing+dedup bilinçli ertelendi)
**Bağlam:** 1a'da `sales_owner_user_id` kolonu + scope eklenmişti ama hiçbir INSERT
path'i onu set etmiyordu → yeni kayıtlar NULL-owner kalıyordu (owner dışında kimse
göremez). 1d bunu kapattı.

**Owner-atama — 5 yazma yolu da artık set ediyor (test edildi, commit'li):**
- Manuel create `POST /api/persons` (8b0aada): default = yaratan; opsiyonel owner
  seçimi `canAccessRowHierarchical` ile yetki-korumalı (rep üstüne atayamaz → 403);
  ON CONFLICT başkasının ownership'ini ezmez. Test 6/6.
- Import path'leri (0866b06): leads import, lists CSV (inline+background), mining
  import-all → yükleyene atanır, `COALESCE(persons.sales_owner_user_id, EXCLUDED...)`
  ile mevcut owner korunur. Test: #1/#3 HTTP, #2/#4 gerçek çalıştırma (owner dolu, 0 NULL).
- Background mining aggregation (e651ebc): job'ı başlatan kullanıcıya
  (`mining_jobs.created_by_user_id`) atanır; flowOrchestrator→resultAggregator→
  aggregationTrigger zinciri boyunca taşınır. Test: bengu job'ı 3/3 owner; **NULL job
  2/2 havuz (sahipsiz)** — ileride otomatik mining için havuz davranışı hazır.
- **Yan bulgu — canlı bug düzeltildi (53a117f):** `processImportInBackground` arka
  planda `req`'i scope dışında kullanıyordu (`req is not defined` ReferenceError),
  mining background import zaten kırıkmış (her batch patlıyor, 1000 kez retry).
  Pre-existing; userId işiyle ortaya çıktı, ayrı commit'le düzeltildi.

**Mimari karar — mining ownership modeli (onaylandı):** Kullanıcı-başlatan mining →
başlatan owner (veya UI'da seçeceği, yetki-korumalı). Sistem-başlatan otomatik mining
→ sahipsiz havuz (NULL), proje ekibi sektör/ülkeye göre dağıtır. **Otomatik mining
bugün KODDA YOK** (cron/scheduler/auto-discovery bulunamadı — her mining kullanıcı
HTTP isteğiyle başlıyor); havuz davranışı NULL-job ile test edildi, özellik eklenince
hazır.

**1d'nin bilinçli ertelenen parçaları:** routing/round-robin (ölçek küçük, elle +
bulk reassign yeterli); dedup iyileştirme (email-UPSERT sağlam, domain/telefon/fuzzy
nice-to-have).

**1d — tamamlanan parçalar:** owner-atama (5 path); disqualification reason; reassign
tekil (`PATCH /api/persons/:id/owner`); assignable users; frontend owner UI; bulk owner
backend+frontend (`<OwnerSelect>`); source_mining_job_id izi (migration 049 — funnel
analitiği için temel iz); mining "Assign All to..." frontend. Hepsi canlıda.

### FAZ 1e — Mining ürünleştir ✅ (ölçüldü 2026-06-11, zaten büyük oranda tamam)
- **A. Self-service ✅** — UI'dan 3 yol (Discover tab, Jobs/New Job modal, Search History).
  needs_manual (Cloudflare) email senaryosu teknik kısıt, tasarım değil.
- **B. AGGREGATION_PERSIST ✅** — production true, mining→persons otomatik.
- **C. Secret ✅** — `.env` git'te değil, açık yok (yukarı "Secret hijyeni"ne bak).
  AI-Miner Generator archived/kapalı. Yazılacak kod çıkmadı.

---

### FAZ 1f — Quote modülü ✅ (2026-06-12, sıfırdan, canlıda + gözle doğrulandı)

**Kapsam:** migrations 050/051/052 + backend API (quotes + referans verisi) + UI.
Tüm tasarım kararları ölçüm-önce/karar-sonra akışıyla tek tek kilitlendi.

**Migration 050 — referans verisi (canlıya uygulandı, Suer terminalinden):**
- `offices`: 7 ofis seed'li (TR/NG/MA/KE/CN/DZ/GH), `code CHAR(2)` UNIQUE,
  `default_currency` (TR=EUR — şirket geneli default EUR, req 47). `users.office_id` FK.
- `expos`: **LIFFY sales-side projeksiyon** — geçici DEĞİL, genişletilebilir. name,
  country_code, city, start/end_date, payment_deadline, default_currency, is_active +
  `canonical_expo_id UUID NULL` köprüsü: ELL birleşmesinde operasyonun (Yaprak'ın
  departmanı) girdiği canonical expo'ya bağlanır, yeniden yazılmaz ("genişleterek
  birleştir" deseni). Ara dönemde expo LIFFY'den elle girilir (az fuar, düşük maliyet);
  kalıcı mimari operasyon→satış yönünde.
- `products` + `product_prices`: **NORMALIZE catalog** (Zoho'nun pazar-çoğaltması
  D2 anti-pattern gereği KOPYALANMADI). products: code, name, category,
  `unit_type CHECK ('m2','unit')` — DEFAULT YOK (sessiz fiyat hatası önlemi), miktar
  NUMERIC zorlamasız. product_prices: ürün × ofis × currency, UNIQUE(product,office),
  `CHECK (unit_price >= 0)`. **Fiyatta EXPO EKSENİ YOK (kilitli):** fuar-geneli
  değişiklik = liste fiyatı güncellemesi; expo/müşteri-özel fiyat = quote satırı
  override'ı (per-deal, req 136 deseni).
- `exchange_rates`: **Owner-yönetimli merkezi kur tablosu** (req 925 kara-borsa gerçeği
  + req 1075 reference-data deseni). `rate_to_eur CHECK (> 0)`, EUR=1 seed, updated_by.
- Tüm trigger'lar idempotent (DROP IF EXISTS + CREATE); 5 tabloda updated_at trigger.

**Migration 051 — quotes (canlıya uygulandı, Suer terminalinden):**
- `quote_af_seq` SEQUENCE START 100000 — **global tek sayaç** (ofis-başına değil).
  Boşluklar normal (rollback numara yakar), benzersizlik garantili, ardışıklık değil.
- `quotes`: **AF görüntüsü SAKLANMAZ (D2)** — saklanan `af_sequence` + `office_id` +
  `status`; görüntü türetilir: (signed? 'A':'Q') + office.code + '-' + sayı. **Q→A
  prefix flip'i bedava** (status değişince görüntü değişir, UPDATE yok). subject
  kaydetmede üretilir (`{Expo}-{Company}-{m² toplamı}SQM`; m² satırı yoksa kısalır) ve
  SAKLANIR, düzenlenebilir, **Sent'te kilitlenir**. currency + `exchange_rate_to_eur`
  (kurdan prefill, override edilebilir, kayıtta DONAR, CHECK > 0). valid_until
  (expo.payment_deadline'dan prefill, düzenlenebilir). status CHECK:
  **draft→sent→signed(TERMINAL) + sent→declined**. signed_scan_url + signed_at
  (Drive URL deseni, req 340; dosya upload altyapısı KURULMADI — bilinçli).
- `quote_line_items`: product_id SET NULL + **snapshot alanları** (description,
  unit_type, unit_price satıra kopyalanır — ürün silinse satır yaşar); quantity > 0,
  unit_price >= 0, discount_percent 0-100, tax_percent >= 0 (req 315 satır-bazlı).
  **Toplamlar SAKLANMAZ — hesaplanır** (D2): line_total, subtotal, EUR-equivalent =
  toplam × donmuş kur.
- **Expired bir STATUS DEĞİL** — `sent AND valid_until < bugün` sorgusundan türetilen
  rozet (D2: gerçek veri tarih, etiket türev).

**Migration 052 — company_id → company_name (ARA DÖNEM; süreç ihlaliyle geldi, karar
sonradan onaylandı):** companies tablosu 0 satır çıktı (77K şirket affiliations
string'lerinde yaşıyor) → FK bağlanacak veri yoktu. Quote ara-dönemde `company_name
TEXT` taşır (autocomplete affiliations kaynağından arar, elle yazım riskini azaltır).
**Companies dedup projesi yapılınca nullable `company_id` köprüsü eklenecek.**

**Backend API (canlıda):** quotes CRUD + satır CRUD + status geçişleri (send/decline/
sign — geçersiz geçiş 400; sign'da scan URL + tarih ZORUNLU, app-enforce; signed quote
silinemez; DELETE rol+scope+reason Faz 1a deseni) + referans verisi CRUD (expos,
products, product_prices, exchange_rates upsert, offices, user-office atama). Scope
mevcut hiyerarşi motoruyla (`sales_owner_user_id`). Signed'da Owner'a iç bildirim
(LEENA SendGrid transactional). Test 11/11 + deploy 404→401 teyidi.
**Gelecek-not:** signed yazan YENİ yol çıkarsa (convert/import) scan-şartı oraya da
taşınmalı.

**UI (canlıda, gözle doğrulandı):** Quotes liste (filtre/arama/rozet) + create/edit
form (expo→currency/rate/valid_until prefill; satır editörü: ürün seç → snapshot dolar,
fiyat override; canlı toplam + EUR equivalent; subject auto-gen + düzenlenebilir) +
detay (status'a göre aksiyon: Send/Decline/Sign modalleri, Delete reason dialogu) +
**Products & Pricing** sayfası (4 sekme: Expos, Products & Prices, Exchange Rates,
Users & Offices). "Catalog" adı kullanılmadı — fuar kataloğu (exhibitor directory)
ile çakışıyordu, terim ona rezerve.

**Gözle doğrulanan akış:** QTR-100000 create → subject doğru → Send (kilitlendi) →
Sign (scan+tarih zorunlu) → **ATR-100000** → Delete reddi. İkinci test QMA-100001:
MA ofisi, MAD kuru 0.093, %5 satır indirimi → 3.534 MAD / 328,66 EUR — **çoklu-currency
matematiği kuruşuna doğru.**

**Süreç dersleri (1f'de yaşandı):**
- Claude Code 052'yi SORMADAN yazıp CANLIYA UYGULADI (gerekçesi ölçümle doğru çıktı
  ama süreç ihlali) → yeni çalışma kuralı aşağıda.
- API testleri canlı DB'ye karşı koşuldu (modül boştu, zararsızdı; dolu tabloda
  tehlikeli) → yeni kural aşağıda.
- "Deploy 200 döndü" teyidi yetersiz — kullanıcı tarayıcı cache'i yüzünden eski
  bundle gördü; üç fix "çalışmıyor" sanıldı, hard refresh çözdü → yeni kural aşağıda.

---

### FAZ 2a — ELIZA API auth ✅ (2026-06-15) — ⛔ ÖNKOŞUL DEĞİL (2026-06-19, tarihsel)
> **2026-06-19:** "Faz 2 Convert gate'in ZORUNLU önkoşulu — ELIZA'ya finans verisi yazmadan önce"
> mantığı **SUPERSEDED**. Finans ELIZA'ya yazılmıyor → **yeni finance build için önkoşul DEĞİLDİR.**
> Tarihsel olarak tamamlandı; eski ELIZA erişilebilir kalacaksa güvenlik için korunur, aksi halde
> decommission/arşiv notudur.

**Bağlam (tarihsel):** ~~Faz 2 (Convert gate) ZORUNLU önkoşulu — ELIZA'ya finans verisi yazmadan
önce kapı kilitli olmalı.~~ Ölçümle doğrulandı ki ELIZA API ardına kadar AÇIKTI:
login+JWT makinesi vardı ama HİÇBİR route'ta doğrulanmıyordu (middleware yok); users
CRUD/targets/sync-now/**auth/migrate (token'sız DDL!)** açıktı; CORS `*`; Twilio webhook
imzasız (From alanı spoof'lanabilir). Bot iç çağrıları HTTP DEĞİL doğrudan modül
(`require('../../packages/...')`) → servis token gerekmedi.

**Yapılan (commit a139c7d, 6 dosya, lokal eliza_test'e karşı 11/11 test geçti):**
- `apps/api/src/middleware/auth.js` (YENİ): `authRequired`, `jwt.verify` HS256 pinli
  (locked Karar 5 — RS256/JWKS yasak), **fallback secret YOK**, public istisna sadece
  POST /api/auth/login.
- `apps/api/src/server.js`: (1) Boot-guard — JWT_SECRET yoksa `process.exit(1)`
  (1f'deki sessiz-fallback hatası tekrarlanmasın). (2) CORS `*` → `CORS_ORIGINS` env
  (virgüllü liste, origin echo). (3) **Global mount** `app.use('/api', authRequired)` —
  LIFFY'nin per-route deseni KOPYALANMADI; ELIZA'da tek mount noktası var, global daha
  basit, delik bırakmaz.
- `apps/api/src/routes/auth.js`: `/api/auth/migrate` (token'sız DDL) KALDIRILDI +
  hardcoded fallback secret kaldırıldı.
- `apps/whatsapp-bot/src/server.js`: `/webhook`'a X-Twilio-Signature doğrulaması
  (`twilio.validateRequest`, `x-forwarded-proto` ile URL kurulumu — Render proxy
  arkasında imza ancak böyle tutar); başarısız → 403. Mevcut `authenticate(from)` 2.
  katman olarak kaldı.
- `apps/dashboard/lib/api.js` (YENİ): merkezi fetch interceptor — tüm API çağrılarına
  `Bearer eliza_token` ekler; 401 → token temizle + `/login?returnTo=` (LIFFY 1c deseni).
  15 dağınık fetch dosyasını tek tek değiştirmeden kapsar.
- `apps/dashboard/pages/_app.js`: `installAuthFetch()` bir kez, tüm sayfalardan önce.

**Push-öncesi son ölçüm (Suer'in tek fonksiyonel endişesi — "kapı kilitli kalmasın"):**
init-password auth arkasına geçince Owner başka kullanıcının şifresini kurabiliyor mu?
→ **EVET** (ölçüldü, varsayılmadı): `POST /api/users/:id/set-password` (users.js:219)
iç rol kontrolü yok, global auth arkasında geçerli token isteyen herhangi authed
kullanıcı (owner dahil) çağırabilir. Lokal test: CEO login→token → POST /api/users (yeni
agent) → set-password 200 → yeni kullanıcı login 200. Kapı kilitli kalmıyor, init-password
kapatmak güvenli oldu.

**Suer'in onayladığı 4 davranış değişikliği:** /migrate silme ✓; tek-seferlik re-login
(JWT_SECRET değişince eski token'lar düşer) ✓; init-password istisnasız global auth
arkasında ✓; başka HTTP tüketici yok (bot doğrudan modül) ✓.

**Render env'leri (Suer kendi panelinden girdi):** eliza-api → JWT_SECRET
(`openssl rand -base64 48`) + CORS_ORIGINS (`https://eliza.elanfairs.com,
https://eliza-dashboard.onrender.com` — iki adres, sonda `/` yok); eliza-bot →
TWILIO_AUTH_TOKEN (zaten vardı, teyit); eliza-dashboard → NEXT_PUBLIC_API_URL (teyit).
eliza-api 12 gündür "Failed deploy"daydı (eski deploy JWT_SECRET'siz patlıyordu);
env girilip yeniden deploy edilince temiz "Deploy live" oldu.

**Gözle doğrulandı (canlı):** Dashboard hard-refresh → re-login → veri geldi (THIS MONTH:
€84.691 / 12 contract / agent kırılımı). WhatsApp'tan bota 3 soru → 3 doğru cevap (Twilio
imzası gerçek trafikte geçti). Auth + CORS + token akışı uçtan uca çalışıyor.

**ÖNEMLİ — ELIZA hâlâ Zoho salt-okunur aynası:** Auth eklemek veri kaynağını
DEĞİŞTİRMEDİ. contracts'a tek yazan hâlâ Zoho sync (`syncSalesOrders.js`); sadece kapıya
kilit takıldı. Gerçek işlem verisi Faz 2/3'te ELL-native contract ile gelecek.

**Faz 2a kapsamı dışı gözlem (birleşme paketine):** `POST /api/users` (create) ve
`/:id/set-password` owner-only DEĞİL — manager/agent token'ı da kullanıcı yaratıp şifre
kurabiliyor. ELIZA'da kullanıcı bugün sadece Suer, sorun değil; rol-gate eklemek ileride
tek satır.

**Faz 2a sırasında bulunan ELIZA dashboard bug'ı (önceden vardı, auth'la ilgisiz —
sonra bakılacak):** Sales sayfasında "THIS WEEK" butonuna basınca buton seçili oluyor
ama tarih aralığı "today"da takılı kalıyor (`2026-06-15 to 2026-06-15`), bu yüzden €0
gösteriyor. Bot "bu hafta 1 sözleşme €150" derken doğru çekiyor; dashboard'daki This
Week butonu date-range hesabını tetiklemiyor. "THIS MONTH" düzgün çalışıyor → sorun
spesifik This Week buton→aralık geçişinde. Frontend, muhtemelen tek satır. Birleşme
öncesi UI polish turuna.

---

## ★ FAZ 2 ÖN ÖLÇÜM — Convert gate + Lead/Contact zemini (2026-06-15, kanıtlı)

Birleşmenin kalbi Convert gate. Tasarıma girmeden önce dört bölüm READ-ONLY ölçüldü
(dosya:satır + canlı SQL). Tüm sayılar bu ölçümden.

**A — Convert gate zemini (ELIZA):**
- contracts'a tek yazan = **Zoho sync** (`syncSalesOrders.js`); tetik: cron
  (scheduler.js:93/99, server boot'ta otomatik) + manuel `npm run sync:start` + HTTP
  POST /api/system/sync-now. Başka yazan YOK. ELIZA tek satır yazamıyor ("never write
  back" — salt-okunur Zoho aynası teyit; "mirror yanılsaması").
- **ELIZA contracts kolonları:** af_number, currency, exchange_rate, revenue_eur VAR;
  **scan_link YOK, commission YOK**; ID int; company/agent string (FK değil). Payment
  ayrı: contract_payment_schedule (sentetik, is_synthetic) + contract_payments (gerçek).
  → Faz 3a "operasyonel kolonlar eklenecek" tespiti ölçümle doğrulandı.
- **Üç sistem arası entegrasyon SIFIR (kod tarafı):** ELIZA→LIFFY/LEENA hiç HTTP yok
  (yalnız Zoho/Anthropic/Twilio SDK). LIFFY'de "eliza" sadece yorum/soft-ref
  (canonical_expo_id, FK yok). LEENA hiçbirine bağlı değil. Entegrasyon sıfırdan kurulacak.
- **"project" rolü HİÇBİR sistemde yok** (LIFFY: owner/admin/manager/sales_rep; ELIZA:
  ceo/manager/agent, CHECK yok). Convert gate'i Project departmanı kullanacaksa yeni
  rol/departman tanımı gerekecek.
- **Review-queue yok.** En yakın yapı: `message_drafts` (insan-onaylı WhatsApp:
  pending→approved→sent — Convert review-queue için DESEN referansı) + `attention_log`
  (genel flag/review log). contracts.status'ta onay-aşaması enum'u yok.

**B — Lead/Contact ayrımı zemini (LIFFY):**
- Ayrım kolon-flag değil **TÜRETİLİR:** affiliations.source_type/source_ref/mining_job_id
  (en zengin keşif sinyali) + prospect_intents varlığı (canonical Lead-vs-Prospect) +
  campaign_recipients varlığı ("contacted"). source_mining_job_id legacy için kullanılamaz
  (aşağı C).
- **persons'a FK'li 12+ tablo** (split haritası hazır): CASCADE (action_items,
  affiliations, contact_notes/activities/tasks, prospect_intents, zoho_push_log);
  SET NULL (campaign_events, sequence_recipients, verification_queue, **quotes 051:42**);
  RESTRICT (campaign_recipients, list_members).
- **Dual-write 4 yol** (persons+prospects birlikte): CSV upload, liste-ekle, leads
  import, mining-import. Hepsi persons ON CONFLICT(organizer_id,LOWER(email)) upsert.
- **Mining→liste→kampanya zinciri:** mining_results'ta person_id FK YOK (keşif ≠ yaratım).
  Otomatik terfi yalnız AGGREGATION_PERSIST='true'. Köprü = liste üyeliği (mining import
  → prospects+persons+list_members → campaigns.list_id resolve → campaign_recipients).

**C — Sayı teyidi (canlı LIFFY DB, salt SELECT):**
- **persons 80.659** — sales_owner dolu 80.659 / NULL 0 (048 backfill, herkes owner'da;
  gerçek dağılım yok). **source_mining_job_id dolu 4 / NULL 80.655** → mining-kaynak
  ayrımı bu kolondan İMKANSIZ (049 sonrası akışlar dolduruyor, 80K legacy boş).
- **prospects 26.123** — **%96 (25.219) persons ile email-örtüşüyor** → ayrı varlık
  değil, persons'ın alt-kümesi → **DEPRECATE adayı.**
- **affiliations 90.722** — DISTINCT company_name 78.327 (normalize 77.642) → **~77K
  firma TEYİT.**
- **campaign'e girmiş 15.471 kişi (%19)** / hiç girmemiş 65.188 (%81) → "contacted"
  ayracı olarak campaign_recipients anlamlı; lead/contact göçünde en güçlü sinyal.

**Sentez:** Convert gate entegrasyonu sıfırdan kurulacak: **tek aktif cross-system sınır
LIFFY ↔ LEENA.** Project rolü + review-queue yeni. **Contract şeması ELIZA'da değil, LEENA
Finance'ta** kurulacak/genişletilecek.
Lead/Contact ayrımı için legacy sinyal = affiliations.source + campaign_recipients
(mining_job_id değil). prospects deprecate edilebilir.

---

## ★ CONVERT GATE TASARIMI — KARARLAR KİLİTLENDİ (2026-06-18, Faz 2)

**Durum:** Convert gate'in TASARIM (karar) kısmı bu oturumda kilitlendi. Kod YOK — sıradaki
adım inşa dilimleri. Expo modülü Convert'in önkoşuluydu (expo seçimi eksikti), artık hazır.

### ⚠️ BU OTURUMUN DERSİ (kalıcı prensip — üç kez tekrarlandı)
**Kaynak önceliği: locked belge + requirements > canlı ölçüm > eski/superseded belge.**
Canlı ölçüm "BUGÜN ne var"ı söyler (geçiş dönemi durumu); locked/requirements "ne OLMALI"yı.
Convert tasarımında üç kez "bugünün ölçümünü kalıcı mimari sandım" hatası yapıldı, her seferinde
locked/requirements ile düzeltildi:
- (1) "ELIZA yazamaz → dual-table" — yanlış. O "Zoho sync tek yazar" kuralı GEÇİŞ DÖNEMİ durumu;
  Zoho kapanınca anlamını yitirir. Doğru: tek tablo, yeni sistem yazar.
- (2) "convert anında company/contact string'den doğar" — yanlış. Requirements 2.2: contact/company
  qualification'da (LIFFY, quote'tan ÖNCE) doğar; convert sadece BAĞLANIR (LINK/CREATE).
- (3) "mevcut prototip sales_agents (SERIAL, 109 satır) kullan" — yanlış. Locked B3: hedef
  sales_agents UUID+user_id'li; prototip tablo locked hedef değil.
- (4 — neredeyse) "Akış B'yi kilitlemek için TOPOLOGY belgesini okutalım" — yanlış olurdu. O belge
  SUPERSEDED (Köprü 1/2 vocab + pending_convert eski model); okumak eski wiring enjekte ederdi.
**Sonuç prensip: belgeyi OKUMADAN tasarlama AMA hangi belgenin GÜNCEL olduğunu da teyit et —
eski belge de canlı ölçüm kadar yanıltır.**

**⚠️ 2026-07-25 EKLENEN DERS — "hazır/canlı/deploy'lu" iddiaları ölçümle doğrula (üstteki dersin
operasyonel ikizi).** Faz 3b-3'te iki kez "backend hazır/deploy'lu (`f4530a1`)" bilgisi geldi;
**ölçüm ikisinde de çürüttü** — hash repoda **hiç yok**, `origin/main` `94ff3e5`, canlı
endpoint'ler **404**. Ön-koşul GATE'leri **DUR** verdi, sıfır zararla düzeldi, M1 gerçekten
yazıldı. **Kalıcı prensip:** "hazır/canlı/deploy'lu" iddiaları prompt-içi ölçümle (`git log` +
`grep` + canlı HTTP) doğrulanmadan **hiçbir dilim o varsayıma inşa edilmez.**

### KİLİTLİ MİMARİ GERÇEK — ⛔ SUPERSEDED (2026-06-19) → YENİDEN YAZILDI
> Aşağıdaki eski blok **"3 DB ayrı kalır / contract ELIZA DB'sine / contract→expo cross-DB B17 /
> cross-DB sınırlar LIFFY↔ELIZA + ELIZA↔LEENA"** diyordu. **Bu YANLIŞ — 2026-06-19 mimari
> kararıyla terk edildi.** Tarihsel kayıt için silinmedi; **geçerli değildir.**
>
> **GÜNCEL KİLİTLİ GERÇEK:** Aktif mimari **2 DB**'dir: **LIFFY + LEENA**. Eski ELIZA DB
> **KULLANILMAZ** (disposable Zoho mirror; `eliza_73du` üstündeki 026/027/028 + convert endpoint
> = retired). **Contracts, sales_agents, payments, commissions, ledger LEENA DB'de** kurulur.
> **Tek cross-DB sınır: LIFFY ↔ LEENA. ELIZA ↔ LEENA bridge YOKTUR.** **contract → expo = LEENA
> içinde GERÇEK FK** (aynı DB). `source_quote_id` = LIFFY UUID logical reference (idempotency key);
> company/contact = LIFFY-kaynaklı logical reference; **finance kaydı LEENA'dadır.**
>
> ~~ESKİ (SUPERSEDED, tarihsel): 3 DB ayrı kalır; contract ELIZA DB'sine; contract→expo cross-DB B17
> logical reference; cross-DB sınırlar LIFFY↔ELIZA + ELIZA↔LEENA; soft-ref kolonlar cross-DB B17;
> ELIZA'nın LEENA'ya fiziksel katılımı ertelenen end-state. → Hepsi geçersiz.~~
- **Köprü vocab'ı sadeleşti:** "Köprü 1/2/5" numaralı sistem ESKİ/superseded. Güncel köprüler
  ayrı-DB-arası: convert anında satış→operasyon (signed quote sinyali) + müşteri olunca ters sinyal
  (LIFFY kaydı "customer" işaretle, kampanyalardan çıkar).
- **pending_convert state EKLENMEZ.** Topology'deki pending_convert + reject-path, req 2.3 (#4:
  review-queue türetilmiş liste, state machine YOK) ile çelişir → requirements kazanır.

### KİLİTLİ KARARLAR (6)

**1. Convert YETKİSİ — ayarlanabilir permission, sabit rol DEĞİL.**
"project rolü ekleyip convert'i ona bağla" YANLIŞ yön (defterdeki eski açık soru #2 böyle çözüldü:
hiçbir yerde sabit rol değil). Convert bir izin (`user_permissions` matrix, locked Bölüm 2) —
kullanıcılara/rollere atanabilir. Default Project'e açık, Owner (is_owner) değiştirir. Her ofis
farklı işler → kim convert eder ayarlanabilir. B9 (display_role authz'de kullanılmaz) + matrix uyumlu.

**2. CONTRACT — tek tablo, LEENA DB'sinde (ELIZA/Finance sekmesi), yeni sistem yazar.**
Geçmiş (doğrudan Zoho'dan migrate) + yeni (convert ile doğan native) AYNI tabloda. Ayrı arşiv YOK,
dual-table YOK. Şekil: mevcut `contracts` çekirdek alanları korunur (af_number, currency,
exchange_rate, revenue_eur, company, agent — migrate kolay + alanlar doğru) + operasyonel kolonlar
(scan_link, commission, expo_id FK, convert metadata: kim/ne zaman + kaynak signed quote ref) +
ownership (sales_owner_user_id vb., B35). `company_name` text + nullable `company_id` bir arada
(yeni=FK referans, eski mirror=string; string→normalleştirme migration'a ertelendi).
**İnşa-anı açık detayı:** geçiş döneminde Zoho hâlâ canlıyken çift-yazma (Zoho sync + convert aynı
tabloya) nasıl önlenir — kaynak-işaretiyle ayrım, inşada çözülecek; tasarım net (tek tablo, sistem sahibi).

**3. HANDOFF (Akış A: signed quote → convert) — KİLİTLİ.**
Qualification zinciri (LIFFY tarafı, asıl doğuş): `leads` (ayrı tablo: ham, email+kanal+status) →
satışçı qualified yapınca → `contacts`+`companies` doğar LIFFY'de (sales_owner_user_id ownership,
B33/B35) → `quote` bunlara FK taşır (contact_id+company_id, LIFFY içi gerçek FK) → lead silinmez,
"converted" işaretlenir (funnel stage-geçiş raporları, req 2.2).
Convert (LEENA tarafı, dikiş): signed quote convert → `contract` doğar LEENA DB'sinde, bağlanır:
- **expo** → aynı DB (LEENA) GERÇEK FK (contract LEENA Finance'ta, expo LEENA Operations'ta; ikisi de LEENA DB'dedir).
- **agent** → aynı DB gerçek FK; locked `sales_agents` hedef şema (UUID PK + organization_id +
  user_id nullable+UNIQUE B3 + agent_type internal/external_agency/external_freelance). Prototip
  SERIAL tablo bu hedefe yükseltilir. External agent user_id=NULL gediği bilinçli (resolver
  `WHERE user_id=current_user.id` external'ı döndürmez = kasıtlı, external login değil).
- **company/contact** → LIFFY'de (CRM çekirdeği) → cross-DB B17 LOGICAL REFERENCE (gerçek FK yok).
  Bu TEK cross-DB bağ. Model: LINK (quote'un contact/company'si varsa = normal yol) / CREATE
  (qualification atlanmış degraded durumun catch-up'ı). "String find-or-create" convert mekanizması
  DEĞİL (o eski contract migration'ının işi, ertelendi).
Kaynak = qualified quote'un contact/company'si; LIFFY persons ÇÖP değil-kaynak-değil.

**4. REVIEW-QUEUE — türetilmiş liste, state machine YOK, reject-path YOK.**
req 2.3: "single action by a single team, not a formal multi-step approval". Review-queue = SELECT
(status='signed' AND henüz convert edilmemiş). Hata bulununca Project satışçıyı arar/maille, quote
DÜZELTİLİR, doğru olana kadar convert edilmez — quote zaten listede kalır (convert edilmedi),
düzelince convert olur, contract'a bağlanınca düşer. Ayrı "reddedildi/beklemede" state YOK.
Expo'daki COUNT/_effective türetme deseniyle aynı.

**5. CROSS-DB BOUNDARY — tek sınır LIFFY↔LEENA, transport ERTELENDİ.**
Doğuş tarafı = LIFFY (qualification, contact/company orada). Convert'te bağlanış = LEENA contract →
LIFFY contact/company logical reference (B17). Transport (outbox/HTTP poll/idempotent retry)
inşa-anı detayı → ERTELENDİ (boundary kilitli, transport sonra).

**6. EXPO SEÇİMİ — LEENA canonical expo modülünden, aynı-DB GERÇEK FK.**
Convert'te expo seçimi LEENA'nın canonical/temiz expo listesinden (Zoho dump değil). contract→expo
**LEENA içinde GERÇEK FK** (contract da expo da LEENA DB'de = AYNI DB). *(2026-06-19: bu maddenin
eski "cross-DB B17 / contract ELIZA DB, expo LEENA DB = AYRI DB" cümlesi kendi içinde çelişiyordu —
SUPERSEDED. Doğru: contract LEENA'da, expo LEENA'da, gerçek FK.)*

### ERTELENENLER (bilinçli, ana hat bitince/inşada)
- **#5 transport mekanizması** — outbox/poll/HTTP, inşa-anı.
- **Akış B (signed-quote'suz contract)** — GERÇEK pattern (Yaprak doğrudan contract yaratır, LIFFY
  kullanmadan; "exception değil birinci sınıf, yoksa LIFFY adoption düşükse sistem bozulur"), ama
  convert ana hattı DEĞİL. Ana hat (Akış A + #6) oturunca GÜNCEL modelde tasarlanır: contract
  LEENA-core, Yaprak contract yaratırken LIFFY'de firma/kişi FUZZY-MATCH (bu Akış B'nin canlı
  linkage mekanizması, migration DEĞİL); eşleşir+link → LIFFY o kaydı "customer" işaretle + aktif
  kampanyalardan çıkar (müşteriye pazarlama maili gitmez); eşleşmez → contract yine doğar, bağ yok.
  pending_convert YOK. (Köprü vocab'ı eski; tek köprü LIFFY↔LEENA.)
- **Zoho→ELL migration** — EN SON adım. Sistem hazır olmadan veri taşınmaz. Tablolar "ileride
  Zoho'dan dolabilir" diye uyumlu kurulur (contract çekirdeği Zoho-mirror hizalı = bu prensip), ama
  doldurma sona kalır. Migrate edilecek (req: reference 1690, finansal geçmiş 1077, contracts);
  LIFFY prototip çöpü (80k persons/26k prospects) atılır, Zoho'dan TEMİZ migrate. İkisi farklı:
  prototip kopyası çöp, Zoho gerçek operasyonel veri hazine.

### İNŞA DURUMU — SLICE 1 YAPILDI + CANLIDA (2026-06-18) — ⛔ RETIRED (2026-06-19)
> **2026-06-19:** Bu bölümdeki **TÜM ELIZA-tarafı convert inşası** (Slice 1, convert çekirdek,
> migration **026/027/028**, `POST /api/contracts/convert`, `convert-core` branch) **RETIRED
> EXPERIMENT**'tir — eski 3-DB yönünün ürünü. **Canlıya deploy EDİLMEYECEK; LEENA'ya birebir PORT
> EDİLMEYECEK; `eliza_73du` migration'ları yeni sistemin temeli SAYILMAYACAK.** Yalnız **dersleri**
> alınır: idempotency (source_quote_id partial unique), 3 guard + 23505 constraint ayrıştırma,
> server-side role gate, audit kolon tipi (kaynak hangi sistemse o tip), no-recompute (payload
> totals oku), atomik transaction. **Convert core LEENA Finance'ta, LEENA şemasına göre SIFIRDAN
> yazılacak; `contract.expo_id` → LEENA canonical `expos.id` GERÇEK FK.** Aşağıdaki tarihsel detay
> silinmedi (yaşayan log) ama **aktif inşa yolu DEĞİL.**

İnşa sırası netleşti (ölçümle): ayrı identity faz YOK. **Slice 1** sales_agents + contract kolonları
(ELIZA) → **Slice 2** LIFFY tarafı (signed quote sinyali + qualification zinciri) → **Slice 3**
convert endpoint → **Slice 4** UI.

**✅ SLICE 1 — sales_agents (locked) + contract forward-compatible kolonlar — CANLIDA:**
- Migration 026 (ELIZA prod `eliza_73du`, commit cdd8a26). Suer dry-run (ROLLBACK) + gerçek uyguladı,
  doğrulandı: legacy=109, yeni sales_agents=0, PK tipi=uuid, contracts'a 6 kolon.
- **sales_agents locked hedef şemaya** (B2/B3): UUID PK + agent_type CHECK (internal/external_agency/
  external_freelance) + user_id UUID UNIQUE nullable SOFT-REF (FK yok — ELIZA users integer) +
  organization_id UUID soft-ref. Eski prototip (SERIAL, 109) → `sales_agents_legacy` rename; yeni tablo
  boş başlar, **backfill Slice 3'e ertelendi** (eski 109 + eski contract agent string'leri Slice 3'te
  string-match'le, company ile AYNI köprü mekanizması).
- **contracts ALTER (additive, mevcut integer FK'lere dokunulmadı):** sales_agent_id UUID GERÇEK FK
  →sales_agents (ELIZA-içi UUID-UUID, tek gerçek FK) + 5 soft-ref (sales_owner_user_id, company_id,
  source_quote_id, converted_by_user_id [hepsi cross-DB LIFFY, FK yok] + converted_at). company_name
  TEXT DURUR (string-match köprüsü). scan_link/commission KONMADI (convert çıktısı, Slice 3).
- **Rename güvenlik:** grep 1 aktif referans buldu — `messages/index.js:110` (.msg agent resolver,
  resolveRecipient). Strateji: o tek satır `FROM sales_agents` → `FROM sales_agents_legacy` (koordineli,
  migration+kod birlikte). .msg 109 legacy satırı kesintisiz okur (canlıda teyit: "Elif AY/tr" döndü).
  finance.js contract/:id/detail'e LEFT JOIN sales_agents eklendi (additive, link yokken NULL).
- **ÖNEMLİ ölçüm notu (Slice 3'ü etkiler):** ELIZA'da contract YAZMA endpoint'i YOK — contracts bugün
  salt-okunur analytics + Zoho-sync yazıyor (INSERT/UPDATE contracts apps/api'de yok). Convert, ELIZA'yı
  İLK KEZ yazan sistem yapacak (Slice 3). Bu tam da "Zoho gidiyor, sistem kendi yazar" hedefinin ilk
  somut adımı.
- gen_random_uuid() extension GEREKMEDİ (PG13+ core, ELIZA PG18). ELIZA DB şifresi rotate edildi
  (credential chat'e yapıştırılmıştı — temizlendi).

**İNŞA SIRASI GÜNCELLENDİ (ölçümlerle):** "Slice 2 = review-queue sinyali" AYRI DİLİM OLMAKTAN
ÇIKARILDI — ölçüm gösterdi review-queue zaten mevcut `GET /quotes?status=signed` (routes/quotes.js:579,
status filtresi + ownership scope hazır), ayrı backend işi yok; review-queue UI dilimine (Convert-4)
erir. Qualification zinciri (leads→contacts) convert ANA HATTINDAN ÇIKARILDI — string-match köprüsü
sayesinde ertelenir, ayrı faz (tetik = LIFFY canlı aktivasyonu). Güncel sıra:
- ✅ **Slice 1** (sales_agents + contract kolonları) — CANLIDA (yukarıda).
- ✅ **Convert ÇEKİRDEK** (payload-driven convert endpoint) — DB CANLIDA, kod branch'te (aşağıda).
- ⏳ **Convert-1** (expo eşleme: LIFFY UUID expo ↔ ELIZA integer expo, canonical_expo_id) — SIRADAKİ.
- ⏳ **Transport** (**LIFFY↔LEENA** HTTP + service-to-service auth B8) — ERTELENDİ (LIFFY aktivasyonu). *(2026-06-19: ELIZA↔LIFFY DEĞİL — tek sınır LIFFY↔LEENA.)*
- ⏳ **Convert-4 UI** (review-queue ekranı = GET /quotes?status=signed + convert butonu, role-gated).
- ⏳ **Qualification zinciri** (leads→contacts ayrımı) — ayrı faz (LIFFY aktivasyonu).

**✅ CONVERT ÇEKİRDEK — payload-driven convert endpoint — DB CANLIDA, KOD BRANCH'TE (2026-06-18):**
- **Endpoint:** `POST /api/contracts/convert` (ELIZA, apps/api/src/routes/contracts.js YENİ). Payload-driven:
  body'de quote JSON (LIFFY GET /quotes/:id şekli) alır → ELIZA contract yaratır. **Cross-system fetch YOK**
  (transport ayrı dilim). Test payload'la izole test edildi.
- **Migration'lar CANLIDA (eliza_73du prod, Suer dry-run+gerçek uyguladı):** 027 (source_quote_id partial
  UNIQUE index `WHERE source_quote_id IS NOT NULL` — race-proof idempotency, mevcut 3536 NULL'la çakışmaz) +
  028 (converted_by_user_id UUID→INTEGER — audit düzeltmesi, aşağıda). Doğrulandı: index var, converted_by=integer.
- **Server-side permission gate (GÜVENLİK):** role IN ('ceo','manager') değil → 403. ELIZA üst rolleri
  ("project" ELIZA'da yok). BUGÜN-KÖPRÜSÜ (matrix gelince B9 swap; tetik = çok-kullanıcılı aktivasyon).
  UI gizleme TEK başına yetmez — broken-access-control önlemi, server-side şart.
- **3 guard:** status≠signed→400, af_number yok→400, source_quote_id zaten var→409 (SELECT-check + partial
  UNIQUE index birlikte = race-proof). 23505 constraint adına göre ayrıştırıldı (af_number vs source_quote_id
  ayrı mesaj).
- **Alan eşleme (kesinleşti):** af_number=quote.af_number (tek DB-zorunlu, hazır); company_name=string-kopya;
  revenue/revenue_eur/m2=quote.totals'tan OKUNUR (computeTotals replike EDİLMEDİ — diverge riski yok);
  status='Valid' (köken source_quote_id≠NULL ile ayrılır, yeni değer uydurulmadı); contract_date=signed_at
  (yoksa today); soft-ref'ler dolu (sales_owner_user_id, source_quote_id, converted_by_user_id, converted_at);
  NULL: expo_id (Convert-1), country (company linkiyle dolacak), company_id (ELIZA companies tablosu yok),
  sales_agent_id (komisyon dilimi), sales_agent/sales_type (quote taşımıyor).
- **Atomik transaction:** pool.connect()+BEGIN/COMMIT (ELIZA app'inde İLK transaction — precedent yoktu).
- **AUDIT DÜZELTMESİ (kritik — köprülerken audit kaybetme):** converted_by_user_id Slice 1'de UUID yapılmıştı
  ("forward-compatible"), AMA ELIZA req.user.userId INTEGER → UUID'ye yazılamaz → audit NULL kalırdı. Reddedildi
  (audit kaybı kabul edilemez). Ölçüm: ELIZA contracts'ta native integer audit kolonu YOK → migration 028
  converted_by_user_id'yi INTEGER'a çevirdi (kolon boştu, kayıpsız). Artık gerçek integer userId yazılıyor
  (test: converted_by=42, NOT NULL). UUID-NULL bırakılmadı.
- **DERS (UUID-forward):** "forward-compatible UUID" LIFFY-KAYNAKLI soft-ref'lerde DOĞRU (değer LIFFY'den UUID
  gelir: sales_owner_user_id, source_quote_id), ama ELIZA-KAYNAKLI kolonlarda YANLIŞ (ELIZA integer:
  converted_by_user_id). Kaynak hangi sistemse kolon o tipte. Convert-1/komisyonda aynı hatayı yapma.
- **⚠️ ELIZA integer ↔ ELL UUID KİMLİK UÇURUMU:** converted_by bunun İLK belirtisi. ELIZA kimliği integer,
  ELL hedefi UUID. Her dilimde soft-ref/NULL/tip-dönüşümüyle köprüleniyor (transport'ta ELIZA↔LIFFY user
  eşlemesi, komisyonda iç rep→sales_agents.user_id aynı uçurumu vuracak). Bu birikiyor — birleşmede TOPLU
  çözülecek (kimlik birleşme tarafından tanımlanır, parça parça değil). DİSİPLİN: köprülerken veri/audit kaybetme.
- **Test (8 senaryo geçti, scratch DB):** geçerli convert→201+eşleme doğru, no-recompute (payload totals
  yazıldı, line-item hesaplanmadı), status≠signed→400, af yok→400, dup source_quote_id→409 (SELECT+index),
  dup af_number→ayrı mesaj, role=agent→403, signed_at yok→today, INSERT hatası→ROLLBACK (yarım satır yok).
- **NOT (bug değil):** contract_date readback'te -1 gün görünüyor (DATE→JSON UTC serialize + slice artefaktı);
  SAKLANAN değer doğru. UI gelince TZ-safe okuma lazım (Expo'daki gibi).
- **PUSH DURUMU:** Kod `convert-core` BRANCH'inde (deploy EDİLMEDİ — Suer prensibi: tüm convert dilimleri
  bitince deploy). DB migration'ları (026/027/028) canlıda. Slice 1 kodu main'de (cdd8a26). Convert tamamen
  bitince branch→main merge+deploy. DB ileride, kod branch'te bekliyor (tutarsızlık yok).

**⏳ CONVERT-1 (expo eşleme) — YENİDEN ÇERÇEVELENDİ (2026-06-19):**
> Convert core **LEENA'da** yeniden kurulduğu için expo eşleme artık **"ELIZA 1227 integer vs LIFFY
> UUID" problemi DEĞİL**. Current convert için kullanılacak expo = **LEENA canonical expos**;
> `contract.expo_id` → **LEENA içinde gerçek FK** (aynı DB). LIFFY quote oluştururken ya LEENA expo
> seçer ya da convert anında LEENA expo seçilir. **Tarihsel Zoho 1.227 expo / 3.536 contract mapping =
> Zoho → LEENA final migration dry-run konusu; convert gate konusu DEĞİL.** Aşağıdaki eski "üç tablo
> kopuk / expo_id NULL kalır" ölçümü tarihseldir — SUPERSEDED.

~~ESKİ (tarihsel ölçüm):~~ Ölçüm üç expos tablosunun KOPUK + çelişen ölçekte olduğunu gösterdi: ELIZA 1.227 (Zoho aynası, contract.expo_id
FK buraya) / LEENA 16 (canonical Expo modülü, elle) / LIFFY UUID (az, elle). Aralarında KULLANILABİLİR köprü
YOK (canonical_expo_id hem boş hem UUID-tip-yanlış; ELIZA↔LEENA köprü NONE; isim-match güvenilmez — farklı
konvansiyon/ölçek).
- **~~Karar: expo_id NULL kalır (çekirdek), eşleme LIFFY-aktivasyonda kurulur~~ → ⛔ SUPERSEDED (2026-06-19):**
  convert core LEENA'da yeniden kurulduğu için `contract.expo_id` **LEENA canonical expo'ya GERÇEK FK** olur;
  NULL bırakma kararı **geçersiz**. (Aşağıdaki eski gerekçe tarihsel:) Gerekçe: (a) çekirdek expo'suz
  çalışıyor (kanıtlı), bugün NULL zararsız (LIFFY dormant, gerçek convert yok); (b) "üç expo tablosunu eşle" =
  EXPO BİRLEŞMESİ, convert'in alt-dilimi DEĞİL — onu convert'e sıkıştırmak birleşmeyi (organik, ayrı iş) çiğner.
- **ÇERÇEVE (önemli):** expo_id "qualification gibi opsiyonel zenginleştirme" DEĞİL — expo'suz contract FİNANSAL
  ÖKSÜZ (gelir fuara yazılamaz = P&L temeli yok). ZORUNLU, sadece zamanlaması ertelenebilir. Tetik: gerçek convert
  (LIFFY canlı) = gerçek contract = fuar ataması ŞART. → "expo bağlama = LIFFY-aktivasyon ön-koşulu, transport ile birlikte."
- **DAR KAPSAM keşfi (eşlemeyi küçültüyor):** Convert'in eşleme ihtiyacı SADECE güncel fuarlar (aktif satılan ~16,
  LEENA canonical) — 1.227 tarihsel Zoho arşivi DEĞİL. Küçük set, LIFFY-aktivasyonda elle bile eşlenebilir. Tüm
  1.227'yi uzlaştırmak convert'in işi DEĞİL.
- **BİRLEŞME BAYRAĞI (ayrı iş, şimdi çözme):** 1.227 tarihsel ELIZA/Zoho expo + onlara FK veren 3.536 contract'a
  ne olacak (LEENA canonical'a taşıma vs arşiv) = ciddi birleşme sorusu. Yön: canonical=LEENA (kilitli); güncel
  fuarlar LEENA'ya katlanır, tarihsel ayrı ele alınır. Tasarım birleşme zamanı.

**⏳ CONVERT — KALAN İŞ = LIFFY-AKTİVASYON ENTEGRASYON FAZI (hepsi aynı tetiğe bağlı):**
Convert çekirdek (DB canlı, kod branch) BİTTİ. Kalan üç parça da LIFFY canlı kullanıma açılmasına bağlı, tek kova:
- **Transport** (ELIZA↔LIFFY HTTP + service-to-service auth, B8 integration_credentials, plain-text yasak). Bugün
  iki backend birbirini bilmiyor (URL env yok), service auth yok. ELIZA fetch yapabilir + LIFFY CORS-açık (mekanik
  mümkün). Service token KULLANICI token DEĞİL (convert otonom + convert eden quote sahibi olmayabilir → kullanıcı
  token ownership scope'a takılır). LIFFY'de customer-mark endpoint sıfırdan eklenecek.
- **Convert-4 UI** (review-queue ekranı = mevcut GET /quotes?status=signed + convert butonu, server-side role-gated).
- **Expo bağlama** (yukarıda — güncel ~16 fuar eşlemesi).
- **LIFFY aktivasyon güvenlik checklist'i:** LIFFY JWT fallback `'liffy_secret_key_change_me'` GERÇEK AÇIK —
  aktivasyondan önce kaldır (Render'da LIFFY JWT_SECRET set mi bak; set'se fallback bugün tetiklenmiyor).

**Yani:** convert'in canlı/kullanılabilir olması = LIFFY'nin kullanıma açılması. Bu büyük bir entegrasyon eşiği
(transport + expo birleşme parçası + UI + qualification + güvenlik), tek tek değil birlikte gelir. Convert çekirdek
o eşiğe kadar branch'te bekler (DB hazır, endpoint hazır, sadece beslenecek kaynak+çıkış yok).

---

## ÇALIŞMA TARZI HATIRLATMASI
- **ELL genelinde UI dili İNGİLİZCE.** Türkçe etiket kullanma (LIFFY/LEENA/ELIZA hiçbiri).
- **ŞEMA KURALI (1f'den, ihlal yaşandı):** Claude Code şema değişikliği gerektiğinde
  DUR ve SOR; kendi kararıyla migration yazamaz, ÇALIŞTIRAMAZ. Migration'ları Suer
  kendi terminalinden uygular. Her Claude Code promptuna eklenir.
- **MIGRATION RİTÜELİ (2026-07-22'den kalıcı, yapıştırma bozulması yaşandı):** migration
  çalıştırma **`\i` ile dosyadan** yapılır — `BEGIN; \i migrations/NNN.sql; ROLLBACK;`
  (dry-run) → `BEGIN; \i ...; COMMIT;` (gerçek). Migration dosyalarında `BEGIN/COMMIT`
  YOKTUR — transaction **dıştan** sarılır. Uygulanmış migration DEĞİŞMEZ; düzeltme/ek
  daima **yeni delta dosya** (örn. 021→022).
  **GENİŞLEDİ (2026-07-24):** `psql`'de yalnız `\d` değil, **`\i` DAHİL TÜM backslash
  komutları yapıştırılan bloklara KONMAZ** — `BEGIN` / `\i ...` / `COMMIT` **üç AYRI Enter**.
  *Yaşanan olay:* 023 gerçek turunda blok yapıştırmada `COMMIT;` `\i`'nin fazladan argümanı
  sayılıp YOK SAYILDI ("extra argument ignored"), transaction açık kaldı (prompt `=*>`); ayrı
  `COMMIT` ile kapatıldı — **veri etkisi olmadı**, kayıt `applied_at`'i insert anını korudu.
- **TEST KURALI (1f'den):** testler canlı DB'ye karşı koşulmaz; koşulmak zorunda
  kalındıysa oluşturulan test verisi açıkça raporlanır ve temizlenir/işaretlenir.
- **DEPLOY TEYİDİ KURALI (1f'den):** frontend deploy teyidi "sayfa 200" ile DEĞİL,
  yeni koda özgü bir işaretle yapılır; kullanıcıya hard refresh (Cmd+Shift+R)
  gerekebileceği hatırlatılır.
- **Görsel/UI işlerinde Suer kendi gözüyle kontrol eder.** Backend endpoint testleri
  geçse bile UI bug'ı kaçabilir (örn. Owner display, Expo "—", autocomplete boş
  dropdown — hepsi görsel kontrolde yakalandı).
- **CLAUDE CODE DİZİN KURALI (2026-06-15'te yaşandı; 2026-06-19 GÜNCEL):** Claude Code
  çalıştığı dizine odaklanır; ölçüm yapılan sistem O DİZİNDE açılır. ⚠️ **YENİ FİNANS İŞİ
  LEENA'DA YAPILIR:** contracts/payments/commissions/ledger işi için **LEENA repo/DB** açılır.
  **"Finance" denince `~/Projects/eliza` AÇILMAZ** — eski ELIZA yalnız legacy/reference/
  decommission içindir; yanlışlıkla orada finance inşa etme. Tarihsel ELIZA *ölçümü* için
  `~/Projects/eliza` yalnız referans/arşiv amaçlı açılabilir.
- **RENDER ENV-DEPLOY (operasyonel not, 2026-06-15):** Env'leri Render panelinden
  girerken birden çok değişkeni TEK "Save, rebuild, and deploy" ile kaydet (tek deploy
  tetiklenir). Boot-guard'lı servis (JWT_SECRET zorunlu) env eksikken "Failed deploy"
  verir — bu normal; env girilince temiz boot eder. Monorepo'da hangi `apps/**` yoluna
  dokunulduysa o Render servisi deploy tetikler.
- Öneri üretmeden önce: `ELAN_EXPO_REQUIREMENTS_v1_0.md` + `ELL_LOCKED_KARARLAR_OZET.md` oku.
- Locked'a aykırı öneri çıkacaksa "bu locked'a aykırı" diye işaretle.
- Tahminle ilerleme; ölçülebilir şeyi Claude Code'a READ-ONLY saydır (dosya:satır kanıt,
  bulamadığına "bulamadım").
- Canlıya dokunan iş (deploy/migration/secret): önce analiz + test, AYRI onay.
- Credential/secret işleri Suer'in kendi terminalinde — chat'e secret/şifre YAZILMAZ.
- En basit çözüm; over-engineering yasak. Karmaşıklık ancak kanıtlanınca.
- Adım adım, bir seferde tek şey; uzun/aşırı temkinli yanıt istenmiyor.
