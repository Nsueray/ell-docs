# ELL — Kilitli Mimari Kararlar (Özet)

> **Bu nedir:** ELL mimari fazında kilitlenmiş kararların tek-satırlık özeti.
> Detaylı enforcement mekanizması ve karmaşık metin BİLEREK çıkarıldı — burada
> sadece "ne karara bağlandı" var. Amaç: köprü/prototip önerileri üretirken bu
> kilitli kararlarla çelişme. Çelişen bir şey önereceksen "bu kilitli karara
> aykırı" diye açıkça işaretle.
>
> **Not:** Bunlar implementasyon reçetesi DEĞİL. Basit, kanıtlı, prototip-temelli
> çalışmaya devam et. Bu liste sadece bir uyum kontrol listesi.

---

## Identity Modeli (Bölüm 1 — kilitli)

> **Zaman ekseni notu:** Bugün geçerli LEENA gerçeği `organizer_id` + **integer PK** (S7 v1.2).
> `organization_id` + UUID **birleşme hedefidir** — aşağıda `[HEDEF — birleşme sonrası]` etiketli
> iki satır bunu tarif eder. Zaman ekseni farkıdır, çelişki değildir.

- **B1** — Schema'da tek isim `organization_id` (LIFFY'nin `organizer_id`'si emekli). [HEDEF — birleşme sonrası]
- **B2** — Üç ayrı identity tablosu: `users`, `sales_agents`, `data_entry_contractors`. Ortak parent tablo yok.
- **B3** — `sales_agents.user_id` nullable + UNIQUE (bazı agent'lar system user değil).
- **B4** — Data entry contractor token'ı ayrı tabloda, HMAC-SHA256 hash + key rotation desteği.
- **B5** — Üç entity için lifecycle: **deactivate default, hard delete istisna** (Owner + ikinci onaylayıcı).
- **B6** — Deactivation entity-spesifik: user → login kapanır + direct report'lar yeni manager'a reassign; agent → yeni attribution'da seçilemez ama eski kayıt bozulmaz; contractor → token revoke.
- **B7** — LEENA legacy login migration: cutover'da ilk Owner user yaratılır, password_must_change.
- **B8** — `organizers` → `organizations` tablosu (multi-tenant root). API key/secret'lar ayrı `integration_credentials` tablosunda, plain text yasak, LEENA/LIFFY secret izole.
- **B9** — `display_role` sadece görüntü; **authorization'da kullanılmaz**. Yetki = permission matrix + scope + `is_owner` flag.
- **B10** — Owner statüsü `users.is_owner` flag'i. Aktif Owner sayısı 1'in altına inemez; self-grant yasak.
- **B11** — Sales agent / contractor yaratma **permission-bazlı**, kişi-bazlı değil.
- **B12** — Tüm kritik aksiyonlarda reason field zorunlu (deactivate, delete, token revoke, password reset, is_owner revoke).
- **B13** — Sales agent banka/IBAN bilgisi ayrı tabloda, `view_sensitive_finance` permission'ıyla korunur, encrypted.
- **B14** — Phone formatı E.164 tek string. WhatsApp opt-in + verified_at.
- **B15** — Serbest metin (`notes`) alanları audit edilir (event log).
- **B16** — `*_by_actor_type` pattern: kayıtların kim/ne tarafından yaratıldığı/güncellendiği tutarlı tutulur.
- **B17** — Cross-DB referanslar logical reference (gerçek FK yok); orphan'lar tespit/rapor/manuel onarım.
- **B18** — Yüzde alanlarında schema-level range CHECK (0–100).
- **B19** — Cross-organization tutarlılık application-layer'da doğrulanır (MVP); UUID global. [HEDEF — birleşme sonrası]
- **B20** — Public form token leak koruması (Referrer-Policy + token maskeleme).

---

## Permission / Yetki Modeli (Bölüm 2 — kilitli)

**EN ÖNEMLİ — prototipteki permission tartışmasıyla doğrudan ilgili:**

- **Yetki modeli ilişkisel `user_permissions` matrix tablosudur — serbest-form JSONB DEĞİL.** LIFFY prototipindeki ölü `permissions` JSONB kolonu hedef mimaride bir yere taşınmıyor; ELL'e geçişte matrix'e dönüşüp atılır. Şimdi ne canlandır ne sil.
- **Field-level visibility gerçek bir ihtiyaç** (requirements 2.2 + 3.1). Örn. `view_sensitive_finance` field-level gate. "Granüler izin yok / over-engineering" çıkarımı YANLIŞ — sadece prototip henüz implement etmemiş.

Diğer kararlar:

- **B21** — Authorization sırası: action classification → self-matrix-edit check → Owner bypass → matrix lookup → scope check → reason → audit.
- **B22/B23** — Permission registry tek key formatı `(module, action)`. Global/protected permission'lar sentinel namespace'lerde.
- **B24** — Protected system operations matrix dışı, kod-level invariant.
- **B25** — **Owner bypass yalnızca authorization'ı bypass eder; business validation (same-org, finance invariant, state machine vb.) Owner için de çalışır.**
- **B27/B28** — Sistem template'leri immutable + silinemez; custom template'ler düzenlenebilir.
- **B30** — `user_permissions` matrix granular; template apply default olarak istisnaları korur.
- **B32** — **Hiçbir kullanıcı kendi permission matrix'ini düzenleyemez (Owner dahil).** İstisnalar ayrı endpoint'ler: password, notification prefs, dil, timezone, display_name, telefon.
- **B33** — Hierarchy enforcement (`reports_to`): self/descendant/cross-org/inactive yasak. Owner için `reports_to = NULL`.
- **B34/B38** — Scope composition module-specific resolver pattern (her modül kendi read + create kuralını sağlar).
- **B35** — **Contract resolver Aşama 3 prerequisite:** explicit ownership alanları (`sales_owner_user_id` vb.) tanımlanmadan implement edilmez.
- **B40** — LIFFY matrix sync: yetki daraltma → anında; yetki genişletme → polling kabul.
- **B42** — `view_sensitive_finance` field-level gate; `export_data` / `send_marketing_campaign` iki aşamalı (capability + target scope) authorization.

---

## Görünürlük kuralı (prototip sorusunun cevabı, kilitli kararlarla uyumlu)

Rep kendi + altının verisini görür; yönetici altının hepsini görür; Owner her şeyi
görür. `reports_to` hiyerarşisiyle. (Requirements 2.2 + 2.8, Bölüm 2 B33 ile uyumlu.)

---

## Açık / hizalanmamış nokta

- **Faz vs Aşama takvimi:** v4 roadmap "Faz", mimari dokümanlar "Aşama" kullanıyor.
  Permission matrix mimaride **zaten tasarlanmış/kilitli** (Bölüm 2), implementasyonu
  sonraya bırakılmış. v4'teki "Faz 4" referansıyla mimarideki "Aşama 3" implementasyon
  zamanlaması henüz birebir hizalanmadı — bir karar gerekirse Sentez chat'e taşınır.

---

## İŞ KURALLARI (build fazı)

> **Bu bölüm nedir:** `ELL_DURUM_DEFTERI_v2.md`'ye geçmiş iş kurallarının **İNDEKSİ**.
> Gerekçe, ölçüm ve tarihçe defterde kalır — burada yalnız hükmün tek cümlesi ve defter satırı var.
> **Çelişkide DEFTER kazanır.** ID tahsisi YALNIZ bu kütükte yapılır; numara asla yeniden kullanılmaz.
>
> **⚠️ ESKİ ADLAR BENZERSİZ DEĞİL:** PS1 (payout) ve PS3 (plan) dilimleri S- numaralarını sıfırdan
> başlatmış. `S-1` · `S-3` · `S-4` · `S-8` iki AYRI hükümde kullanılmış; her biri İKİ yeni ID aldı.
> Eski ada göre arama yapan, iki sonuç bekleyecek.
>
> **Numaralar süreksiz** — deftere geçmemiş hükümler kütük dışıdır, kovalanmaz.
> **⚠️ `K` namespace uzlaştırıldı (2026-07-30):** `V`/`T` hâlâ test ve görsel-tur ID'leridir (kural
> değil). Ancak PS3-B dilimi `K1..K16`'yı GEÇİCİ KURAL etiketi olarak da kullandı; bu tur kalıcı
> ID'lere tahsis edildi: RAP-01..03 · PLN-09..11 · OFS-06 · PLN-04/05/06/07 genişletmeleri ·
> OFS-01. ID ALMAYANLAR: K2→D2 mimari ilkesi · K5→OFS-01 · K6 (UI iskelet) / K9-axis (yerleşim
> tasarımı) / K11 (to_char teknik koruması) tasarım-teknik, kural değil · K12 (organizer scope)
> mimari çok-kiracı invaryantı. Kod etiketleri `55729d6`'te kalıcı ID'lere çevrildi; `K[0-9]` deseni
> cashForecast.js · cash-forecast.html · test dosyasında SIFIR (grep ile doğrulandı).
> Tiresiz `S1..S9` (açık soru takibi) · `D1..D4` (agent import kararı) · `D2` (D2 mimari ilkesi)
> AYRI namespace'lerdir — arama deseni tire'yi zorunlu tutmalı, gevşetilirse çöp girer.
> **YON grubu bu turda dolduruldu** (YON-01..04) — süreç hükümleri.
>
> **⚠️ ATIF BİÇİMİ: `[defter:YYYY-MM-DD BAŞLIK-PARÇASI]`** (ör. `[defter:2026-09-13 FAZ 4 DİLİM 1]`) —
> başlık yazıldıktan sonra değişmez, tek, grep'lenir. Satır-no atıfları KULLANILMAZ (kayar).
> **Dönüşüm TAMAMLANDI 2026-09-13:** 35 eski `[defter:NNN]` atfı içerikten (KOYAN defter kaydına)
> eşleştirilip başlıklı biçime çevrildi; **BULAMADIM: 0**. Çift-kayıtlılar (PLN-05/07, OFS-01/05,
> TAH-04) KOYAN + genişletme ikinci/üçüncü atfına bağlandı. Orta-güven: OFS-04/05 (PS3-A), TAH-04
> [747]→PS1 — defter tarafı doğrulandı, gerekçe defterde.

