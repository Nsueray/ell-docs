# ELL Mimari — Aşama 1: Sistem Topolojisi

**Sürüm:** v1.1 — Final
**Onaylanma tarihi:** 2026-05-11
**Onaylayan:** Suer (Owner)
**Durum:** ✅ Approved — locked
**Doküman türü:** Mimari karar — Aşama 1
**Ön koşul:** ELAN_EXPO_REQUIREMENTS_v1_0 (kanonik ihtiyaç dokümanı), DECISIONS_LOG (D1–D42)
**Kapsam:** ELL platformunun en yüksek seviyeli yapısal kararları — kaç uygulama, hangi veri nerede, aralarındaki köprüler, kullanıcı deneyimi, finansal sistemin invariantları.
**Kapsam dışı:** Tablo şemaları, API kontratları, state machine detayları, migration sırası, frontend kütüphane seçimleri, deployment topolojisi. Bunlar sonraki aşamaların işidir.

**v1.0 → v1.1 amendment (2026-05-11):** Requirements-Claude review'undan sonra altı eksik nokta kapatıldı: (1) Sales agent attribution Akış B'ye eklendi (D41 karşılığı); (2) Akış B'de LIFFY companies fuzzy match arama prensibi eklendi; (3) UX prototype reddedilirse senaryosu yazıldı; (4) A22'de "mimari Phase 1 minimum tanımı yapabilir" netleşti; (5) Lapsed customer lifecycle açık konu olarak eklendi; (6) Disaster recovery açık konu olarak eklendi.

**Bu doküman v1.1 olarak finalize edilmiştir. Aşama 2 ve sonraki aşamalar bu dokümanı **kanonik referans** olarak kullanır. Aşama 1'e dönüş ancak resmi bir amendment (v1.2) ile mümkündür; bu nadir bir durum olmalıdır.**

---

## 0. Bu mimarinin yöntem beyanı

Bu doküman bir mimari karardır, ama **iki kaynaktan** beslenir ve bunu saklamayız:

**Kaynak 1 — Requirements (ELAN_EXPO_REQUIREMENTS_v1_0):** İşin gerçek ihtiyaçları, Suer ile çok seanslı görüşmelerden derlenmiş 42+ karar.

**Kaynak 2 — Pragmatic kısıtlar:**
- LEENA production'da, visitor / floor plan / check-in canlı kullanılıyor. Bozulamaz.
- LIFFY'nin altyapısı (mining, SendGrid, sequence engine, reply detection) çalışır durumda.
- Eski ELIZA'nın AI engine ve WhatsApp bot kodu port edilebilir kalitede.
- Suer'in günlük WhatsApp bot kullanımı kesintisiz devam etmeli.

Saf requirements'tan bakıldığında, **tek monolith uygulama + iki SendGrid hesabı + tek codebase** de geçerli bir cevap olurdu. Email deliverability izolasyonu kod ayrımını değil altyapı ayrımını gerektirir. Onu seçmiyoruz çünkü mevcut çalışan sistemleri sıfırdan yazmaya değecek operasyonel yarar yok.

**Bu beyanın pratik sonucu:** Aşağıdaki kararların bazıları "requirements bunu gerektirdi" değil, **"requirements bunu gerektirmiyor ama mevcut sistem böyle, biz de pragmatic olarak koruduk"** anlamına gelebilir. Her kararın gerekçesinde bu ayrım korunur.

Eğer bir gün pragmatic kısıt değişirse (örn. mevcut LIFFY kodu maintenance açısından artık taşınmıyor), mimari yeniden değerlendirilir. Bu doküman donmuş değil; içinde **bilinçli pragmatik tercihler** var.

---

## 1. Mimarinin felsefesi

### 1.1 Neden iki uygulama, üç değil

**Gerekçe:** Hem requirements (gerçek iş ayrımı), hem pragmatic (mevcut sistemlerin doğal kümeleri).

İşin gerçek kesimi iki:

- **"Müşteri olmadan önceki dünya"** — soğuk lead'ler, mass marketing, mining, sequence, quote oluşturma ve imzalama. Sales rep'lerin günlük dünyası.
- **"Müşteri olduktan sonraki dünya"** — Contract resmi, stand atanıyor, tahsilat yapılıyor, catalogue, badge, fuara gelir, raporlanır. Project, Finance, Owner'ın dünyası.

İki dünya arasında **geçiş bölgesi:** quote signed ama henüz convert edilmemiş kayıtlar.

**Bu ayrım veri modeline kadar iner:** LIFFY'nin company kavramı (prospect/potential) ile LEENA'nın customer_company kavramı **farklı entity'lerdir**. Aynı gerçek-dünya şirketi her iki yerde de bulunabilir; convert anında LEENA'da yeni customer_company yaratılır veya mevcutla eşleşir. İki dünyanın ayrılığı veri yapısında da korunur.

### 1.2 Neden ELIZA çatı

**Gerekçe: Tamamen branding kararı, mimari gerekçe değil.** Suer'in tercihi: ELIZA bugün aktif kullanılıyor, markaya kişisel bağ var.

Bu mimari ELIZA'nın **kodunu emekli ediyor** (AI engine, WhatsApp bot, War Room → LEENA'ya port; Zoho-sync → migration boyunca eski repo, sonra emekli). Ama **kullanıcı yüzünde ELIZA markası kalıyor**.

**ELIZA'nın teknik karşılığı:** Ayrı servis değil, **LEENA'nın bir alt modülü**. Login sayfası, üst navigation, role-based landing logic — hepsi LEENA içinde. LIFFY'ye geçiş LEENA'nın yönlendirmesi ile.

### 1.3 Neden LIFFY ayrı bir uygulama

**Gerekçe:** Yarısı somut requirements (email izolasyonu), yarısı pragmatic (mevcut kodun ayrılığı).

Somut, ölçülebilir sebep: **email deliverability izolasyonu**.

- LEENA email trafiği: imzalı müşterilere operasyonel. Spam riski çok düşük.
- LIFFY email trafiği: 80K+ mass marketing. Spam riski yapısal olarak yüksek.

Aynı SendGrid hesabını, domain'i, IP havuzunu paylaşamazlar.

**Dürüst eklenmesi gereken:** Bu argüman kod ayrımını değil altyapı ayrımını gerektirir. Kod ayrımının asıl sebebi LIFFY'nin mevcut kodu zaten ayrı; yeniden yazma maliyeti birleşik mimarinin marjinal getirisini aşıyor. Bu pragmatic kısıt.

### 1.4 Neden tek DB değil

**Gerekçe:** Requirements + pragmatic.

LEENA içinde cross-modül sorgu çok (visitor + contract + revenue + floor plan), tek DB şart. LIFFY'nin LEENA ile arasında köprüler az.

**Bu kararın maliyetleri var — Bölüm 5.4'te listelenir.**

### 1.5 Finance invariants — kodun disiplini

LEENA'nın finansal sistemi sadece schema değildir; **kodun yazımına da kural koyar**. Üç invariant her finance feature'ın altında yatar:

