# ELL — Yol Haritası v5 (Kanıta Dayalı, Tam Sürüm)

**Tarih:** 2026-06-19 (v5 — mimari karar değişikliği)
**Sahip:** Suer Ay
**Statü:** 🟢 **CANONICAL** — ELL için tek doğru kaynak. **v4'ün yerini alır.**

> ## 🔴 2026-06-19 — MİMARİ KARAR DEĞİŞİKLİĞİ (HER ŞEYDEN ÖNCE OKU)
>
> **ELIZA ayrı sistem olarak terk edildi.** Eski ELIZA backend/database artık gelecek
> sistemin parçası değildir; Zoho'dan sync edilmiş **disposable mirror + raporlama
> prototipidir**. Eski ELIZA verisi LEENA'ya migrate edilmeyecek.
>
> **Yeni aktif mimari:**
> - **LIFFY** = dış halka / satış workspace / freelancer izolasyonu. Ayrı DB ve ayrı servis kalır.
> - **LEENA** = iç halka / operations + finance + contracts + payments + commissions + ledger + reporting.
> - **ELIZA** = kullanıcıya görünen ürün / Finance tab / brand adı; fiziksel backend veya ayrı DB **DEĞİL**.
> - **Tek gerçek cross-DB sınır: LIFFY ↔ LEENA.**
> - Contract, payment, commission, ledger, sales agent, expo finance **LEENA DB'de** kurulur.
> - Final gerçek veri göçü ileride **doğrudan Zoho → LEENA** yapılır; eski ELIZA mirror'dan migration yapılmaz.
>
> *(Bu blok belgenin geri kalanından önceliklidir. Aşağıda eski 3-DB / ELIZA-hedefli ifadeler
> bu karara göre düzeltilmiştir; çelişki görürsen bu blok kazanır.)*

> ### ⚠️ Belge statüsü ve isimlendirme (ÖNEMLİ — karışıklığı önler)
>
> **Bu belge CANONICAL'dır.** Bir çelişki olduğunda bu belge kazanır. ELL'i tarif eden
> tek pusula budur. Bir Claude'a, ChatGPT'ye veya Claude Code'a ELL hakkında soru
> sorulurken referans bu belgedir.
>
> **`ELL_ARCHITECTURE_v1_0_CONSOLIDATED.md` artık canonical DEĞİLDİR — tarihsel taslaktır.**
> O dokümandaki mekanizma önerileri (RS256/JWKS asimetrik imzalama, key-rotation state
> machine, token-family + reuse-detection, saga, scope_version/permission_version/
> auth_version üçlü senkronizasyonu) **bilinçli olarak terk edilmiştir** — 25 kullanıcılı,
> tek-tenant, 2-deployment'lı bu sistem için over-engineering'dir ve kodda zaten hiç
> uygulanmamıştı (hepsi TODO idi). O dokümanın değerli KAVRAMSAL kararları (veri sahipliği,
> field-level permission ilkesi, ADR'ler) bu belgeye ve requirements'a zaten aktarılmıştır.
> Doküman silinmez (kavramsal arşiv) ama uygulamada bu belge esas alınır.
>
> **İsimlendirme:** Bu belgedeki adımlar **"Faz"** (Faz 0..7). Mimari/handover
> dokümanlarındaki "Aşama 1/2" topolojisi AYRI bir şeydir; karıştırma.
>
> **Tek istisna — "8 aşama":** Faz 5'teki email zincirinin "isimli 8 aşaması"
> (Welcome/Catalogue/...) bu faz numaralandırmasıyla ilgisizdir; o, email türlerinin sırasıdır.

> **Bu belge neye dayanıyor:** mimari karar (cross-DB ölçümü, 0 gerçek-join+real-time),
> gap analizi (35 ihtiyaç), üç derin analiz (LIFFY/ELIZA/LEENA, dosya:satır kanıtlı),
> requirements tam okuması (pusula). Tahmin yok; her faz kanıta bağlı.

---

## BÖLÜM 1 — MÜHÜRLENEN GERÇEKLER (tartışma kapandı)

### 1.1 Stratejik gerçek
Zoho senin **gerçek iş motorun**. ELL'in görevi onu (quote→contract→payment→commission→
ledger) yeniden inşa etmek. LEENA/LIFFY/ELIZA, Zoho'nun çevresindeki yardımcı araçlar —
değerli ama motorun kendisi değil. **Ticari çekirdek üç sistemin hiçbirinde yok.**

