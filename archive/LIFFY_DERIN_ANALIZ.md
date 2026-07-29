> 📌 MİMARİ FAZ KANIT BELGESİ (arşiv, 2026-07-28) — tarihsel ölçüm; yürürlükteki
> kural DEĞİL. Güncel durum: ELL_DURUM_DEFTERI_v2.md · faz/ilke: ELL_YOL_HARITASI_v5.md

# LIFFY — DERİN ANALİZ (satışa hazırlık ölçümü)

> **Amaç:** LIFFY'yi satış ekibinin gerçekten kullanabileceği tam bir araç yapmak için
> alan-bazında NE kadar iş gerektiğini ölçmek. Şu an kullanılmıyor ("çok eksiği var") —
> eksiklerin tam, kod-kanıtlı envanteri.
>
> **Kod:** backend `~/Projects/liffyv1`, frontend `~/Projects/liffy-ui`, miner `~/Projects/liffy-local-miner`
> **Referans:** `~/Downloads/ELAN_EXPO_REQUIREMENTS_v1_0.md` (2.1 Lead Mgmt + 2.2 Sales Cycle/Quote)
> **Yöntem:** 3 paralel kod-inceleme ajanı, her iddia `dosya:satır` ile. Dokümana güvenilmedi.
> Hiçbir dosya değiştirilmedi. Bulunamayan → "bulamadım". Spekülasyon yok.

---

## TL;DR — Alan durumları tek bakışta

| Alan | Durum | Tek cümle |
|---|---|---|
| **A. Mining** | **KISMI** | Bulut tarafı scraper gerçek ve güçlü, ama **self-service DEĞİL** — engellenen sitede bir geliştirici e-postayla gelen CLI komutunu elle çalıştırıyor; üstelik madenlenen lead'ler varsayılan olarak contact tablolarına bile düşmüyor. |
| **B. Lead Pipeline** | **KISMI** | Pipeline/atama/CSV-import/enrichment uçtan uca çalışıyor, ama **manuel tek-lead ekleme endpoint'i yok** ve disqualification (sebepli eleme) yok. |
| **C. Campaign** | **TAM** | Sürpriz: sistemin EN olgun parçası — oluştur→doğrula→gönder→sequence→open/click/reply/bounce takibi→unsubscribe hepsi çalışır ve worker'lara bağlı. |
| **D. Quote** | **YOK** | Gerçekten sıfır — tablo yok, route yok, ürün/fiyat kataloğu yok, currency yok, AF-number üreteci yok. Tek iz bir TODO stub'ı. |
| **E. Yetki/Güvenlik** | **BOZUK** (freelancer senaryosu için) | Hiyerarşik izin çatısı var AMA asıl müşteri/lead tablolarına uygulanmamış: **her satışçı tüm şirketin contact/lead/pipeline verisini görüp dışa aktarabiliyor ve silebiliyor.** |
| **F. Frontend** | **KISMI** | En geniş kapsamlı parça — ~20 sayfa gerçek API'lere bağlı, stub yok; ama route koruması sadece client-side localStorage ve backend'in veri sızıntısını aynen ekrana yansıtıyor. |

---

## A. MINING — KISMI

**Ne çalışıyor:**
- **İki motor var.** (1) **Bulut SuperMiner** — backend worker tabanlı: `worker.js:442 processNextJob()` `mining_jobs WHERE status='pending'` poll eder (`worker.js:448-453`), `services/superMiner/` altında gerçek adaptörler (playwright/httpBasic/websiteScraper/ai) `services/superMiner/adapters/`. (2) **`liffy-local-miner` CLI** — yalnız bulut bloklanınca devreye giren fallback.
- ExpoPlatform siteleri için özel miner (`liffy-local-miner/mine.js:1615 isExpoPlatformUrl`, `miners/expoPlatformMiner.js`); ek pluginler `directoryMiner/apiMiner/countryMiner/listMiner`.
- Job akışı: CLI `fetchJob` GET `/mining/jobs/:id` (`mine.js:185`), `postResults` POST `/mining/jobs/:id/results` (`mine.js:229`); backend CLI'yi statik token ile doğrular `routes/miningResults.js:56-68`.

