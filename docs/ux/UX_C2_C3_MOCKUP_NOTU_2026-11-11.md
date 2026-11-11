> **Arşiv notu (CC, 2026-11-11) — aşağıdaki metnin parçası DEĞİLDİR.**
> **Ne:** UX hattının C2 + C3 (Exhibitors listesi + Exhibitor detail; pavyon ve C1'in DIRECT dar-link hali dahil) mockup teslim notu (11 Kas 2026). Orchestrator'ın 11 Kas 21:30 tarihli PAKET UI-TAM-2 bloğundaki kopya; çizginin altındaki metin **AYNEN** (oturum kaydından
> programla alındı). Orchestrator notu: "Baştaki ve sondaki Suer'e hitap satırları alınmadı; iç kod çiti kaldırıldı." Metin Markdown; hiçbir yapı eklenmedi.
> **Statü:** REFERANSTIR, **kriter DEĞİL** (kriter Sentez bloğu + EK-1 + EK-2 + EK-3 — [defter:2026-11-11 SENTEZ 11 Kas: PAKET UI-TAM-2]). Nasıl bakılır: EK-2 (üst koyu şerit senaryo seçici: Scenario · Screen · Exhibitor · Viewport) + nottaki "İstenenler nerede" tablosu. 1–9'un hükmü = EK-2 H1–H9 · 10–13 = EK-2'de KABUL. Mockup hükümlerden ÖNCE yapıldı: H1 · H2 · H3 · H5 · H7 · H8 · H9'da EK-2 geçerlidir.
> **Mockup dosyası:** `Exhibitors-C2-C3-mockup.html` — sha256 `69afb8315182ff861fc04cef17ae5ea3c954a536f19a46ea6a0a1ec433efc0aa` · 129.039 bayt · 1.176 satır. Dosya Suer'in bilgisayarında bulundu, özeti Orchestrator'ın ölçümüyle AYNI;
> **ell-docs'a KONMADI**: public repo taraması (YON-20) dosyada 2 eşleşme (e-posta adresi — ikisi de `.example` alanında) buluyor ve push'u engelliyor; dosya bayt bayt AYNEN girmek zorunda
> olduğundan değiştirilmedi, tarama kuralı da gevşetilmedi → 🔶 Sentez + kuyruk "mockup eklenecek" (`docs/UI_FAZI_TAKIP.md`).
> **Font / dış kaynak (EK-2 N1):** dosyanın 8–10. satırlarında Google Fonts'a 3 `<link>` var (2 preconnect + 1 stil dosyası); fetch / XHR / dış
> script YOK. Üründe anahtarlı sayfalar başka kökenden hiçbir şey yüklemez (kütük GUV-06) — bu satırlar ürüne TAŞINMAZ.
> Mockup'ın CSS'i / token'ları ve üstteki koyu senaryo şeridi de ürüne taşınmaz (ui2 `tokens.css` + `components.js`).

---

(Baştaki ve sondaki Suer'e hitap satırları alınmadı; iç kod çiti kaldırıldı. 1–9'un hükmü = EK-2 H1–H9 · 10–13 = EK-2'de KABUL)
**C2 + C3 mockup hazır:** `Exhibitors-C2-C3-mockup.html` (tek dosya, ~129 KB, tamamı sahte veri). Sentez'in 5 cevabı uygulandı; cevaplarda olmayan yerlerde 3. turdaki tercihlerim geçerli, hepsi aşağıdaki blokta.

## Nasıl bakılır
- Üstteki koyu şerit ürünün parçası değil. Dört seçici var: `Scenario` · `Screen` · `Exhibitor` · `Viewport`.
- Durumlar elle işaretlenmiyor: senaryonun tarihi ile olay kaydından türüyor (17 uydurma exhibitor, tek veri).
- Üç ekran aynı veriyi paylaşıyor: co-exhibitor dar sayfada fascia onaylayınca C3'te ve listede de değişiyor.

## İstenenler nerede

| İstenen | Nerede |
|---|---|
| Expo ayarı eksik şeridi | Scenario: Expo settings missing |
| Deadline sayaçları, hazır görünümler, toplu Remind önizlemesi | C2; satır seç → `Remind…` |
| Fair days (yalnız iskelet) | Scenario: Fair week |
| Failed · Blocked · Overdue, uyarı şeritleri | Scenario: Problems → Quillon, Tessar, Vestra, Lumira |
| E-mail chain, 8 durumun hepsi | C3 altındaki kart; Paused için `⋯ → Put on hold` |
| Deadline sonrası Request changes + yeniden açma tarihi | Problems → Ordane → Stand |
| Enter on behalf (not zorunlu) | Problems → Lumira → Stand |
| Stand type seçimi | Problems → Tessar → Operations info → Edit |
| Pavyon etiketi + Group by contract | Scenario: Pavilion |
| Co-exhibitor alt listesi, DIRECT / VIA AGENCY | Pavilion → Meridia Trade Agency |
| C1'in DIRECT dar-link hali | Screen: C1, ya da co-exhibitor'da `Open as exhibitor` |

## Ölçtüm (headless Chrome, son dosya üzerinde)
- 5.342 ekran ve pencere durumu çizildi (senaryo × ekran × exhibitor × sekme × pencere, masaüstü + telefon): 0 script hatası, 0 bozuk metin.
- 74 tıklama ve kural kontrolü geçti.
- 1280–1680 px'te liste tablosu yana kaymadan sığıyor; 390 px'te sayfa yana taşmıyor.
- Dev boyutlu bir ikon hatasını ekran görüntüsünde yakalayıp düzelttim. Aynı kontrolü teslim edilmiş C1 dosyasında da koştum: 460 durumda sorun yok.

## Ölçmedim
- **Fontlar:** benim ortamımda Google Fonts yine yüklenmedi; yedek fontla baktım.
- **Safari / Firefox / gerçek telefon:** denenmedi, yalnız Chrome.
- **Staging (ui2):** görmedim. Üst menü ve alt menü tasarım setindeki kabuğun kopyası, gerçek ui2 kabuğu değil. Token'lar arşiv kopyasından.
- **SAMPLE adları:** müşteri listesiyle karşılaştırmadım.

## İki not
- **Yeni çip:** "In review" için koyu bir çip ekledim ("sıra bizde" anlamında). Tasarım setinde yok; bu dosyada `chip-info` hiç kullanılmıyor.
- **C1 dosyası:** Address line 2 orada hâlâ zorunlu görünüyor (cevap 2 ile fark). Kriter Sentez bloğu olduğu için dokunmadım.

## Sentez'e tek blok
UX → SENTEZ — C2 + C3 MOCKUP: VARSAYIMLAR / YENİ SORULAR (11 Kas)
Mockup aşağıdaki varsayımlarla duruyor; yanlış olanı söyleyin, düzeltirim.

KARAR GEREKENLER
1. "Stuck" eşikleri: deadline'a 7 gün kala To do · 5+ gün cevapsız Changes
   requested · bir bölüm Overdue (Payment dahil) · e-posta Failed.
   Sayılar ve Payment'ın dahil olması uygun mu?
2. Pavyon sahibi (agent) listede kendi satırıyla duruyor: Stand (pavyon
   inşası) · Orders · Badges · Payment onda; Catalogue "—". Doğru mu?
3. Co-exhibitor e-posta zinciri. DIRECT: Welcome · Stand (fascia) · Catalogue ·
   Build-up · Badge gider; Payment Reminder "Excluded — pavilion contract".
   VIA AGENCY: co-exhibitor'a hiçbir e-posta gitmez, hepsi ve hatırlatmalar
   agency'ye. Doğru mu?
4. "On behalf" girilen stand onayı ve catalogue doğrudan Approved oluyor
   (project team kendi girdisini ayrıca onaylamıyor). Doğru mu?
5. Stand type deadline'dan SONRA girilirse Stand e-postası hiç gitmemiş
   oluyor; mockup "Default applied" + "Reopen" gösteriyor.
   Kendiliğinden yeniden açılmalı mı?
6. Deadline'dan ÖNCE istenen değişiklik cevapsız kalıp deadline geçerse:
   mockup "Changes requested · N gün" + "Reopen until…" gösteriyor
   (exhibitor için kilitli). Doğru mu?
7. Elle "Remind", günde 1 hatırlatma sınırına tabi mi?
   Mockup sınırı yalnız not olarak yazıyor, engellemiyor.
8. Pavyon modu (DIRECT ↔ VIA AGENCY) onay penceresiyle anında değişiyor;
   VIA AGENCY'ye geçince co-exhibitor linkleri geçersiz. Doğru mu?
9. Regenerate link: yeni link alıcılara kendiliğinden "New link"
   e-postasıyla gidiyor. Doğru mu?

VARSAYDIM (itiraz yoksa kalır)
10. Chain'de "Job done" = exhibitor gönderdi (in review dahil); hatırlatma
    o an durur, "Changes requested" olunca yeniden başlar.
11. "Send all now" yalnız Planned olanları yollar; gönderilmişi tekrarlamaz.
12. Beklet: yalnız "Reactivate" kalır, diğer eylemler gizlenir.
    İptal: hepsi gizlenir.
13. Koyu "In review" çipi = sıra project team'de (tasarım setinde yok).

BU DOSYADA YOK
C4 Expo settings (yalnız düğme) · C5 · Fair days tam tarifi (iskelet) ·
satışçının salt-okur görünümü · Add co-exhibitor formu · Transfer akışı ·
e-posta metinleri (yalnız yapı) · FR/TR içerik.

UYDURMA ÖRNEK DEĞERLER (karar değil)
İlk gönderim tarihleri · hatırlatma aralığı (deadline − 14 gün, sonra
7 günde bir) · tutarlar · ürün fiyatları.
