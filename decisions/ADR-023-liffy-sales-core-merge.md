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
>
> **Kesim maddeleri (Sentez 11 Kas — UI-ÖNCE fazı, PAKET UI-TAM; CC, eliza-next):**
> - **070 + Y5 + YET-25 canlı davranışı kesimde DEĞİŞTİRİR:** (a) Project şablonu `contracts.read` (all) alır — Project kullanıcıları kontratları
>   görür (komisyon bölümü gizli kalır, ödeme yazamaz). (b) EMS / ziyaretçi uçları iç kullanıcıdan `operations.read` ister
>   (`middleware/emsGate.js`, `index.js` bağlamaları): kesimden sonra ui2 hesabıyla klasik EMS ekranlarını açan **Finance · Sales · Sales Operations**
>   şablonlu kullanıcı 409 alır — EMS kullanacak kişiye Project / Office Manager şablonu ya da `operations.read` ezmesi kesim günü davet listesinde
>   verilir. **Klasik organizer token'ı ETKİLENMEZ** (kanıt: `tests/test_ui_tam_access.js` G3 — kapılı uç kapısız ikiziyle aynı durum + aynı gövde;
>   G4 — anahtar / kimliksiz / bozuk token yolları aynen) → paylaşılan klasik hesap ve terminal akışı kesimde değişmeden çalışır.
>   070 yalnız 1 kayıt defteri satırı + 1 şablon satırı + `users.ui_theme` kolonu ekler (NULLABLE, varsayılansız — tablo taraması yok).
> - **Prototip katmanı kesimden ÖNCE kalkar:** `/design-preview/` bağlaması (`index.js`) + `design-preview/` dizini + ui2 kapı sayfası + `nav.json`
>   `topbar` öğesi faz sonunda silinir; kesim provası listesine "prototip yok" denetimi (canlıya gitmez — Sentez 11 Kas Y3).
>
> **Kesim maddeleri (Sentez 11 Kas — PAKET UI-TAM-2 + EK-1; CC, eliza-next):**
> - **Exhibitor e-posta zinciri VARSAYILAN KAPALI (kütük EXH-16 — EK-1 madde 2):** otomatik gönderim fuar başına AÇIKÇA açılır; migration hiçbir fuar /
>   kontrat için zincir başlatmaz; planlı tarihi geçmiş satır kendiliğinden gitmez (Send now + önizleme). Kesimde göçmüş fuar / kontratlara toplu
>   e-posta GİTMEZ; zincirin hangi fuarda açılacağı kesim günü listesine fuar fuar yazılır.
> - **071 + 072 (1. parça):** 071 yetkiyi DEĞİŞTİRİR — EMS / ziyaretçi uçlarında YAZMA artık `operations.write` ister (Project · Office Manager şablonlarında
>   var); kesimden sonra yalnız `operations.read` ezmesi verilmiş bir ui2 kullanıcısı EMS'te yazamaz (kesim günü davet listesinde yazacak kişiye şablon ya
>   da `operations.write` ezmesi). **Klasik organizer token'ı ve terminal akışı ETKİLENMEZ** (kanıt: `tests/test_ui_tam2.js` Y2 — kapılı uç kapısız ikiziyle
>   aynı durum + aynı gövde; `tests/test_ui_tam_access.js` G3 / G4). 072 yalnız şema ekler: `contracts`'a 4 NULLABLE, varsayılansız kolon (tablo taraması yok)
>   + yeni tablolar + iki referans tohumu; hiçbir fuar için anahtar / kural / zincir yaratmaz.
> - **Exhibitor Page (2. parça; 073):** (a) **sayfa anahtarı sırrı** — canlıda İLK anahtar doğmadan ayrı ortam değişkeni tanımlanır (yoksa oturum sırrından türer;
>   sır sonradan değişirse bütün linkler ölür); (b) **tıklama izleme** — exhibitor e-postalarında KAPALI olmalı (izleme linki sayfa anahtarını üçüncü tarafa taşır;
>   izleme linkinin adres parçasını koruyup korumadığı ÖLÇÜLMEDİ); (c) **dosya saklama** — exhibitor dosyaları veritabanında (tek dosya 15 MB · kontrat 150 MB);
>   tahmini büyüme yılda ~3–4 GB, tavanla ~45 GB → kesimden önce disk / saklama kararı; (d) **rozet formu** — her fuar için exhibitor rozet formu Expo settings'te
>   elle bağlanır (073 hiçbir fuara bağlamaz); bağlanmamış fuarda Badges bölümü kapalıdır; (e) canlıda echo bayrağı YOK → rozet QR e-postası klasik akışla gerçekten
>   gider, sistem e-postaları worker'la gider; (f) 073 yalnız NULLABLE bir kolon ekler.
> - **Sipariş + Payment (3. parça; 074):** (a) **sipariş kapıları** — extra equipment siparişi çekirdeğin kapılarından geçer: fuar SATIŞA AÇIK olmalı, ana kontratın
>   ofisi çözülmeli, bölge izin vermeli; kesimde satışa açılmayan fuarın exhibitor'ı sayfadan sipariş veremez; (b) **team kaydı** — aktif "team" temsilci kaydı ve
>   varsayılan oranı canlıda VAR olmalı (yoksa sipariş kapalı); (c) **banka bloğu** — Payment bölümü kontratın tüzel kişisinin "belgede göster" hesabını gösterir;
>   tüzel kişisi / belge hesabı olmayan kontratta banka görünmez (göçmüş kontratların tüzel kişi doluluğu kesimde ölçülür); (d) **kod** — canlıda echo bayrağı
>   yok: kod yalnız e-postayla gider → worker + gönderen doğrulaması şart; (e) 074 convert günlüğünün iki kısıtını genişletir (yeni adlar "v2"), satır değiştirmez.
> - **Zincir (5. parça; migration yok):** (a) **tik worker'da** — canlıda zinciri e-posta worker'ı işletir (5 dakikada bir; aralık worker ortamından
>   ayarlanır); anahtarı açık fuar yokken hiçbir şey yapmaz. Staging'deki süreç içi tik canlıda YOK (echo koşuluna bağlı). (b) **açılış sırası** — bir fuarın
>   zinciri, o fuarın kontratları göçtükten SONRA açılır: açılıştan önce doğmuş kontratların vadesi geçmiş satırları kendiliğinden gitmez (kişi "Send now" +
>   önizleme); açılıştan SONRA doğan kontratın e-postaları hemen gider — göç, zinciri açık bir fuara yapılırsa göçen her kontrata Welcome çıkar. (c) **gönderen
>   kutuları** — Project ve Finance kutularının canlıda gönderen doğrulaması (ILT-07); Payment Reminder Finance kutusundan gider. (d) **metinler** — yerleşik
>   metinler kodla gelir, kesimde tohum adımı YOK; metinler gözden geçirilmedi (EN uyarlama · FR; TR ve Build-up FR yok) → zincir açılmadan önce okunmalı.
>   (e) "Stuck" artık zincir Failed / Blocked'ı sayar: alıcı e-postası olmayan (göç) kontratlar ve ayarı eksik fuarların exhibitor'ları Stuck görünür.
> - **Pavyon (6. parça; migration yok):** göçmüş kontratlarda pavyon modu BOŞ, co-exhibitor kaydı YOK (Zoho'da karşılığı ölçülmedi) → pavyonlar kesimden
>   sonra elle işaretlenir, co-exhibitor'lar elle girilir. DIRECT'te eklenen co-exhibitor, zinciri AÇIK fuarda Welcome'ını kendiliğinden alır → pavyon girişi
>   zincir açılmadan önce ya da bunu bilerek yapılır.
> - Paketin diğer kesim maddeleri (worker · gönderen doğrulaması · sonraki migration'lar) parça kayıtlarıyla bu bloğa eklenir.