### 1.2 Mimari (2026-06-19 kararıyla GÜNCELLENDİ — eski "3 DB" superseded)
- **2 DB ayrı kalır: LIFFY + LEENA.** Eski **eliza DB aktif mimariden çıkarıldı** (Zoho
  mirror, disposable). Cross-DB ölçümü zaten gerçek-join+real-time = 0 gösteriyordu; yeni
  karar "her şeyi tek DB'ye merge et" değil, **ELIZA mirror'ı atıp finance'i LEENA'da
  temiz kur**.
- **Ürün kabuğu ELIZA markasıyla görünebilir** ama **fiziksel finance LEENA'dadır**.
- **Tek servis sınırı LIFFY ↔ LEENA'dır. ELIZA ↔ LEENA bridge YOKTUR** (ELIZA ayrı DB değil).
- **ELIZA DB'ye contract/payment/commission İNŞA EDİLMEZ.**
- **LIFFY ayrı kalır — iki sebeple:** (a) email deliverability izolasyonu, (b) **insan/güven
  izolasyonu** (freelancer satışçılar LIFFY'de çalışır, iç finans dünyasına erişemez).
- **Veri akışı olay-bazlı** (convert/signed/cancel), sürekli senkron değil.
- **Over-engineering YASAK:** SSO için basit paylaşılan secret — RS256/JWKS/saga DEĞİL.

### 1.3 İki halka modeli (senin kararın + requirements satır 351-363 ilkesi)
```
DIŞ HALKA — LIFFY                       İÇ HALKA — Ana uygulama
(freelancer/güvenilmez satış ekibi)     (güvenilir proje ekibi + sen)
  lead → campaign → quote                 contract → payment → commission → ledger
  satışçı komisyon/finans GÖRMEZ          catalogue + email zinciri + LEENA operasyon
            └──────── convert gate (güven sınırı kapısı) ────────┘
```

### 1.4 Geçiş güvenlik ağı (senin verdiğin bilgi)
- **Zoho 1 yıl daha açık kalacak** → hata olursa gerçek Zoho'da, kayıp yok.
- **ELIZA ve LIFFY şu an KULLANILMIYOR; sadece LEENA canlı** → ELIZA/LIFFY'de özgür
  hareket; sadece LEENA'nın canlı visitor/badge akışına dikkat.

### 1.5 Korunan adalar (2026-06-19: ELIZA artık "korunan ada" DEĞİL)
- **LEENA ops çekirdeği korunur (canlı):** floor plan builder (18 endpoint, DB-invariant),
  visitor/check-in/badge/QR/terminal, reactivation, conference certificates — kırılmaz.
- **LIFFY campaign/mining/quote korunur:** ZeroBounce, sequence drip, reply takibi, atomic
  çift-gönderim koruması — dış halka için kullanılır.
- **Eski ELIZA codebase korunacak ada DEĞİLDİR.** Dashboard, AI query, bot, risk/target
  ekranları yalnız **gereksinim/prototip referansı** olarak saklanır; yeni sistemin
  foundation'ı yapılmaz. (Fonksiyonlar değerli olabilir; ELIZA *sistemi* korunacak mimari
  ada değil.)

### 1.6 Sistem durumları (2026-06-19: ELIZA aktif sistem DEĞİL)
| Sistem | Durum | Bundan sonra ne yapılır |
|---|---|---|
| **LIFFY** | Aktif dış halka | Güvenlik izolasyonu, quote, convert bridge |
| **LEENA** | Aktif iç halka / canlı ops | Additive finance modülleri, canlı sistemi koruma |
| **Eski ELIZA** | Legacy / retire | Kapat, arşivle veya yalnız referans tut — **launch blocker DEĞİL** |

