> **Arşiv notu (CC, 2026-11-11) — aşağıdaki metnin parçası DEĞİLDİR.**
> **Ne:** UX hattının 2. tur çıktısı (11 Kas 2026): tasarım seti × üç kullanıcının günü. Orchestrator'ın 11 Kas 17:55 tarihli
> "İKİ EK" bloğuyla geldi; çizginin altındaki metin o bloktaki haliyle **AYNEN** (oturum kaydından alındı, elle yazılmadı).
> **Statü:** 2. tur **KRİTER DEĞİLDİR** — arşiv + UI fazı takip belgesinin "tasarım kaynağı" sütunu. Öncelik sırası: Sentez bloğu >
> UX 3. tur > UX 2. tur. 2. turda olup UI-TAM-2 kapsamında olmayan maddeler (ör. Fuarlar listesi · satışçı için kat planı · Owner ana
> sayfası ekleri · katalog üretici · War Room uyarıları) İNŞA EDİLMEZ; takip belgesinde "kuyruk — Sentez kararı bekliyor" olarak durur.
> **Biçim:** tablo Orchestrator'a sekmeyle ayrılmış düz metin olarak ulaştı; sütunlar `|` ile ayrıldı, hücre metinleri AYNEN (Orchestrator
> notu). Bu dosyada yalnız Markdown yapısı eklendi: başlık işaretleri (`#` · `##` · `###`), satırlar arası boş satır, tablonun başlık
> ayırıcı satırı. Sözcük, noktalama ve sıra değişmedi. Tarihseldir (YON-01): ölçüm tarihi 11 Kas 2026.

---

# UX HATTI — 2. TUR ÇIKTISI (11 Kas) · Tasarım seti × üç kullanıcının günü

Kısa cevap: Karşılamıyor. Set “durumu gösteren” ekranlarda güçlü, “işi yaptıran” ekranlarda boş.

Yaprak: en zayıf taraf. Katılımcının durumu görünüyor; form, onay, sipariş, e-posta zinciri ve fuar ayarları yok.

Satışçı: tek teklif ve tek firma sayfası var. Listeler, “gönder” ve “imzalandı” adımları, satışçı için kat planı yok.

Owner: War Room yalnız para. m² ve veri girişi okuduğum hiçbir ekranda yok.

## Neye baktım

22 ekranın 15'ini okudum. 4'ü projede (Sales: My Work, Pipeline, Quotes, Companies). 11'i bilgisayarındaki ell-docs/archive/design kopyasından (dosya tarihi 9 Eyl). Bugün indirdiğin setle aynı olduğunu ölçmedim.

7 ekranı görmedim (satır 38). Mail için 1. tur brief’ine dayandım.

Staging’deki yeni arayüzün (ui2) bugünkü halini ölçmedim.

Finans rakam mantığına dokunmadım; Finance satırları yalnız eksik görünüm ve geçiş.

## İşaretler

† = sette yok, ama bilgi mimarisi belgesi v4'e ya da senin 6 Kas özetine göre ui2'de karşılığı var veya planlı.

‡ = ilgili ekranı görmedim.

Öncelik: 1 = bu olmadan kullanıcı o iş için Zoho’ya döner · 2 = iş yürür ama elle · 3 = sonra.