**Çıktı nereye yazılıyor:**
- Sonuçlar **`mining_results`** tablosuna (`routes/miningResults.js:216-255`), **doğrudan `persons`/`prospects`'e DEĞİL.**
- Canonical `persons`+`affiliations`'a terfi **best-effort ve env-gated:** `services/aggregationTrigger.js:34` yalnız `AGGREGATION_PERSIST==='true'` ise yazıyor; varsayılan shadow/log-only. `.env`'de set DEĞİL → madenlenen kişiler `mining_results`'ta kalıp manuel import bekliyor (`routes/leads.js:149-183` veya `routes/miningResults.js:853`).

**Somut eksikler / "neden kullanılmıyor":**
- **Self-service DEĞİL — en kritik bulgu.** Site bloklanınca/sıfır-sonuç/kirlilikte `worker.js:497-543` → `triggerManualAssist(job)` (`worker.js:616`): job `status='needs_manual'` olur ve admin'e **kopyala-yapıştır terminal komutu e-postalanır** (`worker.js:651`):
  `cd ~/Projects/liffy-local-miner && node mine.js --job-id ${job.id} --api ... --token ${token} ...`
  Bir insanın terminal açıp Node+Playwright'lı bir makinede çalıştırması gerekiyor. Yani mining bir geliştirici aracı, satışçı özelliği değil.
- `generated_miners` (migr 024, AI üretimi scraper + onay akışı): tablo + CRUD + generate/approve endpoint'leri var (`routes/adminAIMiner.js`, `server.js:92`) ama **runtime kapalı** — `flowOrchestrator.js:966` yalnız `AI_MINER_GENERATOR_ENABLED==='true'` ve `ANTHROPIC_API_KEY` varsa çalışır; ikisi de set değil. **İskelet-artı: kod tam, runtime devre dışı.**
- Hardcoded bağımlılık: `.env`'de gerçek uzun-ömürlü `MINING_API_TOKEN` JWT + hardcoded `MINING_JOB_ID=bd4fccb0-...` (`backend/.env:2-3`); aynı token manuel-miner auth secret'ı. Manual-assist e-posta fallback alıcısı hardcoded `suer@elan-expo.com` (`worker.js:674`).
- `http` stratejisi uygulanmamış (`mine.js:1610`); çift/ölü motor (`services/miningWorker.js` yalnız `MINING_TEST=1`), `.bak/.save/worker.js.backup*` dosyaları. `liffy-local-miner/orchestrator.js` standalone, `mine.js` tarafından çağrılmıyor (coverage orchestration gerçek yolda değil).
- 38 adet `mining_*.json` çıktı dosyası (`mine.js:246-280`, gitignored) → mining'in site-başına ad-hoc/elle çalıştırıldığını, yerel JSON'un asıl çalışma artefaktı olduğunu gösteriyor.

---

## B. LEAD PIPELINE & YÖNETİMİ — KISMI

**Intake yolları:**
- Mining→import: çalışıyor `routes/leads.js:149-183` (`result_ids` → prospects+persons+affiliations dual-write, INSERT `:293,:308`).
- CSV import: uçtan uca çalışıyor `routes/lists.js:401` (multer `:145`, csv-parser `:193`, batch + verification kuyruğu `:219-385`).
- Frontend dizi import: `leads.js:145-148`. Dosya mining (PDF/Excel/Word) upload: `routes/miningJobs.js:29`.
- **Manuel tek-lead/kişi oluşturma: YOK.** `routes/persons.js`'te POST yok (yalnız GET/DELETE `:24,:589`); `routes/leads.js`'te düz create yok. Bir satışçı tanıştığı tek kişiyi CSV'siz ekleyemiyor.

**Pipeline / atama / sahiplik:**
- Stage CRUD tam: `routes/pipeline.js:39,57,103,146`; 7 seed stage (Won/Lost flag) `migr 031`. Kanban board `pipeline.js:180`. Stage taşıma `PATCH /api/persons/:id/stage` `pipeline.js:311` + activity log.
- Atama **yalnız first-touch:** `pipeline.js:347-349` (`nextAssignee = currentAssignee || userId`); **round-robin/kural-bazlı routing YOK** (grep boş).

**Enrichment:** çalışıyor — reply webhook `parseEmailSignature`+`enrichPersonFromSignature` (`routes/webhooks.js:843-845`); yalnız NULL alanları doldurur (`utils/signatureParser.js:200-281`), `auto_enrichment` activity loglar.

