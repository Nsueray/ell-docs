# ELL Analiz — Track 3 + Track 4 (READ-ONLY kanıt)

> **Tarih:** 2026-06-08 · **Yöntem:** salt-okuma (SELECT / information_schema / pg_catalog / kod + canlı `pg_dump --schema-only`). Production'a hiçbir yazma. Her bulgu `dosya:satır` veya sorgu çıktısıyla bağlı.
> **Şema kaynağı:** `~/ELL_schema_dumps/t1_0608/{eliza,liffy,leena}_live.sql` (taze canlı dökümler).

---

# TRACK 3 — Ticari çekirdek ground truth (ELIZA)

## 3.1 Kolon dökümü + Zoho-sourced vs ELL-generated

### contracts (`eliza_live.sql:206`; INSERT `syncSalesOrders.js:248-283`)
| kolon | tip | null? | kaynak |
|---|---|---|---|
| id | integer | NOT NULL | ELL (serial PK) |
| af_number | text | NOT NULL | **Zoho** ← `record.AF_Number` (`syncSalesOrders.js:66`) |
| expo_id | integer | NULL | ELL-derived (Expo_Name→local expos.id, `:74`) |
| company_name | text | NULL | Zoho ← `Account_Name.name` (`:67`) |
| country | text | NULL | Zoho ← `Country` (`:68`) |
| sales_agent | text | NULL | Zoho ← `Sales_Agent.name` (`:69`) — **free-text, FK YOK** |
| m2 | numeric | NULL | Zoho ← `M2` (`:70`) |
| revenue | numeric | NULL | Zoho ← `Grand_Total` (`:71`) |
| contract_date | date | NULL | Zoho ← `Contract_Date` (`:72`) |
| sales_type | text | NULL | Zoho ← `Sales_Type` (`:73`) |
| pavilion_flag | boolean | NULL | ELL (DDL default false) |
| currency | text | NULL | Zoho ← `Currency` (`:76`) |
| exchange_rate | numeric | NULL | Zoho ← `Exchange_Rate` (`:77`) |
| **revenue_eur** | numeric | NULL | **ELL-computed** ← revenue/exchange_rate (`:49-56,78`) **— STORED** |
| status | text | NULL | Zoho ← `Status` (`:79`) |
| **balance_eur** | numeric(12,2) | NULL | **ELL-computed** ← toEur(Balance1) (`:81`, migr 013:7) **— STORED** |
| **paid_eur** | numeric(12,2) | NULL | **ELL-computed** ← toEur(Total_Payment) (`:82`, migr 013:8) **— STORED** |
| remaining_payment_eur | numeric(12,2) | NULL | ELL-computed (`:83`, migr 013:9) STORED |
| due_date | date | NULL | Zoho ← `Due_Date` (`:84`) |
| payment_done | boolean | NULL | Zoho ← `Payment_Done` (`:85`) |
| payment_method | text | NULL | Zoho ← `Payment_Method` (`:86`) |
| validity | text | NULL | Zoho ← `Validity` (`:87`) |
| first_payment_eur / second_payment_eur | numeric(12,2) | NULL | ELL kolon, **DOLDURULMUYOR** (migr 013:14-15) |
| created_at / updated_at | timestamp | NULL | ELL (DDL default now()) |

### contract_payments (`eliza_live.sql:169`; INSERT `syncSalesOrders.js:160`)
| kolon | tip | null? | kaynak |
|---|---|---|---|
| id | integer | NOT NULL | ELL (serial PK) |
| contract_id | integer | NOT NULL | ELL (local FK→contracts) |
| af_number | text | NOT NULL | Zoho-derived (taşınıyor) |
| payment_date | date | NULL | Zoho subform `payment.Date` (`:112`) |
| amount_eur | numeric(12,2) | NULL | **ELL-computed** (subform, §3.4) |
| note | text | NULL | Zoho subform + ELL annotation |
| amount_local | numeric(12,2) | NULL | **ELL-parsed** orijinal-para (`:131`, migr 016:6) |
| currency | varchar(10) | NULL (def EUR) | Zoho ← parent contract Currency (migr 016:7) |
| created_at | timestamp | NULL | ELL |

