# EKSİK ENVANTERİ — 2026-11-11 (salt okuma + belge)

> **Ne:** YON-21 (Sentez 11 Kas, Suer kuralları) İLK İŞ — REQ Part 2'nin 8 iş akışı (§2.1–2.8) + Part 3 kesişenler, madde madde ×
> durum: **ui2 VAR** · **klasik VAR** (eski LEENA ekranı, yol) · **LIFFY VAR** · **eliza-legacy VAR** · **KISMİ** (ne eksik) · **YOK**.
> Sentez'in "özellikle" listesi **★** ile işaretli. Ek bölümler: kullanım sinyali (staging) · UI KUYRUĞU · OPERATIONS TAŞIMA PLANI.
> **Kaynak (ölçüldü):** `ell-docs/ELAN_EXPO_REQUIREMENTS_v1_0.md` (repo kökü, 2.435 satır; Part 2 = 289–1488, Part 3 = 1489–2104).
> **Kod tabanı:** LEENA `eliza-next` @ `0d70d4d` (envanter bu commit'te okundu; aynı gün yapılan UI kuyruğu commit'leri §4'te ayrıca) ·
> LIFFY `liffyv1` @ `10047ee` + `liffy-ui` @ `b78231b` · eliza-legacy `eliza` @ `0608477`. **Salt okuma** — kod değişikliği yok (envanter);
> staging yalnız `claude_readonly` + `BEGIN READ ONLY` ile sayıldı. **Kişisel veri YOK** (yalnız tablo adı · satır sayısı · tarih).
> **Yöntem:** 4 bölüm paralel okundu (§2.1–2.3 · §2.4–2.5 · §2.6–2.8 · Part 3); her iddia dosya:satır; bulunamayan "BULAMADIM".
> Kilit iddialar ayrıca elle doğrulandı (gelen e-posta INSERT 0 · convert e-posta 0 · `expo_stands.contract_id` yazan uç 0 · `refund`
> yazan kod 0 · "send all" 0 · katalog yalnız kolon). **Büyüklük:** S = tek ekran/uç, şema yok ya da tek kolon, ≤1 dilim · M = 1–2 tablo +
> 2–4 ekran/uç, ~1 paket · L = yeni alt sistem (zamanlayıcı/motor, dış entegrasyon, katılımcıya açık yüz, çok rollü akış), ≥2 paket.
> Bu belge tarihseldir (YON-01): yazıldığı günün ölçümüdür.
>
> Kısaltmalar: `be` = `backend/leena-v401-backend` · `ui2/` = `be/public/ui2/` · `klasik/` = `be/public/` · `mNNN:x` =
> `be/migrations/NNN_*.sql:x` · `lv/` = `liffyv1/backend/` · `lu/` = `liffy-ui/` · `el/` = `eliza/`.

---

## 0. SUER TABLOSU (öncelik için — 60 satır, kopyalanabilir)

| # | madde | durum | nerede | S/M/L |
|---|---|---|---|---|
| 1 | ★ Kat planı editörü + stand satış durumu | klasik VAR | `klasik/floorplan-builder.html`; ui2'de öğe yok · staging 11 stand, son kayıt 21 Nis | ui2 köprüsü S · taşıma L |
| 2 | ★ Kat planı ↔ kontrat/katılımcı bağı | KISMİ | `expo_stands.contract_id` kolonu var, yazan uç yok; bağ elle girilen `expo_exhibitors`'a | M |
| 3 | ★ Katılımcı katalog formu (güvenli link + editör + gönderim kaydı) | YOK | yalnız `expos.catalogue_form_url` metni (m010:124) | L |
| 4 | ★ Stand formları / ekstra hizmet siparişi | YOK | katalogda "Extra Equipment" ürünleri var (m056:94); sipariş tablosu/formu yok | L |
| 5 | ★ Stand çizimi gönderimi + onayı | KISMİ | `contracts.stand_design_link` (yalnız Zoho göçü yazar; klasik ekranda salt okunur) | M |
| 6 | ★ 8'li operasyon e-posta zinciri (motor · fuar tetikleri · send all · tek tek yeniden gönder · durum) | YOK | altyapı var: `email_queue` + `email_worker.js` + fuar son gün kolonları (m010:104-121) | L |
| 7 | ★ Ödeme hatırlatma (katılımcıya, Finance kutusundan) | KISMİ | fuar ödeme son günü kolonu + iç tahsilat raporu R4; eliza-legacy'de yalnız iç WhatsApp taslağı | M (zincire bağlı) |
| 8 | ★ Hoş geldin e-postası (convert'te) | YOK | convert e-posta yazmıyor (`be/utils/convertCore.js`) | S (zincir altyapısıyla) |
| 9 | ★ Yaka kartı gönderimi (kontratlı firma personeli) | KISMİ | ziyaretçi/exhibitor kayıt e-postasında badge linki + toplu baskı; firma/stand kotası + kontrat bağı yok | M |
| 10 | ★ Kontrat sonrası ek sipariş (ELAN EXPO ekip primi) | YOK | REQ'de tanımlı değil (BULAMADIM); ek satış bugün yeni teklif → kontrat; `team` temsilci kaydı var (067) | ? kural tanımı gerekir |
| 11 | ★ Gelen e-posta → kontrat geçmişi | KISMİ | `be/routes/emailInbound.js` yalnız İLETİR, kayda yazmaz | L |
| 12 | Lead girişi: madencilik · CSV · elle | LIFFY VAR | `lv/routes/leads.js` · `lv/routes/lists.js` | — |
| 13 | Lead girişi: web formu · serbest çalışan · reklam · ziyaretçi → lead | KISMİ | klasik form → `visitors` + form başına bildirim | L |
| 14 | Yanıttan zenginleştirme (öneri + onay) | KISMİ | LIFFY imzadan otomatik yazar, onay ekranı yok | M |
| 15 | Lead yönlendirme kuralı + yedek kuyruk + gerekçe | KISMİ | LIFFY elle / toplu atama | L |
| 16 | Tekilleştirme (alan adı, ad varyantı, LIFFY ↔ LEENA) | KISMİ | LIFFY e-posta tekilliği | L |
| 17 | E-posta doğrulama (ZeroBounce) | LIFFY VAR | `lv/services/verificationService.js` | — |
| 18 | Eleme kategorileri + otomatik eleme ("ilgilenmiyorum", 3 bounce) | KISMİ | LIFFY Lost + sebep | M |
| 19 | Kanal atfı lead → kontrat + kaynağa göre puan | KISMİ | kaynak yalnız lead/ziyaretçide | M |
| 20 | LIFFY kişi → LEENA firma/kişi dönüşümü + geri akış | YOK | iki sistem arasında bağ yok | L |
| 21 | Teklif AF no Q{ISO} → A{ISO} | ui2 VAR | `be/routes/quotes.js:467` | — |
| 22 | Teklif alanları: konu · ödeme koşulu/yöntemi · geçerlilik ve ofis para birimi varsayılanı | KISMİ | `m058:51` | S |
| 23 | İmza: tarama dosyası yükleme + Owner/Proje bildirimi | KISMİ | yalnız tarama URL'si (isteğe bağlı) | M |
| 24 | Convert yalnız Proje'de + inceleme adımı | KISMİ | kodda convert = `sales.write` (Sales own); REQ'te yalnız Proje | M (kural kararı) |
| 25 | Huni dönüşüm raporu (lead → imza) | KISMİ | parçalar iki sistemde | M |
| 26 | Kontrat durumu · transfer · komisyon ataması · ödeme planı | klasik VAR | `klasik/contract-detail.html`; ui2 salt okuma | ui2'ye S (her biri) |
| 27 | Kontrat operasyonel alanları (stand no · m² · katalog sayfası · tasarım linki) düzenleme | KISMİ | kolonlar var (m016), yazan uç yok | S |
| 28 | Kontrat bazında komisyon ödenen/kalan + iptal düzeltmesi | KISMİ | ödeme temsilci bazında (m025) | M |
| 29 | Kontrat zaman çizelgesi (yapılan · bekleyen · sıradaki) | KISMİ | ui2 kontrat + iletişim kartı | M |
| 30 | Katalog şablonu · PDF · herkese açık web katalog | YOK | PDF/render kütüphanesi yok | L |
| 31 | Katalog son tarihi + kilit · istisna · "eksik" panosu | KISMİ | son tarih klasik VAR; kilit/pano YOK | M |
| 32 | Fuar ana kaydı · operasyon son tarihleri · yeni edisyon klonu | klasik VAR | `klasik/expo-form.html` · `be/routes/expos.js` | ui2'ye M |
| 33 | Cluster: kayıt VAR · otomatik tespit (eliza-legacy) · cluster toplamları YOK | KISMİ | `klasik/expo-clusters.html` · `el/packages/targets` | M |
| 34 | Partner kaydı + Welcome'a dinamik girmesi | KISMİ | kayıt klasik VAR (`expo-partners.html`); e-posta bağı YOK | M |
| 35 | Ziyaretçi · check-in · lead scanner · sertifika | klasik VAR | yoğun kullanım: visitors 112.868 · checkins 46.233 | taşıma §5 |
| 36 | Katılımcı listesi = kontratlar (kat planı · yaka kartı · lead scanner bağı) | KISMİ | yalnız ui2 R3 firma listesi | M |
| 37 | Fuar sonrası rapor + çok fuarlı Proje panosu | KISMİ | R3 + klasik ziyaretçi raporu | L |
| 38 | B2B eşleştirme · ziyaretçi portalı · push · ısı haritası | YOK | — | L (yol haritası) |
| 39 | Hesaplar · transfer · owner cari · ekstre · gider · bütçe | ui2 VAR | `ui2/finance-*.html` | — |
| 40 | Ödeme girişi · ters kayıt · plan ui2'de | klasik VAR | yalnız `klasik/contract-detail.html` | S |
| 41 | Kontratsız gelir (sponsorluk) + gelir kategorisi | KISMİ | `payments.contract_id NOT NULL` (m017:38) | M |
| 42 | İade / kredi akışı | KISMİ | ledger `refund` türü tanımlı, yazan kod YOK | M |
| 43 | Komisyon ödemesi = kontrata bağlı gider + bütçeye girer | KISMİ | temsilci carisi (m025) | M |
| 44 | Üçüncü taraf ödeyen + proforma | KISMİ | `payments.payer` serbest metin; proforma YOK | M |
| 45 | Ödeme yöntemi referans tablosu · ödemede kaydı giren | KISMİ | 5 sabit yöntem; `payments.created_by` NULL | S |
| 46 | Operasyon / pazarlama şablon ayrımı + abonelikten çıkma | KISMİ | liste var; şablonda sınıf bayrağı yok; LEENA + LIFFY iki liste | M |
| 47 | 3 dilli tek şablon (8 operasyon şablonu) + dil seçimi | KISMİ | ui2'de yalnız teklif e-postası şablonu | M |
| 48 | Gönderen kutusu (Project / Finance) şablon başına | KISMİ | tek gönderen adresi | M |
| 49 | Kanıt değerinde e-posta geçmişi (sürüm · içerik · cc · izleme) | KISMİ | gönderilmiş kampanya satırları siliniyor (G13); cc yok | M |
| 50 | Pazarlama kampanyası (liste · şablon · adım · günlük limit) | LIFFY VAR | + klasik `email-campaigns.html` | — |
| 51 | Owner ana sayfa · rapor oluşturucu · doğal dil · zamanlanmış e-posta rapor | ui2 VAR | `ui2/owner-home.html` · `ui2/finance-reports.html` | — |
| 52 | Rol panoları (Proje Lideri, takım lideri) | KISMİ | yalnız Owner + Sales home | M |
| 53 | AI içgörü + iç WhatsApp | eliza-legacy VAR | LEENA'da YOK (Zoho aynasını okur) | L |
| 54 | Kişi başı yetki matrisi + yetki denetimi | ui2 VAR | `be/utils/permissions.js` · `ui2/admin-user.html` | — |
| 55 | Özel şablon · şablon anlık görüntüsü · eksik profiller | KISMİ | 6 şablon; özel şablon ucu yok | M |
| 56 | `reports_to` hiyerarşisi (team kapsamı) | LIFFY VAR | LEENA'da team = kişinin kendisi | M |
| 57 | Kayıt düzeyinde kapsam ekleme/dışlama + "neden görüyorum" | KISMİ | tek ofis kapsamı | L |
| 58 | Denetim ekranı · 24 ay saklama · eksik denetim yazımı (kontrat durum, ödeme, temsilci) | KISMİ | `audit_log` var, genel ekran yok | M |
| 59 | Genel arama: gider/ödeme/temsilci grupları + kabukta kutu · kayıtlar arası bağlantı | KISMİ | 5 grup, Sales menüsünde | S |
| 60 | Bildirim merkezi (zil) + kişi tercihi · portföy devri · kur tablosu | YOK | — | L / M / M |

---

## 1. TAM ENVANTER — §2.1 Lead Acquisition & Distribution (REQ 293–401)

| # | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|
| 1.1 | 307, 311, 319 | Madencilik, Excel/CSV içe aktarma, elle lead | LIFFY VAR | `lv/routes/leads.js:138` · `lv/routes/lists.js:402, 1228` | ui2'de lead ekranı yok | — | — |
| 1.2 | 309–317, 360–361 | Web formu, serbest çalışan formu, reklam, ziyaretçi → lead | KISMİ | `be/routes/visitors.js:256-270, 456-489` | klasik form + form başına bildirim var; lead kaydı, ülke → ofis ataması, serbest çalışan formu, reklam girişi, ziyaretçi → lead yok | L | 1.8 |
| 1.3 | 331–332, 390 | İmzadan ayrıştırma, tek tıkla zenginleştirme | KISMİ | `lv/utils/signatureParser.js:200-290` · `lv/routes/webhooks.js:843` | LIFFY otomatik yazar (yalnız boş alan); öneri + onay ekranı yok; LEENA'ya akmaz | M | 1.17 |
| 1.4 | 333 | Teklif/kontrat bilgisi lead'e geri akar | YOK | `be/routes/quotes.js:226-233` · `m057:29-46` | LEENA firma ↔ LIFFY persons bağı yok | M | 2.6 |
| 1.5 | 334 | "İlgilenmiyorum" → otomatik durum | YOK | `lv/routes/webhooks.js:734, 759` | her yanıt "Interested"e gider | M | 1.3 |
| 1.6 | 342–346, 392 | Kategorili, geri alınabilir, otomatik eleme | KISMİ | `lv/routes/pipeline.js:22-25` · `lv/routes/campaigns.js:578` | Lost kişi kampanyadan dışlanmıyor; 3 hard bounce bayrağı yok | M | 1.5 |
| 1.7 | 348–354 | Kampanya atfı; firmaya fuar adaylığı | KISMİ | `lv/migrations/005…:3` · `m060:47` | sektör × ülke → fuar adayı yok | M | 2.6 |
| 1.8 | 366–371, 394 | Kanal kuralı, elle/toplu atama, yedek kuyruk, gerekçe | KISMİ | `lv/routes/persons.js:737, 848` · `lv/engines/action-engine/actionEngine.js:66` | kural motoru, izlenen kuyruk, gerekçe kaydı yok | L | 1.2 |
| 1.9 | 375–380, 398 | Girişte tekilleştirme (e-posta, ad+ülke, alan adı, varyant) | KISMİ | `lv/migrations/015…:28` · `m057:47` | alan adı + varyant eşleşmesi, LIFFY ↔ LEENA tekilleştirme yok | L | 2.6 |
| 1.10 | 382 | ZeroBounce doğrulama, gönderim öncesi süzme | LIFFY VAR | `lv/services/verificationService.js:50` · `lv/routes/campaigns.js:476-496` | LEENA'da karşılığı yok | — | — |
| 1.11 | 386, 394 | Web formu lead'i için 1 haftalık SLA görünürlüğü | KISMİ | `lv/engines/action-engine/actionEngine.js:4-5` · `ui2/sales-home.html:25` | eskime uyarısı + yönetici yanıt hızı görünümü yok | M | 1.2, 1.8 |
| 1.12 | 379, 396 | Kanal atfı imzalı kontrata kadar | KISMİ | `lv/migrations/016…:26` · `be/routes/visitors.js:264-270` | LEENA companies/quotes/contracts'ta kaynak kolonu yok | M | 1.4 |
| 1.13 | 400 | Kaynağa göre puanlama | KISMİ | `lv/engines/action-engine/actionEngine.js:15-18` | etkileşim puanı var, kanal ağırlığı yok | M | 1.12 |

**Kullanım sinyali:** lead verisi LIFFY DB'sinde (LEENA staging'de yok). LIFFY sayımı yalnız tarihsel: `docs/audits/LIFFY_ENVANTER_2026-11-05.md`
(persons 80.855 · prospects 26.123 · mining_results 65.065 — 5 Kas, bu turda yeniden ölçülmedi).

## 1. TAM ENVANTER — §2.2 Sales Cycle (REQ 402–513)

| # | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|
| 2.1 | 410–422 | Huni aşamaları + aşamalar arası dönüşüm raporu | KISMİ | `be/routes/analytics.js:370-389` · `lv/routes/campaigns.js:1068` | Lead → Signed dönüşüm raporu yok | M | 2.6, 1.12 |
| 2.2 | 426 | Fuar başına segmentli kampanya | LIFFY VAR | `lv/routes/lists.js:849` · `lv/migrations/035…:10` | WhatsApp/SMS gelecek | — | — |
| 2.3 | 428, 506 | Niyet sınıfı, güven puanı, "nitelikli" kapısı | KISMİ | `lv/migrations/017…:23-38` · `lv/routes/webhooks.js:317-347` | yalnız 'reply' yazılıyor; kapı yok | M | 1.5 |
| 2.4 | 430, 504 | Yanıttan Kişi + Firma önerisi, tek tık onay | YOK | `be/routes/customers.js:5-7` | LIFFY persons → LEENA companies/contacts yok | L | 1.3 |
| 2.5 | 436, 500 | Teklif konusu otomatik, elle düzeltme ayrı saklanır | KISMİ | `lv/routes/quotes.js:546` · `m058:51-71` | LEENA teklifinde konu kolonu yok | S | — |
| 2.6 | 438–442, 502 | AF numarası Q{ISO}-dizi → A{ISO}-dizi | ui2 VAR | `be/routes/quotes.js:467-472, 140` · `m058:80` | DZ/GH ofis olarak eklenmeli (`be/routes/offices.js:52`) | — | — |
| 2.7 | 444–452 | Teklif: müşteri, ödeme koşulu, kalemler, toplam, geçerlilik | KISMİ | `m058:94-116` · `be/routes/quotes.js:270-274` | ödeme koşulu/yöntemi alanı + geçerlilik varsayılanı yok | S | — |
| 2.8 | 446, 450, 512 | Para birimi ofis varsayılanı, sonra değişmez, EUR karşılığı | KISMİ | `be/routes/quotes.js:256, 523, 142-146` | varsayılan hep EUR (LIFFY'de ofis varsayılanı var) | S | — |
| 2.9 | 456–458 | İmza: tarama yükleme zorunlu, tarih, bildirim | KISMİ | `be/routes/quotes.js:776-790` · `ui2/sales-quote.html:118` | yalnız isteğe bağlı URL; bildirim yok | M | 2.10 |
| 2.10 | 464–482, 508 | Convert yalnız Proje'de; inceleme kuyruğu | KISMİ | `be/routes/quotes.js:90, 797-808` · `ui2/sales-convert-queue.html:102` | kod: convert `sales.write` (Sales own; m057:100-106) — REQ'in tersi; kütükte bunu bağlayan açık hüküm BULAMADIM (KAT-04 / YET-10 convert'ü kuyruğa bağlar) → Sentez notu | M | — |
| 2.11 | 475–480 | Convert alanları kopyalar, otomasyon tetiklenir | KISMİ | `be/utils/convertCore.js:160-215` | konu + kişi kontrata taşınmıyor; e-posta zinciri tetiklenmiyor | S | 2.5, 6.16 |
| 2.12 | 486–496, 510 | Gizlilik sınırı alan düzeyinde, kişi başı | KISMİ | `be/routes/contracts.js:644-646` · `m044:100-114` | komisyon gizleme var (YET-23); iade geçmişi / iptal sebebi / proje notu alanları yok | S | — |

**Kullanım sinyali (staging = canlı 10 Kas kopyası):** quotes 0 · quote_line_items 0 · convert_requests 0 · companies 0 · contacts 0 ·
follow_ups 0 · communications 0 — ui2 Sales canlıda henüz kullanılmıyor (kesim öncesi; LIFFY teklifleri LIFFY DB'sinde).

## 1. TAM ENVANTER — §2.3 Sales Contract Management (REQ 514–699)

| # | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|
| 3.1 | 524–536, 686 | Durum yaşam döngüsü; yalnız Proje değiştirir | klasik VAR | `be/routes/contracts.js:126, 671-708` · `klasik/contract-detail.html:956-973` · `m062:39` | geçiş matrisi yok; durum değişimi audit'e yazılmıyor; ui2 salt okuma | ui2'ye S | — |
| 3.2 | 540–544, 686 | Tek düğmeyle transfer | klasik VAR | `be/routes/contracts.js:1114-1270` · `m019:39-45` | firma, kalemler, tüzel kişi taşınmıyor; transfer sebebi saklanmıyor; ui2'de düğme yok | S | — |
| 3.3 | 550–558 | Convert'te teklif alanları kontrata | KISMİ | `be/utils/convertCore.js:180-186` | kontratta konu, Sales Type, kişi kolonu yok | S | 2.5 |
| 3.4 | 560–575, 653–665 | Stand, m², katalog sayfası, tasarım/tarama linki | KISMİ | `m016:20-29` · `be/scripts/zoho/lib/apply.js:126-127` | kolonlar var, düzenleme ucu/ekranı yok | S | — |
| 3.5 | 579–607, 688 | Agent / SR / SD üç katman, kontrat bazında oran | klasik VAR | `m020:49, 59-74` · `be/routes/contracts.js:1300` | atama klasik ekranda; ui2 okuma | ui2'ye S | — |
| 3.6 | 609–616 | Kontrat bazında komisyon: hak ediş, ödenen, kalan | KISMİ | `be/routes/payouts.js:260` · `m025:36-48` | ödeme temsilci bazında; kontrata dağıtım yok | M | — |
| 3.7 | 618–626, 694 | İptalde komisyon düzeltmesi, mahsup, zarar yazma | KISMİ | `m025:17-18` · `be/routes/commissions.js:17-19` | düzeltme kaydı + zarar yazma yok | M | 3.6, 6.14 |
| 3.8 | 643–651, 690 | Zoho muhasebe alanları yok; hesaplanır | ui2 VAR | `m026:13-14` · `be/routes/analytics.js:174-185` | — | — | — |
| 3.9 | 628–641, 692 | Ödeme planı ↔ gerçek tahsilat | klasik VAR | `m026:49-60, 96` · `be/routes/contracts.js:1455, 1496, 1619` | ui2 kontratta plan yok | ui2'ye S | — |
| 3.10 | 667–682, 696 | Fuar bazında ayarlı e-posta zinciri | KISMİ | `m010:104-121` · `m061:57-58` | son tarih ofsetleri var; kontrat olayına bağlı motor yok | L | 6.16 |
| 3.11 | 665, 698 | Uzun soluklu kontrat görünümü | KISMİ | `ui2/finance-contract.html:85-91` · `ui2/sales-ui.js:32` | kontrol listesi / zaman çizelgesi yok | M | 3.4, 3.10 |

**Kullanım sinyali:** contracts 3.950 (son 2026-11-09) · contract_line_items 7.854 · payments 2.361 · commission_payouts 187 ·
payment_schedule_items 14 (son 2026-07-29). Not: göç satırlarında `created_at` = göç zamanı, iş tarihi değil.

## 1. TAM ENVANTER — §2.4 Catalogue Production (REQ 700–795)

| # | ★ | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|---|
| 4.1 | ★ | 736–751, 784 | Katılımcı katalog formu (web editörü) | YOK | `m010:124` (elle `catalogue_form_url`) · `be/routes/forms.js:217-235` (form → yalnız `visitors`) | logo, açıklama, marka, ürün görseli için tablo/uç/ekran yok | L | 4.2, 5.17 |
| 4.2 | ★ | 742; §2.5 840 | Kontrat imzasında güvenli linkli katalog e-postası | YOK | `be/utils/convertCore.js:182-207` · `reactivation_tokens` deseni | token + link + tetik yok | M | 6.16, 4.1 |
| 4.3 | | 776, 794 | `catalogue_submission` + düzenleme geçmişi | YOK | `m045:23` (genel `audit_log` var) | gönderim tablosu + sürüm yok | M | 4.1 |
| 4.4 | | 745–746, 784 | Proje incelemesi: yorumla geri gönder / onayla | YOK | BULAMADIM | onay durumu, yorum, bildirim yok | M | 4.1, 4.3 |
| 4.5 | | 727–734, 773–782 | 3–4 şablon + fuara göre özelleştirme | YOK | `m010:86-126` | şablon motoru yok | L | 4.6 |
| 4.6 | | 757, 778, 790 | Tek tıkla baskı PDF'i | YOK | `be/package.json:29` (PDF kütüphanesi yok) | render, bleed, arşiv yok | L | 4.3, 4.5 |
| 4.7 | | 759, 786, 792 | Herkese açık web katalog | YOK | BULAMADIM | — | L | 4.3, 4.5 |
| 4.8 | | 719–725 | Fuar + kontratlı katılımcı (stand no) + gönderim birleşimi | KISMİ | `be/routes/analytics.js:294-301` · `m016:23` · `m001:106` | stand no ↔ kontrat bağı ve gönderim verisi yok | M | 5.15, 4.3 |
| 4.9 | | 765, 775, 788 | Katalog son tarihi fuar kaydında | klasik VAR | `m010:107, 117` · `be/routes/expos.js:130` · `klasik/expo-form.html:246` | ui2'de görünmüyor | — | — |
| 4.10 | | 748–749, 767, 788 | Son tarih kilidi, istisna, hatırlatma, "eksik" panosu | YOK | BULAMADIM | — | M | 4.1, 4.3, 6.16 |

**Kullanım sinyali:** katalog tablosu yok. `expos` 214 satır (son 2026-11-10 — çoğu Zoho göçü 4 Kas).

## 1. TAM ENVANTER — §2.5 Expo Operations Management (REQ 796–1051)

| # | ★ | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|---|
| 5.1 | | 806–815 | Fuar ana kaydı (ad, edisyon, sektör, mekân, tarih) | klasik VAR | `m010:87-101, 131` · `be/routes/expos.js:190-200` · `klasik/expo-form.html` | ui2'de yalnız liste + Sales/Visitors sekmesi | ui2'ye M | — |
| 5.2 | | 817–829 | Kurulum/söküm, açık saatler, 4 operasyon son tarihi | klasik VAR | `m010:98, 104-121` · `be/routes/expos.js:127-134` | ui2 ekranı yok | — | — |
| 5.3 | | 831–834 | Operasyon ekibi irtibatı (HQ, saha) → users | KISMİ | `m010:28-29, 147` · `be/routes/partners.js:16-19` | users'a FK değil, serbest metin | S | — |
| 5.4 | | 836–840 | Fuara göre form URL'lerinin otomatik üretimi | KISMİ | `m010:124-126` · `be/routes/expos.js:471` | elle girilen Zoho Forms linki | S | 4.1, 5.12 |
| 5.5 | | 844, 911 | Yeni edisyon klonu (sektör, partner, kat planı) | klasik VAR | `be/routes/expos.js:484-541` · `be/routes/floorplan.js:326` | — | — | — |
| 5.6 | | 846–865 | Cluster kaydı, bağlama/çözme | klasik VAR | `m010:72-80, 101` · `be/routes/clusters.js:17, 91` | ui2'de yok | — | — |
| 5.7 | | 854, 1050 | Cluster otomatik tespiti | eliza-legacy VAR | `el/packages/targets/index.js:184-215` | LEENA'da yalnız elle | S | 5.6 |
| 5.8 | | 862, 1028, 1032 | Cluster düzeyinde toplamlar | YOK | `analytics.js` / `metrics.js`'te "cluster" 0 | — | M | 5.6 |
| 5.9 | | 869–899, 1038 | Partner kaydı (rol, birincil), kardeş fuara kopya | klasik VAR | `m010:140-155` · `be/routes/partners.js:24, 77` · `klasik/expo-partners.html:93` | "X yüklenicisini kullanan fuarlar" sorgusu yok; ui2'de yok | çapraz sorgu S | — |
| 5.10 | | 888–897, 1040 | Partner bilgisinin e-postaya dinamik girmesi | YOK | `be/utils/email.js:12` (yalnız ziyaretçi verisi) | `expo.partners.*` değişkeni yok | M | 6.16 |
| 5.11 | ★ | 901–913 | Kat planı editörü: ızgara, stand, böl/birleştir, sürüm, arka plan | klasik VAR | `klasik/floorplan-builder.html:11` · `klasik/floorplan/grid.js:801, 898-942` · `be/routes/floorplan.js:271` | arka plan görseli yalnız tarayıcı localStorage'ında (grid.js:940-942) | — | — |
| 5.12 | ★ | 901, 1036 | Kat planı: EKRAN | klasik VAR | `klasik/floorplan-builder.html` (Konva) · `ui2/nav.json` (Operations'ta yalnız Expos) | ui2'de öğe/sekme/köprü yok | köprü S · taşıma L | 5.13 |
| 5.13 | ★ | 804, 901 | Kat planı: API | klasik VAR | `be/index.js:193-194` · `be/routes/floorplan.js` (16 uç) · `be/routes/exhibitors.js:16-72` | yalnız organizer `authMiddleware`; ui2 izin kodu yok (`operations.read` "Menu only") | — | — |
| 5.14 | ★ | 907 | Kat planı: stand satış durumu | klasik VAR | `m001:89-94` · `be/routes/floorplan.js:715-746` (5 durum) · `klasik/floorplan/stands.js:260-268` | elle değişir, kontrat olaylarıyla senkron değil | — | 5.15 |
| 5.15 | ★ | 907, 1013 | Kat planı: stand ↔ kontrat/katılımcı bağı | KISMİ | `m001:104-106` (`contract_id` / `company_id` var, uç yazmıyor — `floorplan.js:641`) · `m003:29` · `m001:156` (`expo_stand_assignments` kullanılmıyor) | bağ elle girilen katılımcıya; sürüm klonu `exhibitor_id`'yi kopyalamıyor (`floorplan.js:371-376`) | M | `contracts` |
| 5.16 | | 915–917 | Satış ekibi için kat planı şablonları | YOK | BULAMADIM | — | M | 5.11 |
| 5.17 | | 919–921, 1042 | Kontrat → stand önerisi, Proje onayı | YOK | `be/utils/convertCore.js:182-207` | iptalde stand serbest bırakılmıyor | M | 5.15 |
| 5.18 | | 923–925 | Markalı kat planı PDF'i | YOK | `klasik/floorplan/grid.js:801-834` (istemcide PNG) | — | M | 4.6 |
| 5.19 | | 861 | Cluster ortak salon görünümü | YOK | `m001:23` (salon tek fuara ait) | — | M | 5.6, 5.11 |
| 5.20 | ★ | 825–826, 838, 995, 1031, 1044 | Stand çizimi gönderimi ve onayı | KISMİ | `m016:22` (`stand_design_link`, yalnız Zoho göçü yazar: `apply.js:127`) · `klasik/contract-detail.html:594` · `m010:118, 125` | gönderim/onay durumu, onay oranı, gecikme bildirimi, ui2 alanı yok | M (katılımcı linki açılırsa L) | 4.2 |
| 5.21 | ★ | 944, 951, 1013 | Yaka kartı gönderimi (katılımcı personeli + mobil) | KISMİ | `be/routes/visitors.js:405-423` · `klasik/badge-print.html` · `klasik/bulk-badge-print.html:186-197` | firma başına "Badge" e-postası, kota, kontrat bağı yok; `visitors.booth_number` serbest metin | M | 6.16, 5.27 |
| 5.22 | ★ | §2.3:680 · §2.7:1242 | Stand formları / ekstra hizmet siparişi | YOK | `m056:94` (katalogda ürün) · `be/utils/convertCore.js:207` · `m034:21-34` (kalemler değişmez) | sipariş formu + tablo yok; ek satış yalnız yeni teklif → kontrat | L | 4.2 |
| 5.23 | ★ | BULAMADIM | Ek siparişte ELAN EXPO ekip primi | YOK | REQ'de bonus/prim tanımı yok; kodda "bonus/prim" 0; komisyon yalnız temsilci/acente (`be/scripts/zoho/lib/fields.js:36`); `team` kaydı (m067) | kural tanımı gerekir | ? | 5.22 |
| 5.24 | | 927–938 | Ziyaretçi yönetimi (kayıt, QR, içe aktarma, reaktivasyon, sertifika) | klasik VAR | `be/routes/visitors.js:225, 646` · `be/routes/reactivation.js:494` · `be/routes/conferenceCertificates.js:566` | ui2'de yalnız rapora köprü + dışa aktarım | taşıma §5 | — |
| 5.25 | | 942–947 | B2B eşleştirme, ziyaretçi portalı, randevu | YOK | BULAMADIM | — | L | 4.1 |
| 5.26 | | 951–964 | Check-in: çok terminal, e-posta arama, pano, lead scanner, yerinde kayıt | klasik VAR | `be/routes/terminalCheckins.js:97, 218, 277` · `be/routes/reports.js:189-236` | `lead-scan.html:185` EXPO_ID sabit; lead yetkisi kontrattan değil | — | — |
| 5.27 | | 1008–1015 | Katılımcı listesi = iptal edilmemiş kontratlar | KISMİ | `be/routes/analytics.js:294-301` · `m003:6` · `be/routes/leads.js:26-41` | kat planı, yaka kartı, lead scanner kontrattan beslenmiyor | M | — |
| 5.28 | | 962–963 | Push bildirim, ziyaretçi ısı haritası | YOK | BULAMADIM | — | L / M | 5.11 |
| 5.29 | | 966–997, 1046 | Kendiliğinden fuar sonrası rapor | KISMİ | `be/routes/reports.js:11, 668` · `be/routes/analytics.js:252` · `be/routes/ledger.js:942` | katalog tamamlanma, doluluk, yüklenici kullanımı, e-posta etkinliği yok | M | 4.3, 5.20, 5.15 |
| 5.30 | | 1027–1048 | Tek fuar sayfası + çok fuarlı Proje ana sayfası | KISMİ | `ui2/operations-expos.html:34, 44-48` · `be/routes/analytics.js:333-358` | durum göstergeleri, geri sayım, cluster gruplama yok | L | 4.3, 5.20, 5.6 |

**Kullanım sinyali (staging = canlı 10 Kas kopyası):** kat planı `expo_halls` 6 · `expo_floorplan_versions` 8 · `expo_stands` 11 ·
`expo_stand_cells` 932 — **hepsinin son kaydı 2026-04-21** (Nisan'dan beri yeni kat planı yok) · `expo_exhibitors` 1 (2026-04-21) ·
eski `exhibitors` 0 · `expo_clusters` 1 · `expo_partners` 324 (Zoho göçü) · `visitors` 112.868 (10 Ağu sonrası 53.682; son 2026-11-09) ·
`checkins` 46.233 (son 2026-10-15) · `terminals` 52 · `badge_templates` 7 (son 2026-08-19) · `conference_certificates` 931 (son 2026-10-12) ·
`exhibitor_leads` 1 (2026-02-11).

## 1. TAM ENVANTER — §2.6 Financial Operations (REQ 1052–1213)

| # | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|
| 6.1 | 1062–1068, 1208 | Düzenlenebilir hesap listesi; bakiye türetilir | ui2 VAR | `be/routes/ledger.js:286, 257-266` · `ui2/finance-accounts.html:58` | açılış bakiyesi kolonu bilinçle yok (m036:16) | — | — |
| 6.2 | 1070–1086, 1192 | Her hareket iki taraflı transfer | ui2 VAR | `m039:39` · `be/routes/ledger.js:439, 527` | — | — | — |
| 6.3 | 1088–1098, 1194 | Owner cari hesabı | ui2 VAR | `ui2/finance-accounts.html:55, 118` · `be/utils/ledger.js:200` · `be/routes/ledger.js:1114` | "Owner cash" ödeme yöntemi yok | — | — |
| 6.4 | 1182–1188, 1196 | Ekstre (yürüyen bakiye) + çapraz özet | ui2 VAR | `be/routes/ledger.js:360-420, 1060-1115` · `ui2/finance-summary.html:34-43` | çapraz özet yalnız bugün | — | — |
| 6.5 | 1100–1112, 1198, 1212 | Girişte donan kur, orijinal + EUR, kaydı giren | KISMİ | `m039:63-64` · `m017:41-42` · `be/routes/contracts.js:895` | `payments.created_by` NULL yazılıyor | S | — |
| 6.6 | 1118–1120, 1208 | Referans veri Owner'da (kategori, tip, yöntem, para birimi) | KISMİ | `be/routes/referenceData.js:45-48` · `m039:89-90` | ödeme yöntemi 5 sabit; tedarikçi türü sabit | S | — |
| 6.7 | 1114–1122 | Gider kaydı (fuar / genel gider, tip, hesap, karşı taraf, belge) | ui2 VAR | `m039:57-92` · `ui2/finance-expenses.html` · `be/routes/expenseDrafts.js:115, 177` | — | — | — |
| 6.8 | 1126–1136, 1202 | Ödeme = kontrata bağlı gelir; plan ↔ gerçek | klasik VAR | `be/routes/contracts.js:752, 1455, 1496` · `klasik/contract-detail.html:1041` | ui2 kontrat salt okuma | ui2'ye S | — |
| 6.9 | 1120–1124 | Kontratsız gelir + gelir kategorisi | KISMİ | `m017:38` · `m052:19-21, 110` · `be/routes/contracts.js:746` | sponsorluk gibi gelir girilemiyor | M | — |
| 6.10 | 1138–1144 | Üçüncü taraf ödeyen + proforma | KISMİ | `m038:29` · `be/routes/contracts.js:810` | `payer` serbest metin; proforma BULAMADIM | M | — |
| 6.11 | 1146–1154, 1200 | Fuar bütçesi: satır, gerçekleşen, sapma, revizyon | ui2 VAR | `m040:28, 48` · `be/routes/ledger.js:863-915, 1030` · `ui2/finance-budget.html` | satır yalnız EUR; komisyon ödemesi gerçekleşene girmiyor | — | — |
| 6.12 | 1156–1162 | İşlem tek fuara; küme/ülke/ofis/yıl toplamı | KISMİ | `m039:66` · `be/utils/reportFields.js:156` | küme boyutu yok | S | — |
| 6.13 | 1164–1170, 1206 | Komisyon ödemesi kontrata bağlı gider; düzeltme | KISMİ | `m025:11-18, 36` · `be/routes/payouts.js:61, 260` · `klasik/agent-statement.html:355` | ödeme temsilci düzeyinde; ui2'de ödeme girişi yok (Commissions klasik köprü `nav.json:38`) | M | — |
| 6.14 | 1172–1180, 1204 | İptalde iade ya da kredi | KISMİ | `be/routes/contracts.js:1104-1114` (transfer) · `m039:133` (`refund` türü) · `be/utils/ledger.js:162` | iade yazan kod YOK; firma kredi kaydı yok; karar kontratta saklanmıyor | M | kontrat → firma bağı (m065:5) |
| 6.15 | 1068, 1210 | Zoho geçmişi eksiksiz, geri alınabilir | ui2 VAR | `be/scripts/zoho/migrate.js` · `m052:55` · `ui2/admin-migration*.html` | hesaplar arası transfer göçü BULAMADIM | — | — |

**Kullanım sinyali:** `accounts` 0 · `ledger_entries` 0 · `transfers` 0 · `legal_entities` 0 · `expo_budgets` 0 · `expense_drafts` 0 (ana veri
kesimde girilecek — kütük KES) · `expenses` 1.475 + `suppliers` 296 (Zoho göçü).

## 1. TAM ENVANTER — §2.7 Communication Automation (REQ 1214–1361)

| # | ★ | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|---|
| 7.1 | ★ | 1234–1247, 1342 | 8'li operasyon zinciri motoru | YOK | altyapı: `be/email_worker.js:47-52, 209` · kampanya adım motoru `m004:50, 55` + `email_worker.js:354` · `be/routes/contracts.js:241` (convert e-posta yazmaz) | adım motoru alıcı listesine bağlı, gecikmeyi önceki adımın kuyruğa girişinden sayar (G10); fuar/kontrata bağlı değil; 8 şablon + durum tablosu yok | L | 7.2, 7.10, 7.12; kontrattan alıcı e-postası (m065:5) |
| 7.2 | ★ | 1249–1259, 1346 | Fuar başına tetik ayarları | KISMİ | `m010:104-111` · `be/routes/expos.js:127-133` · `klasik/expo-form.html` | `payment_reminder_days_before` · `buildup_rules_days_before` · `badge_send_days_before` yok; ui2 ekranı yok | S | — |
| 7.3 | ★ | 1261–1267 | "Hepsini şimdi gönder" | YOK | `send_all` araması 0 | — | S | 7.1 |
| 7.4 | ★ | 1269–1271, 1354 | Tek e-postayı yeniden gönder + ayrı kayıt | YOK | yalnız ziyaretçi tarafında benzeri (`conferenceCertificates.js:764`, `visitors.js:1381`) | — | S | 7.1, 7.13 |
| 7.5 | ★ | 1273, 1354 | Zincir durum görünümü + hata uyarısı | KISMİ | `ui2/finance-contract.html:91-93` · `be/utils/salesMail.js:117` | LEENA bounce görmüyor (G9); "planlandı" durumu yok | M | 7.1 |
| 7.6 | ★ | 1238 | Hoş geldin e-postası | YOK | `be/utils/convertCore.js` · `be/utils/salesMail.js:81` (altyapı) | şablon, tetik, partner yer tutucuları yok | S | 7.10, 7.12 |
| 7.7 | ★ | 1244, 1253, 1336 | Ödeme hatırlatma | KISMİ | `m010:109` · `be/routes/analytics.js:120` · `el/packages/messages/index.js:56, 278` (iç WhatsApp taslağı) | katılımcıya hatırlatma + Finance gönderen kimliği yok | M | 7.1, 7.2, 7.10, 7.12 |
| 7.8 | ★ | 1303–1311, 1350 | Gelen yanıtlar kontrat geçmişinde (cc dahil) | KISMİ | `be/routes/emailInbound.js:13, 84-116` (yalnız iletir) · `m061:124-127` ('in' yönü tanımlı) · `lv/routes/webhooks.js:611` | INSERT yok; kontrat eşlemesi, cc, zincir yok | L | 7.1, 7.12 |
| 7.9 | ★ | 1224–1232, 1289–1301, 1348 | Operasyon/pazarlama ayrımı + abonelikten çıkma | KISMİ | `m004:135-139` · `be/email_worker.js:294-298` · `be/routes/unsubscribes.js:132-140` | şablonda sınıf bayrağı yok; yeniden abonelik izi silinir; LEENA + LIFFY iki liste; G7 | M | 7.10 |
| 7.10 | ★ | 1247, 1275–1279, 1344 | Tek şablon, EN/FR/TR tek düzenleyicide | KISMİ | `m061:37` · `be/routes/salesTemplates.js:22` · `ui2/admin-templates.html` | yalnız teklif e-postası; 8 operasyon şablonu + fuar yer tutucuları + sürüm geçmişi yok | M | — |
| 7.11 | | 1281–1287, 1356 | Dil seçimi: kişi → yerel kitle fuarı → EN | KISMİ | `be/utils/salesMail.js:40-56` · `m060:44, 48` | "yerel kitle" fuar bayrağı yok; ülke varsayılan dili boş | S | — |
| 7.12 | | 1305, 1334–1338 | Şablon başına gönderen kutusu | KISMİ | `be/utils/email.js:73` · `m061:103` · `m063:90` · LIFFY `sender_identities` | kimlik tablosu + eşleme yok | M | — |
| 7.13 | | 1319–1332, 1352 | Kanıt değerinde e-posta geçmişi | KISMİ | `be/routes/communications.js:131` · `be/email_worker.js:804` (G13) · `m004:111` | şablon sürümü, cc/bcc, içerik arşivi yok | M | 7.1, 7.5 |
| 7.14 | | 1289–1291, 1358 | Pazarlama kampanyası | LIFFY VAR | `lv/migrations/035…:10` · `lv/utils/dailyLimit.js:18` · `lu/app/campaigns/[id]/sequences/page.tsx` | klasik LEENA'da da var (`email-campaigns.html`); A/B konu yok | — | — |
| 7.15 | | 1313–1317, 1360 | WhatsApp: iç kullanım şimdi | eliza-legacy VAR | `el/apps/whatsapp-bot/src/handler.js:3` | eski ELIZA verisini okur; LEENA'ya bağlamak ayrı iş | — | — |

**Kullanım sinyali:** `email_queue` 571.014 (10 Ağu sonrası 308.447) · `email_logs` 733.953 · `email_events` 753.587 · `email_campaigns` 30
(son 2026-10-08) · `campaign_recipients` 250.963 · `reactivation_tokens` 207.994 · `email_templates` 112 · `email_unsubscribes` 1.688 ·
`sales_email_templates` 3 · `communications` 0.

## 1. TAM ENVANTER — §2.8 Reporting & Intelligence (REQ 1362–1488)

| # | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık |
|---|---|---|---|---|---|---|---|
| 8.1 | 1372–1382, 1467 | Owner günlük görünümü (m²/gelir hızı, açık bakiye) | ui2 VAR | `be/routes/analytics.js:333-362, 252-261` · `ui2/owner-home.html` | önceki edisyon kıyası yalnız fuar detayında | — | — |
| 8.2 | 1378, 1447, 1467 | Kişi ve ofis başına aktivite | KISMİ | `be/routes/analytics.js:370-384` | LIFFY aktivitesi sayılmıyor; pencere sabit 7 gün | M | LIFFY |
| 8.3 | 1384, 1439–1449, 1477 | Rol panoları (Proje Lideri, takım lideri) | KISMİ | `be/routes/analytics.js:335` · `ui2/sales-home.html` | Proje Lideri panosu yok | M | 7.1, 7.2, §2.4/2.5 |
| 8.4 | 1386–1398, 1469 | Zamanlanmış push raporlar | KISMİ | `m066:41` · `be/utils/reportPush.js:167-193` · `el/packages/push/index.js:17` | LEENA kanal yalnız e-posta; zorunlu/sessiz yok | L | 8.8 |
| 8.5 | 1400–1406, 1471, 1483 | Rapor oluşturucu: kaydet, çalıştır, takvime/panoya | KISMİ | `be/routes/reportBuilder.js:47-151` · `ui2/finance-reports.html` | grafik + pano parçası + lead modülü yok | M | 8.2 |
| 8.6 | 1408–1410, 1471 | Doğal dille rapor | ui2 VAR | `be/utils/reportNl.js` · `ui2/finance-reports.html:163` | kayıtlı raporu doğal dille düzenleme yok | — | — |
| 8.7 | 1412–1424, 1473 | AI içgörü (eğilim, anomali, öneri) | KISMİ (yalnız eliza-legacy) | `el/packages/alerts/index.js:108-236` | LEENA'da motor yok | L | 8.1, 8.2, 8.4 |
| 8.8 | 1451–1457, 1479 | WhatsApp doğal dil soru-cevap (kapsamlı) | eliza-legacy VAR | `el/packages/ai/queryEngine.js:1806, 1429` | LEENA verisini okumaz | — | — |
| 8.9 | 1426–1437, 1475 | Hiyerarşik görünürlük + kişiye istisna | ui2 VAR | `be/utils/permissions.js:32` · `m044:85, 100` | yöneticiler ekip görünümü alamaz (team = kişi) | — | 9.13 |
| 8.10 | 1459–1463, 1481 | Her sayıdan kaynak kayıtlara | KISMİ | `ui2/finance-summary.html:34-43` · `ui2/owner-home.html:30` | Owner aktivite satırları detaya inmez | S | — |
| 8.11 | 1485 | Kullanılan Zoho raporları yeniden kurulur | YOK | BULAMADIM | insan işi: rapor seçimi | S | 8.5 |

**Kullanım sinyali:** `saved_reports` 0 · `report_schedules` 0 · `report_runs` 0 (kesim öncesi).

## 1. TAM ENVANTER — Part 3 Cross-Cutting (REQ 1489–2104)

| # | REQ | madde | durum | kanıt | eksik / not | S/M/L | bağımlılık | kural |
|---|---|---|---|---|---|---|---|---|
| 9.1 | §3.1 1520–1533 | Kişi başı yetki matrisi; eylem × kapsam | ui2 VAR | `be/utils/permissions.js:62-86` · `be/routes/users.js:499-552` · `ui2/admin-user.html:74-107` | eylemler read/write/approve | — | — | YET-01/03/07 |
| 9.2 | §3.1 1505–1524 | 10 profil şablonu, anlık görüntü, yeniden uygulama | KISMİ | `m044:118-128` · `m059:116-128` · `m044:157-205` | 6 şablon; özel şablon ucu yok; şablon kullanıcıya CANLI bağlı (REQ "snapshot" tersi) | M | YET-04 yeniden açılırsa | YET-04/18 |
| 9.3 | §3.1 1545–1559 | Özel yetkiler: convert, durum, iade onayı, denetim | KISMİ | `m059:104-106` · `m062:28-31` · `m057:100-103` | ayrı convert / iade onayı / audit.read kodu yok | S | — | YET-19/20/23 |
| 9.4 | §3.1 1567–1569 | Yetki değişiklikleri denetlenir | ui2 VAR | `be/routes/users.js:488, 523, 543` · `m045:23-56` | "bu fuarı kim görüyor" sorgusu yok | — | — | YET-08 |
| 9.5 | §3.2 1591–1615 | Kullanıcı ≠ temsilci; isteğe bağlı bağ | ui2 VAR | `m014:31-45` · `be/routes/salesAgents.js` · `ui2/finance-agent.html` | — | — | — | YET-09/13/20 |
| 9.6 | §3.2 1597–1599 | Veri girişi taşeronu | YOK | — | YET-25 şablon içeriği AÇIK | S | YET-25 (Sentez) | YET-25 |
| 9.7 | §3.2 1601–1605 | Davetle açma, pasif/aktif, geçmiş | ui2 VAR | `be/routes/users.js:263-334, 425-458` · `ui2/admin-user.html` | davette `reports_to` yok | — | — | YET-05/06 |
| 9.8 | §3.2 1607, 1635 | Ayrılan personelin portföy devri | YOK | `m057:80-83` (created_by değişmez) | ayrı sahip kolonu gerekir | M | 9.13 | B6/B35 |
| 9.9 | §3.3 1645–1693 | Orijinal + EUR + donan kur; konsolidasyon | ui2 VAR | `m017:35-42` · `m039:57-64, 100-111` | — | — | — | LED-05, RAP-01 |
| 9.10 | §3.3 1657 | Günlük kur tablosu öneri olarak | KISMİ | `lv/routes/quotes.js:502-511` (LIFFY) | LEENA'da kur tablosu yok | M | — | LED-05 |
| 9.11 | §3.3 1659–1699 | İki taraflı hareket; türetilmiş bakiye; hesap silinmez | ui2 VAR | `m039:20-22, 272-280, 300-312` · `m036:89-112` | hesap türünde "other" yok | — | — | LED-03/06/07/10 |
| 9.12 | §3.4 1705–1715 | `reports_to` hiyerarşisi | LIFFY VAR | `lv/migrations/039_adr015…:14-15` · `lv/middleware/userScope.js:122-140` | LEENA: team = kişinin kendisi (`permissions.js:132-133`) | M | — | B33 |
| 9.13 | §3.4 1717–1728 | Kapsam ekleme/dışlama + "neden" | KISMİ | `m044:89-92` · `be/utils/permissions.js:127-151` | kayıt/fuar bazlı ekleme, dışlama, çoklu ofis yok | L | 9.12 | YET-03 |
| 9.14 | §3.4 1730–1738 | Satış / Proje gizlilik sınırı | KISMİ | `m044:139, 147` · `m062:15-18, 39` | Project şablonunda `contracts.read` yok (S3 kararı) | S | — | YET-18/19/23 |
| 9.15 | §3.4 1740–1744 | Rapor/arama/push kapsamı sorgu katmanında | ui2 VAR | `be/utils/reportFields.js:339-360` · `be/routes/search.js:32-37` | — | — | — | YET-14, RAP-13/15/16 |
| 9.16 | §3.5 1772–1833 | Referans listeleri admin ekranından | ui2 VAR | `be/routes/referenceData.js:34-69` · `ui2/admin-reference.html` | — | — | — | REF-01/03/04 |
| 9.17 | §3.5 1784–1797 | Eksik referans türleri (ödeme yöntemi, stand tipi, satış grubu, partner rolü, şablon tipi, ofis) | KISMİ | `m017:43` · `m010:143-144` · `be/routes/offices.js:8` | CHECK / serbest metin; ofis klasikte kapısız | M | — | REF-02, OFS-01 |
| 9.18 | §3.5 1805–1837 | Pasifle-silme yok; denetim; tür bazlı devir | KISMİ | `be/routes/referenceData.js:15, 225, 296` | `reference.write` tek kod | S | 9.17 | REF-03 |
| 9.19 | §3.5 1823–1841 | Tek liste tüm alt sistemlerde | KISMİ | `m060:10-11` · `lv/migrations/050:2, 22` | LIFFY'nin ayrı ofis/ürün/kur tabloları | S (kesim adımı) | KES | REF-01, KAT-03 |
| 9.20 | §3.6 1849–1888 | Önemli değişiklikler denetime | KISMİ | `m045:23-56` · `be/utils/audit.js:14-21` | kontrat durum/transfer/atama, ödeme, payout, temsilci, ofis yazmıyor | M | — | YET-08/22 |
| 9.21 | §3.6 1872–1894 | Denetim ekranı (Owner + Proje Lideri), öz-denetim | KISMİ | `be/routes/users.js:229-236` | genel ekran + `audit.read` yok | M | 9.20 | YET-08 |
| 9.22 | §3.6 1866–1890 | 24 ay sorgulanabilir, sonra arşiv | YOK | `m045:42-56` | arşiv yok | M | 9.21 | YET-08 |
| 9.23 | §3.6 1880–1896 | Sürüm koruma; created_by / modified_by | KISMİ | `m061:72-99` · `m040:11-12` · `be/routes/salesTemplates.js:70-81` | şablon önceki gövdesi saklanmıyor; kontrat durumu yerinde UPDATE | M | 9.20 | LED-05/15/22 |
| 9.24 | §3.7 1904–1955 | Genel arama (tüm modüller, gruplu) | KISMİ | `be/routes/search.js:40-70` · `ui2/sales-search.html` · `ui2/nav.json:72` | gider/ödeme/temsilci/partner/ürün yok; kabukta kutu yok | S | — | RAP-16 |
| 9.25 | §3.7 1918–1953 | Kayıtlı süzgeç + kişiye/ekibe paylaşım | KISMİ | `m066:26-39` · `be/routes/reportBuilder.js:83-147` | paylaşım yalnız kiracı geneli | M | 9.12 | RAP-14/15 |
| 9.26 | §3.7 1926–1957 | Kayıtlar arası gezinme | KISMİ | `ui2/sales-quote.html:39, 171` · `ui2/finance-contract.html:72-75` (düz metin) | kontrattan firma/kişi/fuar/temsilci bağlantısı yok | S | — | — |
| 9.27 | §3.7 1941–1959 | Son açılanlar + sabitlenenler | YOK | — | — | M (son açılanlar yerel: S) | — | — |
| 9.28 | §3.8 1971–2024 | Uygulama içi bildirim merkezi | YOK | LIFFY zili süs (`lu/components/layout-client.tsx:257-265`) | — | L | — | — |
| 9.29 | §3.8 1967–2016 | E-posta + WhatsApp kanalları; olay kataloğu | KISMİ | `be/utils/security.js:1-12` · `be/utils/reportPush.js:11` · `el/packages/push/index.js` | olay bazlı bildirim yok | L | 9.28 | GUV-03, RAP-15 |
| 9.30 | §3.8 1992–2022 | Kişi tercihi, zorunlu liste, sessize alma | KISMİ | `el/packages/db/migrations/017_push_messages.sql:5` | LEENA'da tercih tablosu yok | M | 9.28 | B32 |
| 9.31 | §3.9 2032–2095 | Çevrimiçi ödeme, e-fatura (Faz 2) | YOK | — | bilinçle Faz 2 | L | — | LED-01 |
| 9.32 | §3.9 2043–2093 | Muhasebeci dışa aktarımı | KISMİ | `be/utils/exportList.js` · `be/utils/reportPush.js` | salt-okuma şablonu yok | S | muhasebeci gereksinimi | RAP-11 |
| 9.33 | §3.9 2064–2097 | Gelen yanıt kontrat geçmişine | KISMİ | `be/routes/emailInbound.js:8-13` · `m061:107` | = 7.8 | M | — | ILT-01/03/05 |
| 9.34 | §3.9 2083–2101 | Alt sistemler arası iç API | ui2 VAR | `m047:9-16` · `be/routes/liffyExpos.js` | köprü kesimde askıya | — | — | KAT-03/04/05 |

**Kullanım sinyali:** `users` 5 (araç hesapları dahil) · `roles` 6 · `user_permissions` 1 · `audit_log` 8 · `access_log` 55 ·
`security_events` 2 · `organizers` 2 (org 2 = GUV-01, pasif).

---

## 2. KULLANIM SİNYALİ — yöntem

Staging = canlı **10 Kas 09:23Z** export'unun kopyası + göç 053→069 + PROVA-1 (araç hesapları, Zoho batch #4). 122 tablonun hepsi
`claude_readonly` + `BEGIN READ ONLY` ile sayıldı: satır · tarih kolonu (`created_at` > `updated_at` > ilk zaman kolonu) · en son tarih ·
10 Ağu sonrası satır. Kişisel veri okunmadı. Uyarılar: göç tablolarında `created_at` = göç zamanıdır (iş tarihi değil); `*_backup_*`
tabloları sayıma alınmadı. Bölüm sonlarındaki "Kullanım sinyali" satırları bu ölçümdür.

---

## 3. ÖLÇÜLMEDİ / BULAMADIM

- **ÖLÇÜLMEDİ:** LIFFY canlı DB (bu turda okunmadı — sayılar 5 Kas belgesinden) · eliza-legacy DB · klasik ekranların gerçek kullanıcı
  trafiği (erişim logu yalnız 069 sonrası, staging'de 55 satır) · Render log'ları.
- **BULAMADIM (aranan yerler bölüm tablolarında):** katalog veri modeli · PDF üretimi · herkese açık web katalog · ekstra hizmet sipariş
  formu · ekip primi kuralı (REQ'de de yok) · Welcome / Payment Reminder / BuildUp / Badge şablonları ve tetikleri · "send all" ·
  gelen e-postanın saklanması · iade yazan kod · firma kredisi · küme finans toplamı · proforma · `users.reports_to` (LEENA) · özel şablon
  ucu · audit okuma ucu / arşiv · bildirim merkezi · LEENA'da WhatsApp · Project Lead panosu · kayıtlı raporu panoya taşıma.
- **Sentez notu (karar değil, gözlem):** REQ §2.2 "convert yalnız Proje'de" ↔ kod `sales.write` (2.10); REQ §3.1 "şablon anlık görüntüsü"
  ↔ kod canlı bağ (9.2); REQ §3.4 "Project kontratları görür" ↔ S3 kararı (9.14). Üçü de kararla ya da yeniden tartıyla kapanır.

---

## 4. UI KUYRUĞU (kütük / defterdeki tüm "UI kuyruğu · UI-1 · tasarım fazı" notları — tek liste)

Süzgeç (YON-21 B): **yalnız karara bağlanmış ve ≤ S** → yapıldı (`eliza-next`, her biri ayrı commit). Kalanlar S/M/L ile.

| # | madde | kaynak | karar | durum (11 Kas) | S/M/L |
|---|---|---|---|---|---|
| U1 | Expenses / Drafts: kategori + tip iki ayrı kutu | [defter:2026-10-26 PAKET 3 CANLIDA] · kütük UI notu (Suer 26 Eki) | VAR | **YAPILDI — Q1** (`ee28499`) | S |
| U2 | Kontrat başlığında `contract_date` ISO zaman damgası | [defter:2026-11-05 B1-b] · Sentez 5 Kas karar 7 | VAR (UI kuyruğu kaydı) | **YAPILDI — Q2** (`342a670`; Admin › Migration › SD listesi de) | S |
| U3 | Sales "Komisyonlarım" ekranı | Sentez 6 Kas karar 7 = a · YET-23 · [defter:2026-11-06 PROMPT 3 (1)+(2)] SAPMA 7 | VAR | **YAPILDI — Q3** (`fa24645`; Sales › Overview › My commissions + `GET /api/sales-agents/mine`) | S |
| U4 | R4 Collections 7,2 sn hızlandırma | [defter:2026-11-06 SENTEZ: S1–S5 + UX HATTI] · 3b SAPMA 9 | VAR | **KISMİ — Q4** (`6fe4465`): dışa aktarım 5,7 / 3,8 sn → 1,0 / 0,75 sn (çıktı bayt bayt aynı). Ekran bugün 3,0–5,0 sn (898 satır; 7,2 sn / 2.080 satır 068 öncesiydi); eşzamanlı sorgu küçük DB'de kazanç vermedi → kalan "tek olgu sorgusu" | kalan S/M |
| U5 | Teklif listesi + convert kuyruğu 390 px | Sentez 5 Kas karar 7 | VAR (ölçüm) | **ÖLÇÜLDÜ — Q5**: 3 sayfada yatay taşma 0, konsol hatası 0; staging'de teklif 0 → satırlı liste ÖLÇÜLEMEDİ | S |
| U6 | Kabukta arama kutusu (S6) | Sentez 9 Kas S6 "UI kuyruğu + UX hattı" | VAR ama UX hattına bağlı | AÇIK — sonuç sayfası Sales alanında; Sales'i olmayan Finance kullanıcısı `L.guard(root, 'sales')`'e takılır (`ui2/sales-search.html:38`) → yer/IA kararı (UI-01 / UX-NN) | S (karar sonrası) |
| U7 | Commissions ui2 karşılığı (`/commissions.html` köprüsü) | UI-01 (Contracts grubu) · ★ | KISMİ (yer var, zaman yok) | AÇIK (`nav.json:38` legacy) | S |
| U8 | Agents yazma (yeni / düzenle, varsayılan %) ui2'de | `nav.json:41` "Agents (classic)" | YOK | AÇIK | S |
| U9 | Kontrata özel komisyon atama ekranı ui2'de | [defter:2026-10-26 PAKET 3 CANLIDA] "UI-1 adayı" | YOK | AÇIK | S |
| U10 | Teklif kopyalama | Sentez 5 Kas karar 7 (kayıt) | kopya anlamı kararı yok | AÇIK | S |
| U11 | Teklif sahibini ekrandan devretme | Sentez 5 Kas karar 7 (kayıt) | devir kuralı kararı yok | AÇIK | M |
| U12 | REF-02: ui2'de gömülü seçim dizileri API'den | REF-02 (Sentez 5 Kas) | VAR | AÇIK (6 dosya) | M |
| U13 | EMS gömülü listeler (visitor_type, 177 ülke, origin) | REF-02 | VAR | AÇIK (15+ yer; veri dönüşümü) | L |
| U14 | Çok dilli teklif PDF'i | 3b SAPMA 21 | zaman yok | AÇIK | M |
| U15 | Communication kartında sayfalama (son 200) | [defter:2026-11-05 PROMPT 2] | YOK | AÇIK | S |
| U16 | Teklif PDF'inde uzun satırlar kaydırılsın | 3b SAPMA 12 | ayrı hüküm yok | AÇIK | S |
| U17 | R1 dışa aktarım: detay alt listeleri, admin listeleri, EMS | 3b SAPMA 8 | ön-onaylı SAPMA | AÇIK | M |
| U18 | R2 aylık eğilim için gerçek grafik | Sentez 6 Kas "tasarım fazı" | VAR (tasarım fazı) | AÇIK — kütüphane kararı (UI-05 "derleme yok") | M |
| U19 | Leads uçları oturumsuz (E2–E4) | Sentez 9 Kas S7 | VAR (UI kuyruğu) | AÇIK | M |
| U20 | Organizer ana paneli (UI-06) + "giriş → fuar seç" borcu | UI-06 · Suer 23 Tem | VAR | KISMİ (R7 Owner ana sayfası örtüşür; kapatan kayıt yok) | L |
| U21 | TAŞI: EMS/klasik sayfaların ui2'ye taşınması | [defter:2026-10-23 UI-0 BELGE KAPANIŞI + UI-0b HÜKÜMLERİ] | KISMİ | AÇIK → **§5 taşıma planı** | L |
| U22 | Sayfa içi bağlantıların menüye alınması | [defter:2026-10-22 PAKET 1b BELGE KAPANIŞI] | VAR (tasarım fazı) | AÇIK | L |
| U23 | ui2 sayfa geçiş yavaşlığı ölçümü (nav.json + /me) | Sentez 22 Eki "ölçülecek" | VAR | AÇIK (ölçülmedi) | M |
| U24 | Tema: bağlantı rengi, tema değiştirici | UI-0 🔶4-5 | YOK | AÇIK | S (teknik) |
| U25 | UX hattı (UX-NN kriterleri) | Sentez 6 Kas UX HATTI | VAR | AÇIK (kriter yok) — YON-21: tasarım fazı ŞİMDİ | L |
| U26 | Rol/yetki ekranı cilası | Sentez 5 Kas B2 kapsam dışı | zaman yok | AÇIK | M |
| U27 | UI-0b açık soruları (common.js, yürüyen bakiye, "(new)" etiketi, tasarım sayfaları) | [defter:2026-10-23 PAKET UI-0b: STAGING'E HAZIR] | YOK | AÇIK | S |
| U28 | LIFFY'de kendi şifresini değiştirme | [defter:2026-11-04 LIFFY STAGING + DENEME-0] | YOK | AÇIK — ADR-023 sonrası anlamı sorgulanır | S |
| U29 | Genel ilke: inşada iskelet, tasarım ayrı faz | Suer 21 Tem · YON-16 · KES-05 | VAR | YON-21 ile DEĞİŞTİ: tasarım fazı şimdi, paketlerle iç içe | L |

**KAPALI çıkanlar (kayıt güncel değil):** servis kullanıcısında "Resend invitation" gizleme (`606d175` → `0c90d0d`, canlı 26 Eki) · kontratta
indirim % + satır toplamı (`c5ad2ee`) · Sales `liffy` alt etiketi (`c5ad2ee`) · dış kullanıcıda Convert queue gizleme (`7428770`) · Agents
ui2 liste + detay (`05bd86f`) · 0 fiyat rozeti (B1-b) · DENEME-0 → UI-1 girdisi ve UI-1 paketinin kendisi (ADR-023 ile İPTAL).
★ bloğundaki "UI-1 kuyruğu" listesi 25–26 Eki tarihli; bu tablo onun yerine geçer.

---

## 5. OPERATIONS TAŞIMA PLANI (klasik EMS ekranları → ui2)

**Bugün:** ui2 Operations = tek öğe (`ops-expos` → `ui2/operations-expos.html`: liste + Sales (R3) / Visitors (R8) sekmesi). R8 Visitors
sekmesi klasik `reports.html`'i `localStorage.selectedExpoId` kurarak açar (`ui2/operations-expos.html:146-150`) — nav.json `legacy`
köprüsü değil, doğrudan bağlantı. **nav.json legacy köprüleri:** 2 (ikisi de Finance › Contracts: `commissions` → `/commissions.html`
`nav.json:38` · `agents` → `/sales-agents.html` `nav.json:41`); Operations'ta legacy öğe yok. Klasik sayfa: kök 51 + `callcenter/` 3;
klasik `main-panel-v2.html` yan menüsünden ui2'ye tek bağlantı ("ELIZA Finance (new)", `main-panel-v2.html:968`).

Şablonlar UI-03: **L**iste · **D**etay · **F**orm · **Ö**zet kartları. Terminal / herkese açık yüzler (qrscanner, badge, badge-print,
bulk-badge-print, conference-scanner, lead-scan, form-public, reactivate*, certificate*, hostess-guide, callcenter agent/supervisor) **ui2
kabuğuna taşınmaz** — anahtar/token ile açılan, menüsüz ekranlardır; yalnız yönetim tarafları taşınır.

| sıra | klasik ekran(lar) | ui2 hedefi | şablon | kullanım (staging) | S/M/L | not |
|---|---|---|---|---|---|---|
| 1 | `dashboard_new.html` · `main-panel-v2.html` · `expo-list.html` · `expo-form.html` · `expo-create.html` · `expo-clusters.html` · `expo-partners.html` | Operations › Expos: detayda **Overview** (main-panel özet) + **Settings** (expo-form: tarih, son günler, form URL, cluster, partner) sekmeleri | L (var) + D sekmesi + F + Ö | expos 214 · clusters 1 · partners 324 | M | çapa: fuar merkezli Operations; 5.1–5.6, 5.9 |
| 2 | `visitorlog-paginated.html` · `import.html` · `reports.html` · `checkins.html` · `checkin-reports.html` · (`checkin-import.html` — ölü aday, Suer istisnası) | Expo › **Visitors** sekmesi (R8 bugün klasik rapora gider) | L + Ö + F (içe aktarma) | visitors 112.868 · checkins 46.233 · import_jobs 73 | M | en yoğun kullanım; G21/G24 tuzakları (içe aktarma) |
| 3 | `form-list.html` (+ `form-builder.html`) | Expo › **Forms** (liste ui2'de; tasarım editörü klasikte kalır, bağlantıyla) | L (+ klasik editör) | forms 70 (son 2026-11-02) | S (liste) · L (editör) | form-public herkese açık kalır |
| 4 | `terminals.html` · `badge-templates.html` | Expo › **On-site** (terminal + yaka kartı şablonu yönetimi) | L + F | terminals 52 · badge_templates 7 | M | G15/G22 (klon, kopya URL) |
| 5 | `email-templates.html` · `email-send.html` · `email-segments.html` · `email-history.html` · `email-campaigns.html` · `reactivation-campaign.html` | Operations › **Communication** | L + D + F | email_campaigns 30 · campaign_recipients 250.963 · reactivation_tokens 207.994 | L | §2.7 zinciriyle (7.1, 7.9, 7.10) BİRLİKTE tasarlanmalı — iki ayrı şablon sistemi doğmasın |
| 6 | `conference-sessions.html` (+ geçici `conference-cleanup.html`) | Expo › **Conferences** | L + Ö | conference_certificates 931 | S | cleanup aracı taşınmaz (geçici, ADR-021) |
| 7 | `callcenter/admin.html` | Operations › **Call center** | L + Ö | callcenter_leads 41.396 (son 2026-10-02) | M | ajan/süpervizör ekranları anahtarla kalır |
| 8 | `floorplan-builder.html` (+ `floorplan/*`) | Expo › **Floor plan** (önce ui2 köprüsü; editör Konva olarak kalır) | köprü + D | stand 11, son 2026-04-21 | köprü S · kontrat bağıyla L | 5.15 (stand ↔ kontrat) ile birlikte; Nisan'dan beri kullanım yok |
| — | Finance klasik: `commissions.html` · `sales-agents.html` · `agent-statement.html` · `contract-list/-detail.html` · `cash-forecast.html` · `offices.html` | Finance (UI-01 grupları) | L + D + F | — | S'ler (U7–U9, 3.1–3.9, 6.8) | Operations dışı; legacy köprüler buradan kalkar |

**Sıra önerisi gerekçesi:** (1) fuar merkezi diğer sekmelerin kabı · (2) en yoğun kullanılan klasik yüz · (3)–(4) fuar kurulumunun kalan
yönetim ekranları · (5) en büyük ve §2.7 ile birlikte tasarlanması gereken alan · (6)–(8) düşük kullanım. Fuar günleri (Cezayir 17–20
Kas) G42 gereği gündüz deploy yok. Paket sırası Suer önceliğinden sonra (YON-21).
