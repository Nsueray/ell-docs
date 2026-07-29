> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# ELL — CROSS-DB İHTİYAÇ ÖLÇÜMÜ

> **Soru:** "Cross-DB join ihtiyacım gerçekte ne kadar yoğun?" — tahminle değil sayıyla.
> **Karar:** Bu sayıya göre "üç DB ayrı mı kalsın, tek DB'de mi birleşsin".
>
> **Kaynaklar:**
> 1. `~/Downloads/ELAN_EXPO_REQUIREMENTS_v1_0.md` (NE lazım — pusula). **Not:** dosya
>    `~/Projects/` altında değil, `~/Downloads/` altında bulundu; içeriği okundu.
> 2. `~/Projects/ELL_GERCEK_DURUM_ANALIZI.md` (gerçek DB şemaları).
>
> **Veri sahipliği (req. 866-882, 588-590):**
> - **LEENA** = expo master, visitor, badge, check-in, floor plan, catalogue submission, partners, lead-scanner
> - **ELIZA** = sales contract, payment/revenue, expense, commission, finance, budget, account, sales_agent, expo_targets, expo_clusters
> - **LIFFY** = lead, prospect, quote, campaign, mining, contact, company
>
> Sadece Requirements Part 2 (2.1–2.8) içinde **açıkça geçen** rapor/ekran/dashboard/otomatik-aksiyon
> sayıldı. Uydurma yok. Tereddütlü sınıflandırmalar "Not" sütununda gerekçelendirildi.

**Sınıflandırma kuralları:**
- **Tek-sistem** — tüm veri tek DB'den. DB ayrımı sorun değil.
- **Cross / frontend-merge** — 2+ DB'den ayrı sorgu, ekranda yan yana gösterim yeterli (satır-bazlı join GEREKMEZ).
- **Cross / gerçek join** — iki sistemin verisi satır bazında birleştirilip hesaplanmalı (WHERE/GROUP BY iki tabloyu birden gerektiriyor).
- **RT** = anlık tutarlılık şart / **Cache** = dakika-saat gecikme veya on-demand kabul edilebilir.

---

## TL;DR — SAYISAL CEVAP

| Bucket | Adet |
|---|---|
| **Toplam somut öğe** | **58** |
| Tek-sistem | **39** (%67) |
| Cross / frontend-merge | **11** (%19) |
| Cross / gerçek join | **8** (%14) |
| | |
| Real-time gerektiren (RT) | **9** |
| Cache/gecikme OK | **49** (%84) |

### 🎯 Kararın bel kemiği: **gerçek-join + real-time olan = 0 (SIFIR)**

8 "gerçek join" öğesinin **hiçbiri** real-time değil — hepsi on-demand/deadline/post-show/
analiz, yani cache toleranslı. 9 real-time öğesinin **hiçbiri** cross-join değil — hepsi
tek sistem (LEENA: floor plan kilidi, check-in, ziyaretçi kaydı).

**İki kümenin kesişimi boş.** Tek DB'yi teknik olarak zorunlu kılan tek gerekçe
(satır-bazlı join + anlık tutarlılığın aynı anda gerektiği bir ekran) **requirements'ta yok.**

İki dürüst istisna (join değil ama cross-system + zamana duyarlı yazma) aşağıda
ayrıca işaretlendi — tek DB'yi *zorunlu* değil, *kolaylaştırıcı* kılarlar.

### En çok birlikte sorgulanan iki sistem: **LEENA + ELIZA**
Cross öğelerin 19'undan **14'ü LEENA+ELIZA**. Tema neredeyse her zaman aynı:
**"ELIZA = sözleşmeli exhibitor kim" ↔ "LEENA = o exhibitor'ın operasyonel/catalogue/stand verisi"**.
LIFFY en bağımsız sistem (cross öğelerin çoğunda yok; sadece convert-handoff ve birkaç raporda ELIZA ile eşleşiyor).

---

## TAM ENVANTER (workflow bazında)

