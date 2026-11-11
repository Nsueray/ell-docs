# PAKET UI-TAM — BAĞLANTI HARİTASI (2026-11-11)

> **Ne:** Sentez 11 Kas "PAKET UI-TAM — TASARIM SETİNİN TAMAMI CANLANIR" ön ölçümü 1-d: setin 22 ürün ekranı × setteki HER öğe
> (kart · sütun · alan · düğme · sekme) → **mevcut uç** | **ucuz yeni uç (S)** | **İŞARETLİ + kuyruk**. Paketin iskeletidir; defterdeki
> ekran başına "bağlı / işaretli" listesi bundan çıkar. Kural: kütük **UI-07** (Y2 gerçek veri kuralı) · YON-21 eki.
> **Kaynak set:** Suer'in bilgisayarı, Downloads › "Eliza PlatformDesign" (11 Kas 11:30; 65 dosya — 22 ürün ekranı). Set ell-docs'a
> (public) GİRMEZ; taranmış kopyası LEENA `design-preview/` (private, prototip katmanı).
> **Kod tabanı:** LEENA `eliza-next` @ `eba7970` · kaynaklar: `docs/audits/EKSIK_ENVANTERI_2026-11-11.md` §1 / §4 / §5 + iki salt-okunur
> ölçüm (Sentez ❓ listesi · EMS kimlik haritası — dosya:satır kanıtları defter kaydında). **Kişisel veri YOK.**
> **Durum sütunu:** **B** = bağlı (mevcut uç / ekran) · **S** = bu pakette açılan ucuz uç (mevcut tablo üstünde okuma ya da tek alan
> yazımı; izin kodu + kapsam; yazımda denetim kaydı) · **İ** = üstünde görünür "Not connected yet" işareti + kuyruk (S / M / L).
> Bu belge PLANDIR (ön ölçüm); paket sonunda gerçekleşen durum defter kaydındaki listeyle kapanır. Tarihseldir (YON-01).
>
> Kısaltma: `A/` = `/api/analytics/` · R2 `…/performance` · R3 `…/expo/:id` · R4 `…/collections` · R5 `…/payments-by-agent` ·
> R7 `…/owner-home` · R6 bütçe `/api/ledger/budgets/:expo` · EMS = klasik uçlar (`/api/visitors` · `/api/checkins` · `/api/reports` ·
> `/api/terminals` · `/api/forms` · `/api/email-templates` · `/api/campaigns` · `/api/floorplan` · `/api/expos`).

---

## 0. Kabuk + Login

| ekran | öğe | bağlanır | durum |
|---|---|---|---|
| Kabuk | marka · üç sekme + alt etiket (Sales · Operations `leena` · Finance) | `nav.json` domains (UI-02) | B |
| Kabuk | rol görünürlüğü (dış kullanıcı yalnız Sales) | `/api/user-auth/me` `areas` (YET-15) | B |
| Kabuk | arama düğmesi + ⌘K | kabuk arama kutusu → `GET /api/search` (RAP-16); sonuç sayfası kabuk alanına taşınır (S6; envanter §4 U6) | B |
| Kabuk | zil | yalnız yer | İ — bildirim merkezi (L) |
| Kabuk | avatar | Settings › Appearance + "Who is signed in" | B |
| Kabuk | Design preview bağlantısı | `nav.json` `topbar` öğesi → `/design-preview/` | B |
| Login | marka paneli (başlık · alt metin · üç alan kutusu) | statik metin (alan adları nav.json ile aynı) | B |
| Login | şehir satırı · sürüm no | uydurma veri → üründe YOK (UI-07) | — |
| Login | e-posta · şifre · Sign in | `POST /api/user-auth/login` (kilit GUV-04 aynen) | B |
| Login | "Forgot?" | şifre sıfırlama yolu YOK (ölçüldü — GUV dilimi) | İ (M) |
| Login | "Keep me signed in" | oturum süresi sabit | İ (S) |
| Login | "Continue with SSO" | — | İ (L) |
| Login | dil seçici | arayüz dili tek (İngilizce) | İ (M) |
| Login | "Need access? Contact admin" | metin: giriş yalnız davetle (GUV-02) | B |
| Login | A (Signal) / B (Atlas) varyantları | yalnız prototipte; ürün = Signal + Vermillion (Sentez A) | — |

