# ELIZA ui2 — Arayüz Kuralları v1

> **Bu nedir:** ui2 (ELIZA arayüzü, LEENA `public/ui2/`) için arayüz kuralları ve UI-0 paketinin kabul
> ölçütleri. Kaynak: **Sentez, 22 Eki 2026 — UI-0 kriter turu** (metin aşağıda AYNEN).
> **Kütük indeksi:** `ELL_LOCKED_KARARLAR_OZET.md` → "UI — arayüz" grubu (UI-01..06). ID tahsisi yalnız kütükte.
> **Bilgi mimarisi karşılığı:** `ELL_BILGI_MIMARISI_v4.md` §4 (Finance alt menü eşlemesi).
> **Çelişkide DEFTER kazanır** (`ELL_DURUM_DEFTERI_v2.md`). Bu belge durum tutmaz; ne yapıldığı defterdedir.
> Atıf: [defter:2026-10-22 UI-0 KRİTERLERİ].

---

## 1. Kurallar (Sentez hükümleri — aynen)

**UI-01 YERLEŞİM:** üst sekme BM §1'den, alt menü §2/3/4 bölümlerinden türetilir. Bölümde yeri
olmayan ekran = IA değişikliği → önce BM yaması, sonra ekran. Finance alt menüsü §4 gruplarıyla
kümelenir: Executive (özet) · Contracts (kontratlar, komisyonlar, agent'lar) · Money (hesaplar,
ekstre, transferler, giderler, tedarikçiler, gider TASLAKLARI) · Expo Finance (bütçe).

**UI-02 NAV TEK KAYNAK:** nav.json (id · domain · grup · etiket · yol · durum canlı|yer-tutucu ·
permission kodu); shell.js yalnız okur. Rol alanı BOŞ DEĞİL: Paket 2'nin permission koduna
bağlanır (ui2CanSee etkin yetkiyi okur, P2-3). Test iki yönlü: nav'daki her yol var + ui2'deki
her sayfa nav'da; "6 öğe" sayı testi silinir.