**Invariant 1 — Two-sided money movement (D34'ün finance kuzeni):**

Her para hareketi iki ayağı olan bir kayıttır. Tek taraflı kayıt yasak.

- Müşteri €5000 ödedi → Banka hesabı +€5000, müşteri credit -€5000 (veya contract balance -€5000)
- Sales rep'e komisyon €1000 ödendi → Banka -€1000, sales rep credit -€1000
- Owner'dan şirket kasasına €10000 transfer → Owner current account -€10000, Şirket kasası +€10000

Tek bir kayıtla "para girdi" denmez. Para nereden geldi, nereye gitti — iki ucu da yazılı olur. Bu invariant Zoho'nun en büyük problemini çözer (Zoho'da bakiyeler aniden değişebiliyor, "para nereden gelmiş" izi sürülemiyor).

**Invariant 2 — Computed balances, not stored:**

Hesapların bakiyesi tabloda **kayıt** olarak tutulmaz, **hesaplanır** (sum of transactions). Bir field "current_balance" olarak saklanmaz.

Sebep: Bakiye depolanırsa, bir transaction silinince/değişince bakiye eski kalır → corruption. Computed balance her zaman gerçek.

Performans endişesi olursa **materialized view** veya **rapor-zamanı cache** kullanılır — ama master truth her zaman transaction sum'ı, asla manuel updated edilen bir field değil.

Bu invariant'ı bozmak büyük cazibe taşır ("performans için bir tane current_balance field'ı eklesek"). Mimari "hayır" der.

**Invariant 3 — Frozen exchange rates per transaction (D34):**

Her finansal transaction kendi exchange rate'ini tutar; bu rate bir kez kaydedildikten sonra değişmez. Sonraki kur dalgalanmaları geçmiş transaction'ları etkilemez.

Mart 1'de €5000 = $5400 olarak girilmişse, Mart 15'te dolar düşse de bu transaction $5400 olarak kalır. Yeni transaction'lar yeni kur kullanır, ama eskiler donmuş.

Bu, A14'ün (pricing snapshot) finance versiyonu. Pricing ve currency birlikte donmuş bir sistem oluşturur.

**Üç invariant'ın birleşik sonucu:** ELL'in finance kodu **deterministic ve auditable** olur. Her tutar her zaman "şu transaction'lar var, toplamı bu" şeklinde açıklanabilir. Zoho'da bu yok — bizim bunu garanti etmemiz lazım.

---

## 2. LEENA — Ana gövde

LEENA bu mimaride **operasyon + finance + intelligence + auth + ELIZA çatı submodule**.

### 2.1 LEENA'nın içinde ne var