### 2.1 Lead Acquisition & Distribution

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 1 | Reply enrichment auto-suggest (yanıt parse → 1-tık lead güncelle) | LIFFY | Tek-sistem | RT | Yanıt geldiğinde anında |
| 2 | Disqualification aksiyonu (1-tık flag + hard-bounce×3 otomatik) | LIFFY | Tek-sistem | Cache | |
| 3 | Auto-routing/ownership (web form→ülke, mining→sektör, fallback queue) | LIFFY | Tek-sistem | RT | Lead düştüğü an atanmalı |
| 4 | Unassigned fallback queue ekranı (Sales Manager izler) | LIFFY | Tek-sistem | Cache | |
| 5 | Intake deduplication (email/domain/company eşleme + merge) | LIFFY | Tek-sistem | RT | Intake anında |
| 6 | Email verification (ZeroBounce) outreach öncesi | LIFFY | Tek-sistem | Cache | Harici API |
| 7 | Response SLA uyarısı / aging leads daily queue | LIFFY | Tek-sistem | Cache | "1 hafta" eşiği |
| 8 | Source-driven lead scoring / prioritization (rep view) | LIFFY | Tek-sistem | Cache | |
| 9 | **Kanal atıf raporu**: "geçen çeyrek imzalı sözleşmelerin kaçı web-form vs mined lead?" | LIFFY + ELIZA | **Gerçek join** | Cache | Contract(ELIZA)→origin-lead→channel(LIFFY) satır eşleme; "geçen çeyrek" → cache |