| # | Ekran | Kim | Eksik olan | Öneri | Önc. |
|---|---|---|---|---|---|
| 1 | Fuarlar listesi (YENİ) | Proje ekibi, Owner | Tüm fuarları yan yana gösteren ekran yok. Dashboard tek fuara bağlı; fuar değiştirici yalnız açılır liste | Proje ekibinin giriş ekranı — eskiz 5 | 1 |
| 2 | Ops – Dashboard | Proje ekibi | Sayı var, “bugün kimi kovalayacağım” listesi yok. Son tarihler yok (katalog, tasarım, ödeme). En büyük kart canlı giriş grafiği; yalnız fuar günlerinde dolu | İki mod: fuar öncesi (son tarihler + kovalanacaklar) / fuar günü (canlı giriş). Her sayı tıklanınca listeye insin | 1 |
| 3 | Convert inceleme (teklif → kontrat) † | Proje ekibi | Sette yok; Quotes’ta yalnız “Operations’a gider” notu | İmzalı teklif ve imzalı tarama yan yana; eksik alanlar tek formda; “Çevir” | 1 |
| 4 | Fuar ayarları (YENİ) | Proje ekibi | Fuar kartı yok: kurulum günleri, son tarihler, ortak firmalar, iletişim kişileri, e-posta zamanlaması | Eskiz 4 | 1 |
| 5 | Ops – Exhibitor (liste) | Proje ekibi | “Onboarding” sütunu adsız 4 nokta; hangi adımın takıldığı okunmuyor. Satışçı ve ülke sütunu yok. Toplu işlem yok | Adlı sütunlar: Katalog · Tasarım · Sipariş · Rozet · Ödeme. Süzgeç “takılanlar”. Seç → “hatırlat” | 1 |
| 6 | Ops – Exhibitor (liste) | Proje ekibi | Tek kontrat–çok katılımcı gösterilemiyor (acente pavyonu, ortak katılımcı). “Add exhibitor” neyi eklediği belirsiz | Kontrat altında alt satır; düğme “Alt katılımcı ekle” | 2 |
| 7 | Ops – Exhibitor Detail | Proje ekibi | Katalog ve tasarım yalnız “tamam” etiketi. Gönderilen içerik, dosya, onay düğmesi yok | Her adım açılır: içerik + Onayla / Düzeltme iste / Hatırlat | 1 |
| 8 | Ops – Exhibitor Detail | Proje ekibi | Ekstra sipariş hiç yok | “Siparişler” kartı: kalem · adet · durum | 1 |
| 9 | Ops – Exhibitor Detail | Proje ekibi | 8 e-postanın durumu yok; yalnız “Message” düğmesi | “E-posta zinciri” kartı: 8 satır, durum + yeniden gönder + “hepsini şimdi gönder” | 1 |
| 10 | Ops – Exhibitor Detail | Proje ekibi | Proje ekibinin kontrata girdiği alanlar yok: satış grubu, nakliye, bedelsiz m², katalog sayfa no. Stand atama adımı yok | “Operasyon bilgileri” kartı; stand kat planından seçilir | 1 |
| 11 | Ops – Exhibitor Detail | Proje ekibi | Müşteriyle yazışma geçmişi yok | “Yazışma” sekmesi; satışçı firma kartındaki aynı bileşen | 2 |
| 12 | Ops – Exhibitor Detail | Proje ekibi | Durum değişikliği yok: beklet · başka fuara aktar · iptal | “⋯” menüsünde üç eylem; aktar = hedef fuar seç | 2 |
| 13 | Ops – Exhibitor Detail | Proje ekibi | Set iki kural varsayıyor: “ödeme yoksa kurulum kilitli” ve 5 maddelik kurulum listesi (yüklenici sigortası, risk değerlendirmesi…). Sizde böyle mi, bilmiyorum | Yaprak’a soru. Kural yoksa etiket “ödeme gecikti” uyarısına insin; liste stand tipine göre kısalsın | 2 |
| 14 | Ops – Communications | Proje ekibi | Ekran “kampanya → alıcı grubu” mantığında. Kontrata bağlı 8'li zincir görünmüyor | “Zincir” görünümü — eskiz 3. Kampanya sekmesi toplu ve pazarlama postası için kalsın | 1 |
| 15 | Communications › Templates | Proje ekibi | Listede 8 türün 2'si var (ödeme hatırlatma, rozet). Düzenleyici yok: 3 dil, gönderen kutu (Proje / Finans) | Tek şablon–üç dil (EN/FR/TR) yan yana + fuar seçerek önizleme | 2 |
| 16 | Katalog formu + takibi (YENİ) | Katılımcı · Proje ekibi | Sette yok | Eskiz 1 | 1 |
| 17 | Stand tasarımı onayı + ekstra sipariş (YENİ) | Katılımcı · Proje ekibi | Sette yok | Eskiz 2 | 1 |
| 18 | Katalog üretici (Corel yerine) | Proje ekibi | Sette yok | Şablon seç → önizle → PDF. Ayrı tur ister | 2 |
| 19 | Rozet + fuar günü ‡ | Proje ekibi, saha | Detail’de “Issue badges” var; isimleri kimin, nereden girdiği yok. “Firma geldi mi · stand teslim · sorun kaydı” okuduğum ekranlarda yok | Rozet isimleri katılımcı sayfasından; Exhibitor listesine fuar günü görünümü | 2 |
| 20 | Ops – Reports | Proje ekibi | Kayıt kaynağı kırılımı yok (ajans · web formu · e-posta). Ofis veri girişi raporu yok | Kayıt grafiğine “kaynağa göre”; veri girişi Owner sayfasıyla aynı kaynaktan | 2 |
| 21 | Sales alt menü | Satışçı | Baktığım 4 dosyada “Mail” sekmesi yok. “Activity” sekmesinin ekranı yok | Sıra: Mail · My Work · Pipeline · Quotes · Companies. Activity kalksın ya da “Takipler” olsun | 1 |
| 22 | Sales – My Work | Satışçı | Sekmeler 1. tur özet kutusuyla uyuşmuyor: “imzalı, kontrata çevrilmemiş teklifler” yok; “Approvals” neyin onayı belirsiz | My Work = kutunun “hepsini gör” sayfası; 4 sekme kutuyla aynı ad, aynı sorgu | 1 |
| 23 | Sales – My Work | Satışçı | “Today” takvimi (arama, toplantı) elle giriş ister; Zoho’da tutmayan model. Hedef kartı yalnız para, m² yok | Takvim yerine “bugünkü takipler”. Hedefte m² + tutar | 2 |
| 24 | Sales – Pipeline | Satışçı | Lead kartlarında m² ve tutar var; sizde lead çoğu zaman yalnız bir e-posta ve sayısı binlerle. Kartta fuar adı yok | Pano “Cevap verdi”den başlasın; öncesi sayı + listeye geçiş. Karta fuar adı | 2 |
| 25 | Sales – Quotes † | Satışçı | Teklif listesi yok; sekme tek teklifi açıyor | Liste: fuar · firma · m² · tutar · durum · kaç gündür bekliyor | 1 |
| 26 | Sales – Quotes | Satışçı, satış müdürü | Kalemler serbest metin. Fiyat listesinden ürün seçimi, indirim satırı, para birimi seçimi, EUR karşılığı yok. “Kimin satışı” (kişi / acente) alanı yok | Ürün seçici (fuar × para birimi), indirim satırı, EUR karşılığı, “kimin satışı” | 1 |
| 27 | Sales – Quotes | Satışçı | “Gönder” penceresi yok (kime, hangi dil, metin, ek). “Mark as signed” imzalı tarama ve tarih istemiyor | Gönder: alıcı + şablon + ek. İmzalandı: tarama yükle + tarih zorunlu | 1 |
| 28 | Satışçı için kat planı | Satışçı | Kat planı Operations sekmesinde; satışçı o sekmeyi görmüyor. Stand ayırma (“48 saat”) planda görünüyor; kimin, nereden yaptığı yok | Sales’te salt okunur plan: boş / ayrılmış / satılmış + “ayır” + “müşteriye gönder” | 1 |
| 29 | Sales – Companies † | Satışçı | Firma listesi ve arama yok; tek firma sayfası | Liste + süzgeç: sektör · ülke · sahibi · son temas | 1 |
| 30 | Sales – Companies | Satışçı | 1. tur firma kartıyla aynı değil: takipler ve yazışma sekmesi, sahiplik / 3 ay uyarısı, “ilgilenmiyor” düğmesi yok. Önceki kontratta m² yok; başkasının tutarı kilitli değil. “Log activity” elle kayıt | Sayfa 1. turdaki tek bileşeni kullansın (uyarılar · düğmeler · 4 sekme) | 1 |
| 31 | Lead listesi + kampanya | Satışçı | Sette ekran yok; v4 belgesine göre geçişe kadar eski LIFFY’de | Sentez’e soru: satışçı iki sisteme mi girecek? | 2 |
| 32 | Owner ana sayfası (YENİ) † | Suer | Üç günlük görünümü bir arada veren ekran yok | Eskiz 6 | 1 |
| 33 | Finance – War Room | Suer | m² yok. Fuar başına hedef ve “geçen edisyonun aynı günü” karşılaştırması yok. Satışçı kırılımı yok. Fuar başına açık bakiye yok (yalnız toplam + vadesine göre döküm) | “Top expos” tablosuna sütun: m² · hedef % · açık bakiye · geciken. Tanım sunucudan | 1 |
| 34 | War Room › Alerts | Suer | 4 uyarının 4'ü finans. Satış ve operasyon uyarısı yok (ofis sessiz · fuar geçen yıldan yavaş · katalog oranı düşük · imzalı teklif çevrilmedi). “Gördüm / ertele” yok | Tek liste, üç kaynak; her uyarı kayda iner; gördüm / ertele | 1 |
| 35 | Finance – Expo Finance | Suer | Satırdan harekete inilmiyor. Tüm fuarların listesi yok (“Expos” sekmesi tek kümeyi açıyor). m² ve firma sayısı yok | Satır tıkla → hareketler. Önce fuar listesi, sonra detay. Üste m² + firma sayısı | 2 |
| 36 | Onaylar + Finance › Reports | Suer | İstisna onayı (büyük indirim, iade) için ekran yok. “Reports” sekmesi boş bağlantı | Owner sayfasında “onay bekleyen” kutusu; Reports = kayıtlı + zamanlanmış raporlar | 2 |
| 37 | Üst çubuk + Settings | Herkes | Zil ve arama simgesi var, açılan ekranı yok. Settings’te yalnız Appearance dolu; Profile (dil), Notifications, Team & roles boş. “Billing” iç ürün için gereksiz | Bildirim paneli + arama sonuç sayfası; Profile’da dil; Billing kalksın | 2 |
| 38 | Görmediğim 7 ekran ‡ | — | Login · Sales – Mail · Ops – Visitor & Access · Finance – Commissions · Mobile – Dashboard · Mobile – Scan · Mobile – Visitor List | Dosyalar gelince satır eklerim | — |