**Somut eksikler:**
- Manuel tek-kişi ekleme endpoint'i yok.
- Disqualification sebep taksonomisi yok (`disqualif/lost_reason` grep boş; sadece generic `Lost` stage).
- Atama first-touch; territory/round-robin yok.
- Dedup yalnız email (`services/validators/deduplicator.js:25-37`); domain/company dedup yok (domain dedup yalnız source discovery'de).
- mining_results→pipeline terfisi manuel adım gerektiriyor (AGGREGATION_PERSIST kapalı).
- **Çalışan günlük-CRM parçaları (artı):** not/görev/activity `routes/contactCrm.js:90,269,327`, tag `leads.js:396,434`.

---

## C. CAMPAIGN — TAM ✅ (sistemin en olgun parçası)

**Ne çalışıyor (uçtan uca):**
- Yaşam döngüsü state machine: create `routes/campaigns.js:60`; list→recipient resolve+verify+unsub+dedup `:414-757`; start/pause/resume/schedule `:760,:866,:907,:948`; zamanlanmış otomatik aktivasyon `services/campaignScheduler.js` (worker `worker.js:107-116`).
- Gönderim altyapısı (SendGrid, gerçek worker): `mailer.js:1,44,136` per-organizer key; worker loop `worker.js:142-353` (`FOR UPDATE SKIP LOCKED` `:185-190`, atomic CAS çift-gönderim önleme `:206-215`, 429 backoff `:121-137`).
- **Email verification (ZeroBounce) çalışır:** `services/verificationService.js` (checkCredits:28, verifySingle:48, queueEmails:79, processQueue:195-264); route `routes/verification.js` (`/verify-list` bir list_id alıp tüm üyeleri kuyruğa atar `:115-187`); worker'da arka plan işleme `worker.js:358-399`; resolve verification-mode'a saygı duyar `campaigns.js:490-497`.
- **Reply takibi var ve aksiyona dönüyor:** SendGrid event webhook `routes/webhooks.js:47-75`; inbound reply handler `:611-868` — kaynak tespiti (`detectReplySource :418`), `reply` event `:726`, `prospect_intent` `:729`, pipeline'ı "Interested"a taşır `:793`, sequence'i durdurur `:818`, Action Engine `reply_received` P1 `:828`, imzadan enrich `:840+`.
- Sequences (multi-touch drip) tam bağlı: `migr 035`, `services/sequenceService.js`, `services/sequenceWorker.js` (60s poll, `server.js:121-123`), route `routes/sequences.js:80-313`.
- Unsubscribe: `migr 012`, `utils/unsubscribeHelper.js` (token/footer/RFC 8058 one-click), endpoint `webhooks.js:934,959`; resolve+sequence suppression listesine uyar.
- Per-user günlük limit: `campaigns.js:805-840` (start'ta), `users.daily_email_limit` `migr 032`.

**Eksik/zayıf:**
- **Marketing-vs-operational template flag YOK** — `email_templates` (migr 001) tür kolonsuz; footer/unsubscribe her gönderimde koşulsuz enjekte (`unsubscribeHelper.js:235-249`). Operasyonel mailler marketing footer'ından muaf olamıyor.
- **Worker-seviye günlük throttle YOK** — limit yalnız `/start` ve sequence-send'de; tek-campaign worker loop'u (`worker.js:142-315`) `daily_email_limit` kontrol etmiyor → `status='sending'` olunca tüm pending'i boşaltır.
- Reply yakalama harici Gmail filter + Inbound Parse setup'ına bağlı (`webhooks.js:877-924` yalnız talimat döner).
- A/B test yok; gönderim-saati/iş-saati penceresi yok (scheduler tek atış `campaignScheduler.js:9-15`).

---

## D. QUOTE — YOK (sıfırdan kurulacak)

**Gerçekten hiç iz yok — Suer haklı, eksiksiz doğrulandı.**
- Tek iz, stub'ı doğrulandı — `engines/action-engine/actionEngine.js:127-131`:
  `// T3: quote_no_response — Priority 2 (STUB) ... // TODO: Implement when quotes table is created (Blueprint Phase 1C)`
  ve `migr 037:20`'de CHECK constraint'te `'quote_no_response'` string literal'i (no-op).
- `quote|proforma|af_number|line_item|sku|catalogue` grep'inin **tüm** isabetleri false-positive (template parser "Quoted literal" `templateProcessor.js:78`, "quoted reply" `webhooks.js`/`signatureParser.js`, URL stopword `'products'` `companyResolver.js:20`, engagement keyword `'pricing'` `actionEngine.js:227`, contact CSV `scripts/Bengu_Quote.csv`).
- **Yeniden kullanılabilir altyapı SIFIR:** 46 migration'da 28 tablo var; quotes/products/pricing/line_items/currencies/invoices **yok**. Currency yönetimi yok (`currency/exchange_rate/eur_equiv` grep boş). AF-number/ISO-seq üreteci yok. Quote router yok, `server.js:66-96` mount listesinde yok.

**Sıfırdan gerekenler:** product/price catalog şeması; quotes + quote_line_items (line-level discount/tax); AF-number `Q{ISO}-{seq}` üreteci; subject auto-gen `{Expo}-{Company}-{M²}`; currency saklama+freeze+EUR-equivalent; CRUD+status (draft→sent→signed)+PDF; `checkQuoteNoResponse` bağlanması.

---

## E. KULLANICI / YETKİ / GÜVENLİK — BOZUK (freelancer senaryosu için)

**Çatı var, ama asıl tablolara uygulanmamış.**

**Çalışan kısım:**
- Auth gerçek: JWT login/register + bcrypt `routes/auth.js:42,117,151`; middleware `middleware/auth.js:25-77`.
- Roller: `['owner','admin','manager','sales_rep']` `userManagement.js:26` (+ legacy CHECK `migr 039:40-41`).
- **Hiyerarşik scope motoru doğru:** `getHierarchicalScope` recursive CTE `reports_to` (self+descendants) `middleware/userScope.js:122-141`; varyantlar `:160,:206,:242`.
- Scope GERÇEKTEN uygulanan endpoint'ler: campaigns `campaigns.js:124,53,436`; tasks/notes/activities `contactCrm.js:70,176,225,423,477`; mining jobs, sequences, intents `intents.js:79`, lists `lists.js:651`, templates/senders; pipeline stage WRITE `pipeline.js:337`.
- User management gated: create/update/reset `isPrivileged` `userManagement.js:32,65,137`; owner rolü yalnız owner verir `:89,:182`; son-owner koruması `:159-166`.

**🔴 BOZUK — cross-user veri sızıntısı (en kritik bulgu):**
Şu liste/detay endpoint'leri YALNIZCA `organizer_id` ile filtreliyor, kullanıcı scope'u YOK. Her authenticated satışçı/freelancer tüm şirketin verisini görüyor:
- **Contacts list `GET /api/persons`** — WHERE sadece `p.organizer_id=$1` `persons.js:33`. Ana "Contacts" ekranı. **SIZINTI.**
- **Contact detail/affiliations/campaigns + `DELETE /api/persons/:id`** `persons.js:475,552,446,589` — organizer-only. Freelancer her kişiyi **okuyup silebiliyor.** **SIZINTI + yıkıcı.**
- **Contacts export `GET /api/persons/export`** `persons.js:257` — tüm org'un kişilerini XLSX/CSV döker. **Toplu sızdırma.**
- **Leads `GET /api/leads`** `leads.js:35,47` — organizer-only (`prospects`'te owner kolonu yok). **SIZINTI.**
- **Prospects `GET /api/prospects`** `prospects.js:106,115` — organizer-only. **SIZINTI.**
- **Companies `GET /api/companies` + `/:name/contacts`** `companies.js:11,24,127` — başka rep'lerin müşteri firmalarını ve içindeki kişileri açar. **SIZINTI.**
- **Pipeline BOARD `GET /api/pipeline/board`** `pipeline.js:180,215` — `pipeline_assigned_user_id` okumada hiç kullanılmıyor; rep başkasının deal'ini taşıyamaz ama **tüm şirketin satış Kanban'ını görür.** **SIZINTI.**
- Not/görev write-target scope'suz: `verifyPersonAccess` yalnız `organizer_id` `contactCrm.js:25` → herhangi bir kişiye not/görev eklenebilir.

**Diğer güvenlik açıkları:**
- JWT fallback secret `liffy_secret_key_change_me` **~28 dosyada** hardcoded (`middleware/auth.js:23`, `routes/auth.js:8`...). `.env`'de `JWT_SECRET` set, yani prod şu an iyi — ama deploy'da set edilmezse sistem sessizce kaynak-kontrollü public secret'a düşer; **boot-time guard yok.**
- `permissions` JSONB kolonu **ölü** (migr 039:24) — hiçbir kod okumuyor/yazmıyor (grep boş). Vaat edilen `can_view_revenue`/`country_scope` granüler izinleri kodda yok.
- **Field-level gizleme yok** — telefon/email/herhangi alanı bir rep'ten gizleme mekanizması yok; endpoint başına ya hep ya hiç.
- İki paralel scope sistemi (legacy `team_ids/manager_id` migr 038 + ADR-015 `reports_to`) bir arada, ıraksak.
- (İyi haber: komisyon/gelir veri modeli hiç yok — sızacak komisyon alanı da yok; ama alan-seviye gizleme de yok.)

**Dürüst verdict:** "Satışçı yalnız kendi verisini görür" **bugün MÜMKÜN DEĞİL.** CRM objeleri (campaign/task/list/sequence/report) izolasyonu çalışıyor; ama asıl müşteri/lead envanteri (Contacts, Leads, Prospects, Companies, Pipeline board, export) **her satışçıya tüm şirketi gösteriyor ve sildirtebiliyor.** Güvenilmez freelancer = tam veri-sızdırma riski. Sistem yarı-dönüştürülmüş: çatı sağlam ama en değerli tablolara hiç uygulanmamış.

---

## F. FRONTEND (liffy-ui) — KISMI (kapsamda TAM'a yakın, güvenlikte zayıf)

**Sayfalar (hepsi `app/` altında, hepsi gerçek API çağırıyor — ~20 sayfa):**
`/` Action Center `page.tsx:99`, `/dashboard`, `/leads` (Contacts→`/api/persons` `:209`) + `/leads/[id]`, `/prospects`, `/pipeline` Kanban `:95`, `/campaigns` (+`[id]`, `/sequences`, `/unsubscribes`), `/tasks`, `/lists`(+`[id]`), `/templates`, `/companies`, `/reports`, `/verification`, `/waiting`, `/settings`, `/admin`, `/mining`(+jobs/new/[id]/results/console), `/source-discovery`(redirect), `/help`, `/login`. Server proxy `app/api/*`.

**Çalışan:**
- Tüm ana satış ekranları gerçek ve dolu (leads 860 satır, campaigns 746, pipeline 298, mining 2875); "coming soon" yok, tek mock mining console dev-fallback `console/page.tsx:82-83`.
- Login tam: `app/login/page.tsx:17`→proxy→backend `app/api/auth/login/route.ts:61`, `liffy_token` saklar `:50`.
- Auth header helper `lib/auth.ts:1-14`; sidebar rol gösterir + Admin linkini owner/admin/manager'a gate'ler `components/sidebar.tsx:432-434`.

**Eksik/bozuk:**
- **Route koruması yalnız client-side ve zayıf** — `components/layout-client.tsx:69-99` + `hooks/useAuthGuard.ts:16-28` sadece localStorage'da `liffy_token` string'i var mı ve base64 decode olur mu bakıyor; `/api/auth/me` doğrulaması YOK. Bozuk/expired ama düzgün-formatlı token guard'ı geçer; gerçek koruma tümüyle backend'in per-request JWT'sinde.
- Token localStorage'da (`lib/auth.ts:5`) — XSS'e açık; httpOnly cookie değil.
- Rol gating kozmetik — yalnız Admin nav linki gizli `sidebar.tsx:432`; bir sales_rep `/admin`'e doğrudan gidebilir, sayfa yüklenir, yalnız `/api/users` 403 dönünce patlar.
- **UI backend sızıntısını yansıtıyor:** `/leads`→scope'suz `/api/persons` `:209`, `/pipeline`→`/api/pipeline/board` `:95` → giriş yapan freelancer tüm rep'lerin müşterilerini/pipeline'ını görür (E'nin frontend tezahürü).
- Kozmetik: footer "© 2025", "All systems operational" statik; header Search + Notifications dekoratif; Profile/Settings dropdown handler'sız `layout-client.tsx:224,238,266-313`.

**Verdict:** Frontend sistemin en olgun parçası — geniş kapsam, gerçek endpoint, stub yok; günlük satış işine kullanılabilir. Ama kendi başına neredeyse sıfır güvenlik sağlıyor; koruma backend'e bağlı, backend de şu an aşırı-cömert.

---

## SATIŞA HAZIRLIK — ALAN BAZINDA EFOR SIRASI (en az → en çok)

| Sıra | Alan | Efor | Neden |
|---|---|---|---|
| 1 | **C. Campaign** | En az | TAM. Yalnız cila: op/marketing template flag + worker-seviye günlük throttle. |
| 2 | **E. Güvenlik sızıntısı** | Küçük-orta kod, ama **BLOKE EDİCİ** | ~8 endpoint'e scope uygula + `persons`/`prospects`'e owner kolonu ekle + JWT boot guard. **Freelancer kullanımından ÖNCE şart.** |
| 3 | **F. Frontend** | Orta | Kapsam hazır; auth sertleştirme (server-side session doğrulama, route guard) + E düzelince ekran zaten doğru veriyi gösterir. |
| 4 | **B. Lead Pipeline** | Orta | Manuel tek-lead create endpoint + disqualification taksonomisi + routing/round-robin + domain/company dedup. |
| 5 | **A. Mining** | Büyük | Productize: self-service tetikleme (geliştirici-CLI'yi kaldır), AGGREGATION_PERSIST'i aç, AI-miner runtime'ı aç, hardcoded token/job-id temizliği. |
| 6 | **D. Quote** | En çok | Sıfırdan komple modül: product/price catalog + quotes + line-items + AF-number + currency-freeze + status + PDF. |

> **Not:** Efor sırası ≠ öncelik sırası. **E (güvenlik) eforu küçük ama bloke edici** —
> güvenilmez freelancer'lar varken LIFFY mevcut haliyle satışa açılamaz. Bu yüzden
> efor olarak 2. ama yapılış önceliğinde 1. olmalı.

---

## EN BÜYÜK 3 RİSK / SÜRPRİZ

1. **🔴 CROSS-USER VERİ SIZINTISI — freelancer-güven gereksinimi bugün İMKANSIZ.**
   İzin "çatısı" var ama asıl müşteri tablolarına (persons/leads/prospects/companies/
   pipeline-board) hiç uygulanmamış: her satışçı tüm şirketin contact'larını **görüp
   dışa aktarabiliyor ve silebiliyor** (`persons.js:33,257,589`, `pipeline.js:215`). 28
   dosyadaki hardcoded JWT fallback secret bunu ağırlaştırıyor. En büyük blocker ve
   ciddi güvenlik açığı.

2. **🟠 MINING SELF-SERVICE DEĞİL — bir satış özelliği değil, geliştirici aracı.**
   Bloklanan her sitede sistem admin'e kopyala-yapıştır terminal komutu e-postalıyor
   (`worker.js:651`) ve bir insan Node+Playwright makinesinde elle çalıştırıyor. Üstelik
   madenlenen lead'ler varsayılan olarak contact tablolarına bile düşmüyor (shadow mode,
   `aggregationTrigger.js:34`). "Mining çalışmıyor/eksik" algısının kök nedeni: aslında
   hiç ürünleşmemiş.

3. **🟡 QUOTE MUTLAK SIFIR + yeniden kullanılabilir altyapı yok.**
   Yalnız quote tablosu değil; currency, ürün/fiyat kataloğu, sequence/AF-number üreteci —
   hiçbiri yok. Lead→quote→sign satış döngüsünün quote aşaması komple eksik; en ağır
   sıfırdan-yapım kalemi.

   **Bonus sürpriz (pozitif):** "LIFFY kullanılmıyor" algısına rağmen **Campaign katmanı
   sistemin en üretim-kalite parçası (TAM)** — ZeroBounce doğrulama, sequence drip, reply
   takibi, atomic çift-gönderim koruması dahil. Yani sorun "outreach motoru yok" değil;
   sorun onun etrafındaki güvenlik + quote + self-service mining eksikliği.

---

## METODOLOJİ & SINIRLAR
- 3 paralel ajan: (A+B), (C+D), (E+F). Her bulgu `dosya:satır`. node_modules taranmadı.
- Olgunluk: TAM/KISMI/İSKELET/BOZUK/YOK. "BOZUK" = kod var ve çalışıyor ama amaç için
  güvenli/doğru değil (E'deki sızıntı gibi).
- **Bulamadım:** web-form lead intake endpoint'i, manuel lead-create POST'u, office-scope,
  marketing/operational template flag, `http` mining stratejisi implementasyonu — hiçbiri yok.
- "Var" denen her şey kanıtlı; kanıtlanamayan "bulamadım" dendi. Hiçbir dosya değiştirilmedi.
