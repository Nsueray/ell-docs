# ELL Implementation Phase Handover

**Tarih:** 2026-06-01
**Son güncelleme:** 2026-07-20
**Statü:** Mimari fazı tamamlandı, implementation fazına geçiş

## 2026-06-19 sonrası kararlar (mimari dokümanların üstünde)

- **ELIZA-terk kararı (2026-06-19):** ELIZA artık ayrı bir sistem/DB
  değil; **marka + LEENA içindeki Finance sekmesi**. Tek cross-DB
  sınır **LIFFY↔LEENA**. Eski `eliza_73du` convert çalışması
  **retired**.
- **Tek-kaynak ilkesi kilitlendi (2026-06-20):** Her ana veri tipinin
  tek authoritative owner'ı var; diğer sistem owner'dan otomatik
  read-only kopya kullanır. Satış öncesi (lead/quote/pre-sale
  contact) → **LIFFY**; operasyon + finans + tüm referans veri
  (expo/country/sector/**currency**/exchange-rate/**office**/agent)
  + ticari kurallar → **LEENA** master. Kanonik detay:
  `decisions/ELL_TEK_KAYNAK_KILIT.md`.

## Ana referans dokümanı

**`ELL_MIMARI_v1.0_KONSOLIDE.md`** — Implementation'ın tek source
of truth'u. Tüm mimari kararlar (sistem topolojisi, identity,
permissions, auth + session, audit) burada konsolide.

**Çakışma kuralı:** Yaşayan durum için **`ELL_DURUM_DEFTERI_v2`** +
**`ELL_YOL_HARITASI_v5`** kanoniktir; konsolide mimari dokümanla
çeliştiklerinde onlar kazanır. Tek-kaynak/ownership sorularında
`decisions/ELL_TEK_KAYNAK_KILIT.md` kazanır. `ELL_RULES.md`
superseded'dır.

## Arşiv

`archive/` klasörü altında detaylı mimari dokümanlar referans olarak
korunuyor:
- ELL_ARCHITECTURE_STAGE_1_TOPOLOGY (Aşama 1, A1-A29)
- ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY (Bölüm 1, B1-B20)
- ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS (Bölüm 2, B21-B44)

Bu dokümanlar deep-dive ve karar justification arşivi. Çakışmada
konsolide doküman kazanır.

**Aşama 2 Bölüm 3 (Auth + Session) detay dosyaları repo'ya commit
edilmedi.** Mimari süreçte 3.1-3.4 alt başlıkları detaylı yazıldı
(C1-C39, ~39 karar) ancak "Bölüm 3 tek dosya olarak komple commit
edilecek" kararı süreç durdurulduğunda henüz uygulanmamıştı. Bu alt
başlıkların tüm kararları konsolide dokümanın §4 (Bölüm 3 — Auth +
Session) bölümünde tam içerilmektedir; ayrı detay dosyalarına
ihtiyaç yoktur.

## Mimari süreçten çıkan kararlar (özet)

- Aşama 1 topology: A1-A29 (29 karar)
- Bölüm 1 Identity: B1-B20 (20 karar) + v1.1 amendment batch
- Bölüm 2 Permissions: B21-B44 (24 karar) + v1.1 amendment batch
- Bölüm 3 Auth + Session: C1-C39 (39 karar)
  - 3.1 Auth boundary: C1-C12
  - 3.2 Credential lifecycle: C13-C25
  - 3.3 Session lifecycle: C26-C32
  - 3.4 JWT detay: C33-C39

## Açık alt bölümler (implementation veya sonraki mimari turlarda)

- Aşama 2 Bölüm 4 — Reference data + LIFFY replikasyon
- Aşama 2 Bölüm 6 — Finance + commission
- Aşama 2 Bölüm 7 — Cache invalidation + propagation
  (auth implementation'ın ön koşulu; MVP minimum kararı konsolide
  dokümanda)
- Aşama 2 Bölüm 8 — WhatsApp bot + channel restriction

Bu bölümlerin scope cümleleri konsolide dokümanın §6'sında.

## Sonraki faz: Implementation

### Sprint-0 kararları (implementation öncesi)
- **Auth provider:** Custom (sıfırdan LEENA) vs hazır çözüm
  (Keycloak, Supabase Auth, Auth0)
- **Backend stack:** Node.js/TypeScript vs Python/FastAPI
- **Repo yapısı:** Monorepo vs ayrı repo
- **Hosting:** Self-hosted vs managed vs cloud
- **AI rol setup:** Feature builder, reviewer, debugger, vb. roller
  hangi platformlarda (claude.ai project, Claude Code, ayrı chat)

### Yaklaşım değişikliği

Mimari fazında kullanılan üçlü AI sistemi (Mimari Claude + Sentez
Claude + ChatGPT review) implementation fazında farklı rollere
evrilecek:
- Mimari aşamada: dokümantasyon ve karar üretimi
- Implementation aşamasında: feature builder, code reviewer,
  debugger, test writer, security auditor rolleri

Over-engineering tuzağından çıkış kararı 2026-06-01'de alındı;
6 aylık detaylı mimari süreç bu konsolide dokümanla kapatıldı.
