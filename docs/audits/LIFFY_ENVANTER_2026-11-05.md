# LIFFY ENVANTERİ — 2026-11-05 (Prompt 1 · B1 ölçümü, salt okuma)

> **Ne:** ADR-023 (LIFFY satış çekirdeğinin LEENA'ya birleşmesi) için LIFFY'nin tablo / rota / ekran / servis envanteri ve
> canlı DB sayımları. **Salt okuma:** kod `liffyv1` `10047ee` + `liffy-ui` `b78231b` (origin ile eşit, `git fetch` ölçüldü);
> canlı DB yalnız SELECT (`BEGIN READ ONLY` + `default_transaction_read_only = on` görüldü · DB adı kapısı `liffy` geçti ·
> PostgreSQL 17.9). **Kişisel veri YOK** — yalnız sayı / durum / rol / ofis kodu. Bağlantı dizesi panodan okundu, basılmadı,
> pano boşaltıldı (K4). Bu belge tarihseldir (YON-01): yazıldığı günün ölçümüdür.
>
> **Sınıf sözlüğü:** `satış çekirdeği` (teklif, kalem, katalog, fiyat, kur, fuar senkronu, convert outbox) · `madencilik-kampanya`
> (madencilik, benzer kaynak, kampanya, sequence, prospect/list, doğrulama, CRM notları) · `ortak` (kullanıcı, auth, organizer,
> ofis, kişi/şirket görünümü) · `altyapı`.
> **B1 hükmü (ADR-023):** satış çekirdeği LEENA'ya taşınır; madencilik-kampanya + 80K kişi BU ADIMDA TAŞINMAZ, LIFFY'de durur;
> köprü kesime kadar durur.

## 1. Tablolar — 36 canlı (migration'lar 37 yaratır, 1 düşürür)

Canlı DB sayımı: `pg_tables` public **36** (migration listesiyle aynı; `email_logs` 027'de düşürüldü). Dizi: `quote_af_seq`.
LIFFY'de migration koşucusu ve `schema_migrations` YOK (053:8, 054:13-14); 005 ve 020 numaraları ikişer kez kullanılmış.

| tablo | sınıf | satır (canlı) | LEENA karşılığı (B1) |
|---|---|---:|---|
| quotes | satış çekirdeği | 3 | `quotes` — **B1b** (Prompt 1b) |
| quote_line_items | satış çekirdeği | 4 | `quote_line_items` — **B1b** |
| products | satış çekirdeği | 228 (aktif 226) | `products` — **B1-a VAR** (055; tohum 227 — JSON, test ürünü hariç) |
| product_prices | satış çekirdeği | 205 | `product_prices` — **B1-a VAR** (056: 204 — DZ fiyatı atlandı) |
| exchange_rates | satış çekirdeği | 1 | yok — LEENA'da kur girişte donar (RAP-01; teklif para birimi fiyat listesinden) |
| expos | satış çekirdeği (köprü kopyası) | 2 (kaynak leena, aktif) | LEENA `expos` kanoniktir (KAT-03) — kopya gerekmez |
| offices | ortak | 7 (CN · DZ · GH · KE · MA · NG · TR) | LEENA `offices` (TR · MA · NG · KE · CN; DZ/IQ yok — OFS-07) |
| users | ortak | 3 (owner · manager · sales_rep; hepsi aktif, ofissiz) | LEENA `users` (Paket 2) |
| organizers | ortak | 1 | LEENA `organizers` |
| persons | ortak / madencilik | 80.855 (son 90 gün 0; madencilikten 201) | **TAŞINMAZ** (80K kişi verisi) — LEENA `contacts` B1-a VAR (boş başlar) |
| affiliations | ortak / madencilik | 90.841 | TAŞINMAZ (teklif şirket otomatik tamamlaması buradan) |
| companies | madencilik (kullanılmıyor) | 0 | LEENA `companies` B1-a VAR (yeni kayıt) |
| prospects · lists · list_members | madencilik-kampanya | 26.123 · 22 · 31.473 | taşınmaz |
| campaigns · campaign_recipients · campaign_events | madencilik-kampanya | 24 · 17.939 · 42.275 | taşınmaz |
| campaign_sequences · sequence_recipients | madencilik-kampanya | 6 · 1.885 | taşınmaz |
| email_templates · sender_identities · unsubscribes | madencilik-kampanya | 34 · 6 · 56 | taşınmaz |
| mining_jobs · mining_results · mining_job_logs · generated_miners | madencilik-kampanya | 113 · 65.065 · 0 · 8 | taşınmaz |
| verification_queue | madencilik-kampanya | 16.122 | taşınmaz |
| prospect_intents · discovery_searches · action_items | madencilik-kampanya | 455 · 4 · 1.761 | taşınmaz |
| contact_notes · contact_activities · contact_tasks · pipeline_stages | madencilik-kampanya (CRM) | 2 · 32 · 1 · 7 | taşınmaz (takip = kapsam dışı, B1) |
| zoho_push_log | madencilik-kampanya | 0 | taşınmaz |

## 2. Rotalar — 34 dosya (`backend/routes/`, hepsi `server.js:80-117`'de bağlı)

| sınıf | dosyalar |
|---|---|
| **satış çekirdeği** | `quotes.js` (`/api/quotes`, 31 uç: me / ofisler / kullanıcı-ofis · kurlar · fuarlar + Sync · ürünler / fiyatlar · teklif CRUD · kalemler · send / decline / sign / convert-resend) |
| ortak | `auth.js` · `userManagement.js` (`/api/users`) · `companies.js` (affiliations'tan şirket görünümü — teklif otomatik tamamlaması) · `persons.js` (kişi seçici) |
| madencilik-kampanya | actions · adminAIMiner · campaignRecipients · campaignSend · campaigns · contactCrm · context · emailLogs · emailTemplates · intents · leads · lists · miningJobs · miningResults · pipeline · prospects · reports · senders · sequences · settings · sourceDiscovery · stats · testEmail · timeline · unsubscribes · verification · waiting · webhooks · zoho |
| altyapı | `GET /api/health` (server.js:68-77) · 404 (server.js:120-122) |

Bağlı olmayan 4 yedek dosya (`*.backup`, `*.save`) dizinde duruyor.

## 3. Ekranlar — 31 sayfa (`liffy-ui/app/**/page.tsx`)

| sınıf | sayfalar |
|---|---|
| **satış çekirdeği** | `/quotes` (liste + form + send / decline / sign / resend) · `/quotes/catalog` (Products & Pricing: ürün, fiyat, fuar + Sync, kur, kullanıcı → ofis) |
| ortak | `/admin` · `/login` · `/help` |
| madencilik-kampanya | `/` (Action Screen) · `/dashboard` · `/campaigns` (+ `[id]`, sequences, unsubscribes) · `/companies` · `/leads` (+ `[id]`) · `/lists` (+ `[id]`) · `/mining` (+ jobs, new, `[id]`, console, results) · `/source-discovery` · `/pipeline` · `/prospects` · `/reports` · `/settings` · `/tasks` · `/templates` · `/verification` · `/waiting` |

Teklif sayfaları API'ye UI rewrite'ı ile gider (`API_REWRITE_URL`, `next.config.ts:6,12-13`).

## 4. Hangi süreç ne koşturuyor

- **`liffy-worker-docker`:** `Dockerfile:34` `CMD ["node", "backend/worker.js"]` — madencilik işleri (5 sn), kampanya zamanlayıcı (10 sn),
  kampanya gönderici (3 sn), ZeroBounce doğrulama kuyruğu (15 sn), SuperMiner. Tamamı **madencilik-kampanya**.
- **`liffy-api` (server.js) içinde ayrıca:** **convert outbox** (60 sn; `DISABLE_CONVERT_OUTBOX` ile kapanır — **satış çekirdeği / köprü**) ·
  sequence worker (60 sn) · action worker (15 dk) — ikisi madencilik-kampanya.
- **`liffy-redis`:** yalnız madencilik yolu (SuperMiner eventBus / ara depolama / HTML önbelleği; Redis yoksa geri düşer).

## 5. Dış servisler (yalnız ad)

- **SendGrid:** kampanya / sequence / test e-postası / gelen e-posta (Inbound Parse) / olay webhook'u — tamamı madencilik-kampanya.
  **Teklif gönderimi SendGrid KULLANMIYOR** (`routes/quotes.js` `sendEmail`'i içe alır ama çağırmaz — §7). Paket notu: `@sendgrid/mail`
  `package.json`'da yok, git'e alınmış `backend/node_modules` içinde.
- **ZeroBounce:** e-posta doğrulama kuyruğu (madencilik-kampanya).
- **Redis (ioredis):** §4. Kuyruk kütüphanesi (BullMQ vb.) BULAMADIM — kuyruklar DB-yoklamalı.
- Diğer: Anthropic (yapay zeka madenci üretimi, kaynak keşfi) · Zoho CRM itme — madencilik-kampanya.

## 6. Kullanıcılar (canlı)

3 kullanıcı: owner 1 · manager 1 · sales_rep 1 — hepsi aktif, **hiçbirine ofis atanmamış**. Organizer 1.

## 7. Son 90 gün (canlı, `created_at`)

- **Teklif:** 1 (signed). Tüm zaman: 3 — sent 1 (outbox yok) · signed + acked 1 · signed + outbox boş 1.
- **Kampanya:** 0. **Madencilik koşusu:** 0 (üretilen kişi 0). **Yeni kişi:** 0.

## 8. Teklif numarası + AF

- Dizi `quote_af_seq` START 100000, kiracılar arası TEK sayaç (051:23-26); `quotes.af_sequence` UNIQUE. Görünen numara SAKLANMAZ:
  `Q` (draft / sent / declined) ya da `A` (signed) + ofis ISO kodu + `-` + dizi — örn. `QTR-100000` → imzada `ATR-100000`
  (`routes/quotes.js:26-30`); LEENA'ya giden AF her zaman `A…` (`services/convertOutbox.js:66`). Sıfır dolgu yok.
- **Canlı:** dizi `last_value` **100002** · teklif `af_sequence` 100000–100002.
- B1b önerisi (ADR-023 + prompt §4.3): LEENA dizisi **200000**'den başlar (LIFFY aralığıyla çakışmaz); kesimde LEENA dizisi LIFFY'nin
  son numarasının üstüne alınır.

## 9. Send / Sign akışı (kod)

- **Durumlar:** `draft | sent | signed | declined` (`chk_quotes_status`); "süresi geçmiş" saklanmaz (`status='sent' AND valid_until < bugün`).
- **Send** (`quotes.js:1021-1047`): yalnız `draft → sent` + `sent_at`. **E-posta YOK, PDF YOK, bağlantı YOK.** Gönderimden sonra konu,
  şirket, fuar ve kalemler kilitlenir (not, geçerlilik, kişi, sahip, ofis düzenlenebilir — ofis değişince numara öneki değişir).
- **Sign** (`quotes.js:1086-1139`): `sent → signed` (TERMİNAL); `signed_at` zorunlu; tarama bağlantısı isteğe bağlı (harf/rakam yoksa NULL);
  imza commit'lenir, sonra convert outbox kuyruğa alınır (`enqueueAndSend`) — convert başarısızsa imza geri alınmaz.
- **Outbox** (`quotes` kolonları, ayrı tablo yok): `convert_status` NULL / pending / sent / acked / failed · 5 deneme, 1-2-4-8 dk ·
  "sent" 5 dk'dan eskiyse pending'e döner · Resend yalnız failed / pending. Sınıflama: 201 → acked · 409 `ALREADY_CONVERTED` → acked ·
  ≥ 500 / ağ / `SERVICE_AUTH_STALE` / `SERVICE_REPLAY` → yeniden dene · diğer 4xx (400 / 422 / 409) → failed (`convert_error` = kod + mesaj).
  İstek öncesi yerel retler: `NOT_FOUND` · `NOT_SIGNED` · `NO_EXPO` · `NO_LINE_ITEMS`.
- **LEENA sebep kodları:** `ALREADY_CONVERTED` açık işlenir · `EXPO_NOT_PUBLISHED` genel 4xx yoluna düşer · **`OFFICE_UNKNOWN`
  liffyv1 / liffy-ui'de BULAMADIM** (LEENA tarafında var) · `NO_PRICE` LIFFY'nin kendi 400'üdür (teklif / kalem yaratırken).
- **Toplamlar:** `utils/quoteTotals.js` — net = round2(q×p×(1−d)) · vergi = round2(net×t) · brüt = round2(net+vergi) · başlık toplamları
  bir kez yuvarlanır (TAH-05; ortak fikstür `tests/fixtures/p3_convert_vectors.json`). UI aynası `liffy-ui/lib/quoteTotals.ts`.
- **Müşteri modeli:** teklif şirketi SERBEST METİN (`quotes.company_name`; `companies` FK'si 052'de düştü) · kişi isteğe bağlı
  `person_id` (e-posta teklifte saklanmaz) · convert yükü `company_name` + satış sahibi e-postasını taşır, kişi taşımaz.

## 10. Katalog tohumu (B1-a girdisi)

`liffyv1/backend/seeds/products_zoho_2026-10-25.json` (format `liffy-products-seed/1`; LIFFY `scripts/zoho/build_products_seed.js`):
**227 ürün · 205 fiyat (188 varsayılan + 17 ofis: DZ 1 · KE 7 · MA 3 · NG 2 · TR 4) · 23 fiyatsız · RF 4 · 0 fiyatlı satır 30 · pasif 2 ·
para birimi yalnız EUR**. LIFFY canlıda 228 ürün = tohum + KAT-01 test ürünü. LEENA 056 bu JSON'dan üretildi (`scripts/catalog/build_seed_sql.js`);
DZ ofis fiyatı LEENA'da DZ ofisi olmadığından ATLANDI (OFS-07) → LEENA'da 204 fiyat · 24 fiyatsız.

## 11. Köprü — kesime kadar DURUR

- LIFFY → LEENA imzalı çağrılar (`services/leenaClient.js`, imza v2): `GET /api/expos` (fuar senkronu) · `POST /api/contracts/convert` (outbox).
- LEENA → LIFFY gelen çağrı: BULAMADIM.
- LEENA tarafı: HMAC servis kimliği (KAT-05) · `convert_requests` (KAT-04) · `expos.published_to_liffy` yayını (KAT-03).
- Hepsi kesime kadar çalışır; kesimde sökülür (ADR-023). Bu belge kodda "kesim" sözcüğü bulmadı — işaret ADR'dendir.