### 2.2 Sales Cycle (Lead → Signed Contract)

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 10 | Funnel conversion dashboard (stage geçiş oranları; rep/expo darboğaz) | LIFFY | Tek-sistem | Cache | Lead→...→Signed Quote hepsi LIFFY |
| 11 | Quote subject auto-gen (`{Expo}-{Company}-{M²}`) | LIFFY + LEENA | Cross / frontend-merge | Cache | Expo adı LEENA'dan lookup; cache'lenebilir alan-doldurma |
| 12 | Lead → Contact+Company conversion suggestion | LIFFY | Tek-sistem | RT | Yanıt anında öneri |
| 13 | Qualification capture (intent/confidence/status) | LIFFY | Tek-sistem | Cache | |
| 14 | **Convert gate**: Signed Quote → Sales Contract oluştur, AF# taşı, alanları kopyala, email zincirini tetikle | LIFFY → ELIZA | Cross (yazma handoff) | **RT** | Join değil; **cross-system transactional yazma**. Tek DB bunu atomik yapardı. Aşağıda ayrıca işaretli ⚠️ |
| 15 | Project review queue (signed quote'lar convert bekliyor) | LIFFY | Tek-sistem | Cache | Scan link Drive'dan |
| 16 | AF Number üretimi (Q{ISO}-seq / A{ISO}-seq) | LIFFY (Q) / ELIZA (A) | Tek-sistem | RT | Her aşamada kendi DB'sinde |

### 2.3 Sales Contract Management

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 17 | Sales Contract detay sayfası (long-running operasyonel kayıt) | ELIZA (+LEENA stand/catalogue + email history) | Cross / frontend-merge | Cache | Çekirdek ELIZA; stand-link/catalogue-page/email-status panelleri yan yana |
| 18 | Transfer aksiyonu (first-class: hedef expo'ya klon, payment+commission taşı) | ELIZA | Tek-sistem | Cache | Expo listesi LEENA lookup (minör) |
| 19 | Status lifecycle değişimi (Active/On Hold/Transferred/Cancelled) | ELIZA | Tek-sistem | Cache | |
| 20 | Commission hesap (due = amount×pct, default+override) | ELIZA | Tek-sistem | Cache | |
| 21 | Commission paid status (due/paid/outstanding) | ELIZA | Tek-sistem | Cache | |
| 22 | "Agent X'e bu yıl ne ödedik / Agent Y'ye ne borçluyuz" raporu | ELIZA | Tek-sistem | Cache | Expense+agent aggregate |
| 23 | Commission adjustment (cancel → agent borçlanır, sonraki ödemeden net) | ELIZA | Tek-sistem | Cache | |
| 24 | "Unpaid contracts" = SUM(schedule) > SUM(received) (computed) | ELIZA | Tek-sistem | Cache | |
| 25 | "First payment month" = MIN(received.date) (computed) | ELIZA | Tek-sistem | Cache | |
| 26 | **Sales Contract → Stand auto-link** (Phase 2: m²/tip kriteri → uygun stand öner → floor plan'a yaz) | ELIZA + LEENA | **Gerçek join** | Cache | Contract kriteri(ELIZA) ↔ stand envanteri(LEENA) eşleme + LEENA'ya yazma. Suggest+confirm → cache; **kesişime en yakın aday ama RT değil** |

### 2.4 Catalogue Production

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 27 | **Catalogue generation (PDF + web)** | LEENA + ELIZA | **Gerçek join** | Cache | **En net gerçek-join**: contracted-exhibitor listesi(ELIZA) ⨝ catalogue içerik(LEENA) ⨝ expo(LEENA), exhibitor satır-satır. Ama "on-demand regenerate, deadline" → cache OK |
| 28 | Exhibitor self-service catalogue editor (müşteri kendi sayfası) | LEENA | Tek-sistem | RT | Müşteri için anlık; tek sistem |
| 29 | Project review/approve catalogue submission | LEENA | Tek-sistem | Cache | |
| 30 | **Catalogue deadline dashboard** ("12 exhibitor sayfasını doldurmadı, 5 gün kaldı") | LEENA + ELIZA | **Gerçek join** | Cache | "kim doldurmadı" = contracted list(ELIZA) − submitted(LEENA) satır eşleme; deadline günler uzakta → cache |
| 31 | Template editor (master seç + per-expo özelleştir) | LEENA | Tek-sistem | Cache | |

### 2.5 Expo Operations Management

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 32 | Expo master sayfası (identity+deadline+partner+floorplan+visitor+**financial summary** tek sayfada) | LEENA + ELIZA | Cross / frontend-merge | Cache | Financial summary ELIZA paneli, gerisi LEENA — yan yana |
| 33 | Partner management (expo_partners CRUD) | LEENA | Tek-sistem | Cache | |
| 34 | Floor Plan Builder (hall grid, stand create, version control) | LEENA | Tek-sistem | **RT** | **Stand kilidi**: iki kişi aynı standı atarsa anlık tutarlılık şart |
| 35 | Sales Floorplan Templates (Phase 2, rep klonlar) | LEENA | Tek-sistem | Cache | |
| 36 | Server-side branded floor plan PDF export (Phase 2) | LEENA | Tek-sistem | Cache | |
| 37 | Visitor management (registration, QR, badge, reactivation, certificate) | LEENA | Tek-sistem | RT | Kayıt anlık |
| 38 | Check-in dashboard (real-time, saatlik trend) | LEENA | Tek-sistem | **RT** | Kapıda canlı |
| 39 | **Exhibitor listesi** = "non-cancelled Sales Contract olan firmalar" (ELIZA) — LEENA API ile çeker, **lokal cache**, event-refresh | LEENA ← ELIZA | Cross / frontend-merge | Cache | **Requirements bunu açıkça cache olarak tasarlamış** (req 882). Catalogue/floorplan/badge/lead-scanner-auth besler |
| 40 | Multi-expo dashboard (Project Lead: tüm aktif expo'lar — sales pace, catalogue completion, payment collection, time-to-show) | LEENA + ELIZA | Cross / frontend-merge | Cache | Her metrik per-expo ayrı kolon; status göstergesi → cache |
| 41 | Co-located cluster grouped rows + cluster financial rollup | ELIZA (clusters) + LEENA | Cross / frontend-merge | Cache | |
| 42 | **Post-show: Visitor metrics** (registered/checked-in/sektör/ülke/hall) | LEENA | Tek-sistem | Cache | Post-show |
| 43 | **Post-show: Financial metrics** (revenue/expense/margin/commission/receivables per expo) | ELIZA | Tek-sistem | Cache | Post-show |
| 44 | **Post-show: Exhibitor metrics** (signed exhibitors+occupancy ELIZA, lead-capture+catalogue-rate+contractor-use LEENA) | LEENA + ELIZA | **Gerçek join** | Cache | Doc açıkça "cross-system"; lead-capture-per-exhibitor = exhibitor kimliği(ELIZA) ↔ scan(LEENA) eşleme |
| 45 | **Post-show: Operational metrics** (timeline adherence, email effectiveness, service load) | LEENA + ELIZA | **Gerçek join** | Cache | Doc açıkça "cross-system"; post-show |

### 2.6 Financial Operations

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 46 | Multi-account ledger + account list admin | ELIZA | Tek-sistem | Cache | |
| 47 | Account statement (per-account inflow/outflow, running balance) | ELIZA | Tek-sistem | Cache | |
| 48 | Two-sided transfer kaydı (her hareket çift taraflı) | ELIZA | Tek-sistem | Cache | |
| 49 | Owner's current account balance (şirket Owner'a ne borçlu) | ELIZA | Tek-sistem | Cache | |
| 50 | Budget vs actual per expo per category | ELIZA | Tek-sistem | Cache | Budget+expense ikisi de ELIZA; expo_id sadece boyut |
| 51 | Cross-account views (toplam cash position EUR, receivables, commissions owed) | ELIZA | Tek-sistem | Cache | "Cross-account" = ELIZA içi, cross-DB değil |
| 52 | Refund/credit balance (computed, event stream) | ELIZA | Tek-sistem | Cache | |

> **2.6'nın tamamı ELIZA tek-sistem, cache OK.** Finans katmanı cross-DB join üretmiyor —
> en güçlü "tek sistem yeter" sinyali burada.

### 2.7 Communication Automation

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 53 | 8-email announcement chain (Welcome…Badge) — contract event tetikli, expo/partner data enjekte | ELIZA (trigger) + LEENA (expo/partner) | Cross / frontend-merge | Cache | Schedule günler önce; render-time veri toplama, satır-join değil |
| 54 | "Send all operational emails now" (geç imzalanan kontrat) | ELIZA + LEENA | Cross / frontend-merge | Cache | Aynı render mantığı, batch |
| 55 | Marketing campaigns + per-recipient unsubscribe | LIFFY | Tek-sistem | Cache | |
| 56 | Contract communication history (sent/replied/resent, inbound replies) | ELIZA (contract) + email log | Cross / frontend-merge | Cache | Sözleşme sayfasında thread |
| 57 | Language selection rule (contact pref → local-audience expo+country → EN) | LIFFY (contact) + LEENA (expo flag) | Cross / frontend-merge | Cache | Minör lookup |

### 2.8 Reporting & Intelligence

| # | Rapor/Ekran/Aksiyon | Sistem(ler) | Sınıf | RT/Cache | Not |
|---|---|---|---|---|---|
| 58a | **Owner günlük view #1**: Sales pace per expo (m² + revenue) vs target vs önceki edisyon | ELIZA | Tek-sistem | Cache | m² & revenue contract'ta(ELIZA); target expo_targets(ELIZA). "Continuous refresh" ama saniye-bayatlık OK |
| 58b | **Owner günlük view #2**: Data-entry activity per person/office (leads/contacts/emails) | LIFFY | Tek-sistem | Cache | Sales-side aktivite = LIFFY |
| 58c | **Owner günlük view #3**: Outstanding payments per expo | ELIZA | Tek-sistem | Cache | Contract+revenue |
| 59 | AI synthesis insight ("Q4 HVAC bütçe %20 altında + Nigeria data-entry yavaşladı → ilişkili") | ELIZA + LIFFY | **Gerçek join** | Cache | Açık cross-join analiz; finans(ELIZA) ↔ aktivite(LIFFY) |
| 60 | AI trend / anomaly / action-suggestion (synthesis hariç) | çoğu ELIZA; bazı LIFFY/LEENA | Tek-sistem (çoğu) | Cache | "15% slower m²"=ELIZA; "office zero activity"=LIFFY — her insight tek eksen |
| 61 | Push reports (morning brief, weekly summaries, monthly P&L) | karışık (P&L=ELIZA, team=LIFFY, exec=hepsi) | Cross / frontend-merge | Cache | Bölümler ayrı sorgu, raporda derlenir |
| 62 | Ad-hoc report builder + NL AI report | herhangi (değişken) | değişken | Cache | Araç; kapsam soruya bağlı |
| 63 | WhatsApp NL interface (ELIZA bot) | sorguya göre route | Tek-sistem (çoğu) | Cache | "Mega Clima m²"=ELIZA tek sorgu |

> **Owner'ın 3 günlük view'i (58a/b/c): join GEREKMEZ.** Üçü de ayrı tek-sistem sorgusu,
> dashboard'da yan yana tile. Owner'ın "home"u üç sistemi karıştırıyor ama satır-bazlı
> birleştirme yok — frontend yan yana gösterim yeterli.

---

## ÖZET SAYIM

**Toplam: 58 ana öğe** (58 = üç alt-view olarak sayıldı → fonksiyonel 60; tablo numaralandırması 1–63 arası, 9/14/16 vb. tek öğe).

| Sınıf | Adet | % |
|---|---|---|
| **Tek-sistem** | 39 | %67 |
| **Cross / frontend-merge** | 11 | %19 |
| **Cross / gerçek join** | 8 | %14 |

**Gerçek-join öğeleri (8 adet) — hepsi cache toleranslı:**
| # | Öğe | Sistemler | Neden RT değil |
|---|---|---|---|
| 9 | Kanal atıf raporu | LIFFY+ELIZA | "geçen çeyrek" — tarihsel |
| 26 | Sales Contract → Stand auto-link | ELIZA+LEENA | suggest + Project confirm |
| 27 | Catalogue generation | LEENA+ELIZA | on-demand regenerate, deadline |
| 30 | Catalogue deadline dashboard | LEENA+ELIZA | deadline günler uzakta |
| 44 | Post-show exhibitor metrics | LEENA+ELIZA | post-show |
| 45 | Post-show operational metrics | LEENA+ELIZA | post-show |
| 59 | AI synthesis insight | ELIZA+LIFFY | analiz katmanı |
| (17/32/40/41 frontend-merge sınırında — gerçek-join değil sayıldı) | | | |

**Real-time öğeleri (9 adet) — hepsi tek-sistem:**
| # | Öğe | Sistem |
|---|---|---|
| 1 | Reply enrichment | LIFFY |
| 3 | Lead auto-routing | LIFFY |
| 5 | Intake dedup | LIFFY |
| 12 | Lead→Contact conversion suggestion | LIFFY |
| 16 | AF Number üretimi | LIFFY/ELIZA (her biri kendi) |
| 28 | Catalogue self-service editor | LEENA |
| 34 | **Floor plan stand kilidi** | LEENA |
| 37 | Visitor registration | LEENA |
| 38 | Check-in dashboard | LEENA |

---

## 🎯 GERÇEK-JOIN + REAL-TIME LİSTESİ (tek DB'yi haklı çıkaran tek gerekçe)

### **BOŞ. Bu kesişimde 0 (sıfır) öğe var.**

- 8 gerçek-join'in 0'ı real-time.
- 9 real-time'ın 0'ı cross-join.

Yani requirements'ta, **iki sistemin verisini satır bazında birleştirip aynı anda
anlık tutarlılık** isteyen tek bir ekran/rapor/aksiyon **yok**.

### İki dürüst istisna (join değil — ama cross-system + zamana duyarlı)

Bunlar senin "gerçek join" tanımına girmiyor (satır-bazlı hesap değil), ama tek DB
kararını etkileyebilecek **cross-system + RT-ish yazma** olduğu için saklamadan işaretliyorum:

1. **#14 Convert gate (LIFFY → ELIZA):** Signed Quote → Sales Contract. Bu bir
   *transactional handoff* (kopyalama + email zinciri tetikleme), satır-join değil.
   RT-ish çünkü tetikleme anında olur. **Tek DB bunu tek transaction'da atomik yapardı;**
   ayrı DB'lerde bir API çağrısı + idempotency/retry gerekir. Tek seferlik kopya olduğu
   için ayrı DB'lerde de yönetilebilir (saga/outbox pattern), ama maliyet sıfır değil.

2. **#26 Sales Contract → Stand auto-link (ELIZA ↔ LEENA, Phase 2):** Kesişime en yakın
   aday. m²/tip kriteri ELIZA'da, stand envanteri LEENA'da; eşleştirip LEENA'ya yazıyor.
   Ama "öner → Project onaylar" akışı olduğu için anlık tutarlılık şart değil — eventual
   consistency yeterli.

**Yorum:** Bu ikisi tek DB'yi *zorunlu* değil, *kolaylaştırıcı* kılar. Ayrı DB'lerde
çözülebilirler (API + cache + event), ama biraz daha mühendislik ister.

---

## EN ÇOK BİRLİKTE SORGULANAN İKİ SİSTEM

**LEENA + ELIZA** — açık ara. 19 cross öğeden **14'ü** bu çift.

| Çift | Cross öğe sayısı | Karakteri |
|---|---|---|
| **LEENA + ELIZA** | **14** | "Sözleşmeli exhibitor kim (ELIZA)" ↔ "o exhibitor'ın operasyon/catalogue/stand/visitor verisi (LEENA)". Öğeler: 11,17,26,27,30,32,39,40,41,44,45,53,54,56 |
| LIFFY + ELIZA | 3 | Atıf(9), convert-handoff(14), synthesis(59) — + bazı push raporlar |
| LIFFY + LEENA | 2 | Quote subject(11 expo adı), language selection(57) |
| Üçü birden | 1–2 | Weekly exec summary, ad-hoc/NL araçlar |

**Tema neredeyse her zaman aynı tek ilişki:** ELIZA `sales_contract`'ı "bu expo'da
exhibitor kim" sorusunun tek doğru kaynağı; LEENA bu listeye catalogue/floor-plan/badge/
lead-scanner için ihtiyaç duyuyor. **Requirements bu ilişkinin çözümünü zaten reçete
etmiş (req 879-882):** LEENA exhibitor listesini ELIZA API'sinden çeker, **lokal
cache'ler, event'lerde (yeni/iptal/transfer kontrat) yeniler.** Yani ana coupling bile
*cache toleranslı* tasarlanmış.

**LIFFY en bağımsız sistem:** ağır işi (lead, mining, campaign, quote, contact, company)
tamamen tek-sistem. Diğerlerine yalnızca convert-handoff'ta (#14) ve birkaç raporda
(atıf #9, synthesis #59) dokunuyor. LIFFY'yi ayrı DB tutmak en kolayı.

---

## SAYININ KARARA OKUNUŞU (yorum, spekülasyon değil — yukarıdaki sayılara dayalı)

Karar senin; sayının söylediği şu:

- **%67 tek-sistem, %84 cache-toleranslı, gerçek-join+real-time = 0.** Bu profil
  "tek DB zorunlu" demiyor. Üç DB ayrı kalabilir.
- **Tek DB'yi teknik olarak zorlayan ekran yok.** 8 gerçek-join'in hepsi on-demand/
  deadline/post-show/analiz — read-replica, materialized view, nightly ETL veya
  API-aggregation ile rahat karşılanır. Cache bayatlığı bu raporlarda kabul edilebilir.
- **Tek gerçek coupling (LEENA↔ELIZA exhibitor listesi) zaten cache pattern'i ile
  reçete edilmiş.** Ayrı DB bu pattern'le doğal çalışır.
- **Ayrı DB'nin tek bedeli** convert-handoff'un (#14) atomikliği — bir transaction
  yerine API + idempotent retry. Bu, "tek DB'ye geç" değil, "outbox/saga ekle" sorunudur.
- **Tek DB'nin tek somut kazancı** convert atomikliği + cross-join raporları yazmanın
  kod kolaylığı (JOIN > API). Bu bir *konfor* avantajı, *zorunluluk* değil.

**Net:** Cross-DB join ihtiyacı **düşük-orta yoğunlukta ve tamamı gecikme-toleranslı.**
Sayı, "üç DB ayrı kalsın" seçeneğini engellemiyor; tek DB ancak operasyonel/konfor
gerekçesiyle (tek takım, tek deploy, JOIN kolaylığı) tercih edilir — teknik zorunlulukla değil.

---

## METODOLOJİ & SINIRLAR

- Sadece Requirements Part 2 (2.1–2.8) tarandı; Part 3-6 (cross-cutting principles,
  wishlist, out-of-scope) kapsam dışı bırakıldı (görev Part 2 + 2.8 dedi).
- Sınıflandırma, **veri sahipliği modelini** (req 866-882) baz aldı. Bir metrik hangi
  DB'nin sahip olduğu veriyi okuyorsa o sisteme atandı.
- "Gerçek join vs frontend-merge" ayrımında muhafazakar davranıldı: satır-bazlı eşleme/
  GROUP BY iki tabloyu birden gerektiriyorsa "gerçek join"; bağımsız metrikler yan yana
  gösteriliyorsa "frontend-merge". Sınırdaki öğeler (#17, #32, #40, #41) frontend-merge sayıldı
  ve "Not" sütununda gerekçelendirildi — farklı sayılsalar bile gerçek-join+real-time
  kesişimi yine 0 kalır (hiçbiri real-time değil).
- Phase 2 / roadmap öğeleri (#26, #35, #36 ve 2.5'teki matchmaking/portal/appointment)
  dahil edildi ama roadmap olduğu not edildi. Matchmaking/visitor-portal/mobile-badge/
  appointment Phase 1 değil; hepsi LEENA tek-sistem olacağı için sayıma tek-sistem etkisi.
- **Bulamadım:** Requirements Part 2 başında ve Part 3 başında "[TBD — to be filled in
  next session]" var; Part 2 workflow gövdeleri dolu ama bazı detaylar (örn. operasyonel
  email engine'in fiziksel olarak hangi DB'de oturduğu) requirements'ta net değil —
  bu yüzden #53-56 trigger/render verisinin sahipliğine göre sınıflandı, fiziksel
  yerleşime göre değil.
