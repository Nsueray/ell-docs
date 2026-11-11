# UI FAZI — TAKİP (ekran envanteri × tasarım kaynağı · inşa · Suer turu · kuyruk)

> **Ne:** UI-ÖNCE fazının (kütük YON-21) tek takip belgesi — Sentez 11 Kas PAKET UI-TAM-2 §1. Her ekran için: tasarım kaynağı · inşa durumu ·
> Suer turu · kuyruk. Kriter bu belge DEĞİLDİR: kriter Sentez blokları (defterde AYNEN) + kütük; bu belge nerede ne olduğunu gösterir.
> **Güncelleme:** her paket parçasında (defter kaydıyla aynı commit). **Son güncelleme:** 2026-11-12 — PAKET UI-TAM-2 4. parça (proje ekibi ekranları) staging'de.
> **Ortam:** yalnız staging (`https://leena-staging.onrender.com/ui2/`). Canlıda bu fazın hiçbir ekranı yok. Tarihseldir (YON-01).

## 1. Tasarım kaynakları

| Kaynak | Nerede | Statü |
|---|---|---|
| Tasarım seti (Claude Design, 22 ürün ekranı; Signal + Vermillion) | Suer'in bilgisayarı · taranmış kopyası LEENA `design-preview/` (private; staging'de `/design-preview/`, "PROTOTYPE" şeritli) | PAKET UI-TAM'ın kaynağı; set ell-docs'a (public) GİRMEZ |
| Sentez blokları (UI-ÖNCE kuralları · PAKET UI-TAM · PAKET UI-TAM-2 + EK-1 + EK-2 + EK-3) | defter (AYNEN) + kütük UI-07 · EXH-01…20 · GUV-06 · RAP-18 · ILT-07 · YET-19 eki | **KRİTER** — ekler öncekini düzeltir (EK-3 > EK-2 > EK-1 > blok) |
| UX hattı 3. tur (C1–C6: Exhibitor Page + project team ekranları) | `docs/ux/UX_HATTI_3_TUR_2026-11-11.md` (AYNEN) | ekran tarifi; kriterle çelişirse kriter kazanır |
| UX hattı 2. tur (set × üç kullanıcının günü; 38 satır + 7 eskiz) | `docs/ux/UX_HATTI_2_TUR_2026-11-11.md` (AYNEN) | kriter DEĞİL — arşiv + bu belgenin "tasarım kaynağı" sütunu; öncelik Sentez bloğu > 3. tur > 2. tur |
| C1 mockup (`Exhibitor-Page-C1-mockup.html`) + UX notu | not: `docs/ux/UX_C1_MOCKUP_NOTU_2026-11-11.md` · dosya: Suer'in bilgisayarı | REFERANS (kriter değil). Dosya ell-docs'a KONMADI — §4 kuyruk "mockup eklenecek" |
| C2 + C3 mockup (`Exhibitors-C2-C3-mockup.html`) + UX teslim notu | not: `docs/ux/UX_C2_C3_MOCKUP_NOTU_2026-11-11.md` · dosya: Suer'in bilgisayarı | REFERANS (kriter değil). Dosya ell-docs'a KONMADI — §4 kuyruk "mockup eklenecek" |

## 2. Ekran envanteri

İnşa sütunu: **staging** = staging'de çalışıyor (LEENA `eliza-next` commit'i) · **UI-TAM-2 §n** = bu paketin o parçasında yapılacak / değişecek.
Suer turu: Y7 — Suer kendi Owner hesabıyla gezer, cevabı tek "değişiklik listesi".

