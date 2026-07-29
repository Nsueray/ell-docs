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
> **Kütük dışı namespace'ler:** `K`/`V`/`T` = test ve görsel-tur ID'leri, kural değil.
> Tiresiz `S1..S9` (açık soru takibi) · `D1..D4` (agent import kararı) · `D2` (D2 mimari ilkesi)
> AYRI namespace'lerdir — arama deseni tire'yi zorunlu tutmalı, gevşetilirse çöp girer.
> **YON grubu bu turda boş** — süreç hükümleri deftere ID'li geçmemiş.

### MOT — komisyon motoru

- **MOT-01** (eski S-8) — Dilim CTE'leri `utils/commissionSlices.js → SLICE_CTES`'te tek kaynaktır; ikinci komisyon formülü açılmaz. [defter:660]
- **MOT-02** (eski S-8) — Komisyon tahsilat oranına bağlıdır (`paid_eur/revenue_eur`), vade planına DEĞİL. [defter:762]
- **MOT-03** (eski U1a) — Tavan kümülatif-marjinal uygulanır ve dilimlere "(cap)" notuyla yansır. [defter:559]
- **MOT-04** (eski U2a) — Kesim takvim günüdür (`payment_date` DATE, TZ yok). [defter:559]
- **MOT-05** (eski U3a) — Rapor yalnız hak edilmişi gösterir; potansiyel detayda kalır. [defter:560]

### TAH — tahsilat / ödeme girişi

- **TAH-01** (eski W-8) — Reversal ve transfer satırında ofis/method sunucuda orijinalden devralınır; istemciden gelen değer yok sayılır. [defter:801]
- **TAH-02** (eski W-9) — Add-payment tarihi bugünle ön-doldurulur; sunucuda tarih zorlaması yoktur. [defter:836]
- **TAH-03** (eski W-10) — Tek ödeme formu vardır (`contract-detail.html`); satır içi hızlı form açılmaz. [defter:838]
- **TAH-04** (eski S-6) — `payments.schedule_item_id` kolonu vardır ama ödeme↔kalem eşleştirme mantığı bilinçli olarak YOKTUR. [defter:747]

### ODE — payout / cari hesap

- **ODE-01** (eski S-1) — Payout modeli CARİ HESAPTIR; kayıtta dönem/kesim kolonu yoktur, bakiye her okumada türetilir. [defter:642]
- **ODE-02** (eski S-3) — Clawback ayrı mekanizma değildir; fazla ödeme bakiyeyi negatife düşürür, sonraki ödemede mahsuplaşır. [defter:656]
- **ODE-03** (eski S-4) — Payout immutable'dır; UPDATE/DELETE yok, düzeltme = negatif tutarlı yeni satır + `reverses_payout_id`. [defter:658]

### PLN — vade planı

- **PLN-01** (eski S-1) — Yarım plan yasaktır; `contract_date`/`expo_id`/`expo.start_date`/`revenue`'dan biri NULL ise 400 + 0 satır. [defter:755]
- **PLN-02** (eski S-2) — `d2 <= d1` ise tek kalem %100 @ d1; değilse %40 @ d1 + kalan @ d2. [defter:752]
- **PLN-03** (eski S-3) — Yuvarlama artığı ikinci kaleme yazılır; Σ kalem ≡ revenue TAM olur. [defter:754]
- **PLN-04** (eski S-4) — Planda kur dondurulmaz; `exchange_rate`/`amount_eur` kolonu yoktur, tutar kontrat para birimindedir. [defter:725]
- **PLN-05** (eski S-5, eski H3) — Tutar/tarih ASLA UPDATE edilmez; revizyonda eski satırlar `superseded_at` damgalanır, yeni satırlar `revision = max+1` ile eklenir. [defter:727, 929]
- **PLN-06** (eski S-7) — Ödeme durumu saklanmaz; "ödenmemiş" = Σ schedule > Σ payments olarak kontrat seviyesinde türetilir. [defter:730]
- **PLN-07** (eski S-9) — Σ ≠ revenue engellenmez; elle girişte uyuşmazlık kabul edilir, yanıtta `warning` döner. [defter:760]
- **PLN-08** (eski S-13r) — Plan ≠ gerçektir; plan ofisi ile ödeme ofisinin eşleşmesi zorlanmaz, uyarı üretilmez. [defter:724]

### OFS — ofis

- **OFS-01** (eski S-16r) — Ofis listesi koda gömülmez; enum/CHECK/frontend sabiti yoktur, tüketici `GET /api/offices`'ten okur. [defter:739]
- **OFS-02** (eski S-11r) — Ofis × para birimi × tahsilat şekli çarpım tablosu kurulmaz; kombinasyon seçilir, saklanmaz. [defter:738]
- **OFS-03** (eski W-6) — Ofis zorunluluğu API/form katmanındadır (yeni payment/payout → 400); DB kolonları nullable kalır, reversal ve transfer muaftır. [defter:807]
- **OFS-04** (eski U-10) — Plan ofisi zorunlu değildir; ödemeden KASITLI farktır, boş bırakılabilir. [defter:882]
- **OFS-05** (eski W-7, eski D-1) — Ofis `agent → sr → NULL` sırasıyla ön-doldurulur, kilit değildir (kullanıcı ezebilir); **aynı kural frontend'de ve SQL'de AYRI uygulanır, ortak kod yoktur — kural değişirse İKİ yer de güncellenir.** [defter:831, 872]

### SEM — şema / veri

- **SEM-01** (eski H7) — Tek sözlük: `expected_method` / `payout_method` / `payment_method` aynı beş değeri kullanır; kısa sözlük açılmaz. [defter:742, 798]
- **SEM-02** (eski H-4) — `CURRENCIES` sabiti tek yerde tanımlanır; kopyalar borçtur (kalan kopya sayısı defterde izlenir). [defter:841]

### YON — yönetim / süreç

- *(bu turda boş — deftere ID'li geçmiş süreç hükmü yok)*
