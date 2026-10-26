# ELIZA + LIFFY Kullanım Kılavuzu v1 (TASLAK)

> 26 Ekim 2026, Paket 3 canlıya geçişi. Kaynak: [defter:2026-10-26 PAKET 3 CANLIDA]. Kuralların kendisi kütükte (KAT, TAH,
> LED, SEM grupları). Ekran adları uygulamadaki İngilizce etiketlerle yazıldı. Bu bir taslak: cila ve ekran görüntüleri sonra
> eklenecek.

**Akış tek cümlede:** Fuar ELIZA'da (LEENA) açılır → proje ekibi fuarı LIFFY'ye yayınlar → satışçı LIFFY'de quote hazırlar,
gönderir ve imzalatır → kontrat ELIZA'da kendiliğinden oluşur → Finans oranı, ödemeyi ve hesabı yönetir.

---

## 1. Proje ekibi: fuarı satışa açmak

1. Fuarlar yalnız ELIZA'da açılır; LIFFY'de fuar oluşturulamaz, düzenlenemez, silinemez (KAT-03).
2. Fuarı yayınlamak için: **ui2 → Admin › Organization › Expos → LIFFY**, ilgili satırda **Publish to LIFFY**. Satırda
   `published` görünür. LIFFY yalnız yayınlanmış fuarları görür.
3. Fuarı yayından kaldırmak için aynı ekranda **Unpublish**. Fuar bir sonraki senkronda LIFFY'de pasifleşir. Var olan
   quote'lar ve kontratlar bundan etkilenmez.
4. **Yetki:** ekran `expo_publish.write` izniyle açılır. Owner her zaman görür. Proje ekibinden birine Owner şöyle verir:
   **Admin › Users** → kişi → *Role & permissions* → **Per-user override** → `expo_publish.write` → **Save overrides**.
5. Gelen kontratları izlemek için: **Sales › Handoff › Convert queue** (Project rolünde bu izin var). Okuma rehberi §3.3'te.

## 2. Satışçı: LIFFY'de quote'tan kontrata

1. **liffy.app → Quotes → New Quote.** Fuar listesinde ELIZA'nın yayınladığı fuarlar çıkar. Liste 10 dakikadan eskiyse form
   açılırken kendiliğinden tazelenir; satışçının Sync'e basması gerekmez. Sync düğmesi yalnız owner ve admin'de vardır.
2. **Ofis:** kendi ofisin varsayılan olarak gelir. Kullanıcına ofis atanmamışsa formda sarı bir uyarı görürsün. O durumda
   quote'un ofisini kendin seç ve yöneticinden **Products & Pricing › Users & Offices** ekranında sana ofis atamasını iste.
3. **Kalemler:** ürünler katalogdan seçilir. Fiyatı olmayan ürün quote'a eklenemez. RF (kayıt ücreti) ürünleri işaretlidir.
   Vergi oranı her satırda ayrı tutulur. Ekrandaki toplam, ELIZA'daki kontrat brütüyle birebir aynıdır (iki sistem aynı
   kuralı kullanıyor, TAH-05).
4. Sıra şöyle: **Create → Send → Sign.** İmza adımında imza tarihi ve **Signed Scan URL** istenir.
   *Şimdilik bu alan zorunlu.* Zorunluluk kaldırılacak (Suer kararı, kod henüz değişmedi). Tarama yoksa staging testindeki
   gibi `*` yazılabilir.
5. İmzadan sonra quote detayındaki **Convert to ELIZA** kartına bak:

   | Görünen | Anlamı | Ne yapılır |
   |---|---|---|
   | **Converted · Contract #N** | Kontrat ELIZA'da oluştu | Bir şey yapılmaz |
   | **Convert pending** / **Sending…** | Gönderim sürüyor; sistem 1, 2, 4 ve 8 dakika arayla en çok 5 kez dener | Bekle |
   | **Convert failed** + hata kodu | ELIZA isteği reddetti ya da denemeler bitti | Sorunu düzelttir, sonra **Resend** |

   Sık görülen hata kodları:
   - `EXPO_NOT_PUBLISHED`: fuar yayından kaldırılmış (proje ekibine haber ver).
   - `OFFICE_UNKNOWN`: ofis ELIZA'da aktif değil.
   - `NO_LINE_ITEMS`: quote'ta kalem yok.
   - `NOT_CONFIGURED`: entegrasyon kapalı (teknik ekibe haber ver).

   Resend düğmesi yalnız *failed* ve *pending* durumunda çıkar. Aynı quote ikinci kez gönderilse bile ELIZA ikinci bir
   kontrat açmaz.