**Bugünden korunan (production, dokunulmuyor):**
- Expo master record
- Visitor management (registration, QR, badge, conference, re-activation)
- Floor Plan Builder
- Check-in (terminal, QR scan, lead scanner)
- Mevcut email infrastructure (LIFFY'ninkinden ayrı SendGrid hesabı)

**Eski ELIZA'dan port edilen:**
- AI query engine
- WhatsApp bot (LEENA içinde yaşar, LIFFY verilerini liffy_daily_metrics + notifications stream üzerinden okur — doğrudan LIFFY API çağrısı yapmaz)
- War Room dashboard
- Risk engine, expo metrics view
- Reference data master (countries, sectors, currencies, languages)
- Zoho-sync (geçici, migration süresince — sonra emekli)

**Yeni inşa edilecek:**
- **customer_companies** ve **customer_contacts** (müşteri dünyası — LIFFY prospect'inden ayrı entity)
- **sales_agents tablosu** (system user olmayan dış ajans/freelance acenteler — D41 karşılığı, A28)
- Sales Contract — **iki giriş yolu desteklenir:** (a) Köprü 1'den gelen pending convert listesinden; (b) Project'in sıfırdan yarattığı contract (signed quote olmadan da)
- Revenue (multi-account, two-sided money movement — Invariant 1)
- Expense (kategorize, expo-attributed, multi-currency, frozen exchange rate — Invariant 3)
- Multi-account ledger (computed balances — Invariant 2)
- Owner's current account
- Commission engine (Agent + SR + SD, preset + override, payment tracking; hem sales rep hem sales agent için)
- Quote → Contract conversion gate (convert sırasında customer_company yaratımı/eşleşmesi dahil)
- Manual contract creation flow (üç sales attribution kategorisi: sales rep / sales agent / Project department veya Elan Expo)
- 8-mail Announcement chain
- **Catalogue MVP — Phase 1 minimum:** exhibitor submission + storage + basic list view (PDF export, web catalogue, template editor Phase 2'ye kalır)
- Audit log (resilient writes, 24-month rolling)
- Users + permission matrix + hierarchy (auth sahibi — LIFFY de buradan okur; sales_agents bu tabloda yer almaz)
- Auth servisi (JWT üretimi)
- **ELIZA çatı submodule** (login + üst navigation + role-based landing)
- Manager raporları (scope-aware, liffy_daily_metrics tablosunu okuyan)
- `liffy_daily_metrics` tablosu (LIFFY'den nightly push ile beslenen)
- Search global
- Notification merkezi (real-time event stream dahil)
- Product katalogu + pricing
- `stand_reservations` tablosu (floor plan'dan ayrı entity)

### 2.2 LEENA'nın sınırı

- Lead yönetimi yapmaz
- Mass marketing email göndermez
- Mining, sequence, action engine yok
- Quote entity'si LEENA'da doğmaz (LIFFY'de doğar). Akış B'de (Bölüm 6.5) Yaprak signed quote olmadan **doğrudan contract** yaratabilir — bu durumda LIFFY `quotes` tablosuna hiç kayıt düşmez; pricing snapshot LEENA'da contract line item'larına manuel oluşturulur.

### 2.3 LEENA'nın geleceği

LEENA, ELL'in **gerçek kalbi**. LIFFY zamanla başka araca devredilse, LEENA Elan Expo'yu çalıştırmaya devam eder. Bu yüzden LEENA'nın mimari yatırımı en yüksek.

---

## 3. LIFFY — Sales workspace

LIFFY bu mimaride **sales workspace**: sales rep'in günlük çalışma ekranı. Action Engine + quote + lead follow-up + reply handling ana değer. Mining ve mass campaign bunun arkasında background araç olarak kalır.

### 3.1 Adoption riski — operasyonel önkoşul ve LEENA fallback

LIFFY bugün aktif kullanılmıyor. Quote modülü adoption garantili değil — requirements 5.1'de Tasks/Meetings/Calls adoption failure örneği gibi.

**Bu mimari kararı bir bahistir.** LIFFY'nin sales workspace olarak başarısı **mimari karara değil, UX tasarımına ve adoption stratejisine** bağlıdır.

**Operasyonel önkoşul:** Quote modülü inşasına başlamadan önce, sales rep'lerle (Elif, Bengü, mümkünse 1-2 local office sales) UX prototype review yapılır. Prototype, mevcut workflow'larından (Excel taslakları, email draft'ları) ölçülebilir şekilde daha hızlı ve kolay olduğunu **göstermeli, varsayılmamalı**.

**LEENA fallback (operasyonel gerçeklik):** Mimari LIFFY adoption'ına bağlı değildir. Sales rep'ler quote'u LIFFY'de yapsa da yapmasa da, **Project (Yaprak) LEENA'da signed quote olmadan da contract yaratabilir** — Bölüm 6.5'te detaylı. Bugün Zoho'da da bu böyle çalışıyor: her sözleşmenin quote'u olmuyor.

Bu fallback "plan B" değil, **birinci sınıf bir akış**: Yaprak ister Köprü 1'den gelen pending listesinden contract yaratır, ister sıfırdan açar. İki akış da birinci sınıftır.

LIFFY adoption başarısı **istenir**, ama mimari adoption olmasa da çalışır. Olmazsa kaybedilen: structured quote pipeline, sales-side data entry, hot lead conversion tracking. Bunlar değerli ama mimari için **var-yok** kategorisinde değil.

**UX prototype reddedilirse — karar noktası:** Eğer prototype review sales rep'ler veya Suer tarafından reddedilirse, mimari Suer ile yeniden değerlendirilir. Muhtemel üç sonuç:

- (a) Quote modülü LIFFY'ye hiç eklenmez; sadece Akış B yaşar (LIFFY mining/campaign tarafına odaklanır)
- (b) Quote modülü LIFFY yerine LEENA'da inşa edilir (LIFFY tamamen mining/marketing background araç olur)
- (c) Farklı UX yaklaşımı ile yeniden prototype denenir

Hangi sonucun seçileceği iş kararı; mimari her üçünü de destekler. Bu karar verilmeden Quote modülü inşasına başlanmaz.

### 3.2 LIFFY'nin içinde ne var

**Mevcut altyapı (korunan, background araç):**
- Persons (80K — canonical identity)
- Companies (table var, backfill bekliyor)
- Affiliations (90K)
- Mining infrastructure (15+ miner)
- Campaigns + sequences
- Email infrastructure (kendi SendGrid hesabı, kendi domain'i, kendi reply pipeline'ı)
- ZeroBounce verification
- Reply detection (plus-addressing v4)

**Ana değer:**
- Sales Action Screen (günlük dashboard)
- Quote modülü (sıfırdan inşa — UX prototype onayı sonrası)
- Lead follow-up
- Pipeline yönetimi (aktif kullanım)
- Sales rep performans görünümü

**Köprü görünümleri:**
- Floor plan okuma + stand_reservations yazma
- Product/pricing okuma (snapshot ile)
- Kullanıcı preset komisyon oranları okuma
- Customer / disqualified / do-not-contact listesi okuma

**Auth/scope değişiklikleri:**
- Kendi login sayfası kaldırılır; ELIZA çatı JWT'sini kabul eder
- Role-based → matrix-based scope (LEENA'dan okur)

### 3.3 LIFFY'nin sınırı

- Müşteri (customer) yönetmez
- Ödeme, sözleşme, expense, komisyon LIFFY'de yok
- **Floor plan'ın kendisini yazmaz** (geometry, stand status, occupant alanları sadece LEENA Project)
- **Stand reservation yazabilir** (floor plan'dan ayrı tabloya)
- Operasyonel email göndermez

### 3.4 LIFFY Phase 1 inşa sırası

1. Companies backfill (affiliations.company_name → companies tablosu)
2. Contact + Company eşleştirme (affiliations.company_id NULL → doldur)
3. Pipeline aktif kullanım (bugün 4 person var, 80K dışarıda)
4. **Quote modülü UX prototype review ve onay**
5. Quote modülü inşası
6. Signed quote → LEENA pending convert köprüsü

Bu sıra atlanırsa quote firma-string-based başlar, sonra düzeltmek zorlaşır.

### 3.5 LIFFY'nin geleceği

LIFFY'nin mining/marketing tarafı zamanla başka bir araca taşınabilir veya tamamen değiştirilebilir. Sales workspace rolü kalıcı. Yapısal yatırımın LEENA'da yoğunlaşması mantıklı, ama LIFFY'nin sales workspace olarak başarısı mimarinin önemli bir hedefi.

---

## 4. ELIZA çatısı — Bir kapı, bir tabela

ELIZA = ürün adı + giriş kapısı + üst navigation. Branding katmanı.

### 4.1 ELIZA ne yapar

- Tek login sayfası (LEENA'nın auth API'sini çağırır)
- Üst navigation çubuğu (iki sekme: Operasyon / Outreach)
- Role-based default landing — Owner / Project → LEENA War Room; sales rep → LIFFY Action Screen
- Branding (elan-expo.com, "ELIZA" markası kullanıcı yüzü)

### 4.2 ELIZA ne yapmaz

- Veri tutmaz, kendi DB'si yok
- İş mantığı çalıştırmaz
- users / permissions / sessions sahibi değil (LEENA'da)

### 4.3 ELIZA'nın teknik karşılığı

**Ayrı servis değil; LEENA'nın bir alt modülü.** Login sayfası ve üst navigation LEENA içinde yaşar; LIFFY'ye geçiş LEENA'nın yönlendirmesiyle olur. Üç deployment / üç repo / üç auth pipeline kurmaya değecek bir mimari gereksinim yok.

---

## 5. İki sistem arası köprüler

İki tür köprü var: **iş akışı köprüleri** (event-driven, açık tetikleyici) ve **shared infrastructure** (sürekli mevcut).

### 5.1 İş akışı köprüleri

#### Köprü 1: LIFFY → LEENA — "Quote signed, pending convert"

**Yön:** LIFFY → LEENA (push)
**Tetik:** Quote stage = "Signed"
**İçerik:** Quote'un tamamı — firma bilgisi (LIFFY company_id ve company_name string), kontak, ürünler **snapshot fiyatlarla**, m², stand_reservation referansı, komisyon yüzdeleri, sales rep, signed timestamp.

**LEENA davranışı:**
- "Pending convert" listesine ekler
- Henüz customer değil — `quote_signed_pending_convert` durumunda
- Authorized Project user (bugün genellikle Yaprak) convert ederken:
  - customer_company yaratır veya mevcutla eşleştirir
  - customer_contact yaratır veya mevcutla eşleştirir
  - Eksik alanları doldurur
  - Stand reservation kararını verir (Köprü 3)
  - Contract resmileşir → şimdi customer

**Reject durumu:** Quote `returned_to_sales` durumuna düşer, sales rep haber alır.

**Not:** Bu köprü Contract yaratmanın **bir yolu** ama tek yolu değil. Bölüm 6.5 quote-less contract creation'ı tanımlar.

#### Köprü 2: LEENA → LIFFY — Lead enrichment geri beslemesi

**Yön:** LEENA → LIFFY (push)

| Tetik | LIFFY davranışı |
|---|---|
| Quote signed (Köprü 1 paralel) | Person/company'i aktif soğuk kampanyalardan çıkar; `signed_pending_convert` işaretle |
| Convert tamamlandı | "Customer" işaretle (LEENA'da customer_company yaratıldı bilgisi gelir; LIFFY company'sine bu source linki ile bağlanır); do-not-cold-contact aktif |
| **Manual contract created (Bölüm 6.5 Akış B)** | Akış B'nin 3. adımında Yaprak fuzzy match aramasında LIFFY company'sine link verdi ise: "Customer" işaretle, do-not-cold-contact aktif. Link verilmedi ise: sinyal yok (LIFFY zaten o firmayı bilmiyor). |
| Convert reddedildi | `signed_pending_convert` kaldır; sales rep dashboard'una geri döner |
| Manuel disqualified | Aktif kampanyalardan çıkar; "disqualified" işaretle |
| Manuel do-not-contact | Tüm bağlı person'lar kampanyalardan çıkar; "do_not_contact" işaretle |

**Neden iki kademeli (signed vs converted):** Quote signed ile convert arası gün/hafta olabilir. Bu sürede LIFFY hâlâ soğuk email atarsa kötü deneyim; ama henüz "customer" diye saymak da yanlış (Project reddedebilir).

**Bounce/spam yönetimi köprü 2'de değil:** LIFFY kampanya bounce'u LIFFY iç olayıdır, LEENA'yı ilgilendirmez. LEENA operasyonel email bounce'u ise LIFFY'yi ilgilendirmez. Bunlar her sistemin kendi sorumluluğunda.

#### Köprü 3: LEENA ↔ LIFFY — Floor plan okuma + stand_reservation yazma

**Önemli ayrım:** LIFFY floor plan'ı **değiştirmez**. Stand geometry, fiziksel status (available/reserved/sold), occupant alanları sadece LEENA Project'in yazdığı alanlar. LIFFY ayrı bir tabloya (`stand_reservations`) kayıt yazar — satış niyeti, fiziksel stand'ı değiştirmez.

**Yön ve içerik:**
- **LEENA → LIFFY (read):** Stand listesi — kod, m², fiziksel durum, fiyat aralığı, pozisyon, **mevcut reservation'lar** (kim için, ne zaman, deadline, sıra)
- **LIFFY → LEENA (write):** Sadece `stand_reservations` tablosuna — sales_rep_id, company_id, stand_id, deadline, state

**Çoklu rezervasyon — operasyonel kural:**

Sistem geçmişi sunar, karar Project'in.

- Aynı stand için birden fazla active reservation mümkün (Bengü → A firması, Elif → B firması)
- Sales rep stand'ı seçmeden önce mevcut reservation'ları görür ("B12 için Bengü 17 Mayıs deadline'lı, A firması için, 1. sırada")
- Reservation'lar sıralı (created_at) — sıra **sosyal görünürlük göstergesi**, sales rep'in müşterisini hızlandırması veya alternatif düşünmesi için sinyal
- Reservation yaparken **zorunlu deadline**, **max 3 hafta**
- Deadline geçince state otomatik `expired`

**Convert anındaki karar:**

- **Otomatik kazanan yok.** Sıra (kim önce rezerve etti) otomatik kuralı belirlemez.
- Karar tek mercii: **Project**. O günün şartlarına göre verir.
- Sistem Project'e bilgi sunar: hangi reservation'lar var, hangileri active, deadline'lar, hangi sales rep, hangi firma, sıra.
- Sales rep signed yaptığında bir uyarı çıkabilir: "Bu stand için senden önce X. sırada başka reservation var. Lütfen Project'ten onay iste."

Diğer bütün reservation'lar Project kararı sonrası kapanır; sales rep'ler bildirim alır.

**Reservation state machine:**

```
active     → reservation geçerli, sales rep müşteriyle konuşuyor
expired    → deadline geçti, otomatik düştü
converted  → bu reservation Project kararıyla kazandı
cancelled  → sales rep elle iptal etti / quote cancelled / quote lost
superseded → quote yenisi geldi, yeni reservation yarattı
not_selected_by_project → Project başka reservation'ı seçti
```

Detay state geçiş kuralları (extend, çakışan onaylar, vb.) Aşama 3'te.

#### Köprü 4: LIFFY → LEENA — Data entry metrikleri (nightly push aggregation)

**Yön:** LIFFY → LEENA (push, nightly aggregation)
**Tetik:** Gece scheduled job (LIFFY tarafında)
**İçerik:** Bir gün için per-user, per-office aggregated metrikler — yeni lead sayısı, gönderilen email, alınan reply, yaratılan quote
**Mekanizma:** LIFFY her gece aggregation üretir → LEENA `liffy_daily_metrics` tablosuna POST → manager raporu ve WhatsApp bot LEENA tablosundan okur, LIFFY'ye anlık sorgu atmaz

**Bu köprünün sınırı:**

- **Tarihsel ve aggregated metrikler** içindir (haftalık raporlar, geçmiş dönem karşılaştırmaları, manager dashboard'ları). "Geçen ay kaç quote" sorusu buradan cevaplanır.
- **Gün-içi gerçek-zamanlı olaylar** ("Bengü az önce yeni quote yarattı", "yeni reply geldi") buradan değil — **notifications dispatcher real-time event stream** üzerinden akar. Bu Aşama 2'de tasarlanır.
- Mimari "her veri 24 saat geç" iddia etmiyor; sadece manager raporları aggregation tablosundan okuyor.

**Geç push durumu:** LIFFY bir gece push yapmazsa, sonraki gece kaçırılan günü beraber gönderir. İdempotent yazma (günlük key).

#### Köprü 5: LEENA → LIFFY — Product/pricing okuma + snapshot

**Yön:** LEENA → LIFFY (read at query time, frozen into LIFFY at quote creation)
**Tetik:** Quote yaratıldığında, expo seçilince
**İçerik:** Seçilen expo'nun ürün listesi — PES, RF, SYK, extras (TV, fridge, counter, vb.), her birinin fiyatı, currency, tax kuralı, pricing tier'ları, **price_version_id**

**Pricing snapshot/freeze prensibi (Finance Invariant 3'ün pricing versiyonu):**

LIFFY pricing'i LEENA'dan okur, **quote oluşturulduğu anda quote line item'larına snapshot olarak yazar**. Donan alanlar:
- Unit price, currency, exchange rate (non-EUR ise)
- Tax rate, discount tier'ları
- EUR-equivalent değer
- **price_version_id** (kaynak fiyat listesinin versiyonu — audit için)

**Neden:** LEENA'da expo pricing sonradan değişirse eski quote/contract değişmemeli. Müşteri "ben €185'e anlaştım" demişse sözleşme €185 olmalı; sonradan €195'e güncellenmiş pricing geçmiş quote'u kirletmemeli.

`price_version_id` ile snapshot kaynağa kadar gidilebilir: "bu quote hangi fiyat listesinin v3'üne göre oluşturuldu?" sorusu cevaplanır.

**Convert sırasında:** Authorized Project user aynı snapshot'ı contract'a taşır. Override mümkün (audit log'lanır).

### 5.2 Shared infrastructure (sürekli mevcut bağımlılıklar)

Bunlar event-driven köprü değil; LEENA'nın sahibi olduğu, LIFFY'nin sürekli okuduğu kaynaklar.

| Kaynak | LEENA rolü | LIFFY rolü |
|---|---|---|
| Reference data (countries, sectors, currencies, languages) | Sahibi, yazıyor | Okuyor, senkron tutuyor |
| Users + permission matrix + hierarchy | Sahibi, auth API sunuyor | API'yi çağırıyor; JWT claims kullanıyor |
| Audit log | Tek merkezi tablo, resilient yazma | LIFFY de buraya yazar; LEENA down ise local outbox + retry |
| Notifications dispatcher | LEENA çalıştırıyor (real-time event stream dahil) | LIFFY notification yaratıp LEENA dispatcher'ına gönderiyor |

**Audit resilience prensibi:** LIFFY merkezi audit'e yazmak zorunda, ama LEENA API geçici olarak ulaşılamazsa LIFFY işlemleri **durmamalı**. Pattern: LIFFY işlemi yapar → audit event lokal outbox'a düşer → background worker LEENA audit API'ye gönderir → başarısızsa retry (exponential backoff). İmplementation detayı Aşama 3'te.

**Tasarım prensibi:** Shared infrastructure değişiklikleri **tek yerde** yapılır (LEENA). LIFFY bunları **okuyup uyar**. Çift kayıt yok.

### 5.3 Köprü tasarım disiplini

- Her köprünün açık tetikleyicisi var
- Her iş akışı köprüsü tek yönlü (Köprü 3 istisna — yazma `stand_reservations`'a sınırlı, floor plan'a değil)
- API ile, doğrudan DB cross-connect yok
- Her köprünün hata durumu tasarlanmış
- Shared infrastructure dökümante, saklanmıyor
- Resilient yazma (audit gibi) outbox/retry ile

Yeni köprü gerektiğinde bu dokümana eklenir, gerekçesi yazılır, yönü ve içeriği netleşir.

### 5.4 Tek-DB-değil kararının maliyetleri

LEENA tek DB + LIFFY ayrı DB kararı "bedava" değil. Somut maliyetler:

| Maliyet | Açıklama | Çözüm yaklaşımı |
|---|---|---|
| **Cross-DB join yapılamaz** | Manager raporu "Bengü kaç quote yaptı + kaç contract imzalandı" sorusunu tek SQL ile çözemez | Köprü 4 ile LIFFY metriklerini LEENA'ya nightly push; LEENA kendi tablosundan join |
| **Audit log writes network call'lar** | LIFFY her yazma sonrası LEENA'ya HTTP request; LEENA down ise audit boşa düşebilir | Outbox + retry pattern; başarısız ise alert |
| **Reference data senkronu** | LEENA'da yeni currency eklenince LIFFY ne zaman fark eder? | Aşama 2'de karara bağlanacak — muhtemelen change event + LIFFY tarafında cache invalidation |
| **JWT geçerlilik vs permission değişikliği** | LEENA'da bir kullanıcının yetkisi kısıtlandı; LIFFY ne zaman fark eder? | Kısa token expiry (15-30 dk); kritik permission değişiklikleri için forced re-auth |
| **Müşteri/prospect dağıtımı** | LIFFY companies/persons = prospect dünyası; LEENA customer_companies/customer_contacts = müşteri dünyası. Aynı gerçek-dünya şirketi iki yerde olabilir. | **Bu maliyet değil, iki dünya ayrımının doğal sonucu.** Convert anında LEENA'da yeni veya eşleşen kayıt oluşur. Eşleştirme algoritması (tax_id, isim+ülke benzerliği, manuel onay) Aşama 3'te |
| **Backup/restore karmaşıklığı** | İki DB ayrı backup, ayrı restore; consistency point of failure | Migration roadmap'inde her cutover öncesi koordineli backup planı |

Bu maliyetler **şu an kabul edilebilir** çünkü Köprü 4 pattern'i nightly aggregation ile çoğunu çözüyor, permission değişiklikleri günlük operasyonda nadir, reference data değişiklikleri haftalık ölçekte. Ama **görünmez maliyet değil** — Aşama 2'de her birinin detayı tasarlanacak.

---

## 6. Migration ve mevcut sistemlere etki

### 6.1 LEENA'da neler değişiyor

**Bozulmayan parçalar:** Visitor registration, Floor Plan Builder, Check-in, email_queue/logs/reactivation flow.

**Genişleyen parçalar:** `organizers` tek password_hash → users tablosu; permission matrix; audit log; `stand_reservations` tablosu.

**Yeni eklenen modüller:**
- customer_companies, customer_contacts
- Contracts, Revenues, Expenses, Accounts, Commissions
- AI engine + WhatsApp bot (eski ELIZA'dan port)
- War Room (port)
- Auth servisi
- Catalogue MVP (Phase 1 minimum)
- 8-mail Announcement engine
- Manager raporları + liffy_daily_metrics tablosu
- Search
- Notifications (real-time event stream dahil)
- Product katalogu + pricing
- ELIZA çatı submodule

**Frontend stratejisi:** Yeni sayfalar modern teknoloji (Next.js + React); çalışan eski sayfalar (visitor form, floor plan builder, check-in) Vanilla JS kalır. Zamanla modernize edilir, **bir gecede yeniden yazılmaz**.

### 6.2 Eski ELIZA'nın akıbeti

1. AI engine kodu LEENA'ya port
2. WhatsApp bot kodu LEENA'ya port
3. War Room dashboard LEENA'da yeniden yazılır
4. Risk engine, expo metrics view LEENA'da
5. Zoho-sync migration boyunca eski repo'da kalır, sonra emekli
6. Eski ELIZA repo'su arşivlenir

**Kullanıcı yüzünde ELIZA markası kalır** (login + üst navigation + ürün adı).

### 6.3 LIFFY'de neler değişiyor

Phase 1 ön koşulları (sıralı): Companies backfill → Contact-Company eşleştirme → Pipeline aktif kullanım → Quote modülü UX prototype review ve onay.

Sonra: Sales Action Screen, Quote modülü, köprü görünümleri, auth değişikliği, matrix-based scope, lifecycle_stage enum.

Core mining/campaign/sequence/action engine/reply detection **kod olarak dokunulmaz**; UI'de arka plana alınır.

### 6.4 Zoho geçişi — prensip

**Çift master dönemi yok.** Bir modül için aynı anda iki sistemde yeni veri yaratılmaz.

Her modülün ELL'e geçişi bir **cutover noktasına** sahiptir:
- **Öncesi:** Zoho master, ELL read-only mirror (Zoho-sync ile)
- **Sonrası:** ELL master, Zoho read-only veya kapalı

Cutover anında o modülün yeni verisi sadece ELL'de yaratılır. Eski Zoho verisi historical olarak okunmaya devam edebilir, ama yazma kapatılır.

Somut cutover sıralaması ("yeni quote ne zaman LIFFY'de, payment ne zaman ELL'de") migration roadmap'in işi. Mimari her modülün cutover'a hazır olmasını garanti eder. Zoho kapatma için acele yok — modül modül, hazır olunca.

### 6.5 Contract creation — iki birinci sınıf akış

Sales Contract iki yolla yaratılır. **İkisi de birinci sınıf akıştır**, biri "asıl" diğeri "fallback" değil.

**Akış A — Signed quote'tan convert (Köprü 1'den gelen):**

1. Sales rep LIFFY'de quote yarattı → signed durumuna getirdi
2. Köprü 1 LEENA'ya push → pending convert listesine düştü
3. Authorized Project user (genellikle Yaprak):
   - Pending listesinden bu kaydı açar
   - customer_company yaratır veya mevcutla eşleştirir
   - customer_contact yaratır veya mevcutla eşleştirir
   - Pricing snapshot zaten var; gerekirse override eder (audit'lenir)
   - Stand reservation kararını verir (Köprü 3)
   - Convert → Contract resmileşir
   - Köprü 2 LIFFY'ye "customer" sinyali yollar

**Akış B — Quote-less manual contract creation:**

1. Yaprak bir contract yaratacak (sebep: sales rep dış araçta anlaştı, telefon üzerinden geldi, doğrudan iletişim, walk-in, dış acente üzerinden geldi, vb.)
2. LEENA'da "New Contract" diyerek başlar
3. **Sistem proaktif olarak LIFFY companies'i fuzzy match ile arar** (firma adı, ülke, sektör üzerinden). Eşleşme bulursa Yaprak'a sorar: *"Bu firma LIFFY'de '[X]' olarak var, linklemek ister misin?"* Yaprak link, ignore veya yeni yarat seçeneklerinden birini seçer. Bu adım data bifurcation'ı (aynı firmanın iki yerde farklı isimlerle bulunmasını) önler.
4. customer_company yaratır veya mevcutla eşleştirir (LEENA tarafında)
5. customer_contact yaratır veya mevcutla eşleştirir
6. Product line item'larını LEENA pricing'den seçer (snapshot manuel oluşur — Invariant 3 uygulanır)
7. Stand atamasını yapar (LEENA floor plan'dan)
8. **Sales attribution — üç kategori (D41 karşılığı):**
   - (a) **Sales rep** seçer — system user, komisyonlu (preset komisyon oranı LEENA users tablosundan gelir, override edilebilir)
   - (b) **Sales agent** seçer — system user **değil**, dış ajans / freelance acente; komisyon oranı manuel girilir (LEENA `sales_agents` tablosunda kayıtlı entity'lerden seçilir)
   - (c) "**Project department**" veya "**Elan Expo**" diye işaretler — komisyonsuz contract
9. Contract resmileşir

**Sales rep vs Sales agent ayrımı (D41):**

| | Sales rep | Sales agent |
|---|---|---|
| System user mu? | Evet (auth, login, scope) | Hayır (sadece kayıt) |
| LEENA users tablosunda mı? | Evet | Hayır — `sales_agents` tablosunda |
| Quote yaratabilir mi? | Evet (LIFFY'de Akış A) | Hayır — deal'i Yaprak'a bildirir, Yaprak Akış B ile contract yaratır |
| Komisyon alabilir mi? | Evet (preset oran, contract bazında override) | Evet (contract bazında manuel oran) |
| Permission matrix'te yer alır mı? | Evet | Hayır |
| Hierarchy'de yer alır mı? | Evet (reports_to) | Hayır |

Bu ayrım Aşama 2'de auth/users/permissions tasarımında detaylanır.

**İki akışın ortak noktaları:**
- Aynı customer_company / customer_contact entity'leri
- Aynı pricing snapshot disiplini (Invariant 3)
- Aynı stand reservation davranışı
- Aynı audit log
- Aynı 8-mail Announcement chain'i tetikler (Welcome, Catalogue Form, vb.)
- Aynı raporlamada görünür

**Akış B'nin LIFFY ile ilişkisi:**
- Adım 3'teki fuzzy match aramasıyla Yaprak LIFFY'deki olası eşleşmeyi görür
- Yaprak link ettiyse (LIFFY'de bu firma vardı), Köprü 2 tetiklenir — LIFFY o person/company'yi "customer" işaretler, aktif kampanyalardan çıkarır
- Yaprak ignore ettiyse veya match bulunamadıysa, Köprü 2 sinyali yok — LIFFY bu firmayı görmez, normal
- Bu disiplin sayesinde "aynı firma iki yerde farklı isimle, biri customer, diğeri hâlâ cold lead" senaryosu engellenir

**Neden bu akış kritik:**

Bugün Zoho'da Yaprak signed quote olmadan da contract yaratabiliyor — gerçek operasyonel pattern bu. Mimari bu pattern'i **birinci sınıf** olarak desteklemeli, "exception" olarak değil. Yoksa LIFFY adoption olmazsa sistem bozulur.

Bu da mimarinin LIFFY'ye **bağımlı değil, esnek** olmasını sağlar: LIFFY adoption yüksek olursa Akış A baskın olur, düşük olursa Akış B baskın olur, ikisi de işliyor.

---

## 7. Bu mimari requirements'ı nasıl karşılıyor

| Requirements prensibi | Mimari karşılığı |
|---|---|
| İki dünya ayrımı (müşteri öncesi/sonrası) | LIFFY + LEENA; geçiş bölgesi pending_convert; veri modelinde de korunur |
| ELIZA çatısı, tek login | ELIZA = LEENA submodule |
| Cross-modül sorgu kolaylığı | LEENA tek DB; view'larla çoklu modül sorgusu |
| Email itibar izolasyonu | LIFFY ayrı SendGrid + domain + IP |
| Quote → Convert kontrol kapısı (D12) | Köprü 1 + Köprü 2 + pending_convert state (Akış A) |
| Her sözleşmenin quote'u olmaz | Akış B — quote-less manual contract creation, birinci sınıf akış |
| Sales rep sadece kendi sözleşmesi (S11) | LIFFY → LEENA tab geçişi, scope-limited |
| Reference data tek yerde (3.5) | LEENA sahibi; LIFFY okur |
| Audit her şeyin altında (3.6) | LEENA merkezi; LIFFY resilient yazma |
| Hierarchy değişimi anında yansır (3.4) | users + matrix LEENA'da |
| Phase 2 scaffolded (4.6) | LEENA modülleri olarak eklenecek |
| Lead enrichment geri beslemesi | Köprü 2 (iki kademeli) |
| Multi-rezervasyon esnekliği | Köprü 3 — Project tek karar mercii |
| Two-sided money movement | Finance Invariant 1 |
| Computed balances | Finance Invariant 2 |
| Frozen exchange rates (D34) | Finance Invariant 3; pricing versiyonu Köprü 5 snapshot |
| Corel Draw'dan kurtulma (Catalogue) | Phase 1 minimum: submission + storage + list. Phase 2: template editor + PDF + web catalogue |
| Customer history, credit balance, cross-expo participation | LEENA customer_companies first-class entity |
| WhatsApp bot Owner için günlük araç | LEENA içinde yaşar; LIFFY verilerini aggregated + notifications stream üzerinden okur |
| Sales agent ≠ user (D41) | A28 — üç kategori: sales rep (user), sales agent (`sales_agents` tablosu), Project department |
| Aynı firma iki yerde farklı isim olmasın | A29 — Akış B'de proaktif fuzzy match arama (data bifurcation önleme) |

---

## 8. Açık konular (sonraki aşamalara veya Suer'in karara bağlamasına bırakılan)

### 8.1 Catalogue Phase 1 vs Phase 2 ayrımı

**Mimarinin kararı:**

- **Phase 1 minimum:** exhibitor submission + storage + basic list view. Veri modeli ve 8-mail Announcement chain'in Catalogue Form mailini desteklemek için zorunlu.
- **Phase 2:** template editor + advanced PDF export + web catalogue + Corel Draw replacement.

Suer'in kararı: Catalogue MVP'nin geniş yorumu (web view + PDF dahil) Phase 1 değildir; sadece submission + storage + list. Roadmap aşaması bu ayrımla devam eder.

### 8.2 Köprü 3 — sales rep deneyimi politikası

Köprü 3'ün veri ve karar modeli çözüldü: Project tek karar mercii, otomatik kural yok. Ama operasyonel/sosyal politika tanımlanmadı:

**Senaryo:** Bengü stand B12'yi A firması için 1. sırada rezerve etti. Elif aynı standa B firması için 2. sırada. Elif'in müşterisi imzaladı. Project Elif'in reservation'ını seçti. Bengü'nün müşterisine ne diyecek?

Mimari her senaryoyu destekler ama politika seçimi Suer'e ait. Olası yaklaşımlar:
- Early warning bildirimi (Elif rezerve edince Bengü'ye uyarı)
- Müşteri beklenti yönetimi (rezervasyon = öncelikli teklif, garanti değil prensibi)
- Project'in saydam karar gerekçesi
- Bunların kombinasyonu

**Aksiyon:** Aşama 2 paralelinde Suer + Elif/Yaprak ile konuşulmalı.

### 8.3 Sales agent attribution — detay tasarımı

A28 sales attribution'ın üç kategorisini (sales rep / sales agent / Project department veya Elan Expo) ve sales agent'ın system user olmadığını netleştirdi. Kalan detaylar Aşama 2'de:

- `sales_agents` tablosunun şema detayı (zorunlu alanlar: isim, contact bilgileri, default komisyon oranı, IBAN/payment info, vergi durumu)
- Sales agent için onboarding süreci (kim ekleyebilir, hangi onaylar gerekir)
- Quote yaratma yetkisi: dış acente bir deal'i bildirdiğinde quote LIFFY'de bir sales rep proxy olarak mı açılır, yoksa Yaprak doğrudan Akış B ile mi contract yaratır? (Mimari her ikisini de destekler; iş kararı)
- Sales agent için raporlama/dashboard (kendisi sisteme giremez ama Yaprak/Elif onun performansını görebilmeli)
- Commission ödeme akışı (sales agent'a expense olarak mı yansır, ayrı bir payable mi)

### 8.4 Diğer konular (sonraki aşamalara)

- Frontend kütüphane seçimi — Aşama 5 (veya Aşama 2'de auth ile beraber)
- Migration roadmap detayı — Migration aşaması
- Notifications channel mimarisi — Aşama 2
- Search global teknik yaklaşımı — Aşama 3
- Reservation state geçiş detay kuralları — Aşama 3
- Audit outbox/retry implementation — Aşama 3
- Reference data senkron mekanizması — Aşama 2
- JWT expiry stratejisi — Aşama 2
- Customer_company eşleştirme algoritması (fuzzy match heuristics, eşik değerleri, manuel onay UX'i) — Aşama 3
- WhatsApp bot için "Owner'a izinli veri scope'u" — Aşama 2
- **Lapsed customer lifecycle politikası** — Bir müşteri 1-2-5 yıl katılmazsa LEENA'da customer_company olarak mı kalır, LIFFY'ye re-engagement için mi döner? Bu hem **mimari** (entity nerede yaşar) hem **iş** (kim re-engagement yapar) kararı. Aşama 3 + Suer iş kararı.
- **Disaster recovery senaryoları** — LEENA tamamen kaybolursa LIFFY tek başına ne kadar süre işleyebilir (auth/ref data kaybı)? LIFFY tamamen kaybolursa LEENA hangi özellikleri kaybeder (Köprü 4 metrik, lead enrichment)? Veri kaybı durumunda LIFFY outbox'ı ne kadar büyür? Operations aşamasında detay; mimari prensip seviyesinde her sistemin diğeri olmadan ne yapabildiği belgelenmeli.

---

## 9. ADR çakışma listesi — önceliklendirilmiş

Bu doküman bazı mevcut ADR'lar ve planlama dokümanlarıyla çakışıyor. Onlar revize edilmeden Aşama 2'ye geçilirse, yeni ekip eski-yeni çakışmasında saatler kaybeder.

### 9.1 Aşama 2 öncesi mutlaka revize edilmesi gerekenler

Tek-DB-değil kararı (LEENA tek DB + LIFFY ayrı) ile direkt çakışıyorlar:

| Doküman | Çakışma | Aksiyon |
|---|---|---|
| **ADR-004 (Shared Database)** | İki DB kararı eski "shared database" varsayımını geçersiz kılıyor | Tamamen revize |
| **ADR-017 (Three-Database Architecture)** | Üç DB değil, iki DB | Tamamen revize |

### 9.2 Aşama 2 paralelinde revize edilebilir

İlgili Aşama 2 konusu çalışılırken yan ürün olarak güncellenebilir:

| Doküman | Çakışma | Aksiyon |
|---|---|---|
| ADR-001 (ELIZA Commercial Core) | ELIZA artık branding katmanı; commercial core LEENA'da | Yeni rol tanımla |
| ADR-003 (Quote-Contract Separation) | Köprü 1 + Köprü 2 + pending_convert state + Akış B | State machine güncellemesi; iki akış da yazılı |
| ADR-005 (ELIZA Write Policy) | ELIZA artık servis değil, LEENA submodule | Archive; yeni "LEENA write policy" |
| ADR-010 (Floor Plan Sales Weapon) | Köprü 3 + state machine ile genişledi | Hafif revize: çoklu reservation, Project tek karar mercii |
| ADR-015 (Hierarchical Data Visibility) | Matrix + hierarchy kombinasyonu | Requirements 3.1, 3.4 ile uyumlu hale getir |
| **ELL_ROADMAP.md** | Eski roadmap eski varsayımlarla (tek DB, ortak company, LIFFY contract-payment sahibi) yazıldı | Tamamen revize — yeni mimariye göre yeniden yaz |
| LIFFY Phase 1 MVP Plan | Sıra değişti, UX prototype önkoşulu eklendi | Revize |
| ELL_RULES (v3-v5.1) | Yeni mimariyle büyük ölçüde uyumsuz | Yeniden yaz |

### 9.3 Sonraya bırakılabilir

| Doküman | Aksiyon |
|---|---|
| 9 adet RFC | Her biri ayrı değerlendirme |

---

## 10. Bu dokümanın kararları

| ID | Karar |
|---|---|
| A1 | Üç sistem değil, iki uygulama (LEENA + LIFFY) + bir çatı (ELIZA) |
| A2 | ELIZA = ürün adı + login + üst navigasyon; uygulama değil; branding kararı |
| A3 | LEENA = ana gövde (operasyon + finance + intelligence + auth/users/audit sahibi) |
| A4 | LIFFY = sales workspace; mining/marketing background araç; adoption riski UX prototype önkoşuluyla |
| A5 | LEENA tek DB; LIFFY ayrı DB |
| A6 | Eski ELIZA repo'su emekli, parçaları LEENA'ya |
| A7 | LIFFY-LEENA arası 5 iş akışı köprüsü + 4 shared infrastructure |
| A8 | LEENA'nın çalışan parçaları bozulmaz; üstüne ekleme yapılır |
| A9 | Email infrastructure izolasyonu mimari prensip |
| A10 | Reference data + permission matrix + hierarchy + audit log LEENA'da merkezi |
| A11 | Floor plan: çoklu görünür reservation + zorunlu deadline (max 3 hafta) + Project tek karar mercii (otomatik kazanan yok) + 6-state machine |
| A12 | Lead enrichment geri beslemesi köprüsü; iki kademeli (signed + converted) |
| A13 | Zoho geçişinde çift master dönemi yok; modül modül cutover |
| A14 | Pricing snapshot/freeze: quote line item'a snapshot olarak yazılır; price_version_id ile kaynak izlenebilir |
| A15 | LIFFY Phase 1 sırası: Companies backfill → Contact-Company eşleştirme → Pipeline → Quote UX prototype → Quote modülü |
| A16 | Audit yazımı resilient: outbox + retry pattern |
| A17 | ELIZA çatı = LEENA'nın alt modülü (ayrı servis değil) |
| A18 | Tek-DB-değil kararının maliyetleri açıkça beyan edildi: cross-DB join yok, audit network call, ref data sync, JWT expiry, müşteri/prospect dağıtımı (maliyet değil, iki dünya ayrımının doğal sonucu), backup karmaşıklığı |
| A19 | Hibrit mimari beyanı: bu mimari requirements + pragmatic kısıtlardan çıkıyor; açıkça yazılı *(meta-beyan, somut yapısal karar değil — detayı Bölüm 0)* |
| A20 | Köprü 4 = nightly push aggregation, tarihsel/aggregated metrikler için; gün-içi olaylar notifications dispatcher real-time stream üzerinden |
| A21 | İki dünya ayrımı veri modelinde de korunur: LIFFY companies/persons (prospect) ≠ LEENA customer_companies/customer_contacts (müşteri); convert anında entity yaratımı/eşleşmesi |
| A22 | Phase kompozisyonu (hangi modül hangi phase'de) bu dokümanın genel kararı değil — roadmap aşamasında belirlenir. Ancak mimari, **bazı kritik modüller için Phase 1 minimum tanımı** belirleyebilir (örn. A26 Catalogue minimum). Genel kural: mimari modüllerin bağımsız inşa edilebilir olmasını garanti eder. |
| A23 | Köprü 3'te otomatik kazanan yok: Project tek karar mercii; sıra (created_at) sadece sosyal görünürlük göstergesi; sales rep signed yaptığında uyarı çıkabilir ama otomatik öncelik vermez |
| **A24** | **Contract creation iki birinci sınıf akış destekler: Akış A (signed quote'tan convert) ve Akış B (Yaprak'ın quote-less manual creation). Mimari LIFFY adoption'ına bağlı değil — Akış B "fallback" değil, gerçek operasyonel pattern.** |
| **A25** | **WhatsApp bot LEENA içinde yaşar; LIFFY verilerini liffy_daily_metrics tablosu + notifications real-time stream üzerinden okur; doğrudan LIFFY API çağrısı yapmaz.** |
| **A26** | **Catalogue Phase 1 minimum: submission + storage + basic list view. Phase 2: template editor + PDF export + web catalogue (Corel Draw replacement).** |
| **A27** | **Finance Invariants: (1) Two-sided money movement — tek taraflı kayıt yasak. (2) Computed balances, not stored — bakiyeler hesaplanır, depolanmaz. (3) Frozen exchange rates per transaction — kur kaydedildikten sonra değişmez. Bu üç invariant LEENA finance kodunun yazım disiplinidir.** |
| **A28** | **Sales attribution üç kategori (D41 karşılığı):** (a) Sales rep — system user, komisyonlu, preset oran. (b) Sales agent — system user **değil**, dış ajans/freelance, `sales_agents` tablosunda kayıtlı, contract bazında manuel komisyon oranı. (c) Project department / Elan Expo — komisyonsuz contract. Sales rep ve sales agent farklı entity tipleridir; sales agent auth/scope/hierarchy'de yer almaz. |
| **A29** | **Akış B'de proaktif LIFFY fuzzy match arama:** Yaprak LEENA'da manual contract yaratırken sistem LIFFY companies'i fuzzy match ile arar (firma adı + ülke + sektör); eşleşme bulursa Yaprak'a link/ignore/yeni-yarat seçeneklerini sunar. Bu data bifurcation'ı (aynı firmanın iki sistemde farklı isimlerle bulunması) önler. Match heuristics ve eşik değerleri Aşama 3'te. |

---

## 11. Sonraki adım

**Aşama 2 — Cross-cutting infrastructure.**

Aşama 2 konuları:
- Auth sistemi (LEENA submodule içinde JWT yapısı, LIFFY token paylaşımı)
- Users + sales agents + data entry contractors üçlemesi (D41)
- Permission matrix (CRUD + special permissions, profile templates, override)
- Hierarchy (reports_to recursive CTE) ve scope composition
- Reference data master tabloları ve LIFFY'ye replikasyon mekanizması
- Audit log yapısı (outbox/retry pattern, LIFFY entegrasyonu)
- Notification merkezi (in-app/email/WhatsApp dispatcher + real-time event stream)
- Search global yaklaşımı
- JWT expiry stratejisi
- Sales agent attribution kuralları
- WhatsApp bot "Owner için izinli veri scope'u"

### 11.1 Aşama 2 başlamadan önce zorunlu

- Bu doküman onaylanmalı
- ADR-004 ve ADR-017 revize edilmeli (9.1)

### 11.2 Aşama 2 paralelinde yürür

- Köprü 3 operasyonel politika kararı (8.2) — Suer + Elif/Yaprak konuşması
- ADR-001, ADR-003, ADR-005, ADR-010, ADR-015 revizyonu
- LIFFY Phase 1 MVP Plan ve ELL_ROADMAP.md güncellenmesi (9.2)
- ELL_RULES yeniden yazımı
- **Roadmap dokümanı yazımı** — Aşama 3 başlamadan önce onaylanmalı

### 11.3 Quote modülü inşası öncesi zorunlu

- LIFFY Quote UX prototype review — Elif, Bengü ve mümkünse local office sales ile

Bu, Aşama 2'yi bloklamaz; Aşama 2 altyapı işleri UX prototype'a bağımlı değil. Ama Quote modülü inşası başlamadan önce yapılmış olmalı.

---

*Bu doküman ELL mimari aşamasının ilk çıktısıdır. ELAN_EXPO_REQUIREMENTS_v1_0 ile çakıştığı yerlerde requirements doc geçerlidir; eski ADR'lar ve planlama dokümanlarıyla çakıştığı yerlerde bu doküman geçerlidir ve onlar revize edilecektir (Bölüm 9).*
