# ELL — Bilgi Mimarisi (Information Architecture) v3

> ## 🔴 2026-06-19 — MİMARİ KARAR DEĞİŞİKLİĞİ (HER ŞEYDEN ÖNCE OKU)
>
> **ELIZA ayrı sistem olarak terk edildi.** Eski ELIZA backend/database disposable Zoho
> mirror + raporlama prototipidir; verisi LEENA'ya migrate edilmeyecek.
> - **LIFFY** = dış halka / satış / freelancer izolasyonu. Ayrı DB + ayrı servis.
> - **LEENA** = iç halka / operations + finance + contracts + payments + commissions + ledger + reporting.
> - **ELIZA** = kullanıcıya görünen ürün / **Finance tab** / brand adı; fiziksel backend/DB **DEĞİL**.
> - **Tek cross-DB sınır: LIFFY ↔ LEENA.** ELIZA↔LEENA bridge yoktur.
> - Contract/payment/commission/ledger/sales agent/expo finance **LEENA DB'de** kurulur.
>
> *(Aşağıdaki "üç app" / "ELIZA'ya yaz" dili bu karara göre düzeltildi. Belgenin doğru çekirdeği
> zaten §0'daki nottaydı; kalan eski dil temizlendi.)*

**Rol sınırı (2026-07-25):** Bu belge yalnız **BİLGİ MİMARİSİ**dir — hangi varlık hangi
sistemde/DB'de yaşar, sahiplik kimde. **Durum/ilerleme TUTMAZ.** Aşağıdaki 🟢/🟡/🔴
olgunluk işaretleri ve "bugün/şu an" ifadeleri **2026-06-19 tarihli donmuş fotoğraftır**;
güncel durum **ELL_DURUM_DEFTERI_v2.md**'dedir. Çelişkide defter kazanır.

**Amaç:** "Hangi iş hangi kullanıcı domain'inde/sekmede görünür ve fiziksel olarak hangi sistemde yaşar" ve "her domain içinde sayfalar nasıl gruplanır" sorularını cevaplamak. Renk/component değil; **sunum + kullanış kolaylığı** katmanı. Kaynak: ELAN_EXPO_REQUIREMENTS v1.0 + iki aktif sistemin (LIFFY + LEENA) mevcut durumu (eski ELIZA yalnız tarihsel referans) + kilitli mimari (Aşama 1, Bölüm 1–2) + 2026-06-19 mimari karar bloğu.

**v2 değişiklikleri (Sentez review):** Convert iki-dönüşüm netleşti (#2); AF number prefix-flip notu (#1); scope reports_to zinciri (#3); Cluster eklendi (#4, #8); pipeline 7-aşama kaynaklandı + 6/7 convert sınırı (#5); **olgunluk katmanı eklendi (#6)**; **iki-halka domain erişim matrisi eklendi (#7)**; global search **eski 3-DB notundan 2-DB modeline düzeltildi** (#9).

**Design-iterasyon güncellemesi (2026-06-10):** Operations nav ikiye ayrıldı — **Exhibitor** + **Floor plan** ayrı bölüm, **Conferences → Visitor & Access içinde sayfa** (§2). Shell'e **Settings → Appearance tema sistemi** eklendi (§6): Vermillion default + Cobalt, light/dark planlı, token-tabanlı.

---

## ⛔ Olgunluk lejantı — DONMUŞ FOTOĞRAF (2026-06-19), DURUM KAYDI DEĞİL

Bu belge kullanıcı-açısından hedef IA'yı tarif eder. Ama her ekran bugün mevcut değil — çoğu **greenfield**. Tasarımcı buna göre varsayım yapmalı:

- 🟢 **Bugün canlı** — LEENA operasyon (tek canlı sistem). Re-skin + IA düzenlemesi.
- 🟡 **Var ama kullanımda değil / kısmi** — LIFFY (mining/CRM/campaign kurulu, dormant), ELIZA dashboard/AI.
- 🔴 **Greenfield — sıfırdan inşa** — **ticari çekirdek: quote → contract → payment → commission → ledger** (şu an Zoho'da; yeni sistemde **LEENA Finance içinde** sıfırdan kurulacak — ELIZA adı Finance UI/brand olarak kalır) + Catalogue Generator. **ELL'in asıl ödülü burası.**

---

## 0. Ana ilke — iki sistem, üç kullanıcı domain'i

> **Not (terminoloji — önemli):** Bu belgede **"ELIZA" = UI / Finance domain adı, ayrı servis DEĞİL.** Tüm "→ ELIZA" atıfları "ELIZA/Finance sekmesinde sunulur" demektir; **fiziksel saklama LEENA DB'sinde**. **2 sistem + 2 DB** vardır (LEENA + LIFFY); ELIZA ayrı DB değildir. Tek cross-DB sınırı LIFFY↔LEENA. (Bkz. Glossary kanonik blok + 2026-06-19 mimari karar bloğu.)

Üç kullanıcı domain'i şöyle eşlenir (teknik olarak üç sistem YOK):
- **Sales domain = LIFFY**
- **Operations domain = LEENA**
- **Finance domain / ELIZA tab = LEENA Finance**

Requirements'taki **function split** doğrudan bu üç domain'e oturuyor:

```
        SATIŞ (imza ÖNCESİ)         |   CONVERT   |        PROJE / PARA (imza SONRASI)
  ─────────────────────────────────┼─────────────┼──────────────────────────────────────
        LIFFY  🟡                   |    geçit    |   LEENA Operations 🟢 + LEENA Finance / ELIZA tab (çekirdek 🔴)
   "kim alabilir + imzalat"         |  =GÜVEN     |  "etkinliği       "para + gerçek
   lead→outreach→quote→signed       |   SINIRI    |   çalıştır"        + içgörü"
```

- **LIFFY = Satış tarafı** (Sales Manager'ın dünyası): lead, outreach, qualify, quote, "signed". İmzaya kadar.
- **LEENA = Proje/Operasyon tarafı**: imzalı exhibitor'ı sahaya yerleştir/kataloğa koy/badge'le; ziyaretçiyi kaydet/içeri al; expo'yu çalıştır.
- **LEENA Finance / ELIZA tab = Ticari kayıt + zeka; fiziksel sahip LEENA DB'dir**: contract, payment, commission, expense, ledger, yönetici dashboard, AI. Her şeyin üstünden.

**Convert = iki dönüşümü birden yapan dikiş yeri** (Proje ekibi, D12):
1. **Quote → Sales Contract** (AF number'da prefix Q→A; aynı sequence)
2. **Lead → Contact + Company** *(garanti)* — normalde qualify anında (pipeline stage 4) doğmalı; pratikte atlandığı için convert gate bunu garanti eder.

Convert ayrıca **güven sınırı:** dış halka (satış/freelancer) ile iç halka (proje+Owner) arasındaki geçiş. Bkz. §6.

---

## 1. "Ne nerede yaşıyor" — sahiplik haritası (karışıklığı bitiren kısım)

Karışıklığın kaynağı: **bazı kavramlar birden fazla app'te ama farklı ROLLERDE.**

> **2026-06-19:** "Sahip app" kolonu **"Kullanıcıya görünen alan" + "Fiziksel sahip"** olarak
> ikiye ayrıldı. Finans kavramlarının fiziksel sahibi artık **LEENA DB** (ELIZA değil).

| Kavram | Kullanıcıya görünen alan | Fiziksel sahip |
|---|---|---|
| **Lead** | Sales / LIFFY | LIFFY DB |
| **Contact + Company** | Sales / LIFFY | LIFFY DB |
| **Quote** | Sales / LIFFY (AF `Q{ISO}-{seq}`) | LIFFY DB |
| **Sales Contract** | Finance / ELIZA tab 🔴 (AF `Q`→`A`, aynı sequence) | **LEENA DB** |
| **Payment / Revenue** | Finance / ELIZA tab 🔴 (frozen FX) | **LEENA DB** |
| **Commission** | Finance / ELIZA tab 🔴 (computed, per-row override) | **LEENA DB** |
| **Sales Agent** | Finance / ELIZA tab (~150 entity, çoğu login DEĞİL) | **LEENA DB** (Finance; Operations'ta DEĞİL — §5) |
| **Expense / Ledger / Accounts** | Finance / ELIZA tab 🔴 (çok-hesap, two-sided) | **LEENA DB** |
| **Expo (master)** | Operations / LEENA 🟢 | LEENA DB |
| **Cluster** | Operations / LEENA 🟢 (D28) | LEENA DB |
| **Expo finansal özeti (P&L)** | Finance / ELIZA tab 🔴 | **LEENA DB** |
| **Visitor / Check-in / Badge** | Operations / LEENA 🟢 | LEENA DB |
| **Exhibitor (operasyonel)** | Operations / LEENA 🟢 | LEENA DB |
| **Floor plan (Konva)** | Operations / LEENA 🟢 | LEENA DB |
| **Catalogue Generator** | Operations / LEENA 🔴 | LEENA DB |
| **Conference / session** | Operations / LEENA 🟢 | LEENA DB |
| **User (login kimliği)** | Admin / shared spine (§6) | **LEENA DB** (fiziksel sahiplik) |
| **Data entry contractor** | Admin / shared spine (login yok, public form) | **LEENA DB** |

### "Exhibitor" tek bir şey değil — üç rol
1 numaralı karıştırma sebebi:
- **Satılan şirket** (imza öncesi) → LIFFY (prospect/contact/company)
- **Para ilişkisi** (contract/payment/balance/commission) → **Finance / ELIZA tab (fiziksel LEENA DB)**
- **Sahadaki katılımcı** (floor/katalog/badge/build-up) → LEENA

→ "Exhibitor management" diye **tek bir app yok**. Satış = LIFFY, para = **LEENA Finance (ELIZA tab)**, operasyon = LEENA.

### Bir cross-app akış
On-site **lead scanner** (LEENA, exhibitor standında badge okutur) → yakalanan kişiler **LIFFY'ye lead** olarak akar.

---

## 2. LEENA — iç bilgi mimarisi (senin asıl odağın) 🟢

LEENA bugün ~15 düz menü gibi duruyor ("tek işi visitor" hissi buradan). Aslında **6 net iş kümesi** var. Kitle: Proje ekibi + saha + Owner.

**Kök = Expo bağlamı.** Önce expo seçilir, sonra her şey o expo'nun altında. + cross-expo "tüm expolar".

| # | Bölüm | Ne içerir | Ekran şekli | Durum |
|---|---|---|---|---|
| 1 | **Expolar** | Tüm expo portföyü; her expo'ya girince ops dashboard. **Cluster-aware** (aşağı bak) | Portföy listesi → expo ops dashboard | 🟢 |
| 2 | **Exhibitor** | İmzalı exhibitor onboarding (katalog, stand design, build-up, exhibitor badge); Catalogue Generator; on-site lead scanner | Liste+detay / generator wizard | 🟢 (Catalogue Gen 🔴) |
| 3 | **Floor plan** | Hall/stand/hücre editörü (Konva); stand yerleşimi + doluluk | Görsel editör (canvas) | 🟢 |
| 4 | **Visitor & Access** | Kayıt formları; visitor kayıt+import; check-in; badge template; terminaller; **Conferences buraya gömülü ayrı sayfa** (oturum + konferans tarayıcı + katılım) | Form builder / yoğun tablo (Visitor Log) / check-in konsolu | 🟢 |
| 5 | **Communications** | Email template/campaign/segment/gönderim; re-activation | Template editör / campaign composer / segment builder | 🟢 |
| 6 | **Reports** | Check-in/katılım/operasyonel raporlar | Dashboard + rapor görünümleri | 🟢 |

→ ~15 düz öğe **6 anlaşılır bölüme** indi. Üst nav (expo bağlamı = kök): **Dashboard · Exhibitor · Floor plan · Visitor & Access · Communications · Reports.** ("Exhibitor & Floor" ikiye ayrıldı; Conferences artık Visitor & Access içinde bir sayfa — üst-seviye tab değil.)

### Cluster — Expolar + dashboard bundan etkilenir
Bir venue'da aynı tarihte 2+ expo varsa (Cluster), tasarımcı **tek-expo varsayımıyla layout kurmamalı.** Expolar listesi cluster'ı bir grup olarak göstermeli; ops dashboard ya **birleşik** (operasyon tek) ya **expo-bazlı ayrılmış** (ticari ayrı) görünüm sunabilmeli. Layout'ta bu seçeneği baştan tut.

### LEENA dashboard'u tüm operasyonu yansıtmalı (sadece visitor değil)
"Tek işi visitor" algısını kıran şey bu. Bir expo'nun (veya cluster'ın) ops dashboard'u:
- **Exhibitor:** kaç imzalı / onboarded, floor doluluk %, katalog gelen/bekleyen
- **Visitor:** kaç kayıt / check-in, bugünkü kapı trafiği
- **Conference:** bugünkü oturum + katılım
- **Comms:** bekleyen/giden operasyonel mailler (badge, payment reminder…)
- **Geri sayım:** expo tarihine kalan, build-up durumu
- **Cluster ise:** birleşik vs expo-bazlı toggle

→ LEENA "bir expo'nun operasyon komuta merkezi" gibi okunur.

### Senin aday gruplaman → düzeltilmiş
- "visitor management" → ✅ **Visitor & Access** (ama altılıdan biri, app'in tek işi değil)
- "exhibitor management" → ⚠️ tek şey değil: operasyon LEENA, satış LIFFY, para ELIZA
- "expo management" → ✅ operasyonel **LEENA**, finans **ELIZA**
- "staff management" → ❌ LEENA değil; **Admin/shared spine** (§6). Sales agent ≠ staff.

---

## 3. LIFFY — iç bilgi mimarisi (satış workspace, imza öncesi) 🟡

Kitle: satış temsilcileri + Sales Manager.

**Pipeline = 7 aşama (requirements §2.2):** Lead → Contacted → Replied → Qualified Contact+Company → Quote Sent → Quote Signed → Sales Contract.
→ **Stage 1–6 LIFFY içinde** (lead → quote signed). **Stage 7 (Sales Contract) convert çıktısı = Finance / ELIZA tab; fiziksel olarak LEENA contract** (LIFFY dışına çıkar → LEENA DB).

| # | Bölüm | Ne içerir | Ekran şekli | Durum |
|---|---|---|---|---|
| 1 | **İşim / Action Screen** | Bugün ilgilenilecekler: gelen cevaplar, vadesi gelen takipler, kovalanacak quote'lar | Öncelikli iş akışı (home) | 🟡 |
| 2 | **Prospecting** | Lead mining (scraper), lead listeleri, campaign, sequence, segment | Mining konsolu / liste / campaign composer | 🟡 |
| 3 | **Contacts & Companies** | Qualify olmuş gerçek kişi/şirketler (CRM çekirdeği) | Liste + 360 detay | 🟡 |
| 4 | **Pipeline & Quotes** | Aşama board'u (1–6); quote oluştur/gönder/"signed" takibi | Pipeline board + quote editör/wizard | 🟡 pipeline / 🔴 quote |

> Requirements net: aktivite takibi ayrı "log" modülünden DOĞMAMALI; yapılan işten (mail gitti, quote üretildi, cevap geldi) **kendiliğinden** çıkmalı → home = Action Screen, ayrı "Tasks" değil. (Zoho task adoption başarısızlığının dersi.)

**Convert burada biter:** signed quote → Proje ekibinin kuyruğuna düşer.

---

## 4. Finance / ELIZA tab — LEENA içindeki ticari kayıt + zeka (kısa)

Kitle: Owner, Finance, Proje ekibi (finans tarafı). **Çoğu greenfield — dikkat.**

| # | Bölüm | Ne içerir | Durum |
|---|---|---|---|
| 1 | **War Room / Executive** | Owner'ın günlük yönetici görünümleri | 🟡 |
| 2 | **Contracts** | Sales Contract'lar (convert sonrası), operasyonel alanların doldurulması | 🔴 |
| 3 | **Money** | Payment/Revenue, Expense, Ledger/Accounts (çok-hesap, two-sided, frozen FX) | 🔴 |
| 4 | **Commissions & Agents** | ⭐ Komisyon hesabı + **Sales Agent registry** (burada yaşıyor) | 🔴 |
| 5 | **Expo Finance** | Expo başına P&L / bütçe-vs-gerçek | 🔴 |
| 6 | **Intelligence** | AI query engine + WhatsApp bot | 🟡 |

> ⚠️ Bu 6 bölüm "nihai hedef"; kullanıcıya **ELIZA / Finance tab** olarak görünür ama **fiziksel olarak LEENA DB**'dedir. **Eski ELIZA contracts/payments Zoho mirror'dır; aktif mimariye migrate edilmeyecek.** Faydalı ekranlar/raporlar gereksinim olarak saklanır; finance modeli **LEENA'da yeniden kurulur** (gerçek migration ileride Zoho → LEENA).

---

## 5. "Sales agent nerede?" — net cevap

**Sales Agent, LEENA'nın Operations modülünde DEĞİLDİR; LEENA Finance / ELIZA tab içinde yaşar.** Çoğu login olmayan komisyon entity'sidir; User ile aynı şey değildir. (Fiziksel olarak LEENA DB; LIFFY'de değil.)

- Sales agent = bir **Sales Contract** üstünde **komisyonun atfedildiği entity**. Sözleşme + komisyon LEENA Finance'ta → agent oraya ait.
- ~150 agent'ın çoğu (dış acente, freelancer, ayrılmış personel) **login DEĞİL** — hiçbir app açmaz; sadece sözleşmede isim. Yani finans/admin kavramı.
- LEENA **Operations** (visitor/exhibitor/floor) ile ilgilenmez; agent **LEENA Finance**'ta yaşar. "LEENA'da değil" değil → **"LEENA Operations'ta değil; LEENA Finance'ta."**

**Üç kimlik ayrı (locked Bölüm 1):**
- **User** (~25): login var. Platform spine, Admin'de.
- **Sales Agent** (~150): komisyon entity'si. **LEENA Finance / ELIZA tab.** Çoğu login yok.
- **Data entry contractor**: login yok, public form. Spine.

→ Bir user *aynı zamanda* agent olabilir, ama "user" (login) ≠ "agent" (komisyon): iki ayrı kavram, iki ayrı tablo.

---

## 6. Paylaşılan kabuk (ELL shell) — iki halka + erişim matrisi + Admin

**Omurga = iki halka, arada convert gate (güven sınırı):**
- **Dış halka — LIFFY (satış/freelancer):** finans/komisyon GÖRMEZ. Sadece satışını yapar.
- **İç halka — LEENA Operations + LEENA Finance / ELIZA tab (proje + Owner):** güvenilir; operasyon + para.

Bu sadece veri-scope'u değil, **app erişim sınırı** — shell'in üst navigasyonunu belirler. Bir freelancer'da **Finance (ELIZA) sekmesi hiç görünmez.**

### Kim hangi domain'i görür (üst nav)

| Rol | Sales (LIFFY) | Operations (LEENA) | Finance (ELIZA) |
|---|:---:|:---:|:---:|
| **Owner** | ✅ | ✅ | ✅ |
| **Proje ekibi** | —† | ✅ | ✅ |
| **Sales Manager** | ✅ | — | (ince komisyon dilimi? — teyit*) |
| **Sales rep / freelancer** | ✅ | — | — |

\* §1.5: CEO + Sales Manager komisyon-oranını ayarlar → Sales Manager'a sınırlı bir komisyon görünümü gerekebilir. Shell detaylandırılırken Suer teyit eder.
† Proje ekibinin LIFFY'ye **tam** erişimi yok; ama convert'i onlar yapar (D12) → signed quote'ları **convert kuyruğunda görüp kalite-kontrol eder.** Yani "—" tam-kapalı değil: convert review için **sınırlı/read LIFFY görünürlüğü** vardır. Şekli (ayrı convert kuyruğu mu, LIFFY-içi read mi) shell tasarımında netleşir.
> Local office staff fonksiyonuna göre miras alır: local **sales** → Sales halkası; local **project** → Operations(+Finance) halkası. Profil şablonları (10 adet, requirements 3.1) bu matrisi seed eder.

### Domain-içi scope = reports_to zinciri
Halka erişiminden SONRA, halka içinde görünürlük **reports_to hiyerarşi zinciri** üzerinden: her yönetici kendi astlarını (zincir boyunca) görür. Üç seviye kapsanır: **Sales Manager → Sales Team Lead → Sales Rep.** (İki-uçlu değil; ara katman da kendi altını görür.)

### Global search
Scope'a saygılı. **Not (2026-06-19):** Global search **iki DB** üstünden çalışır: **LIFFY + LEENA**. Sonuçlar kullanıcıya **Sales / Operations / Finance** diye gruplanabilir; **Operations ve Finance aynı LEENA DB'den** gelir.

### Admin (= senin "staff management")
User'lar, roller, raporlama hattı (reports_to), ofis atamaları, permission matrisi. **Admin/shared spine kullanıcıya platform-seviyesi görünür; fiziksel sahiplik LEENA DB'de kabul edilir** (aksi açıkça kararlaştırılmadıkça ayrı üçüncü DB yaratılmaz). LIFFY bu kullanıcıları SSO/service bridge ile tanır/map eder.

### Settings → Appearance (tema sistemi)
Renk **token-tabanlı** (role'lere bağlı: primary/accent/neutral/semantic) → tema = bir set token değeri. Kullanıcı ayarlardan tema seçer, tercih **kişi-bazlı** saklanır, tüm ekranlara uygulanır.
- **Default: Vermillion** (Japanese editorial — sıcak ivory + vermillion + jade). İkinci tema: **Cobalt** (vivid cool).
- **Light / Dark:** planlı (rol-flip token yapısı hazır).
- **Tema kütüphanesi:** keşifte üretilen diğer paletler saklı, istenince "promote" edilir.
- **Sınır (kalite, estetik değil):** her tema okunur kontrast + sağlam semantic renk (success/warning/error/live) korur. Serbest "her hex'i seç" editörü YOK — over-engineering + okunabilirlik riski; küçük tasarlanmış tema seti yeterli.

---

## 7. Özet — dört cümlede

1. **İki sistem = iki güven halkası; üç kullanıcı domain'i = Sales, Operations, Finance.** LIFFY satış (imza öncesi), LEENA operasyon (imza sonrası saha) + **LEENA Finance (ELIZA tab)** para+zeka. **Finance/ELIZA ayrı sistem değil, LEENA Finance modülüdür.** Convert = iki dönüşüm + güven sınırı.
2. **Çakışan kavramlar farklı rollerde:** exhibitor → satış LIFFY / para **LEENA Finance** / saha LEENA. Expo → master LEENA / finans **LEENA Finance**. **Sales agent → LEENA Finance (Operations'ta değil). Staff/user → Admin (spine, fiziksel LEENA DB).**
3. **LEENA 6 bölüm** (Expolar → Exhibitor / Floor plan / Visitor&Access [Conferences içinde] / Communications / Reports), cluster-aware, dashboard tüm operasyonu yansıtır.
4. **Shell = iki halka:** freelancer sadece Sales görür, Finance sekmesi yok; halka-içi scope reports_to zinciriyle. **Harita nihai hedef — ticari çekirdek 🔴 greenfield, tasarımcı bunu bilmeli.**
