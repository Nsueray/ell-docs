> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# ELIZA — DERİN ANALİZ (yazılabilir ticari çekirdek ölçümü)

> **Amaç:** ELIZA'yı ticari çekirdeğin İÇ HALKASI (yazılabilir contract + payment +
> commission + ledger + finans) yapmak için alan-bazında NE kadar iş gerektiğini ölçmek.
> Ayrıca KORU denilen güçlü parçaları (AI/raporlama) dokunulmadan korunacak şekilde net sınırlamak.
>
> **Kod:** `~/Projects/eliza` (monorepo: apps/{api,dashboard,whatsapp-bot}, packages/{ai,alerts,attention,briefing,db,messages,push,targets,zoho-sync})
> **Referans:** `~/Downloads/ELAN_EXPO_REQUIREMENTS_v1_0.md` — yalnız 2.3 (Sales Contract), 2.6 (Financial Ops), 3.3 (Multi-currency)
> **Yöntem:** 3 paralel kod-inceleme ajanı, her iddia `dosya:satır`. Dokümana güvenilmedi. Hiçbir dosya değiştirilmedi. Bulunamayan → "bulamadım".

---

## TL;DR — Alan durumları tek bakışta

| Alan | Durum | Tek cümle |
|---|---|---|
| **A. Contract** | **İSKELET** | Salt-okunur Zoho aynası — tek yazan `syncSalesOrders.js`; write route yok, af_number üreteci yok, status sadece okuma filtresi, operasyonel alanlar (scan/catalogue/stand) şemada bile yok. |
| **B. Payment** | **İSKELET** | %100 Zoho subform; schedule tamamen sentetik (30/70); `paid_eur` denormalize saklanıyor; ELIZA'da yeni ödeme girilemiyor. |
| **C. Commission** | **YOK** | Three-tier komisyon kodda/şemada sıfır; `sales_agents` var ama pct kolonu yok, sadece isim listesi; hesaplama/adjustment yok. |
| **D. Multi-account ledger** | **İSKELET** (neredeyse greenfield) | accounts/transactions/transfers/budget tabloları yok; `expenses` var ama ölü kod; `finance.js` baştan sona salt-okunur (9 GET). |
| **E. AI/Rapor/Risk/Targets** | **TAM** (KORU adası) | queryEngine+router+risk sağlam, targets YAZILABİLİR (ELIZA'nın tek owned yazılabilir varlığı), finance/revenue salt-okunur gerçek — iki bounding caveat ile. |
| **F. Kullanıcı/Yetki** | **İSKELET** | Şema + JWT/bcrypt login gerçek ve Zoho'dan bağımsız AMA **API'de hiç auth middleware yok** — 4 auth endpoint'i dışında her şey kimliksiz çağrılabilir. |
| **G. Zoho bağımlılığı** | **TAM** (tek yönlü) | Kesin Zoho→ELIZA downstream mirror; asla geri yazmıyor; Zoho kapanınca tüm contract/payment/expo verisi donuyor. |

> **Yapısal uyarı (her alanı etkiler):** Migration'lar 001, 002, 003, 010 repoda **YOK**
> (`packages/db/migrations/` 004'ten başlıyor). `contracts.status/currency/exchange_rate/
> revenue_eur/expo_name` kolonları ve `edition_contracts`/`fiscal_contracts`/`expo_metrics`
> view'ları sadece bu eksik dosyalarda (veya elle DB'de) tanımlı — her yerde kullanılıyor,
> repoda tanımı yok. **DB salt migration'lardan yeniden kurulamaz.**

---

## A. CONTRACT — İSKELET (salt-okunur Zoho kopyası)

**Tek yazan doğrulandı.** `contracts`'a tek INSERT/UPDATE = `packages/zoho-sync/syncSalesOrders.js:247-284` (`INSERT ... ON CONFLICT (af_number) DO UPDATE`). apps/+packages genelinde `(INSERT|UPDATE|DELETE).*contract` taraması başka yazan döndürmedi (auth.js:39,52 yalnız `REFERENCES contracts(id)` FK). **Önceki analiz doğrulandı.**

**Eksikler:**
- **Write route yok.** Tüm POST/PUT/PATCH/DELETE route envanteri (`apps/api/src/routes/*`): auth, reference, messages, targets, expos/calculate-targets, system/sync-now, users. Hiçbiri contracts'a dokunmuyor. LIFFY'nin çağıracağı **convert/create-contract endpoint'i yok.**
- **af_number üreteci yok** — Zoho'dan birebir geliyor (`syncSalesOrders.js:66`); generate/nextval yok.
- **status salt-okunur** — yalnız sync upsert yazıyor (`syncSalesOrders.js:248`, Zoho `record.Status`'tan `:79`). Okuma filtresi olarak: `finance.js:55,273,407`, `targets.js:54`, `queryEngine.js:1220,1236,1251`, view'lar. Active/On Hold/Transferred/Cancelled lifecycle'ı **app yazmıyor — geçişler Zoho'da oluyor.**
- **Operasyonel alanlar şemada YOK** — `scan_link`, `catalogue_page`, stand details, `sales_group` `schema.sql:18-30`'da ve hiçbir migration'da yok (013 yalnız `balance_eur/paid_eur/...` ekledi). Zoho'dan da sync edilmiyor.
- **Sync üzerine-yazma tuzağı:** ON CONFLICT upsert (`syncSalesOrders.js:250-260`) bir sonraki sync'te ELIZA-tarafı düzenlemeleri **ezecek** — Zoho-owned vs ELIZA-owned alan ayrımı yok.

**Yazılabilir yapmak için:** operasyonel kolonlar + create/update endpoint + af_number sequence + status state-machine + convert endpoint + **Zoho/ELIZA alan-sahipliği çatışma çözümü** (en zor kısım: hangi alanı sync ezecek, hangisini ELIZA koruyacak).

---

## B. PAYMENT — İSKELET (Zoho türevi; schedule uydurma)

- **contract_payments kaynağı = yalnız Zoho.** `syncSalesOrders.js`'te delete-then-reinsert: `syncReceivedPayments()` DELETE `:105`, INSERT `:160` (Zoho `Received_Payment` subform'u `:89`); ikinci geçiş `syncPaymentsPass()` `:330-383`. Başka yazan yok.
- **Sentetik schedule = %100 uydurma.** `syncPaymentSchedule()` `:173-208` schedule'ı siler `:174`, tam 2 satır ekler, ikisi de `is_synthetic=true`: %30 deposit (`revenue_eur*0.30`, due=contract_date+30g) + %70 final (`revenue_eur*0.70`, due=expo_start−30g). Yorum `:170-171` Zoho'nun gerçek `Date_Amount_Type` alanlarının terk edildiğini doğruluyor. → **%0 gerçek / %100 uydurma.**
- **paid_eur denormalize saklanıyor (req 2.6'ya aykırı).** `paid_eur` contracts'ta saklanan kolon, Zoho `Total_Payment`'tan yazılıyor (`syncSalesOrders.js:82,257`), `contract_payments`'tan hesaplanmıyor. View `COALESCE(c.balance_eur, c.revenue_eur - COALESCE(c.paid_eur,0))` (`013_payment_fields.sql:68`). Req 2.6'nın "stored, not computed" anti-pattern'i.
- **Native ödeme girişi yok** — `contract_payments`'a POST route yok; `/api/finance/*` hepsi salt-okuma.

**Yazılabilir yapmak için:** payment-create endpoint + computed paid_eur/balance (contract_payments toplamı) + gerçek installment schedule modeli.

---

## C. COMMISSION — YOK (greenfield)

- **Komisyon domain'i sıfır.** `commission|agent_pct|sr_pct|sd_pct|commission_adjustment|payable` taraması fonksiyonel sıfır isabet (sadece false-positive: `PRIMARY KEY`, `permission`, CSS). Tek "commission" = `apps/whatsapp-bot/src/handler.js:973` EUR formatlama keyword listesi.
- **sales_agents var ama pct yok.** `schema.sql:52-59`: `id, name, office, phone_number, role, preferred_language`. Default komisyon pct kolonu YOK. Tek okuyan `packages/messages/index.js:107-115` — isim/iletişim listesi, **hiçbir hesaplamada kullanılmıyor.**
- **Migration 013 yalnız ödeme kolonları ekledi** (`013:7-15`), sıfır komisyon kolonu. Doğrulandı.
- **Zoho komisyonu bilerek atlıyor:** Zoho `Sales_Orders`'ta `Agent/SR/SD` pct + `Agent_Comission/SD_Comision/SR_Prim_S` + `*_Done/*_Paid` alanları VAR ama `syncSalesOrders.js` hiçbirini map etmiyor (INSERT `:248` yalnız contract/payment kolonları).

**Sıfırdan gerekenler:** agent default-pct + tier kolonları (agent/sr/sd) + Agent-vs-SR exclusivity + per-contract override pct + hesaplama motoru (amount×pct) + paid-status (due/paid/outstanding) + cancellation adjustment/netting + (zaten Zoho'da duran kullanılmayan komisyon alanlarının sync'i).

---

## D. MULTI-ACCOUNT LEDGER — İSKELET (neredeyse tam greenfield)

**Tam CREATE TABLE envanteri (schema.sql + tüm migration'lar):** expos, contracts, exhibitors, expenses, sales_agents, alerts, whatsapp_messages, message_drafts (schema.sql:5-95); sync_log (004); users, user_permissions (005); message_logs (006); contract_payments, contract_payment_schedule (013); push_log (017); expo_clusters, expo_targets (019); core_countries/sectors/currencies/languages (021-024). View: outstanding_balances (013/014/015).

**Ledger primitif kontrolü:**
- `accounts` — **YOK** (tek "accounts" isabeti Zoho OAuth URL'i `zohoAuth.js:7`)
- `transactions` — **YOK**
- `transfers` — **YOK**
- `budget` — **YOK**
- `expenses` — **VAR ama ölü:** `schema.sql:41-49` (`id, expo_id, category, amount, currency, source`); **hiçbir kod okumuyor/yazmıyor** (INSERT/UPDATE/SELECT FROM expenses taraması boş); Zoho expense sync yok. Tek-seviye `category TEXT` — gereken 2-seviye 6-kat/~75-tip taksonomisi değil, payer/frozen-rate yok.

**finance.js — her endpoint (apps/api/src/routes/finance.js): 9 GET, %100 salt-okunur:**
`/summary`(:24), `/action-list`(:118), `/aging`(:212), `/upcoming`(:250), `/by-expo`(:288), `/by-agent`(:321), `/contract/:id/detail`(:350), `/forecast`(:388), `/recent-activity`(:435). Sıfır INSERT/UPDATE/DELETE.

**Req 2.6/3.3 özellik kontrolü — hepsi YOK:**
- Editable account list (bank/cash/virtual) → YOK
- Two-sided money movement → YOK (contract_payments tek-taraflı, karşı-hesaba bağlı değil)
- İşlem-bazlı frozen rate → YOK (rate contract düzeyinde `contracts.exchange_rate`, işlem düzeyinde değil)
- Computed balance from stream → YOK/TERS (account balance hiç yok; bunun yerine `balance_eur/paid_eur` contracts'ta SAKLANIYOR)
- Owner's current-account → YOK
- EUR consolidation → KISMİ (yalnız contract düzeyi `*_eur`, multi-account konsolidasyon yok)
- Budget-vs-actual → YOK (budget tablosu yok, actuals kaynağı expenses ölü)
- Refund/credit event flow → YOK

**Var olan tek şey:** contracts + contract_payments üstüne kurulu salt-okunur A/R (alacak) tahsilat dashboard'u. **Sıfırdan gerekenler:** editable `accounts` + CRUD, double-entry `transactions`/`transfers` (bağlı iki-taraflı event), işlem-bazlı frozen rate, computed-balance sorguları (stored balance'ları kaldır), Owner current-account, multi-account EUR consolidation, `budget` + budget-vs-actual, refund/credit event flow, gerçek expenses subsystem (2-seviye taksonomi + payer + frozen rate + write path + Zoho `Expensess` sync). **Finansın en ağır parçası, neredeyse tamamen yeni.**

---

## E. AI QUERY ENGINE + RAPOR + RISK + TARGETS — TAM (KORU adası)

**Pipeline gerçek ve uçtan uca bağlı; iki bounding caveat ile dokunmadan korunabilir.**

**E1. AI Query Engine — KORU (sağlam).** `packages/ai/queryEngine.js` + `router.js`:
- Akış: `run()` `:1799` → `extractSemanticFrame()` `:1812` → intent (sıfır-maliyet keyword router `router.js:581`, 20 kural; fallback **Claude Haiku** `FRAME_PROMPT` `:437`, model `AI_INTENT_MODEL` default `claude-haiku-4-5`) → `buildQuery()` `:544` (~25 intent için **parametreli** SQL şablonları, `$N`) → `applyScope()` `:1422` → `validateSQL()` `:1488` (SELECT/WITH zorunlu, INSERT/UPDATE/DELETE/DROP... blocklist `:13`, otomatik LIMIT 200) → `generateAnswer()` **Claude Sonnet** `:1622` (`ANSWER_MODEL` default `claude-sonnet-4-6`).
- **LLM: yalnız Anthropic** (`@anthropic-ai/sdk` `:1,8`, `ANTHROPIC_API_KEY` — tek LLM key, OpenAI yok). **DB: Postgres** (`packages/db`, `DATABASE_URL`), whitelist `ALLOWED_TABLES` `:12`.
- SQL-injection güvenliği: şablon yolu için **iyi** ($N param + tablo whitelist + keyword blocklist). Tek istisna: hybrid Text-to-SQL (`generateSQL()` `:1691`) Sonnet'e raw SQL ürettirir AMA gated (yalnız `general_stats` + boş entity + **CEO only**), yine validateSQL + 3s timeout + max-5-JOIN.
- Bağlı: `POST /api/ai/query` (`ai.js:5`, `server.js:42`) **+** WhatsApp bot (`handler.js:526`).

**E2. Risk Engine — KORU.** `packages/ai/riskEngine.js` velocity/risk_score/risk_level hesaplar (`:36-65`), `expo_metrics`'e UPSERT yazar (`:67`); `briefing/index.js:25` + AI intent `queryEngine.js:947` çağırır.

**E3. Targets — KORU ve YAZILABİLİR.** `packages/targets/index.js` + `apps/api/src/routes/targets.js`: `PUT /:expo_id` `expo_targets`'e UPSERT yazar (`:155,186`), `POST /seed` cluster+target seed (`:218`). **Doğrulandı: `expo_targets`/`expo_clusters` ELIZA'nın TEK owned yazılabilir iş varlığı.** Geri kalan her yazma ya Zoho-sync ya operasyonel log (push_log/message_logs/users).

**E4. Reporting/Finance — KORU (salt-okunur, gerçek).** finance.js (9), revenue.js (`/summary` vb. — `2026` hardcoded caveat `:15`), sales.js (`/leaderboard`, 2026 hardcoded `:13`), fiscal.js. Hepsi çalışır salt-okuma.

**E5. WhatsApp brief/push/attention/alerts — KISMI.** `briefing/attention/alerts/push` bağlı ve wired (`server.js:74`), ama Twilio runtime'a + `sent_briefings` gibi (004-024'te olmayan) tablolara bağlı → çalışma data/runtime-bağımlı.

**E6. Dashboard — KORU.** `apps/dashboard/pages/*` hepsi gerçek ve dolu (War Room 1101 satır, finance 976, targets 760...), client-side AuthGuard ile.

### 🔒 DOKUNULMADAN KORUNACAK (KEEP-UNTOUCHED) sınırı
- **Çekirdek motor (en yüksek güven):** `packages/ai/queryEngine.js`, `router.js`, `riskEngine.js`. Bağımlı: `@anthropic-ai/sdk`+`ANTHROPIC_API_KEY`; `packages/db`; DB objeleri `edition_contracts, fiscal_contracts, contracts, expos, expo_metrics, outstanding_balances, expo_targets`; `packages/attention`.
- **Targets (yazılabilir, owned):** `packages/targets` + `routes/targets.js` + `expo_targets/expo_clusters` (migr 019).
- **Salt-rapor:** `routes/{finance,revenue,sales,fiscal}.js` + `outstanding_balances` view + contract_payments/schedule.
- **Dashboard:** `apps/dashboard/pages/*`.
- **Bot brief/push zinciri:** `packages/{briefing,attention,alerts,push}` (KISMI — koru ama runtime + `sent_briefings` doğrula).

**Korumayı sınırlayan 2 caveat:**
1. **API'de hiç auth yok** (bkz. F) — E'yi korumak erişim kontrolünü korumaz; `applyScope` yalnız `user` geçilince çalışır, HTTP `ai.js:13` geçmiyor → unscoped.
2. **Bağımlılık boşluğu** — `edition_contracts`, `fiscal_contracts`, `expo_metrics` objelerinin CREATE'i 004-024'te **yok**. Çalışan DB'de var ama DDL repo dışında → migration'lardan yeniden kuran bunları alamaz. **"Doğru koruma"nın en büyük riski.**

---

## F. KULLANICI / YETKİ — İSKELET

**Şema + login gerçek; ama API'de server-side yetkilendirme neredeyse yok.**

- **Şema/roller:** `users` (migr 005: role default 'agent', whatsapp_phone, dashboard_permissions JSONB, ...); `user_permissions` (data_scope default 'own', visible_years, can_see_expenses/financials/...). **Roller: ceo/manager/agent** (`users.js:31`). Seed CEO 'Nihat Suer AY'.
- **Login:** `auth.js` JWT + bcrypt (SALT 10). `/login` `:189` email-veya-telefon + bcrypt.compare → JWT {userId, role}. `/me`, `/change-password`, `/set-password`(CEO-only `:394`) JWT doğruluyor.
- **🔴 Yetkilendirme — kritik boşluk:** **Hiçbir auth middleware YOK.** `server.js:39-54` route'ları sıfır global auth ile mount ediyor; routes/ genelinde jwt/Bearer/middleware taraması (auth.js hariç) **boş**; `middleware/` dizini yok. Yani `users` CRUD, `targets` (PUT/POST yazma), `finance`, `system`, `logs`, `ai`, **`/api/auth/migrate`** (DDL çalıştırır!) — hepsi **kimliksiz çağrılabilir.** Tek server-side rol kontrolü `set-password` (`auth.js:394`).
- **Data scope yalnız tek yolda:** `data_scope`/`visible_years` yalnız `queryEngine.applyScope()` içinde uygulanıyor (`:1422`), ve yalnız `user` geçilince → **WhatsApp yolu** (`handler.js:526`) uyguluyor, **HTTP `/api/ai/query` uygulamıyor** (`ai.js:13`). Diğer hiçbir REST route scope'a bakmıyor.
- **Field-level permission YOK** — `can_see_financials/expenses` yalnız WhatsApp `.expense/.note` komutlarını gate'liyor (`handler.js:799`), sonuç kolonlarını maskelemiyor. Kolon-bazlı gizleme mekanizması yok. (Komisyon kolonları zaten sync edilmiyor.)
- **Hardcoded JWT fallback secret KULLANIMDA:** `auth.js:7` `JWT_SECRET || 'eliza-dashboard-secret-key-change-in-production'`; `.env`'de `JWT_SECRET` **YOK** → production fiilen bu public secret'ı kullanıyor. **Bu string'i bilen herkes admin token üretebilir.**
- **Dashboard permission client-only** (`_app.js`), API hiçbir şey zorlamadığı için bypass edilebilir.
- **Auth Zoho'dan bağımsız** — login yalnız local `users` tablosu (`auth.js:197`); WhatsApp `auth.js:16` telefon lookup. Zoho offline iken login çalışır. ✓
- **WhatsApp webhook spoofable** — `whatsapp-bot/src/server.js:20` `req.body.From`'u doğrudan okuyor, **X-Twilio-Signature kontrolü yok** → kayıtlı bir numarayı POST'layan kimliği taklit edebilir.

---

## G. ZOHO BAĞIMLILIĞI — TAM (tek yönlü Zoho→ELIZA)

**Entegrasyon noktaları:**
1. `zohoAuth.js:7,21-22` — OAuth token refresh, **Zoho'ya tek POST** (`accounts.zoho.com/oauth/v2/token`, refresh_token). Auth = `ZOHO_CLIENT_ID/SECRET/REFRESH_TOKEN` env.
2. `syncSalesOrders.js:5,358` — GET `Sales_Orders` → contracts, contract_payments, contract_payment_schedule. Entry: `syncSalesOrders`, `syncPaymentsPass`.
3. `syncExpos.js:5,13` — GET `Vendors` → expos. Entry: `syncExpos`.
4. `fetchSalesOrders.js`, `testToken.js` — debug/util (DB yazmaz).

**Üretim sync entry point sayısı: 3** (`syncSalesOrders`, `syncPaymentsPass`, `syncExpos`), `scheduler.js:36-83` orkestrasyonu.
**Senkronlanan modül: yalnız Sales_Orders + Vendors.** CLAUDE.md'nin bahsettiği Expensess/Sales_Agents/Accounts/Invoices/Contacts **sync edilmiyor** (kod referansı yok). → `expenses`, `sales_agents`, `exhibitors` Zoho'dan hiç dolmuyor.
**Yön: kesin tek-yönlü.** Her CRM çağrısı GET; tek non-GET = OAuth refresh. **ELIZA Zoho'ya asla geri yazmıyor** (zohoapis.com/crm'e POST/PUT/PATCH/DELETE yok).
**Zamanlama:** `node-cron` `scheduler.js:94` (list hourly `0 * * * *`), `:102` (payment 06:00 & 18:00). `server.js:62-63` başlatır (yalnız credential varsa) + manuel `POST /api/system/sync-now`.

### 🔌 ZOHO KAPANINCA ÇALIŞMAYI DURDURAN HER ŞEY
**Donar (güncellenmeyi durdurur — yazarları hep zoho-sync):**
- `contracts` — yeni sözleşme yok, revenue/status/m²/payment güncellemesi yok (`syncSalesOrders.js:247`)
- `contract_payments` — yeni tahsilat yok (`:160`)
- `contract_payment_schedule` — sentetik schedule yalnız sync'te üretiliyor (`:196`)
- `expos` — yeni edisyon/tarih yok (`syncExpos.js:84`)
- Scheduler `getAccessToken()`'da hata verir, loglar; ama API server ayakta kalır (hatalar yakalanıyor)

**Bayatlar (donmuş veriyle render etmeye devam eder):**
- Finance/Collections cockpit, Sales, Fiscal, Revenue, Expo Radar (`finance/sales/fiscal/revenue/expos.js`, `riskEngine.js`)
- AI query cevapları (`queryEngine.js` — edition_contracts/outstanding_balances/expo_metrics)
- Push brief, alerts, briefing, message generator (`packages/{push,alerts,briefing,messages}`)

**Değişmeden çalışır (Zoho bağımlılığı yok):**
- Login/auth, users & permissions, dashboard settings
- Reference data CRUD (core_countries/sectors/currencies/languages via `reference.js`)
- Targets & clusters (`targets.js` — zaten-senkron veriden hesaplanır)
- message_logs, WhatsApp bot'un zaten-senkron veri üstündeki query yolu
- Tüm read endpoint'leri (son-senkron snapshot'ı servis eder)

**Net:** Zoho kesilince ELIZA'nın tüm operasyonel veri seti (contracts/payments/expos) son sync'te donar; uygulama ayakta ve sorgulanabilir kalır ama giderek bayatlar — ve **veriyi güncel tutacak uygulama-içi bir yol yoktur** çünkü yazılabilir giriş yolu yok (A & B'ye bağlanır).

---

## "ELIZA'yı yazılabilir ticari çekirdek yapmak" — EFOR SIRASI (en az → en çok)

| Sıra | Alan | Efor | Neden |
|---|---|---|---|
| 0 | **API auth (önkoşul)** | Orta, **BLOKE EDİCİ** | Bugün API'de hiç auth yok. Yazılabilir finans verisi koymadan ÖNCE şart. JWT middleware + JWT_SECRET + scope enforcement + Twilio imza. |
| 1 | **B. Payment native girişi** | Orta | POST route + paid_eur'u contract_payments'tan hesapla + gerçek schedule. Tablo zaten var. |
| 2 | **A. Contract yazılabilirlik** | Orta-yüksek | Operasyonel kolonlar + create/update route + af_number + status state-machine + convert endpoint + **Zoho/ELIZA alan-sahipliği çatışma çözümü** (en zor). |
| 3 | **C. Commission** | Yüksek (greenfield) | Tier kolonları + agent pct + hesaplama motoru + paid-status + adjustment netting; sıfırdan. |
| 4 | **D. Multi-account ledger** | En çok (neredeyse tam yeni) | accounts + double-entry transactions/transfers + frozen rate + computed balance + owner current-account + budget + refund/credit + gerçek expenses subsystem. |

> **Önkoşul vurgusu:** Sıra-0 (API auth) eforu orta ama **bloke edici** — finansal yazma
> verisi açık bir API'ye konulamaz. Yapılış önceliğinde mutlak 1.

---

## KORU ADALARI (dokunulmadan korunacaklar) — net liste

1. **AI çekirdek motoru** — `packages/ai/queryEngine.js`, `router.js`, `riskEngine.js`
2. **Targets (yazılabilir, owned)** — `packages/targets`, `routes/targets.js`, `expo_targets/expo_clusters`
3. **Salt-okunur raporlama** — `routes/{finance,revenue,sales,fiscal}.js`, `outstanding_balances` view
4. **Dashboard** — `apps/dashboard/pages/*`
5. **Bot brief/push zinciri** — `packages/{briefing,attention,alerts,push}` (KISMI — runtime doğrulanmalı)

**İki şart:** (a) bu adaların önüne gerçek API auth eklenmeli (şu an açık), (b) eksik DDL
(`edition_contracts/fiscal_contracts/expo_metrics` view/tablo) repoya alınmalı — yoksa
"korunan" parça yeniden kurulamaz.

---

## EN BÜYÜK 3 RİSK / SÜRPRİZ

1. **🔴 API'DE HİÇ AUTH YOK — LIFFY'den daha kötü.** ELIZA'nın TÜM REST API'si (users CRUD,
   targets yazma, finance, hatta DDL çalıştıran `/api/auth/migrate`) **kimliksiz çağrılabilir**
   (`server.js:39-54`, middleware yok). Üstüne hardcoded JWT fallback secret fiilen kullanımda
   (`auth.js:7`, `.env`'de JWT_SECRET yok) ve WhatsApp webhook imzasız → kimlik taklit edilebilir.
   LIFFY en azından authenticate ediyordu; ELIZA etmiyor. Yazılabilir finansal çekirdek
   koymadan önce **mutlak blocker.**

2. **🟠 ELIZA'nın "kendi alanı" bir sahiplik yanılsaması.** Contract+payment+finance, ELIZA'nın
   çekirdeği sanılıyor ama gerçekte **donmuş salt-okunur Zoho aynası**: write path yok, operasyonel
   alanlar şemada bile yok, sync upsert herhangi bir düzenlemeyi ezer. Yazılabilir yapmak "genişlet"
   değil, **write katmanını sıfırdan kur + Zoho/ELIZA alan-sahipliğini çöz.** ELIZA'nın tek gerçek
   owned yazılabilir varlığı `expo_targets`/`expo_clusters`. Üstelik tüm finans CLAUDE.md'de
   "never write back" diye **tasarımca read-only** — yazılabilir yapmak kurucu tasarıma aykırı.

3. **🟡 EKSİK MIGRATION'LAR — KORU adasını bile tehdit ediyor.** Migration 001-003/010 repoda yok;
   `contracts.status/currency/exchange_rate/revenue_eur` kolonları ve **korumak istediğimiz AI
   motorunun bağımlı olduğu** view'lar (`edition_contracts/fiscal_contracts/expo_metrics`) repoda
   CREATE'siz. DB salt kaynaktan yeniden kurulamaz — gizli bir devir/handover mayını.

   **Bonus sürpriz (pozitif):** "ELIZA zayıf" beklenirken AI/raporlama katmanı gerçekten
   üretim-kalitesinde (TAM): parametreli SQL şablonları, whitelist+blocklist SQL validator,
   Haiku-intent + Sonnet-cevap, yazılabilir targets motoru. Sorun "zeka katmanı yok" değil;
   sorun onun altındaki **yazılabilir işlem çekirdeğinin hiç olmaması + API'nin açık olması.**

---

## METODOLOJİ & SINIRLAR
- 3 paralel ajan: (A+B+G), (C+D), (E+F). Her bulgu `dosya:satır`. node_modules + apps/dashboard/.next taranmadı.
- Olgunluk: TAM/KISMI/İSKELET/BOZUK/YOK. ELIZA'da "BOZUK" yerine çoğunlukla "İSKELET" (kod var
  ama amaç=yazılabilir-çekirdek için yetersiz/salt-okunur) ve "YOK" hakim.
- **Bulamadım:** migration 001-003/010; `edition_contracts/fiscal_contracts/expo_metrics` CREATE'i;
  herhangi bir contracts/payments write route'u; commission tablosu/kolonu; accounts/transactions/
  transfers/budget tabloları; herhangi bir API auth middleware'i — hiçbiri yok.
- "Var" denen her şey kanıtlı; kanıtlanamayan "bulamadım" dendi. Hiçbir dosya değiştirilmedi.
