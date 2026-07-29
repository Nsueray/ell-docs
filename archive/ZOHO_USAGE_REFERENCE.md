# Elan Expo — Zoho CRM Kullanım Referansı

**Versiyon:** 1.0
**Tarih:** 6 Mayıs 2026
**Hazırlayan:** Suer Ay (CEO) ile yapılan walkthrough oturumu, Claude tarafından derlendi
**Amaç:** ELL ekosistemi (ELIZA + LIFFY + Leena) tasarımı için, mevcut Zoho CRM kullanımının tam dökümü. Bu dosya LIFFY/ELIZA/Leena chat'leri ve dış AI review (ChatGPT, Gemini) için ortak referans noktasıdır.

---

## Bölüm 1 — Yönetici Özeti

Elan Expo, Zoho CRM'i 2018'den beri kullanıyor. Şirketin tüm ticari verisi ve operasyonel akışı bu sistemde toplanmış durumda. Zoho retirement hedefi **Ocak 2027** (ADR-008).

**Anahtar gerçekler:**

- **18,197 firma**, **17,675 contact**, **586,910 lead** Zoho'da kayıtlı
- **202 fuar** Expos modülünde tanımlı
- **242 ürün** Products modülünde
- **150 sales agent** (iç çalışan + freelance + dış acenta) Sales Agents modülünde
- **Aktif kullanılan modül sayısı:** 13
- **Pasif/kullanılmayan modül sayısı:** 25+
- **Öne çıkan otomasyon:** Sales Contract signed → tetiklenen email zinciri (8 mail tipi)

**ELL'e taşınması gereken iş yükü** sadece "CRM verisi" değil; aynı zamanda **muhasebe (Expenses + Revenues), operasyonel raporlama (Reports), fuar operasyon yönetimi (Expos), ve katalog/ödeme tahsilat süreçleri.**

---

## Bölüm 2 — İş Akışı: Lead'ten İmzalı Sales Contract'a

```
[1] Hazırlık (proje ekibi - Yaprak)
    ├─ Products oluştur (PES 410, RF 350, vb.)
    └─ Expos oluştur (MegaClima Algeria 2026, vb.)

[2] Lead toplama (satışçılar - Bengü, Cynthia, Damilola, Elif, vb.)
    ├─ Manuel olarak Zoho'ya lead gir
    └─ Web sitesi "Contact Us" formu → otomatik Zoho'ya düşer

[3] Outreach (satışçı)
    ├─ Lead'e email at, takip et
    └─ İlgilenen lead'e Quote aç
        ├─ Subject: "{ExpoName}-{CompanyName}-{XM2}"
        ├─ Quoted Items: PES (M² × birim fiyat), RF (sabit), Discount (varsa)
        ├─ Quote Stage: Draft
        └─ Currency: EUR/NGN/MAD/TL (fuara göre)

[4] Quote imzalanma (satışçı + müşteri)
    ├─ Satışçı Quote Stage'i "Signed" yapar
    ├─ → Otomatik email gider: PROJE EKİBİ + CEO bilgilendirilir
    └─ AF Numarası burada atanır (örn. A809455)

[5] Convert (proje ekibi - Yaprak)
    ├─ Quote sayfasında "Convert" butonuna basar
    ├─ Lead → Contact + Company'ye dönüşür (Lead silinir)
    ├─ Quote → Sales Contract'a dönüşür
    ├─ Eksik/hatalı bilgiler kontrol edilir, satışçının bilmediği alanlar
    │  proje ekibi tarafından doldurulur
    └─ Bu adım resmi onay değil ama doğal kontrol kapısı işlevi görüyor

[6] Sales Contract aktif
    ├─ Stand Type, M2, Sales Group, Transportation gibi detaylar girilir
    ├─ Komisyon yapısı tanımlanır (Agent / SR / SD - 3 kademe)
    ├─ Announcement checkbox'ları işaretlenir → email akışları tetiklenir
    │   • Welcome Mail
    │   • Catalogue form mail (→ Catalogues modülüne kayıt oluşur)
    │   • Stand Design Mail
    │   • Boost Mail
    │   • Extra Service Mail
    │   • BuildUp Rules Email
    │   • Payment Reminder
    │   • Internal Notification
    └─ Payment Method, Validity, Net Total kayıt edilir

[7] Tahsilat (lokal ofisler)
    └─ Revenues modülüne kayıt girilir
        ├─ Sales Contract'a bağlanır
        ├─ Receipt No, Payment Method, Currency, Exchange Rate
        ├─ Payment Terms subform: Date + Payment(amount) + Note
        └─ "Kim ne kadar borçlu" Revenues + Sales Contract birlikte gösterir

[8] Operasyon (proje ekibi)
    └─ Expense'ler girilir (Salaries, Rent, Sales Commission, vb.)
        ├─ Per ofis: HQ, Morocco, Nigeria, Kenya, vb.
        ├─ Multi-currency: EUR + Euro Rate kaydı
        └─ Sales Commission de Expenses içinde "expense type" olarak yazılıyor
```

---

## Bölüm 3 — Aktif Modüller (Detaylı)

### 3.1 Analytics

**Durum:** Çok aktif kullanılıyor.

**Ne için:** Yıllık ve haftalık performans takibi. Dashboard üzerinden CEO ve sales manager hedefleri görüyor.

**Kullanılan görseller:**
- Revenue Current Week / Area Current Week
- Area THIS MONTH / Revenue THIS MONTH (önceki ay karşılaştırmalı, yüzde değişim)
- Signed Contracts This Month
- FY Area Target (gauge: tamamlanan vs hedef)
- FY Revenue Target (bar: achieved vs target)
- Revenue FY BY EXPO (top expolar, sum of grand total + record count)
- Area FY BY EXPO (top expolar, sum of total m² + record count)
- Revenue FY BY REPS (per satışçı performansı)
- Area FY BY REPS

**ELL karşılığı:** ELIZA War Room dashboard. Mevcut FINANCE_MODULE.md'de bu metriklerin bir kısmı tanımlı, bir kısmı eksik.

---

### 3.2 Leads

**Durum:** Aktif. Toplam **586,910 kayıt**.

**Ne için:** Henüz convert olmamış ham veri. Satışçının müşteriye çevirmek için temas kurduğu liste.

