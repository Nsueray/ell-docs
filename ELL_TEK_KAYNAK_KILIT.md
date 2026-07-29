# ELL — TEK KAYNAK İLKESİ (KİLİTLENDİ — 2026-06-20)

> **Durum:** KİLİTLİ. Taslak → Claude Code ölçümü → 3 bağımsız AI kontrolü (eski mimari
> Claude + ChatGPT + Gemini) → Suer onayı. Beş kaynak aynı çekirdekte uzlaştı. Bu belge
> tüm belgelere (defter, yol haritası, glossary, requirements) ilke olarak işlenecek;
> eski çelişen kural (ELL_RULES "ELIZA owner, manuel SQL sync") iptal edilecek.

---

## 1. İLKE (kilitli çekirdek)

**Tek Kaynak İlkesi (Single Source of Truth):** Her ana veri tipinin tek bir AUTHORITATIVE
OWNER sistemi vardır. O veri yalnız owner sistemde yaratılır/değiştirilir/silinir. Diğer
sistemler o veriyi owner'dan gelen **otomatik, read-only, türetilmiş kopya** olarak kullanır.

**Kritik tanım:** Tek kaynak = tek FİZİKSEL kopya değil, tek YAZMA/KARAR otoritesi. Kopya
olabilir — ama read-only, owner'dan türemiş, elle düzenlenemez, tek yönde gelir (owner→kopya).

**YASAK:** Aynı verinin iki sistemde BAĞIMSIZ (birbirinden habersiz, ayrı ayrı elle
düzenlenen) iki listesi. Bu çelişir, zamanla ayrışır (Turkey/Türkiye/TR). Ölçekten
bağımsız geçerli — ayrışma ölçekle değil zamanla olur.

**Manuel SQL sync YASAK:** İki tabloyu elle SQL ile eşitlemek (kim/ne zaman/ne eksik belli
olmaz) yasaktır. Sync app-seviyesinde, otomatik, denetlenebilir olur.

---

## 2. VERİ DAĞILIM HARİTASI (kilitli)

Mimari: 2 sistem — LIFFY (dış halka/satış, ayrı DB) + LEENA (iç halka/operasyon+finans,
ayrı DB). ELIZA = LEENA içinde marka/Finance-tab. Tek cross-DB sınır: LIFFY↔LEENA.

**Sahiplik kriteri:** "Nerede zengin/önce kuruldu" DEĞİL → "verinin uzun vadeli iş sahibi /
kim yönetiyor" belirler.

### İş verisi (business data)
| Veri | Owner | Diğer sistem nasıl alır | Gerekçe |
|---|---|---|---|
| Lead / prospect | **LIFFY** | LEENA gerekirse güvenli özet | Satış keşfi dış halka işi |
| Quote | **LIFFY** | LEENA convert'te okur+doğrular | İmza öncesi satış çekirdeği |
| Contact/Company (pre-sale) | **LIFFY** | — | Satış keşif kaydı |
| Contact/Company (post-convert customer) | **LEENA** | LIFFY'ye güvenli read-only geri-sync (yeni quote için) | Müşteri iç halka; convert sonrası truth LEENA |
| Sales Contract | **LEENA** Finance | — | Post-convert finans |
| Payment / Revenue / Expense | **LEENA** Finance | — | Finans iç halka |
| Commission | **LEENA** Finance | — | Finans iç halka |
| Ledger / hesaplar | **LEENA** Finance | — | Finans iç halka |
| Visitor / Badge / Check-in | **LEENA** Operasyon | — | Operasyon çekirdeği |

