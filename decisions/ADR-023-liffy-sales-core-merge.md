# ADR-023 — LIFFY satış çekirdeğinin LEENA'ya birleşmesi

Tarih: 2026-11-05 · Durum: KABUL (Suer; Sentez direktifi v3) · KB @ 02166e0

> **Ölçülen alanlar (CC, 5 Kas, Prompt 1):** LEENA `main` `5c4c34b` (canlı, donuk) · birleşme dalı `eliza-next` `8161678` (main'i
> içeren merge) → P4-KAPANIŞ `05bd86f` → B1-a `222ac41` · liffyv1 `10047ee` · liffy-ui `b78231b` · ell-docs taban `02166e0`.
> Envanter (`docs/audits/LIFFY_ENVANTER_2026-11-05.md`): LIFFY 36 canlı tablo (satış çekirdeği 7 · ortak 5 · madencilik-kampanya 24) ·
> 34 rota dosyası (satış çekirdeği 1: `quotes.js`, 31 uç) · 31 ekran (satış çekirdeği 2) · 3 kullanıcı · 3 teklif · son 90 günde
> kampanya 0, madencilik koşusu 0 · 80.855 kişi (taşınmaz).

Bağlam: 19 Haz 2026 kararı LIFFY'yi dış halka (satış/freelancer izolasyonu) olarak ayrı
DB + ayrı servis tutuyordu; LIFFY ↔ LEENA tek cross-DB sınırdı. Paket 3–4 sonunda köprü
(HMAC servis kimliği, outbox, convert_requests, fuar yayını) kuruldu ve maliyeti ölçüldü:
iki kimlik sistemi, iki katalog, iki yetki modeli, her yeni akış için yeni köprü.

Karar: LIFFY'nin satış çekirdeği (teklif, takip, e-posta alıp verme, kontrata çevirme,
katalog, müşteri/kişi) LEENA/ui2'ye taşınır. Madencilik, benzer firma bulma, kampanya
motoru, 80K kişi verisi bu adımda taşınmaz; LIFFY geçici madencilik/kampanya aracıdır.
Nihai kaderi envanter (LIFFY_ENVANTER) sonrası karar: içeri alınır ya da emekli edilir;
kalıcı olarak ayrı DB'de kalmaz, yeni köprü kurulmaz. Dış kullanıcı (freelancer, dış
acente) LEENA'ya girer: kapsam kendi/ekip/ofis/hepsi + finans görünmez — tek duvar budur,
testli (kriter: Sentez, B2).

Gerekçe: (a) e-posta itibarı ayrı uygulama/DB gerektirmez (tek uygulama, birden çok
SendGrid hesabı); (b) güven izolasyonu yetki matrisi + kapsamla sağlanır (B21–B42, YET);
(c) kod ayrılığı mimari gerekçe değildir.

Sonuçlar: çalışma biçimi YON-16 (staging-only; canlı donuk 5c4c34b; hotfix sınırı) ·
prompt planı: Prompt 1 = Paket 0 + B1 → Prompt 2 = B2 + B3 → Prompt 3 = Paket 5 →
kesim provası ×2 → kesim (kaba ufuk 4–6 hafta; B1 raporuyla düzeltilir) · DENEME-0
iptal; Elahe B1 kabul turuna katılır · tek giriş ve UI-1 ayrı iş olarak iptal ·
tasarım fazı kesimden sonra · SUPERSEDED: defter 19 Haz bloğu, yol haritası v5
§1.2–1.3, konsolide §1.1, bilgi mimarisi v3 LIFFY sahiplik satırları (v4'te
"kesime kadar") · köprü kodu kesime kadar durur, kesimde sökülür.

Kesim tasarımı (prova ile olgunlaşır): staging'i canlıdan tazele → prova → export
(YON-12) → merge → migration zinciri → ZOHO FARK PARTİSİ (4 Kas'tan kesime kadar
Zoho'ya girenler: yeni çekim + Paket 4 runner'ı artımlı koşu — SAPMA 14 tasarımı,
canlıda hiç koşulmadı, provada ölçülür; mutabakat) → deploy → doğrulama (TABAN'lar) →
LIFFY kapat. Teklif/AF dizisi LIFFY'nin son numarasının üstüne alınır. Geri alma:
Faz A restore + rollback.js. Prova ≥ 2 kez, canlının taze kopyasında.

> **Uygulama notu (CC, 5 Kas):** Prompt 1'in B1'i promptun kendi "SIĞMAZSA" kuralıyla bölündü — B1-a (katalog + müşteri) bu
> oturumda; B1b (teklif · send · sign · çevirme · kuyruk) Prompt 1b'de. LIFFY dizisinin canlı son değeri 100002 (envanter §8).
