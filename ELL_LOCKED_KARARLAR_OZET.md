# ELL — Kilitli Mimari Kararlar (Özet)

> **Bu nedir:** ELL mimari fazında kilitlenmiş kararların tek-satırlık özeti.
> Detaylı enforcement mekanizması ve karmaşık metin BİLEREK çıkarıldı — burada
> sadece "ne karara bağlandı" var. Amaç: köprü/prototip önerileri üretirken bu
> kilitli kararlarla çelişme. Çelişen bir şey önereceksen "bu kilitli karara
> aykırı" diye açıkça işaretle.
>
> **Not:** Bunlar implementasyon reçetesi DEĞİL. Basit, kanıtlı, prototip-temelli
> çalışmaya devam et. Bu liste sadece bir uyum kontrol listesi.

---

## Identity Modeli (Bölüm 1 — kilitli)

- **B1** — Schema'da tek isim `organization_id` (LIFFY'nin `organizer_id`'si emekli).
- **B2** — Üç ayrı identity tablosu: `users`, `sales_agents`, `data_entry_contractors`. Ortak parent tablo yok.
- **B3** — `sales_agents.user_id` nullable + UNIQUE (bazı agent'lar system user değil).
- **B4** — Data entry contractor token'ı ayrı tabloda, HMAC-SHA256 hash + key rotation desteği.
- **B5** — Üç entity için lifecycle: **deactivate default, hard delete istisna** (Owner + ikinci onaylayıcı).
- **B6** — Deactivation entity-spesifik: user → login kapanır + direct report'lar yeni manager'a reassign; agent → yeni attribution'da seçilemez ama eski kayıt bozulmaz; contractor → token revoke.
- **B7** — LEENA legacy login migration: cutover'da ilk Owner user yaratılır, password_must_change.
- **B8** — `organizers` → `organizations` tablosu (multi-tenant root). API key/secret'lar ayrı `integration_credentials` tablosunda, plain text yasak, LEENA/LIFFY secret izole.
- **B9** — `display_role` sadece görüntü; **authorization'da kullanılmaz**. Yetki = permission matrix + scope + `is_owner` flag.
- **B10** — Owner statüsü `users.is_owner` flag'i. Aktif Owner sayısı 1'in altına inemez; self-grant yasak.
- **B11** — Sales agent / contractor yaratma **permission-bazlı**, kişi-bazlı değil.
- **B12** — Tüm kritik aksiyonlarda reason field zorunlu (deactivate, delete, token revoke, password reset, is_owner revoke).
- **B13** — Sales agent banka/IBAN bilgisi ayrı tabloda, `view_sensitive_finance` permission'ıyla korunur, encrypted.
- **B14** — Phone formatı E.164 tek string. WhatsApp opt-in + verified_at.
- **B15** — Serbest metin (`notes`) alanları audit edilir (event log).
- **B16** — `*_by_actor_type` pattern: kayıtların kim/ne tarafından yaratıldığı/güncellendiği tutarlı tutulur.
- **B17** — Cross-DB referanslar logical reference (gerçek FK yok); orphan'lar tespit/rapor/manuel onarım.
- **B18** — Yüzde alanlarında schema-level range CHECK (0–100).
- **B19** — Cross-organization tutarlılık application-layer'da doğrulanır (MVP); UUID global.
- **B20** — Public form token leak koruması (Referrer-Policy + token maskeleme).

---

## Permission / Yetki Modeli (Bölüm 2 — kilitli)

**EN ÖNEMLİ — prototipteki permission tartışmasıyla doğrudan ilgili:**

- **Yetki modeli ilişkisel `user_permissions` matrix tablosudur — serbest-form JSONB DEĞİL.** LIFFY prototipindeki ölü `permissions` JSONB kolonu hedef mimaride bir yere taşınmıyor; ELL'e geçişte matrix'e dönüşüp atılır. Şimdi ne canlandır ne sil.
- **Field-level visibility gerçek bir ihtiyaç** (requirements 2.2 + 3.1). Örn. `view_sensitive_finance` field-level gate. "Granüler izin yok / over-engineering" çıkarımı YANLIŞ — sadece prototip henüz implement etmemiş.

Diğer kararlar:

- **B21** — Authorization sırası: action classification → self-matrix-edit check → Owner bypass → matrix lookup → scope check → reason → audit.
- **B22/B23** — Permission registry tek key formatı `(module, action)`. Global/protected permission'lar sentinel namespace'lerde.
- **B24** — Protected system operations matrix dışı, kod-level invariant.
- **B25** — **Owner bypass yalnızca authorization'ı bypass eder; business validation (same-org, finance invariant, state machine vb.) Owner için de çalışır.**
- **B27/B28** — Sistem template'leri immutable + silinemez; custom template'ler düzenlenebilir.
- **B30** — `user_permissions` matrix granular; template apply default olarak istisnaları korur.
- **B32** — **Hiçbir kullanıcı kendi permission matrix'ini düzenleyemez (Owner dahil).** İstisnalar ayrı endpoint'ler: password, notification prefs, dil, timezone, display_name, telefon.
- **B33** — Hierarchy enforcement (`reports_to`): self/descendant/cross-org/inactive yasak. Owner için `reports_to = NULL`.
- **B34/B38** — Scope composition module-specific resolver pattern (her modül kendi read + create kuralını sağlar).
- **B35** — **Contract resolver Aşama 3 prerequisite:** explicit ownership alanları (`sales_owner_user_id` vb.) tanımlanmadan implement edilmez.
- **B40** — LIFFY matrix sync: yetki daraltma → anında; yetki genişletme → polling kabul.
- **B42** — `view_sensitive_finance` field-level gate; `export_data` / `send_marketing_campaign` iki aşamalı (capability + target scope) authorization.

---

## Görünürlük kuralı (prototip sorusunun cevabı, kilitli kararlarla uyumlu)

Rep kendi + altının verisini görür; yönetici altının hepsini görür; Owner her şeyi
görür. `reports_to` hiyerarşisiyle. (Requirements 2.2 + 2.8, Bölüm 2 B33 ile uyumlu.)

---

## Açık / hizalanmamış nokta

- **Faz vs Aşama takvimi:** v4 roadmap "Faz", mimari dokümanlar "Aşama" kullanıyor.
  Permission matrix mimaride **zaten tasarlanmış/kilitli** (Bölüm 2), implementasyonu
  sonraya bırakılmış. v4'teki "Faz 4" referansıyla mimarideki "Aşama 3" implementasyon
  zamanlaması henüz birebir hizalanmadı — bir karar gerekirse Sentez chat'e taşınır.