**UI-03 DÖRT ŞABLON:** Liste · Detay · Form · Özet kartları (tek stat-card, tıklayınca kayda iner —
D2'nin ekran karşılığı). Bileşenler YALNIZ components.js'ten; test bunu sınar. "Para çifti"
(işlem birimi + EUR) ayrı bileşen, Finance'ta zorunlu (RAP-01 ekran karşılığı).

**UI-04 TOKENS:** tek tokens.css (renk/yazı/boşluk), tema html[data-theme]; sayfalarda sabit hex
YASAK (grep ile ölçülür, kabul ölçütü).

**UI-05 NİHAİ ARAYÜZ:** giydirme ŞİMDİ, düz HTML/JS, derleme yok (K-G). React/Next (brief §8)
ERTELENDİ; yeniden tartı tetiği: Sales alanının (LIFFY) ui2'ye taşınma kararı.

**UI-06 ORGANIZER ANA PANELİ:** ui2'de YENİ sayfa olacak — UI-0 DIŞINDA (UI-1 adayı). UI-0 asgarisi:
ui2 girişi → Finance özet; Sales/Operations sekmeleri boş-durum ekranı, ölü link değil.

**AÇIK SORULAR — KAPANDI:** taslaklar = gider taslakları → Money · Intelligence ui2'de YOK ·
Commissions & Agents → Contracts grubu, ui2 ikizi yok (UI-1 adayı).

---

## 2. UI-0 paketi — kapsam (Sentez, aynen)

**İNŞA (UI-0 kapsamı):**
- tokens.css: tek dosya (renk/yazı/boşluk), tema html[data-theme]; sayfalarda sabit hex YASAK.
- components.js: UI-03 bileşenleri — Liste · Detay · Form · Özet kartı (stat-card, tıklayınca
  kayda iner) · "para çifti" (işlem birimi + EUR, Finance'ta zorunlu). Bileşen YALNIZ buradan;
  sayfada kopya bileşen = test kırmızı.
- nav.json (id · domain · grup · etiket · yol · durum canlı|yer-tutucu · permission kodu);
  shell.js yalnız okur; ui2CanSee etkin yetkiyi okur (P2-3). Finance alt menü 4 grup:
  Executive (özet) · Contracts (kontratlar, komisyonlar, agent'lar) · Money (hesaplar, ekstre,
  transferler, giderler, tedarikçiler, gider taslakları) · Expo Finance (bütçe). Test iki yönlü:
  nav'daki her yol var + ui2'deki her sayfa nav'da; "6 öğe" sayı testi silinir.
- /ui2/_sablon/: dört şablon, sahte veri, üç durum (boş/yükleniyor/hata).
- Giriş → Finance özet. Sales/Operations sekmeleri boş-durum ekranı (ölü link değil).
- Mevcut TÜM ui2 sayfaları (Paket 2'ninkiler dahil) şablon + tokens'a taşınır; API sözleşmesi
  ve rakamlar DEĞİŞMEZ (K-G): contract 4 €342.00, özet toplamları taşıma öncesiyle birebir —
  taşıma öncesi/sonrası ekran görüntüsü + DOM metin karşılaştırması testle.
- Düz HTML/JS, derleme YOK (UI-05). Yeni stil dosyası yalnız tokens.css.

**KAPSAM DIŞI:** tema değiştirici · yeni Finance sayfası · organizer paneli (UI-06, UI-1 adayı) ·
rol/yetki mantığı (yalnız okunur) · EMS sayfaları.

**ORTAK:** migration YOK (UI işi) · testler yeşile kadar (TABAN dahil) · kütük UI grubu · tek defter
kaydı "PAKET UI-0: STAGING'E HAZIR".

---

## 3. UI-0 kabul ölçütleri (staging, Suer bakar — Sentez, aynen)

1. giriş → Finance özet
2. alt menü nav.json'dan, 4 grup, tüm sayfalar açılır, 404 yok
3. dört şablon üç durumuyla (/ui2/_sablon/)
4. ui2'de sabit hex 0 (grep)
5. Sales/Operations boş-durum
6. Liste şablonu 390px'te yatay kaydırmaz
7. nav testi iki yönlü + bileşen-kopya testi yeşil
8. Finance rakamları birebir (c4 342.00)

---

## 4. Sapma notu — ELIZA_DESIGN_BRIEF_v1.md

Sentez paketi brief'in başına 3 satırlık sapma notu istedi (§8 React/Next ertelendi, UI-05).
**ell-docs'ta BULAMADIM** (2026-10-22, `grep -rln` + dosya adı araması). Not bu yüzden brief'e değil
buraya yazıldı; brief ell-docs'a girdiğinde başına aynı not eklenir:

> ⚠️ Sapma (2026-10-22, Sentez UI-05): §8'deki React/Next yönü ERTELENDİ — ui2 düz HTML/JS, derleme
> yok. Yeniden tartı tetiği: Sales alanının (LIFFY) ui2'ye taşınma kararı. Kaynak:
> `ELIZA_UI2_ARAYUZ_KURALLARI_v1.md` UI-05.

---

## 5. Uygulama notu (UI-0 inşası, LEENA `1ad8456` — kural DEĞİL, eşleme)

- **nav.json alan adları** (kod İngilizce): id · domain · `group` (grup) · `label` (etiket) · `path` (yol) ·
  `status` = `live` | `placeholder` (canlı | yer-tutucu) · `permission` (Paket 2 kodu, 044 kayıt defteri).
  Ek alanlar: `parent` (alt sayfa — menüde ayrı satır değil, ebeveyni etkin yapar: ekstre → Accounts) ·
  `legacy` (yer-tutucunun bugünkü klasik ekranı) · üst düzey `landing` (giriş alanı = finance) · domain `userOnly`
  (Admin). `domain: "shell"` = menüde görünmeyen kabuk / giriş / şablon sayfaları (iki yönlü testin "her sayfa nav'da" ayağı).
- **Dosyalar:** `public/ui2/styles/tokens.css` (tek token dosyası; sabit renk yalnız burada) · `styles/signal.css`
  (bileşen stilleri; ledger.css birleşti, themes.css tokens.css'e girdi) · `components.js` (bileşenler) · `nav.json` ·
  `shell.js` (yalnız okur; üst çubuk + alt menü işaretlemesi) · `placeholder.html` · `_sablon/` (dizin + 4 şablon).
- **Sabit hex ölçümü** (kabul 4), repo kökünden:
  `find backend/leena-v401-backend/public/ui2 -type f ! -name tokens.css -exec grep -oE '#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?([0-9a-fA-F]{2})?\b' {} + | wc -l` → 0.
- **Testler:** `tests/test_ui2_ui0.js` (iki yönlü nav · bileşen-kopya · hex · token · şablonlar · para çifti · giriş) ·
  `tests/test_ui2_ui0_render.js` (API rakamı = ekran rakamı, TABAN) · `tests/ui0_compare.js` (tarayıcı, önce/sonra; zincir dışı).
- **Para çifti istisnası:** EUR karşılığı API'de OLMAYAN tutar tek birimli `money` ile gösterilir (kalem birim fiyatı ·
  ekstre dönem giriş/çıkış toplamı · taslak tutarı); yürüyen bakiye hesap biriminde (LED-11). Liste testte sabit.