### MOT — komisyon motoru

- **MOT-01** (eski S-8) — Dilim CTE'leri `utils/commissionSlices.js → SLICE_CTES`'te tek kaynaktır; ikinci komisyon formülü açılmaz. [defter:2026-07-25 FAZ 3b-3 TAMAM]
- **MOT-02** (eski S-8) — Komisyon tahsilat oranına bağlıdır (`paid_eur/revenue_eur`), vade planına DEĞİL. [defter:2026-07-25 FAZ 3b-3 TAMAM]
- **MOT-03** (eski U1a) — Tavan kümülatif-marjinal uygulanır ve dilimlere "(cap)" notuyla yansır. [defter:2026-07-25 FAZ 3b-3 TAMAM]
- **MOT-04** (eski U2a) — Kesim takvim günüdür (`payment_date` DATE, TZ yok). [defter:2026-07-25 FAZ 3b-3 TAMAM]
- **MOT-05** (eski U3a) — Rapor yalnız hak edilmişi gösterir; potansiyel detayda kalır. [defter:2026-07-25 FAZ 3b-3 TAMAM]

### TAH — tahsilat / ödeme girişi

- **TAH-01** (eski W-8) — Reversal ve transfer satırında ofis/method sunucuda orijinalden devralınır; istemciden gelen değer yok sayılır. [defter:2026-07-28 PS2 CANLIDA]
- **TAH-02** (eski W-9) — Add-payment tarihi bugünle ön-doldurulur; sunucuda tarih zorlaması yoktur. [defter:2026-07-28 PS2 CANLIDA]
- **TAH-03** (eski W-10) — Tek ödeme formu vardır (`contract-detail.html`); satır içi hızlı form açılmaz. [defter:2026-07-28 PS2 CANLIDA]
- **TAH-04** (eski S-6) — `payments.schedule_item_id` kolonu vardır ama ödeme↔kalem eşleştirme mantığı bilinçli olarak YOKTUR. [defter:2026-07-28 PAYMENT SCHEDULE PS1] Bu yüzden PLN-10'un ay dağılımı bir VARSAYIMDIR (satır eşleştirme yapılamıyor). [defter:2026-07-30 PS3-B CANLIDA]
- **TAH-05** (Paket 3 hüküm 3 — Suer S2, Sentez 24 Eki) — Gelir BRÜTTÜR (vergi dahil), komisyon matrahı NETTİR (RF hariç — K7b; MOT-01 formülü değişmez). `contracts.revenue` = BRÜT (müşterinin borcu; paid/balance brüte karşı). net = Σ(q×p×(1−d)) · vergi = Σ(net_satır × tax%) · BRÜT = net + vergi; L4 = BRÜT(satırlar) ↔ revenue ±0.01. `revenue_net` saklanmaz (D2, türetilir); raporda ciro iki sütun brüt + net (RAP-02). [defter:2026-10-24 PAKET 3 KRİTER TURU]

### ODE — payout / cari hesap