> Eski "ELIZA API auth finans yazmadan önce şart" mantığı **kalktı** — finans artık ELIZA'ya
> yazılmayacak. Önceki ortak-borç ölçümü (LIFFY zayıf auth/kırık tenant/28-dosya fallback;
> LEENA visitor-export izolasyonu + commit'li secret + eksik migration) **LIFFY ve LEENA için
> hâlâ geçerli**; ELIZA satırı tarihsel referanstır.

### 1.7 Güvenliğin doğru konumu (senin uyarın)
Bugün dışa kapalı, sadece sen+asistanın → **acil yangın değil.** Ama:
- LIFFY izolasyonu = freelancer'a açmadan ÖNCE şart (önkoşul, takvimsel acil değil)
- ~~ELIZA auth = finans yazmadan ÖNCE şart~~ → **KALKTI** (2026-06-19): finans ELIZA'ya
  yazılmıyor; bunun yerine **LEENA Finance permissions + server-side yetki** önkoşuldur.
- Commit'li secret + eksik migration = ucuz, erken yapılmalı (LEENA/LIFFY repo/sistem koruması)
Yani güvenlik "ayrı kriz aşaması" değil, **ilgili dilimin gömülü önkoşulu.**

---

## BÖLÜM 2 — TEMEL YÖNTEM

**Dikey dilim, yatay katman değil.** Her dilim baştan sona çalışan EN İNCE hattır;
gerektirdiği minimum zemini yanında getirir. Her dilim sonunda GÖREBİLECEĞİN çalışan
bir şey olur. (v1'in hatası: önce tüm zemini kurmak → boğulma.)

**Diğer Claude'un 8 düzeltmesi — nasıl ele alındı:**
1. LIFFY-ELIZA kararı → ÇÖZÜLDÜ: quote LIFFY'de (güven izolasyonu), convert=sınır kapısı
2. Dual contract tablosu → Faz 3'te "tek source of truth: LEENA Finance; **eski ELIZA mirror yalnız tarihsel/prototip referans — migration kaynağı DEĞİL** (gerçek migration Zoho → LEENA)"
3. Aşama'yı böl → ticari çekirdek 3 ayrı dilime bölündü (quote / contract+convert / payment+commission+ledger)
4. Audit baştan → her yazılabilir tabloya gün-1'den created/updated/by + değişiklik tablosu
5. UUID + users → gün-1 kuralı: tüm yeni PK'lar UUID, ID çakışması engellenir
6. Lead→quote köprüsü → LIFFY içi (cross-app değil), senin kararınla basitleşti
7. Test → her dilime gömülü smoke test + happy-path checklist + finans için unit test
8. Multi-tenant → gün-1 kuralı: tüm yeni tablolar organizer_id ile

---

## BÖLÜM 3 — FAZLAR

### FAZ 0 — Temel hijyen (şema kurtarma + secret) ⏱️ ~1 hafta · DÜŞÜK risk
> İnşaata başlamadan binanın planını çıkar. Ucuz, risksiz (çoğu salt-okuma), ama
> bugünkü tek geri-DÖNÜLEMEZ riski (eksik şema) kapatır.

**0a. Şema kurtarma (2026-06-19: amaç "üç sistemi kurtarmak" değil → LEENA+LIFFY güvene al, ELIZA'yı dondur)**
- **LEENA canlı DB şeması kesin korunur** + **LIFFY şeması korunur** (`pg_dump --schema-only`, READ-ONLY).
- Eksik LEENA tablolarının CREATE'lerini migration olarak koda ekle:
  - LEENA: terminals, badge_templates, conference_certificates, exhibitor_leads,
    import_logs, reactivation_tokens, visitor_event_status (+qr_code UNIQUE)
- **Eski ELIZA şeması yalnız ARŞİV/REFERANS olarak dump alınır.** ELIZA migration'larını yeni
  sistemin migration kaynağı yapmak **YANLIŞ**; eski ELIZA contracts/expos/payments tabloları
  **LEENA'ya migrate edilmeyecek**.
- `initial.sql`'in başındaki `DROP TABLE CASCADE`'i güvene al (yanlış çalıştırma koruması)
- Doğrula: temiz bir test DB'sine migration'lardan kur, canlı şemayla diff'le
- **Yeni amaç:** LEENA canlı ops'u güvene al + LIFFY dış halkayı güvene al + **eski ELIZA'yı dondur/arşivle**.

**0b. Secret hijyeni (ucuz, repo koruması)**
- LEENA: `.env.backup` (+kopyaları) git'ten kaldır, JWT/SendGrid secret rotate et
- Eski ELIZA (terk edildi) erişilebilir kalacaksa: JWT_SECRET .env'e koy (hardcoded default'tan kurtar); aksi halde decommission/arşiv — launch blocker değil
- LIFFY: 28 dosyadaki fallback temizliği + boot-time guard (JWT_SECRET yoksa başlama)
- Zoho webhook hardcoded token'larını env'e taşı (LEENA webhook.js, vb.)
- Üç repoda `.gitignore` `.env*` kapsasın

**Çıktı:** Şema koddan kurulabilir; secret'lar düz metin değil. Canlı sistem bozulmadı.
**Risk notu:** LEENA canlı — şema çekimi READ-ONLY; hiçbir migration canlıya uygulanmaz,
sadece koda yazılır.

---

### FAZ 1 — LIFFY'yi satışa hazırla ⏱️ ~8-12 hafta · ORTA risk
> Dış halka. ELIZA/LIFFY kullanılmadığı için özgür. İçeride alt-dilimlere bölünür;
> her alt-dilim çalışan parça. ÖNCELİK sırası (efor sırası değil):

**1a. GÜVENLİK İZOLASYONU ← MUTLAK İLK (bloke edici)**
- persons/prospects/companies/pipeline/export'a owner + organizer_id scope uygula
- `permissions` JSONB'yi canlandır (bugün ölü kod) veya scope tablosuna bağla
- "satışçı sadece kendi lead/quote/müşterisini görür+export eder" gerçekleşsin
- Bu olmadan LIFFY freelancer'a AÇILAMAZ (requirements satır 351-363 ihlali)
- *Smoke test:* iki test satışçısı, biri diğerinin verisini görememeli/export edememeli

**1b. CAMPAIGN CİLA ← en az iş (zaten TAM)**
- op/marketing template flag (operasyonel mail marketing footer'ından muaf)
- worker-seviye günlük throttle (şu an sadece /start'ta)

**1c. FRONTEND AUTH SERTLEŞTİR**
- server-side session doğrulama (şu an sadece client-side localStorage)
- route guard; rol gating kozmetikten gerçeğe (1a düzelince ekran doğru veriyi gösterir)

**1d. LEAD PIPELINE TAMAMLA**
- manuel tek-lead create endpoint (bugün YOK — satışçı tanıştığı kişiyi ekleyemiyor)
- disqualification sebep taksonomisi (requirements satır 209-213)
- routing/round-robin + fallback queue (requirements satır 233-238)
- domain/company dedup (bugün sadece email)

**1e. MINING ÜRÜNLEŞTİR**
- self-service tetikleme (geliştirici-CLI'yi kaldır — bugün admin'e terminal komutu maillıyor)
- AGGREGATION_PERSIST'i aç (madenlenen lead contact tablosuna düşsün)
- AI-miner runtime'ı aç; hardcoded token/job-id temizliği

**1f. QUOTE MODÜLÜ ← en çok iş (sıfırdan)**
- product/price catalog (~242 SKU, m²-bazlı paketler PES/RF/SYK + ekstralar)
- quotes + line-items tabloları (UUID, organizer_id, audit kolonları)
- subject auto-gen `{Expo}-{Company}-{M²}` (requirements satır 303)
- AF-number: `Q{ISO}-{Sequence}` (office ISO kodu, requirements satır 305-309)
- currency seçimi + frozen EUR-equivalent (requirements satır 313, 317)
- validity period; durum Draft→Sent→Signed; signed-scan upload (satır 325)

**Çıktı:** LIFFY satış ekibinin güvenle kullanabileceği tam araç. Quote oluşturulup
Signed yapılabiliyor, satışçılar izole.

---

### FAZ 2 — Convert gate (güven sınırı kapısı) ⏱️ ~3-5 hafta · ORTA-YÜKSEK risk
> Sistemin kalbi ve en hassas organizasyonel sınır. Sadece veri dönüşümü DEĞİL —
> sales→project devri + kalite kapısı (requirements satır 327-349).

> **2026-06-19 değişikliği:** Eski hat `LIFFY signed quote → ELIZA contract → LEENA expo link`
> idi. **Yeni hat: `LIFFY signed quote → LEENA contract → LEENA expo FK`.** ELIZA API auth
> artık convert önkoşulu DEĞİL.

- **Signed quote LIFFY'de doğar.**
- **Review/convert aksiyonu authorized iç kullanıcı** tarafından yapılır (server-side yetki).
- Signed quote → Owner + Project'e bildirim (sales rep'e DEĞİL — satır 333)
- Project review kuyruğu; "Convert" aksiyonu yalnız Project'e görünür
- Convert kalite kapısı: Project her alanı gözden geçirir; hata varsa convert ETMEZ,
  satışçıyı arar düzelttirir (insan-denetimli akış kodla desteklenmeli, satır 341)
- **Convert sonucu LEENA DB'de contract oluşturur.** `contract.expo_id` → **LEENA'daki canonical
  `expos.id`'ye gerçek FK**. AF# Q→A (aynı sequence), alanları kopyala, operasyonel alanları boş bırak.
- **Tek cross-system bridge: LIFFY → LEENA.**
- **Idempotency şart:** aynı quote iki kez convert edilirse iki contract doğmamalı
  (`source_quote_id` LIFFY UUID = logical reference + idempotency key).

**Çıktı:** Quote → (LEENA) Contract zinciri çalışıyor. Güven sınırı kuruldu.

---

### FAZ 3 — LEENA Finance Core / ELIZA Finance tab ⏱️ böl: 3a + 3b
> **2026-06-19:** Eski başlık "ELIZA artık işlem sistemi" idi → **TERS DÖNDÜ.** Finans
> çekirdeği **LEENA DB'de** kurulur; kullanıcıya **ELIZA / Finance tab** olarak görünür.
> Eski ELIZA Zoho-mirror'ı **kullanılmaz**; gerçek migration ileride **Zoho → LEENA** yapılır.
> Yeni model: contracts / payment schedule / actual payments / commissions / sales agents /
> ledger-accounts hepsi **LEENA DB'de**; reporting/AI/bot daha sonra bu yeni LEENA modelinin
> üstüne kurulur.

**3a. Contract yazılabilirlik + payment ⏱️ ~4-6 hafta · ORTA-YÜKSEK**
- contracts'a operasyonel kolonlar (scan_link, catalogue_page, stand, sales_group — bugün şemada YOK)
- 5-status lifecycle yazılabilir (Active/On Hold/Transferred/Cancelled), Project-restricted
- Transfer first-class (transferred_from_contract_id)
- **payment-create endpoint** (bugün YOK); paid_eur'u contract_payments'tan HESAPLA
  (denormalize saklama YASAK — requirements satır 510-518)
- gerçek installment schedule (sentetik 30/70'i değiştir)
- *Unit test:* payment toplamı = balance; currency freeze doğru
- *(Not: Eski "Zoho/ELIZA alan-sahipliği" maddesi kaldırıldı — finans LEENA-owned'dır;
  tarihsel Zoho verisi ileride Zoho→LEENA migration fazında ele alınır.)*

**3b. Commission + multi-account ledger ⏱️ ~6-10 hafta · YÜKSEK (en ağır)**
- Commission (greenfield ama BASİT — "kural yok, sadece sayı", satır 468-474):
  agent/sr/sd nullable FK + nullable pct + default+override + `amount×pct`
  + paid-status + cancellation netting (satır 485-493 — tek karmaşık kısım)
- Multi-account ledger (en ağır, neredeyse tam yeni):
  accounts (bank/cash/virtual) + two-sided transactions + transfers
  + işlem-bazlı frozen rate + stream'den computed balance + owner current-account
  + budget + refund/credit (kredi tercihli, satır 146)
  + gerçek expenses subsystem (2-seviye 6-kat/~75-tip taksonomi)
- *Unit test:* her para hareketi iki-taraflı; EUR konsolidasyon doğru

**Çıktı:** Contract→payment→commission→ledger zinciri tam. Çekirdek OMURGA bitti.
**LEENA Finance artık işlem sistemi** (kullanıcıya ELIZA/Finance tab). Zoho'nun finans işini
paralel yapabiliyor. *(Eski "ELIZA artık işlem sistemi / Zoho-mirror referans / mirror 1 yıl
sonra emekli / ELIZA alan sahipliği" ifadeleri kaldırıldı — eski ELIZA mirror kullanılmaz.)*

---

### FAZ 4 — Zemini birleştir: kimlik + yetki + entegrasyon ⏱️ ~4-6 hafta · ORTA
> Omurga çalışınca, "tek sistem" haline getiren zemin. Artık ihtiyaç somut, spekülatif değil.

- **Paylaşılan kimlik** — tek kullanıcı kaynağı (UUID sayesinde çakışma yok). Faz 1-3'ün
  ayrı users'ları tek kaynağa map'lenir.
- **Permission matrix** (requirements 3.1) — field-level, per-user. LIFFY scope altyapısı temel.
  Profile template (10 rol), hierarchy (reports_to), special-perm ("Convert Quote")
- **Field-level visibility** — sales rep komisyonu görmesin ama contract'ı görsün (satır 361)
- **SSO** — **HS256 (basit paylaşılan secret)** kararı sabittir. **LIFFY + LEENA/ana uygulama**
  arasında basit auth/SSO; ağ çağrısı yok. (Üç-sistem değil iki-sistem; ELIZA ayrı token-doğrulayan
  sistem değil.) RS256/JWKS over-engineering; gerçek üçüncü taraf girerse o gün geçilir.
- **Contract listesi zaten LEENA'dadır** — ~~ELIZA'dan çek+cache~~ **KALDIRILDI**; cache/bridge gerekmez.
- **Finance field visibility LEENA içinde çözülür** — sales rep komisyonu görmesin ama contract'ı görsün.
- LEENA'da **organizer_id izolasyonunu da düzelt** (1a'nın LEENA karşılığı — buildVisitorFilter)
- **Admin/shared spine fiziksel sahibi:** iki-sistem mimarisinde doğal aday **LEENA DB**'dir
  (aksi açıkça kararlaştırılmadıkça üçüncü DB yaratılmaz).
- **Audit log detaylandır** — before/after JSON (Faz 0'daki temel kolonların üstüne)

**Çıktı:** Bu faz artık "üç sistemi birleştirme" değil; **LIFFY dış halkası ile LEENA iç
halkasını tek kullanıcı deneyimine bağlama** fazı. Tek giriş, tek yetki.

---

### FAZ 5 — Operasyonel verimlilik: catalogue + email zinciri ⏱️ ~5-8 hafta · ORTA
> Requirements'ın "en büyük verimlilik kazancı" dediği parçalar. Omurga+kimliğe bağlı.

- **Catalogue generator** (sıfırdan, requirements 2.4 — "Corel Draw'ı bir daha açma"):
  - 3 kaynaktan render: Expo (LEENA) + Contract listesi (**LEENA Finance**) + submission (LEENA)
    — *(catalogue generator artık ELIZA'dan contract çekmez)*
  - 3-4 master template + per-expo customization (renk/kapak/sponsor)
  - exhibitor self-service editör + deadline lock
  - on-demand PDF + web çıktı (PDF kütüphanesi bugün YOK — teknik olarak en yeni alan)
- **Email otomasyon zinciri** (requirements 2.7):
  - isimli 8 aşama (Welcome/Catalogue/Stand Design/Boost/Extra/BuildUp/Payment Reminder/Badge)
  - per-expo days-before trigger config (hardcoded "30 gün" DEĞİL — satır 549)
  - tek template + expo'dan dinamik veri (satır 150)
  - LEENA email altyapısı temel (GENİŞLET); marketing/operational flag (3b'den)

**Çıktı:** Corel'den kurtuldun; operasyonel mailler otomatik. Manuel iş ciddi azaldı.

---

### FAZ 6 — Zoho'yu emekliye ayır ⏱️ duruma göre · 1 yıl güvenlik ağı sonrası
> Zoho 1 yıl açık kalacak — baskısız, en sona.

- **Tarihsel veri migrasyonu hedefi açıkça `Zoho → LEENA`** (eski ELIZA mirror migration kaynağı DEĞİL).
- **Faz 3 boyunca staging LEENA DB'ye Zoho'dan örnek/full dry-run import yapılır** — migration
  uyumluluğu en sona bırakılmaz; sadece **final production cutover** en son yapılır.
- Reference data seed (kategoriler/sektörler/ülkeler) bir kez import, sonra LEENA sahibi
- 1 yıl paralel doğrulama: LEENA ile Zoho aynı sonucu veriyor mu (sürekli kontrol)
- **Eski ELIZA mirror tablolarını emekli etmek bir migration sonucu değil** — mimari kararla
  yapılacak **legacy cleanup**'tır.
- Güven oturunca Zoho OAuth kes, abonelik iptal

**Çıktı:** Zoho kapalı. ELL (LEENA çekirdekli) bağımsız tam iş motoru.

---

### FAZ 7 (opsiyonel, gelecek) — LEENA'yı satılabilir ürün yap
> "Belki satarım" hedefi. Her şey oturduktan SONRA.
- LEENA'nın visitor+badge çekirdeğini ayrı ürün olarak soyutla
- multi-tenant zaten şemada (organizer_id) AMA izolasyon Faz 4'te düzeltilmeli (yoksa
  ikinci tenant veri sızdırır — bugünkü kırık buildVisitorFilter)
- Elan Expo hardcode'larını temizle
- Bugünün değil, yarının işi.

---

## BÖLÜM 4 — HER FAZDA GEÇERLİ İLKELER

1. **Over-engineering'e dönme.** En basit çözüm. Karmaşıklık ancak gerçek ihtiyaç
   kanıtlanınca. (Architecture dokümanının RS256/JWKS/saga makinesi = senin boğulma sebebin.)
2. **Requirements = pusula.** Sadece "ne lazım" değil "hangi tuzaktan kaçın" da söylüyor
   (örn. denormalize saklama yasağı). Çakışmada requirements kazanır.
3. **Dikey dilim.** Her parça baştan sona çalışsın; her dilim sonunda görünür çıktı.
4. **Adaları koru.** LEENA ops canlı akışlarını koru; LIFFY campaign/quote dış halkasını koru.
   **Eski ELIZA AI/dashboard/bot kodunu yalnız REFERANS kabul et** — yeni finance foundation
   için onu koruma zorunluluğu yok.
5. **Güvenlik = gömülü önkoşul**, ayrı kriz değil. İlgili dilimden hemen önce.
6. **UUID + organizer_id + audit = gün-1 kuralı.** Her yeni tabloda. Sonradan eklemek pahalı.
7. **Zoho ayakta — risk düşük.** Hata gerçek Zoho'da; acele etme, paralel doğrula.
8. **Canlıyı (LEENA) bozma:** QR'ı yeniden üretme; email_worker SKIP LOCKED'a dokunma;
   yeni visitor endpoint organizer_id ile filtrele; migration'ı dry-run test et.

---

## BÖLÜM 5 — SIRADAKİ SOMUT ADIM

**2026-06-19 — yeni sıradaki somut adımlar:**
1. **Belgeleri kanonik hale getir** — roadmap v5 + bilgi mimarisi v3 + durum defteri amendment/superseded (bu iş).
2. **Eski ELIZA'yı freeze/legacy ilan et** — yeni feature/migration yok; convert-core branch deploy edilmez.
3. **ELIZA convert-core branch'i deploy ETME** — *retired experiment* olarak işaretle (026/027/028 dahil).
4. **LEENA'da additive finance foundation tasarla** (sales_agents, contracts, payment schedule/payments, commissions, ledger — canlı ops'a dokunmadan).
5. **LEENA staging DB'de finance migration dry-run** yap.
6. **LIFFY → LEENA convert bridge'i yeniden kur** (LEENA contract + canonical expo FK).

> *(Eski "üç sistemin canlı şemasını çek" adımı LEENA+LIFFY şema güvene-alma + eski ELIZA arşivleme
> olarak revize edildi — yukarıdaki Faz 0a.)*

> **Süreler yaklaşık.** Kod yazmıyorsun, AI'a prompt veriyorsun — esner. Önemli olan
> SIRA ve MANTIK. Kabaca toplam: ~8-14 ay, ama Zoho 1 yıl açık olduğu için baskı yok.
> Her dilim bittiğinde çalışan bir şey var — kaybolmanın panzehiri bu.
