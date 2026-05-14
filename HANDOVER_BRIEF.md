# ELL Architecture — Handover Brief

**Son güncelleme:** 2026-05-13
**Source of truth:** github.com/Nsueray/ell-docs (`/architecture/`)

## Mevcut durum

### Aşama 1 — Sistem Topolojisi
- **v1.1 kilit** (2026-05-11)
- Dosya: `/architecture/ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md`
- Karar seti: A1-A29

### Aşama 2 — Cross-Cutting Infrastructure

- **Bölüm 1 — Identity Model: v1.0 kilit** (2026-05-12)
  - Dosya: `/architecture/ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY_v1_0.md`
  - Karar seti: B1-B20 (20 karar)
  - Yakınsama: 4 turda kilit (13→10→6→2 düzeltme)

- **Bölüm 2 — Permission Matrix + Hierarchy + Scope: v1.0 kilit** (2026-05-12)
  - Dosya: `/architecture/ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS_v1_0.md`
  - Karar seti: B21-B44 (24 karar)
  - Yakınsama: 7 turda kilit (19→20→9→6→3→3→1 düzeltme)
  - Anahtar yapısal kararlar: permission registry sentinel namespace
    (__global__, __protected__), module-specific scope resolver pattern,
    create payload validation, applies_to_action field, registry
    enforcement pipeline (API + migration + startup scan)

