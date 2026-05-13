# ELL Documentation

ELL Platformu'nun source-of-truth dokümantasyon repo'su.

## 📌 Master karar

**[Aşama 1: Sistem Topolojisi v1.1](architecture/ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md)**
(KİLİTLİ, 2026-05-11)

ELL'in en yüksek seviyeli yapısal kararları. İki uygulama
(LEENA + LIFFY) + bir çatı (ELIZA), iki DB, beş köprü, üç
finansal invariant, 29 mimari karar.

**[Aşama 2 Bölüm 1: Identity Model v1.0](architecture/ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY_v1_0.md)**
(KİLİTLİ, 2026-05-12)

users / sales_agents / data_entry_contractors üçlemesinin schema
modeli, lifecycle kuralları, organization aidiyeti, LEENA legacy
login migration'ı, integration credentials izolasyonu. B1-B20.

**[Aşama 2 Bölüm 2: Permission Matrix + Hierarchy + Scope v1.0](architecture/ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS_v1_0.md)**
(KİLİTLİ, 2026-05-12)

permission_templates, user_permissions matrix, permission registry
(sentinel namespace), protected system operations, scope resolver
pattern, authorization order, scope composition, hierarchy
enforcement. B21-B44.

## Klasör yapısı

- `/architecture/` — **Master mimari kararlar (kanonik)** — bu
  klasördeki dokümanlar diğer her şeyin üstündedir
- `/decisions/` — ADR'lar; bazıları banner'larla revize edilmesi
  gerektiği işaretli (bkz. INDEX.md)
- `/decisions/archived/` — Geçersiz kılınmış ADR'lar
- `/eliza/`, `/liffy/`, `/leena/` — Sistem-spesifik
  dokümantasyon (Aşama 2'de revize edilecek)

## Süreç durumu

- ✅ Aşama 1 — Sistem Topolojisi (v1.1, kilitli)
- ⏳ Aşama 2 — Cross-Cutting Infrastructure (devam ediyor: Bölüm 1 v1.0 ✅, Bölüm 2 v1.0 ✅, Bölüm 3-8 bekliyor)
- ⏸️ Aşama 3 — Data Ownership & API Contracts
- ⏸️ Roadmap — Aşama 2 sonrası

## Eski planlama dosyaları

`ELL_RULES.md`, `ELL_ROADMAP.md`, `ELL_GLOSSARY.md`, ve
`ELL_FEATURE_INSPIRATION.md` requirements gathering yapılmadan
önce yazıldı. Üst kısımlarındaki SUPERSEDED / NEEDS UPDATE /
CONTEXT UPDATE banner'larına dikkat. Bu dosyalar Aşama 2
paralelinde yeniden yazılacak; o zamana kadar **tarihsel referans**
olarak görün.

## Çakışma kuralı

Eğer bir dokümanın söylediği başka bir dokümanla çakışıyorsa:

1. `/architecture/` klasöründeki master karar her zaman geçerlidir
2. Sonra: `ELAN_EXPO_REQUIREMENTS_v1_0.md` (kanonik ihtiyaç dokümanı)
3. Sonra: Aktif (banner'sız veya CONTEXT UPDATE'li) ADR'lar
4. SUPERSEDED işaretli dokümanlar artık geçerli değildir