## Eskizler

### Eskiz 0 — Katılımcı sayfası (1 ve 2'nin çatısı; iki yol)

Yol A: Tek sayfa, tek link, şifre yok. Bölümler: Katalog · Stand tasarımı · Ekstra sipariş · Stand görevlileri (rozet) · Kurallar ve belgeler · Ödeme özeti. 8 e-postanın her biri ilgili bölüme götürür.

Yol B: Her iş için ayrı form linki (bugünkü Zoho Forms düzeni).

Tercihim A. Müşteri tek yere bakar; her bölümün durumu aynı yerden okunur, zincir ekranı kendiliğinden dolar.

Risk: Link başkasına iletilirse fiyat ve ödeme görünür; bu iki bölüm e-postaya gelen kodla açılsın. Requirements §5.2 girişli portalı kapsam dışı sayıyor; bu girişsiz. Sınırı Sentez tartar.

### Eskiz 1 — Katalog formu + takibi

Ekran:

Katılımcı yüzü: katalogdaki firma adı · markalar · ürün grupları · tanıtım yazısı · logo · iletişim · ürün görselleri. Üstte son tarih; o güne kadar düzeltilir, sonra kilitlenir.

Proje ekibi yüzü: fuar başına liste (Gönderilmedi · Taslak · Gönderildi · Düzeltme istendi · Onaylandı). Satıra tıkla → sayfa önizlemesi + Onayla / Düzeltme iste / Hatırlat.