| # | Alan | Ekran | Sayfa | Tasarım kaynağı | İnşa | Suer turu |
|---|---|---|---|---|---|---|
| 1 | — | Login | `login.html` | set | staging (`a71164f`) | bekliyor |
| 2 | Sales | My Work | `sales-home.html` | set · UX 2. tur #22–23 | staging (`5032a1f`) | bekliyor |
| 3 | Sales | Mail (v1) | `sales-mail.html` | set | staging (`5032a1f`) | bekliyor |
| 4 | Sales | Pipeline | `sales-pipeline.html` | set · UX 2. tur #24 | staging (`5032a1f`) | bekliyor |
| 5 | Sales | Quotes + teklif | `sales-quotes.html` · `sales-quote.html` | set · UX 2. tur #25–27 | staging (`5032a1f`) | bekliyor |
| 6 | Sales | Companies + firma kartı | `sales-customers.html` · `sales-customer.html` | set · UX 2. tur #29–30 · YET-26 | staging (`5032a1f`) | bekliyor |
| 7 | Operations | Dashboard | `ops-dashboard.html` | set · UX 2. tur #2 | staging (`e7b77ef`) | bekliyor |
| 8 | Operations | **Exhibitors** (liste) | `ops-exhibitors.html` | set → **UX 3. tur C2 · C2/C3 mockup · EXH-19** | staging (`e7b77ef`) → **yeniden kuruldu: staging (`df63427`)** | bekliyor |
| 9 | Operations | **Exhibitor** detayı | `ops-exhibitor.html` | set → **UX 3. tur C3 · C2/C3 mockup · EXH-20** | staging (`e7b77ef`) → **yeniden kuruldu: staging (`df63427`)** | bekliyor |
| 10 | Operations | Floor plan | `ops-floorplan.html` | set | staging (`e7b77ef`) — DEĞİŞMEZ (EXH-20; floor plan modülü Mimari hattında) | bekliyor |
| 11 | Operations | Visitor & Access | `ops-visitors.html` | set | staging (`e7b77ef`) | bekliyor |
| 12 | Operations | Communications | `ops-communications.html` | set · UX 2. tur #14–15 | staging (`e7b77ef`) | bekliyor |
| 13 | Operations | Reports | `ops-reports.html` | set · UX 2. tur #20 | staging (`e7b77ef`) | bekliyor |
| 14 | Finance | War Room | `owner-home.html` | set · UX 2. tur #33–34 | staging (`e61d0a9`) | bekliyor |
| 15 | Finance | Contract | `finance-contract.html` | set | staging (`e61d0a9`) → UI-TAM-2 §3: dekont şeridi | bekliyor |
| 16 | Finance | Commissions | `finance-commissions.html` | set | staging (`e61d0a9`) | bekliyor |
| 17 | Finance | Ledger | `finance-ledger.html` | set | staging (`e61d0a9`) | bekliyor |
| 18 | Finance | Expo Finance | `finance-expo.html` | set · UX 2. tur #35 · RAP-18 | staging (`e61d0a9`) → UI-TAM-2 §3: Gross margin / Net profit bağlanır | bekliyor |
| 19 | Operations · On-site | Mobile Dashboard | `mobile-home.html` | set | staging (`caa9f09`) | bekliyor |
| 20 | Operations · On-site | Mobile Scan | `mobile-scan.html` | set · YET-19 eki (A1) | staging (`caa9f09`) · oturumla check-in **staging (`de7d486`)** | bekliyor |
| 21 | Operations · On-site | Mobile Visitor List | `mobile-visitors.html` | set | staging (`caa9f09`) | bekliyor |
| 22 | Kabuk | Settings › Appearance | `settings-appearance.html` | set | staging (`caa9f09`) | bekliyor |
| 23 | Operations | **Expo settings** (YENİ) | `ops-expo-settings.html` | UX 3. tur C4 · UX 2. tur #4 + eskiz 4 · EXH-18 · EXH-06 (paket kuralı) | **staging (`de7d486`)** | bekliyor |
| 24 | Exhibitor yüzü (ui2 DEĞİL) | **Exhibitor Page** (YENİ) — kabuk · Stand · Catalogue · Badges · Build-up & documents · Contacts · geçersiz link sayfası | `/x/#<anahtar>` (repo: `exhibitor-page/`) | UX 3. tur C1 · C1 mockup · UX 2. tur #16–17 + eskiz 0–2 · EXH-01…14 · GUV-06 | **staging (`dc2e3e1`)** | bekliyor |
| 25 | Exhibitor yüzü | Exhibitor Page — **Extra equipment + Payment** (kodlu) | `/x/#<anahtar>/extra-equipment` · `/payment` | UX 3. tur C1 · EXH-05 · EXH-10 · EXH-13 | **staging (`0da9c4f`)** | bekliyor |
| 26 | Finance | Collections — **"receipts to check"** (+ kontrat sayfasında şerit · Expo Finance'ta RAP-18 marj) | `finance-collections.html` · `finance-contract.html` · `finance-expo.html` | Sentez C14 · EXH-10 · RAP-18 | **staging (`0da9c4f`)** | bekliyor |
| 27 | Operations · Communications altında | **Chain status** (YENİ) — tablo · özet · next 7 days · Send now / Send all now / Resend / Exclude (önizlemeli) + listede Chain sütunu + detayda chain kartı | `ops-chain.html` | UX 3. tur C5 · C3 · UX 2. tur #9 · #14 + eskiz 3 · EXH-16 | **staging (`9cb08d4`)** | bekliyor |
| 28 | Operations · Communications altında | **Rules** (YENİ; salt okuma — 12 yerleşik satır; kural motoru işaretli) | `ops-rules.html` | UX 3. tur C5 · EXH-17 | **staging (`9cb08d4`)** | bekliyor |
| 29 | Exhibitor yüzü + Operations | **Pavyon**: mod (DIRECT / VIA AGENCY) · co-exhibitor alt kayıtları · dar link · acentenin sayfasında "Co-exhibitors" bölümü · detayda pavyon kartı + co-exhibitor görünümü · listede co-exhibitor satırları + gruplama | `/x/#<anahtar>` (dar sayfa · `…/co-exhibitors`) · `ops-exhibitor.html` (`?co=`) · `ops-exhibitors.html` (`?group=contract`) | Sentez B6 · EK-2 H2 / H3 / H8 · C2/C3 mockup · UX 2. tur #6 · EXH-15 | **staging (`934d6d0`)** | bekliyor |

## 3. Çeviri ve metin durumu (UI-TAM-2)

| Konu | Durum |
|---|---|
| Exhibitor Page arayüz metinleri FR / TR | CC taslaklar — **çeviri gözden geçirilmedi** (EK-1 madde 5) |
| 6 yerleşik e-posta EN / FR | LEENA'da 13 metin (7 EN + 6 FR) — Drive'daki 14 şablondan tohumlandı (12 Kas), Exhibitor Page'e uyarlandı: form linki → düğme, tutar ve kişisel imza çıktı. EN'de birkaç taslak cümle var; FR'de yalnız Drive'ın hâlâ geçerli satırları (yeni FR cümle yazılmadı). **Metin gözden geçirilmedi** (ell-docs'a metin GİRMEDİ) |
| Build-up & Breakdown FR | **eksik** — Drive'da FR sürümü yok; EN'e düşer |
| E-posta TR | **eksik** — EN'e düşer; CC TR e-posta metni yazmaz (UX / Yaprak sonra yazar) |
| E-posta çerçevesi (üst bilgi etiketleri · alt not) | yalnız EN — FR / TR "eksik" |
| Hatırlatma kalıbı + sistem e-postaları | Drive'da karşılığı YOK (ölçüldü); EN'i CC taslakladı — **metin gözden geçirilmedi**; FR / TR "eksik" |

## 4. Kuyruk

**UI-TAM-2'den çıkanlar (Sentez / Orchestrator):**
- **UI-DÜZELTME-1** (ayrı küçük paket, Suer'in staging listesiyle): token düzeltmesi (Vermillion'da chip-info ≈ chip-dang) · kendi-dosya fontların ui2
  geneline uygulanması · yavaşlık ölçümü.
- Satışçı kendi kontratlarının exhibitor durumunu salt okunur görsün mü — Suer kararı, Faz 4.
- stand no'nun kaynağı → yeni floor plan modülünün yerleştirme kaydı (Mimari hattı)
- Sürümü olan kontratı yeni Equipped paket sürümüne geçirme eylemi.
- FR / TR çeviri gözden geçirme (arayüz) · TR e-posta metinleri.
- **Pavyon (§6) kuyruğu:** pavyon payına özel Stand e-posta metni · büyük pavyonda liste süresi ölçümü · toplu Remind'in co-exhibitor satırlarını da
  alması · Sentez'e iki okuma sorusu: VIA AGENCY'de acente co-exhibitor EKLEYEBİLSİN mi · DIRECT'te acente co-exhibitor'larının durumunu salt okunur
  görsün mü. Yeni arayüz metinleri (co-exhibitor bölümü) FR / TR taslak — gözden geçirilmedi.
- **Zincir (§5) kuyruğu:** zincir e-posta metinlerinin gözden geçirilmesi (EN uyarlama + FR) · Build-up FR metni · çerçeve etiketlerinin FR / TR'si · metni
  ekrandan düzenleme (kural motoruyla) · büyük fuarda Chain status süresi ölçümü · Sentez'e iki okuma sorusu: "Stuck"ta fuar düzeyindeki bloklar sayılsın mı ·
  "Send all now" günü gelmemiş satırı da yollasın mı.
- **mockup eklenecek:** `Exhibitor-Page-C1-mockup.html` · `Exhibitors-C2-C3-mockup.html` — dosyalar bulundu, özetleri tutuyor; public repo taraması
  (YON-20) içlerindeki `.example` e-posta adreslerini (ve C1'deki IBAN biçimli örnek dizgiyi) engelliyor → 🔶 Sentez (tarama kuralı mı, yer mi).
- Kural motoru (EXH-17) · Gmail / gelen cevaplar · Fair days görünümünün tam tarifi · Transfer akışı ekranı · "Add co-exhibitor" dışındaki pavyon
  ekleri — paket kapsamı dışında, işaretli.

**UX 2. turun UI-TAM-2 kapsamında OLMAYAN maddeleri — kuyruk — Sentez kararı bekliyor** (satır no = 2. tur tablosu):
- #1 Fuarlar listesi (proje ekibinin girişi; eskiz 5) · #2 Ops Dashboard'un iki modu ("bugün kimi kovalayacağım" + son tarihler).
- #3 Convert inceleme ekranı (imzalı teklif + tarama yan yana) · #12 beklet / aktar / iptal eylemlerinin ekranı (sayfa ve zincir davranışı EXH-14'te).
- #15 Communications › Templates düzenleyicisi (tek şablon–üç dil yan yana + önizleme) · #18 katalog üretici (PDF) · #19 fuar günü görünümü (iskelet
  UI-TAM-2 §4'te) · #20 Ops Reports kaynak kırılımı + veri girişi raporu.
- #21–#27 Sales alt menü / My Work / Pipeline / Quotes maddelerinden UI-TAM'da karşılanmayanlar · #28 satışçı için kat planı · #29–#30 Companies
  listesi süzgeçleri + firma kartı ekleri · #31 lead listesi + kampanya ekranları.
- #32 Owner ana sayfası (eskiz 6) · #33 War Room sütunları (m² · hedef % · açık bakiye · geciken) · #34 War Room uyarıları (üç kaynak, gördüm / ertele) ·
  #35 Expo Finance: satırdan harekete inme + fuar listesi (Gross margin / Net profit RAP-18 ile UI-TAM-2'de) · #36 onaylar + Finance › Reports.
- #37 üst çubuk (bildirim paneli) + Settings (Profile dil · Notifications · Team & roles) · #38 UX'in görmediği 7 ekran için satırlar.