- **Bölüm 3 — Auth + Session + Cache Invalidation: DEVAM EDİYOR**
  - Repo'da henüz dosya yok. Tüm Bölüm 3 bittiğinde tek dosya olarak
    commit edilecek: `ELL_ARCHITECTURE_STAGE_2_SECTION_3_AUTH_v1_0.md`
  - Kapsam: 13 alt başlık + 2 iç checkpoint
    - 3.1 Auth boundary ve actor model — **v1.0 kilit**
      (C1-C12, 5 tur, 2026-05-13)
    - 3.2 Credential ve password lifecycle — v0.1 draft hazır,
      review bekliyor
    - 3.3 Session lifecycle + refresh token modeli
    - 3.4 JWT payload, signing, JWKS ve key rotation
    - --- ARA CHECKPOINT 1 ---
    - 3.5 LIFFY token verification ve cross-app session
    - 3.6 Service-to-service auth
    - --- ARA CHECKPOINT 2 ---
    - 3.7 Permission / scope / auth versioning
    - 3.8 Cache invalidation ve LIFFY replica
    - 3.9 Critical security change propagation
    - 3.10 Self-edit endpoints
    - 3.11 WhatsApp opt-in verification flow
    - 3.12 Public form token authentication
    - 3.13 WhatsApp bot user identification
  - 3.1 anahtar kararları: 5 runtime actor tipi (user / service
    [internal+external integration subtype] / contractor / bot /
    anonymous), delegated user context iki kanal (browser sync forwarded
    JWT + bot channel server-generated signed context), async akışta
    source_user_id audit context, entity metadata actor_type vs audit
    log actor_type ayrımı (Bölüm 1/2 amendment v1.1 zorunlu —
    'integration' enum eklenmesi Bölüm 3 finalinde)
  - Önemli mimari prensipler (3.1'de oturmuş):
    - JWT minimal payload — authorization facts (is_owner gibi)
      authoritative taşınmaz, cache'den okunur (C10)
    - Üç ayrı version: permission_version, scope_version, auth_version
      (3.7'de detay)
    - Owner bypass authorization-only, business validation Owner için de
      aktif (B25 paralel, Service actor için de geçerli)

- **Bölüm 4-8: bekliyor**
  - 4: Reference data sync
  - 5: Audit log (audit log actor_type enum tam tanımı, audit-worthy
    actions sınıflandırması, delegation redaction)
  - 6: Notification dispatcher
  - 7: Search
  - 8: WhatsApp bot scope (channel restriction layer)

### Aşama 3 — Module-by-module
Aşama 2 bitince başlar. Prerequisite'ler:
- Contract resolver explicit ownership alanları
  (sales_owner_user_id, account_owner_user_id,
  responsible_project_user_id) — B35 prerequisite
- Permission registry kod-level implementation
- Module read + create resolver'ları her modül için
- Permission matrix UI mockup
- Migration framework CI/lint hook
- Startup scan implementation

## Çalışma yöntemi — üçlü AI orchestration

**Roller:**
- **Mimari Claude** (ayrı chat / proje): draft üretir, self-review
  uygular, iterasyonları yazar
- **Sentez Claude** (ayrı chat / proje): cross-document tutarlılık
  kontrolü, ChatGPT review'ları sentezi, kanonik doküman uyumu
  (Aşama 1 + Bölüm 1+2'yi okur)
- **ChatGPT** (Suer doğrudan kullanır): detay-seviye review, insert
  simülasyonu, edge case yakalama. Kanonik dokümanları görmez — sadece
  o turun metnine bakar
- **Suer**: orchestrator, son karar verici

**Akış:**
1. Mimari Claude draft yazar (self-review checklist uygulayarak)
2. Suer draft'ı sentez Claude'a ve ChatGPT'ye paralel iletir
3. Sentez Claude paralel review yapar (ChatGPT'nin haklı olanlarını
   doğrudan kabul ediyor, eksik gördüklerini ekliyor — uzun kıyaslama
   yapmıyor)
4. Suer sentezi mimari Claude'a iletir
5. Mimari Claude patch'leri uygular, yeni versiyon çıkar
6. Yakınsayana kadar tekrarla (geometrik azalış pattern'i)

**Yakınsama bekleyişi:**
- Bölüm 1: 4 tur, 31 düzeltme
- Bölüm 2: 7 tur, 61 düzeltme
- Bölüm 3.1: 5 tur, 19 düzeltme (self-review disiplini sayesinde daha hızlı)
- Beklenti: sonraki alt başlıklar 3-5 tur arası

**Self-review checklist (mimari Claude her draft öncesi uygular):**
- Bölüm 1+2 cross-reference kontrolü (özellikle B5, B10, B19, B21, B22,
  B25, B32 ve C1-C12)
- Bölüm 1 LEENA legacy migration uyumluluğu — kopyalanmış password_hash
  + must_change=true state'i her state model değişikliğinde teyit edilir
- Schema'da invalid kategoriye eklenen state'ler, kanonik dokümanlarda
  geçerli olarak işaretli mi double-check
- Schema'larda actor pattern (`*_by + *_by_actor_type` + CHECK) tutarlı mı
- Pseudocode senaryo simülasyonu (Owner senaryosu, system actor
  senaryosu, edge case)
- Sentinel namespace (`__global__`, `__protected__`) doğru kullanım
- Schema NOT NULL + CHECK kombinasyonları enforcement gediği bırakıyor mu

## Suer'in iletişim stili
- Mixed Turkish/English
- "stres yapma" = yavaşla, acele etme
- "kabul" / "onaylıyorum" / "devam" = onay
- Yorgun olabilir ama kararlı. Section-by-section onay.
- Uzun metinleri okumaz — özet ister, full text değil
- Doğrudan, dürüst değerlendirme bekler
- Kalibrasyonu sürekli sorgular (multi-AI dynamic'i sağlıklı tutmak için)

## Proje yapısı (claude.ai)

İki ayrı Claude projesi paralel çalışıyor:

- **"ELL Architecture Design"**: Mimari Claude'un çalıştığı yer.
  Draftlar burada üretilir.
- **"Elan Expo Requirements"**: Sentez Claude'un çalıştığı yer.
  Suer drafts'ı buraya yapıştırır, ChatGPT yorumlarını buraya
  yapıştırır, sentez burada üretilir. (Proje adı eski needs-doc
  fazından kalma; mimari faz da burada yürüyor.)

Her iki proje de bu HANDOVER_BRIEF + Aşama 1 + Bölüm 1 + Bölüm 2
dosyalarına ihtiyaç duyar (project knowledge'da).

## Bekleyen action'lar

**Hemen sıradaki:**
- 3.2 Credential ve password lifecycle v0.1 draft review

**Bölüm 3 sonu için:**
- C12 amendment: Bölüm 1/2 entity metadata enum'larına 'integration'
  actor_type eklenmesi (Bölüm 3 final review'da, Bölüm 5 audit log enum
  tasarımıyla koordineli)

**Açık kalan büyük konular (Bölüm 4+):**
- Scope cache expiry disiplini (Bölüm 4)
- Audit log actor_type enum tam tanımı + audit-worthy classification +
  delegation redaction (Bölüm 5)
- Channel restriction layer (Bölüm 8)

## Repo organizasyonu
```
ell-docs/
├── architecture/                 # Master mimari kararlar (kanonik)
│   ├── ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md
│   ├── ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY_v1_0.md
│   ├── ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS_v1_0.md
│   └── README.md
├── decisions/                    # ADR'lar (Aşama 2 sonrası revize)
├── eliza/, liffy/, leena/        # Sistem-spesifik docs (Aşama 2 sonrası)
├── ELL_RULES.md, ELL_ROADMAP.md, # Eski planlama, tarihsel referans
│   ELL_GLOSSARY.md, ELL_FEATURE_INSPIRATION.md
├── HANDOVER_BRIEF.md             # Bu dosya
└── README.md
```

## Çakışma kuralı
Bir doküman başkasıyla çakışıyorsa, /architecture/ her şeyin
üstündedir. Aşama 1 v1.1 + Bölüm 1 v1.0 + Bölüm 2 v1.0 + (Bölüm 3
ilerledikçe alt başlık kilitleri) kanonik.