### Referans verisi (reference data) — hepsi LEENA master, LIFFY read-only synced-copy
| Veri | Owner | Not |
|---|---|---|
| Expo (fuar) | **LEENA** | Expo'nun gerçek hayatı LEENA'da (visitor/floor/badge/catalogue/contract). LIFFY artık bağımsız expo YARATAMAZ — read-only synced görür. published_to_liffy + sales_open flag'leri ile yayınlanır. |
| Country (ülke) | **LEENA** | ISO code + display name + **aliases** (Turkey/Türkiye/TR→TR). LIFFY'de serbest-text BİTER. |
| Sector (sektör) | **LEENA** | Canonical sector. (LIFFY'nin "mining tag/campaign kategorisi" AYRI bir LIFFY verisi olabilir — canonical sektörle karıştırma.) |
| Currency (para birimi listesi) | **LEENA** | Yaprak (iç ekip) yönetir; revenue/expense/contract'ta kullanılır → finans verisi. LIFFY'deki tablo seed kaynağı olur, sonra read-only kopya. |
| Exchange rate (kur) | **LEENA** Finance | **Snapshot kuralı:** kur listesi LEENA master, AMA işlemde kullanılan kur quote/contract'ta DONAR (snapshot). Kur sonradan değişince eski belge değişmez. (Contract'ta zaten exchange_rate+revenue_eur frozen.) |
| Office (ofis listesi) | **LEENA** Admin | Organizasyonel/permission/reporting/komisyon scope verisi. LIFFY read-only kullanır. |
| Sales Agent | **LEENA** Finance | Komisyon entity (≠ user). LIFFY quote'ta seçer ama liste LEENA'dan gelir. |

### Ticari kural verisi (commercial rules) — LEENA Finance master, LIFFY kullanır
| Veri | Owner | Gerekçe |
|---|---|---|
| Price book / m² fiyat / stand tipi fiyatları | **LEENA** Finance | Quote LIFFY'de hazırlanır ama resmi fiyat politikası finans kontrolünde |
| Payment term şablonları (peşinat/taksit/vade) | **LEENA** Finance | Finans kontrolünde |
| Discount authority / indirim yetkisi | **LEENA** Finance/Admin | Satış quote yapar, indirim yetkisi iç kurala bağlı |
| Commission rules (komisyon kuralları) | **LEENA** Finance | Komisyon finans tarafı |
| Tax/VAT (kullanılıyorsa) | **LEENA** Finance | Finans domain |

### Kimlik (Faz 4'te netleşir)
| Veri | Owner | Not |
|---|---|---|
| User / permissions | **LEENA** (muhtemel) | Kimlik birleştirme Faz 4. Basit SSO/sync — büyütme. |

**Özet kural:**
- Satış öncesi (lead/quote/pre-sale contact) → **LIFFY** üretir.
- Operasyon + finans + tüm referans + ticari kural → **LEENA** master.
- Convert = LIFFY→LEENA tek geçiş (quote→contract; pre-sale→customer). LEENA doğrular.
- LEENA→LIFFY = güvenli read-only referans sync (expo/country/sector/currency/office/agent/
  price/terms) + post-convert customer geri-sync.

---

## 3. MEKANİZMA (ilke kilitli; mekanizma LIFFY aktivasyonunda kurulur)

**Read-live DEĞİL → Synced-copy (tek yön, read-only).** Gerekçe: güven sınırı (LIFFY finans
görmemeli) + LEENA kapanınca LIFFY çalışmaya devam etmeli + sürekli bağımlılık olmamalı.

**Desen (basit, ölçeğe uygun — Kafka/event-bus/distributed-tx GEREKMEZ):**
1. LEENA güvenli "sales reference bundle" endpoint'i yayınlar (whitelist — yalnız güvenli
   alanlar: expo published alanları, country, sector, currency, office, active agents,
   price/terms; ASLA revenue/payment/commission/margin/internal).
