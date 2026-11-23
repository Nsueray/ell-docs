> **Arşiv notu (CC, 2026-11-23) — aşağıdaki metnin parçası DEĞİLDİR.**
> **Ne:** UX hattının "KABUK-2 TESLİM (14 Kas)" notu — üç kabuk (A · B2 · B1) + font seçenekleri. Orchestrator'ın 23 Kas 2026 tarihli PAKET KABUK-2
> promptundaki "(2)" bölümünün kopyası; çizginin altındaki metin o dosyadan programla alındı (112 satır). Düz metindir; satır yapısı korunsun diye
> dört işaretli kod çiti içinde verildi (çit metnin parçası değil; metnin kendi içinde üç işaretli bir çit var).
> **Statü:** REFERANSTIR, **kriter DEĞİL** — kriter Sentez bloğu ([defter:2026-11-23 SENTEZ 23 Kas: PAKET KABUK-2]). Baştaki giriş satırları ve son satır Suer'e hitaptır.
> İçindeki "KARAR / CEVAP BEKLEYENLER" Sentez bloğunda (C) ve (D) ile KAPANDI: B1 yapılmaz (kuyruk) · varsayılan düzen A · varsayılan font DM Sans + DM Mono
> · aday listesi Sentez D2 (mockup'taki dört takım ürünün listesi değildir).
> **Mockup dosyası:** `ELIZA-Kabuk-2-A-B-mockup.html` — sha256 `384a6c1034eebb38f84860bb9ab658acce1d2650d702a80abb71dc5efffa891b` · 76.182 bayt · 649 satır.
> T8 (Sentez 23 Kas): HTML mockup'lar **LEENA (private) `docs/ux/`** altında bayt bayt AYNEN durur; ell-docs'ta yalnız ad + sha256 (`docs/UI_FAZI_TAKIP.md` §5).
> Mockup'ın CSS'i / token'ları, üstteki koyu şerit (Shell option · Font · Numbers · Font check), B1 ve Google Fonts bağlantıları ürüne TAŞINMADI.

---

````
Üç kabuğu ve font seçeneklerini mockup'a ekliyorum: A, benim B'm (açılır menü) ve senin B'n (üstte modüller, solda sayfalar). Fontları bu sefer gerçek font dosyalarıyla deneyeceğim.

Üç kabuk ve dört font takımı aynı dosyada: `ELIZA-Kabuk-2-A-B-mockup.html` (önceki sürümün yerine geçer).

"Zorlaştırırsa A ve benim B" kuralına göre önerim A + senin B'n (B2): ikisi aynı sol listeyi kullanıyor. Benim B'm (B1) ayrı bir menü sistemi; kesin maliyeti Claude Code'un ölçmesini blokta istedim.

## Nasıl bakılır
- **Kabuk:** üstteki koyu şeritte `Shell option` → A · B2 (senin tarifin) · B1 (açılır menü).
- **Font:** aynı şeritte `Font` ve `Numbers`. Dört takım var: bugünkü, yalnız IBM Plex Sans, Inter, Manrope.
- **Ayarın üründeki yeri:** sağ üstteki yuvarlak "SU" düğmesi → `Menu layout` (her kullanıcı kendi) ve `Font` (kurum geneli, admin).
- **Font check satırı:** fontun senin bilgisayarında gerçekten yüklenip yüklenmediğini ve Türkçe harflerini orada ölçer. "Not loaded" yazarsa gördüğün gerçek font değildir; bana söyle.

## Ölçtüm
- Fontları bu sefer gerçek dosyalarıyla yükledim (paket deposundaki Fontsource 5.3.0 kopyaları). Dört takımın hepsinde 23 Türkçe/Fransızca harf var.
- Inter, Manrope ve Space Grotesk'te rakamlar kendiliğinden eşit genişlikte değil; ayar açılınca eşit oluyor. Bu Claude Code için şart olarak blokta.
- 2.712 ekran durumu (3 kabuk × 4 font × 2 rakam biçimi × 43 sayfa, 1440 ve 1280): 0 hata, 0 taşma.
- 36 tıklama kontrolü geçti. Contracts'a 43 sayfanın her birinden: A 2 tık, B2 2 tık, B1 menüyle 2, kısayolla 1.

## Ölçemedim
- Google'ın font adresi Inter ve Manrope için yazı tipi tanımı döndürdü, yani bağlantılar çalışıyor. O yanıt kalın çeşitleri ve Türkçe harf bloğunu doğrulamadı; Google tarayıcıya göre farklı dosya verdiği için bunu ancak senin ekranındaki Font check satırı gösterir.
- Safari, Firefox, 1280'in altı ve telefon denenmedi.

**Düzeltme:** önceki blokta "29 sayfa" yazmıştım; doğrusu 43 (42 menü sayfası + Exhibitor detail). Aşağıdaki blok doğru sayıyı taşıyor.

## Sentez'e tek blok (13 Kas bloğunun yerine)

```
UX → SENTEZ — KABUK-2 TESLİM (GÜNCEL, 14 Kas): ÜÇ KABUK + FONT SEÇENEKLERİ
Bu blok 13 Kas teslim bloğunun yerine geçer.
Dosya: ELIZA-Kabuk-2-A-B-mockup.html (tek HTML; kabuk ve font anahtarı üstte).

SUER'İN HÜKMÜ (14 Kas)
- Tercihi A. Alışamayan olabilir diye düzeni HER KULLANICI kendi seçebilsin.
- Kendi B tarifi: üstte modüller (Sales · Operations · Finance · Admin),
  solda A'daki sayfa listesi. Mockup'ta adı "B2".
- "A, UX'in B'si (B1) ve benim B'm (B2) üçü de olsun; zorlaştırırsa A + B2."
- Font seçenekleri olsun: admin panelinden, kurum geneli.

UX DEĞERLENDİRMESİ (gerekçe; ölçüm değil — maliyeti CC ölçsün)
- A ↔ B2: aynı sol liste, aynı yol, aynı fuar seçici. Değişen yalnız dört
  modülün yeri. Tek kabuk + bir kullanıcı ayarı.
- B1: ayrı menü sistemi (açılır panel + sekme sırası + kısayollar). Seçenek
  olarak tutulursa her menü değişikliği iki kez yapılır ve denenir.
- Önerim: ürüne A + B2. B1 mockup'ta yalnız karşılaştırma için duruyor.
- SORU (CC ölçsün): B1'i üçüncü seçenek yapmanın ek maliyeti ne?
  Küçük çıkarsa Suer'in hükmüyle üçü; değilse A + B2.

ÜÇ KABUK — KISA GEREKÇE
A  (modüller solda)      Güçlü: modülün tüm sayfaları hep görünür.
                         Zayıf: 320 px genişlik alır (1280'de içerik 960 px).
                         Kime: çok ekran gezen, yeri ezberlememiş kullanıcı.
B2 (üstte modül, solda   Güçlü: modül seçimi üstte net; sayfalar yine hep
    sayfalar)            görünür; A'dan 76 px geniş içerik.
                         Zayıf: üstte iki sıra (102 px).
                         Kime: "sekme" alışkanlığı olan kullanıcı.
B1 (üstte modül, açılır  Güçlü: içerik tam genişlik; üç kısayol tek tık.
    menü)                Zayıf: menü tıklanana kadar gizli; ayrı sistem.
                         Kime: günü 2–3 ekranda geçen kullanıcı.

MOCKUP'TA NE VAR
- Üç kabuk, aynı 6 ekran, aynı veri; 42 menü sayfasının hepsi tıklanır.
- Ayarların yeri: hesap menüsü → "Menu layout" (her kullanıcı kendi) ve
  "Font" (kurum geneli, admin).
- Dört font takımı: bugünkü (Space Grotesk + IBM Plex) · yalnız IBM Plex
  Sans · Inter · Manrope. Rakamlar: mono ya da metinle aynı font.
- Üst şeritte "Font check": font o bilgisayarda yüklendi mi, Türkçe ve
  Fransızca harfler var mı, rakamlar eşit genişlikte mi — tarayıcıda ölçer.
- Ortak bileşen ölçeği (üç kabukta aynı): düğme 36 px ve üç kademe; kart ve
  tablo başlıkları normal yazı; tutar €100,793.00 · −€250.00 · kutuda €1.5M;
  tarih "17 May 2026"; yükleme gri iskelet; boş durum tek cümle + düğme;
  "Not connected yet" küçük gri işaret, kalkmıyor.

ÖLÇÜLDÜ (headless Chrome; fontlar Fontsource 5.3.0 kopyalarından yüklendi)
- Dört takımın hepsinde 23 Türkçe/Fransızca harf var.
- Inter, Manrope, Space Grotesk: rakamlar kendiliğinden eşit genişlikte
  DEĞİL; "eşit genişlikte rakam" ayarıyla eşit. IBM Plex Sans'ta zaten eşit.
- 2.712 ekran durumu (3 kabuk × 4 font × 2 rakam biçimi × 43 sayfa ×
  1440/1280): 0 script hatası, 0 taşma, 0 kesilmiş yol, 36 px altı düğme yok.
- Contracts'a 43 sayfanın her birinden: A 2 tık · B2 2 tık · B1 menüyle 2,
  kısayolla 1.
- İçerik genişliği 1280'de: A 960 px · B2 1036 px · B1 1280 px
  (A'da liste gizlenince 1204, B2'de 1280).
- Üstte kaplanan yükseklik: A 56 px · B2 102 px · B1 108 px.

CC İÇİN ŞARTLAR (font seçeneği yapılırsa)
- Yazı tipleri tek yerden yönetilir; ekranlarda sabit font adı kalmaz.
- Sayı yazan her yerde eşit genişlikte rakam ayarı açık olur
  (yoksa Inter ve Manrope'ta sütunlar kayar).
- Yalnız seçili font yüklenir.
- Her font için gerçek ekranlar 1280 ve 1440'ta kontrol edilir. Mockup'taki
  kontrol 6 ekran + yer tutucular içindir; gerçek ekranların yerine geçmez.

KARAR / CEVAP BEKLEYENLER
1. B1 üçüncü seçenek mi (yukarıdaki soru).
2. Yeni kullanıcının başlangıç düzeni. Varsayılanım: A (Suer'in tercihi).
3. Varsayılan font ve aday listesi: Suer mockup'ta bakıp söyleyecek.
4. Font ayarının kapsamı. Varsayılanım: iç ekranlar + Exhibitor Page uyar;
   PDF'ler ve e-postalar değişmez.
5. Önceki turdan açık üç soru (varsayılanlarım mockup'ta):
   "Contracts" kısayolu Owner'da Finance › Contracts'a gidiyor, Sales
   rolünde Sales › Contracts'a gitsin mi · Exhibitor detail yeni bileşen
   ölçeğini alsın mı · "Design preview" hesap menüsünün içinde mi kalsın.

ÖLÇÜLMEDİ / YOK
- Safari, Firefox; 1280'in altı; telefon.
- Rol farkı (menüde görünmeyen modüller).
- Google Fonts'un Suer'in tarayıcısına verdiği dosyalar; sayfadaki
  "Font check" orada ölçer.
- 6 ekranın içeriği ekran görüntülerinden yeniden kuruldu; rakamlar yer tutucu.
```

**Sıradaki tek adım:** dosyayı aç, B2'ye ve dört fonta bak; varsayılan fontu seç ve bu blokla birlikte Sentez'e ilet.
````