- **ODE-01** (eski S-1) — Payout modeli CARİ HESAPTIR; kayıtta dönem/kesim kolonu yoktur, bakiye her okumada türetilir. [defter:2026-07-27 PAYOUT P1 CANLIDA]
- **ODE-02** (eski S-3) — Clawback ayrı mekanizma değildir; fazla ödeme bakiyeyi negatife düşürür, sonraki ödemede mahsuplaşır. [defter:2026-07-27 PAYOUT P1 CANLIDA] · **Çapraz ref (21 Eki):** REQ §2.3 "commission_adjustment" SUPERSEDED (amendment 2026-10-21). [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **ODE-03** (eski S-4) — Payout immutable'dır; UPDATE/DELETE yok, düzeltme = negatif tutarlı yeni satır + `reverses_payout_id`. [defter:2026-07-27 PAYOUT P1 CANLIDA]

### PLN — vade planı

- **PLN-01** (eski S-1) — Yarım plan yasaktır; `contract_date`/`expo_id`/`expo.start_date`/`revenue`'dan biri NULL ise 400 + 0 satır. [defter:2026-07-28 PAYMENT SCHEDULE PS1]
- **PLN-02** (eski S-2) — `d2 <= d1` ise tek kalem %100 @ d1; değilse %40 @ d1 + kalan @ d2. [defter:2026-07-28 PAYMENT SCHEDULE PS1]
- **PLN-03** (eski S-3) — Yuvarlama artığı ikinci kaleme yazılır; Σ kalem ≡ revenue TAM olur. [defter:2026-07-28 PAYMENT SCHEDULE PS1]
- **PLN-04** (eski S-4) — Planda kur dondurulmaz; `exchange_rate`/`amount_eur` kolonu yoktur, tutar kontrat para birimindedir. [defter:2026-07-28 PAYMENT SCHEDULE PS1] Rapor tarafı: PLN-09 (kontratın kuruyla EUR'ya çevrilir).
- **PLN-05** (eski S-5, eski H3, eski K3) — Tutar/tarih ASLA UPDATE edilmez; revizyonda eski satırlar `superseded_at` damgalanır, yeni satırlar `revision = max+1` ile eklenir. **Okuma tarafı:** aktif plan = `superseded_at IS NULL`; `MAX(revision)` aktif seçmez, yalnız sonraki numarayı üretir. [defter:2026-07-28 PAYMENT SCHEDULE PS1; 2026-07-28 PS3-A CANLIDA; 2026-07-30 PS3-B CANLIDA]
- **PLN-06** (eski S-7) — Ödeme durumu saklanmaz; "ödenmemiş" = Σ schedule > Σ payments olarak kontrat seviyesinde türetilir. [defter:2026-07-28 PAYMENT SCHEDULE PS1] Satır seviyesi tahsilat dağılımı → PLN-10.
- **PLN-07** (eski S-9, eski K4) — Σ ≠ revenue engellenmez; elle girişte uyuşmazlık kabul edilir, yanıtta `warning` döner. **Rapor yüzeyi:** uyuşmazlık kontrat satırında ⚠ işaretlenir (`matches_revenue = false`). [defter:2026-07-28 PAYMENT SCHEDULE PS1; 2026-07-30 PS3-B CANLIDA]
- **PLN-08** (eski S-13r) — Plan ≠ gerçektir; plan ofisi ile ödeme ofisinin eşleşmesi zorlanmaz, uyarı üretilmez. [defter:2026-07-28 PAYMENT SCHEDULE PS1]
- **PLN-09** (eski K7) — Nakit öngörü raporunda plan satırı EUR'ya kontratın KENDİ kilitli kuruyla çevrilir (`amount × contracts.exchange_rate`); yeni/bugünkü kur kullanılmaz, plana kolon eklenmez. PLN-04'ün rapor-tarafı tamamlayıcısı. [defter:2026-07-30 PS3-B CANLIDA]
- **PLN-10** (eski K8) — Tahsilat düşümü SATIR seviyesindedir: `Σ payments.amount_eur` (NET, reversal dahil, status filtresi yok) aktif satırlara `due_date ASC`, eşitlikte `item_no ASC` teleskopuyla düşülür (MOT `effective_pay` formülü, ikinci formül yazılmaz); `remaining` < 0 olmaz, fazla tahsilat ayrı sütunda. ⚠️ Hangi taksitin kapandığı KAYITLI DEĞİL (TAH-04) → ay dağılımı VARSAYIMDIR, toplam kalan doğrudur. PLN-06'nın satır-seviyesi genişletmesi. [defter:2026-07-30 PS3-B CANLIDA]
- **PLN-11** (eski K14) — Plan satırı "vadesi geçmiş" sayılır: `due_date < bugün AND remaining > 0`. Satır bayrağı + ofis-içi alt toplam olarak gösterilir (ayrı üst grup DEĞİL); `remaining = 0` geçmiş satır overdue değildir ama gizlenmez. [defter:2026-07-30 PS3-B CANLIDA]

### OFS — ofis

- **OFS-01** (eski S-16r, eski K5) — Ofis listesi koda gömülmez; enum/CHECK/frontend sabiti yoktur, tüketici `GET /api/offices`'ten okur (nakit öngörü raporu da öyle). [defter:2026-07-28 PS2 CANLIDA; 2026-07-30 PS3-B CANLIDA]
- **OFS-02** (eski S-11r) — Ofis × para birimi × tahsilat şekli çarpım tablosu kurulmaz; kombinasyon seçilir, saklanmaz. [defter:2026-07-28 PS2 CANLIDA]
- **OFS-03** (eski W-6) — Ofis zorunluluğu API/form katmanındadır (yeni payment/payout → 400); DB kolonları nullable kalır, reversal ve transfer muaftır. [defter:2026-07-28 PS2 CANLIDA]
- **OFS-04** (eski U-10) — Plan ofisi zorunlu değildir; ödemeden KASITLI farktır, boş bırakılabilir. [defter:2026-07-28 PS3-A CANLIDA]
- **OFS-05** (eski W-7, eski D-1) — Ofis `agent → sr → NULL` sırasıyla ön-doldurulur, kilit değildir (kullanıcı ezebilir); **aynı kural frontend'de ve SQL'de AYRI uygulanır, ortak kod yoktur — kural değişirse İKİ yer de güncellenir.** [defter:2026-07-28 PS3-A CANLIDA; 2026-07-28 PS2 CANLIDA]
- **OFS-06** (eski K1) — Rapor anında ofis TAHMİN/ÇIKARIM yapılmaz; plan satırının `expected_office_id`'si NULL ise "(No office)" kovasında GÖRÜNÜR, gizlenmez. OFS-04'ün (plan ofisi zorunlu değil) rapor-tarafı tamamlayıcısı. [defter:2026-07-30 PS3-B CANLIDA]

### SEM — şema / veri

- **SEM-01** (eski H7) — Tek sözlük: `expected_method` / `payout_method` / `payment_method` aynı beş değeri kullanır; kısa sözlük açılmaz. [defter:2026-07-28 PS2 CANLIDA]
- **SEM-02** (eski H-4) — `CURRENCIES` sabiti tek yerde tanımlanır; kopyalar borçtur (kalan kopya sayısı defterde izlenir). [defter:2026-07-28 PS2 CANLIDA]
- **SEM-03** (F, Sentez 13 Eyl) — `users.id` = **uuid**; gerekçe LEENA'nın KENDİ ölçütü (sıralı ID sayım sızdırır · kayıt öncesi üretilebilir · import çakışmaz). `organizers.id` **SERIAL KALIR** (ayrı karar, kuyrukta). Dilim 1'de uygulandı (`bbc69ff`). [defter:2026-09-13 FAZ 4 DİLİM 1 CANLIDA]
- **SEM-04** (G, Sentez 13 Eyl) — `users.password_hash` **nullable**; NULL = "henüz şifre yok". Hash kolonuna hash-OLMAYAN (sentinel) değer yazmak YASAK (veride yalan). İlk Owner NULL + `password_must_change = true`. [defter:2026-09-13 FAZ 4 DİLİM 1 CANLIDA]
- **SEM-05** (H, Sentez 13 Eyl — dilim 2 öncesi BAĞLAYICI) — HEDEF: `organizers` saf kiracı, giriş `users`'a **TAŞINIR** (e-posta/şifre kopyalanmaz, tek-kaynak). YOL: JWT geçişte ikisini taşır (`organizer_id`, `users.organizer_id`'den türetilir); **exp=30d → eski yol dilim 2'den en erken 30 gün sonra emekli (takvim)**. Dilim 2 kapsamı: JWT `user_id`+`name` + **ŞİFRE BELİRLEME AKIŞI** (Owner NULL bootstrap açığı; 401 guard giriş yolu DEĞİL); `ui2CurrentUser()` SENKRON KALIR. [defter:2026-09-13 FAZ 4 DİLİM 1 CANLIDA]
- **SEM-06** (B3, Sentez — RTM nihai, 8 Eki) — `Transferred` TEK statüdür (yalnız devreden kaynak taşır; elle geçiş kapalı, yalnız Transfer aksiyonu yazar). Yön ayrı statüyle değil `transferred_from_contract_id` ile tutulur (devam = yeni `Active` satır; "transferred to" ters join'le türetilir, saklanmaz). [defter:2026-10-08 KENYA ÖLÇÜM PAKETİ + ui2 LİSTE KAPANIŞI]
- **SEM-07** (Faz B b2, Sentez 23 Eki) — Abonelikten çıkış imzası JWT'den BAĞIMSIZ sırla atılır (LIFFY `UNSUBSCRIBE_SECRET`); JWT rotasyonu gönderilmiş e-postalardaki çıkış linklerini bozamaz. Uygulama (liffyv1 `532d173`): imza JWT'ye de sabit değere de düşmez; sır yoksa süreç açılmaz (`FATAL: UNSUBSCRIBE_SECRET missing`). [defter:2026-10-23 FAZ B (b2)]

### LED — ledger (hesaplar · transfer · gider · gelir · bütçe)

- **LED-01** (Ç3, Sentez 8 Eki) — Ödeme yöntemi sözlüğü SEM-01'in 5 değeridir; SWIFT = `bank_transfer`; "kredi bakiyesi" ödeme yöntemi DEĞİL, ledger olayıdır. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-02** (Ç4, Sentez 8 Eki) — Para birimleri bir referans TABLOSUDUR (8 birim, ISO kodu; TL→TRY); koda gömülmez, arayüz listeleri tablodan okur. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-03** (Ç5, Sentez 8 Eki) — "account" = para hesabı (banka / kasa / sanal); Zoho'nun Account'u her yerde "company"dir. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-04** (Ç7, Sentez 8 Eki) — Tek kaynak: her tutar bir kez saklanır; ledger hareketi payout'a / payment'a FK ile bağlanır, tutarı kopyalamaz; gelir `payments`'tan türetilir, ayrı gelir tablosu doğmaz (D2). [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ] · **Çapraz ref (21 Eki):** REQ §2.3 "komisyon = gider" SUPERSEDED; payout tablosu + ledger bağı. [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **LED-05** (Ç8, Sentez 8 Eki) — Kur satırda değişmez; "kur düzeltmesi" = ters kayıt + yeni kayıt. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-06** (boşluk 1, Sentez 8 Eki) — Transfer = tek mantıksal olay, iki bağlı hareket, tek atomik yazım; iki hareket ayrı silinemez/değişemez; bakiye türetilir. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-07** (boşluk 2, Sentez 8 Eki) — Sahibin cari hesabı = "owner" tipinde sanal hesap; cebinden ödenen gider buradan çıkar, eksi bakiye = şirketin sahibe borcu, geri ödeme = banka→owner transferi. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-08** (boşluk 3, Suer 8 Eki) — Gider onayı YOKTUR: gider değiştirilemez olaydır, düzeltme ters kayıttır; onay statüsü/akışı kurulmaz; "kim girebilir" Faz 4 iznidir. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-09** (boşluk 5, Suer 8 Eki) — Bütçeyi Owner kilitler; kilit sonrası değişiklik yalnız yeni revizyondur (eski satırlar superseded, UPDATE yok), kim/ne zaman kaydıyla; kilidi yalnız Owner açar; "kim yazar" Faz 4 iznidir. [defter:2026-10-08 LEDGER KRİTER HÜKÜMLERİ]
- **LED-10** (Paket 1 inşası, 21 Eki — Sentez teyitli 21 Eki) — Hareket (`ledger_entries`) TAM BİR kaynağa bağlıdır (payment / payout / expense / transfer); tutar-kur-EUR YALNIZ transfer bacağında saklanır, diğerlerinde kaynaktan `ledger_lines` view'iyle türetilir — LED-04'ün şema karşılığı, tek türetme yeri (MOT-01 emsali). [defter:2026-10-21 PAKET 1: STAGING'E HAZIR]
- **LED-11** (Paket 1 inşası, 21 Eki — Sentez teyitli 21 Eki) — Hesabın para birimi = hareketin para birimi; uyuşmazlık reddedilir (API 400 + DB trigger). Para birimi çevirmek hesaplar arası transferdir; aynı para biriminde transfer bacakları EŞİTTİR, masraf ayrı giderdir. [defter:2026-10-21 PAKET 1: STAGING'E HAZIR]
- **LED-12** (Paket 1 inşası, 21 Eki — Sentez teyitli 21 Eki; KAPI-2 şartının uygulaması) — Ödeme/payout hesabı: açık hesap (doğrulanır, yanlışsa 400) → ofisin (ofis × para birimi) TEK varsayılan hesabı (`is_office_default`) → yoksa hesapsız kayıt + uyarı. Hesap eksikliği 400 DEĞİLDİR. Ödemede `account_id` dolu ⇔ hareket var. [defter:2026-10-21 PAKET 1: STAGING'E HAZIR]
- **LED-13** (Paket 1 inşası, 21 Eki — Sentez teyitli 21 Eki) — Ters ödeme / kontrat devri satırı hesabı ve payer'ı orijinalden devralır (TAH-01 deseni); ters hareket YALNIZ orijinalin hareketi varsa yazılır; kontrat devri aynı hesapta devir gününde kapama + kopya hareketi yazar (bakiye değişmez). [defter:2026-10-21 PAKET 1: STAGING'E HAZIR]
- **LED-14** (Paket 1 kriteri, 21 Eki) — Ledger öncesi satırlara (canlıda 15 ödeme / 8 payout) geriye dönük hareket YAZILMAZ; ekstre ve özette "ledger dışında" sayacıyla görünür (RAP-02). [defter:2026-10-21 PAKET 1: STAGING'E HAZIR]
- **LED-15** (Paket 1 inşası, 21 Eki — Sentez teyitli 21 Eki; LED-09 uygulaması) — Bütçede her değişiklik yeni revizyondur (PLN-05). Kilidi Owner atar (`users.is_owner`, ui2 oturumu); kilitli aktif revizyonun ardılını YALNIZ Owner yazar (= kilidi açma); kilit kaydı ardıl revizyonda da korunur. Owner-dışı ret HTTP 409 `OWNER_REQUIRED` — 403 DEĞİL (leena-fetch 401/403'te oturumu siler, G45). [defter:2026-10-21 PAKET 1: STAGING'E HAZIR]
- **LED-16** (Paket 1 P1-0, 21 Eki) — 036+ migration'lar YALNIZ `scripts/migrate.js` ile uygulanır (dosya içi `ell.migration_runner` koruması; kaydı runner yazar, dosya yazmaz). Runner DUR koşulları: kayıtlı-dosyasız · kayıtsız-ama-şema-izli (yarım) · numara boşluğu/çakışması · sıra dışı bekleyen · eşzamanlı koşu. [defter:2026-10-21 PAKET 1: STAGING'E HAZIR] · **Not (21 Eki, Paket 1b):** yarım-iz denetimi `CREATE OR REPLACE VIEW/FUNCTION` ile adı geçen VAR OLAN nesneyi de iz sayar → 036+ dosyasında mevcut view/fonksiyon yeniden tanımlanmaz; genişletme yeni nesneyle ya da sorgu tarafında join'le yapılır (041'de `ledger_lines` bu yüzden değişmedi). [defter:2026-10-21 PAKET 1b: STAGING'E HAZIR]
- **LED-17** (Paket 1 inşası, 21 Eki — Sentez teyitli 21 Eki) — Referans tohumu YALNIZ belgeli değerlerdir (REQ:1680/1682/1059 + Zoho referansı §3.7/3.8); tam Zoho listesi (6 kategori × ~75 tip, 15 gelir kategorisi) belgede YOK → admin ekranından girilir. Tohum aktif Owner'ı olan kiracıya yazılır. [defter:2026-10-21 PAKET 1: STAGING'E HAZIR] · **Not (22 Eki, Sentez):** tam liste Zoho CSV'sinden tohumlanır, ZOHO ADIYLA (büyük harf normalize, yazım hatası düzeltilir; çakışmada Zoho kazanır; mevcut 6 kategori Zoho adıyla eşleşir, ID korunur); gelir kategorisi 15, ödemede zorunlu değil, varsayılan "Contract revenue". [defter:2026-10-22 PAKET 1b BELGE KAPANIŞI]
- **LED-18** (Paket 1b P1b-1, 21 Eki — Sentez teyitli 22 Eki) — Gider karşı tarafı bir KAYITTIR (`suppliers`, Suer ilkesi: serbest metin değil seçmeli): tür `supplier | venue | contractor | other` — `expo_partners` rollerinden AYRI sözlük (para karşı tarafı ≠ fuar-operasyon rolü; bağ kurulmaz); ülke `core_countries` FK (zorunlu), ofis ve vergi no isteğe bağlı; SİLİNMEZ, pasiflenir (pasif tedarikçi yeni gidere seçilemez); ad tekliği kiracı × normalize ad × ülke. `expenses.supplier_id` nullable; eski `counterparty` metni kalır (geriye dönük eşleme YOK); ui2 girişi seçmelidir, API metni geriye uyum için kabul eder. [defter:2026-10-21 PAKET 1b: STAGING'E HAZIR]
- **LED-19** (Sentez EK, 21 Eki — Paket 1b P1b-3) — Yapay zeka giderde yalnız taslak yazar; gider insan kabulüyle doğar (YZ-01 + LED-08 birlikte). [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **LED-20** (Paket 1b P1b-1, 21 Eki — Sentez teyitli 22 Eki) — Tedarikçi ödeme geçmişi SAKLANMAZ: gider hareketlerinden (`ledger_lines` → `expenses.supplier_id`) okuma anında türetilir (D2); ters gider tedarikçiyi devralır (geçmişte net sıfır); toplam EUR, girişte donmuş kurla (RAP-01). [defter:2026-10-21 PAKET 1b: STAGING'E HAZIR]
- **LED-21** (Paket 1b P1b-3, 21 Eki — Sentez teyitli 22 Eki) — Gider taslağı (`expense_drafts`): içerik DEĞİŞMEZ ("ne önerildi" kaydı), tek karar `pending → accepted | rejected`, silinmez; eksik alan listesi sunucuda; biçimce yanlış değer "eksik" sayılmaz (400). Kabul = gider yolunun KENDİSİ (`createExpense`, `POST /api/ledger/expenses` ile aynı doğrulama ve mesaj); insanın tamamladığı/düzelttiği değerler doğan gider satırına yazılır. Tedarikçi eşleşmesi (normalize + ILIKE skoru) ÖNERİDİR — giderin tedarikçisini kabulde insan seçer (OFS-05). [defter:2026-10-21 PAKET 1b: STAGING'E HAZIR]

### RAP — raporlama (alan-bağımsız)

> **Sınır:** RAP yalnız ALAN-BAĞIMSIZ raporlama ilkelerini taşır. Bir hüküm tek bir alanı
> (plan, ofis, komisyon, payout) ilgilendiriyorsa O grubun içine yazılır — RAP çöp çekmecesi değildir.
> (Emsal: komisyon raporlaması MOT-05'te yaşar, nakit-plan raporlaması PLN-09/10/11'de.)

- **RAP-01** (eski K9-global) — Tüm raporlama EUR'dadır; başka para biriminde girilen işlem GİRİŞ ANINDAKİ KİLİTLİ KURDAN çevrilir (yeni/bugünkü kur değil). Orijinal para birimi satırda görünür, toplama EUR üzerinden yapılır. Suer iş kuralı; cash-forecast'tan büyük, her rapora uygulanır. [defter:2026-07-30 PS3-B CANLIDA] · **Not — ekran istisnası (Sentez 23 Eki, UI-0 🔶2):** ui2'de tek birimli tutar (EUR karşılığı olmadan) YALNIZ ÜÇ yerde: kalem birim fiyatı · ekstre dönem giriş/çıkış toplamı · gider taslağı tutarı. Para çiftinde EUR karşılığı yoksa "—" yazılır (boş bırakılmaz). Yeni istisna Sentez kararıdır. [defter:2026-10-23 UI-0b HÜKÜMLERİ]
- **RAP-02** (eski K13, eski K15, eski K16) — Rapordan DIŞLANAN veya EKSİK olan hiçbir şey sessizce kaybolmaz; sayaçta görünür. **Alt maddeler:** E1 netleşme yasak (eksik ve fazla birbirini götürmez — yalnız `revenue > plan` toplanır); E2 ayrıklık (her kontrat tek sayaçta, Y∩X=∅). **Not:** teşhis eksenleri (`contracts_unconvertible`, `contracts_missing_revenue_eur`) parent sayaçlarla örtüşebilir — çifte sayım DEĞİL, tasarım gereği. [defter:2026-07-30 PS3-B CANLIDA]
- **RAP-03** (eski K10) — Rapor kapsamı dışlaması KARA LİSTEDİR (beyaz liste DEĞİL): yeni bir statü eklenirse otomatik DAHİL olur, sessizce düşmez. **Not (nakit öngörü örneği):** dışlanan statüler = Transferred + Cancelled + On Hold; İKİ KATMANDA uygulanır (Transferred+Cancelled plan CTE'de tamamen; On Hold gruplamada, RAP-02 sayacında görünür — CTE'de atılsaydı kalanı hesaplanamazdı). **⚠️ AÇIK SORU (bu dilimde ÇÖZÜLMEDİ):** 5. bir statü eklenirse hangi katmana yazılacağı açık karar gerektirir — yanlış katman sessizce "on hold" muamelesi görür. [defter:2026-07-30 PS3-B CANLIDA]

### YON — yönetim / süreç

- **YON-01** — Defterdeki her kayıt TARİHSELDİR: yazıldığı günün ölçümüdür, bugünkü durum değildir. Defterden okunan hiçbir şey güncel durum olarak aktarılmaz; güncel durum yalnız ölçümle bilinir. Kayıt DOĞRU ve düzgün yazılmış olsa bile geçerlidir.
- **YON-02** — Sentez KRİTER yazar, KOMUT yazmaz; dosya yolu / SQL prosedürü / shell adımı Sentez'in işi değildir.
- **YON-03** — Belge commit'i kapanış şartı: push → KB yeniden yükleme (Sentez VE Orchestrator) → deftere tek satır `KB @ <hash>`. Teyit yoksa dilim AÇIK.
- **YON-04** — Para biriminin nasıl raporlanacağı İŞ KARARIDIR; Sentez veremez (uygulama: RAP-01).
- **YON-05** (B, Sentez 9 Eyl) — Bir ölçüm turu bir varsayımı ÇÜRÜTTÜYSE bulgusu aynı turda deftere kısa kayıt girer (ne varsayılıyordu / ne ölçüldü / kanıt file:line|çıktı). Yalnız TEYİT eden ölçüm ayrı kayıt açmaz. [defter:2026-09-09 SUER HÜKÜMLERİ] · **Not (21 Eki):** Sentez'in "yapay zeka mining'in yerini aldı" varsayımı Suer ölçümüyle (261 kişi / 5 e-posta) çürüdü → SAT-01/02. [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **YON-06** (C, Suer 10 Eyl) — LEENA push öncesi İKİ ölçüm: (a) pencere açık mı (kampanya/fuar takvimi), (b) platform sağlığı (status.render.com). Kod riskinin temiz olması deploy riskini KAPATMAZ. Kaynak: 10 Eyl kesintisi. [defter:2026-09-10 WEB KESİNTİSİ]
- **YON-07** (D, Suer 13 Eyl) — Her tasarım kararı çok-kiracı SaaS hassasiyetinde tartılır; hızlı çözüm tercih DEĞİL; en kaliteli seçenek kurulumu aşırı uzatmıyorsa her zaman en doğru yol seçilir. [defter:2026-09-13 FAZ 4 DİLİM 1 CANLIDA]
- **YON-08** (E, Suer 13 Eyl) — LIFFY vazgeçilebilir (kullanıcı/önemli veri yok, kapatılabilir); **LEENA çekirdektir**; LIFFY'yi değiştirmemek için LEENA'da taviz verilmez. [defter:2026-09-13 FAZ 4 DİLİM 1 CANLIDA]
- **YON-09** (I, Sentez 13 Eyl) — Test DB'si tüm veritabanının değil **TEST EDİLEN KODUN** aynasıdır; finans testleri → finans şeması + omurga (`organizers`); email/callcenter evreni girmez; dışla-listesi gerekçeli; yeni EMS migration'ı unutulursa setup GÜRÜLTÜYLE patlar (doğru arıza biçimi, sessiz değil). [defter:2026-09-13 TEST DB SENKRONU]
- **YON-10** (J, Suer 13 Eyl) — Çalışma kuralları: K1 tek iş · K2 çok-aşamalı iş ayrı tur · K3 Suer yazmaz, yapıştırır. Metin LEENA `CLAUDE.md`'de (tek kaynak, `dd116d5`); burada yalnız ATIF. [defter:2026-09-13 FAZ 4 PLANLAMA TURU]
- **YON-11** (madde 8, Sentez 19 Eki) — İş birimi görev paketidir (tek dal / tek merge / tek revert / ui2 ekranı + Suer görsel onayı). Kapılar etki alanına göredir: SERBEST / KAPI-1 (merge = deploy, Suer) / KAPI-2 (auth, boot, worker, mevcut davranış-kolon-trigger, veri değiştiren migration, para tablolarında mevcut satır, sır rotasyonu — Sentez kararı). Ölçüm ve inşa aynı oturumdadır. Geri dönüş iddiası ancak kanıtlanmış restore ile geçerlidir. [defter:2026-10-21 FAZ A / A0]
- **YON-12** (Suer önerisi + Sentez 22 Eki) — Canlı push öncesi YENİ export alınır: (a) veri değiştiren/silen migration varsa · (b) son export 24 saatten eskiyse · (c) KAPI-2 paketlerinde HER ZAMAN. PITR yedek değildir; kanıtlı restore yedektir (YON-11). [defter:2026-10-22 PAKET 1b BELGE KAPANIŞI]

### AD — adlandırma / marka

- **AD-01** (A, Suer 9 Eyl) — **ELIZA** = platformun ürün/marka adı (kullanıcının gördüğü); **ELL** = yalnız iç kod adı (repo/dosya adlarında yaşar); eski bağımsız sistem = **"eliza-legacy"**. LEENA Finance sekmesi yalnız "Finance"; nav'da `liffy`/`leena` küçük etiket. ⚠️ **CUTOFF: Bu kayıttan ÖNCEKİ tüm defter/kod kayıtlarında ELIZA = eliza-legacy.** [defter:2026-09-09 SUER HÜKÜMLERİ] · **Not (8 Eki):** eliza-legacy emekli = üzerine inşa edilmez; birleşmeye kadar okuma aracı olarak serviste. [defter:2026-10-08 SENTEZ KAPANIŞ KARARLARI + 034 (dal)]

### YZ — yapay zeka (yeni grup, 2026-10-21)

- **YZ-01** (Suer, 21 Eki) — Çalışma anındaki yapay zeka iş verisi YAZMAZ, yalnız okur; ürettiği her şey insan onayıyla girer; yapay zekasız yapılabilen yapay zekasız yapılır. Claude Code'un inşa zincirinde kod/migration yazması kapsam DIŞI. [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **YZ-02** (Suer D5 = b, 3 şart; 21 Eki) — Veri paylaşımı: yalnız şirket kontrolündeki entegre hesap (API); şifre/anahtar/bağlantı dizesi ASLA; kişisel yapay zeka hesaplarına şirket verisi girmez; ajan isteyen kullanıcının kapsamını aşmaz; sağlayıcı eğitimde-kullanmama şartı açılışta teyit (ölçülmedi). [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **YZ-03** (teknoloji turu, 21 Eki) — Her yapay zeka yüzeyi mevcut API'lerin istemcisi (2026-07-21 uzantısı); bot yazması = onay diyaloğu sonrası deterministik kayıt; L-3 gider API'si gün-1 bot-yazılabilir. GEÇİCİ: rapor modülü gelene kadar özel sorular salt-okunur bağlantıyla yapay zekaya, yalnız Owner. [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]

### SAT — satış tarafı kazanım ve sahiplik (yeni grup, 2026-10-21)

- **SAT-01** (Suer 21 Eki 16:51) — Lead/kontak/katılımcı kaydı e-posta ister. E-postasız bulgu ayrı "ikincil kayıt" tablosunda ("doğrudan e-posta yok"), kampanyaya giremez, lead sayılmaz; "e-postalarını bul" aksiyonu takılabilir; e-posta bulununca insan onayıyla terfi. Mükerrer: ad+şirket+ülke(+LinkedIn URL). [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **SAT-02** (teknoloji turu, 21 Eki) — Kazanım boru hattı SABİT (istek → şablon → bekleme masası → içeri al), bulucu DEĞİŞTİRİLEBİLİR; ELL içinde bulucu yazılmaz; dış araçla sistem entegrasyonu şart değil; mevcut robota geliştirme yok, verimi/servisi/maliyeti ölçülür (açık). [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **SAT-03** (teknoloji turu, 21 Eki) — Sahiplik ve havuz TABLODAN: ayrılan → havuz; N gün iletişimsiz → uyarı → havuz → yeniden dağıtım; info@/web form → ülke→ofis tablosu; Owner değiştirir, kod değişmez; önkoşul olay kaydı; N ve tablolar dilim gelince Suer'den. [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]
- **SAT-04** (teknoloji turu, 21 Eki) — Bölge yasağı TABLODAN (ofis/kullanıcı → satabileceği ülkeler); atama kuralı + yetki girdisi (Faz 4); Owner kararı, değişken. [defter:2026-10-21 TEKNOLOJİ GÜNCELLEME TURU]

### YET — yetki, kullanıcı yönetimi, denetim (yeni grup, 2026-10-22, Paket 2)

- **YET-01** (Paket 2 P2-2, 22 Eki — Sentez teyitli 23 Eki) — Yetki çözümlemesi TEK yerdedir (`utils/permissions.js`): etkin yetki = rol şablonu (`role_permissions`) + kişi başı ezme (`user_permissions`: grant kapsamıyla ekler/değiştirir, revoke kaldırır). Route'lar rol ADINI kontrol etmez (B9; Owner şablonu `roles.owner_template` bayrağıyla tanınır). Owner (`users.is_owner`) kısa devredir, ezme yazılamaz (DB), değiştirilemez (B10); kısa devre yalnız yetkiyi atlar, iş doğrulaması koşar (B25). Kayıt defteri (`permissions`, kod `<module>.<action>`, eylem read|write|approve — B22) sistem geneldir, `organizer_id` taşımaz. [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]
- **YET-02** (Paket 2 P2-3, 22 Eki — Sentez teyitli 23 Eki) — Güvenlik sınırı SUNUCUDADIR: `requirePermission(kod)` bu pakette yalnız ledger yazma · gider taslakları · payout yazma · `/api/users` uçlarında; EMS / contracts / payments uçları kapısız (eskisi gibi). Ret 409 + kod (`PERMISSION_REQUIRED` · `OUT_OF_SCOPE` · `NOT_USER_SESSION` · `SELF_EDIT` · `OWNER_FIXED`) — 403 DEĞİL (G45). Eski token (user_id YOK) kapılı uçta 409 köprüsü. Migration öncesi (043–045 yok) kapı eski davranışa düşer. Menü gizleme (`ui2CanSee`, /me özeti) yalnız UX'tir. [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]
- **YET-03** (Paket 2 P2-2, 22 Eki — Sentez teyitli 23 Eki) — Kapsam own | team | office | all, kaydın hedefiyle denetlenir: ledger'da HESAP üzerinden (ofis = hesabın ofisi, own/team = hesabı açan; taslak kabulü dahil), tedarikçide tedarikçinin ofisi, payout'ta ödeyen ofis. Ofis boyutu olmayan kayıt (referans veri, bütçe) yalnız `all` ile yazılır. Ofissiz kullanıcının ofis kapsamı BOŞTUR (sessiz genişleme yok). `team` = kişinin kendisi (`reports_to` yok). SAT-04 bölge filtresi yuvası (`regionFilter`) office/team çözülürken çağrılır, bugün süzgeci değiştirmez. [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]
- **YET-04** (Paket 2 P2-2, 22 Eki — Sentez teyitli 23 Eki) — 5 sistem şablonu (Owner · Finance · Project · Office Manager · Sales) DEĞİŞMEZ ve silinmez (B27/B28, DB trigger; yalnız runner'lı migration değiştirir); kişiye özel fark kişi başı ezmeyle verilir. Şablon kullanıcıya CANLI bağlıdır — sistem şablonu değişmediği için REQ §3.1 "anlık görüntü" ilkesiyle bugün çelişmez; özel şablon (admin ekranı) bu pakette YOK, gelince bu nokta karar ister. [defter:2026-10-22 PAKET 2: STAGING'E HAZIR] · **Not (Sentez 23 Eki):** sistem şablonu düzenlenebilir olduğu gün bu hüküm ÖNCE yeniden açılır. [defter:2026-10-23 UI-0b HÜKÜMLERİ]
- **YET-05** (Paket 2 P2-1, 22 Eki — Sentez teyitli 23 Eki) — Davet: Owner/yetkili e-posta girer → `users` satırı (şifre NULL, SEM-04) + tek kullanımlık token (DB'de YALNIZ SHA-256 özeti, 72 saat; yeniden davet ve pasifleştirme açık daveti iptal eder). Link token'ı URL FRAGMENT'ında taşır (sunucu loguna / Referer'a düşmez, B20); link tabanı yalnız izinli origin. Geçersiz / kullanılmış / iptal / süresi geçmiş → tek tip genel hata. E-posta `email_queue` transactional satırı (campaign_id NULL). `INVITE_ECHO=1` yalnız staging; bayraksız ortamda link yanıta da loga da yazılmaz. [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]
- **YET-06** (Paket 2 P2-1, 22 Eki — Sentez teyitli 23 Eki) — Pasif kullanıcı giremez; eldeki token'ı HER korumalı uçta 401 alır (`authMiddleware`, yalnız user_id taşıyan token'da tek PK sorgusu; klasik token DB'ye gitmez — KAPI-2). Pasifleştirme sebep ister (B12) ve denetlenir; kimse kendini pasifleştiremez; Owner'ı yalnız Owner pasifleştirir; son aktif Owner pasifleştirilemez (B10, 032 trigger'ı). [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]
- **YET-07** (Paket 2 P2-2, 22 Eki — Sentez teyitli 23 Eki) — B32: kimse kendi şablonunu, yetkisini ve ofisini (ofis = kapsam girdisi) değiştiremez, Owner dahil. Owner olmayan yetkili, kendinde olmayan yetkiyi ya da kendi kapsamından genişini veremez (şablon ataması dahil). `is_owner` verme/alma bu pakette YOK (B24 korumalı işlem). [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]
- **YET-08** (Paket 2 P2-4, 22 Eki — Sentez teyitli 23 Eki) — `audit_log` YALNIZ EKLENİR (UPDATE/DELETE/TRUNCATE reddedilir): kim · ne (`<alan>.<olay>`) · ne zaman · hedef · sebep · diff özeti. Bu pakette yazılan olaylar: davet / yeniden davet / davet kabulü · aktif/pasif · profil (ofis, ad, temsilci bağı) · şablon · kişi başı yetki set/clear · bütçe kilidi (LED-15). Olay ile kayıt aynı transaction'dadır. Kullanıcı detayındaki geçmiş yalnız Owner'a görünür (REQ §3.1 "View Audit Log — Owner by default"). [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]
- **YET-09** (Paket 2 P2-1, 22 Eki — Sentez teyitli 23 Eki) — Kullanıcı ↔ satış temsilcisi bağı (`sales_agents.user_id`) geriye dönük YALNIZ tek eşleşmede doldurulur (aynı kiracıda e-postası tam bir internal temsilciyle eşleşen kullanıcı); çoklu eşleşme boş kalır, sayısı defterde; external temsilci bağlanmaz. Yeni bağ seçmelidir — e-posta eşleşmesi ÖNERİDİR (OFS-05). [defter:2026-10-22 PAKET 2: STAGING'E HAZIR]

### UI — arayüz (yeni grup, 2026-10-22, Sentez — UI-0)

> Sentez hükümleri **aynen** (UI-0 kriter turu, 22 Eki). Kural metni + UI-0 kabul ölçütleri:
> `ELIZA_UI2_ARAYUZ_KURALLARI_v1.md`. Bilgi mimarisi karşılığı: `ELL_BILGI_MIMARISI_v4.md` §4.

- **UI-01** (Sentez 22 Eki) — YERLEŞİM: üst sekme BM §1'den, alt menü §2/3/4 bölümlerinden türetilir. Bölümde yeri olmayan ekran = IA değişikliği → önce BM yaması, sonra ekran. Finance alt menüsü §4 gruplarıyla kümelenir: Executive (özet) · Contracts (kontratlar, komisyonlar, agent'lar) · Money (hesaplar, ekstre, transferler, giderler, tedarikçiler, gider TASLAKLARI) · Expo Finance (bütçe). [defter:2026-10-22 UI-0 KRİTERLERİ]
- **UI-02** (Sentez 22 Eki) — NAV TEK KAYNAK: nav.json (id · domain · grup · etiket · yol · durum canlı|yer-tutucu · permission kodu); shell.js yalnız okur. Rol alanı BOŞ DEĞİL: Paket 2'nin permission koduna bağlanır (ui2CanSee etkin yetkiyi okur, P2-3). Test iki yönlü: nav'daki her yol var + ui2'deki her sayfa nav'da; "6 öğe" sayı testi silinir. [defter:2026-10-22 UI-0 KRİTERLERİ] · **Güncelleme (Sentez 23 Eki, UI-0 🔶3 kabul):** alan listesi `group` · `label` · `path` · `status` · `permission` + `parent` · `legacy` · `landing` · `userOnly`; `userOnly` = yalnız ui2 (kullanıcı) oturumunda görünür, klasik oturumda gizli. **Köprü (🔶1, GEÇİCİ):** ui2 ikizi olmayan ekran klasik ekrana köprülenebilir — öğe `legacy=true` + `status=placeholder`; klasik ekran bağlantısı YALNIZ nav.json'dan gelir (sayfaya gömülmez). [defter:2026-10-23 UI-0b HÜKÜMLERİ]
- **UI-03** (Sentez 22 Eki) — DÖRT ŞABLON: Liste · Detay · Form · Özet kartları (tek stat-card, tıklayınca kayda iner — D2'nin ekran karşılığı). Bileşenler YALNIZ components.js'ten; test bunu sınar. "Para çifti" (işlem birimi + EUR) ayrı bileşen, Finance'ta zorunlu (RAP-01 ekran karşılığı). [defter:2026-10-22 UI-0 KRİTERLERİ] · **Not (Sentez 23 Eki):** EUR karşılığı yoksa çift "—" gösterir; tek birim istisnaları RAP-01 notunda (üç yer). [defter:2026-10-23 UI-0b HÜKÜMLERİ]
- **UI-04** (Sentez 22 Eki) — TOKENS: tek tokens.css (renk/yazı/boşluk), tema html[data-theme]; sayfalarda sabit hex YASAK (grep ile ölçülür, kabul ölçütü). [defter:2026-10-22 UI-0 KRİTERLERİ]
- **UI-05** (Sentez 22 Eki) — NİHAİ ARAYÜZ: giydirme ŞİMDİ, düz HTML/JS, derleme yok (K-G). React/Next (brief §8) ERTELENDİ; yeniden tartı tetiği: Sales alanının (LIFFY) ui2'ye taşınma kararı. [defter:2026-10-22 UI-0 KRİTERLERİ]
- **UI-06** (Sentez 22 Eki) — ORGANIZER ANA PANELİ: ui2'de YENİ sayfa olacak — UI-0 DIŞINDA (UI-1 adayı). UI-0 asgarisi: ui2 girişi → Finance özet; Sales/Operations sekmeleri boş-durum ekranı, ölü link değil. [defter:2026-10-22 UI-0 KRİTERLERİ]
- **AÇIK SORULAR — KAPANDI** (Sentez 22 Eki): taslaklar = gider taslakları → Money · Intelligence ui2'de YOK · Commissions & Agents → Contracts grubu, ui2 ikizi yok (UI-1 adayı). [defter:2026-10-22 UI-0 KRİTERLERİ]

### KAT — katalog / quote → kontrat köprüsü (yeni grup, 2026-10-24, Paket 3)

> Sentez Paket 3 kriter turunun (24 Eki) bu pakette doğan hükümleri. Gelir brüt / matrah net hükmü TAH-05'te.
> Kapılar: LEENA tarafı KAPI-2 (authMiddleware + L4), LIFFY tarafı SERBEST.

- **KAT-01** (Paket 3 hüküm 1 — Suer S1, Sentez 24 Eki) — Katalog kaynağı Zoho Products dışa aktarımıdır (Suer CSV); pazar-kopyası ürünler TEK ürün + `product_prices` (ürün × ofis × para birimi — LIFFY 050 şeması) olarak normalize edilir. Tohum AYRI ve idempotent dosyadır (`ON CONFLICT DO NOTHING`); test ürünü + 2 test quote KALIR (S8 E2E çapası), tohum sonrası sayım deftere. [defter:2026-10-24 PAKET 3 KRİTER TURU]
- **KAT-02** (Paket 3 hüküm 2, Sentez 24 Eki) — RF bayrağı ÜRÜN kaydındadır (`products.is_registration_fee`, varsayılan false); convert anında satıra DONMUŞ kopya olarak geçer (L2a). Kod önekiyle türetme YOKTUR (sessiz hata). `product_code` = `products.code`. [defter:2026-10-24 PAKET 3 KRİTER TURU]
- **KAT-03** (Paket 3 hüküm 4, Sentez 24 Eki) — Expo'nun tek kaynağı LEENA'dır: LIFFY expo YARATMAZ, LEENA'dan salt-okunur kopya çeker (`published_to_liffy`); quote'ta `canonical_expo_id` ZORUNLUDUR, convert onunla `contracts.expo_id` gerçek FK'sını doldurur. [defter:2026-10-24 PAKET 3 KRİTER TURU]
- **KAT-04** (Paket 3 hüküm 6, Sentez 24 Eki) — Convert = LIFFY PUSH → LEENA `POST /api/contracts/convert`; idempotency anahtarı `source_quote_id` (ikinci gönderim 409); `line_items` ZORUNLU (L3 kapanır — satırsız 400). Gönderici tarafı outbox'tır (`quotes.convert_status` pending|sent|acked|failed + retry + elle yeniden gönder); sign anında otomatik gönderim. [defter:2026-10-24 PAKET 3 KRİTER TURU]
- **KAT-05** (Paket 3 hüküm 6, Sentez 24 Eki — KAPI-2) — Sistemler arası çağrı SERVİS KİMLİĞİYLE yapılır: LEENA `users` satırı `is_service = true` (şifre NULL, giriş yolu yok, davet yok); istek HMAC imzalıdır, paylaşılan sır env'den, JWT'den BAĞIMSIZ (SEM-07 ilkesi); token uzun ömürlü değildir. Servis kimliği YALNIZ izinli uçlarda geçer (P3-1: yalnız convert), diğer her uç reddeder. [defter:2026-10-24 PAKET 3 KRİTER TURU]
- **KAT-06** (Paket 3 hüküm 5 — Suer S3, Sentez 24 Eki) — Bölge yasağı LEENA'da TABLODUR (`sellable_territories`: ofis × ülke; koda gömülmez — OFS-01/S-16r); Owner ui2 admin ekranından doldurur. LIFFY'de UYGULAMA Paket 4'tedir (tek giriş sonrası). SAT-04'ün tablo karşılığı. [defter:2026-10-24 PAKET 3 KRİTER TURU]
