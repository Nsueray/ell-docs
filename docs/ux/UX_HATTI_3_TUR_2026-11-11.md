> **Arşiv notu (CC, 2026-11-11) — aşağıdaki metnin parçası DEĞİLDİR.**
> **Ne:** UX hattının 3. tur çıktısı (11 Kas 2026): Exhibitor Page + project team ekranları (C1–C6 + Sentez'e 15 soru). Orchestrator'ın
> 11 Kas 21:30 tarihli PAKET UI-TAM-2 bloğundaki kopya; çizginin altındaki metin o bloktaki haliyle **AYNEN** (oturum kaydından programla
> alındı, elle yazılmadı; metin zaten Markdown — hiçbir yapı eklenmedi).
> **Statü:** EKRAN TARİFİDİR; **kriter Sentez bloğu + EK-1 + EK-2 + EK-3** (defterde AYNEN — [defter:2026-11-11 SENTEZ 11 Kas: PAKET UI-TAM-2]; kütük EXH-01…20). Çelişkide kriter
> kazanır: örn. stand no "floor plan'dan seçim" UYGULANMAZ (EK-3 F1 — elle metin) · "Place order" kodludur (C1) · catalogue zorunlu kümesi EK-1 4.2 ·
> sondaki 15 "karar gerektiren"in hükümleri Sentez bloğu C'de. "Zorunlu" sütunları ve sayılar UX'in ÖNERİSİDİR (metnin kendi okuma notu).
> **İlgili:** 2. tur `UX_HATTI_2_TUR_2026-11-11.md` (kriter değil; öncelik Sentez bloğu > 3. tur > 2. tur) · mockup notları
> `UX_C1_MOCKUP_NOTU_2026-11-11.md` · `UX_C2_C3_MOCKUP_NOTU_2026-11-11.md`. Tarihseldir (YON-01): ölçüm tarihi 11 Kas 2026.

---

**UX HATTI — 3. TUR ÇIKTISI (11 Kas) · Exhibitor Page + project team ekranları**

**Okuma notu**
- Staging'i (ui2) görmedim. Teklif, kontrat, müşteri ve rapor ekranlarına dokunmadım.
- A ve B maddelerini verili aldım. Zoho'daki formu, stand onay PDF'ini ve e-posta metinlerini kendim görmedim.
- "Zorunlu" sütunları ve sayılar (kod süresi, karakter sınırı gibi) önerimdir, karar değildir.
- Tutar ve bakiye alanları sunucudan gelir; hesap tarif etmedim.
- Durum adları (ekranda İngilizce): To do = bekliyor · Overdue = deadline geçti · Done = tamam · In review = bizde, inceleniyor.

---

## C1 — Exhibitor Page (müşteri yüzü)

**Amaç:** exhibitor'ın imzadan fuar gününe kadar yapacağı her şey tek linkte.
**Kim:** exhibitor'ın yetkilisi ve linki ilettiği kişiler (ör. müteahhit). Project team "Open as exhibitor" ile aynısını görür.

### Çerçeve

| Parça | Tarif |
|---|---|
| Başlık | expo adı · tarih · mekân · firma · stand no / m² / tip · fuara kalan gün · dil (EN/FR/TR) · "Help" (Contacts'a iner). Stand no atanmadıysa "to be confirmed" |
| Durum şeridi | bölüm başına tek çip: To do + kalan gün · Overdue · Done ("in review" ya da "approved" alt yazısıyla). Görevi olmayan bölümde çip yok. Şerit hep görünür; çipe dokun → bölüme iner |
| "Next step" satırı | şeridin altında tek cümle: en yakın deadline'lı eksik bölüm + düğme |
| Bölüm sırası | Stand · Extra equipment · Catalogue · Badges · Payment · Build-up rules & documents · Contacts. Sıra hiç değişmez |
| Deep-link | her e-posta aynı link + bölüm adı. Sayfa o bölümde açılır; o bölüm açık, diğerleri kapalı. Bölüm adı yoksa ilk eksik bölüm. Welcome → Contacts. Payment → önce kod adımı |
| Gelecek (A1) | "Leads" ve "Meetings" bölümlerinin yeri Badges'ten sonra; bugün görünmez |

**Sıra için iki yol**
- Yol A: işler üstte, bilgi altta (tablodaki).
- Yol B: e-posta sırası, Contacts en üstte.
- Tercihim A. Müşteri sayfaya çoğunlukla bir hatırlatmadan dönüyor; işi üstte bulmalı. Contacts'a "Help" ile tek dokunuşta inilir.

Aşağıdaki tablolarda "sistem" yazmayan her alanı exhibitor doldurur. Project team hepsini görür ve "adına gir" ile doldurabilir (C3).

### Stand — EQUIPPED

| Alan | Tür | Zorunlu | Not |
|---|---|---|---|
| Stand özeti (no · m² · açık kenarlar) | salt okunur, sistem | — | kontrat + floor plan |
| Fascia name | metin, karakter sayacı | Evet | varsayılan: katalogdaki ad |
| Included equipment | salt okunur liste (kalem · adet), sistem | — | masa · sandalye · halı · spot · priz · çöp kovası · 3 kW; kaynak expo ayarı |
| Layout | not + işaretli çizim yükleme | Hayır | iki yol aşağıda |
| Panel printing | adet + baskı görseli | Hayır | ücretli; Extra equipment sepetine kalem olarak düşer (tek sipariş yolu) |
| Approved by (ad soyad) | metin | Evet | |
| "I approve" | onay + düğme | Evet | tarih-saat kayıtlı |
| Signed PDF | dosya | Hayır | |

### Stand — SPACE-ONLY

| Alan | Tür | Zorunlu | Not |
|---|---|---|---|
| 3D design | dosya (görsel/PDF), birden çok | Evet | |
| Technical drawing | dosya (PDF/DWG) | Evet | |
| Dimensions (en · boy · yükseklik) | sayı, metre | Evet | yükseklik expo'daki üst sınırı aşarsa uyarı; gönderilir, incelemede işaretli gelir |
| Contractor (firma · kişi · telefon · e-posta) | metin | Evet | |
| Note | metin | Hayır | |
| "Submit for approval" | düğme | — | her gönderim yeni sürüm |

**Stand durumları**
- Equipped: Not started → Approved. Sonradan "Request a change" (not) → project team "Reopen" → yeniden Not started. Onaysız deadline → Overdue.
- Space-only: Not started → Submitted (In review) → Approved ya da Changes requested (yorum) → yeniden Submitted. Onaydan sonra yeni dosya = yeni sürüm, yeniden inceleme.
- Kontratta stand tipi boşsa: bölümde "Your stand details are being prepared" yazar ve Stand e-postası gitmez.

**Layout için iki yol**
- Yol A: not + şablonu indir, işaretle, yükle.
- Yol B: ekranda ızgara; kareye dokun, dahil ekipmandan seç.
- Tercihim A. Alan isteğe bağlı ve telefonda ızgara zor. B'nin değeri stand firmasına tek tip çıktı vermesi.

### Extra equipment

| Parça | Tür | Zorunlu | Not |
|---|---|---|---|
| "Already included" | salt okunur, sistem | — | Equipped'da dahil ekipman; çift siparişi önler |
| Price note | bilgi şeridi, sistem | — | "Pre-show prices until {tarih}. After that: on-site price (+100%)" |
| Product list | kategorili kartlar: ad · foto · birim fiyat · adet seçici | — | expo'nun ürün/fiyat listesi (B4 kalemleri) |
| Basket | kalem · adet · satır tutarı · toplam | en az 1 kalem | para birimi kontratınki |
| Ordered by (ad soyad) | metin | Evet | |
| Note | metin | Hayır | |
| "Place order" | düğme → özet + "bu bağlayıcı bir sipariştir" onayı | Evet | sipariş = ana kontrata bağlı yeni kontrat (A4) |
| My orders | liste: kontrat no · tarih · kalemler · tutar · durum | — | Placed · Delivered; ödeme durumu Payment bölümünde |

- Durumlar: sipariş yok ("Optional", hatırlatma yok) → Order placed → Delivered.
- Değişiklik ya da iptal: "Request a change" notu project team'e düşer; kontrattaki mevcut iptal eylemiyle çözülür.
- Fiyat listesi boşsa: "Price list will be available soon".

### Catalogue (A9)

| Grup | Alanlar | Tür | Zorunlu (öneri) |
|---|---|---|---|
| Firma | firma adı (kontrattan, salt okunur) · katalogdaki ad | metin | katalogdaki ad |
| İçerik | markalar · ürün grupları · firma profili | metin · uzun metin (karakter sayacı) | ürün grupları, profil |
| Ana kişi | unvan · ad · soyad · görevi | seçim + metin | ad, soyad |
| İletişim | web · telefon · mobil · e-posta | adres / telefon / e-posta | telefon, e-posta |
| Adres | sokak · satır 2 · şehir · ülke | metin + ülke listesi | sokak, şehir, ülke |
| Görsel | logo · ürün fotoğrafı ×3 | dosya; düşük çözünürlükte uyarı | logo |
| Sosyal | Facebook · LinkedIn · Instagram · diğer | adres | — |

- Ön doldurma: firma kaydından adres, telefon, web. Önceki edisyonda kaydı varsa "Copy from last edition".
- Düğmeler: Save draft (kendiliğinden de kaydeder) · Preview · Submit · Edit (deadline'a kadar).
- Durumlar: Not started → Draft → Submitted (In review) → Approved ya da Changes requested (yorum) → yeniden Submitted. Approved sonrası düzeltme yeniden incelemeye düşer.
- Deadline: bölüm kilitlenir (Locked). Project team tek exhibitor için "Reopen until {tarih}" açar.
- Uyarı metni: "These details will be printed and published."

### Badges (A6)

| Parça | Tür | Zorunlu | Not |
|---|---|---|---|
| Team list | tablo: ad soyad · görev · e-posta (maskeli) · durum | — | Registered · QR sent · Printed |
| "Add person" | form: ad · soyad · e-posta · görev · mobil | ad, soyad, e-posta | kişi QR'ı kendi e-postasına alır |
| Team registration link | kopyalanan link | — | kişi kendini kaydeder; kayıt kontrata bağlanır |
| Satır eylemi | Resend QR · Remove | — | Remove basılmadan önce |
| Bilgi | kayıt masası yeri + build-up günleri, sistem | — | expo ayarından |

- Durum: 0 kişi = To do; en az 1 kişi = Done. Limit yok.

### Payment (kodla açılır)

| Parça | Tür | Zorunlu | Not |
|---|---|---|---|
| Kilit ekranı | "Send code" → kayıtlı e-postalardan biri seçilir (maskeli) | — | akış aşağıda |
| Özet | kontrat başına toplam · ödenen · bakiye | — | salt okunur, sunucudan; ana kontrat ve extra equipment kontratları ayrı satır |
| Vade planı | satırlar: vade · tutar · durum | — | salt okunur |
| Banka bilgisi | satıcı tüzel kişi: hesap adı · banka · IBAN · SWIFT · para birimi | — | "kopyala" düğmesi · banka masrafı notu · açıklamaya yazılacak kontrat no |
| "I paid — upload receipt" | form: kontrat · tutar · tarih · ödeyen firma (farklıysa) · dekont | tutar, tarih, dekont | Finance'a bildirim gider; bakiye değişmez |
| My notices | liste: tarih · tutar · durum | — | Sent · Confirmed |

- Durumlar: Balance due → dekont yüklendi ("Receipt received — being checked") → Paid (Finance ödemeyi kaydedince, veriden). Vade geçtiyse Overdue.

### Build-up rules & documents · Contacts

| Bölüm | İçerik | Kaynak |
|---|---|---|
| Build-up | kendi stand türünün programı üstte, diğeri kapalı · yükleme kuralları · ülke notu (+görsel) · açılış saatleri · söküm | expo ayarı, kişinin dilinde |
| Documents | exhibitor manual · stand çizimi şablonu · diğer dosyalar | expo ayarı |
| Contacts | HQ · local office · travel · forwarder · contractor · visa: firma · kişi · telefon · e-posta. Boş rol görünmez | expo ortak tablosu |

### Boş / hata / kilitli durumlar

| Durum | Sayfada görünen |
|---|---|
| Link geçersiz ya da yenilenmiş | sade sayfa: project team kişisi + "Send me a new link" (e-posta kontrattaki kişiyle eşleşirse yeni link gider) |
| Kontrat iptal | sayfa salt okunur + "participation cancelled" + kişi |
| Bölüm hazır değil (stand tipi boş · fiyat listesi boş · metin girilmemiş) | "Not available yet — we will e-mail you" |
| Deadline geçti, bölüm kilitli | gönderilen içerik salt okunur + "Ask the project team to reopen" |
| Dosya büyük · türü yanlış · bağlantı koptu | alanın yanında hata; taslak kaybolmaz |
| Kod yanlış ya da süresi doldu | yeniden gönder; 5 yanlışta 15 dk bekleme |
| Fuar bitti | sayfa salt okunur arşiv |

### Telefon görünümü
- Tek sütun; bölümler açılır-kapanır, aynı anda biri açık.
- Durum şeridi yana kayan çipler.
- Altta sabit ana düğme (Save draft / Submit / Place order).
- Catalogue 4 adım: Firma · Kişi ve adres · Görseller · Sosyal.
- Dosya yüklemede kamera ve galeri. Sepet alttan açılan panel.

### Link paylaşımı ve kod akışı

| Konu | Tarif |
|---|---|
| Kodsuz | durum görme · Contacts · Build-up · Catalogue · Stand yükleme ve onay · Badges'e kişi ekleme |
| Kodlu | Payment (A2). Önerim: "Place order" da |
| Akış | "Send code" → kayıtlı e-posta seçilir → 6 haneli kod, 10 dk geçerli → bu tarayıcıda 24 saat açık |
| E-postası listede olmayan | kod alamaz; project team kişiyi C3'te ekler |
| İz | her gönderimde yazılan ad + tarih-saat; kodlu eylemde doğrulanmış e-posta |
| Link yenileme | project team "Regenerate link" der, eski link ölür |
| Diğer | sayfa arama motorlarına kapalı; Badges'te e-postalar maskeli |

**Riskler (C1)**
- Linki müteahhide iletmek meşru bir kullanım; aynı linkle sipariş de verilebilir. Bu yüzden sipariş kodlu olmalı.
- Sipariş = kontrat: üç küçük sipariş üç kontrat ve üç ödeme takibi demek.
- Catalogue'daki mobil ve e-posta yayımlanır; uyarı metni şart.
- Pavyon kontratında tek sayfa yetmez (karar 11).

---

## C3 — Exhibitor detail (project team yüzü)

**Amaç:** bir exhibitor'ın tüm durumu ve inceleme eylemleri tek sayfada.
**Kim:** project team yazar; Finance ve Owner görür; satışçı kendi kapsamında salt okur.

| Blok | İçerik | Eylemler |
|---|---|---|
| Başlık | firma · expo · stand no / m² / tip · kontrat no · satışçı · dil · ödeme uyarı rozeti (A3) · "sayfa son açılış" tarihi | Open as exhibitor · Copy link · Send link · Regenerate link · ⋯ (beklet / aktar / iptal — mevcut) |
| Durum şeridi | Exhibitor Page ile aynı bileşen; "In review" olanlar "bizde bekliyor" diye vurgulu | çipe tıkla → karta in |
| Stand kartı | Equipped: fascia · panel adedi · layout notu/dosyası · onaylayan + tarih · signed PDF. Space-only: dosya sürümleri · ölçüler (üst sınır işareti) · contractor | Equipped: Remind · Reopen · Enter on behalf · Stand sheet (stand firmasına döküm). Space-only: Approve · Request changes (yorum) · Remind |
| Orders kartı | bağlı extra equipment kontratları: no · tarih · kalem özeti · tutar · ödeme durumu · teslim | New order on behalf · Open contract · Mark delivered |
| Catalogue kartı | durum · gönderilen içeriğin önizlemesi · son sürümden farklar | Approve · Request changes (alan bazlı yorum) · Remind · Reopen until… · Edit on behalf |
| Badges kartı | kişi listesi · durum · sayı | Add person · Resend QR · Remove · Remind |
| Payment kartı | bakiye özeti (sunucudan) · vade · exhibitor'ın yüklediği dekont bildirimleri | Open contract (mevcut Finance ekranı) · Remind |
| E-mail chain kartı | 6 satır (aşağıda) | Send all now |
| Operations bilgileri | alanlar (aşağıda) | Edit |
| Sekmeler | Overview · Correspondence · History | — |

### E-mail chain kartı

| Sütun | İçerik |
|---|---|
| E-mail | Welcome · Stand (Equipped ya da Space-only) · Catalogue · Build-up & Breakdown · Payment Reminder · Badge |
| Planned | tarih; expo ayarından türetilir |
| Last sent | tarih · kime · hangi dilde |
| Result | Sent · Failed (neden) |
| Reminders | kaç kez gitti · sıradaki tarih |
| Job done? | Stand, Catalogue, Badge: bölüm Done mı · Payment Reminder: bakiye sıfır mı · Welcome ve Build-up: tek seferlik, yok |
| Eylem | Send now / Resend · Exclude (not zorunlu) / Include · View (giden metnin aynısı) |

- Satır durumları: Planned → Sent → Reminding → Stopped (iş bitti) · Failed · Blocked · Excluded · Paused (kontrat beklemede).
- Blocked nedenleri: stand tipi boş · kişinin e-postası yok · expo metni ya da deadline eksik · dil sürümü eksik.
- "Send all now": önce alıcı ve e-posta listesi önizlenir, sonra gider.
- Kutucuk ve etiket yok; her şey olay kaydından (B2).

### Operations bilgileri

| Alan | Tür | Zorunlu | Not |
|---|---|---|---|
| Stand type | seçim: Equipped / Space-only | Evet | boşsa Stand bölümü ve e-postası Blocked |
| Stand no | floor plan'dan seçim | Hayır | atanana dek "to be confirmed" |
| m² · free m² · total m² | sayı | m² kontrattan | total türetilir |
| Sales group | seçim | Evet | |
| Transportation | Included / Excluded | Evet | |
| Catalogue page | sayı | Hayır | katalog dizilince |
| Links | scan link · stand design link | Hayır | eski Drive linkleri |
| E-posta dili + alıcılar | seçim + kişi listesi (alıcı / bilgi) | en az 1 alıcı | ödeme kodunu alabilecek kişiler de burası |
| Co-exhibitors | alt liste | — | pavyon (karar 11) |

**Sekmeler**
- Correspondence: sistemin gönderdiği her e-postanın giden hali + exhibitor'ın sayfada yazdığı talepler + project team notları. Gelen cevaplar Gmail kararına bağlı.
- History: kim, ne zaman, ne yaptı (onay, yeniden açma, adına giriş, hariç tutma).

**Uyarı şeritleri**
- Stand type boş: "Stand type seçilmeden Stand e-postası gitmez".
- E-posta geri döndü: "Primary contact e-postası geri döndü" + "Edit recipients".
- Sayfa hiç açılmadı: "Not opened yet".

**Telefon:** başlık + uyarılar üstte, kartlar kapalı. Fuar günü için hızlı eylemler: Mark delivered · Add person · kişiyi ara.

**Riskler (C3)**
- "Enter on behalf" hataya açık; not zorunlu olmalı ve History'ye düşmeli.
- Payment kartı yalnız özet olmalı; ikinci bir ödeme ekranına dönüşmemeli.

---

## C2 — Operations › Exhibitors (liste)

**Amaç:** kim nerede takıldı, bugün kimi kovalayacağım, bende ne bekliyor.
**Kim:** project team; yerel ofis kendi expo'ları.

| Sütun | İçerik |
|---|---|
| Seçim | toplu eylem için kutu |
| Exhibitor | ad · ülke · alt satır: satışçı · varsa "Pavilion: {agent}" etiketi |
| Stand | no · m² · Equipped / Space-only |
| Catalogue | çip + sayaç: "To do · 12d" · "Overdue · 3d" · "In review" · "Approved" |
| Stand | aynı düzen |
| Orders | "—" · "2 orders" · "1 undelivered" (görev değil) |
| Badges | kişi sayısı; deadline yaklaşırken 0 ise uyarılı |
| Payment | Paid · Balance due · Overdue rozeti (A3). Tutar listede yok |
| Chain | yalnız sorun varsa işaret (Failed / Blocked) |
| ⋯ | Open · Remind · Copy link |

| Parça | Tarif |
|---|---|
| Deadline sayaçları (üstte) | Catalogue "12 days · 26 missing" · Stand · Orders ("pre-show price ends in 20 days") · Badges ("58 with 0 badges") · Payment ("14 overdue"). Tıkla → liste süzülür |
| Hazır görünümler | All · Stuck (exhibitor'da bekleyen) · Waiting for us (incelenecek) · Payment warning · Fair days |
| "Stuck" tanımı (öneri) | bir bölüm Overdue · ya da deadline'a N gün kala To do · ya da "Changes requested" N gündür cevapsız · ya da chain Failed/Blocked |
| Süzgeçler | stand tipi · hall · ülke · satışçı · sales group · bölüm durumu · arama |
| Toplu eylem | Remind (bölüm seç → alıcı önizleme: kime gidecek, kim neden atlanacak) · Send all now · Export (stand firması dökümü: fascia + panel + orders) |
| Fair days görünümü | sütunlar: Badges printed · Stand handed over · Orders delivered · Payment warning · Issue note. Tam tarifi bu turda yok |
| Boş / eksik | kontrat yoksa boş durum. Expo ayarı eksikse üstte şerit: "3 deadline girilmemiş — hatırlatmalar planlanmadı" → Expo settings |
| Telefon | exhibitor başına kart: ad + stand; yalnız sorunlu bölümler yazıyla ("Catalogue overdue") |

**Pavyon için iki yol**
- Yol A: satır = kontrat; açılınca altında co-exhibitor'lar.
- Yol B: satır = exhibitor; "Pavilion: {agent}" etiketi + "Group by contract" anahtarı. Co-exhibitor'ın Payment ve Orders hücresinde "at pavilion contract" yazar.
- Tercihim B. Catalogue, fascia ve badge exhibitor başına kovalanıyor; liste de öyle saymalı.

**Riskler (C2)**
- "Stuck" tanımı net olmazsa süzgece güven kalmaz.
- Durum yalnız renkle verilmemeli; çip yazılı olmalı.

---

## C4 — Expo settings

**Amaç:** e-postaların, Exhibitor Page'in ve sayaçların tek veri kaynağı.
**Kim:** project team yazar; satış salt okur (tarihler, deadline'lar, kişiler, fiyat listesi, dokümanlar); Finance payment deadline'ını ve kendi gönderen kutusunu görür.

| Bölüm | Alanlar | Tür | Zorunlu | Neyi besler |
|---|---|---|---|---|
| 1 Kimlik | ad · edisyon · sektör · şehir · ülke · mekân · başlangıç–bitiş · küme (aynı mekân ve tarihteki kardeş expo) | metin · tarih · seçim | ad, tarih, mekân | tüm e-postalar, sayfa başlığı |
| 2 Build-up & breakdown | special stand programı · standard stand programı · yükleme kuralları · ülke notu (+görsel) · açılış saatleri · söküm · kayıt masası yeri ve saatleri | tarih-saat satırları + EN/FR/TR yan yana metin blokları | programlar, açılış saatleri | Build-up e-postası · sayfadaki Build-up · Badge e-postası |
| 3 Stand | Equipped paketi (kalem · adet) · fascia karakter sınırı · Space-only üst yükseklik · on-site fiyatın başladığı tarih | liste · sayı · tarih | paket, üst yükseklik | sayfadaki Stand ve Extra equipment |
| 4 Deadline'lar ve zamanlama | catalogue · stand · order · payment · badge · shipment: tarih + "ilk hatırlatma N gün önce" + "geçince her N günde" + "son hatırlatma günü". Ayrıca ilk gönderim: Stand ve Catalogue fuardan N gün önce (bugün 45), Build-up ve Badge N gün önce | tarih + sayı | ilk beş deadline | chain planı · sayfa ve liste sayaçları |
| 5 Ortaklar ve kişiler | HQ · local office · travel · forwarder · contractor · visa: firma · kişi · telefon · e-posta | kişi kartları | HQ, local | Welcome · sayfadaki Contacts |
| 6 Ürün/fiyat listesi | bağlı liste: ad · kalem sayısı · para birimleri · "open list" | bağ | sipariş için evet | Extra equipment |
| 7 Dokümanlar | stand çizimi şablonu · equipment list · exhibitor manual · diğer; dil etiketi | dosya | exhibitor manual | sayfadaki Documents · e-posta linkleri |
| 8 Gönderim | gönderen kutuları (Project / Finance) · varsayılan dil kuralı · "Pause automatic sends" | seçim · anahtar | kutular | chain |

| Parça | Tarif |
|---|---|
| Hazırlık paneli (üstte) | e-posta başına "Ready / eksik": ör. "Stand: 2 alan eksik (Equipped paketi, stand deadline)". Ayrıca eksik dil sayacı: "FR eksik: 3 blok" |
| "Copy from previous edition" | metinler, kişiler, paket, hatırlatma günleri, dokümanlar kopyalanır. Tarihler kopyalanmaz. Kopyalanan her blok "copied — not reviewed" işaretli; biri açıp "Reviewed" diyene kadar sayaçta kalır |
| Küme | "Copy to sibling expo" (kişiler ve program) |
| Deadline değişince | onay penceresi: "N exhibitor'ın hatırlatma planı değişecek" |
| Durumlar | Incomplete → Ready · Paused |
| Boş durum | yeni expo: büyük "Copy from previous edition" düğmesi |
| Telefon | salt okunur özet |

**Riskler (C4)**
- Geçen yılın metni bu yıl gidebilir; "not reviewed" kapısı bunun için.
- Dil eksikse EN'e düşer; sayaçta görünmeli.
- Ayar değişikliği planı sessizce kaydırmamalı.

---

## C5 — Communications: Chain status + Rules

### Chain status tablosu

| Parça | Tarif |
|---|---|
| Kapsam | seçili expo. Satır = exhibitor, sütun = 6 e-posta |
| Hücre | Planned {tarih} · Sent {tarih} · Reminded ×n · Done · Failed · Blocked · Excluded · Paused |
| Özet (üstte) | e-posta başına: gönderildi · planlı · hata · işi bitenlerin oranı |
| "Next 7 days" | önümüzdeki 7 günde kendiliğinden gidecekler: tarih · e-posta · alıcı sayısı → liste |
| Varsayılan süzgeç | yalnız sorunlular: Failed · Blocked · Overdue ve hatırlatması biten · 3+ hatırlatma cevapsız |
| Hücreye tıkla | gönderim geçmişi (tarih · kime · dil · sonuç) + giden metin + detail linki |
| Toplu eylem | Send now · Resend · Exclude. Önce alıcı önizleme: gidecek N, atlanacak M ve nedeni |
| Payment Reminder sütunu | Finance kutusundan gider; project team görür ve "Remind" basabilir (A2) |
| Telefon | tablo yerine sorun listesi: exhibitor · e-posta · neden · eylem |

**Risk:** toplu gönderim yanlış kitleye gidebilir; önizleme atlanamaz olmalı.

### Rules eskizi (A10, yalnız yer)
- **Yer:** Communications › Rules. Liste: ad · koşul özeti · şablon · eylem · zamanlama · açık/kapalı · son çalışma · etkilenen sayı.
- **Kural yapısı:** When (kontrat oluştu / bir tarih alanından N gün önce-sonra / alan değişti) + If (kontrat, expo, ülke alanları) + Then (şablon gönder, 3 dil · etiket ekle · alan güncelle).
- **Tek model:** 6 sabit e-posta aynı listede "built-in" satır olarak durur; silinmez, metni ve zamanı düzenlenir.
- **Açmadan önce:** "Preview" bugün kimlere gideceğini listeler; ilk çalıştırma onaylıdır. Örnekler: Boost (expo başına) · Shipment (Türk pavyonu, shipment deadline'ından N gün önce).
- **Risk:** çakışan kurallar aynı kişiye çok posta yollar; kişi başı günlük üst sınır ve kural günlüğü gerekir. "Alan güncelle" finans alanlarına kapalı olmalı.

---

## C6 — E-posta yapıları

**Ortak çerçeve**
- Konu: "{Expo adı} — {konu}". Hatırlatmada: "{Expo adı} — Reminder: {bölüm} · due {tarih}".
- Üst: expo adı · tarih · mekân · stand no.
- Tek ana düğme = Exhibitor Page deep-link.
- Alt: project team HQ + local kişi (Payment'ta Finance imzası) · "operational message" notu.
- Dil: kişinin dili → yoksa expo/ülke kuralı → EN. Tek şablon, EN/FR/TR yan yana.
- Gönderen: Project kutusu; Payment Reminder'da Finance kutusu. Cevap adresi gönderen kutu.

| E-posta | Ne zaman | Bölümleri | Hangi alanlardan dolar | Deep-link | Gönderen |
|---|---|---|---|---|---|
| Welcome | kontrat oluşunca | katılım onayı (expo · tarih · mekân · stand tipi / m² / no) · tek link tanıtımı · sıradaki adımlar + deadline'lar · kişiler tablosu | kontrat · expo kimlik · deadline'lar · ortaklar | Contacts | Project |
| Stand (Equipped / Space-only; stand tipine göre) | fuardan N gün önce (bugün 45); geç imzada hemen | stand özeti · istenen (Equipped: fascia + onay; Space-only: tasarım + contractor + üst yükseklik) · Equipped'da dahil ekipman · extra equipment + fiyatın değiştiği tarih · deadline | Operations bilgileri · stand paketi · üst yükseklik · stand ve order deadline'ı | Stand | Project |
| Catalogue | fuardan N gün önce (bugün 45) | katalog nedir · ne istenir (kısa) · deadline + kilit notu | expo kimlik · catalogue deadline | Catalogue | Project |
| Build-up & Breakdown | fuardan N gün önce | kendi stand türünün programı · yükleme kuralları · ülke notu · açılış saatleri · söküm · exhibitor manual | expo ayarı bölüm 2 + dokümanlar | Build-up | Project |
| Payment Reminder | payment deadline'ına göre; yalnız bakiye varsa | bakiye + vade (sunucudan) · dekont isteği · banka masrafı notu | kontrat ödeme özeti · satıcı tüzel kişi | Payment (kod) | Finance |
| Badge | fuardan N gün önce | nasıl işler (kendi e-postası → QR → masada baskı) · kayıt masası yeri ve saatleri · ekip linki | expo ayarı bölüm 2 | Badges | Project |
| Reminder (her bölüm için tek kalıp) | deadline'dan N gün önce; geçince her N günde | tek paragraf: eksik bölüm + deadline (ya da "geçti") · tek düğme | bölüm durumu · deadline | ilgili bölüm | Project (Payment: Finance) |

- **Bu tasarımın doğurduğu ek e-postalar:** Changes requested · Approved · Order confirmation (yeni kontrat no) · Payment code · New link. Badge QR e-postası LEENA'da zaten var.
- **İç bildirimler** (yeni kontrat · iptal · quote signed): mevcut, dokunmadım.

---

## Karar gerektirenler (Sentez'e)

1. "Place order" da kodlu olsun mu? Önerim evet; sipariş yeni kontrat doğuruyor.
2. +%100 hangi tarihten başlar: order deadline mı, build-up'ın ilk günü mü? Deadline'dan sonra sayfadan sipariş açık kalır mı?
3. Aynı exhibitor'ın ikinci siparişi yine ayrı kontrat mı?
4. Panel baskı Stand bölümünde seçilince Extra equipment siparişine kalem olarak mı düşer? B3'teki "tam baskı %10" indirim mi? Baskı görseli sayfadan mı yüklenir?
5. Equipped paketi (dahil ekipman + adet) expo ayarında mı tutulur; m²'ye göre adet kuralı var mı?
6. Stand deadline'ı onaysız geçerse varsayılan uygulanır mı (fascia = katalogdaki ad)?
7. Catalogue'da hangi alanlar zorunlu, profil kaç karakter?
8. Build-up rules için "okudum" onayı istenip izlenecek mi?
9. Hatırlatma ne zaman durur ve kişi başı üst sınır var mı? Önerim: build-up'ın ilk günü.
10. Chain e-postalarını ve ödeme kodunu kim alır: yalnız ana kişi mi, kontrattaki tüm kişiler mi?
11. Pavyon: her co-exhibitor'a dar bir sayfa linki mi (Stand fascia · Catalogue · Badges), yoksa hepsini kontrat sahibi mi doldurur?
12. Beklet / aktar / iptal olunca sayfa ve chain ne yapar? Aktarmada doldurulan içerik yeni kontrata taşınır mı?
13. Banka bilgisi Payment Reminder e-postasında da yer alsın mı? Önerim: yalnız kodlu bölümde (sahte banka bilgili e-posta riskine karşı).
14. "I paid — upload receipt" ödeme kaydı değil, bildirim. Finance bunu nerede görür? (Finans akışına dokunuyor; tarif etmedim.)
15. Ek e-postalar (Changes requested · Approved · Order confirmation · code · new link) sabit mi olacak, kural mı? Badge'de aynı e-posta visitor olarak kayıtlıysa ne olur?

İstersen sıradaki adım olarak C1'i Vermillion'da görsel mockup'a çeviririm.
