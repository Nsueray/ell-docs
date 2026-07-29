> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# ELL — Karar Oturumu Özeti

**Tarih:** 2026-06-01
**Amaç:** Yol haritası v4'e nasıl varıldığının kaydı — hangi kararlar, hangi gerekçe,
hangi yanlış yoldan dönüldü. "Bu karar neden böyle?" sorusunun cevabı burada.

> Bu belge yol haritası DEĞİLDİR (o v4'tür). Bu, kararların ARKASINDAKİ akıl yürütme.
> Gelecekte bir karar sorgulandığında buraya bakılır.

---

## Başlangıç durumu (neden kaybolunmuştu)

Suer 3 sistem kurmuştu (LEENA/LIFFY/ELIZA), hepsi prototip, hepsi çalışıyor ama hiçbiri
Elan Expo'nun gerçek ihtiyacını tam karşılamıyor. "Hepsini birleştirip Zoho'dan kurtulayım"
derken kaybolmuştu. Kaybolmanın iki kök sebebi tespit edildi:

1. **"ELIZA" isim çakışması:** Bugünkü eliza (Zoho'dan finans çeken dashboard) ile
   hayalindeki birleşik sistem (kızının adı, marka) aynı kelimeyle anılınca, belgeler
   birbiriyle çelişti.
2. **Over-engineering:** Architecture dokümanı, gerçekte var olmayan (kodda hep TODO olan)
   devasa bir mimari (RS256/JWKS/saga/key-rotation) tasarlamıştı. Kağıt üstünde bile
   altından kalkılamadı.

---

## Yöntem: her karar tahminle değil, KANITLA verildi

Sırayla 4 ölçüm yaptırıldı (Claude Code, dosya:satır kanıtlı, kod hiç değiştirilmeden):

1. **Gerçek durum analizi** — 3 sistemin kod/şema röntgeni
2. **Cross-DB ölçümü** — 58 rapor/ekran sayıldı: kaç sistemden veri çekiyor
3. **Gap analizi** — 35 ihtiyaç: ne var, ne yok, ne kurtarılır
4. **Üç derin analiz** — LIFFY, ELIZA, LEENA tek tek, alan bazında

Bu disiplin önemli: her büyük karardan önce "tahmin etme, ölçtür" yaklaşımı uygulandı.
Yeni kararlar da böyle verilmeli.

---

## Verilen kararlar ve GEREKÇELERİ

### Karar 1: 3 DB ayrı kalır, tek DB'de birleştirilmez
**Gerekçe:** Cross-DB ölçümü, gerçek-join + real-time gerektiren ekran sayısını **0**
buldu. Tek DB'yi teknik olarak zorunlu kılan hiçbir ihtiyaç yok. Üstelik 3 ayrı DB ile
bir senedir sorunsuz çalışılıyor. Tek DB'ye taşımak, çalışan sistemi riske atan büyük
bir migration olurdu — getirisi yok.

### Karar 2: 2 deployment (ana app = ELIZA+LEENA, LIFFY ayrı)
**Gerekçe:** Tek kişi 4 mikroservis yönetemez (operasyonel yük). Ama LIFFY iki sebeple
ayrı kalmalı: (a) email deliverability izolasyonu, (b) **güven izolasyonu** — freelancer
satışçılar LIFFY'de çalışır, iç finans dünyasına erişemez. Bu "modular monolith + ayrı
LIFFY" yapısı, microservice'in karmaşıklığını taşımadan modülerliği verir.

### Karar 3: Ticari çekirdek (quote→contract→payment) = asıl iş
**Gerekçe:** Gap analizi gösterdi ki bu çekirdek üç sistemin HİÇBİRİNDE yok. ELIZA'nın
"finans"ı bir yanılsama — contracts/payments Zoho'dan çekilen salt-okunur kopya, ELIZA
tek satır yazamıyor (tasarımca "never write back"). Yani "Zoho'dan kurtulmak" =
işlemsel çekirdeği sıfırdan ELL'de kurmak. Birleştirme değil, İNŞA asıl iş.

### Karar 4: Quote LIFFY'de kalır (ana uygulamada değil)
**Gerekçe:** Suer'in iş modeli — satışçılar freelancer, güvenilmez, işe girip çıkıyor.
Quote'ları onlar yapıyor. Requirements satır 351-363 de bunu "privacy boundary" ilkesi
olarak yazmış. Quote LIFFY'de tutulunca, convert gate = dış halkadan (güvenilmez satış)
iç halkaya (güvenilir finans) geçişin kontrol kapısı olur.

### Karar 5: SSO için HS256 (basit secret), RS256/JWKS DEĞİL
**Gerekçe:** RS256/JWKS'in tek gerçek avantajı, güvenilmeyen üçüncü taraflara "doğrula
ama üretme" yetkisi vermektir. Suer'in 2 deployment'ı da kendisinin, birbirine güveniyor
→ bu senaryo yok. RS256 burada daha güvenli değil, sadece kalıcı bakım yükü. (Gelecekte
LEENA satılırsa, o gün HS256→RS256 geçişi birkaç günlük iş — ihtimal için bugünden kurma.)

### Karar 6: Güvenlik = ayrı kriz değil, gömülü önkoşul
**Gerekçe:** Üç sistemde de güvenlik açığı var (LIFFY veri izolasyonu, ELIZA hiç auth yok,
LEENA commit'li secret). AMA bugün dışa kapalı, sadece Suer + asistanı kullanıyor → acil
yangın değil. Doğru konumlama: "LIFFY'yi freelancer'a açmadan önce izolasyon", "ELIZA'ya
finans yazmadan önce auth" — yani ilgili dilimin önkoşulu, ayrı bir kriz fazı değil.

### Karar 7: Şema kurtarma EN BAŞA (Faz 0a)
**Gerekçe:** Bu, bugünkü tek GERİ-DÖNÜLEMEZ risk. LEENA'nın 7 üretim tablosu + ELIZA'nın
4 migration'ı kaynak kodda YOK; şema sadece canlı Render DB'sinde yaşıyor. O DB bir gün
kaybolursa/taşınırsa koddan yeniden kurulamaz. Düzeltmesi ucuz ve risksiz (READ-ONLY
şema çekimi). Bu yüzden inşaattan önce ilk adım.

### Karar 8: Zoho 1 yıl açık kalır, en sona kapatılır
**Gerekçe:** Suer'in kararı. Güvenlik ağı — ELL'de bir şey yanlış giderse gerçek Zoho
duruyor, kayıp yok. Bu, tüm geçişi baskısız ve paralel-doğrulamalı yapar.

---

## Reddedilen yollar (ve neden)

- **Tek DB'de birleştirme** → ölçüm gerekçelendirmedi; çalışanı riske atardı
- **Microservice (4 ayrı servis)** → tek kişi yönetemez
- **Quote'u ana uygulamaya almak** → güven izolasyonunu bozardı
- **RS256/JWKS/saga** → over-engineering, kaybolmanın asıl sebebi
- **Sıfırdan her şeyi yeniden yazmak** → korunan adalar (LEENA ops, ELIZA AI, LIFFY
  campaign) üretim kalitesinde, yeniden yapmak israf
- **Architecture dokümanını canonical tutmak** → gerçeğe değil hayale dayanıyordu

---

## Değişmeyen ilkeler (gelecekteki her karar için)

1. Over-engineering'e dönme. En basit çözüm. Karmaşıklık ancak gerçek ihtiyaç kanıtlanınca.
2. Requirements = pusula. Çakışmada requirements kazanır.
3. Dikey dilim. Her parça baştan sona çalışsın; her faz sonunda görünür çıktı.
4. Adaları koru. LEENA ops, ELIZA AI, LIFFY campaign — dokunma.
5. Tahminle değil kanıtla. Belirsizse Claude Code'a ölçtür.
6. Çalışanı (özellikle canlı LEENA) bozma.
