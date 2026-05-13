# ELL Architecture Documentation

Bu klasör ELL platformunun master mimari kararlarını içerir.

## Aktif dokümanlar
- **[ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md](ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md)**
  — Aşama 1: Sistem Topolojisi (KİLİTLİ, 2026-05-11)
- **[ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY_v1_0.md](ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY_v1_0.md)**
  — Aşama 2 Bölüm 1: Identity Model (KİLİTLİ, 2026-05-12)
- **[ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS_v1_0.md](ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS_v1_0.md)**
  — Aşama 2 Bölüm 2: Permission Matrix + Hierarchy + Scope (KİLİTLİ, 2026-05-12)

## Gelecek dokümanlar
- Bölüm 3 — Auth + Session + Cache Invalidation: yazımı sürüyor
  (3.1 v1.0 kilit, 3.2-3.13 sıradaki turlarda, tüm bölüm bitince
  tek dosya olarak commit edilecek)
- Aşama 2 Bölüm 4-8 (bekliyor)
- Aşama 3: Data Ownership & API Contracts (henüz başlamadı)
- Roadmap (Aşama 2 sonrası yazılacak)

## Karar setleri
Her bölümün karar tablosu kendi dokümanı içindedir. Pointer:

- **A1-A29** — [Aşama 1 Topology v1.1](ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md)
- **B1-B20** — [Aşama 2 Bölüm 1 Identity v1.0](ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY_v1_0.md)
- **B21-B44** — [Aşama 2 Bölüm 2 Permissions v1.0](ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS_v1_0.md)
- **C1-C12** (devam ediyor) — Aşama 2 Bölüm 3.1 Auth Boundary, kilit
  (full dosya Bölüm 3 sonu)

## Çakışma kuralı
Bu klasördeki dokümanlar diğer her şeyin üstündedir.
/decisions/, kök seviye eski planlama dosyaları (ELL_RULES,
ELL_ROADMAP, ELL_GLOSSARY, ELL_FEATURE_INSPIRATION) ile
çakışma durumunda buradaki master karar geçerlidir.
