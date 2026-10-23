# archive/design — ELIZA tasarım seti (tarihsel)

- **Ne:** UX çıktısı ELIZA tasarım seti (Claude Design, Eyl 2026; 45 HTML). Kaynak: Suer'in Mac'i,
  `~/Downloads/Eliza Platform new ui design/`. Alındığı gün: 2026-10-23 (Sentez UI-0b).
- **Durum:** TARİHSEL. Renk / yazı / boşluk kaynağı artık LEENA `public/ui2/styles/tokens.css` (kütük UI-04).
  Buradaki `styles/signal.css` + `styles/themes.css`, LEENA'ya UI-0 öncesi girmiş kopyalarla bayt bayt aynıdır.
- **Brief:** `../../ELIZA_DESIGN_BRIEF_v1.md` (ell-docs kökü; başında §8 sapma notu, UI-05).
- **Alınan (42 dosya):** 35 HTML (kök 20 · `themes/` 12 · `warm/` 3) · `styles/` 4 CSS · `design-canvas.jsx` ·
  `screenshots/thumb-a-dash.png`, `screenshots/thumb-b-dash.png`. Her dosyanın sha256'sı kaynakla aynı.
- **Alınmayan — sır/kişisel veri taraması bulgusu (12 dosya):**
  - e-posta / telefon taşıyan 6 HTML: `A - Login`, `B - Login`, `Login` (gerçek kişi adından türemiş şirket
    e-postası) · `Sales - Companies` (4 e-posta + 4 telefon) · `Ops - Visitor & Access` (13 e-posta) ·
    `Sales - Quotes` (2 e-posta).
  - LEENA ziyaretçi kayıtlarındaki gerçek bir tam adla eşleşen kişi adı taşıyan 4 HTML (2 ad): `Finance - Commissions`,
    `Mobile - Dashboard`, `Mobile - Scan`, `Mobile - Visitor List` (`Ops - Visitor & Access` da bu gruptadır).
  - Aynı e-postayı gösteren 2 ekran görüntüsü: `screenshots/thumb-a-login.png`, `screenshots/thumb-b-login.png`.
- **Alınmayan — hiçbir dosyanın yüklemediği:** 4 ekran görüntüsü (`hub-a`, `hub-b`, `hub-verify`, `warm-compare`),
  `.DS_Store`, `.thumbnail`, `uploads/` (brief'in aynı kopyası).
- **Sonuç:** bazı sayfalardaki bağlantılar alınmayan sayfalara gider (ör. `ELIZA Directions.html` → Login), bu beklenir.
- **Kalan kişi adları:** 4 HTML'de 14 satır (`Finance - Contract`, `Ops - Exhibitor Detail`, `Sales - My Work`,
  `Sales - Pipeline`) — LEENA çalışan / kullanıcı / organizatör / ziyaretçi kayıtlarında ve ell-docs'ta eşleşmesi 0
  (2026-10-23, salt-okunur ölçüm) → kurgusal kabul edildi. Ayrıntı: defter [2026-10-23 UI-0b HÜKÜMLERİ].
