> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# ELL — GAP + KURTARILABİLİRLİK ANALİZİ

> **Soru (her ihtiyaç için):** (a) Bugün var mı? (b) Ne kadar tam/sağlam? (c) Kurtarılır mı, baştan mı?
>
> **Kaynaklar:**
> 1. `~/Downloads/ELAN_EXPO_REQUIREMENTS_v1_0.md` — Part 2 (8 workflow) + Part 3 (cross-cutting). (Not: `~/Projects/` değil `~/Downloads/`'ta.)
> 2. Üç sistemin **gerçek kodu** (dokümana değil koda bakıldı):
>    - LEENA: `~/Desktop/Leena_Projesi/Leena_v401_monorepo` (app: `backend/leena-v401-backend`)
>    - LIFFY: `~/Projects/liffyv1` (+ `~/Projects/liffy-ui`)
>    - ELIZA: `~/Projects/eliza`
>
> **Yöntem:** Üç paralel kod-inceleme ajanı; her iddia `dosya:satır` ile. Hiçbir dosya değiştirilmedi. Bulunamayan → "bulamadım". Spekülasyon yok.
>
> **Olgunluk:** YOK (hiç kod) / İSKELET (tablo/route var, iş mantığı boş-yarım) / KISMI (çalışıyor ama requirement'ın altında) / TAM (büyük ölçüde karşılıyor)
> **Kurtarılabilirlik:** KORU / GENİŞLET / REFAKTÖR / BAŞTAN (kod referans bile olamaz) / YENİ (hiç yok)

---

## TL;DR — SUER'İN 6 SORUSU (net cevap)

1. **QUOTE üçünde de var mı?** → **HİÇBİRİNDE YOK. Suer haklı.** LIFFY'de tek iz bir TODO yorumu (`actionEngine.js:129-130` "// Implement when quotes table is created"). ELIZA'da yok, LEENA'da yok. Ürün/fiyat kataloğu, line-item, AF-number üretimi, subject auto-gen — hiçbiri yok. **Olgunluk: YOK / Kurtarılabilirlik: YENİ (sıfırdan).**

2. **SALES CONTRACT — Zoho-sync kopya mı, gerçek yönetim mi? Convert gate var mı?** → **Salt-okunur Zoho cache.** ELIZA `contracts` tablosuna yazan TEK yol Zoho sync (`syncSalesOrders.js:247-284`). Hiçbir route contracts'a INSERT/UPDATE yapmıyor; 5-status lifecycle yok (status yalnız okuma filtresi); operasyonel alanlar (scan_link, catalogue_page, stand) şemada hiç yok. **Convert gate (quote→contract, Q→A) HİÇ YOK.** Gerçek sözleşme yönetimi olarak: **YOK / BAŞTAN.**

3. **CATALOGUE GENERATOR — Corel Draw'ı bitirecek otomatik üretim izi?** → **HİÇ İZ YOK.** LEENA'da `catalogue/corel/pdf-engine` grep = sıfır; `package.json`'da PDF kütüphanesi yok (pdfkit/puppeteer/playwright yok); `catalogue_submission` tablosu yok; self-service editör yok. Tek "PDF" = sertifikada tarayıcı print dialog'u. **YOK / YENİ.**

4. **EMAIL AUTOMATION — 8'li operasyonel zincir + per-expo trigger?** → **Zincir YOK.** LEENA'da genel e-posta altyapısı var (`email_templates`, `email_queue`, `email_worker.js`, reactivation, sequence campaigns) ama isimli 8-aşama (Welcome/Catalogue/Stand Design/Boost/Extra Service/BuildUp/Payment Reminder/Badge) ve **per-expo days-before-expo trigger config** yok. Altyapı: İSKELET/GENİŞLET; zincirin kendisi: YENİ.

5. **MULTI-ACCOUNT LEDGER — ELIZA'da ne kadarı gerçek?** → **Neredeyse hiçbiri.** accounts / transactions / transfers / budget tablolarının **hiçbiri yok**. `finance.js` baştan sona salt-okunur (9 endpoint, hepsi SELECT). Two-sided money movement, işlem-bazlı frozen rate, transaction-stream'den hesaplanan bakiye, Owner's current-account, budget-vs-actual — **hiçbiri uygulanmamış.** Mevcut "finance" = Zoho sözleşme bakiyelerinin tahsilat raporlaması. **YOK / YENİ.**

6. **PERMISSION MATRIX — field-level per-user mi, basit role mu?** → **Hiçbirinde field-level matris YOK.**
   - LIFFY: rol string + olgun hiyerarşik data-scope; `users.permissions` JSONB kolonu var ama **hiçbir kod okumuyor** (ölü iskelet). → İSKELET/GENİŞLET
   - ELIZA: rol (ceo/manager/agent) + data_scope (all/team/own) + **modül-seviye** `dashboard_permissions` JSONB. Alan-seviye yok. → KISMI/GENİŞLET
   - LEENA: yalnızca tek-tenant organizer auth, rol bile yok. → YOK/YENİ
   - **Hiçbirinde:** module×action matrisi, "Convert Quote" gibi special-perm, profile template, hücre-bazlı düzenleme. Field-level matris sıfırdan kurulacak ama LIFFY'nin scope altyapısı sağlam temel.

---

## TAM ENVANTER

### Part 2.1 — Lead Management (sahip: LIFFY)

| İhtiyaç | Bugün var mı | Olgunluk | Kurtarılabilirlik | Gerekçe (dosya:satır) |
|---|---|---|---|---|
| Lead intake çok-kanallı (mining/web-form/excel/manual) | Kısmen | KISMI | GENİŞLET | Import iki format `liffyv1 leads.js:133`; web-form & manual create endpoint **bulamadım**; `source_type` serbest metin `leads.js:268` |
| Lead enrichment (reply parse → güncelle) | Evet | KISMI | KORU | İmza parse `utils/signatureParser.js:61`; hedef `affiliations`/`persons`, "lead" değil |
| Disqualification (kategorize sebep) | Hayır | YOK | YENİ | `disqualif` grep boş; sadece pipeline `is_lost` stage `migr 031` |
| Auto-routing / ownership | Hayır (otomatik) | İSKELET | YENİ | `created_by_user_id`/`pipeline_assigned_user_id` var `migr 032` ama atama mantığı yok |
| Intake dedup (email/domain/company) | Sadece email | KISMI | GENİŞLET | `leads.js:219-224,295` email ON CONFLICT; domain/company dedup yok |
| Email verification (ZeroBounce) | Evet | TAM | KORU | `services/verification.js:5,28`; org-bazlı key; queue/verify |
| Lead scoring / prioritization | Engagement kısmi | İSKELET | GENİŞLET | Formal skor yok; sadece `action_items.priority` P1-P4 `migr 037` |

### Part 2.2 — Sales Cycle / Quote / Convert Gate

| İhtiyaç | Sahip | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|---|
| Contact + Company + lead→contact conversion | LIFFY | Tablolar var, akış yarım | KISMI | GENİŞLET | `persons`(015)/`affiliations`(016)/`companies`(046); `companies.js:24` hâlâ affiliations'tan aggregate, formal convert yok |
| **QUOTE** (subject auto-gen, AF#, ürün katalog, line-item, currency-freeze, validity, Signed) | LIFFY | **HAYIR** | **YOK** | **YENİ** | `quote/proforma/af_number/product/pricing` grep = sıfır; tek iz TODO `actionEngine.js:129-130` |
| **CONVERT GATE** (Signed→notify Project→Convert→ELIZA contract, Q→A) | LIFFY→ELIZA | **HAYIR** | **YOK** | **YENİ** | LIFFY: `convert/sales_contract` grep boş (`zoho.js` push alakasız). ELIZA: convert/quote kodu yok |

### Part 2.3 — Sales Contract Management (sahip: ELIZA)

| İhtiyaç | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|
| **Sales Contract yönetimi** (long-running kayıt, edit) | Sadece read-cache | **YOK** (mgmt) | **BAŞTAN** | contracts'a tek yazan Zoho sync `syncSalesOrders.js:247-284`; hiçbir route yazmıyor |
| 5-status lifecycle (Active/On Hold/Transferred/Cancelled), Project-restricted | Hayır | YOK | YENİ | `status` yalnız okuma filtresi `finance.js:55`; lifecycle yazımı yok |
| Transfer (first-class, transferred_from_contract_id) | Hayır | YOK | YENİ | string olarak okunuyor; transfer linki/devir mantığı yok |
| Three-tier commission (agent/SR/SD, default+override, paid status, adjustment) | Hayır | YOK | YENİ | "commission" tek yerde WhatsApp format `handler.js:973`; migr 013 yalnız ödeme alanı ekledi, komisyon değil |
| Payment schedule vs received | Kısmen | KISMI | Payments KORU / Schedule REFAKTÖR | Payments gerçek Zoho subform `syncSalesOrders.js:99-167`; schedule SENTETİK `is_synthetic=true :170-208`; `paid_eur` denormalize (computed değil) |

### Part 2.4 — Catalogue Production (sahip: LEENA)

| İhtiyaç | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|
| **Catalogue generator (print PDF + web)** | Hayır | YOK | YENİ | `catalogue/corel` grep sıfır; PDF lib yok `package.json:18-31`; `catalogue_submission` tablosu yok |
| Exhibitor self-service editör + 3-4 master template + deadline lock | Hayır | YOK | YENİ | `public/`'te catalogue sayfası yok; template engine yok |

### Part 2.5 — Expo Operations (sahip: LEENA; cluster: ELIZA)

| İhtiyaç | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|
| Expo master record (timing/deadline/contacts/URL alanları) | Kısmen | İSKELET | GENİŞLET | `expos` yalnız 6 alan `initial.sql:17-29`; edition/sector/venue/build-up/deadline/contacts YOK |
| Expo partners (role enum, contact, is_primary) | Hayır | YOK | YENİ | `partner` grep sıfır; `expo_partners` tablosu yok |
| Co-located clusters | ELIZA'da var, LEENA'da yok | ELIZA KISMI / LEENA YOK | GENİŞLET(ELIZA)/YENİ(LEENA) | ELIZA `expo_clusters` (migr 019); LEENA'da `cluster` grep sıfır |
| **Floor plan builder** (grid, version, split/merge/clone, special area) | Evet | **TAM** | **KORU** | `migr 001` 5 tablo; `routes/floorplan.js` 16 endpoint (activate:271, clone:326, split:764, merge:902); `floorplan-builder.html` |
| **Visitor mgmt + check-in** (reg/QR/badge/import-upsert/reactivation/cert/terminal/lead-scan) | Evet | **TAM** | **KORU** | visitors 12 endpoint (upsert :530); QR `utils/qrcode.js`; terminal `terminalCheckins.js`; lead `leads.js`; reactivation 40KB |
| Exhibitor list entegrasyonu (ELIZA'dan çek, cache, event-refresh) | Hayır | YOK | YENİ | `eliza/axios` grep sıfır; outbound API client yok; `company_id` hiç sync edilmeyen nullable kolon |

### Part 2.6 — Financial Operations (sahip: ELIZA)

| İhtiyaç | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|
| **Multi-account ledger** (editable accounts, two-sided, frozen rate, computed balance, Owner current-acct, EUR consol.) | Hayır | YOK | YENİ | accounts/transactions/transfers/budget tabloları **yok**; `finance.js` salt-okunur 9 GET |
| Expenses (2-seviye kategori/tip, expo attribution, payer, frozen rate) | İskelet (kullanılmıyor) | İSKELET | BAŞTAN | `schema.sql:41-49` tek-seviye category TEXT; okuyan/yazan kod yok; `.expense` komutu stub `handler.js:798-803` |
| Budget-vs-actual per expo/category | Hayır | YOK | YENİ | budget tablosu yok |
| Multi-currency frozen rate (original+EUR dual) | Sync-seviye | KISMI | GENİŞLET | `syncSalesOrders.js:49-56,121-163` çevrim var ama Zoho `Exchange_Rate`'e bağlı, işlem-bazlı kalıcı ledger değil |
| Refund / credit balance (event flow) | Hayır | YOK | YENİ | ledger olmadığı için yok |

### Part 2.7 — Communication Automation

| İhtiyaç | Sahip | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|---|
| 8-email operasyonel zincir + per-expo trigger | LEENA/? | Altyapı var, zincir yok | İSKELET | GENİŞLET(altyapı)+YENİ(zincir) | LEENA `email_templates/email_queue/email_worker.js`, sequence campaigns `migr 004`; isimli 8-aşama + days-before config YOK |
| Marketing campaigns + per-recipient unsubscribe + op/marketing flag | LIFFY | Campaign TAM, unsub global | KISMI | GENİŞLET | `campaigns.js`+`campaignSend.js`+`migr 035` TAM; unsub global org `migr 012`; per-recipient state + template tür flag YOK |
| Inbound reply → contract communication history | ELIZA/LEENA | Hayır | YOK | YENİ | Sözleşme sayfası + email history birleşimi yok (contract mgmt olmadığı için) |

### Part 2.8 — Reporting & Intelligence (sahip: ELIZA)

| İhtiyaç | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|
| **Reporting / dashboard / AI insights / risk / targets / WhatsApp brief** | Evet | **TAM** | **KORU** | AI query engine `queryEngine.js`(2234 satır)+`router.js`; risk `riskEngine.js`; finance dashboard `finance.js`; targets yazılabilir `targets.js:155-230`; `packages/push,briefing,attention` |

### Part 3 — Cross-Cutting

| İhtiyaç | Sahip | Bugün var mı | Olgunluk | Kurtar. | Gerekçe |
|---|---|---|---|---|---|
| **Permission matrix (field-level per-user)** | hepsi | Hayır (role+scope) | İSKELET | GENİŞLET | LIFFY `permissions` JSONB ölü `migr 039`; ELIZA modül-seviye `dashboard_permissions` `users.js:6-27`; LEENA tek-tenant; field-level matris/special-perm/template yok |
| Hierarchical visibility / data scope | LIFFY/ELIZA | Evet | TAM(LIFFY)/KISMI(ELIZA) | KORU | LIFFY recursive CTE `userScope.js:122-141`; ELIZA data_scope all/team/own `005_users.sql:20-31`; LIFFY'de office scope bulamadım |
| Identity ayrımı (users / sales-agents / data-entry contractors) | hepsi | Kısmen | İSKELET | GENİŞLET | ELIZA `sales_agents` var; LIFFY yalnız `users`+role; üçlü ayrım eksik, contractor entity yok |
| Reference data yönetimi (admin-editable) | ELIZA owns | Kısmen | KISMI | GENİŞLET | ELIZA `core_countries/sectors/currencies/languages` (migr 021-024); admin UI + cross-system replikasyon eksik; LIFFY/LEENA reference yok |
| Audit log (who/when/before-after) | hepsi | Hayır | YOK | YENİ | Üçünde de audit tablosu yok; sadece created/updated_at; ELIZA `message_logs/sync_log` audit değil |
| Search & navigation (global, scope-aware, saved filters) | hepsi | Hayır | YOK | YENİ | Global cross-module search + saved/shared filter + pinned/recent kodu bulamadım |
| Notification system (in-app/email/WhatsApp + prefs) | hepsi | Hayır | YOK | YENİ | LIFFY `action_items` komşu iskelet; in-app/prefs tablosu yok; ELIZA WhatsApp push var ama genel notif değil |
| Internal API (sistemler arası) | hepsi | Hayır | YOK | YENİ | Hiçbirinde diğerine API client yok (önceki analiz + bu taramada doğrulandı) |

---

## ÖZET SAYIM (35 ana ihtiyaç)

### Olgunluğa göre
| Olgunluk | Adet | Hangileri (özet) |
|---|---|---|
| **TAM** | **4** | Floor plan, Visitor+check-in, Email verification, Reporting/AI |
| **KISMI** | **9** | Lead intake, enrichment, dedup, contact+company, payment schedule/received, multi-currency, marketing campaigns, reference data, hierarchical scope(ELIZA) |
| **İSKELET** | **7** | Lead auto-routing, lead scoring, expo master, expenses, email-chain altyapı, permission matrix, identity ayrımı |
| **YOK** | **15** | Quote, convert gate, contract mgmt, status lifecycle, transfer, commission, catalogue gen, catalogue editor, expo partners, multi-account ledger, budget, refund/credit, exhibitor-integration, audit, search, notification, internal-API, inbound-reply-history *(bazıları aşağıda gruplandı)* |

*(Hierarchical scope LIFFY'de TAM, ELIZA'da KISMI — tek satırda KISMI/TAM olarak sayıldı.)*

### Kurtarılabilirliğe göre
| Kurtar. | Adet | Anlamı |
|---|---|---|
| **KORU** | **5** | Floor plan, Visitor+check-in, Email verification, Reporting/AI, Hierarchical scope |
| **GENİŞLET** | **12** | Lead intake/enrichment/dedup/scoring, contact+company, expo master, clusters(ELIZA), multi-currency, marketing campaigns, permission(scope altyapısı), identity, reference data |
| **REFAKTÖR** | **1** | Payment schedule (sentetik → gerçek vade) |
| **BAŞTAN** | **2** | Sales contract management (cache referans değil), expenses (iskelet) |
| **YENİ** | **15** | Quote, convert gate, status lifecycle, transfer, commission, catalogue gen, catalogue editor, expo partners, LEENA-cluster, multi-account ledger, budget, refund/credit, exhibitor-integration, audit, search, notification, internal-API |

### Kabaca: "mevcut üzerine ekleme" vs "sıfırdan"
- **Mevcut üzerine (KORU+GENİŞLET+REFAKTÖR): ~18 ihtiyaç (~%51)**
- **Sıfırdan (BAŞTAN+YENİ): ~17 ihtiyaç (~%49)**

> ⚠️ **Sayı yanıltıcı olabilir — EFOR ile ADET farklı.** Sıfırdan yapılacaklar
> sistemin **ticari çekirdeği**: quote → contract → convert → commission → multi-account
> ledger → catalogue generator → email chain. Bunlar hem en ağır hem en kritik modüller.
> "Mevcut üzerine" tarafı ise çoğunlukla **çevre/destek** (lead pipeline iyileştirme,
> scope, reference data) + iki güçlü ada (LEENA operasyon, ELIZA raporlama).
> **Adetçe ~50/50; eforca ağırlık net biçimde "sıfırdan" tarafında.**

---

## EN ÇOK KURTARILABİLİR vs EN ZAYIF

**En kurtarılabilir (KORU adaları) — ama farklı KATMANLARDA:**
- **LEENA = en güçlü OPERASYONEL temel.** Floor plan builder ve visitor/check-in/badge/
  lead-scanner gerçekten TAM ve sağlam (`floorplan.js` 16 endpoint, `visitors.js` upsert,
  terminal/reactivation/cert). Requirement 2.5'in "bugün operasyonel" dediği kısım doğru.
- **ELIZA = en güçlü ZEKA/RAPORLAMA temeli.** AI query engine (2234 satır), risk engine,
  targets, finance/collections raporlaması, WhatsApp brief — hepsi çalışır durumda (KORU).
- **LIFFY = en güçlü VERİ-PİPELİNE temeli.** Mining + email verification + campaign +
  hierarchical scope olgun; lead pipeline GENİŞLET ile büyür.

**En zayıf — ve en kritik boşluk: TİCARİ ÇEKİRDEK.**
- Quote, sales-contract yönetimi, convert gate, three-tier commission, multi-account
  ledger, catalogue generator, 8-email operasyonel zinciri — **hiçbiri yok.** Üç sistemin
  hiçbiri bu çekirdeği taşımıyor.
- **ELIZA'nın kritik yanılsaması:** kendi alanı (contract + finance) sanılıyor ama gerçekte
  contracts/payments **tamamen Zoho'dan türetilen salt-okunur kopya.** ELIZA içinde
  yazılabilir tek "owned" varlık `expo_targets` / `expo_clusters`. Yani ELIZA bir
  **oversight/analiz katmanı**, bir işlem (transaction) sistemi değil. Ticari çekirdeği
  ELL'de sıfırdan kurmak gerekiyor — Zoho mirror'ı temel alınamaz.

**Özet tablo:**
| Sistem | Güçlü (KORU) | Zayıf/eksik |
|---|---|---|
| LEENA | Floor plan, visitor, check-in, badge, lead-scan | Catalogue gen, expo master detay, partners, cluster, email-chain, permission, audit |
| LIFFY | Mining, email-verify, campaign, data-scope | Quote, convert, disqualification, auto-routing, reference, audit, notification |
| ELIZA | AI/query, risk, targets, raporlama | Gerçek contract mgmt, ledger, expenses, commission, convert, audit |

---

## METODOLOJİ & SINIRLAR

- 35 ana ihtiyaç Part 2 (8 workflow) + Part 3 (3.1-3.9) içinden çıkarıldı. Part 4 (wishlist)
  ve Part 5 (out-of-scope) kapsam dışı.
- Bir ihtiyaç birden çok sistemi ilgilendiriyorsa (permission, audit, identity, scope)
  baskın durum tek satırda verildi; sistem-bazlı nüanslar "Gerekçe" sütununda.
- Phase-2 işaretli requirement öğeleri (online payment, e-invoice, accounting export,
  sales-floorplan-template, stand-auto-link) ölçüme dahil edilmedi (3.9 zaten "Phase 2" diyor).
- **Bulamadım (dürüst boşluklar):** ELIZA migration listesinde 001-003 ve 010 yok;
  `contracts.revenue_eur/currency/exchange_rate/status` kolonlarının `ALTER TABLE`'ı
  bulunamadı (eksik migration veya elle uygulanmış şema) — kod bu kolonları kullanıyor
  ama tanımları izlenemedi. LIFFY web-form/manual lead-create endpoint'i, office-scope;
  üç sistemde search & notification kodu — hiçbiri bulunamadı (yokluk delili, ama
  derinlemesine her dosya taranmadı). Bu öğeler "YOK" olarak işaretlendi; aksini gösteren
  kod çıkarsa güncellenebilir.
- "Var" denen her şey `dosya:satır` ile kanıtlandı; kanıtlanamayan "bulamadım" dendi.
