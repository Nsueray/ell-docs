# ELL Documentation

ELL Platformu'nun tek-ev (source-of-truth) dokümantasyon repo'su.

## Canlı belgeler (4)

| dosya | rol |
|---|---|
| [ELL_DURUM_DEFTERI_v2.md](./ELL_DURUM_DEFTERI_v2.md) | Tek durum kaydı — ne canlı, hangi commit, sıradaki adım |
| [ELL_YOL_HARITASI_v5.md](./ELL_YOL_HARITASI_v5.md) | Pusula — faz sırası + her fazda geçerli ilkeler |
| [ELL_BILGI_MIMARISI_v4.md](./ELL_BILGI_MIMARISI_v4.md) | Bilgi mimarisi — hangi varlık hangi sistemde/DB'de, sahiplik (v4: §4.1 ui2 Finance alt menüsü; v3 tarihsel) |
| [ELL_GLOSSARY.md](./ELL_GLOSSARY.md) | Kanonik terimler (ELIZA/LIFFY/LEENA, 2 DB) |

## Referans belgeler

| dosya | ne |
|---|---|
| [ELAN_EXPO_REQUIREMENTS_v1_0.md](./ELAN_EXPO_REQUIREMENTS_v1_0.md) | Kanonik ihtiyaç dokümanı (ne lazım) |
| [ELL_LOCKED_KARARLAR_OZET.md](./ELL_LOCKED_KARARLAR_OZET.md) | Kilitli mimari kararlar — uyum kontrol listesi |
| [ELIZA_UI2_ARAYUZ_KURALLARI_v1.md](./ELIZA_UI2_ARAYUZ_KURALLARI_v1.md) | ui2 arayüz kuralları (UI-01..06) + UI-0 kabul ölçütleri |
| [ELL_FAZ_B_RUNBOOK_v1.md](./ELL_FAZ_B_RUNBOOK_v1.md) | Faz B başı adım tarifi: Anthropic anahtarı + LIFFY JWT_SECRET (ölçüm + adımlar, sır değeri yok) |
| [ELIZA_DESIGN_BRIEF_v1.md](./ELIZA_DESIGN_BRIEF_v1.md) | Ürün tasarım brief'i (Claude Design için, Eyl 2026); başında §8 sapma notu (UI-05) |
| [ELL_TEK_KAYNAK_KILIT.md](./ELL_TEK_KAYNAK_KILIT.md) | Tek-kaynak ilkesi (kilitli, 2026-06-20) |
| [ELL_MIMARI_v1.0_KONSOLIDE.md](./ELL_MIMARI_v1.0_KONSOLIDE.md) | Konsolide mimari (mimari fazı çıktısı) |
| [ELL_FEATURE_INSPIRATION.md](./ELL_FEATURE_INSPIRATION.md) | Özellik fikir/ilham |
| [HANDOVER_BRIEF.md](./HANDOVER_BRIEF.md) | Implementation fazı devir brifingi |

## archive/

Yürürlükte olmayan tarihsel belgeler. Okunmaz, silinmez — referans için korunur.
Mimari faz kanıt belgeleri (gap analizi, üç derin analiz, cross-DB ölçümü, gerçek durum, oturum özeti, FAZ0) da burada — yol haritasının dayandığı ölçümler.
`archive/design/` — ELIZA tasarım setinin (UX çıktısı, 45 HTML) taramadan geçen kısmı; tarihsel, kaynak artık LEENA `ui2/styles/tokens.css` (ayrıntı: `archive/design/README.md`).

## Çakışma kuralı

Çelişkide **ELL_DURUM_DEFTERI_v2.md** kazanır (durum/ilerleme); faz sırası ve ilkelerde **ELL_YOL_HARITASI_v5.md** kazanır.
