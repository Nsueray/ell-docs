# DENEME-0 Kılavuzu v1: LIFFY'de teklif → ELIZA'da kontrat (STAGING)

> 4 Kasım 2026. Kaynak: [defter:2026-11-04 SENTEZ: DENEME-0 + LIFFY STAGING] ve `docs/KULLANIM_KILAVUZU_v1.md` §2 + §3.3 (aynı
> akış, deneme ortamına uyarlandı). Kişisel veri, adres değeri ya da şifre içermez. Ekran adları uygulamadaki İngilizce
> etiketlerdir.

## 0. Bu ortam DENEME

- **Burası deneme (staging) ortamıdır. Gerçek tek kaynak Zoho'dur.** Burada girilen hiçbir şey sayılmaz ve ortam tazelenince
  silinir (YON-14).
- LIFFY ekranının üst çubuğunda kırmızı **STAGING** etiketi görünür. Etiket yoksa yanlış adrestesin: dur ve Suer'e haber ver.
- Canlı adreslere (liffy.app, leena.app) bu deneme için **girme**.
- **Gerçek firma ya da kişi adı yazma.** "Deneme Firma A" gibi uydurma adlar kullan.
- Kapsam yalnız **kontrattır**: teklif, gönderim ve imza. Ödeme ya da gider girişi bu denemede yok.

## 1. Giriş

| Sistem | Adres | Giriş |
|---|---|---|
| **LIFFY (staging)** | Suer'in ilettiği `liffy-ui-staging` adresi | E-posta + Suer'in verdiği geçici şifre |
| **ELIZA (staging)** | `leena-staging.onrender.com/ui2/` | Suer'in ilettiği davet bağlantısı → şifreni belirle → giriş |

Şifreleri kimseyle paylaşma. Sorun olursa Suer'e yaz.

## 2. LIFFY'de teklif: Create → Send → Sign

1. **Quotes → New Quote.**
2. **Fuar:** `DENEME 2026`. Listede başka fuar da çıkabilir; yalnız `DENEME 2026`'yı seç.
3. **Ofis:** senin ofisin (Turkey) kendiliğinden gelir. Sarı "ofis yok" uyarısı görürsen dur ve Suer'e haber ver.
4. **Firma adı:** uydurma bir ad.
5. **Kalemler:** ürünü katalogdan seç, miktarı yaz. Fiyatı olmayan ürün eklenemez; başka ürün seç. Ekrandaki toplam,
   ELIZA'daki kontrat brütüyle aynıdır.
6. **Create**, ardından **Send**. Send müşteriye e-posta göndermez, yalnız durumu "sent" yapar. Gönderilen teklifin
   kalemleri kilitlenir.
7. **Sign:** imza tarihini gir. **Signed Scan URL boş kalabilir** (bu denemede tarama yok).
8. İmzadan sonra quote detayındaki **Convert to ELIZA** kartına bak:

   | Görünen | Anlamı | Ne yapılır |
   |---|---|---|
   | **Converted · Contract #N** | Kontrat ELIZA'da oluştu | 3. adıma geç |
   | **Convert pending** / **Sending…** | Gönderim sürüyor (1, 2, 4, 8 dk arayla en çok 5 deneme) | Bekle |
   | **Convert failed** + kod | ELIZA reddetti ya da denemeler bitti | Ekran görüntüsü al, 5. adım. **Resend**'e Suer'e sormadan basma |

## 3. ELIZA'da kontratı görmek

1. ELIZA staging → **Finance › Contracts**.
2. Kontratı LIFFY'deki **A** ile başlayan numarayla ya da firma adıyla bul (en yeni kontrat listenin başındadır).
3. Satıra tıklayınca detay açılır. Brüt tutar LIFFY'deki toplamla aynı olmalı. Farklıysa ekran görüntüsü al.
4. **"needs agent"** etiketi bu denemede **beklenir**: kontrat satış temsilcisi atanmadan doğar. Atama senin işin değil.

## 4. Convert kuyruğu (yalnız izlemek için)

- **LIFFY:** Quotes listesinin üstündeki **Converted / Failed / Pending** sayaçları. Tıklayınca liste süzülür.
- **ELIZA:** **Sales › Handoff › Convert queue**. Yalnız ELIZA'ya *ulaşan* istekleri gösterir. Sütunlar: Quote · Office ·
  State · Attempts · Last error · Contract · Last event (UTC). Bu ekran sende görünmüyorsa sorun değil, Suer bakar.

## 5. Hata bildirimi

Bir şey beklenenden farklıysa:

1. **Ekran görüntüsü** al (hata kodu ya da mesaj görünsün).
2. **Ne yaptığını** adım adım yaz (hangi ekran, hangi düğme), yaklaşık saatiyle birlikte.
3. İkisini **Suer'e** gönder. Suer bunları deftere işlenmek üzere Orchestrator'a iletir.

Hatayı kendin düzeltmeye çalışma, aynı adımı tekrar tekrar deneme. Her bildirim üç sınıftan birine girer: **ürün hatası**,
**kılavuz eksiği** ya da **eğitim**. Sınıflamayı Suer yapar.

## 6. Denemenin bitişi (kabul)

- Uçtan uca **3 kontrat**: LIFFY'de Create → Send → Sign → **Converted**, ve her biri ELIZA'da **Finance › Contracts**'ta
  görünür.
- Hata listesi deftere yazılır. Paket 5 ve UI-1 bu listeden beslenir.