**Kayıt kaynakları:**
1. Manuel giriş (satışçı veya freelance data entry)
2. Web formu — şirket websitelerindeki "Contact Us" form'larından otomatik
3. Geçmişte Zoho Forms üzerinden public data entry (freelance'lar için)

**Önemli alanlar:**
- Lead Owner (atanmış sales agent)
- Lead Type (Unknown, Customer, Prospect)
- Country, Company, Last Name, Email, Created Time
- Sector (HVAC, Construction, vb.)
- Company Response, Réponse de l'entreprise

**Lead durumları:**
- **Today / May 5 / Apr 23** gibi follow-up tarihi tag'leri ile takip ediliyor
- Convert olunca Lead silinir, Company + Contact oluşur

**ELL karşılığı:** LIFFY persons tablosu, lifecycle_stage='lead'. ADR-014 ve LIFFY_PHASE_1_MVP_PLAN W3 bu modeli zaten ele alıyor.

**KRİTİK NOT:** 510K lead Zoho'da kalıyor (ADR-008/D9), sadece ~75K LIFFY'ye import edildi. Tam taşıma Ocak 2027.

---

### 3.3 Contacts

**Durum:** Aktif. Toplam **17,675 kayıt**.

**Ne için:** Convert olmuş kişiler (firma temsilcisi/decision maker). Quote açılmadan önce veya Sales Contract sonrası.

**Görünen alan grupları:**

**Contact Information:**
- Contact Owner, Contact Name, Email, Phone, Mobile, Title, Home Phone
- Created By, Modified By
- Email Opt Out
- Lead Score
- Previous Exhibitor (boolean — daha önce fuara katılmış mı)
- Currency, Exchange Rate
- Layout (örn. "International Sales")
- Social Lead ID

**Company Details (denormalize):**
- Company Name (Companies'e referans), Department, Assistant, Asst Phone
- Secondary Email, Reporting To, Other Phone, Fax

**Detailed Information:**
- Sector (HVAC/Decoration/Construction/Water Systems/Food Machinery/Ceramics/Information Technology/Electricity)
- Product Groups
- Contact Type (Customer)
- Ownership (International)
- Interested Exhibitions
- Lead Source, Date of Birth, Skype ID, Twitter
- Sales Agent

**Address Information:**
- Mailing Street, Mailing Zip, Mailing City, Country

**Related Lists:**
- Notes, Connected Records, Attachments, Cadences, Potentials, Open Activities, Closed Activities, Products, Invited Meetings, **Quotes (1)**, **Sales Contracts (1)**, Purchase Orders, **Emails (1)**, Sales Agents, Product Groups1, Invoices, Campaigns, Social, Reporting Contacts, **Kurum Baskani**, **Catalogue Page**, Primary Contact, Secondary Contact, Zoho Survey, Voice of the Customer

**ELL karşılığı:** persons tablosu, lifecycle_stage='contact' veya 'customer'.

---

### 3.4 Companies (Zoho'da "Accounts")

**Durum:** Aktif. Toplam **18,197 kayıt**.

**Ne için:** Convert olmuş firmalar.

**Görünen alan grupları:**

**Company Information:**
- Company Owner, Company Name, Company Email, Phone, Website, Fax
- Created By, Modified By
- Parent Company
- Currency, Exchange Rate
- Layout

**Detailed Information:**
- Account Type (Customer)
- Ownership (International)
- Sector
- Product Groups
- Related Bodies - Expos
- Previous Exhibitor

**Address Information:**
- Country, Billing Street, Billing City, Billing Code

**Bank Details (KRİTİK):**
- Tax Office
- Tax ID
- Bank Name
- Branch Name
- IBAN Number

**Related Lists:**
- Notes, Connected Records, Attachments, Potentials, **Contacts (1)**, Open Activities, **Emails**, Closed Activities, Products, **Quotes (1)**, **Sales Contracts (1)**, Invoices, **Member Companies**, **Kurumlar**, Product Groups1, Social, **Sales Agent**, **Catalogue**, **Expense**, **Expensess**, **Revenue**

**ELL karşılığı:** companies tablosu (LIFFY_PHASE_1_MVP_PLAN W1-W2). Bank details kısmı LIFFY blueprint'te eksik — ELIZA tarafına da gerekebilir (faturalama).

---

### 3.5 Quotes

**Durum:** Aktif. Çok yoğun kullanılıyor.

**Quote Stage'leri:** Draft → Signed (bazen Cancelled)

**Subject formatı:** `{ExpoName} - {CompanyName} - {M²}m²` veya `{ExpoName}-{CompanyName}-{M²}sqm`
- Örnekler: "MegaClima Algeria - Polidoro S.p.A. - 9M2", "BUILDEXPO2026-RAYA ENGR-9SQM", "MEGAWATER2026-PANAR PIPES-9SQM"

**Görünen alan grupları:**

**Quote Information:**
- Convert to Sales Contract (boolean trigger)
- Quote Owner, Subject
- Expo Name (Expos modülüne referans)
- Contact Name (Contacts'a referans)
- Company Name (Companies'e referans)
- Country of Company
- Created By, Modified By
- Layout (Admin / International Sales / vb.)
- Quote Stage (Draft / Signed / Cancelled)
- Valid Until
- AF No (Signed olunca atanır, sequence: A809455 gibi)
- Currency, Exchange Rate

**Quoted Items (line items):**
- S.NO, Product Name (Products'a referans), List Price, Quantity, Amount, Discount, Tax, Total
- Tipik dizilim: PES (Participation with Equipped Stand) + RF (Registration Fee) + Discount

**Sub Total / Total (footer)**

**Para birimleri ekran görüntülerinde:** EUR, NGN (₦), MAD, TL

**Related Lists:** Notes, Connected Records, **Sales Contracts (1)**, Attachments, Open Activities, Closed Activities, Emails, **Stand Leads**

**Convert akışı:**
1. Satışçı Quote Stage'i "Signed" yapar
2. Sistem otomatik email atar: proje ekibi (Yaprak) + CEO bilgilendirilir
3. Yaprak Quote sayfasındaki "Convert" butonuna basar
4. Quote → Sales Contract'a dönüşür
5. Lead → Company + Contact'a dönüşür (eğer hâlâ Lead ise)
6. Yaprak eksik bilgileri tamamlar, satışçının doldurmadığı alanları doldurur

**Bu adım gizli onay kapısıdır:**
> Suer'in ifadesi: "Kontrol var mı? Evet vardır ama asıl amaç o değil. Ama doğal bir kontrol oluyor."

**ELL karşılığı:** LIFFY Phase 1.5 Quote modülü + ELIZA Quote Approval Flow. ADR-003 (quote-contract separation) ve LIFFY_PHASE_1_MVP_PLAN'da ele alınıyor.

---

### 3.6 Sales Contracts (Zoho'da "Sales Orders")

**Durum:** Aktif. Quote → Convert sonrası oluşur.

**Görünen alan grupları:**

**Sales Contract Information:**
- Status (Valid / Cancelled)
- Sales Contract Owner
- Subject (Quote'tan inherit)
- Quote Name (Quote'a back-reference)
- AF Number (PostgreSQL SEQUENCE benzeri, A809455 formatı)
- Contract Date
- Expo Name, Expo Date
- Contact Name, Country of Company
- Company Name
- Sales Agent (Sales Agents modülüne referans)
- Agent Name (varsa dış agent)
- Sales Type (Exhibition / vb.)
- Created By, Modified By
- Potential Name (genelde boş)
- Currency, Exchange Rate
- Advertising

**Ordered Items (Quote'tan inherit):**
- Product Name, List Price, Quantity, Amount, Discount, Tax, Total
- Sub Total, Discount, Tax, Adjustment, Grand Total

**Terms and Conditions:** serbest text alanı

**Sales Contract Details:**
- Stand Type (Equipped / vb.)
- Sales Group (International / Local / Nigeria Office / vb.)
- Transportation (Excluded / Included)
- M2, Free M2, Total M2
- Catalogue Page (numarası/atıf)
- Scan Link (Google Drive link, taranan imzalı kontrat)
- Stand Design Link

**Received Payments (subform):**
- Date, Payment(€), Note
- Total Payment, Balance

**Payment Details:**
- Payment Method (Bank Transfer / vb.)
- Validity, Balance Details
- Reason for Cancellation
- Payment Done, Net Total

**Agent Comissions:**
- Agent %
- Agent Comission (hesaplanan tutar)
- Agent Comission Paid
- Agent Com. Done (boolean)
- Agent Comissions Note

**SR Comissions** (SR = Sales Representative, içerideki satışçı):
- Registration Fee
- SR %
- SR Comission
- SR Comission Paid
- SR Com. Done
- SR Comission Notes
- SR Comission Remaining

**Sales Director Comissions** (SD = Sales Director, satışçının müdürü):
- SD %
- SD Comission
- SD Comission Paid
- SD Com. Done
- SD Comission Notes
- SD Remaining Payment

> **NOT:** SD genelde Elif (Sales Manager). Ama Suer şunu söyledi: "değişken olabilmeli." Ekip yapısı zamanla değişiyor — Bengü düz satışçıydı, geçen ay ekip lideri oldu, ona bağlı satışçılar var. Müdürler hem kendi satışlarından hem ekibinin satışlarından komisyon alıyor.

**Announcement (8 email tetikleyici checkbox):**
- Internal Notification
- Send Them All Now (master switch — hepsini birden tetikle)
- Welcome Mail
- Catalogue form mail
- Stand Design Mail
- Boost Mail
- Extra Service Mail
- BuildUp Rules Email
- Payment Reminder
- Badge

**Description Information:** serbest text

**Cancelled Fields** (iptal durumunda):
- 1st Payment / 1st Payment Details
- 2nd Payment / 2nd Payment Details
- 3. Date/Amount/Type / 4. Date/Amount/Type
- Remaining Payment

**Related Lists:** Notes, Connected Records, Invoices, Attachments, Open Activities, Closed Activities, Emails, **Catalogue**

**ELL karşılığı:** ELIZA Sales Contracts (ADR-001 ELIZA Commercial Core). LIFFY'de oluşturulmaz — ELIZA approval sonrası ELIZA yazar, Leena okur.

**KRİTİK:** Bu modül ekibin tahmin ettiğinden çok daha karmaşık. Phase 1.5 (Quote modülü, 4-6 hafta) bunu değil sadece Quote'u kapsıyor. Sales Contract'a geçiş — özellikle 3-kademe komisyon (Agent/SR/SD) ve 8-email tetikleyici Announcement — Phase 2'ye taşınacak ama planlanan kapsam yetersiz olabilir.

---

### 3.7 Expenses

**Durum:** Aktif. Tüm ofisler harcamalarını buraya giriyor.

**Ne için:** Şirketin tüm operasyonel harcamaları + Sales Commission ödemeleri.

**Örnek kayıt — "salaire sarah mars 2026":**
- Expense Owner: Morocco Office
- Fiscal Year: 2026
- Expense Description: salaire sarah mars 2026
- Expense Category: OFFICE EXPENCES
- Expense Type: Salaries/Wages
- Exp. ID: EXP-101267-HQ
- Payee Name: Sarah Hamza
- Vendor Description: -
- Created By: Morocco Office
- Budgeted: MAD 4,612.00 (€422.34)
- Currency: MAD, Exchange Rate: 10.92
- Due Date, Payment Terms, Invoice/Receipt
- Payments subform: Date, Payment(MAD), Created By, Note, Euro Rate
- Total Payment: MAD 4,612.00 (€422.34)
- Status: Fully Payed

**Expense Categories:**
- OFFICE EXPENCES
- SALES COSTS

**Expense Types:**
- Salaries/Wages
- Communication/Technology/Software
- Rent/Maintenance/Utilities (electricity, water, gas)
- Taxes/Legal Expenses/Bank Fees
- HQ Sales Commission (KRITIK — Sales Commission burada giriliyor)

**Currency'ler:** MAD (Morocco), TL (Türkiye), EUR, NGN

**Expo bağlantısı:** "Expo Name" alanı var → fuara göre maliyet attribution mümkün
- Örn: Sales Commission expense'leri "Nigeria Build Expo 2026", "Mega Clima Nigeria 2026" gibi expo'lara bağlanmış

**Office'ler:** HQ, Morocco Office, Nigeria, Kenya

**Yaklaşık hacim (Image 2'den görünen filterlar):**
- Toplam görünen kayıt: 589 (sadece HQ filter)
- Pixad Ex...: 10
- ödeme t...: 42

**ELL karşılığı:** ELIZA Finance Module — Expenses tablosu. FINANCE_MODULE.md mevcut ama basit — Zoho'daki **multi-office, multi-currency, payment subform, expense categorization, expo attribution** kompleksitesi tam yansıtılmamış.

---

### 3.8 Revenues (Custom Module 15)

**Durum:** Aktif. Tüm ofisler gelirleri ve tahsilatlarını giriyor.

**Ne için:** Cash flow takibi + borç takibi. Sales Contract = anlaşılan tutar; Revenues = gerçekten tahsil edilen.

**Örnek kayıt — "Participation Fees" Panar Pipes Limited:**
- Revenue Owner: Elan Exhibitions West Africa
- Modified By: Elan Exhibitions West Africa
- Payer Company: Panar Pipes Limited
- Income Description: Participation Fees
- Income Category: Expo Participation
- Expo Name: Nigeria Mega Water Expo 2026
- Created By: Elan Exhibitions West Africa
- Receipt No: 92328
- Exchange Rate: 1880
- Currency: NGN
- Payment Method: Bank Transfer / SWIFT

**Payment Date / Payment Terms (subform):**
- Date | Payment(₦) | Note
- Örn: 27.04.2026 | ₦3,547,500.00 (€2,217.19) | (boş)
- Total Payment: ₦3,547,500.00 (€2,217.19)

**Income Categories (örnekler):**
- Expo Participation
- Sponsorship Income
- Extra Equipment

**Income Descriptions:**
- Participation Fees
- Sponsorship Fee
- Extra Equipment / Extra Stand Materials

**Görünen toplam kayıt:** 731

**Currency'ler ekran görüntülerinde:** EUR, NGN, MAD, TL

**Sales Contract bağlantısı:** Var. Revenues sales contract ile bağlantılı, "kimin ne kadar borcu kaldı" bunlar üzerinden hesaplanıyor.

**ELL karşılığı:** ELIZA Finance Module — Revenues tablosu. FINANCE_MODULE.md'de explicit yok. Sales Contract toplam tutar + Revenues tahsilat → Open Balance hesaplaması ELIZA tarafında olmalı.

> **MİMARİ NOTU:** Sales Contract'ta "Received Payments" subform var, Revenues'de de "Payment Date" subform var. Şu an çift kaynak — ya satıcı Sales Contract içinde ya proje ekibi Revenues içinde tahsilat giriyor. Bu **Veri tutarsızlık riski** taşıyor. ELL tasarımında tek doğruluk kaynağı olmalı (kanonik: Revenues, Sales Contract'ta sadece toplam balance gösterilir).

---

### 3.9 Reports

**Durum:** Aktif. Çok yoğun kullanılıyor (özellikle Yaprak).

**Ne için:** Operasyonel + finansal + veri-girişi takibi. Multi-amaçlı.

**Recently Viewed Reports (örnekler):**

**Per-fuar Visitor Registration raporları:**
- MC Nigeria Visitor Registration Pixad
- MC Nigeria 2026 Visitor Registration
- MC Nigeria 2026 Visitor Registration - Landing Page
- Mega Clima Nigeria 2026 Workshop Registration
- Pixad - Mega Horeca Nigeria 2026
- Nigeria 2025 Visitor Registration 2025 - Pixad
- Nigeria Engineering Expo - Pixad
- Morocco Madesign Expo 2025 - Pixad
- Ghana Visitor Records - Pixad
- Morocco Sigma Expo 2025 Visitor Registration - Pixad

**Per-ülke Data Entry takip raporları:**
- Kenya Office Data
- Nigeria Weekly Data Entry
- Nigeria Daily Data Entry
- Data Nigeria
- China Office Weekly Data Entry
- Kenya Weekly Data Entry
- Morocco Weekly Data Entry
- Weekly Nigeria DataBase Report
- Weekly Kenya DataBase Report

**Per-agent Ödeme Takip raporları:**
- Anka Ödeme Takip 2026 (Anka Fuarcılık komisyon ödemeleri)
- Sinerji Ödeme Takip 2026 (Sinerji International Exhibitions Ltd.)
- Mega Clima Nigeria Ödeme Takip 2026
- Bengü Sales Comm

**Çoğu Yaprak (yaprak@elan-expo.com) tarafından oluşturulmuş.**

**ELL karşılığı:** ELIZA War Room dashboard'lara dönüşmesi gereken farklı raporlama ihtiyaçları. INTELLIGENCE_ROADMAP.md'de bu ihtiyaçların önemli bir kısmı eksik — özellikle:
- Veri girişi takibi (data entry productivity per office)
- Per-agent komisyon takibi
- Per-fuar visitor registration funnel

> **NOT:** Visitor Registration raporları aslında Leena'ya ait olacak (Visitors modülü Leena'ya devredildi). Ama veri Zoho'da olduğu için raporlar hâlâ orada üretiliyor.

---

### 3.10 Expos (Zoho'da "Vendors")

**Durum:** Aktif. Toplam **202 fuar**.

**Ne için:** Tüm fuarların master kayıtları. Quote/Sales Contract/Expense/Revenue/Visitor bunlara bağlanır.

**Örnek kayıt: Morocco Siema Expo 2026**

**Expo Information:**
- Expo Name: Morocco Siema Expo 2026
- Website: http://www.siemamaroc.com/
- Sector: Food / Agriculture
- City: Casablanca
- Country: Morocco
- GL Account: Main Organizer (vs "Agent")
- Status: Active
- Currency: EUR, Exchange Rate: 1
- Country..: Morocco (duplicate alan)
- Email_Template_ID: -
- Email Opt Out: -
- Start Date: 22.09.2026
- End Date: 24.09.2026
- Created By: Elan Exhibitions, 29 Jul 2025
- Modified By: Elan Exhibitions, 5 Mar 2026
- Imported tag

**Operation Team:**
- Istanbul Contact: Ms. Yaprak GUZELCIK
- Istanbul Phone: +90 850 255 53 77
- Istanbul Email: yaprak@elan-expo.com
- Local Contact: Mrs. Meriem Houmaid
- Local Phone: +212 661-849913
- Local Email: maroc@elan-expo.net

**Online Forms:**
- Catalogue Form: https://zfrmz.com/xWn4mwxcEX2lgahNYps3
- Form2: -
- Form3: -

**Stand Contractor:**
- Contractor Company: Plus Design
- Contractor Contact: Andrew Maalouf
- Contractor Email: andrew@plusdesignmaroc.com
- Contractor Phone: +212 618-243235
- BuildUp Day1: 20.09.2026
- BuildUp Day2: 21.09.2026
- Venue Permission Day: 17.09.2026
- Deadline Date: 23.08.2026
- Extra Equipment List: -

**Visa:**
- Visa Email: elan02@elan-expo.com
- Visa Phone: +90 850 255 53 77

**Travel:**
- Travel Name: 212Tour
- Travel Contact: Mr. Furkan GUNAY
- Travel Email: furkan@212tur.com
- Travel Phone: +90 533 209 53 78

**Forwarder:**
- Forwarder Name: Global Event Logistics
- Forwarder Contact: Mr. Antonio Barhouche
- Forwarder Email: Antonio.Barhouche@gel-eventlogistics.com
- Forwarder Phone: +961 1 496059
- Turkish Forwarder Contact / Company / Email / Phone: -
- Shippment Deadline: -

**Hostess:**
- Agency Name: Elan Expo Maroc
- Agency Contact: Ms. Sarah HAMZA
- Agency Email: casablanca@elanexpo.net
- Agency Phone: +212 665-760760

**Catering:**
- Caterer Company: Elan Expo Maroc
- Caterer Contact: Ms. Sarah HAMZA
- Caterer Email: casablanca@elanexpo.net
- Catering Phone: +212 665-760760

**Expo Stats:**
- Number Of Countries
- Sellable Area
- International Exhibitors / International m2
- Local Exhibitors / Local m2
- Total Exhibitors / Total m2

**Visitor Stats:**
- International Visitors
- Local Visitors
- Total Visitors

**Online Registration:**
- Marketing Agent
- Other Sources
- Website Form
- Total Registration
- Emailing
- Digital Marketing Budget

**Description Information:** serbest text

**Related Lists:** Notes, Connected Records, **Expense (3)**, **Catalogue (1)**, Attachments, **Sales Contract (10+)**, **Visitors (10+)**, Related List Label 1 (10+), **Expo Check in Log**

**ELL karşılığı:** ELL `expos` tablosu (ELL_RULES R3, ELL_FloorPlan_Builder_Spec_v2). **Mevcut spec çok yetersiz** — Zoho'da bu kadar zengin bir alan seti var, Leena Phase 2'de bunların önemli kısmı UI'a girmeli.

---

### 3.11 Products

**Durum:** Aktif. Toplam **242 ürün**.

**Ne için:** Quote ve Sales Contract'ta line item olarak kullanılan ürün katalogu.

**Örnek kayıt: Standlı Yurtdışı Fuar Katılımı (SYK 430)**
- Product Name: Standlı Yurtdışı Fuar Katılımı (SYK 430)
- Product Code: -
- Zone: International
- Product Category: Space Sales
- Product Owner: Elan Exhibitions
- Product Active: ✓
- Usage Unit: M2
- Unit Price: -
- Commission Rate: -
- Tax / Taxable: -

**Product kategorileri (görülen):**
- Space Sales (PES, RF, SYK gibi ana satış kalemleri)
- Equipment (Fridge, TV, Showcase, Counter, Chair, Table — fuar standı ekipmanları)
- Visa Letters (Visa Letter V, Apostilled Visa Letter, Double Visa Letter)
- Sponsorship (Customized, Conference)
- Extra Services (Extra Electricity 20kw, Local Printing Service, Conference Area Rental)
- Wood/Wall (Wood Seamless Flat Wall F, Upgraded Stand F)

**Ülke/Fuar Suffix'leri ürün adlarında:**
- GH (Ghana?), F, C, V (?) — örn. "TV 55 inc GH" vs "TV 55 inc F"
- Bu, ürünlerin **per-fuar duplicate edildiğini** gösteriyor (aynı TV farklı fuar/ülkede farklı kayıt). Bu Zoho'da kaçınılmaz çünkü unit price farklı oluyor.

**Unit Price'lar:**
- PES 410: €410
- RF 350: €350
- TV 55 inc GH: €450
- TV 55 inc F: €500
- Apostilled Visa Letter: €85
- Visa Letter V: €150

**ELL karşılığı:** Ortak `products` tablosu (muhtemelen ELIZA tarafında, çünkü Quote ELIZA'da approve edilip Sales Contract'a yazılıyor). Mevcut blueprint'lerde Product modeli zayıf. Per-fuar fiyatlandırma ya `products` × `expos` junction tablosu ya da daha karmaşık bir pricing model gerektirir.

---

### 3.12 Sales Agents (Custom Module 2)

**Durum:** Aktif. Toplam **150 kayıt**.

**Ne için:** **Suer'in açık ifadesi:** "Zoho kullanıcı başına ücret aldığı için, ve sürekli satışçılar girip çıktığı için, bazı kişiler satış yapıyor ama CRM kullanmıyor olduğundan, bazı kişiler bizde çalışmıyor ya freelance ya acenta oldukları için, kim ne sattı, hangi quote hangi sales contract hangi leads kimin olduğunu görebilmemiz için, herkesi buraya kaydediyoruz."

**Bu kritik bir karar:** Sales Agent ≠ Zoho User. Sales Agent = "satış atfedilebilen herhangi bir entity" (kişi veya firma).

**2 ana tip:**

**1. Employee (iç çalışanlar):**
- Bengü Akgül, Yaprak Guzelcik, Suer, Sema Yılmaz
- Lokal ofis çalışanları:
  - **Kenya Office:** Caroline Muthoni, William Kangethe, Benson Jumba, Franklin Mwaniki
  - **Morocco Office:** Sarah Hamza, Meriem Houmaid, Hind Karim, Bouchra Garmoumi, Semih Seckin
  - **Nigeria Office West Africa:** Damilola Olori, Cynthia Okeke, Tina Ezenwa, Honour E. Ndah, Annette Ubah, Kemi Otuyemi, Amaka Okwumabua, Ronza Ah, Deborah Chidinma Anyanwu, Raji Zainab, Ashrae Ghana
  - Diğer: Joanna Jiang (China), Ghada Kawaf, Elahe Dorreh, Emircan Çakmak

**2. External (dış agent / partner / freelance):**
- Mars Fuarcılık Hizmetleri Tic. Ltd. Şti
- Anka Fuarcılık Tic. Ltd. Şti
- Sinerji International Exhibitions Ltd.
- Bola Associates
- ICF Fuarcılık
- Atlm Fuarcılık Tic. Ltd. Şti.
- M B EXPO CONSULTANT
- PK Marketing
- Gershonu (?)

**Alanlar (Raji Zainab örneği):**
- Sales Agent Owner: Elan Exhibitions West Africa
- Sales Agent Name: Raji Zainab
- Email: raji@elanexpo.net
- Modified By: Elan Exhibitions
- Currency: EUR
- Active: ✓
- Exchange Rate: 1
- Sales Agent Type: Employee
- Sales Group: Nigeria Office
- Sales Team: Nigeria Office
- Description: -

**Related Lists:** Notes, Connected Records, Attachments, Emails, Open Activities, Closed Activities, Cadences, **Kisiler** (kişiler), **Quote (Sales Agent) (3)**, **Sales Contracts (Sales Agent) (3)**, Zoho Survey, **Data Assigned to (10+)**, **Réponse de l'entreprise**, **Company Response**, Related List Label 1 (10+)

**Atamalar:** Lead/Quote/Sales Contract/Data atamalarının tümü Sales Agent ID üzerinden referansla yapılıyor.

**ELL karşılığı:** Bu **çok kritik mimari karar**. ELL'de:
- `users` tablosu = sistem kullanıcıları (Liffy/ELIZA/Leena'ya login olanlar)
- `sales_agents` tablosu = satış atfedilebilen herhangi bir kişi/firma (User olabilir veya olmayabilir)
- Junction: `sales_agent_id` → `user_id` (nullable, çoğunda null)

**Mevcut LIFFY tasarımı bunu doğru yansıtmıyor.** ADR-014, ADR-015 (reports_to hierarchy) Sales Agent yapısını da kapsayacak şekilde genişletilmeli.

---

### 3.13 Catalogues (Custom Module 4)

**Durum:** Aktif (otomatik oluşan kayıtlar).

**Ne için:** Sales Contract Signed olduğunda otomatik tetiklenen email + form akışının çıktısı.

**Akış:**
1. Sales Contract → Signed
2. Sistem otomatik email atar: exhibitor'a Catalogue formunu doldurması için
3. Email içeriği örneği (Mega Clima Nigeria 2026):
   ```
   Subject: Expo Catalogue for Mega Clima Nigeria 2026
   From: Yaprak Guzelcik <yaprak@elan-expo...>
   To: terry@tramos-group.com

   Dear Terry Beecham,
   We need the details of Tramos Group company for our exhibition catalogue.
   An equal size of area will be dedicated to every exhibitor of Mega Clima
   Nigeria 2026 regardless their size of participation.
   Company contact details, company profile, product groups and your logo
   will be published.
   ...
   Please click the link below to access our online form where you can input
   your company details and pictures that will be published in our catalogue.
   Click for your form: https://zfrmz.com/CHigJRCW7lkO4DvT5l2o
   Deadline for Catalogue Entry: 19.04.2026
   ```
4. Exhibitor formu doldurur → Catalogues modülünde kayıt oluşur

**Form içeriği (Nigeria Exhibitor Catalogue Form örneği):**
- Company Name (resmi imza atan firma)
- Expo Name (dropdown — fuara katılan)
- CATALOGUE INFORMATION:
  - Company Name in the Catalogue
  - Brands to be Exhibited at Your Stand
  - Product Groups
  - Company Profile

**Catalogues kayıt alanları:**
- Page ID, Company, Email, Page Owner (Sales Agent), Modified Time
- Catalogue Stage

**Görünen toplam:** 1300+ kayıt (tüm yıllar)

**Related Lists in Catalogues:** Tags Information (Tags Name, Tags Country, Mentioned Email, Tags Owner), Kişi/Email/Page Owner, vb.

**ELL karşılığı:** Bu **Leena'ya ait** olmalı (fuar exhibitor data toplama). Mevcut Leena spec'inde explicit değil — ELL_FloorPlan_Builder_Spec_v2 catalogue toplama akışını ele almıyor.

---

## Bölüm 4 — Pasif Modüller (Kısa Notlar)

| Modül | Durum | Sebep / Notlar |
|---|---|---|
| **SalesInbox** | Kullanılmıyor | - |
| **Potentials** (Deals) | Kullanılmıyor | Quote varken gerek yok |
| **Tasks** | Sorunlu | Suer zorluyor, kimse uygulamıyor (UX sorunu) |
| **Meetings** | Sorunlu | Aynı |
| **Calls** | Sorunlu | Aynı |
| **Purchase Orders** | Kullanılmıyor | - |
| **Invoices** | Kullanılmıyor | - |
| **Feeds** | Kullanılmıyor | - |
| **Campaigns** | Kullanılmıyor | LIFFY bu ihtiyacı karşılıyor |
| **Bodies/Expos** (Custom Module 1) | Kullanılmıyor | - |
| **Price Books** | Kullanılmıyor | - |
| **Cases** | Kullanılmıyor | - |
| **Documents** | Kullanılmıyor | - |
| **LeadChain** (WebTab1) | Kullanılmıyor | - |
| **Visits** | Kullanılmıyor | - |
| **Solutions** | Kullanılmıyor | - |
| **Social** | Kullanılmıyor | - |
| **Google Ads** | Kullanılmıyor | - |
| **Forecasts** | Kullanılmıyor | - |
| **Product Groups** (Custom Module 3) | Kullanılmıyor | - |
| **Visitors** (Custom Module 5) | Eskiden Zoho Form'la, **şimdi Leena yapıyor** |
| **Stand Leads** (Custom Module 6) | Plus Design firması için, ELL ile alakasız, kullanılmıyor |
| **New Leads** (Custom Module 14) | Kullanılmıyor |
| **My Jobs** (Approvals) | Kullanılmıyor | Quote onayı manuel yürüyor (Convert butonu) |
| **Check-in** (Custom Module 13) | Leena'nın işi, Zoho'da kullanılmıyor |
| **Check in Logs** (Custom Module 17) | Aynı |
| **Data** (Custom Module 18) | Kullanılmıyor |
| **Services** | Kullanılmıyor |

> **NOT — Tasks/Meetings/Calls problemi:**
> "Karışık olduğu için kimse kullanmıyor, ben zorluyorum ama uygulatamıyorum."
>
> Bu LIFFY Action Engine için **kritik bir UX uyarısı**. Aynı tuzağa düşmemek için "neden başarısız oldu" sorusunun derinleşmesi gerek. Zoho Tasks/Meetings/Calls satışçıların doğal iş akışına entegre değil — manuel veri girişi gerektiriyor. LIFFY Action Engine'in bunu otomatik (mesaj yazınca task oluştur, email açınca log düş) yapması gerekiyor.

---

## Bölüm 5 — Roller ve İş Bölümü

> Suer'in net ifadesi: "Kabaca doğru ama bunlar değişebilir."

### Mevcut hiyerarşi (May 2026):

```
Suer (CEO)
├── Elif (Sales Manager — tüm satışlardan sorumlu)
│   ├── Bengü (Ekip Lideri — geçen ay terfi etti, eskiden düz satışçıydı)
│   │   └── (Bengü'nün ekibindeki düz satışçılar)
│   ├── (Diğer düz satışçılar — Cynthia, Damilola, Caroline, vb.)
│   └── Lokal ofis ekipleri (Nigeria, Morocco, Kenya, China)
│
└── Yaprak (Project / Operations Lead)
    ├── Lokal ofis project ekipleri
    └── Veri girişi koordinasyonu
```

### Komisyon yapısı:
- **SR Comission** (Sales Representative) → kendi satışını yapan satışçı
- **SD Comission** (Sales Director) → satışçının müdürü
  - Müdür hem **kendi satışlarından** hem **ekibinin satışlarından** komisyon alır
  - Şu an genelde **Elif** SD pozisyonunda
  - Ama Bengü ekip lideri olduğu için onun ekibinde Bengü'de SD olabilir
- **Agent Comission** → dış agent (Anka, Sinerji, vb.) anlaşmalı satıştan komisyon alır

### Önemli prensip:
> "Bunlar değişken olabilmeli." — Roller dondurulamaz, sistem hiyerarşi değişimine esnek olmalı.

**ELL karşılığı:** ADR-015 (hierarchical data visibility) reports_to recursive CTE doğru yaklaşım. Ama komisyon hesaplama mantığı ELIZA tarafında olmalı — kim kime ne kadar komisyon verecek bunu sales contract'a göre dinamik hesaplama gerekir.

---

## Bölüm 6 — Otomasyonlar (Workflow Rules + Triggers)

> Suer'in ifadesi: "Workflow rules var işleyişi kolaylaştıran ve profile ayrıca roles diye kullanıcıları sınıflandırma var."

### Tespit edilen otomatik akışlar:

**1. Quote Signed → Email tetikleyici:**
- Tetik: Quote Stage = "Signed"
- Eylem: Proje ekibi (Yaprak) + CEO'ya email atılır
- Sonuç: Yaprak Convert butonuna basar

**2. Sales Contract → Catalogue email:**
- Tetik: Sales Contract Status = Valid + Catalogue form mail = ✓
- Eylem: Exhibitor'a Catalogue formu gönderilir (sender: Yaprak)
- Form linki: zfrmz.com URL (per-fuar farklı)
- Sonuç: Catalogues modülünde kayıt oluşur

**3. Sales Contract → 8 farklı email akışı:**
- Welcome Mail, Stand Design Mail, Boost Mail, Extra Service Mail, BuildUp Rules Email, Payment Reminder, Internal Notification, Badge
- "Send Them All Now" master switch ile hepsi aynı anda tetiklenebilir

**4. Web formundan Lead → Zoho:**
- Tetik: Şirket websitesindeki "Contact Us" form gönderimi
- Eylem: Otomatik Lead oluşur Zoho'da

**5. Email_Template_ID alanı (Expos modülünde):**
- Her fuar için farklı email template ID tutuluyor
- Tahmin: Bir email akışı tetiklendiğinde, fuara göre hangi template kullanılacağı buradan belirleniyor

**ELL karşılığı:** ELIZA "Action Engine" + LIFFY workflow trigger sistemi. Mevcut tasarımda Sales Contract'ın 8-mail akışı henüz tanımlı değil — bu Phase 2'de ELIZA tarafında implement edilmeli.

---

## Bölüm 7 — Veri Hacmi (Mayıs 2026)

| Modül | Kayıt Sayısı | Notlar |
|---|---|---|
| Leads | 586,910 | Çoğu eski/cold; ~75K LIFFY'de aktif |
| Contacts | 17,675 | Convert sonrası |
| Companies (Accounts) | 18,197 | Convert sonrası |
| Quotes | yüksek (binlerce) | Aktif kullanım |
| Sales Contracts | yüksek (binlerce) | Aktif kullanım |
| Expenses | 589+ | (HQ filter'lı) |
| Revenues | 731 | (görünen sayfa) |
| Expos (Vendors) | 202 | Aktif fuarlar + arşiv |
| Products | 242 | Per-fuar duplicate'lar dahil |
| Sales Agents | 150 | Employee + External |
| Catalogues | 1300+ | Otomatik oluşan kayıtlar |

**Para birimleri:** EUR, NGN, MAD, TL (her biri Exchange Rate ile)

**Ofisler:** HQ (Istanbul), Morocco Office (Casablanca), Nigeria Office (West Africa), Kenya Office, China Office, Algeria, Ghana

---

## Bölüm 8 — Lokal Ofis Operasyonları

### Ofis listesi:
1. **HQ** — Istanbul (Yaprak, Suer, Elif, Bengü, vb.)
2. **Morocco Office** — Casablanca (Sarah Hamza, Meriem Houmaid, vb.)
3. **Nigeria Office West Africa** — (Damilola, Cynthia, Raji, vb.)
4. **Kenya Office** — (Caroline, William, Benson, Franklin)
5. **China Office** — (Joanna Jiang)
6. **Algeria** — (görünür ama detay yok)
7. **Ghana** — (görünür ama detay yok)

### Lokal ofis akışları:
- **Veri girişi:** Lokal satışçılar Zoho'ya direkt giriyor. Zaman zaman **freelance data entry** kişileri tutuluyor — onlar için **Zoho Form (public URL)** ile data entry yapılıyor
- **Tahsilat girişi:** Lokal ofisler Revenues modülüne kendi para birimlerinde girişi yapıyor (NGN, MAD, TL, EUR), Exchange Rate ile EUR'a normalize
- **Harcama girişi:** Lokal ofisler kendi Expense'lerini giriyor (maaş, kira, telefon, vb.)
- **Komisyon:** HQ Sales Commission expense type olarak Expenses'e giriliyor (lokal ofis veya HQ tarafından)

### Veri girişi takibi:
- **Yaprak**, "Nigeria Daily Data Entry", "Kenya Weekly Data Entry", "Morocco Weekly Data Entry", "China Office Weekly Data Entry" raporları üzerinden lokal ofislerin ne kadar veri girdiğini takip ediyor
- Bu önemli bir **performans metriği** — lokal ofisler aktif lead/contact/visitor toplamak zorunda

**ELL karşılığı:** Multi-office multi-currency desteği LIFFY ve ELIZA'da first-class. Veri girişi performans metriği şu an blueprint'lerde yok — INTELLIGENCE_ROADMAP'e eklenmesi lazım.

---

## Bölüm 9 — Önemli Mimari Çıkarımlar (ELL için)

### 9.1 Quote → Sales Contract Geçiş Mimarisi
- **Mevcut:** Manuel "Convert" butonu (Yaprak basar)
- **Doğal kontrol:** Onay değil ama eksik bilgi tamamlama + sanity check
- **ELIZA tarafında:** Quote approval flow (ADR-003) bu doğal kontrolü resmileştirebilir, ama **fazla bürokratik olmamalı** — sadece "convert et + eksik alanları doldur" UX akışı yeterli
- **AF Number sequencing:** Şu an Zoho otomatik. ELIZA'da PostgreSQL SEQUENCE ile yapılacak

### 9.2 Sales Contract Karmaşıklığı
- **Phase 1.5 yetersiz:** Mevcut Quote modülü (LIFFY_PHASE_1_MVP_PLAN) sadece quote kapsamında, Sales Contract'ın 3-kademe komisyon yapısı + 8-mail Announcement akışı + Stand detayları + Cancelled Fields ele alınmıyor
- **Phase 2 plan revizyonu:** Sales Contract'a geçişin gerçek kapsamı **8-12 hafta** olabilir, sadece 4-6 değil

### 9.3 Sales Agent vs User Ayrımı
- **Kritik mimari karar:** Sales Agents tablosu sistem kullanıcılarından ayrı
- **150 agent** vs muhtemelen **20-30 sistem kullanıcısı** (Liffy/ELIZA/Leena'ya login olan)
- Junction tablosu gerekli: `sales_agent_id` ↔ `user_id` (nullable)
- ADR-015 reports_to bu yapıyı kapsayacak şekilde genişletilmeli

### 9.4 Multi-Currency Her Yerde
- 4 para birimi (EUR, NGN, MAD, TL) her ticari modülde
- Exchange Rate kayıt zamanında dondurulmalı (audit trail için)
- ELIZA'da `currency_code` + `exchange_rate_at_record_time` first-class

### 9.5 Revenues vs Sales Contract Çift Veri Riski
- Şu an Sales Contract "Received Payments" subform + Revenues "Payment Date" subform — çift kaynak
- **ELL'de tek doğruluk kaynağı: Revenues** olmalı
- Sales Contract sadece toplam balance göstermeli, payment subform kaldırılmalı

### 9.6 Expenses Aslında Tam Bir Muhasebe Modülü
- Sadece "expense entry" değil — multi-office, multi-currency, payment subform, expense categorization, expo attribution, sales commission tracking
- ELIZA Finance Module mevcut spec'inden 2-3 kat daha karmaşık

### 9.7 Reports Operasyonel + Finansal + Veri-Girişi Takibi
- Tek tip raporlama yetmez — 3 farklı amaç var (visitor reg, data entry productivity, payment tracking)
- ELIZA War Room dashboard + LIFFY Reports + Leena Visitor Funnel ayrı katmanlar olarak tasarlanmalı

### 9.8 Email Otomasyon Zinciri
- Sales Contract'ın 8-email tetikleyicisi (Welcome, Catalogue, Stand Design, Boost, Extra Service, BuildUp Rules, Payment Reminder, Badge) ELL'de eksik
- Her email per-fuar template kullanıyor (Email_Template_ID Expos modülünde)
- Phase 2 ELIZA tarafında bu akış implement edilmeli

### 9.9 Tasks/Meetings/Calls Adoption Failure Sinyali
- Suer aktif olarak zorluyor ama kimse kullanmıyor
- LIFFY Action Engine bunu otomatikleştirmeli (manuel veri girişi minimum)
- ChatGPT/Gemini reviewer'lar bunu "UX kritik risk" olarak işaretlediler — doğru sinyal

### 9.10 Visitors Modülü Migration Precedent
- Visitors zaten Zoho'dan Leena'ya geçti (önceden Zoho Form, şimdi Leena UI)
- Bu **migration template'i** olarak diğer modüller için yararlı:
  - Önce Leena UI hazırla
  - Veri girişi yeni UI'da başlasın
  - Eski Zoho Form deprecated olsun
  - Tarihsel veri Leena'ya import edilsin

---

## Bölüm 10 — Açık Sorular ve Eksik Bilgi

Bu doküman tamamlanırken hâlâ netlik gerektiren noktalar:

1. **Sales Director komisyonu hesaplama mantığı:** Müdür ekibinin satışlarından ne yüzde alıyor? Sabit mi, anlaşmaya göre mi?
2. **Workflow Rules listesi:** Suer "var" dedi ama tam liste yok. Tüm tetikleyiciler ve eylemleri inventory edilmeli.
3. **Profiles ve Roles:** Zoho'daki kullanıcı yetki matrisi (kim ne görür, kim ne edit edebilir) doküman edilmedi.
4. **Per-ülke özelleşme:** Nigeria Office'in spesifik akış farkları (Nigeria Daily Data Entry varken Morocco Weekly olması)
5. **Lead source breakdown:** Web formu vs manuel vs freelance data entry oranları
6. **Hangi raporlar günlük/haftalık otomatik gönderiliyor:** Raporların manuel mu yoksa schedule edilmiş mi olduğu
7. **AF Number formatı ve sequence:** Tam format (A809455 — A prefix'i nedir, sequence nereden başlıyor)
8. **Cancelled Sales Contract akışı:** İptal durumunda 1st/2nd/3rd payment fields nasıl çalışıyor
9. **Inter-office currency transfer:** Lokal ofis NGN'de tahsilat yapınca, HQ'ya nasıl yansıtılıyor
10. **Catalogue formundan gelen verinin Sales Contract'a geri-entegrasyonu:** Form doldurulduktan sonra Sales Contract'a otomatik bağlanıyor mu

---

## Bölüm 11 — Bu Dosyanın Kullanımı

**Bu dosya nereye kaydedilmeli:**
- GitHub: `Nsueray/ell-docs/zoho/ZOHO_USAGE_REFERENCE.md`
- Liffy Project Knowledge: yüklenmiş halde
- Lokal: `~/Desktop/ell-docs-snapshot/zoho/`

**Hangi chat'lerde referans olarak kullanılır:**
- Liffy chat (LIFFY tasarım kararları)
- ELL chat (cross-system mimari)
- Leena chat (Visitors, Catalogues, Check-in tarafı)
- Dış AI review (ChatGPT, Gemini) — RFC review öncesi context dosyası olarak

**Güncelleme prensibi:**
- Zoho akışları değiştikçe versiyon güncellenir (v1.1, v1.2)
- Her değişiklik Bölüm 10'daki açık soruların cevaplanmasıyla yapılmalı
- Mimari çıkarımlar (Bölüm 9) ELL_RULES veya ADR'lere yansıdıkça referans verilmeli

**Versiyon geçmişi:**
- v1.0 (6 Mayıs 2026): İlk derleme — Suer ile yapılan walkthrough oturumu

---

*Bu doküman ELL ekosistemi tasarımı için referans niteliğindedir. Spesifik implementasyon kararları ELL_RULES, ADR'ler ve LIFFY/ELIZA/Leena Phase planlarında yer alır.*