6. Quotes listesinin üstündeki **Converted / Failed / Pending** sayaçlarına tıklayınca liste o duruma göre süzülür.
7. Quote gönderildikten sonra konu ve kalemler kilitlenir. İmzalı quote silinemez.

## 3. Finans

### 3.1 SR oranı

- Convert, kontrata SR'ı (satış temsilcisi) yazar ama **oranı yazmaz**. Oran boş kalınca motor temsilcinin varsayılan oranını
  ("Comm %") kullanır. Varsayılan 0 ise komisyon %0 görünür. Staging'deki ilk kontrat bu yüzden %0 çıktı.
- **Oranı Finans girer.** İki yol var:
  - **Temsilcinin varsayılanı:** klasik **Sales Agents** ekranında "Comm %". ui2'de Finance › Contracts › Agents yer tutucu
    sayfası bu ekrana götürür.
  - **Bu kontrata özel oran:** klasik kontrat detayında (`contract-detail.html`) komisyon atama bölümü (Agent / SR / SD) →
    SR satırına oranı yaz → kaydet. Alan boş bırakılırsa varsayılan geçerli olur.
  - Kurallar: Agent ile SR aynı anda olamaz; SD yalnız SR varken atanabilir.
- **"needs agent"** etiketi: LIFFY'deki satış sahibinin e-postası ELIZA'da tek bir aktif iç temsilciyle eşleşmediyse kontrat
  SR'sız oluşur. Aynı atama bölümünden SR atanınca etiket kalkar.

### 3.2 Hesap ve yöntem ne demek

- **Hesap (account):** para hesabıdır; türü `bank`, `cash` ya da `virtual` olur. Sahibin cari hesabı sanal bir "owner"
  hesabıdır. Zoho'daki "Account" ELIZA'da **firma (company)** demektir, hesap değil (LED-03, LED-07).
- Bir hesabın para birimi sabittir; hareketler o birimle girilir. Para birimi çevirmek, hesaplar arası transfer yapmak
  demektir (LED-11).
- Ödeme girerken hesap seçilmezse ofisin o para birimindeki varsayılan hesabı kullanılır. O da yoksa ödeme hesapsız
  kaydedilir ve uyarı görünür (LED-12).
- **Yöntem (method):** beş değerden biridir. `bank_transfer` (SWIFT dahil) · `cash` · `cheque` · `credit_card` · `other`.
  "Kredi bakiyesi" bir yöntem değildir (SEM-01, LED-01).
- Kayıtlar silinmez ve değiştirilmez; düzeltme ters kayıtla yapılır (LED-05, LED-08).
- **Gelir brüttür** (vergi dahil); kontrattaki *Revenue* brüt tutardır. **Komisyon matrahı ise nettir ve RF hariçtir.**
  Örnek, staging kontrat #5: net 4220.00 + vergi 844.00 = brüt 5064.00; matrah 3870.00 (TAH-05).

### 3.3 Convert queue nasıl okunur (Sales › Handoff › Convert queue)

- Ekran yalnız **ELIZA'ya ulaşan** istekleri gösterir. İmzalanıp hiç ulaşmamış quote'lar LIFFY'deki sayaçlarda görünür
  (KAT-04).
- Özet kartlar:
  - **Converted:** kontrat oluştu.
  - **Failed:** son deneme reddedildi; sebebi *Last error* sütununda.
  - **No outcome yet:** istek ulaştı ama sonuç yazılmadı (ya sürüyor ya yarıda kesildi).
  - **Needs agent:** SR'sız kontrat; §3.1'deki gibi SR ata.
- Sütunlar: Quote (AF numarası ve quote kimliği) · Office · State · Attempts · Last error · Contract · Last event (saat UTC).

---

**Açık işler (bu taslağı değiştirecek):** imzada tarama zorunluluğunun kalkması (LIFFY kodu) · Agents / Commissions ekranlarının
ui2 karşılığı (UI-1) · Expenses / Drafts formunda kategori ve tipin iki ayrı kutu olması (UI-1).