### contract_payment_schedule (`eliza_live.sql:130`) — **%100 ELL sentetik**
30% deposit + 70% pre-event uydurma plan (`syncSalesOrders.js:170-208`). `is_synthetic=true`, due_date = contract_date+30 / expo_start−30, planned_amount = revenue_eur×0.30/×0.70. Gerçek Zoho ödeme planı **kullanılmıyor**.

### expenses (`eliza_live.sql:400`) — **YAZAR YOK (bulamadım)**
Kolonlar: id, expo_id(FK→expos), category(text), amount(numeric), currency(text), source(text), created_at. **Hiçbir sync kodu doldurmuyor** (zoho-sync'te `INSERT INTO expenses` yok). category serbest metin, referans tablosu yok.

### sales_agents (`eliza_live.sql:834`) — **YAZAR YOK**
Kolonlar: id, name, office, phone_number, role, preferred_language(def 'en'). **Komisyon/pct/rate kolonu YOK.** İçeri alan sync kodu yok (`syncSalesAgents.js` yok). `preferred_language` mesaj üreticisinde kullanılıyor.

### expo_targets (`eliza_live.sql:519`; migr 019) — **%100 ELL-generated**
target_m2/target_revenue = önceki edisyon actual × (1+pct) (`targets/index.js:78-82`), source auto/manual, auto_percentage def 15.0. ELIZA'nın **tek gerçek owned-yazılabilir** finans varlığı.

## 3.2 af_number — atama: **Zoho-copy (verbatim), yerel sequence YOK**
`af_number: record.AF_Number || null` (`syncSalesOrders.js:66`), ON CONFLICT anahtarı (`:250`). `nextval/generateAf/Q{ISO}/A{ISO}` **hiçbir yerde yok** (grep boş). DDL'de af_number = plain `text NOT NULL`, sequence/default yok.

**Mevcut değer pattern'leri (canlı, rakamlar `#` maskeli):**
| pattern | adet | | prefix | adet |
|---|---|---|---|---|
| `AF######` | 1372 | | AF | 2408 |
| `A######` | 884 | | A | 885 |
| `AF#####` | 636 | | (boş/numeric) | 257 |
| `######` (sadece rakam) | 205 | | E | 51 |
| `E#####` | 47 | | AFaz… | 18 |
| `AF############`…`AF#################` | ~155 | | AZ/Az/T | ~11 |

→ **Karışık legacy format** (AF/A/E/numeric, değişken uzunluk). Faz 1f/2'nin `Q{ISO}-{seq}` / `A{ISO}-{seq}` şeması **bugün yok**; ELL bu sequence'i sahiplenirse hem legacy karışıklığı hem 1 yıl paralelde Zoho'nun ürettiği numaralarla **çakışma riski** yönetilmeli.

## 3.3 Denormalize para — **EVET, stored**
contracts'ta `revenue_eur`, `paid_eur`, `balance_eur`, `remaining_payment_eur` **stored** (migr 013, sync-time yazılıyor). `finance.js` bunları **stored kolondan** okuyor (`outstanding_balances` view üzerinden `SUM(paid_eur)/SUM(balance_eur)`, `finance.js:31-34`), computed SUM değil — tek istisna "Paid This Month" `SUM(amount_eur) FROM contract_payments` (`finance.js:79`).
`queryEngine.js:1176` TODO verbatim: `// TODO: Add balance field from Zoho Balance1 formula field` — **bayat** (balance_eur artık sync ediliyor `:81`). `queryEngine.js:364`: "Balance1 is not synced … Only Grand_Total available" — yine bayat.
→ Roadmap'in "computed, denormalize etme" ilkesine **aykırı mevcut durum** (stored EUR alanları).

## 3.4 FX / currency freeze — **rate tablosu YOK; per-CONTRACT frozen**
Exchange-rate **tablosu yok** (ELIZA + LIFFY). Tek kur saklama: `contracts.exchange_rate` (Zoho'dan, sync-time donmuş). `contract_payments`'ta **rate kolonu YOK** → ödeme-bazlı frozen rate yok. `amount_eur` sync-time hesaplanıyor: dual-format `"X (€Y)"` → parantez EUR (`:123-135`), yoksa `amount_local / exchange_rate` (`:149`) — kullanılan kur **contract-seviye**. Sync tekrar çalışınca yeniden türetiliyor (DELETE+re-INSERT). LIFFY'de hiç FX/para kolonu yok.
→ Ledger'ın istediği **işlem-bazlı frozen rate** bugün yok; sadece sözleşme-bazlı var (kısmen).

## 3.5 Agent + komisyon
- Bağ **free-text**: `contracts.sales_agent text` (FK YOK — FK listesi yalnız expo_id). Join isim-string ile (`users.sales_agent_name → contracts.sales_agent`).
- `sales_agents`'ta **komisyon oranı kolonu YOK**.
- **Komisyon hesaplama kodu YOK** (bulamadım; tek "commission" eşleşmesi WhatsApp EUR-format dalı).

## 3.6 Greenfield teyidi (3 repo)
| Yetenek | Durum |
|---|---|
| **Quote** | **YOK (greenfield)** — 3 repoda quote tablosu/endpoint yok |
| **Product/SKU/price/catalog** | **YOK (greenfield)** — `CREATE TABLE …(product\|sku\|price\|catalog)` 3 dökümde 0 |
| **Payment-create endpoint** | **YOK (greenfield)** — ödeme POST/PUT yok; ödemeler yalnız sync-write |
| **Commission** | **YOK (greenfield)** — kolon yok, kod yok |
| **Multi-account ledger** | **YOK (greenfield)** — accounts/transactions/ledger/journal/bank/cash 3 dökümde 0 |
| **FX-freeze** | **kısmen var** — `contracts.exchange_rate` per-contract frozen; ama rate tablosu yok, per-payment frozen yok |

---

# TRACK 4 — Kimlik + reference reconciliation

## 4.1 Kimlik matrisi (canlı sorgu)

| Sistem | Tablo | Kullanıcı modeli | Sayı |
|---|---|---|---|
| **LEENA** | `organizers` | tek hesap = login (password_hash); **users/role YOK** | **1** |
| **LIFFY** | `organizers`(1) + `users` | uuid PK, role + reports_to + permissions JSONB | users **3** |
| **ELIZA** | `users` + `user_permissions` | int PK, role + data_scope + visible_years + flags | users **3** |

### Aynı insanın 3 sistemdeki kimliği (Faz 4 tek-kimlik map'i)
| İnsan | LEENA | LIFFY | ELIZA |
|---|---|---|---|
| **Suer** (suer@elan-expo.com) | organizers `id=1` "Nihat Suer AY" | users `cfb66f28-…d40b`, **owner** | users `id=1`, **ceo**, scope=all |
| **Elif** (elif@elan-expo.com) | — (LEENA'da user yok) | users `1798e4e3-…c95b`, **manager**, reports_to=Suer | users `id=2`, **manager**, scope=all |
| **Bengü** (bengu@elan-expo.com) | — | users `c845b557-…4d43`, **sales_rep**, reports_to=Elif | **— YOK** |
| **Yaprak** (yaprak@elan-expo.com) | — | **— YOK** | users `id=3`, **manager**, scope=all |

**Bulgular:**
- **ID şizmi:** aynı insan 3 farklı id-uzayında — LEENA organizer **int**, LIFFY users **uuid**, ELIZA users **int**. Ortak/paylaşılan kimlik anahtarı YOK.
- **Email tek tutarlı eşleştirme anahtarı** (hepsi `@elan-expo.com`, aynı local-part). Faz 4 tek-kimlik map'i pratikte **email join** üzerinden kurulabilir.
- **İnsan kümeleri asimetrik:** Suer 3'te de var; Elif LIFFY+ELIZA; **Bengü yalnız LIFFY**; **Yaprak yalnız ELIZA**. LEENA hiç user/role modeli taşımıyor (tek organizer = Suer).
- **Scope gerçekte kısıtlamıyor:** ELIZA'da 3 user da `data_scope=all` (manager'lar dahil). LIFFY'de `permissions` JSONB **3'ünde de boş `{}`** → ölü kolon (önceki tespitle tutarlı).

## 4.2 Reference data — **PAYLAŞILMIYOR, 3 bağımsız silo**

| Sistem | Reference gerçeği | Kanıt |
|---|---|---|
| **ELIZA** | `core_countries`(249)/`core_sectors`/`core_currencies`(15)/`core_languages` **sahibi**; yalnız **kendi içinde** tüketiyor | `routes/reference.js:6-58`, `server.js:54`, `apps/dashboard/.../reference.js`, migr 021-024 |
| **LIFFY** | **per-system duplicate** — core_* okumuyor | `core_*` yalnız **yorumda** (`migr 046:24,28` "soft FK, ELIZA writes Liffy reads" — FK/JOIN/SELECT YOK). TODO `actionEngine.js:137` "when ELIZA shared DB connected". Kendi: `companies.country_code`+`sector_id`, `affiliations.country_code`+`industry`, `prospects.country`+`sector` (hepsi free-text); hardcoded ülke listeleri `sourceDiscovery.js:42-65`, `zohoService.js:19-24` |
| **LEENA** | **per-system duplicate** — core_* okumuyor (grep 0), outbound HTTP client yok | Kendi: `visitors.country`+`sector`, `expo_exhibitors.country`+`sector` (free-text); hardcoded ~190-ülke HTML dropdown (`fix_countries.sh` → `public/qrscanner.html`) |

**ELIZA'da `/api/reference/*` endpoint'i VAR** (CORS `*`, GET'lerde auth yok, `server.js:27-33`) — teknik olarak erişilebilir, ama **hiçbir dış sistem çağırmıyor** (bulamadım). ELIZA CLAUDE.md §24: "Leena/Liffy API entegrasyonu henüz yapılmadı".

**Net:** Reference data bugün **paylaşılmıyor; 3 bağımsız silo.** "Shared core_*" tasarımı dokümante niyet (ELL_RULES R1/R9) ama production'da yalnız ELIZA'nın kendi tabloları + tüketilmeyen bir endpoint olarak var. Convert gate (LIFFY→ELIZA) sector/country eşlemesi gerektiğinde, üç sistemin farklı free-text temsilleri **eşleme/duplicate sorunu** yaratır.

---

## ÖZET (Faz tasarımına girdi)
- **Ticari çekirdek tamamen greenfield:** quote, product catalog, payment-create, commission, multi-account ledger — 3 sistemde de **YOK**. FX yalnız contract-seviye frozen (kısmen).
- **ELIZA finans = Zoho aynası + denormalize stored EUR:** revenue_eur/paid_eur/balance_eur stored (013), af_number Zoho-copy (yerel sequence yok), payment schedule sentetik, expenses/sales_agents boş (yazar yok), agent free-text, komisyon yok.
- **Kimlik:** 3 ayrı id-uzayı (int/uuid/int), email tek ortak anahtar; insan kümeleri asimetrik (Bengü yalnız LIFFY, Yaprak yalnız ELIZA, LEENA user'sız). Faz 4 tek-kimlik = email-join + yeni surrogate id.
- **Reference:** 3 bağımsız silo, hiç paylaşım yok; ELIZA core_* yalnız kendi içinde tüketiliyor.
