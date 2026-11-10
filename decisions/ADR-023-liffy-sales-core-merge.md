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
>
> **Kesim maddesi TEYİT (Sentez 5 Kas, karar 2 — B1-b, LEENA `c5ad2ee`):** "Teklif/AF dizisi LIFFY'nin son numarasının üstüne
> alınır" maddesi geçerli. LEENA dizisi kiracı başına sayaç satırıdır (`quote_sequences.last_value`, ilk numara 200000; biçim
> `Q<ofis ISO>-<dizi>`, AF = Q → A). Kesim adımı (migration zincirinden sonra, LIFFY kapanmadan önce, provada ölçülür):
> `UPDATE quote_sequences SET last_value = GREATEST(last_value, <LIFFY quote_af_seq son değeri>)` — LEENA'da o ana kadar açılmış
> numara varsa GREATEST onu korur. LIFFY tarihçesi LEENA `quotes` tablosuna taşınırsa kimlik uuid olduğundan çakışmaz (karar 3).

> **Kesim maddeleri (Sentez 5 Kas, Prompt 1b karar 5 = a + Prompt 2 REF-01 — CC, LEENA `b67b9fc`):**
> - **LIFFY tarihçesi içeri alınırsa eşleme:** iç yolda doğan kontratlarda `contracts.sales_owner_user_id` ve `company_id` (LIFFY soft-ref
>   uuid'leri) BOŞ kalır; sahip `source_quote_id → quotes.owner_user_id` ile türetilir (D2). LIFFY teklif tarihçesi LEENA `quotes`'a
>   taşınırsa: LIFFY kullanıcı → LEENA `users` (e-posta eşleşmesi, tekil olmayan elle) ve LIFFY firma adı → LEENA `companies` eşlemesi
>   kesim tasarımının ayrı adımıdır; eşleşmeyen satır sayacı mutabakata girer (RAP-02).
> - **ELIZA `core_*` kopyası kesimde EMEKLİ (REF-01):** referans verinin kanonik kaynağı LEENA tablolarıdır (`core_countries` ·
>   `core_sectors` · `languages` · `currencies` · `product_categories` · gider / gelir kategorileri). eliza-legacy'nin core_* kopyaları
>   kesimden sonra okunmaz (Paket 6 kapatma ile birlikte). Not: ADR-005 (ELIZA write policy) zaten SUPERSEDED; ADR-016 core_* ile
>   ilgisizdir (kampanya alıcı tamamlama) — Sentez'in "ADR-005/016" atfı 🔶 olarak soruldu.
>
> **Kesim maddesi (Suer 6 Kas — 061 ve büyük `email_queue`):** 061 `email_queue`'ya iki NULLABLE kolon (`reply_to`,
> `attachment_document_id` + `quote_documents` FK) ekler. Canlıda tablo büyük (Suer: ~570k satır / ~16 GB — bu turda canlı
> boyut CC tarafından ÖLÇÜLMEDİ). Staging ölçümü (6 Kas, salt okuma): 570.815 satır · toplam 3.123 MB (heap 115 MB; gerisi TOAST
> `html_content`) · FK `convalidated = true` · 059-061 tek runner işleminde (süre ölçülmedi). Kesimde: ADD COLUMN nullable (yalnız
> katalog) + FK doğrulama taraması (heap üzerinden; tablo kilidi ShareRowExclusive — worker yazımını o süre bekletir) süresi PROVADA
> ölçülür; uzunsa FK `NOT VALID` eklenir, `VALIDATE CONSTRAINT` ayrı adımda (kilit daha hafif) koşulur. Karar provada.
> **Teyit (Sentez 6 Kas, Prompt 3 KESİM NOTU):** provada süre ölçülür; **> 60 sn ise** FK `NOT VALID` + `VALIDATE CONSTRAINT` ayrı adım.
> **Prova raporunda ZORUNLU satır:** "061 `email_queue` FK süresi: … sn (karar: tek adım | NOT VALID + VALIDATE)".
>
> **Kesim maddesi (Sentez 6 Kas, Prompt 3 karar 3 = a):** klasik (organizer token'lı) giriş kullanıcıları kesimde ui2 girişine (`users`)
> geçer (SEM-05). Kesim tasarımına adım: **"klasik token'lı kullanıcı listesi + geçiş günü"** — kesimden önce canlıda klasik girişle
> çalışan kişilerin listesi (ad · e-posta · kullandığı ekranlar), her biri için `users` daveti + şablon, ve geçiş günü (o günden sonra
> klasik giriş yalnız EMS köprüsü — YET-02). Liste provada çıkarılır.
>
> **Karar 6 cevabı (Sentez 6 Kas):** core_* emekliliği yalnız **ADR-005**'i ilgilendirir; ADR-016'ya DOKUNULMAZ. "ADR-005/016" ifadesi
> Sentez hatasıydı (ölçülmeden ELIZA chat'ten alındı). Yukarıdaki maddedeki 🔶 kapandı.
>
> **Kesim notu (Prompt 3 — 062 / 063, CC, 6 Kas):** 062 yalnız kayıt defteri + sistem şablonu SATIRI ekler (veri değiştirmez). 063
> `email_queue`'ya `from_name text` (NULLABLE, varsayılansız, FK'sız → yalnız katalog; tarama yok) ekler; `quotes` / `contracts` /
> `accounts` / `offices`'e NULLABLE FK kolonları (yeni kolon tamamen NULL → doğrulama taraması tablo boyutunca, `email_queue`'ya FK YOK).
> Canlı `contracts` boyutu bu turda ölçülmedi (staging 3.934 satır).

>
> **Kesim maddeleri (Sentez 10 Kas — GUV, olay GUV-01; CC, eliza-next):**
> - **GUV-04 erişim logu + giriş kilidi (069) — kesim ÖNCESİ dilim, zincirle canlıya:** `access_log` · `auth_failures` · `security_events` (+2 tetikleyici)
>   + `security.read` (şablonsuz → Owner). 069 YALNIZ yeni tablo / tetikleyici / kayıt defteri satırı ekler; mevcut satıra dokunmaz (tarama yok). Yazım
>   web süreci içinde asenkron (log hatası isteği düşürmez); saklama (90 gün) + bildirimler `leena-email-worker`'da (worker `main`'den gelir → kesim
>   push'uyla başlar). Kesim günü env: `SECURITY_ALERT_EMAILS` worker servisinde (G34; tanımsızsa aktif Owner'lar alır). Yük ve büyüme PROVA-1
>   raporunda (canlı kopyadan).
> - **`JWT_SECRET` yenileme (kesim günü, Suer):** klasik organizer token'ı DB'ye bakılmadan doğrulanır → 17 Eyl–kesim arasında verilmiş her token (dış
>   hesap dahil, GUV-01) süresi dolana kadar (30 gün) geçerli kalır. Kesimde `JWT_SECRET` yenilenir → tüm oturumlar kapanır, herkes yeniden girer
>   (ui2 davetleri zaten kesim günü listesinde). Abonelikten çıkış imzası JWT'den bağımsız (SEM-07) → gönderilmiş e-postalardaki çıkış linkleri bozulmaz.
>   Faz A'da (21 Eki) bir kez yapıldı; aynı yol.
> - **GUV-02:** eliza-next'te `POST /api/auth/register` KALDIRILDI (404); canlıda hotfix 4'ün 403'ü kesime kadar kalır (SAPMA, defter). Yeni kiracı
>   yalnız Owner davetiyle (Admin › Organizations).