2. LIFFY backend service-token ile çağırır (LIFFY frontend doğrudan LEENA'ya gitmez;
   LIFFY DB'ye doğrudan erişim yok).
3. LIFFY gelen veriyi local read-only ref_* tablolarında tutar (ref_expos, ref_countries,
   ref_sectors, ref_currencies, ref_offices, ref_sales_agents...).
4. LIFFY kullanıcıları bu kayıtları EDİT EDEMEZ.
5. Sync: admin "Sync" butonu / nightly cron / deploy-seed; sonra updated_at incremental.

**Convert'te LEENA doğrular:** "Bu quote geçerli LEENA expo'ya mı ait? Expo satışa açık mı?
Currency/rate/agent geçerli mi? Fiyat/vade kabul edilebilir mi?" → LIFFY'ye güven, LEENA'da
doğrula.

**Stable public ID/code:** LEENA integer ID içeride kalır, ama cross-system'de stable code
kullanılır (expo_code, ISO country/currency code, sector slug, office code) — integer'a
aşırı bağımlılık migration'da sorun çıkarmasın.

---

## 4. İZİN VERİLEN "kopya" türleri (yasak değil — gerekli)
- **Read-only cache:** LIFFY'deki ref_* tabloları (owner'dan türemiş, düzenlenemez).
- **Historical snapshot:** quote/contract'ta donmuş değerler (expo adı, kur, fiyat, agent
  o günkü hali) — referans master sonradan değişse de eski belge değişmez. Audit/legal.
- **Reporting read-model:** ileride dashboard için materialized view/cache (derived, owner değil).

---

## 5. GEÇİŞ / MIGRATION DİKKAT (LIFFY dormant iken yapılacak temizlik)
- **LIFFY serbest-text country → LEENA reference FK'ye** çevir (LIFFY dormantken ucuz).
- **LIFFY hedefsiz sector_id** → LEENA sector read-only sync.
- **LIFFY bağımsız expo listesi** → kapat, LEENA expo'ya map/read-only.
- **LIFFY currency/office tabloları** → LEENA'ya seed olarak taşı, sonra LIFFY read-only.
- **Canonical code + alias** tabloları kur (Zoho kirli verisi için: Turkey/Türkiye→TR).
- **Delete yerine inactive/deprecated** (eski sector'e bağlı historical contract olabilir).
- **Zoho gerçek canonical kaynak (~1 yıl):** bugünkü LEENA seed (26 sektör vb.) GEÇİCİ —
  Zoho migration'da canonical liste yeniden gelecek; bugünkü seed'i kalıcı doğru SAYMA.
- **Zoho mapping dry-run ERKEN** (final cutover son, ama uyumluluk erken test):
  Zoho country/sector/expo/agent/currency/office → LEENA canonical tablolarına map.

---

## 6. ESKİ KURAL İPTALİ (ELL_RULES.md)
Eski: "Referans veri üç DB'de identical replica; owner ELIZA; manuel SQL sync." → **TAMAMEN
İPTAL.** (ELIZA retired → "ELIZA owner" void; hiç uygulanmamıştı; manuel SQL sync yasak.)
Yeni: bu belge (Tek Kaynak İlkesi — referans master LEENA, LIFFY'ye güvenli read-only sync).

---

## 7. KİLİTLENEN TEK PARAGRAF (belgelere işlenecek)
> **Tek Kaynak İlkesi:** Her ana veri tipinin tek authoritative owner sistemi vardır; yalnız
> orada yaratılır/değiştirilir; diğer sistemler owner'dan otomatik read-only türetilmiş kopya
> kullanır. Bağımsız elle-düzenlenen çift liste ve manuel SQL sync yasaktır. Dağılım: satış
> öncesi (lead/quote) → LIFFY; operasyon + finans + tüm referans (expo/country/sector/
> currency/exchange-rate/office/agent) + ticari kurallar (price/payment-terms/discount/
> commission) → LEENA master. Convert = LIFFY→LEENA tek geçiş, LEENA doğrular. LEENA→LIFFY =
> güvenli read-only referans sync (mekanizma LIFFY aktivasyonunda; synced-copy, tek yön,
> Kafka/ayrı-servis YOK). İşlem kuru snapshot olarak donar. Zoho ~1 yıl canonical kaynak;
> bugünkü seed geçici.
