# ELIZA (eliza-legacy) Özellik Envanteri — 26 Eki 2026

SENTEZ → CC · salt okuma · Paket 6 girdisi (Paket 4'ü bloklamaz)

## Kapsam ve kanıt

- **Kaynak repo:** `~/Projects/eliza`, remote `Nsueray/eliza`, `main` @ `cdd8a26`. AD-01'e göre eliza-legacy bu repodur (`ELL_LOCKED_KARARLAR_OZET.md:220`).
- **LEENA klonu:** `~/Desktop/Leena_Projesi/Leena_v401_monorepo` @ `0c90d0d` (26 Eki). Beklenen yol olan `~/Projects/Leena_v401_monorepo` yok.
- **Yöntem:** Yalnız dosya okundu (cat/grep/sed/Read). Hiçbir servis, DB, Zoho, Twilio veya Render çağrısı yapılmadı. `.env` okunmadı.
- **Kişisel veri:** Kişi ve firma adları yerine `<temsilci>`, `<firma>`, `<fuar>` yazıldı. Numara, e-posta ve token yazılmadı.
- **Yol kökleri:**
  - ELIZA yolları `~/Projects/eliza/` köküne göredir.
  - LEENA yolları `backend/leena-v401-backend/` köküne göredir (`LEENA:` önekiyle).
  - `ENV-22` ve `ENV-23`, LEENA'daki `docs/audits/SAYFA_ENVANTERI_2026-10-22.md` ve `…-23.md` belgeleridir.
- **Satır numaraları** yukarıdaki HEAD'lere göredir.
- **Başlangıçtaki `git status --short`** (bu çalışmadan önce de vardı; dokunulmadı):
  - eliza: ` M packages/db/migrations/021_core_countries.sql` · `?? ELIZA_CURRENT_STATE.md`
  - ell-docs: ` M leena/CLAUDE.md` · ` M leena/todo.md`

---

## 0. Ölçüm

### 0.1 Repo yapısı (üst 2 seviye, `node_modules` hariç)

```
eliza/
├─ apps/
│  ├─ api/            Express API — 16 route dosyası, 74 uç
│  ├─ dashboard/      Next.js (pages router) — 16 sayfa
│  └─ whatsapp-bot/   Twilio webhook botu — server.js · auth.js · handler.js
├─ packages/
│  ├─ ai/             queryEngine · router · conversationMemory · personalityEngine · riskEngine · expoMetrics · benchmark
│  ├─ alerts/ · attention/ · briefing/ · messages/ · push/ · targets/
│  ├─ db/             index.js (pg havuzu) · schema.sql · migrations 004–026
│  └─ zoho-sync/      zohoAuth · syncExpos · syncSalesOrders · scheduler
├─ docs/              architecture · benchmark · decisions · foundation + 14 md
├─ CLAUDE.md · ELIZA_CURRENT_STATE.md (izlenmiyor) · package.json (npm workspaces)
└─ .env (VAR, okunmadı) · .env.example
```

Toplam yaklaşık 20 bin satır JS var. Bot çekirdeği: `handler.js` 1034, `router.js` 750, `queryEngine.js` 2234 satır.

### 0.2 Servisler

| servis | klasör | dil / çatı | giriş | not |
|---|---|---|---|---|
| api | `apps/api` | Node.js · Express · pg · jsonwebtoken (HS256) · bcrypt · node-cron · @anthropic-ai/sdk | `src/server.js` | Zoho ve push zamanlayıcılarını da başlatır (`server.js:84-104`) |
| bot | `apps/whatsapp-bot` | Node.js · Express · twilio | `src/server.js` | API'yi çağırmaz; `packages/*` üzerinden DB'ye doğrudan bağlanır (`handler.js:3-9`) |
| dashboard | `apps/dashboard` | Next.js (pages) · React · chart.js / react-chartjs-2 · jspdf (+autotable) · xlsx | `pages/` | JWT localStorage'da durur; tüm API çağrılarına token ekleyen fetch sarmalayıcısı var (`lib/api.js:8-55`) |

### 0.3 Ortam anahtarları (yalnız ad, değer okunmadı)

- **Kodda okunanlar:**
  - Altyapı: `DATABASE_URL` · `PORT` · `WHATSAPP_BOT_PORT` · `JWT_SECRET` · `CORS_ORIGINS` · `NEXT_PUBLIC_API_URL`
  - Zoho: `ZOHO_CLIENT_ID` · `ZOHO_CLIENT_SECRET` · `ZOHO_REFRESH_TOKEN`
  - Twilio: `TWILIO_ACCOUNT_SID` · `TWILIO_AUTH_TOKEN` · `TWILIO_WHATSAPP_FROM` · `CEO_WHATSAPP_NUMBER` (`packages/briefing/index.js:109`)
  - Model: `AI_INTENT_MODEL` · `AI_ANSWER_MODEL`
- **SDK'nın kendisi okuyor:** `ANTHROPIC_API_KEY` (`new Anthropic()`, `packages/ai/queryEngine.js:8`, `conversationMemory.js:6`).
- **Yalnız `.env.example`'da, kodda kullanılmıyor:** `OPENAI_API_KEY` · `AI_MODEL` · `NODE_ENV`.
- **Render'daki değerler:** ölçülmedi.

### 0.4 Klonlar

- **ell-docs:** VAR (`~/Projects/ell-docs`). Rapor bu repoya yazıldı.
- **LEENA:** `~/Projects` altında YOK.
  - Kullanılan klon: `~/Desktop/Leena_Projesi/Leena_v401_monorepo` (en güncel; 26 Eki).
  - Kullanılmayan eski kopyalar: `~/Documents/GitHub/…` (2025-08-19) ve `~/Desktop/proje-ozetleri/…` (2026-04-07).

---

## 1. BOT

### 1a. Motor: kalıp + LLM (ikisi birlikte; önce kalıp)

| # | adım | dosya:satır | tür |
|---|---|---|---|
| 1 | Twilio imza doğrulaması; geçmezse 403 | `apps/whatsapp-bot/src/server.js:25-36` | kural |
| 2 | Numara → kullanıcı (`users.whatsapp_phone`); pasif kullanıcı reddedilir | `src/auth.js:16-36` | kural + DB |
| 3 | Bekleyen netleştirmeyi iptal; CEO'nun "gönder/iptal" komutu | `handler.js:236-274` | kalıp |
| 4 | Nokta komutları | `handler.js:276-292`, `:752-860` | kalıp |
| 5 | Netleştirme cevabını çözme (numara ya da metin) | `handler.js:296-492` | kalıp |
| 6 | Öz-referans: "ben/benim/bana" → kullanıcının temsilci adı | `handler.js:497-510` | regex |
| 7 | Takip sorusunu bağımsız soruya çevirme (son 5 mesaj / 2 saat; kalıp ön-kontrolü `ALWAYS_INDEPENDENT`) | `packages/ai/conversationMemory.js:105-110`, `:136-196`, `:147-164` | **LLM (Haiku)** |
| 8 | Kapsam dışı ret (kur, maaş, genel bilgi) | `queryEngine.js:74-126` | kelime listesi |
| 9 | Niyet: `route()` — 23 kural, öncelik sıralı, ilk eşleşen kazanır, 0 API çağrısı | `router.js:160-596` | **kalıp** |
| 10 | Kural eşleşmezse semantik çerçeve çıkarımı | `queryEngine.js:283-403` (prompt), `:420-541` | **LLM (Haiku)** |
| 11 | Netleştirme kapısı (öncelik: yıl > fuar > metrik) | `queryEngine.js:1874-2045` | kural + DB |
| 12 | Varsayılan yıl | `queryEngine.js:2054-2077` | kural |
| 13 | Serbest SQL — yalnız CEO, `general_stats` + boş varlık durumunda | `queryEngine.js:2120-2148`, `:1663-1720` | **LLM (Sonnet)** |
| 14 | Şablon SQL → kapsam filtresi → doğrulama → pg | `buildQuery :544-1402` · `applyScope :1422-1485` · `validateSQL :1488-1507` | kural |
| 15 | Cevap: 6 niyette deterministik metin; diğerlerinde Sonnet (2-3 cümle) | `queryEngine.js:1513-1608` · `:1611-1660` | kural / **LLM (Sonnet)** |
| 16 | Panel linki, kişilik (selam/kapanış), `message_logs` kaydı | `handler.js:129-224` · `:112-123` · `:14-45` | kural |

- **Sağlayıcı:** Anthropic (`@anthropic-ai/sdk`). OpenAI kodda yok.
- **Anahtar adı:** `ANTHROPIC_API_KEY` (SDK varsayılanı).
- **Model seçimi:**
  - `AI_INTENT_MODEL`: niyet çıkarımı ve soru yeniden yazımı.
  - `AI_ANSWER_MODEL`: cevap ve SQL üretimi.
  - Kod varsayılanları Haiku 4.5 ve Sonnet 4.6 (`queryEngine.js:9-10`).
- **Soru başına LLM çağrısı:** En az 0 (kural eşleşir, cevap deterministik çıkar). En çok 4: yeniden yazım + çerçeve + SQL + cevap.

### 1b. Anladığı soru türleri

**Durum sütunu yalnız koddan okundu; hiçbir şey çalıştırılmadı.**
- **ÇALIŞIR:** Şablon ve parametreler tutarlı.
- **KIRIK:** Koddan bir hata ya da yanlış sonuç görülüyor.
- **BELİRSİZ:** Koddan karar verilemiyor.

**Veri kaynakları:**
- `edition_contracts` = durum Valid ya da Transferred In.
- `fiscal_contracts` = durum Valid ya da Transferred Out.
- `outstanding_balances` = açık bakiye görünümü.
- İkisi de `packages/db/migrations/025_missing_views.sql:10`, `:29`, `015_simplify_collection_stages.sql:5`.

| # | niyet | örnek soru (kişisiz) | veri (ayna tablosu · alan) | kural `router.js` | şablon `queryEngine.js` | durum |
|---|---|---|---|---|---|---|
| 1 | expo_progress | "<fuar> 2026 kaç m² satıldı?" | expos (name, start_date, target_m2) + edition_contracts (m2, revenue_eur) | `:322` | `:601` | ÇALIŞIR |
| 2 | target_progress | "<fuar> hedefi ne durumda?" | expos + expo_targets (target_m2, target_revenue, source) + edition_contracts | `:306` | `:548` | ÇALIŞIR |
| 3 | agent_performance | "<temsilci> bu yıl kaç sözleşme yapmış?" | fiscal_contracts (sales_agent, m2, revenue_eur, contract_date) | `:346` | `:618` | ÇALIŞIR |
| 4 | agent_country_breakdown | "<temsilci> hangi ülkelerden müşteri bulmuş?" | fiscal_contracts.country | `:410` | `:682` | ÇALIŞIR |
| 5 | agent_expo_breakdown | "<temsilci> hangi fuarlara satmış?" | fiscal_contracts + expos | `:421` | `:698` | ÇALIŞIR |
| 6 | expo_agent_breakdown | "<fuar>'da en çok kim satmış?" | edition_contracts + expos | `:364` | `:983` | ÇALIŞIR (yıl/metrik netleştirmesi sorabilir; `:1748` önce tahminle çözmeyi dener) |
| 7 | expo_company_list | "<fuar> 2026 firma listesi" | edition_contracts (company_name, country, m2, revenue_eur) | `:530` | `:1000` | ÇALIŞIR |
| 8 | country_count | "<fuar>'da kaç ülke var?" | edition_contracts.country | `:443` | `:716` | ÇALIŞIR |
| 9 | exhibitors_by_country | "<ülke>'den kaç firma katılıyor?" | edition_contracts + expos | `:431` | `:731` | ÇALIŞIR (yalnız ileri tarihli fuarlar, `:740`, `:751`) |
| 10 | top_agents | "en iyi satışçı kim?" | fiscal_contracts | `:390` | `:758` | ÇALIŞIR |
| 11 | revenue_summary | "bu hafta kaç sözleşme geldi?" · "toplam gelir" | edition_contracts (contract_date, m2, revenue_eur) | `:473` | `:806` | ÇALIŞIR |
| 12 | contract_list | "bu hafta gelen sözleşmeleri listele" | edition_contracts (company_name, m2, revenue_eur, contract_date, af_number) + expos | `:456` | `:897` | **KIRIK** (bkz. 1b-2) |
| 13 | monthly_trend | "bu yıl ay ay satışlar" | fiscal_contracts | `:377` | `:1018` | ÇALIŞIR |
| 14 | cluster_performance | "<şehir> cluster toplamı" | expos.country ILIKE cluster adı + edition_year + edition_contracts | **kural yok** (yalnız Haiku) | `:1050` | BELİRSİZ (`expo_clusters` tablosunu kullanmıyor; şehir adını country alanında arıyor, `:1060`) |
| 15 | collection_summary | "kaç alacağımız var?" | outstanding_balances (balance_eur, paid_eur, collection_stage) | `:179` | `:1080` | ÇALIŞIR |
| 16 | collection_no_payment | "hiç ödeme yapmayan firmalar" | outstanding_balances | `:196` | `:1096` | ÇALIŞIR |
| 17 | collection_expo | "<fuar> tahsilat durumu" | outstanding_balances | `:237` | `:1134` | ÇALIŞIR |
| 18 | company_collection | "<firma> firmasının borcu ne kadar?" | outstanding_balances | `:219` | `:1328` | ÇALIŞIR |
| 19 | payment_status | "ödemesi geciken firmalar" | edition_contracts.revenue_eur — ödeme verisi **değil** | `:248` | `:1177` | BELİRSİZ (`:1176` TODO; ödeme/bakiye alanı kullanmıyor, sözleşme tutarını listeliyor) |
| 20 | rebooking_rate | "<fuar>'a tekrar katılan firmalar" | contracts (status) + expos.edition_year | `:266` | `:1209` | ÇALIŞIR |
| 21 | price_per_m2 | "<fuar> ortalama m² fiyatı" | edition_contracts revenue_eur / m2 | `:283` | `:1259` | ÇALIŞIR |
| 22 | days_to_event | "<fuar>'a kaç gün kaldı?" | expos.start_date | `:162` | `:1305` | ÇALIŞIR |
| 23 | company_search | "<firma> şirketi hakkında" | edition_contracts | `:545` | `:1377` | **KIRIK** (filtre `company_name` yerine `expo_name‖agent_name` okuyor, `:1386`. Kural `company_name` çıkarıyor (`router.js:716`) ama şablon kullanmıyor; sonuç `'%%'` olur ve genel ilk 20 firma döner) |
| 24 | expo_list | "hangi fuarlar risk altında?" · "2026 fuarları" | expo_metrics (risk) / expos + edition_contracts | `:555` | `:946` | ÇALIŞIR |
| 25 | general_stats | "genel durum nedir?" | edition_contracts (yıllık toplamlar) | (yedek) | `:1389` | ÇALIŞIR |
| M1 | hybrid_sql | sınıflanamayan herhangi bir soru (yalnız CEO) | Sonnet'in ürettiği SELECT (izin verilen tablo listesi `:12`) | — | `:2128` | ÇALIŞIR (cevap kalitesi BELİRSİZ; bkz. §6-1) |
| M2 | compound | "<temsilci A> ve <temsilci B> kaç satmış?" | alt sorulara bölme | — | `:2080` | BELİRSİZ (çerçeve çıktı şemasında `sub_questions` yok (`:332-350`) ama kod onu okuyor (`:518`); bölme gerçekleşmez, `general_stats` şablonuna düşer (`:1390`)) |
| M3 | clarification | yıl / fuar / metrik / bağlam sorusu | users.pending_clarification (10 dk) | — | `:1934-2045` · `handler.js:296-492`, `:585-678` | ÇALIŞIR |
| M4 | unavailable | "1 euro kaç TL?" | — | — | `:74-126`, `:1835` | ÇALIŞIR |

**Komutlar** (`handler.js:752-860`):

| komut | ne yapar | veri | durum |
|---|---|---|---|
| `.brief` | Sabah brifingi üretir. Önce risk metriklerini, dikkat taramasını ve uyarıları yeniden hesaplar (yazar) | `packages/briefing/index.js:24-28` → expo_metrics, attention_log, alerts, edition_contracts | ÇALIŞIR |
| `.risk [<fuar>]` | Soruyu "risk durumu" sorusuna çevirip motora verir | expo_metrics | ÇALIŞIR (`:766-772`) |
| `.attention` | Dikkat gerektiren ilk 5 konu | attention_log (`packages/attention/index.js:61`) | ÇALIŞIR |
| `.msg <kişi> <konu>` | 4 şablon × 3 dilde mesaj taslağı | message_drafts, sales_agents_legacy (`packages/messages/index.js:113`) | ÇALIŞIR (izin: `can_use_message_generator`) |
| `gönder` / `iptal` | Taslağı onaylayıp Twilio ile gönderir ya da düşürür (yalnız CEO) | message_drafts | ÇALIŞIR (`:250-274`, `:864-885`) |
| `.help` | Komut listesi | — | ÇALIŞIR |
| `.note` · `.today` · `.expense` | Yalnız "henüz aktif değil" der | — | YOK (`:790-803`) |

#### 1b-2. Suer'in bildirdiği üç soru

**"bu ay kaç sözleşme" → çalıştı.**
- `normalize`, "bu ay" ifadesini "this month" yapar (`router.js:20-27`, `:37-39`). "this month + sözleşme" çiftini yakalayan bir kural yok, bu yüzden soru Haiku'ya gider.
- Haiku hangi niyeti döndürse de ay bilgisi geliyor. Ay varsa `run()` yılı doldurur (`queryEngine.js:2059-2061`), dolayısıyla aşağıdaki hata tetiklenmez.

**"<temsilci>'nin 2026 sözleşmeleri" → çalıştı.**
- Yıl açıkça verildiği için `e.year` dolu. Haiku `contract_list` ya da `agent_performance` döndürse de hata yolu kısa devre olur.

**"en son hangi sözleşme" → hata verdi. Muhtemel neden: `packages/ai/queryEngine.js:923`.**
1. `normalize` sonrası soru "en son hangi sozlesme" olur. 23 kuralın hiçbiri eşleşmez:
   - `contract_list` "liste/list" ister (`router.js:458-469`).
   - `expo_list` "en son fuar" ister (`:569`).
   - `revenue_summary` zaman kelimesi ister (`:484-511`).
   - Sonuç: `route()` null döner (`:595`).
2. Soru Haiku çerçevesine gider (`queryEngine.js:437`). Prompt'ta "en son/latest" örneği yok; tek sözleşme listeleme niyeti `contract_list` (`:319`).
3. `contract_list` ve zamansız bir çerçeve dönerse yıl varsayılanı bu niyeti kapsamaz:
   - Varsayılan yalnız şu durumlarda uygulanır: ay varsa, `EXPO_INTENTS_NEED_YEAR`, `AGENT_INTENTS_NEED_YEAR` (`:2057-2077`).
   - Bu yüzden `entities.year` boş kalır.
4. `buildQuery('contract_list')` dönem dalına girmez ve `else` dalına düşer (`:921-926`). Orada `const yr = e.year || currentYear;` çalışır (`:923`).
5. `currentYear` yalnız `run()` içinde `const` olarak tanımlı (`:1846`). `buildQuery` (`:544`) ayrı bir üst düzey fonksiyondur. Modülde ya da global'de başka `currentYear` yok (grep: yalnız `queryEngine.js:1846` ve `handler.js:600`, ikisi de yerel).
   - Sonuç: `ReferenceError: currentYear is not defined`.
6. Hata `run()` dışına fırlar ve `handler.js:728-746` içinde yakalanır.
   - Kullanıcı şu cevabı görür: "Sorgu işlenirken hata oluştu. Lütfen tekrar deneyin."
   - Hata metni `message_logs.error`'a yazılır (`handler.js:730-739`).
7. Satır `f230c60` commit'iyle girdi (2026-03-27, "weekly contract mismatch … contract listing").

**Alternatif yol:** Haiku `general_stats` döndürür ve varlık boşsa, CEO için serbest SQL yoluna girilir. Bu yol hata mesajı üretmez; hata olursa şablona düşer (`:2145-2157`). Haiku'nun gerçekte ne döndürdüğü **ölçülmedi**.

**Çalıştırmadan doğrulama (Suer):** `/admin/logs` → Status: error. İlgili kartın hata alanında `currentYear is not defined` görünmeli. Panel bu filtreyi `message_logs.error` üzerinden uyguluyor (`apps/api/src/routes/logs.js:29-30`).

**Bağlantılı ikinci kusur:** `contract_list` ay filtresi uygulamıyor.
- Yalnız `period === 'this_month'` dalı var (`:915`). Oysa kural da Haiku da ayı `entities.month` olarak veriyor (`router.js:619-621`, `queryEngine.js:492-494`).
- Sonuç: "bu ay sözleşmeleri listele" ayın değil yılın listesini döndürür.
- Hata giderilirse "en son" sorusu kendiliğinden doğru cevaplanır, çünkü liste `ORDER BY c.contract_date DESC` sıralı (`:940`).

### 1c. Cevap biçimi, yetki, dil

- **Biçim:**
  - Düz metin, TwiML içinde (`server.js:80-91`); 4000 karakterde kesilir (`:82-84`).
  - Tablo ya da dosya YOK. Metin ya deterministik şablondan (`queryEngine.js:1513-1608`; örn. "1. <temsilci> — €… m² (N kontrat)") ya da Sonnet'ten gelir. `handler.js:985-1032`'deki satır biçimlendirici (`rowToLine`/`formatDataLines`) tanımlı ama hiçbir yerde çağrılmıyor.
  - 5'ten fazla satırda "… ve N sonuç daha" ile panel linki eklenir; azsa yalnız link (`handler.js:690-706`).
  - Kişilik katmanı: takma adla selam ve kapanış (`handler.js:112-123`, `packages/ai/personalityEngine.js:93-128`).
- **Yetki:**
  - 1. katman: Twilio imzası (`server.js:25-36`).
  - 2. katman: numara listesi VAR, ama DB'de (`users.whatsapp_phone`, `auth.js:16-27`); kodda numara yok. Kayıtlı numara sayısı **ölçülmedi**.
  - Roller ceo / manager / agent. `data_scope` (all / team / own) ve `visible_years` SQL'e enjekte edilir (`queryEngine.js:1422-1485`).
  - Serbest SQL yalnız `data_scope=all` için açık (`:2128`).
  - "gönder/iptal" yalnız CEO (`handler.js:250`). `.msg`, `.note` ve `.expense` izin bayrağına bağlı (`:792-806`).
- **Dil:** TR / EN / FR kelime skoruyla otomatik algılanır; varsayılan TR (`handler.js:88-107`). Cevap sorunun dilinde verilir (`queryEngine.js:1638`).

---

## 2. DASHBOARD VE RAPORLAR

### 2.1 Sayfalar

**Ortak noktalar:**
- Tüm sayfalar JWT ister.
- Sayfa izinleri istemci tarafında uygulanır (`pages/_app.js:13-28`, `components/Nav.js:6-33`).
- Yollar `apps/dashboard/pages/` köküne göredir.
- "Dışa aktarım": C = Copy (panoya), CSV, X = Excel, P = PDF.

| # | yol · ad | ne gösteriyor | API uçları (dosya:satır) | ayna tablosu · alan | filtreler | dışa aktarım | grafik | yazma |
|---|---|---|---|---|---|---|---|---|
| D01 | `/` · War Room | Edition / fiscal KPI, Expo Radar, risk radarı, satış sıralaması, AI sohbet kutusu | `index.js:139-143` (revenue/summary, revenue/edition-summary, expos/metrics, expos/risk, sales/leaderboard) · `:104` POST ai/query | fiscal_contracts · edition_contracts · expos · expo_metrics | mode edition/fiscal · upcoming/tüm yıl | YOK | Bar (`:1000`) | YOK (POST yalnız soru gönderir) |
| D02 | `/expos` · Expo Directory | Fuar listesi: tarih, m², gelir, sözleşme, risk | `expos.js:52-53` | expos · edition_contracts · expo_metrics | `?year ?expo ?country ?agent` + metin + sıralama | C · CSV · X · P (`:120-160`) | YOK | YOK |
| D03 | `/expos/detail` · Expo Detail | Özet kartlar; temsilci, firma, ülke dağılımı; aylık satış | `expos/detail.js:72-76` | expos · edition_contracts · expo_metrics | `?name ?year` · firma araması · grafik metriği | C · CSV · X (3 sayfa) · P (`:215-264`) | Bar (`:704`) | YOK |
| D04 | `/sales` · Fiscal Sales | Dönem KPI'ları ve değişim %; temsilci / fuar / ülke tabloları; trend | `sales.js:93-97` (fiscal/summary, by-agent, by-expo, by-country, trend) | fiscal_contracts · expos | dönem: bugün/hafta/ay/yıl/özel aralık · temsilci | C · CSV · X · P (`:246-295`) | Bar (`:702`) | YOK |
| D05 | `/finance` · Collections Cockpit | 8 KPI; aksiyon listesi; aging; yaklaşan tahsilat; 8 haftalık tahmin; fuar ve temsilci bazında açık bakiye; son ödemeler; firma çekmecesi | `finance.js:89-96`, `:182` (9 finance ucu) | outstanding_balances · contracts · contract_payments · contract_payment_schedule · expos · sales_agents | mode · stage · risk · arama · 7/14/30/60 gün | C · CSV · X (`:198-225`); PDF yok | Bar (aging, `:620`) | YOK |
| D06 | `/targets` · Target Tracker | Hedef vs gerçekleşen (m² ve €), cluster grupları, önceki edisyon | `targets.js:127`, `:164`, `:140` PUT, `:195` POST seed | expos · expo_targets · expo_clusters · contracts | mode · yıl | C · CSV · X (`:229-294`) | SVG halka (`:58`) | **VAR** (hedef düzenleme, otomatik hedef üretme) |
| D07 | `/admin` · `/admin/users/new` · `/admin/users/[id]` · Kullanıcılar | Kullanıcı listesi ve formu: rol, kapsam, panel izinleri, WhatsApp numarası, takma ad, push ayarları, şifre, test push | `admin/index.js:27-43` · `users/new.js:68`, `:103` · `users/[id].js:176-292` | users · user_permissions | — | YOK | YOK | **VAR** (POST/PUT/DELETE users, set-password) |
| D08 | `/admin/logs` · Logs | Bot mesaj kartları; özet KPI; router/Haiku dağılımı; günlük grafik | `admin/logs.js:468`, `:492` | message_logs | kullanıcı · niyet · durum · tarih aralığı · sekme | C (kart, `:47`) | Doughnut + Bar (`:151`, `:228`) | YOK |
| D09 | `/admin/intelligence` · Intelligence | Router kuralları, niyet istatistikleri, benchmark, netleştirme istatistikleri | `admin/intelligence.js:70-73` | message_logs (+ router.js, docs/benchmark) | — | YOK | YOK | YOK |
| D10 | `/admin/system` · System | Servis sağlığı, DB tabloları, sync özeti ve logu, manuel sync | `admin/system.js:94`, `:102-103`, `:139` POST sync-now | pg_stat_user_tables · sync_log · message_logs · users | otomatik yenileme | C · CSV · X (`:152-159`) | YOK | **VAR** (Zoho sync tetikler → contracts/expos yazılır) |
| D11 | `/admin/reference` · Reference | Ülke / sektör / para birimi / dil düzenleme | `admin/reference.js:57-60`, `:78` PUT | core_countries · core_sectors · core_currencies · core_languages | sekme | YOK | YOK | **VAR** |
| D12 | `/login` · `/settings` · `/unauthorized` | Giriş; profil, tema, yoğunluk; şifre değiştirme; erişim reddi | `lib/auth.js:33`, `:53`, `:95` · `settings.js:56` | users | `?return` | YOK | YOK | **VAR** (last_login, settings, password_hash) |

- **Sayfa sayısı:** 16 (`pages/api/hello.js` Next.js şablon kalıntısı; sayılmadı).
- **Grafik:** 6 sayfada var.
- **Dışa aktarım:** 6 sayfada var. PDF yalnız D02, D03 ve D04'te.
- **Yazma:** 6 sayfa yazıyor (D06, D07 ×3, D10, D11, D12 settings).

### 2.2 API uçları

Toplam **74** uç (`apps/api/src/routes/*.js`, + `/health`). Dosya başına sayı:
- 1: ai, sales
- 2: attention, logs
- 3: alerts, messages
- 4: intelligence, revenue
- 5: fiscal, system, targets
- 6: auth
- 7: users
- 8: reference
- 9: expos, finance

**Panelin çağırmadığı uçlar:**
- `alerts/*` (3), `attention/*` (2), `messages/*` (3)
- `revenue/by-country`, `revenue/by-year`
- `expos/:id`, `expos/calculate-targets` (expos.target_m2'yi yazar, `expos.js:60-104`)
- `targets/clusters`
- `system/push-status`
- `auth/set-password`, `auth/init-password`

Bu uçları başka bir istemcinin kullanıp kullanmadığı ölçülmedi.

### 2.3 Zamanlanmış işler

| iş | dosya:satır | sıklık | ne yapar | nerede başlar |
|---|---|---|---|---|
| Zoho ilk çekim | `packages/zoho-sync/scheduler.js:87` | API her açıldığında 1 kez | Önce fuarlar, sonra sözleşmeler (aşağıdaki modüller) | `apps/api/src/server.js:85-88` (`ZOHO_CLIENT_ID` + `ZOHO_REFRESH_TOKEN` varsa) |
| Zoho liste çekimi | `scheduler.js:94` (`0 * * * *`) | saatlik | **Vendors** → expos (`syncExpos.js:5`, `:84-86`) · **Sales_Orders** → contracts (`syncSalesOrders.js:5`, upsert `:248-284`). Liste yanıtında `Received_Payment` gelirse contract_payments yazılır; her sözleşme için sentetik %30/%70 ödeme planı (`:286` sonrası, plan çağrısı `:303`). Adı "incremental" ama her seferinde tüm sayfaları çekiyor (`:13`, `syncExpos.js:13`; modified_since yok) | aynı |
| Zoho ödeme çekimi | `scheduler.js:102` (`0 6,18 * * *`) | günde 2 | `paid_eur > 0` olan sözleşmeler için tek tek `Sales_Orders/{id}` çağrılır; `Received_Payment` → contract_payments (`syncSalesOrders.js:330-370`) | aynı |
| Push mesajları | `packages/push/scheduler.js:51` (`*/5 * * * *`) | 5 dakikada bir kontrol | 5 tip, kullanıcının saat dilimine göre; push_log ile tekilleştirme (`push/index.js:4-9`, `:141`) | `apps/api/src/server.js:97-100` |
| CEO sabah brifingi | `packages/briefing/scheduler.js:6-52` | 05:00 UTC (setTimeout) | `sendBriefing` → `CEO_WHATSAPP_NUMBER`'a gönderim | **Hiçbir servis başlatmıyor** (grep: yalnız kendi dosyası; kök `package.json`'da script yok). Render'da ayrı worker olup olmadığı ölçülmedi |
| Talep üzerine yeniden hesaplama | `apps/api/src/routes/expos.js:8` | her `GET /api/expos/risk` çağrısında | riskEngine → expo_metrics yazılır | API |

- **Çekilen Zoho modülleri:** yalnız `Sales_Orders` ve `Vendors`.
- **Çekilmeyenler:** `Expensess`, `Sales_Agents`, `Accounts` — zoho-sync'te çağrı yok. CLAUDE.md §13 bunları "primary" olarak listeliyor.
- **Cron saat dilimi:** sunucu TZ'si; ölçülmedi.

### 2.4 Raporlar (gönderilen)

| # | rapor | dosya:satır | içerik (özet) | kanal |
|---|---|---|---|---|
| R01a | morning_brief (08:00) | `push/index.js:180` | Dünkü satışlar, ödemeler, açık bakiye, 120 gün içindeki fuarların hedef ilerlemesi, yaklaşan tahsilatlar | WhatsApp (Twilio) |
| R01b | midday_pulse (13:00) | `:349` | Günün ilerlemesi (sözleşme, ödeme) | WhatsApp |
| R01c | daily_wrap (16:00) | `:426` | Gün özeti + yarın beklenen ödemeler | WhatsApp |
| R01d | weekly_report (Pazartesi 08:00) | `:528` | Hafta özeti | WhatsApp |
| R01e | weekly_close (Cuma 16:00) | `:626` | Hafta kapanışı + gelecek hafta | WhatsApp |
| R02 | CEO brifingi + uyarılar | `briefing/index.js:24-147` · `alerts/index.js:69-249` | 5 uyarı tipi: risk_high, payment_watch, attention_gap, velocity_drop, rebooking_gap + dikkat taraması | WhatsApp (`.brief` ya da zamanlayıcı) |

**Ortak özellikler:**
- Kişi başı ayarlar ve kapsam: all / team / own (`push/index.js:156-178`).
- Dil: TR / EN / FR.

**Sayılar:**
- 6 rapor: 5 push tipi + 1 CEO brifingi.
- 5 uyarı tipi brifingin içinde.
- Dışa aktarımlı rapor ekranı 6: D02–D06, D10.

### 2.5 Ayna şeması (tablo + alan sayısı; içerik okunmadı)

**Yöntem:**
- Sayılar `schema.sql` ile 004–026 migration'larındaki `CREATE TABLE` ve `ADD COLUMN` satırlarından hesaplandı.
- `010_reconcile_drift.sql` var; canlı DB ile fark olabilir — **ölçülmedi**.
- Görünümler: `edition_contracts`, `fiscal_contracts` (`025_missing_views.sql:10`, `:29`) ve `outstanding_balances` (son tanım `015_simplify_collection_stages.sql:5`).

| grup | tablo · alan sayısı | beslenme |
|---|---|---|
| Zoho aynası | contracts 32 · contract_payments 9 · contract_payment_schedule 11 · expos 11 | Zoho sync (schedule sentetik; expos.target_m2 ve cluster_id ELIZA'da üretiliyor) |
| Ajan | sales_agents_legacy 6 · sales_agents 10 | legacy: 109 satır (`026_…sql:4`); yeni UUID tablo boş, Slice 3'te dolacak (`026:5`, `:32`) |
| ELIZA üretimi | expo_targets 10 · expo_clusters 7 · expo_metrics 21 · attention_log 11 · alerts 12 · sent_briefings 5 | targets, riskEngine, attention, alerts |
| Bot / kullanıcı | users 22 · user_permissions 11 · message_logs 18 · message_drafts 14 · push_log 10 · sync_log 9 | bot, panel, zamanlayıcılar |
| ELL referans (sahip: ELIZA) | core_countries 9 · core_sectors 11 · core_currencies 6 · core_languages 6 | migration seed + `/admin/reference` |
| Kodda kullanılmayan | exhibitors 4 · expenses 7 · whatsapp_messages 5 | apps/packages'ta okuma/yazma yok (grep 0) |

**Toplam:** 25 tablo + 3 görünüm.

---

## 3. LEENA KARŞILIĞI

**Kaynaklar:**
- `ENV-22`, `ENV-23` ve LEENA ui2'deki 22 HTML sayfası.
- Ayrıntılı eşleme bir alt ajanla yapıldı. Temel iddiaları kendim grep ile doğruladım:
  - ui2'de dışa aktarım ve grafik 0.
  - routes/utils'de anthropic/openai 0.
  - leaderboard 0.
  - `LEENA:routes/contracts.js:315-322` yalnız `expo_id` ve `status` filtresi alıyor.

**Lejant:**
- VAR = eşdeğer var.
- KISMEN = bir kısmı var.
- YOK = yok.
- TAŞINACAK = LEENA belgelerinde planlı.

**Genel not:** LEENA'da bot / doğal dil / LLM yok (routes ve utils içinde anthropic/openai araması 0). Bu yüzden B-satırlarındaki karşılık, aynı soruyu cevaplayan bir ekran olup olmadığına göre verildi.

| ID | özellik | LEENA | beslendiği LEENA verisi | not (kanıt) |
|---|---|---|---|---|
| B01 | Fuar ilerlemesi (m², gelir, sözleşme) | YOK | contracts (sqm, revenue_eur) · expos | sqm API'de var, UI'da gösterilmiyor (`LEENA:routes/contracts.js:329`). Bütçe ekranında yalnız tahsil edilen gelir (`LEENA:public/ui2/finance-budget.html:98`) |
| B02 | Hedef ilerlemesi | KISMEN | expos · payments (+ expo_budgets, listede yok) | Fuar gelir hedefi vs tahsil (`finance-budget.html:74-75`, `:97-99`). m² hedefi yok |
| B03 | Temsilci performansı | YOK | contracts · sales_agents · commission_payouts | En yakın karşılık temsilci başı komisyon toplamı (`LEENA:routes/commissions.js:81`) |
| B04 | Temsilci ülke / fuar kırılımı | YOK | contracts · sales_agents · expos | — |
| B05 | Fuarda temsilci sıralaması | YOK | contracts · sales_agents | — |
| B06 | Fuar firma listesi | KISMEN | contracts · expos | Liste var (`finance-contracts.html:54`). API `expo_id` kabul ediyor ama UI'da filtre yok |
| B07 | Ülke sayısı / ülkeden firmalar | YOK | contracts | LEENA contracts'ta ülke alanı ölçülmedi |
| B08 | En iyi satışçılar | YOK | contracts · sales_agents | leaderboard 0 |
| B09 | Dönem satış özeti | YOK | contracts | fiscal 0 |
| B10 | Sözleşme listesi | KISMEN | contracts · contract_line_items · payments | `finance-contracts.html:54`. Tarih / temsilci / ülke filtresi yok (`ENV-23:103`) |
| B11 | Aylık trend | YOK | contracts | — |
| B12 | Cluster performansı | YOK | expos | — |
| B13 | Tahsilat soruları (özet, ödemesiz, fuar, firma borcu) | KISMEN | payments · contracts · ledger | Açık alacak (`finance-summary.html:35`, `LEENA:routes/ledger.js:983-990`). Sözleşme başı bakiye (`finance-contracts.html:45-46`). Aging kovası yok; yalnız overdue/upcoming (`LEENA:routes/cashForecast.js:24-26`) |
| B14 | Ödeme durumu | KISMEN | payments | Ödemeler okunuyor (`finance-contract.html:54-61`); yazma yalnız eski `public/contract-detail.html:208-216` |
| B15 | Tekrar katılım | YOK | contracts · expos | — |
| B16 | m² fiyatı | YOK | contracts (sqm, revenue_eur) | — |
| B17 | Fuara kalan gün | KISMEN | expos | Tarihli fuar listesi var (`admin-liffy-expos.html:35-46`); kalan gün hesabı yok |
| B18 | Firma arama | YOK | contracts | Sözleşme listesinde arama yok |
| B19 | Fuar listesi / risk listesi | KISMEN | expos | Liste var; risk / hız yok |
| B20 | Genel istatistik + serbest SQL | YOK | — | LLM yok |
| B21 | Bileşik soru | YOK | — | — |
| B22 | Netleştirme + konuşma hafızası + kapsam dışı ret | YOK | — | — |
| B23 | `.brief` / `.risk` / `.attention` | YOK | — | briefing / alert araması 0 |
| B24 | `.msg` mesaj taslağı + gönder | YOK | sales_agents | — |
| B25 | `.note` / `.today` / `.expense` (çalışmayan komutlar) | KISMEN | expenses | Gider girişi ui2'de var (`finance-expenses.html`, `finance-drafts.html`; `LEENA:routes/expenseDrafts.js:3`, `:31` AI'yı taslak yazarı olarak öngörüyor) |
| D01 | War Room | KISMEN | ledger · payments · commission_payouts · contracts | `finance-summary.html:65`: nakit, açık alacak, ödenecek komisyon. Satış KPI'ları, sıralama ve risk yok |
| D02 | Expo Directory | KISMEN | expos | `admin-liffy-expos.html`: ad / tarih / yer. m², gelir ve sözleşme yok |
| D03 | Expo Detail | YOK | contracts · expos · payments | Bütçe ekranı kısmen yakın |
| D04 | Fiscal Sales | YOK | contracts · sales_agents | — |
| D05 | Collections Cockpit | KISMEN | payments · ledger · contracts | summary, contracts, contract, cash-forecast var. Aksiyon listesi, aging kovaları ve dışa aktarım yok. LEENA'da ödeme **gerçek kayıt**; ELIZA'nın planı sentetik |
| D06 | Targets | KISMEN | expos · payments (+ expo_budgets) | Yalnız fuar gelir hedefi. m² hedefi, cluster ve otomatik hedef yok |
| D07 | Kullanıcı yönetimi | VAR | users (+ roles, permissions) · sales_agents | `admin-users.html`, `admin-user.html:69-95`: rol / yetki matrisi, davet, audit. WhatsApp numarası, takma ad ve push ayarı alanı **yok** |
| D08 | Bot logları | YOK | — | audit_log var (`LEENA:utils/audit.js:17`); bot / mesaj logu yok |
| D09 | Intelligence | YOK | — | — |
| D10 | System / Sync | YOK | — | Zamanlanmış çekim yok |
| D11 | Referans veri | VAR | core_countries · core_sectors (+ currencies, kategoriler) | `LEENA:routes/reference.js:13`, `:29`; `routes/ledger.js:116-214`. core_* sahibi ELIZA (ELIZA `CLAUDE.md` §7: "ELIZA writes, LiFTY/LEENA read only"); aynı DB'yi mi okuduğu ölçülmedi |
| D12 | Login / Settings | VAR | users | `ui2/login.html`, `whoami.html`. Tema / yoğunluk ayarı ölçülmedi |
| D13 | Dışa aktarım (Copy / CSV / Excel / PDF) | YOK | — | ui2 ve eski finans sayfalarında 0. Excel yalnız EMS ziyaretçi tarafında (`LEENA:routes/visitors.js:1180`) |
| R01 | Push mesajları (5 tip) | YOK | — | Tek zamanlanmış rapor EMS callcenter günlük e-postası (`LEENA:email_worker.js:911`) |
| R02 | CEO brifingi + uyarılar | YOK | — | — |
| R03 | Zoho ayna senkronu | TAŞINACAK | contracts · contract_line_items · payments · expos · expenses · sales_agents | Paket 4 = tek seferlik göç + fark senkronu (`ELL_DURUM_DEFTERI_v2.md:5153-5157`). Bugün yalnız elle salt-okunur çekim var (`LEENA:scripts/zoho/pull.js:3-6`) |
| R04 | Risk motoru (hız, risk skoru) | YOK | contracts · expos | m²/satılan % yalnız floorplan'da (`LEENA:public/floorplan/stands.js:265`); sözleşmeye bağlı değil |
| R05 | Otomatik hedef + cluster tespiti | YOK | expos | — |

**LEENA'da planlı ama bitmemiş, ilgili kalemler:**
- ui2 sözleşme listesi kısmi (`ENV-23:103`).
- ui2 sözleşme detayı kısmi (`ENV-23:102`).
- Commissions ve Agents yalnız klasik sayfaya köprü; ui2 ekranı "UI-1 adayı" (`ENV-23:28`, `:189-191`).
- Klasik ekranların ui2'ye taşınması "KAPSAM DIŞI" (`ENV-23:311`).

---

## 4. SUER ŞABLONU (Suer doldurur)

Öncelik: 1 = vazgeçilmez · 2 = olsa iyi · 3 = gerekmez.

| ID | özellik | beğendim | neden / nasıl kullanıyorum | öncelik (1-3) |
|---|---|---|---|---|
| B01 | Bot: fuar ilerlemesi | ☐ | | |
| B02 | Bot: hedef ilerlemesi | ☐ | | |
| B03 | Bot: temsilci performansı | ☐ | | |
| B04 | Bot: temsilci ülke / fuar kırılımı | ☐ | | |
| B05 | Bot: fuarda temsilci sıralaması | ☐ | | |
| B06 | Bot: fuar firma listesi | ☐ | | |
| B07 | Bot: ülke sayısı / ülkeden firmalar | ☐ | | |
| B08 | Bot: en iyi satışçılar | ☐ | | |
| B09 | Bot: dönem satış özeti ("bu ay kaç sözleşme") | ☐ | | |
| B10 | Bot: sözleşme listesi ("en son hangi sözleşme") | ☐ | | |
| B11 | Bot: aylık trend | ☐ | | |
| B12 | Bot: cluster performansı | ☐ | | |
| B13 | Bot: tahsilat soruları | ☐ | | |
| B14 | Bot: ödeme durumu | ☐ | | |
| B15 | Bot: tekrar katılım | ☐ | | |
| B16 | Bot: m² fiyatı | ☐ | | |
| B17 | Bot: fuara kalan gün | ☐ | | |
| B18 | Bot: firma arama | ☐ | | |
| B19 | Bot: fuar listesi / risk listesi | ☐ | | |
| B20 | Bot: genel istatistik + serbest soru | ☐ | | |
| B21 | Bot: bileşik soru | ☐ | | |
| B22 | Bot: netleştirme + takip sorusu hafızası | ☐ | | |
| B23 | Bot: `.brief` / `.risk` / `.attention` | ☐ | | |
| B24 | Bot: `.msg` mesaj taslağı + gönder | ☐ | | |
| B25 | Bot: `.note` / `.today` / `.expense` | ☐ | | |
| D01 | Panel: War Room | ☐ | | |
| D02 | Panel: Expo Directory | ☐ | | |
| D03 | Panel: Expo Detail | ☐ | | |
| D04 | Panel: Fiscal Sales | ☐ | | |
| D05 | Panel: Finance / Collections Cockpit | ☐ | | |
| D06 | Panel: Targets | ☐ | | |
| D07 | Panel: kullanıcı yönetimi | ☐ | | |
| D08 | Panel: bot logları | ☐ | | |
| D09 | Panel: Intelligence | ☐ | | |
| D10 | Panel: System / Sync | ☐ | | |
| D11 | Panel: referans veri | ☐ | | |
| D12 | Panel: login / settings | ☐ | | |
| D13 | Panel: dışa aktarım (CSV / Excel / PDF) | ☐ | | |
| R01 | Push mesajları (5 tip) | ☐ | | |
| R02 | CEO brifingi + uyarılar | ☐ | | |
| R03 | Zoho ayna senkronu | ☐ | | |
| R04 | Risk motoru | ☐ | | |
| R05 | Otomatik hedef + cluster | ☐ | | |

---

## 5. ÖNERİ (Paket 6 girdisi)

**Ölçüt:** Defterdeki kapanış şartı "kapatma Paket 6'da, yeni sistem aynı cevapları verince" (`ELL_DURUM_DEFTERI_v2.md:5161-5163`).

**Kategoriler:**
- **KALSIN:** Geçiş süresince ELIZA'da kalır; LEENA'da karşılığı planlanmamış ya da ELIZA'ya bağlı.
- **TAŞI:** LEENA'ya taşınır; "P6" = kapanış ölçütü için gerekli.
- **SİL:** Taşınmaz.

Bu tabloda paket atanmadı; P6 dışı bir paket uygunsa onu Sentez atar.

| ID | öneri | gerekçe (1 satır) |
|---|---|---|
| B01–B11 | KALSIN | Bot kanalı LEENA'da yok; defter "WhatsApp botu KALIR" diyor (`ELL_DURUM_DEFTERI_v2.md:3121`). Verisi D-satırlarıyla taşınır |
| B10 | KALSIN (+ düzeltme) | "En son" hatası `queryEngine.js:923`'teki tek satır. P6'ya kadar bot canlı olduğundan beklemesi gerekmez (karar Sentez'in) |
| B12 | SİL | `expo_clusters` tablosunu kullanmıyor; cluster görünümü zaten D06'da var |
| B13 | KALSIN | En çok kullanılabilir finans sorusu; LEENA'da yalnız ekran karşılığı var |
| B14 | SİL | Ödeme verisi değil sözleşme tutarı döndürüyor; işi B13 gerçek ödeme verisiyle yapıyor |
| B15–B17 | KALSIN | Bot kanalı |
| B18 | KALSIN (+ düzeltme) | Filtre yanlış alanı okuyor (`queryEngine.js:1386`); B13'teki firma borcu sorusu çalışıyor |
| B19–B20 | KALSIN | Bot kanalı; serbest SQL yalnız CEO |
| B21 | SİL | Çerçeve şemasında `sub_questions` yok; bölme pratikte çalışmıyor |
| B22 | KALSIN | Botun kullanılabilirliği buna bağlı |
| B23–B24 | KALSIN | WhatsApp'a özgü; LEENA'da karşılığı yok |
| B25 | SİL | Çalışmıyor; gider girişi LEENA ui2'de var |
| D01 | TAŞI (P6) | Yönetici özeti; LEENA'da finans var, satış KPI'ları ve sıralama yok |
| D02 | TAŞI (P6) | Fuar başına m², gelir ve sözleşme sayısı LEENA'da yok |
| D03 | TAŞI (P6) | Fuar detayı (temsilci, firma, ülke, aylık) LEENA'da yok |
| D04 | TAŞI (P6) | Dönem satış raporu ve sıralama LEENA'da yok (fiscal ve leaderboard 0) |
| D05 | TAŞI (P6) | Aging kovaları, aksiyon listesi ve dışa aktarım eksik; LEENA'nın gerçek ödeme verisiyle daha doğru olur |
| D06 | TAŞI (P6) | m² hedefi ve cluster LEENA'da yok; yalnız gelir hedefi var |
| D07 | KALSIN | Bot kullanıcıları (numara, takma ad, push) yalnız burada yönetiliyor; bot kapanınca SİL |
| D08 | KALSIN | Bot logu; bot kalırken gerekli |
| D09 | KALSIN | Bot hata ayıklama ekranı; bot kapanınca SİL |
| D10 | KALSIN | Zoho aynası P6'ya kadar canlı; sync izlemesi yalnız burada |
| D11 | TAŞI (P6) | core_* sahibi ELIZA; sahiplik devredilmeden ELIZA kapanamaz |
| D12 | SİL | LEENA'da giriş ve oturum var; panel kapanınca düşer |
| D13 | TAŞI (P6) | LEENA finansında dışa aktarım 0; Suer'in rapor alışkanlığı buna bağlı olabilir |
| R01 | KALSIN | WhatsApp push; LEENA'da bildirim altyapısı yok |
| R02 | KALSIN | `.brief` çalışıyor. Zamanlayıcı dosyası hiçbir yerde başlamıyor; işi R01 morning_brief yapıyor |
| R03 | KALSIN | Zoho P6'ya kadar kanonik; Paket 4 göçü bunun yerini tutmuyor (tek seferlik + fark senkronu) |
| R04 | KALSIN | Bot ve War Room risk paneli buna bağlı; taşıma kararı D01 ile birlikte verilmeli |
| R05 | TAŞI (P6) | D06'nın veri üreticisi |

**Toplamlar:**
- **Bot:** 25 soru türü. Ayrıca 4 meta yol (serbest SQL, bileşik, netleştirme, kapsam dışı), 6 komut ve 3 çalışmayan komut var.
  - Durum: 21 ÇALIŞIR · 2 KIRIK (`contract_list`, `company_search`) · 2 BELİRSİZ.
- **Panel:** 16 sayfa (13 özellik satırı) · 74 API ucu.
- **Rapor:** 6 (5 push + 1 CEO brifingi) + 5 uyarı tipi.
- **Zamanlanmış iş:** 5. Dördü çalışıyor; CEO brifingi zamanlayıcısı başlatılmıyor.
- **Ayna:** 25 tablo + 3 görünüm.
- **Özellik satırı:** 43 → **KALSIN 29 · TAŞI 9 · SİL 5**.

---

## 6. Yan bulgular (envanter dışı; hiçbir şey düzeltilmedi)

1. **Serbest SQL doğrulaması zayıf.**
   - `validateSQL` tablo listesini (`queryEngine.js:12`) uygulamıyor.
   - Yasak kelime kontrolü, SELECT ile başlayan sorguda etkisiz: `upper.replace(/^SELECT[\s\S]*$/, '')` metnin tamamını siliyor (`:1497`).
   - Yol yalnız CEO'ya açık (`:2128`).
   - SQL üretim prompt'u şemada `users` tablosunu da gösteriyor (`:1671`).
2. **`POST /api/ai/query` kullanıcıyı motora geçirmiyor** (`apps/api/src/routes/ai.js:13`).
   - Kapsam filtresi uygulanmıyor (`queryEngine.js:1423`); serbest SQL yolu da açık (`:2128`, `!user`).
   - Sonuç: giriş yapmış her panel kullanıcısı (agent dahil) tüm veriyi sorgulayabilir.
3. **API'de rol kontrolü yalnız `/auth/set-password`'de var** (`apps/api/src/routes/auth.js:218`).
   - `users` POST/PUT/DELETE, `reference` PUT, `system/sync-now`, `targets` PUT ve seed uçları JWT'si olan herkese açık.
   - Panel izinleri yalnız istemci tarafında uygulanıyor.
4. **CLAUDE.md'de hassas satırlar.**
   - `CLAUDE.md:640` düz metin başlangıç CEO parolası içeriyor (değer yazılmadı).
   - `CLAUDE.md:880` repoyu "public" olarak tanımlıyor; GitHub görünürlüğü ölçülmedi.
   - Dosyada kişi adları da var.
5. **Zoho senkron kusurları.**
   - `syncExpos` `ON CONFLICT DO NOTHING` kullanıyor (`syncExpos.js:86`): Zoho'da değişen fuar tarihi ve ülkesi aynaya yansımaz.
   - İlk ham Zoho kaydı loga basılıyor (`syncExpos.js:57-58`).
6. **Okuma ucu yazıyor:** `GET /api/expos/risk` her çağrıda expo_metrics'i yeniden yazıyor (`expos.js:8`).
7. **`.msg` cevabı alıcının telefon numarasını gösteriyor** (`handler.js:822`).

## 7. Ölçülmedi / açık

**Ölçülmedi:**
- Haiku'nun "en son hangi sözleşme" sorusuna ne döndürdüğü (1b-2, A/B yolu).
- Canlı DB satır sayıları, kolon farkı ve kayıtlı bot numarası sayısı.
- Render'da çalışan servis ve worker listesi; cron saat dilimi.
- Bot kullanım sıklığı (`message_logs`): en çok hangi soruların sorulduğu.
- LEENA `core_*` tablolarının ELIZA DB'si mi, kendi DB'si mi olduğu.

**Açık sorular:**
1. `/admin/logs` hata kartında `currentYear is not defined` görünüyor mu (doğrulama)? Düzeltme P6'yı beklesin mi?
2. CEO brifingi zamanlayıcısı (`packages/briefing/scheduler.js`) Render'da ayrı bir worker olarak çalışıyor mu? Kodda hiçbir servis onu başlatmıyor.
3. `core_*` referans tablolarının sahipliği P6'da LEENA'ya mı geçecek?

## 8. Bitiş durumu

`git status --short` sonu (başlangıçla aynı; tek fark yeni rapor dosyası):

- eliza: ` M packages/db/migrations/021_core_countries.sql` · `?? ELIZA_CURRENT_STATE.md`
- ell-docs: ` M leena/CLAUDE.md` · ` M leena/todo.md` · `?? docs/audits/` (yalnız bu rapor)
- LEENA klonu: yalnız okundu. Başlangıçta durum çıktısının yalnız ilk 5 satırı kaydedildiği için tam karşılaştırma yapılamadı; sonda 34 satır (önceden var olan değişiklikler).

Commit ve push yapılmadı (Suer).
