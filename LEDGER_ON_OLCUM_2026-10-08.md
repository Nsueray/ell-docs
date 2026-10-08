# LEDGER ÖN-ÖLÇÜMÜ — 2026-10-08 (2d, salt okuma)

> **Ne:** Sentez'in ledger kriter turuna girdi. Ledger = hesaplar (kasa/banka) · transferler ·
> bütçe · gider · gelir. Yalnız ÖLÇÜM: bugün ne yazılı, ne var, ne boş. **Öneri, tasarım,
> karar YOK.**
> **Ölçüm anı:** ell-docs `5e8b193` · LEENA `main` `ae3cd4f` · DB bağlantısı YOK.
> **Kural:** başka belgelerden uzun alıntı yok — satır referansı + kendi cümlemle özet.
> Kısaltma: **REQ** = `ELAN_EXPO_REQUIREMENTS_v1_0.md`.

---

## 0. Gereksinim belgesi

- Tek sürüm: `ELAN_EXPO_REQUIREMENTS_v1_0.md` (kök), **2305 satır**, son commit `a416fa9`
  (2026-07-20, ELIZA amendment'ı). Repoda başka sürüm YOK (`git ls-files` taraması). README
  bunu "kanonik ihtiyaç dokümanı" olarak listeler.
- Etiketler (REQ:20-22): `[TBD]` yalnız REQ:163 ve REQ:1363'te (Part 2 ve Part 3 girişleri);
  `[PRINCIPLE]` 3.1 / 3.2 / 3.3 başlıklarında (REQ:1365, 1459, 1509); `[FACT]` Part 1'de.
  §2.6'nın kendisi etiketsizdir.

---

## 1. Gereksinim maddeleri (ledger kapsamı)

| # | Başlık | Satır | Etiket | Özet (kendi cümlem) | İçindeki açık soru / TBD |
|---|---|---|---|---|---|
| R1 | Çok-hesaplı ledger, düzenlenebilir hesap listesi | 934-940 · 3.3: 1549-1553 | — · [PRINCIPLE] | Hesaplar referans veridir (ad, para birimi, ofis, tür: banka / kasa / sanal); admin ekranından eklenir; kapanan hesap silinmez, pasiflenir. | Hesap türlerinin tam listesi yalnız örnekle verilmiş. |
| R2 | Her para hareketi iki taraflı | 942-958 · 3.3: 1531-1541 | — · [PRINCIPLE] | Hesaplar arası her hareket çıkış + giriş olarak, tek mantıksal olay halinde bağlı kaydedilir; tek taraflı kayıt hata durumudur. | **Veri şekli açık:** tek transfer olayı mı, iki bağlı işlem mi — "implementation choice is not made here" (956). |
| R3 | Sahibin şirkete karşı cari hesabı | 960-970 | — | Sahibin cebinden ödediği gider, şirketin ona borcu olarak otomatik görünür; geri ödeme bu bakiyeyi azaltır. | **Mekanizma açık:** gider doğrudan cari hesabı mı gösterir, yoksa "Owner cash" yöntemi eşli transfer mi üretir (970). Başka kişilere genişleme opsiyonel (968). |
| R4 | Para birimi, donmuş kur, EUR konsolidasyonu | 972-984 · 3.3: 1517-1529, 1555-1559 · 1.2: 52 | — · [PRINCIPLE] · [FACT] | Her EUR-dışı işlem girişteki kuru taşır, kur sonradan değişmez; EUR karşılığı girişte hesaplanıp saklanır; günlük kur tablosu yalnız öneri olabilir. | Kur farkı kar/zararı yalnız yer tutucu (984). |
| R5 | Gider ve gelir: temel varlıklar ve kategoriler | 986-996 · 3.5: 1658-1662 | — | Gider iki seviyeli (6 kategori × ~75 tip), gelir düz liste (15 kategori) + serbest açıklama; her kayıtta expo (nullable), kategori, tutar+kur+EUR, hesap, karşı taraf, tarih, yöntem, not, oluşturan; gelirde kontrat bağı. | — |
| R6 | Gelir = ödeme başına bir kayıt, kontrata bağlı | 998-1008 · 2.3: 505-518 | — | Her tahsilat ayrı gelir kaydıdır; kontratın "alınan" toplamı türetilir, saklanmaz; plan (vade) ile gerçekleşen ayrı tutulur. | — |
| R7 | Üçüncü taraf ödeyen | 1010-1016 | — | Gelirde kontrat şirketinden bağımsız `payer` alanı; gerçek ödeyene proforma kesilebilir. | Proforma ile REQ:2133'teki "faturalar kapsam dışı" ilişkisi tanımlı değil (bkz. §5). |
| R8 | Expo bazında bütçe vs gerçekleşen | 1018-1026 | — | Her expo için kategori/tip satırlı bütçe; gerçekleşen giderlerden fark sorgusu; bütçe düzenlenebilir ama değişiklik geçmişi korunur. | Gelir hedefinin yapısı tanımsız (1020'de "target revenue level" geçer, satır yapısı yalnız gider için 1022). Bütçe onayı/yetkisi tanımsız. |
| R9 | İşlem başına tek expo atfı | 1028-1034 | — | Gider/gelir ya expo'ya ya genel gidere bağlanır; cluster raporu toplam sorgusudur; çok-expo giderinde en büyük faydalanana atanır. | Bölünmüş atıf bilinçli olarak yok (1034, 2195). |
| R10 | Komisyon bir finans akışıdır | 1036-1042 · 2.3: 488-498 | — | Ödenen komisyon "Sales Costs" kategorisinde bir giderdir, kontrata bağlıdır; iptal sonrası alacak, agent bakiyesinde tutulur ve sonraki ödemeden düşülür. | LEENA'daki ayrı payout tablosuyla ilişki (bkz. §3, §5). |
| R11 | İade ve kredi bakiyesi akış olarak | 1044-1052 · 1.5: 151 | — · [FACT] | İade gerçek bir çıkıştır, ilk alan hesaptan ve kaynak gelire bağlı; kredi bakiyesi saklanmaz, olaylardan türetilir; şirket krediyi tercih eder. | — |
| R12 | Hesap ekstreleri ve nakit akışı | 1054-1060 | — | Her hesap tek sıralı hareket akışı olarak okunur (yürüyen bakiyeyle); hesaplar arası toplam nakit, alacak, ödenecek komisyon, cari bakiye tek tıkla. | — |
| R13 | Bakiyeler türetilir, saklanmaz | 3.3: 1543-1547 | [PRINCIPLE] | Hesap bakiyesi, kredi bakiyesi, açık tutarlar ve komisyon düzeltmeleri hep işlem toplamıdır; bakiye kolonu yok. | — |
| R14 | Açılış bakiyesi yok, tam tarihçe | 940 · 1082 | — | Zoho tarihçesi tümüyle aktarılır; açılış bakiyesi alanı tutulmaz. | Transferlerin "yeniden kurulabildiği ölçüde" aktarımı (1082) — ölçüt yok. |
| R15 | Finans raporları | 2.8: 1252, 1317 · 2.5: 860-866 | — | Expo başına gelir/gider/marj, bütçe-gerçekleşen, hesap bakiyeleri, açık alacak, ödenecek komisyon; açık ödemeler Owner'ın günlük üç görünümünden biri. | — |
| R16 | Yetki satırları | 3.1: 1387, 1388, 1423 · 3.4: 1581 | [PRINCIPLE] | "Finance" profili finans modüllerini tam görür; "Admin" hesap listesi ve gider kategorisi yönetir; iade onayı varsayılan Owner. | Gider girme/onaylama yetkisi ayrıca tanımlı değil. |
| R17 | Finansal işlemlerin denetimi | 3.6: 1728 | — | İade onayları, komisyon düzeltmeleri, hesaplar arası transferler ve kur düzeltmeleri denetim kaydına girer. | "Kur düzeltmesi" ile R4'ün "kur asla değişmez" kuralının ilişkisi tanımsız (bkz. §5). |
| R18 | Finansal referans verisi | 3.5: 1656-1662, 1697 | — | Ödeme yöntemleri, gider kategori/tipleri, gelir kategorileri, hesaplar referans veridir; açılışta Zoho'dan tohumlanır. | — |
| R19 | Entegrasyonlar | 3.9: 1906, 1915-1921, 1923-1934 | — | Online tahsilat, muhasebe dışa aktarımı, e-fatura — hepsi sonraki faz. | Muhasebecinin ihtiyacı belgelenmemiş (1921). |
| R20 | Kapsam dışı / gelecek | 5.x: 2133, 2139, 2191, 2195 | — | Fatura/satın alma emri, Zoho forecast modülü, kur farkı kaydı, bölünmüş atıf: kapsam dışı ya da sonra. | — |
| R21 | Operasyon gerçekleri | 1.5: 135, 137, 139 | [FACT] | Para birimleri karışık; elden nakit tahsilat bankaya yatırılır; merkez ↔ ofis sübvansiyon ve geri gönderim iki yönlü. | — |

**Zoho'daki mevcut davranış tarif edilen satırlar:** 946 (transferde yalnız alan taraf
kaydediliyor) · 962 (sahibin ödemeleri kayda geçmiyor) · 1002 (taksitler tutarsız
kaydediliyor) · 1058 (raporlar hesap değil modül eksenli) · 516-518 (Zoho'daki elle tutulan
muhasebe alanları anti-örüntü) · 1917 (muhasebeci Zoho'dan veri çekmiyor) · 1697 (Zoho
referans sayıları: 6 kategori / 75 tip / 15 gelir kategorisi) · 125 [FACT] (~731 görünür
tahsilat kaydı) · 2211 (kaynak: ZOHO_USAGE_REFERENCE).

**Sayım:** 21 gereksinim maddesi (R1–R21).

---

## 2. Diğer belgelerdeki kararlar

| Kaynak | Tarih | Özet |
|---|---|---|
| `ELL_YOL_HARITASI_v5.md:19, :22` | 2026-06-19 kararı (dosya 2026-07-27) | Ledger dahil finans çekirdeği LEENA DB'de kurulur. |
| `ELL_YOL_HARITASI_v5.md:262-273` | aynı | Faz 3b kapsamı: hesaplar (banka/kasa/sanal), iki taraflı işlemler + transferler, işlem bazlı donmuş kur, akıştan bakiye, sahibin cari hesabı, bütçe, iade/kredi, iki seviyeli gider alt sistemi; "en ağır" iş. |
| `ELL_BILGI_MIMARISI_v3.md:60, :83, :86, :178, :180` | dosya 2026-07-29 | Gelir, gider, ledger, hesaplar ve expo P&L / bütçe-gerçekleşen LEENA DB'de, Finance sekmesinde; hepsi 🔴 (yok). |
| `ELL_TEK_KAYNAK_KILIT.md:44, :46, :55, :56` | kilit 2026-06-20 | Ödeme/gelir/gider ve ledger/hesaplar tek kaynağı LEENA Finance; para birimi listesi LEENA master; kur listesi master ama işlemde donar. (`decisions/` altındaki kopya birebir aynı.) |
| `ELL_GLOSSARY.md:310` | dosya 2026-07-29 | "account" terimi Zoho'nun Company karşılığı olarak işaretli (bkz. §5). |
| Defter `:156-169` (#1 `:157`, #2 `:158`, #3 `:159-160`, #5 `:163`, #7 `:168-169`) | 2026-07-22 (3a-2 KİLİTLİ) | Ödeme yöntemi 5 değer; `account_id` + `payer` ledger fazına ertelendi; ödemeler değiştirilemez olay, düzeltme ledger fazının işi; para birimi listesi yalnız arayüzde; `payments` = gelir kaydının kontrata bağlı minimal öncüsü, ledger'da iki evrim yolu açık. |
| Defter `:638-650` | 2026-07-27 | Payout modeli cari hesap; bakiye her okumada türetilir; dönem kolonu eklenmeyecek. |
| Defter `:1679-1680` | 2026-09-09 | ui2 kapsama ölçümü: Expo Finance 0/8, Ledger 0/10 — kaynak endpoint yok. |
| Defter `:2190, :2204` | 2026-10-08 | Canlı DB'de ledger tablosu 0; sıra: Faz 4 dilim 2 → LEDGER → katalog/quote. |
| Kütük ODE-01..03 (`:129-131`) | 2026-07-27 | Payout cari hesap; fazla ödeme negatife düşer ve mahsuplaşır; payout değiştirilemez, düzeltme ters kayıtla. |
| Kütük TAH-01..04 (`:122-125`) | 2026-07-28 | Ters kayıt/transfer satırında ofis/yöntem orijinalden; tek ödeme formu; ödeme↔vade kalemi eşleştirme mantığı bilinçli yok. |
| Kütük PLN-04, PLN-09, PLN-10 (`:138, :143, :144`) | 2026-07-28 / 07-30 | Vade planında kur dondurulmaz; nakit öngörüde plan kontratın kendi kuruyla çevrilir; tahsilat satır seviyesinde düşülür. |
| Kütük OFS-01..06 (`:149-154`) | 2026-07-28 | Ofis listesi koda gömülmez; ofis × para birimi × yöntem tablosu kurulmaz; ofis zorunluluğu API katmanında. |
| Kütük SEM-01, SEM-02 (`:158-159`) | 2026-07-28 | Ödeme / payout / plan yöntemleri tek sözlük (5 değer); `CURRENCIES` tek yerde tanımlanır, kopyalar borçtur. |
| Kütük SEM-06 (`:163`) | 2026-10-08 | Kontrat statüsü `Transferred` tektir, yön `transferred_from_contract_id` ile. |
| Kütük RAP-01..03 (`:171-173`) | 2026-07-29 | Raporlama EUR'da, girişteki kilitli kurdan; dışlanan hiçbir şey sessizce kaybolmaz; dışlama kara listedir. |
| Kütük YON-07 (`:183`) | 2026-09-13 | Tasarım kararları çok kiracılı SaaS hassasiyetinde tartılır. |
| `decisions/ADR-011-payment-authority.md:25-57` | 2026-06-01 (DECIDED) | Ödeme girme/düzenleme/silme yetkisi rol bazlı; yerel ofisler yalnız kısıtlı formla girer, düzenleyemez, silemez, yalnız kendi ülkesini görür. |
| `decisions/ADR-012-historical-migration-scope.md:27-46` | 2026-06-01 (DECIDED) | 2014'ten itibaren tam tarihçe aktarılır; mali yıl ≠ expo edisyonu; yerel para birimli ödemeler orijinal tutar + Zoho kuru + EUR ile aktarılır; aktarım sağlama toplamıyla doğrulanır. |
| `decisions/ADR-015-hierarchical-data-visibility.md:38` | 2026-06-01 | Örnek kullanıcının gelir görüp gider görmemesi — görünürlüğün gelir/gider ayrı tanımlanabildiğinin işareti. |
| `analysis/TRACK_3_4_RESULTS.md:56-57, :87, :101` | 2026-06-08 | eliza-legacy'de bir `expenses` tablosu vardı ama yazan kod yoktu; işlem bazlı donmuş kur yoktu; çok-hesaplı ledger hiçbir sistemde yoktu. |

---

## 3. LEENA'da bugün olan (main `ae3cd4f`)

**Ledger tabloları:** `migrations/` + `initial.sql` içinde `accounts`, `transfers`,
`budget(s)`, `expenses`, `revenues`, `ledger_*`, `journal*`, `transactions` için
CREATE TABLE **YOK** (grep 0). 8 Eki canlı DB ölçümüyle (defter `:2190`) uyumlu.

**Ledger kavramlarına bugün değen yapılar:**

| Yapı | Yer | Ne |
|---|---|---|
| `contracts.revenue / currency / exchange_rate / revenue_eur` | `012_finance_foundation.sql:72-75` | Kontrat tutarı, para birimi, kontrat kuru, EUR karşılığı. |
| `payments` | `017_payments.sql:35-49` (tutar, para birimi, kur, EUR: `:39-42`; yöntem: `:43`) | Kontrata bağlı tahsilat olayı. `account_id` ve `payer` bilinçli olarak yok — "ledger fazı" notu `017:21`. |
| `payments.reverses_payment_id` | `018_payment_reversal.sql:41-55` | Ters kayıt (negatif tutar). |
| `payments.schedule_item_id / received_office_id` | `026_payment_schedule.sql:96-97` | Vade kalemi bağı (eşleştirme mantığı yok, TAH-04) ve tahsil eden ofis. |
| `payment_schedule_items` | `026_payment_schedule.sql:49-81` | Vade planı: tutar kontrat para biriminde, kur yok (PLN-04); beklenen ofis/yöntem; revizyon + `superseded_at`. |
| `commission_payouts` | `025_commission_payouts.sql:36-59` (para alanları `:40-43`) · `027_payout_office_method.sql:19-27` | Agent'a ödenen komisyon: tutar, para birimi, kur, EUR, ters kayıt; ödeyen ofis + yöntem. |
| `offices` | `026_payment_schedule.sql:26-35` (+5 seed `:38-43`) | Ofis referansı (ad, ülke, aktif). Hesap/para birimi alanı yok. |
| `expos.payment_deadline*` | `010_expo_operations.sql:109, :119` | Ödeme son tarihi ofseti/override'ı (operasyonel tarih; tutar değil). |
| Kontrat liste/detay paid/balance | `routes/contracts.js:244-255` (liste), `:284-287` (detay) | Ödemelerden okuma anında türetilir. |
| Ödeme girişi / ters kayıt / transfer | `routes/contracts.js` `POST /:id/payments`, `POST /:id/payments/:paymentId/reverse`, `POST /:id/transfer` | Kontrat düzeyinde para olayları (transfer = kontrat devri, hesaplar arası para transferi DEĞİL). |
| Agent cari ekstresi | `routes/payouts.js:206` (`/api/agents/:id/statement`, mount `index.js:155`) | Earned − paid bakiyesi türetilir. |
| Komisyon listesi | `routes/commissions.js:46` (mount `index.js:154`) | Kesim dönemi komisyon raporu. |
| Nakit öngörü | `routes/cashForecast.js:175` (mount `index.js:157`) | Ofis × vade × para birimi beklenen tahsilat. |
| Ofisler | `routes/offices.js` (GET/POST/PUT; mount `index.js:156`) | Ofis yönetimi. |
| Para birimi listesi (arayüz) | `public/contract-detail.html:228`, `public/sales-agents.html:156` | Sabit 6 değer (EUR, USD, TRY, MAD, NGN, KES); iki kopya (SEM-02 borcu). |
| Finans ekranları | `public/contract-list.html`, `contract-detail.html`, `agent-statement.html`, `commissions.html`, `cash-forecast.html`, `offices.html`, `sales-agents.html`, `ui2/finance-contract(s).html` | Hiçbiri hesap, transfer, gider, bütçe göstermez. |

**RTM (`LEENA docs/audits/RTM_ENVANTER_RAW_2026-09-14.md`) ledger satırları:**
`:374-396` (A6: accounts / iki taraflı transfer / sahibin cari hesabı / bütçe / gider / gelir
tablosu → hepsi YOK; gelir yalnız kontrat kolonu olarak) · `:298` (017'deki ertelenen
`account_id`, `payer` notu) · `:599` (agent cari ekstresi VAR, `payouts.js:206`) ·
`:786-790` (ui2'de Ledger ekranı yok; yalnız `finance-contract.html`).

---

## 4. Gereksinimde boş / TBD olanlar

1. Transferin veri şekli: tek olay mı, iki bağlı işlem mi — REQ:956 açık bırakıyor.
2. Sahibin cebinden ödenen giderin kayıt mekanizması — REQ:970 açık bırakıyor.
3. **Gider onay akışı** — tanımlı değil. Onay geçen tek finans eylemi iade (REQ:96, 1423).
4. **Gider belgesi / makbuz eki** — gereksinimde hiç geçmiyor (ek/makbuz araması 0 isabet, finans bağlamında).
5. Bütçe yetkisi ve onayı (kim kurar, kim değiştirir) — tanımsız. Yalnız değişiklik geçmişi şart (REQ:1026).
6. Gelir hedefinin yapısı — REQ:1020 hedeften söz ediyor, satır yapısı yalnız gider için (REQ:1022).
7. Kur farkı kâr/zararı — yalnız yer tutucu (REQ:984, 2191).
8. Bölünmüş expo atfı — bilinçli olarak yok (REQ:1034, 2195).
9. Muhasebe dışa aktarımı — muhasebecinin ihtiyacı belgelenene kadar ertelendi (REQ:1915-1921).
10. Türkiye e-fatura / e-arşiv — sonra (REQ:1923-1934).
11. Online tahsilat — sonraki faz (REQ:1906).
12. Yerel ofisin gider girişi yetkisi — 3.1'de ayrıca yok; ADR-011 yalnız ödeme (tahsilat) için kural koyuyor.
13. Banka ekstresiyle mutabakat — geçmiyor. REQ:958'deki mutabakat iki iç hesap arasında.
14. Ledger raporlarında dönem tanımı (mali yıl / takvim yılı / expo edisyonu) — REQ'de yok. Yalnız ADR-012 #1 mali yıl ≠ edisyon diyor.
15. Transferlerin tarihsel aktarımı "yeniden kurulabildiği ölçüde" — ölçüt yok (REQ:1082).
16. Hesap türlerinin tam listesi ve "başka kişilerin cari hesabı" kapsamı — örnekle sınırlı (REQ:938, 968).
17. Belge geneli: `[TBD]` işaretleri REQ:163 ve REQ:1363'te duruyor, ancak altlarındaki bölümler dolu (bkz. §5-Ç1).

**Sayım:** 17 boş/TBD maddesi.

---

## 5. Belgeler arası çelişkiler

| # | Çelişki | Kanıt |
|---|---|---|
| Ç1 | REQ kendi künyesinde tutarsız: sürüm "1.0 (Document complete)" ama durum "In progress"; dolu bölümlerin başında `[TBD]` işareti duruyor. | REQ:9 vs REQ:11 · REQ:163, REQ:1363 |
| Ç2 | Ödeme düzenleme/silme yetkisi: ADR-011 iki rolün ödemeyi düzenleyip silebildiğini söylüyor; defter 3a-2 ve kütük ödemeleri değiştirilemez olay sayıyor (düzeltme = ters kayıt). | ADR-011:33-34 vs defter `:159-160`, kütük TAH-01 (`:122`), ODE-03 (`:131`, payout için aynı ilke) |
| Ç3 | Ödeme yöntemi sözlüğü: REQ "bank transfer, cash, SWIFT, credit balance" sayıyor; defter/kütük ve şema 5 değer kullanıyor (`bank_transfer, cash, cheque, credit_card, other`). SWIFT ve kredi bakiyesi yok; çek ve kredi kartı REQ'de yok. | REQ:1656 vs defter `:157`, kütük SEM-01 (`:158`), `017_payments.sql:43-44` |
| Ç4 | Para birimi listesi: REQ 8 para birimi sayıyor (DZD, GHS dahil, Türk lirası "TL"); defter 3a-2 arayüz listesi 6 değer (DZD, GHS yok; "TRY"). | REQ:52, REQ:1655 vs defter `:163` (3a-2 #5), `contract-detail.html:228` |
| Ç5 | "account" terimi: glossary Zoho'nun Company karşılığı diye işaretliyor; REQ §2.6/§3.3'te "account" = para hesabı (banka/kasa/sanal). | `ELL_GLOSSARY.md:310` (ve `:324`) vs REQ:934-940, 1549-1553 |
| Ç6 | Kontrat statüleri (ledger'a "transfer" terimi üzerinden değiyor): REQ ve glossary "Transferred In / Transferred Out" ayrımı yapıyor; ADR-012 bu ikisinin "aynen" aktarılmasını istiyor; kütük SEM-06 tek `Transferred` diyor. | REQ:400-404 · `ELL_GLOSSARY.md:121` · ADR-012:39 vs kütük SEM-06 (`:163`), yol haritası `:253` |
| Ç7 | Komisyon ödemesinin yeri: REQ ödenen komisyonu "Sales Costs" kategorisinde bir gider kaydı olarak tanımlıyor; LEENA'da ayrı bir `commission_payouts` tablosu ve cari hesap modeli var. Defter bunu ledger fazına bağlamamış. *(Belge ↔ kod farkı; belgeler arasında açık bir hüküm yok.)* | REQ:1038-1040 vs defter `:638-650`, kütük ODE-01 (`:129`), `025_commission_payouts.sql:36` |
| Ç8 | Kur değişmezliği ile denetimdeki "kur düzeltmesi": REQ kuru kalıcı olarak değiştirilemez sayıyor; aynı belgenin denetim maddesi "exchange rate corrections" olayını sayıyor. | REQ:976, 1527 vs REQ:1728 |
| Ç9 | Proforma ile fatura kapsamı: REQ gerçek ödeyene proforma kesilebileceğini söylüyor; aynı belge faturaları kapsam dışı sayıyor. Proforma ↔ vergi faturası ayrımı yazılı değil. | REQ:1014 vs REQ:2133 |

*Çözülmüş olarak kayda geçti (çelişki sayılmadı):* REQ:874 "ELIZA finansal veriyi tutar" der;
REQ:4-7 amendment'ı ve yol haritası `:22` bunu LEENA olarak okutur.

**Sayım:** 9 çelişki (Ç7 belge↔kod farkı olarak işaretli).

---

## 6. ÖLÇÜLMEDİ / GÖZLENEMEDİ

- Canlı ya da test DB — bağlanılmadı. LEENA bulguları yalnız koddan; canlı satır sayıları 8 Eki
  defter kaydından aktarıldı.
- Zoho'nun kendisi ve `archive/ZOHO_USAGE_REFERENCE.md` ayrıntısı okunmadı. Zoho davranışı
  yalnız REQ'deki tariflerden.
- LIFFY tarafı (quote/ürün/kur tabloları) ölçülmedi — ledger kapsamı dışında tutuldu.
- Sentez'in kendi KB'si — erişim yok, ölçülmedi.
- `ELL_MIMARI_v1.0_KONSOLIDE.md`, `HANDOVER_BRIEF.md`, `ELL_FEATURE_INSPIRATION.md` ve
  `archive/` ledger için taranmadı. Taranan: REQ, yol haritası v5, bilgi mimarisi v3, tek
  kaynak kilidi, glossary, defter, kütük, ADR-003/011/012/015, `analysis/TRACK_3_4_RESULTS.md`.
- Satır referansları ölçüm anındaki dosya hâline göredir (`5e8b193`); defter büyüdükçe satır
  numaraları kayar.
