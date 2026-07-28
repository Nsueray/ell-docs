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
> - **Devir brief'indeki "ELL_GLOSSARY.md commit'siz M duruyor" notu YANLIŞTI** —
>   2026-07-27 ölçümü: dosya **temiz**, commit'siz değişiklik yok (son dokunuş `a416fa9`).
>   Madde kapandı, aksiyon gerekmiyor.

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

> ## ★ SIRADAKİ ADAYLAR (Faz 3b-3 sonrası — karar Suer'de, seçim yapılmadı)
>
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
> kuyrukların tek kaydı. Faz başına ayrı belge YOK — her şey burada, en üstte en güncel.
> Durumu buradan gör.
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
