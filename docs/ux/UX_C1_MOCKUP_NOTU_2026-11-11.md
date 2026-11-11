> **Arşiv notu (CC, 2026-11-11) — aşağıdaki metnin parçası DEĞİLDİR.**
> **Ne:** UX hattının C1 (Exhibitor Page) mockup'ıyla birlikte Sentez'e yazdığı not — varsayımlar / yeni sorular (11 Kas 2026). Orchestrator'ın 11 Kas 21:30 tarihli PAKET UI-TAM-2 bloğundaki kopya; çizginin altındaki metin **AYNEN** (oturum kaydından
> programla alındı). Düz metindir; satır yapısı korunsun diye kod çiti içinde verildi (çit metnin parçası değil).
> **Statü:** REFERANSTIR, **kriter DEĞİL** (kriter Sentez bloğu + EK-1 + EK-2 + EK-3 — [defter:2026-11-11 SENTEZ 11 Kas: PAKET UI-TAM-2]). Nasıl bakılır: EK-1 madde 3 (üstteki koyu şerit senaryo seçicidir; Scenario · Viewport · deep-link). 1–5'in hükmü = EK-1 madde 4.1–4.5 · 6–9 = EK-1'de "Varsayımlar KABUL".
> **Mockup dosyası:** `Exhibitor-Page-C1-mockup.html` — sha256 `1e98f0a2d03acf9fd3077e11de59701e5fd9f1c4a14bd94d80513ac35fd8d2a6` · 100.909 bayt · 1.179 satır. Dosya Suer'in bilgisayarında bulundu, özeti Orchestrator'ın ölçümüyle AYNI;
> **ell-docs'a KONMADI**: public repo taraması (YON-20) dosyada 11 eşleşme (10 e-posta adresi — hepsi `.example` alanında + 1 IBAN biçimli örnek dizgi) buluyor ve push'u engelliyor; dosya bayt bayt AYNEN girmek zorunda
> olduğundan değiştirilmedi, tarama kuralı da gevşetilmedi → 🔶 Sentez + kuyruk "mockup eklenecek" (`docs/UI_FAZI_TAKIP.md`).
> **Font / dış kaynak (EK-2 N1):** dosyanın 8–10. satırlarında Google Fonts'a 3 `<link>` var (2 preconnect + 1 stil dosyası); fetch / XHR / dış
> script YOK. Üründe anahtarlı sayfalar başka kökenden hiçbir şey yüklemez (kütük GUV-06) — bu satırlar ürüne TAŞINMAZ.
> Mockup'ın CSS'i / token'ları ve üstteki koyu senaryo şeridi de ürüne taşınmaz (ui2 `tokens.css` + `components.js`).

---

```
(1–5'in hükmü = EK-1 madde 4.1–4.5 · 6–9 = EK-1'de "Varsayımlar KABUL")
UX → SENTEZ — C1 MOCKUP: VARSAYIMLAR / YENİ SORULAR (11 Kas)
Mockup aşağıdaki varsayımlarla duruyor; yanlış olanı söyleyin, düzeltirim.

KARAR GEREKENLER
1. Space-only + stand deadline geçti: bölüm AÇIK kalıyor, etiket "Overdue".
   (Cevap 6 yalnız Equipped'i kapsıyor.) Doğru mu?
2. Catalogue zorunlu alanları cevap 7'ye harfiyen uygulandı: address line 2,
   mobile, website, logo ve 3 ürün fotoğrafı da zorunlu. Böyle mi kalsın?
3. Catalogue deadline geçti + gönderilmedi = kilitli; exhibitor yalnız project
   team'e yazabiliyor. Deadline sonrası "Changes requested" bölümü o exhibitor
   için yeniden açıyor (mockup: "Reopened until 30 Apr 2027").
   Yeniden açma kimin eylemi, süre nereden gelir?
4. Gönderilmiş/onaylı catalogue deadline'a kadar düzenlenebilir; düzenlenince
   yeniden "in review". Deadline sonrası kilitli. Doğru mu?
5. Equipped stand onaylandıktan sonra exhibitor kendisi değiştiremez;
   deadline'a kadar "Request a change" ile project team'e yazar. Doğru mu?

VARSAYDIM (itiraz yoksa kalır)
6. Üst başlıkta expo kimliği var; ELIZA yalnız altta "Powered by ELIZA".
7. Payment bölümü ana kontrat + extra equipment kontratlarını tek özet
   tabloda gösterir; dekont formu hangi kontrat olduğunu sorar.
   Kod girilmeden hiçbir tutar görünmez (durum şeridi dahil).
8. Geçersiz link sayfası adresin kayıtlı olup olmadığını söylemez
   ("If this address is registered…").
9. Equipped paket mockup'ta +12 m² adımıyla hesaplanıyor
   (24 m² → 2 table · 6 chairs). Gerçek kural expo ayarındaki tablodan.

BU DOSYADA YOK
10. Pavilion görünümleri (DIRECT dar link / VIA AGENCY liste).
11. FR ve TR içerik: dil düğmesi var, metin yalnız EN.

UYDURMA ÖRNEK DEĞERLER (karar değil)
Fascia sınırı 24 karakter · ürün fiyatları · m² fiyatı · 30/70 ödeme planı ·
badge masası saatleri · build-up saatleri.
```