## 1. Operations (fuar bağlamı: seçilen fuar)

**Ortak bağlam çubuğu:** fuar seçici `GET /api/expos` **B** · yer / tarih `GET /api/expos/:id` **B** · cluster rozeti (fuarın cluster kaydı)
**B** · fuar kodu (`EXPO-…`) — alan yok **İ (S)** · geri sayım (gün / saat / dk + "doors open") — sunucu hesaplar, **S**
`GET /api/operations/dashboard?expo_id=` · cluster görünüm anahtarı (Combined / fuar) **İ (M — cluster toplamları, envanter #33)**.

### 1.1 Ops — Dashboard

| öğe | bağlanır | durum |
|---|---|---|
| KPI "Exhibitors": imzalı kontrat sayısı | R3 `totals.contracts` (Y5: Project `contracts.read`) | B |
| KPI "Exhibitors": onboarded sayısı · çubuk · "this week" | onboarding durumu yok | İ (L — katalog / stand / rozet akışları) |
| KPI "Floor occupancy": satılan m² / hedef | R3 `totals.m2` + `m2_target` (R6) | B |
| KPI "Floor occupancy": salon doluluğu % · "on hold" | kat planı ↔ kontrat bağı yok | İ (M) |
| KPI "Visitor registrations": toplam + bugün | EMS `/api/reports/summary` | B |
| KPI "Visitor registrations": hedef | ziyaretçi hedefi alanı yok | İ (S) |
| KPI "Conference seats": oturum + kayıt | EMS `/api/visitors/conference-topics` | B |
| KPI "Conference seats": kapasite / doluluk | kapasite alanı yok (ADR-021 konferans varlığı) | İ (M) |
| Live check-in traffic (saatlik) + Checked in / Registered today | EMS `/api/checkins/reports` + `/api/checkins/stats/summary` (CSS çubuk; grafik kütüphanesi yok) | B |
| "Peak" etiketi | sunucu saatlik dağılımından | S (aynı uç) |
| Onboarding pipeline: Catalogue · Stand design · Build-up · Badges issued | — | İ ×4 (L · M · M · M) |
| "Open Exhibitor →" | Ops › Exhibitors | B |
| Floor plan · salon mini haritası | hücre haritası editörde | İ (M) — köprü var |
| Floor plan: stand sayısı / m² (durum bazında) | **S** `GET /api/operations/floorplan-summary?expo_id=` (aktif sürüm) | S |
| Pending operational email (satırlar · Send · Review · sayı) | 8'li zincir motoru yok | İ (L) |
| "Open Communications →" | Ops › Communications | B |
| Export düğmesi | EMS `/api/visitors/export` (tam ziyaretçi listesi) | B |
| Fuar ana kaydı Overview: 8 son tarih (etkin tarihle) | `GET /api/expos/:id` `*_effective` | B |
| "Edit in Classic" | köprü: `nav.json` legacy → klasik `expo-form.html` | B (köprü) |

### 1.2 Ops — Exhibitor (liste)

| öğe | bağlanır | durum |
|---|---|---|
| Başlık sayacı "signed" · şerit "Signed exhibitors" | R3 / kontrat listesi (fuar süzgeci) | B |
| Sayaç "onboarded" · şerit "Fully onboarded" · "Catalogue complete" | — | İ ×3 (L) |
| Şerit "Blocked / at risk" | ödeme bazlı risk R4'te; fuar-satır bayrağı yok | İ (S) |
| Sekme All / Onboarding / Ready / Blocked | yalnız All (kontrat statüsü süzgeci B) | İ ×3 |
| Arama | kontrat listesi `search` | B |
| Süzgeç Hall · Stage | — | İ ×2 |
| Export | R3 `?list=companies&export=` | B |
| "Add exhibitor" | katılımcı = imzalı kontrat (teklif → çevirme) | İ — bağlantı: Sales › Quotes |
| Sütun Exhibitor (firma + ülke) | kontrat + firma | B |
| Sütun Stand: m² | kontrat m² (RAP-04) | B |
| Sütun Stand: no · salon | kat planı ↔ kontrat bağı yok | İ (M) |
| Sütun Contract: AF no · tutar · ödenen | `GET /api/contracts/paginated` (kapsam YET-03) | B |
| Sütun Onboarding (4 adım + %) | — | İ (L) |
| Sütun Lead scanner | exhibitor_leads uçları oturumsuz (EMS E sınıfı) | İ (M) |
| Sütun Status | kontrat statüsü | B |
| Sayfalama | sayfalı uç | B |
| Satır → Exhibitor detail | kontrat kimliğiyle | B |

### 1.3 Ops — Exhibitor Detail (kontrat)

| öğe | bağlanır | durum |
|---|---|---|
| Hero: firma · AF no · sektör · temsilci · m² | `GET /api/contracts/:id` (+ firma kartı) | B |
| Hero: stand no · salon · "VIP buyer" rozeti | — | İ |
| "Issue badges" | yaka kartı kotası / kontrat bağı yok | İ (M) |
| "Message" | iletişim günlüğüne not (`POST /api/communications`, hedef kontrat) | B |
| Onboarding bandı (4 adım + genel %) | — | İ (L) |
| Checklist: Catalogue (son tarih) | fuar `catalogue_submission` etkin tarihi | B (tarih) · durum İ |
| Checklist: Stand design (son tarih + link) | fuar etkin tarihi + `contracts.stand_design_link` | B (tarih · link) · onay İ |
| Checklist: Build-up (tarihler) · görev listesi | fuar build-up etkin tarihleri | B (tarih) · görevler İ |
| Checklist: Badges | — | İ (M) |
| Lead scanner kartı (koltuk · lead · açılış) | açılış = fuar başlangıcı B; koltuk / lead | İ (M) |
| Contract & stand: no · tutar · ödenen · bakiye | kontrat detayı (para çifti) | B |
| "Open in Finance" | Finance › Contract | B |
| Stand: tip · m² · boş m² · katalog sayfası · stand tasarım linki · nakliye — OKUMA | `contracts` operasyon kolonları (016) | B |
| Aynı alanlar — DÜZENLEME | **S** `PUT /api/contracts/:id/operations` (`contracts.write`, kapsam YET-03, denetim YET-08) | S |
| Stand no | kontratta kolon yok (kat planı ↔ kontrat bağı kuyruğu) | İ (M) |
| "View on floor plan" | Ops › Floor plan | B |
| Key people | firmanın kişileri (`/api/customers/:id`, sales.read) | B |
| Documents: imzalı kontrat taraması · stand tasarım linki | `scan_link` · `stand_design_link` | B |
| Documents: "+ Upload" · diğer belgeler | dosya yükleme yok | İ (M) |
| İletişim günlüğü (Sentez §2) | `GET /api/communications` (hedef kontrat; `communications.read`) | B — 🔶 Project şablonunda bu kod YOK |

### 1.4 Ops — Floor plan

| öğe | bağlanır | durum |
|---|---|---|
| Salon sekmeleri | `GET /api/floorplan/halls?expo_id=` | B |
| "Open floor designer" · "Edit layout" | köprü: `nav.json` legacy → klasik `floorplan-builder.html` | B (köprü) |
| Tuval önizlemesi (stand haritası · araçlar · zoom · iğne) | editör klasikte | İ (L — taşıma) |
| Occupancy: stand sayısı + m² (sold / hold / available) | **S** floorplan-summary (aktif sürüm, durum bazında) | S |
| Stands listesi (kod · firma · m² · tip · durum) | `GET /api/floorplan/versions/:id/stands` | B |
| Stand → katılımcı bağlantısı | stand ↔ kontrat bağı yok | İ (M) |
| Export | — | İ (S) |

### 1.5 Ops — Visitor & Access

| öğe | bağlanır | durum |
|---|---|---|
| Sekme Visitors (sayı) | EMS `/api/visitors/paginated` | B |
| Sekme Conferences (sayı) | EMS `/api/visitors/conference-topics` | B |
| Sekme Access control | terminaller `GET /api/terminals?expo_id=` | B |
| Sekme Badges | yaka kartı şablonları `GET /api/badge-templates` + klasik editör köprüsü | B |
| (Sentez §2) Forms · Import | `GET /api/forms/expo/:id` + klasik form editörü / içe aktarma köprüsü | B (köprü) |
| Şerit Registered · Checked-in today | `/api/reports/summary` · `/api/checkins/stats/summary` | B |
| Şerit Confirmed · No-shows | bu durumlar veride yok | İ ×2 |
| Arama · Type · Source süzgeci | `/paginated` (`search` · `visitor_type` · `source`) | B |
| Status · Day süzgeci | — | İ ×2 |
| Export | `/api/visitors/export` | B |
| "Add visitor" | `POST /api/visitors/manual` (YET-25 kapısı) | B |
| Sütunlar: Visitor · Company / Role · Type · Badge ID · Source · Registered | `/paginated` satırı | B |
| Sütun Access zones | bölge modeli yok | İ (M) |
| Sütun Status | check-in durumu satırda varsa B; "Confirmed / Pending / No-show" yok | B (check-in) · İ |
| Toplu seçim kutuları | toplu işlem klasikte | İ (S) |
| Sayfalama | `/paginated` | B |

### 1.6 Ops — Communications

| öğe | bağlanır | durum |
|---|---|---|
| Sekme Campaigns | EMS `GET /api/campaigns` (fuar) | B |
| Sekme Templates | EMS `GET /api/email-templates` | B |
| Sekme Segments | kayıtlı segment yok (yalnız önizle / gönder ucu) | İ (M) |
| "New message" · "Start a message" · "Manage" | köprü: `nav.json` legacy → klasik kampanya / şablon ekranları | B (köprü) |
| Şerit Operational: Sent (7d) · Queued | **S** `GET /api/operations/communications-summary?expo_id=` (`email_queue`) | S |
| Şerit Operational: Bounce | gözlenemez (G9) | İ (M) |
| Şerit Marketing: Opted out | `email_unsubscribes` (aynı S uç) | S |
| Şerit Marketing: Consented · Avg open | onay modeli / şerit ortalaması yok | İ ×2 |
| OPS / MKT etiketi (şablon sınıfı) | şablonda sınıf bayrağı yok (envanter #46) | İ (M) |
| Kampanya tablosu: ad · alıcı · durum · açılma | `/api/campaigns` satırı (G13 / G14 notlarıyla) | B |
| Kampanya tablosu: tür · segment | — | İ ×2 |
| Operasyon zinciri (8 e-posta) bölümü | motor yok | İ (L) |

### 1.7 Ops — Reports

| öğe | bağlanır | durum |
|---|---|---|
| KPI Registrations | `/api/reports/summary` | B (hedef İ) |
| KPI Exhibitors ready | imzalı B; "ready / blocked" | İ |
| KPI Floor sold | R3 m² / hedef B; salon doluluğu | S (floorplan-summary) |
| KPI Check-in | `/api/checkins/stats/summary` | B |
| Registrations over time | `/api/reports/summary` günlük kayıt dizisi (CSS çubuk) | B |
| Exhibitor status (halka) | toplam imzalı B; dağılım | İ |
| Floor occupancy by hall | floorplan-summary | S |
| Visitor mix by type | `/api/reports/summary` `visitor_type_breakdown` | B |
| Saved & scheduled reports | rapor oluşturucu `/api/report-builder/saved` + takvimler | B |
| Range · panel CSV'leri | — | İ |
| "Schedule" | Finance › Scheduled reports | B |
| "Export all" | `/api/visitors/export` | B |
| R8: kayıt raporu (klasik) | köprü: klasik `reports.html` | B (köprü) |

## 2. Sales

### 2.1 Sales — My Work

| öğe | bağlanır | durum |
|---|---|---|
| Kuyruk "Follow-ups due" | `GET /api/follow-ups` (ILT-04) | B |
| Kuyruk "Quotes to chase" (cevapsız teklifler) | `GET /api/quotes?status=sent` | B |
| Kuyruk "Approvals" → imzalı, çevrilmemiş | `GET /api/convert-queue` / imzalı teklifler | B |
| Kuyruk "Incoming replies" | gelen e-posta yok (B4 inbound) | İ (L) |
| Satır düğmeleri Open · Done | kayda iner · `PUT /api/follow-ups/:id` | B |
| Satır düğmeleri Reply · Call · Send contract | — | İ |
| "New quote" | Sales › Quotes | B |
| "Filters" | — | İ (S) |
| Today (takvim) | bugünkü vadeli takipler | B — takvim etkinlikleri İ (M) |
| Quarter targets | kişi / çeyrek hedefi yok | İ (M) — bağlantı: Performance |
| LIVE rozeti | — | İ |

### 2.2 Sales — Mail (v1)

| öğe | bağlanır | durum |
|---|---|---|
| Görünüm "Sent" | iletişim günlüğü (yön out, kanal email) + `email_queue` durumu (ILT-03; echo rozeti ILT-05) | B |
| Görünüm "My follow-ups" | `/api/follow-ups` | B |
| Görünüm Inbox · Awaiting reply · Starred · Drafts | Gmail bağlantısı yok (ayrı karar) | İ ×4 (L) |
| Compose · Reply | sistemden gönderim yalnız teklif Send (ILT-01) | İ (L) |
| Hesap seçici (15 adres) · "Synced" | Gmail | İ ×2 |
| Arama | yüklenen liste üstünde | B |
| Expos (auto) klasörleri | gönderilen kaydın fuarı (teklif / kontrat) | B |
| Campaigns klasörleri | kampanya LIFFY / EMS'te | İ (M) |
| Liste satırı: alıcı · konu · zaman · teslim durumu · hedef | iletişim günlüğü satırı | B |
| Etiketler Known / New? / Exhibitor | — | İ |
| Okuma bölmesi: gövde | `GET /api/communications/:id` | B |
| Bağlam paneli: firma · ülke · sektör · kişi · geçmiş | firma kartı + iletişim günlüğü | B |
| Bağlam paneli: sahip uyarısı | YET-17 uyarısı (başka sahibin açık teklifi) | B |
| Bağlam paneli: intel / benzer firmalar · katılımcı uyarıları · "Add as Lead" | — | İ ×3 |

### 2.3 Sales — Pipeline

| öğe | bağlanır | durum |
|---|---|---|
| Sütunlar Draft · Sent · Signed · Declined | `GET /api/quotes` (durum; kapsam YET-03) | B |
| Sütunlar Lead · Contacted · Replied · Qualified | lead aşamaları LIFFY'de | İ ×4 (L) |
| Kart: firma · teklif no · tutar · sahip · yaş | teklif listesi satırı | B |
| Kart: m² · şehir · "next step" | — | İ |
| Bağlam: Open pipeline | teklif özet sayaçları | B |
| Bağlam: Weighted · Win rate | — | İ ×2 (M) |
| Süzgeç Expo · Sort | teklif listesi süzgeci | B (expo) · İ (sort) |
| "New deal" / "Add deal" | yeni teklif | B |

### 2.4 Sales — Quotes (mevcut teklif ekranı, setin düzeniyle)

| öğe | bağlanır | durum |
|---|---|---|
| Kâğıt: no · revizyon · satıcı bloğu · müşteri · fuar · tarih · geçerlilik · para birimi · satırlar · toplamlar | `GET/PUT /api/quotes/:id` (mevcut) | B |
| Konu · ödeme koşulu | `quotes`'ta alan yok (ölçüldü) | İ ×2 (S) |
| "Add line item" · düzenleme | mevcut | B |
| Durum + zaman çizelgesi: Drafted · Sent · Signed | teklif tarihleri | B |
| "Viewed N×" | izleme yok | İ (M) |
| "Mark as signed" · PDF | mevcut | B |
| "Send reminder" | — | İ (S) |
| El değiştirme kutusu (imza → kontrat) | mevcut çevirme | B |
| "Your commission" | YET-23 (teklifte komisyon önizlemesi yok) | İ (M) |

### 2.5 Sales — Companies (Customers + firma kartı)

| öğe | bağlanır | durum |
|---|---|---|
| Kimlik: ad · sektör · ülke / şehir · web · vergi no | `GET /api/customers/:id` | B (olan alanlar) |
| Kimlik: çalışan sayısı · rozetler (VIP / cluster) | — | İ |
| Düğmeler New quote · Log activity · Edit | mevcut (teklif · iletişim notu · firma düzenleme) | B |
| Sayaçlar Open deals · Contracts · Since | **S** `GET /api/customers/:id/card` | S |
| Sayaç Lifetime value | aynı uç — yalnız görünür tutarlar; kilitli kontrat varsa işaretli | S |
| Uyarılar | başka sahibin açık teklifi (YET-17) · açık bakiye (görünürse) | B |
| 4 sekme: Contracts · Quotes · Contacts · Communication | sette SEKME YOK (kartlar); mevcut verinin sekmeleri — ön-onaylı SAPMA 🔶 | B |
| Contracts sekmesi: başka satışçının kontratı = fuar · edisyon · m², TUTAR KİLİTLİ | **S** aynı uç — tutar SUNUCUDA süzülür (alan yok + bayrak), ekranda kilit (YET-26) | S |
| "Tutarı görsün" | kişi başı ezme (yeni kod, şablon satırı yok) | S |
| Dış kullanıcı | yalnız kendi kontratları (YET-15 tavanı aynen) | B — 🔶 |
| Affiliations | — | İ (M) |
| Activity | iletişim günlüğü | B |
| Account team | firma sahibi | B — "Ops liaison" İ |
| Quick facts | para birimi / kaynak / tipik stand yok | İ |

## 3. Finance

### 3.1 Finance — War Room (= R7)

| öğe | bağlanır | durum |
|---|---|---|
| KPI Revenue (yıl) + hedef % | R2 `period=year` | B |
| KPI Cash position | `GET /api/ledger/summary` `total_cash_eur` | B |
| KPI Outstanding (AR) + vadesi geçen | R4 toplam + yaş kovaları | B |
| KPI Commission accrued | ledger özeti komisyon borcu | B |
| Revenue vs target (aylık) | R2 aylık dizi (CSS çubuk) | B — hedef çizgisi İ |
| Top expos: Revenue | R7 fuar başına satış | B |
| Top expos: Costs · Margin · Cash in | fuar başına gider / marj tek uçta yok | İ ×3 (M) |
| Alerts: vadesi geçen | R4 | B |
| Alerts: blocked exhibitor · FX exposure · payout run | — | İ ×3 |
| Cash by account | `GET /api/ledger/accounts` | B |
| Receivables aging | R4 kovaları (RAP-10) | B |
| "Board pack" | — | İ (M) |
| R7 mevcut bölümleri (fuar başına satış · aktivite · açık bakiye) | aynen | B |

### 3.2 Finance — Contract (mevcut ui2 kontrat + setin düzeni)

| öğe | bağlanır | durum |
|---|---|---|
| Başlık: firma · AF no · fuar · imza tarihi · temsilci | `GET /api/contracts/:id` | B |
| Başlık: stand | — | İ (M) |
| Büyük rakamlar: tutar · ödenen · bakiye (para çifti) | mevcut | B |
| Satırlar + EUR karşılığı | mevcut (satır EUR) | B |
| Satır başı Comm % · Commission | satır bazlı komisyon modeli yok | İ ×2 (M) |
| Transactions (tarih · yöntem · tutar · kur · EUR) | kontrat ödemeleri | B |
| Transactions: tür etiketi · "Scheduled" satırı | ödeme planı ayrı listede (B) | B / İ |
| FX snapshot: kontrat kuru | `contracts.exchange_rate` | B — canlı kur / kaynak İ |
| Commission bloğu | mevcut, YET-23 ile | B |
| Parties | firma kişisi · temsilci | B — "Finance owner" İ |
| "Record payment" | köprü: klasik kontrat detayı (`nav.json` legacy) | B (köprü) — ui2 formu kuyruk (S) |
| "Note" | iletişim günlüğü notu | B |
| "PDF" | tekliften doğan kontratta teklif PDF'i | B / İ |

### 3.3 Finance — Commissions (Agents + ekstre)

| öğe | bağlanır | durum |
|---|---|---|
| Şerit Agents (sayı) | `GET /api/sales-agents` | B |
| Şerit Accrued · Paid · Due | `GET /api/commissions` + ledger özeti | B |
| Tablo: temsilci · tür · kontrat sayısı · hak edilen · ödenen · bakiye | temsilci listesi + ekstre (`/api/agents/:id/statement`) | B |
| Tablo: Blended % · Status | — | İ ×2 |
| Arama · Type süzgeci | liste üstünde | B |
| Export | liste dışa aktarımı | B |
| "Add agent" | köprü: klasik temsilci ekranı (mevcut legacy öğe) | B (köprü) |
| "Run payout" · "Approve & run payout" · Next payout run kartı | toplu ödeme motoru yok (ödeme temsilci ekstresinden tek tek) | İ (M) |
| Per-line commission kartı | — | İ (M) |

### 3.4 Finance — Ledger

| öğe | bağlanır | durum |
|---|---|---|
| Hesap sekmeleri + bakiyeler | `GET /api/ledger/accounts` | B |
| Consolidated toplam | `GET /api/ledger/summary` | B |
| Özet: Opening · In · Out · Closing | hesap ekstresi (seçili hesap) | B — konsolide İ |
| Defter tablosu (tarih · ref · açıklama · yöntem · giriş / çıkış · kur · EUR · bakiye) | hesap ekstresi `GET /api/ledger/accounts/:id` | B |
| Konsolide (tüm hesaplar) tek liste | — | İ (M) |
| Arama · Type · Method | — | İ |
| "New entry" | Transfers · Expenses formları | B |
| Export | ekstre dışa aktarımı | B |

### 3.5 Finance — Expo Finance (P&L tek ekran)

| öğe | bağlanır | durum |
|---|---|---|
| Fuar seçimi | fuar listesi | B |
| KPI Revenue | R3 / R6 brüt | B |
| KPI Costs | R6 gider gerçekleşen | B |
| KPI Gross margin · Net profit | sunucuda hazır toplam yoksa | İ (S) |
| Budget vs actual tablosu | R6 | B |
| Margin halkası | — | İ |
| Cluster split · Combined / fuar anahtarı | cluster toplamı yok | İ (M) |
| Cash vs invoiced: Invoiced · Collected · Outstanding | R3 `gross` · `paid` · `open` | B |
| Overdue (90+) | R4 fuar süzgeci | B / İ |
| Export | R6 / R3 dışa aktarım | B |

## 4. Mobile (390 px; terminal akışı DEĞİŞMEZ)

| ekran | öğe | bağlanır | durum |
|---|---|---|---|
| Dashboard | fuar adı | seçilen fuar | B |
| Dashboard | KPI Checked-in (bugün) · Registered | `/api/checkins/stats/summary` · `/api/reports/summary` | B |
| Dashboard | KPI On-site now | çıkış kaydı yok | İ (M) |
| Dashboard | KPI Exhibitors ready | imzalı B; "ready" İ | B / İ |
| Dashboard | Check-in traffic | saatlik dağılım (CSS çubuk) | B |
| Dashboard | "Doors open" canlı şerit · "Needs attention" | — | İ ×2 |
| Dashboard | Quick actions: Scan · Visitors · Floor | ilgili ekranlar | B |
| Dashboard | Quick action: Print | rozet baskısı terminalde | İ — köprü |
| Dashboard | Recent check-ins | `GET /api/checkins?expo_id=` | B |
| Scan | kod / e-posta ile bulma | `/api/visitors/paginated?search=` (oturum) | B |
| Scan | kamera QR | tarayıcı destekliyorsa (BarcodeDetector); kütüphane eklenmez | B / İ |
| Scan | Check-in | `POST /api/checkins` (oturum JWT'si — ölçüldü) | B |
| Scan | Print badge | klasik rozet penceresi (`badge.html`) | B |
| Scan | Lead modu | lead uçları oturumsuz (EMS E sınıfı) → klasik lead scanner köprüsü | İ — köprü |
| Scan | terminal anahtarıyla tarama | köprü: klasik terminal ekranı (yeni kimlik yolu AÇILMAZ) | B (köprü) |
| Visitor List | arama · liste · sayaç | `/api/visitors/paginated` | B |
| Visitor List | süzgeç VIP · Press (tür) | `visitor_type` | B |
| Visitor List | süzgeç Checked-in · Pending | uç süzgeci yoksa | İ |
| Visitor List | satırdan check-in | `POST /api/checkins` | B |
| Sekme çubuğu | Home · Visitors · Scan · Floor · More | ilgili ekranlar | B |

## 5. Settings — Appearance

| öğe | bağlanır | durum |
|---|---|---|
| Tema kartları — setteki 15 tema (12 Ops + 3 warm), varsayılan Vermillion | `tokens.css` `html[data-theme]` (UI-04) | B |
| Seçimin kişiye kaydı (cihaz değişince gelir) | **S** kullanıcı kaydında tek alan + `PUT /api/user-auth/preferences` (yalnız KENDİ tercihi) | S |
| Mode: Light | geçerli durum | B |
| Mode: Dark · System | — | İ ×2 (M) |
| Display: Comfortable / Compact · Reduce motion | — | İ ×3 (S) |
| Theme library "+ Add" | 15 temanın hepsi seçilebilir (Y4) → ayrı raf yok | — |
| Ayar menüsü: Profile | "Who is signed in" | B |
| Ayar menüsü: Security | şifre değiştirme (`/api/user-auth/change-password`) | B |
| Ayar menüsü: Team & roles | Admin › Users (yetkiliyse) | B |
| Ayar menüsü: Notifications · Billing · Integrations | — | İ ×3 |

---

## 6. Bu pakette açılacak ucuz uçlar (S) — özet

| uç | okur / yazar | izin + kapsam |
|---|---|---|
| `GET /api/operations/dashboard?expo_id=` | fuar + geri sayım + etkin son tarihler | iç kullanıcı `operations.read`; fuar sahipliği EMS-01 |
| `GET /api/operations/floorplan-summary?expo_id=` | aktif sürüm: salon × durum → stand sayısı + m² | aynı |
| `GET /api/operations/communications-summary?expo_id=` | `email_queue` son 7 gün gönderilen / bekleyen · `email_unsubscribes` | aynı |
| `PUT /api/contracts/:id/operations` | stand tipi · m² · boş m² · katalog sayfası · stand tasarım linki · nakliye | `contracts.write` + YET-03 + denetim (YET-08) |
| `GET /api/customers/:id/card` | firma kartı sayaçları + kontrat / teklif listeleri; görünmeyen tutar SUNUCUDA süzülür | `sales.read` + YET-26 |
| `PUT /api/user-auth/preferences` | kullanıcının KENDİ tema tercihi | oturum sahibi (yetki matrisi değil) |

Kuyruk (işaretlenen her öğe: ne · hangi ekran · S/M/L) defter kaydındadır — `docs/audits/EKSIK_ENVANTERI_2026-11-11.md` §4'ün devamı.

---

## 7. Uygulama sonrası (11 Kas, paket kapanışı) — haritadan SAPANLAR

Bu harita paketin PLANIYDI (ön ölçüm). Uygulamada ölçümle değişenler — ayrıntı ve gerekçe defterde ([defter:2026-11-11 PAKET UI-TAM 4. PARÇA] …
[defter:2026-11-11 PAKET UI-TAM KAPANIŞ]):

| harita | uygulama |
|---|---|
| §6 "ucuz uç" tablosu 6 uç | + `GET /api/operations/exhibitors` · `GET /api/operations/expos` (hafif fuar seçici listesi) · `GET /api/communications/sent` · `GET /api/commissions/agents` · `GET /api/user-auth/preferences` · alan ekleri: takip `due_today` · teklif `sums_eur` + `?expo_id=` · bütçe `totals` |
| §6 operasyon alanları yazımında "m²" | `sqm` YAZILMAZ (göçmüş kontratta ölçünün m² yedeği — RAP-04); beş alan yazılır |
| §4 Scan → Check-in = `POST /api/checkins` (B) | İŞARETLİ — uç yalnız rozet-baskı terminali etiketini kabul ediyor; check-in klasik tarama ekranında (köprü) |
| §4 Visitor List satırdan check-in (B) | İŞARETLİ (aynı neden) |
| §3.4 Ledger dışa aktarım (B) | İŞARETLİ (ekstre ucunda dışa aktarım yok) |
| §3.5 Gross margin / Net profit (İ — S) | İŞARETLİ kaldı (marj tanımı kararı yok) |
| §2.3 Pipeline lead sütunları | dört aşama tek işaretli kutuda (pano = dört gerçek sütun) |
| §2.2 Mail thread | seçili e-postanın ait olduğu kaydın iletişim günlüğü |