Ne çözüyor: Kimin göndermediği tek bakışta görülmüyor; takip elde.

Kim: Katılımcının yetkilisi · proje ekibi.

Bugüne göre: Zoho Forms ve Catalogues modülü kalkar; onay adımı ve tek tık hatırlatma gelir.

Risk: Yarım bırakılan form (otomatik hatırlatma şart); baskıya yetmeyen logo (yüklemede uyarı); kilit sonrası istisna yetkisi kimde.

### Eskiz 2 — Stand tasarımı onayı + ekstra sipariş

Ekran:

Tasarım, iki yön: hazır standda proje ekibi çizimi yükler, katılımcı “onaylıyorum / değişiklik istiyorum” der. Özel tasarımda katılımcı çizimini ve yüklenicisini yükler, proje ekibi onaylar. Her tur kayıtlı.

Sipariş: fuarın fiyat listesinden kalem + adet (ekipman · ek hizmet · vize yazısı), toplam, gönder.

Proje ekibinde “Siparişler” listesi + stand firmasına verilecek döküm.

Ne çözüyor: Sipariş e-posta ve formda dağınık; tasarım onayı Drive linkinde kalıyor.

Kim: Katılımcı · proje ekibi · yerel ofis; stand firması yalnız dökümü alır.

Bugüne göre: Sipariş kayda dönüşür; son tarihten sonra gelen “gecikmiş” işaretlenir.

Risk: Sipariş paraya nasıl dönüşecek (mevcut kontrata ek kalem mi, yeni kontrat mı) Sentez’in kararı. Zoho’daki gerçek sipariş formunu görmedim; alanlar varsayım.

### Eskiz 3 — E-posta zinciri durumu (8 e-posta)

Ekran:

Satır = katılımcı. Sütun = Welcome · Katalog · Stand tasarımı · Boost · Ekstra hizmet · Kurulum kuralları · Ödeme hatırlatma · Rozet.

Hücre: planlı (tarih) / gitti / açıldı / hata. İş isteyen e-postada ikinci işaret: iş bitti mi.

