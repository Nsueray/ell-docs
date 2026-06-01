# ELL Documentation

ELL Platformu'nun source-of-truth dokümantasyon repo'su.

Mimari fazı tamamlandı (2026-06-01). Ana referans:
[ELL_MIMARI_v1.0_KONSOLIDE.md](./ELL_MIMARI_v1.0_KONSOLIDE.md).
Detaylı mimari dokümanlar `archive/` altında referans olarak
korunuyor.

Implementation fazına geçiş notları için: [HANDOVER_BRIEF.md](./HANDOVER_BRIEF.md).

## Klasör yapısı

- `ELL_MIMARI_v1.0_KONSOLIDE.md` — **Konsolide mimari (kanonik)** — implementation'ın tek source of truth'u
- `archive/` — Detaylı mimari dokümanlar (Aşama 1 + Bölüm 1 + Bölüm 2 + legacy README)
- `/decisions/` — ADR'lar; bazıları banner'larla revize edilmesi
  gerektiği işaretli (bkz. INDEX.md)
- `/decisions/archived/` — Geçersiz kılınmış ADR'lar
- `/eliza/`, `/liffy/`, `/leena/` — Sistem-spesifik
  dokümantasyon

## Eski planlama dosyaları

`ELL_RULES.md`, `ELL_ROADMAP.md`, `ELL_GLOSSARY.md`, ve
`ELL_FEATURE_INSPIRATION.md` requirements gathering yapılmadan
önce yazıldı. Üst kısımlarındaki SUPERSEDED / NEEDS UPDATE /
CONTEXT UPDATE banner'larına dikkat. **Tarihsel referans** olarak görün.

## Çakışma kuralı

Eğer bir dokümanın söylediği başka bir dokümanla çakışıyorsa:

1. `ELL_MIMARI_v1.0_KONSOLIDE.md` her zaman geçerlidir
2. Sonra: `archive/` altındaki detay mimari dokümanları
3. Sonra: `ELAN_EXPO_REQUIREMENTS_v1_0.md` (kanonik ihtiyaç dokümanı)
4. Sonra: Aktif (banner'sız veya CONTEXT UPDATE'li) ADR'lar
5. SUPERSEDED işaretli dokümanlar artık geçerli değildir