Üstte 8 küçük özet kartı. Varsayılan süzgeç “yalnız sorunlular”.

Eylemler: yeniden gönder · hepsini şimdi gönder · hariç tut (not ile). Toplu gönderimden önce alıcı listesi önizlenir.

Ne çözüyor: Bugün kontrattaki kutucuklar; kimin hangi e-postayı aldığı, hangisinin döndüğü görünmüyor.

Kim: Proje ekibi; Finans (ödeme sütunu).

Bugüne göre: Kutucuk işaretlemek yerine zincir kendi yürür; ekran yalnız istisnayı gösterir.

Risk: “Açıldı” bilgisi güvenilmez; karar “iş bitti mi”ye bakmalı.

İki yol: A) firma × e-posta tablosu. B) e-posta türü listesi → alıcılar. Tercihim A; B üstteki özet şeridi olur.

### Eskiz 4 — Fuar ayarları

Ekran: Tek sayfa, 5 bölüm:

Kimlik (ad, edisyon, şehir, mekân, tarih)

Kurulum (kurulum günleri, saatler, söküm)

Son tarihler (katalog, tasarım, sipariş, ödeme, vize)

Ortaklar (stand firması, seyahat, vize, nakliye, hostes, ikram)

E-posta zamanlaması (imzadan kaç gün sonra / fuardan kaç gün önce)

Ne çözüyor: 8 e-posta ve katılımcı sayfası bu veriyi kullanır; bugün Zoho’daki fuar kartında.

Kim: Proje ekibi yazar; satış okur.

Bugüne göre: Form linkleri elle girilmez; zamanlama fuar başına ayarlanır.

Risk: Yeni fuarda onlarca alan boş kalır; “önceki edisyondan kopyala” + eksik alan sayacı gerekir.

### Eskiz 5 — Fuarlar listesi (proje ekibinin girişi)

Ekran: Satır = fuar. Aynı mekânda aynı tarihte yapılanlar (küme) gruplu. Sütunlar: kalan gün · imzalı firma · satılan m² · katalog % · tasarım % · açık bakiye · bugün bekleyen iş. Tıkla → o fuarın Dashboard’u.

Ne çözüyor: Proje ekibi aynı gün birkaç fuara bakıyor; set tek fuar varsayıyor.

Kim: Proje ekibi, Owner; yerel ofis yalnız kendi fuarları.

Bugüne göre: Fuar fuar rapor açmak yerine tek tablo.

Risk: Sütun şişer (7 ile sınırlı kalsın); rakamlar Owner sayfasıyla aynı tanımdan gelmeli.

### Eskiz 6 — Owner ana sayfası

Ekran: Üç blok + uyarılar; her sayı kayıtlara iner.

Satış hızı: fuar başına m² ve tutar; hedefe göre %, son 7 gün, geçen edisyonun aynı gününe göre fark.

Veri girişi: kişi ve ofis başına son 7 gün; sıfıra düşen işaretli.

Açık bakiye: fuar başına kontrat · tahsil edilen · kalan · geciken.

Sağda tek uyarı listesi (satış + operasyon + finans) ve onay bekleyenler.

Ne çözüyor: Bugün Zoho Analytics + üç ayrı rapor; War Room yalnız finans.

Kim: Suer; satış müdürü kendi kapsamıyla ilk iki bloğu görür.

Bugüne göre: Owner’ın girişi Finance özeti yerine bu sayfa olur.

Risk: “Geçen edisyonun aynı günü” eski kontratların imza tarihine dayanır; verinin yeterli olup olmadığını Sentez ölçtürür.

İki yol: A) alan sekmelerinin üstünde ayrı sayfa. B) War Room’u genişlet. Tercihim A; War Room Finance sekmesinde ve satış müdürü o sekmeyi görmüyor.

## Açık sorular

Yaprak’a: Ödeme gelmeden kurulum gerçekten kilitleniyor mu?

Yaprak’a: Kurulum için firmadan gerçekte ne isteniyor?

Yaprak’a: Rozet isimleri bugün nasıl toplanıyor (kaç hak, kim giriyor)?

Yaprak’a: Zoho’daki stand tasarımı ve ekstra sipariş formlarından birer örnek gerekiyor.

Sentez’e: Ekstra sipariş kontrata nasıl bağlanır?

Sentez’e: Ürün ve fiyat listesini bugün proje ekibi açıyor, yeni sistemde yalnız Owner yazabiliyor; bilinçli mi?

Sentez’e: Lead ve kampanya ekranları geçişe kadar nerede?
