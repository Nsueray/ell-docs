# ELL Mimari — Aşama 2, Bölüm 3.2: Credential ve Password Lifecycle

**Sürüm:** v0.1 — Draft (mimari Claude'un ilk çıkardığı)
**Durum:** Review bekliyor — paralel ChatGPT + Sentez Claude review'a hazır
**Ön koşul:** Aşama 1 v1.1, Bölüm 1 v1.0, Bölüm 2 v1.0, **Bölüm 3.1 v1.0 (kilit)**
**Bu draft kapsamı:** Sadece **3.2 Credential ve password lifecycle**. Önceki başlık 3.1 v1.0 kilit; sonraki başlıklar (3.3-3.13) ayrı turlarda.

---

## 3.2 Credential ve password lifecycle

### 3.2.1 Bu bölümün kapsamı

3.1 actor matrix'i kurdu. Bu bölüm **User actor'ın credential lifecycle**'ını detaylar: password set, change, forgot/reset, force reset, ve brute-force koruması.

**Kapsam:** Sadece User actor. Service actor credential'ları 3.6'da, Contractor token'ları Bölüm 1 1.5'te zaten tanımlı, Bot identity 3.11'de WhatsApp opt-in flow olarak ele alınır.

**Kapsam dışı (sonraki bölümlere):**
- Session lifecycle, refresh token rotation, logout (3.3, 3.5).
- JWT payload, `auth_version` field detayı (3.4).
- Cache invalidation sonrası password değişikliği etkisi (3.7).
- 2FA/MFA, SSO/OAuth (Phase 2).

### 3.2.2 Password policy

**NIST 800-63B yaklaşımı.** Karmaşıklık kuralları (büyük/küçük/sayı/sembol zorunluluğu) modern güvenlik literatüründe **terk edilmiş**; uzunluk + breached password check daha etkili.

**MVP kuralları:**

1. **Minimum uzunluk:** 12 karakter.
2. **Maksimum uzunluk:** 128 karakter (DoS koruması).
3. **Karmaşıklık zorunluluğu yok.** Passphrase ("correct horse battery staple" tarzı) kabul edilir.
4. **Yasaklı password'ler:**
   - User'ın `email` veya `full_name`'ini içeren password (case-insensitive substring match).
   - Bilinen weak password listesi (örn. "password", "123456789012", "qwertyuiopasdf").
5. **Breached password check** (Phase 2 işareti): HaveIBeenPwned API veya equivalent ile karşılaştırma. MVP'de yok; gerekirse Phase 2'de eklenir.

**Password hashing:**

- **Algorithm:** Argon2id (memory-hard, modern). Alternatif: bcrypt (cost ≥12), eğer Argon2id deployment'ta zor olursa.
- Salt: per-password random salt (algorithm built-in).
- `users.password_hash` text field içeriği: full algorithm + parameters + salt + hash (örn. PHC string format).
- **Pepper:** Uygulama seviyesinde pepper kullanılmaz (key rotation karmaşıklığı yarattığı için). Bunun yerine secret manager'da güvenli storage + DB encryption at rest.

**Enforcement noktaları:**

Password policy şu noktaların hepsinde uygulanır:
- Initial password set (admin tarafından create user sırasında, eğer admin password set ediyorsa).
- "Set password" email link ile user kendi yaratırken.
- Password change.
- Password reset confirm.

Policy ihlali endpoint'te 400 + standart hata mesajı ("Password does not meet requirements", spesifik kural hangisi olduğunu UI'da gösterir).

### 3.2.3 Password lifecycle flow'ları

Beş ayrı flow. Her birinin ayrı endpoint'i + ayrı authorization gereği var.

#### 3.2.3.1 Initial password set (yeni user yaratılırken)

**İki alt-akış:**

**(a) Admin set ile:**
- `manage_users` permission'lı user yeni user yaratır, geçici bir password set eder.
- `users.password_hash = hash(geçici_password)`, `users.password_must_change = true`, `users.password_set_at = now()`.
- Geçici password güvenli kanal üzerinden iletilir (UI'da bir defa gösterilir + audit log + iletildikten sonra UI'dan silinir).
- User ilk login'de `password_must_change` flag'i nedeniyle change endpoint'ine yönlendirilir.

**(b) Set password email link ile:**
- Admin user yaratır, password set etmez. `users.password_hash = NULL`, `users.password_must_change = true`.
- Sistem "set password" reset token yaratır (aşağıdaki reset token mekanizması ile aynı pattern).
- Email link'le user kendi password'ünü set eder (reset confirm endpoint'i aynı endpoint, ilk set durumu için de çalışır).

**Audit log:** User create event'i + initial password set method (`admin_set` veya `email_link`).

#### 3.2.3.2 Password change (authenticated User actor — kendi password'ü)

**Endpoint:** `POST /auth/password/change` (authenticated).

**Authorization:**
- **Matrix dışı endpoint** (Bölüm 2 B32 istisnası — user kendi password'ünü değiştirebilir).
- Authorize check: `actor.id == target.id` (target implicit, header'daki JWT'den gelir).
- Başka user'ın password'ünü change etmek için bu endpoint kullanılmaz — `force_password_reset` permission gerekir (3.2.3.4).

**Request body:**
- `current_password`: mevcut password (re-authentication için).
- `new_password`: yeni password.

**Akış:**
1. `current_password` doğrulanır (hash karşılaştırma). Yanlışsa 401 + `failed_login_count` artırılır (brute-force koruması bu endpoint'te de aktif).
2. `new_password` policy validation'dan geçer (3.2.2). İhlal varsa 400.
3. `new_password != current_password` kontrolü (UX guard, opsiyonel — aynı password kabul edilirse warning).
4. `users.password_hash = hash(new_password)`, `users.password_set_at = now()`, `users.password_must_change = false`.
5. **Aktif session etkisi:** Tüm refresh token'lar revoke edilir, `auth_version` bump tetiklenir (detay 3.3 + 3.7). Access token'lar max 15 dk'da expire. User'ın diğer cihazlarındaki oturumları kapanır; mevcut cihazına yeni token verilir.
6. Audit log: `actor_type = 'user'`, `actor_id = X`, `event = 'password_changed'`.

**Reason zorunluluğu:** Yok (kendi password'ü, B12 reason listesi force reset için).

#### 3.2.3.3 Password forgot/reset (anonymous, user başlatır)

İki endpoint:

**(a) `POST /auth/reset-password/request` (anonymous)**

**Request body:** `email`.

**Akış:**
1. **Rate limiting** (IP-based + email-based). CAPTCHA invocation eşiği aşılırsa CAPTCHA challenge.
2. `users` tablosunda email lookup. **Sonuçtan bağımsız aynı response** (3.1 C7 — email enumeration koruması): hem var olan hem var olmayan email için 200 + "If an account exists for this email, a reset link has been sent."
3. Eğer user var ve `is_active = true`:
   - Yeni reset token yaratılır (3.2.4 schema).
   - Önceki aktif reset token varsa revoke edilir (race condition koruması — sadece son istek geçerli).
   - Plain reset token email link'inde gönderilir (örn. `https://app.elanfairs.com/reset-password?token={plain}`).
   - Plain token DB'de saklanmaz; sadece `HMAC-SHA256(plain, server_secret_v[N]) + hash_key_version` saklanır (Bölüm 1 B4 pattern aynısı).
4. Eğer user yok veya `is_active = false`: hiçbir email gönderilmez ama response aynı kalır.
5. Audit log: rate-limited security event (3.1.4.2 webhook pattern'i — saldırı senaryosunda audit şişmesi engellenir). Başarılı reset request `users.id` üzerinden audit'lenir, başarısız (email yok) ise sadece security log.

**(b) `POST /auth/reset-password/confirm` (anonymous)**

**Request body:** `token` (plain, email link'ten), `new_password`.

**Akış:**
1. Submitted token `HMAC-SHA256(token, server_secret_v[matching_version])` ile hash'lenir, `password_reset_tokens.token_hash` ile karşılaştırılır.
2. Token bulunamadıysa: 400 ("Invalid or expired token"). Specifically "not found" denmez (token enumeration koruması).
3. Token bulundu ama `expires_at < now()`: 400 ("Invalid or expired token").
4. Token bulundu ama `used_at IS NOT NULL` (tek kullanımlık ihlali): 400 ("Invalid or expired token").
5. Token bulundu ama bağlı user `is_active = false`: 400 ("Invalid or expired token").
6. `new_password` policy validation'dan geçer. İhlal varsa 400.
7. Atomic transaction:
   - `users.password_hash = hash(new_password)`, `password_set_at = now()`, `password_must_change = false`.
   - `users.failed_login_count = 0`, `users.locked_until = NULL` (başarılı reset lock'u kaldırır — 3.2.5 detayı).
   - `password_reset_tokens.used_at = now()`.
   - Diğer tüm aktif reset token'lar revoke edilir.
   - Tüm refresh token'lar revoke edilir.
   - `auth_version` bump (3.7).
8. Audit log: `event = 'password_reset_completed'`, `actor_type = 'user'`, `actor_id = X`. Reset method (`user_initiated`).

**Initial password set durumu:**

`users.password_hash = NULL` user için reset confirm endpoint'i ilk password set'i için de çalışır. Sadece tek farkı: initial set'te `current_password` kontrolü yok zaten.

#### 3.2.3.4 Force password reset (admin, başkasının password'ü)

**Endpoint:** `POST /auth/password/force-reset` (authenticated, `force_password_reset` permission).

**Authorization (B21 order):**
1. Action classification: `('__global__', 'force_password_reset')`, `scope_mode = 'global_capability'`, `reason_required = true`.
2. Self-matrix-edit değil (matrix değişikliği değil) — skip.
3. Self-target kontrolü: `actor.id ≠ target.id` zorunlu. Eşitse 400 ("Use change-password endpoint for your own password"). User kendi password'ünü change endpoint'i ile değiştirir.
4. Owner bypass (eğer Owner ve owner_bypass_exempt değilse): authorize OK.
5. Non-owner: matrix lookup (`force_password_reset` permission).
6. Reason field zorunlu — body'de yoksa 400.

**Request body:**
- `target_user_id`: hedef user.
- `reason`: zorunlu, audit log'a yazılır.
- `delivery_method`: enum (`email_link` veya `temporary_password`).
  - `email_link`: sistem reset token yaratır, email gönderir (user normal forgot flow ile devam eder).
  - `temporary_password`: admin geçici password set eder, UI'da bir defa gösterilir, user'a güvenli kanal ile iletilir.

**Akış:**
1. Yetki + reason check (yukarıda).
2. Atomic transaction:
   - `users.password_must_change = true` (her iki delivery method için).
   - `delivery_method = 'temporary_password'` ise: `users.password_hash = hash(temp_password)`, `password_set_at = now()`. Temp password admin UI'da bir defa gösterilir.
   - `delivery_method = 'email_link'` ise: sistem yeni reset token yaratır + email gönderir; `users.password_hash` dokunulmaz (eski hash kalır ama `password_must_change = true` nedeniyle kullanılamaz).
   - Tüm aktif reset token'lar revoke edilir (sadece yeni token geçerli).
   - **Tüm refresh token'lar revoke edilir.**
   - **`auth_version` bump** (force reset target session'larını anında kapatır — 3.7'de critical security change propagation).
   - `users.failed_login_count = 0`, `locked_until = NULL` (lock kaldırılır).
3. Audit log: `event = 'password_force_reset'`, `actor_type = 'user'`, `actor_id = admin`, `target_user_id = X`, `reason`, `delivery_method`. Audit-worthy (kesin).
4. **Notification:** Target user'a email "Your password has been reset by an administrator. Please log in and set a new password." (security awareness — kullanıcı haberdar olur).

**Critical kural:** Force reset Owner statüsünü değiştirmez. Owner password'ü force reset edilse bile `is_owner` flag korunur. Last active Owner invariant force reset'i tetiklemez (sadece deactivate/hard delete/revoke_is_owner için geçerli — Bölüm 1 B10).

#### 3.2.3.5 Password expire / rotation policy

**MVP'de yok.** Periodic password change zorunluluğu NIST 800-63B önerisinde **terk edilmiş** — kullanıcılar zayıf, predictable değişiklikler yapıyor.

Phase 2 işareti: eğer compliance gerekliliği çıkarsa (örn. PCI DSS, ISO 27001) policy-based expire eklenir.

### 3.2.4 `password_reset_tokens` schema

```sql
CREATE TABLE password_reset_tokens (
  id                          uuid PRIMARY KEY,
  user_id                     uuid NOT NULL REFERENCES users(id),
  
  token_hash                  text NOT NULL UNIQUE,            -- HMAC-SHA256(token, server_secret_vN)
  hash_key_version            text NOT NULL,                   -- "v1", "v2", ...
  
  purpose                     text NOT NULL                    -- 'user_initiated' | 'admin_force_reset' | 'initial_set'
                              CHECK (purpose IN ('user_initiated','admin_force_reset','initial_set')),
  
  issued_at                   timestamptz NOT NULL DEFAULT now(),
  issued_by                   uuid REFERENCES users(id),       -- user_initiated için NULL olabilir, admin_force_reset için NOT NULL
  issued_by_actor_type        text NOT NULL DEFAULT 'user'
                              CHECK (issued_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  expires_at                  timestamptz NOT NULL,
  
  used_at                     timestamptz,
  
  revoked_at                  timestamptz,
  revoked_by                  uuid REFERENCES users(id),
  revoked_by_actor_type       text
                              CHECK (revoked_by_actor_type IS NULL OR revoked_by_actor_type IN ('user','system','migration','zoho_sync')),
  revocation_reason           text,
  
  CHECK (expires_at > issued_at),
  
  CHECK (
    (used_at IS NULL OR used_at >= issued_at)
  ),
  
  CHECK (
    (revoked_at IS NULL AND revoked_by IS NULL AND revocation_reason IS NULL)
    OR (revoked_at IS NOT NULL AND revocation_reason IS NOT NULL)
  ),
  
  -- Actor pattern Bölüm 1 ile tutarlı
  CHECK (
    (issued_by_actor_type = 'user' AND issued_by IS NOT NULL)
    OR (issued_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    revoked_by_actor_type IS NULL
    OR (revoked_by_actor_type = 'user' AND revoked_by IS NOT NULL)
    OR (revoked_by_actor_type IN ('system','migration','zoho_sync'))
  )
);

CREATE INDEX password_reset_tokens_user_active
  ON password_reset_tokens (user_id)
  WHERE used_at IS NULL AND revoked_at IS NULL AND expires_at > now();
```

**Notlar:**

- **Token storage:** Plain token DB'de saklanmaz — sadece HMAC hash. Bölüm 1 B4 pattern aynısı.
- **`purpose` field'ı:** Token'ın hangi flow'dan yaratıldığını audit edebilmek için. `user_initiated` (forgot password), `admin_force_reset` (force_password_reset endpoint'inden), `initial_set` (user create sırasında set password email link).
- **`expires_at`:** Default 1 saat. Initial set token için 7 gün olabilir (admin user yarattı, user link'i kontrol etmek için zamana ihtiyaç duyabilir). Purpose'a göre TTL deployment config.
- **`used_at`:** Tek kullanımlık enforcement. NOT NULL ise token tekrar kullanılamaz.
- **Revocation:** Yeni token yaratıldığında veya force reset/change sonrası eski token'lar revoke edilir. `revocation_reason` zorunlu.
- **Partial unique index:** Aynı user için aktif (kullanılmamış + iptal edilmemiş + süresi dolmamış) birden fazla token olabilir mi? Hayır — yeni request öncekini revoke eder (3.2.3.3 (a) adım 3). Ama schema-level UNIQUE constraint koymak yerine application-layer disiplin yeterli (race condition'da kısa süreli iki aktif token olabilir, sonuncusu kazanır).
- **Index `WHERE` filter:** Aktif token'ları hızlı sorgulamak için.

**Token leak koruması (Bölüm 1 B20 referansı):**

Reset link email içinde gider — email gönderim sırasında Referrer-Policy + meta tag pattern uygulanamaz (email client'ın kontrolü dışı). Bunun yerine:
- Email link short-lived (1 saat).
- Tek kullanımlık.
- Email içeriği plain text + HTML olarak gönderilir; HTML versiyonunda link sadece "Reset Password" buton metnine bağlı (URL açıkça görünür ama Referrer-Policy email client davranışına bağlı).
- Reset confirm endpoint kendi HTTP response'unda Referrer-Policy header set eder (sonraki sayfa geçişlerinde token URL'inin başka site'a leak'ini engeller).

### 3.2.5 Brute-force koruması

**Kullanılan field'lar (Bölüm 1 1.3.1):**
- `users.failed_login_count` (integer, default 0)
- `users.locked_until` (timestamptz, nullable)

**Login flow brute-force davranışı:**

1. Login attempt'inde:
   - Email lookup. Yoksa: standart 401 ("Invalid credentials"). User enumeration koruması — "user not found" denmez.
   - User varsa: `locked_until > now()` ise: 401 ("Invalid credentials"). Lock durumu kullanıcıya specifically söylenmez (email enumeration sızıntısı + saldırgan'a bilgi vermez).
   - User varsa, lock yoksa: password verify.
2. Password yanlış:
   - `failed_login_count++`.
   - Threshold aşıldıysa (örn. 5 başarısız attempt): `locked_until = now() + lock_duration`.
   - Lock duration eskalasyonu (opsiyonel — Phase 2): ilk lock 5 dk, ikinci 30 dk, üçüncü 24 saat. MVP'de sabit 15 dk yeterli.
   - 401 response (locked durumla aynı mesaj — sızıntı yok).
3. Password doğru:
   - `failed_login_count = 0`, `locked_until = NULL`.
   - `last_login_at = now()`.
   - Token yaratılır, response döner.

**Threshold + lock parameters (deployment config, mimari karar değil):**
- `BRUTE_FORCE_THRESHOLD`: default 5.
- `LOCK_DURATION`: default 15 dakika.
- `LOCK_ESCALATION`: Phase 2.

**Lock'tan çıkış yolları:**

1. **Otomatik:** `locked_until` zamanı geçince. User retry yapabilir.
2. **Başarılı password reset:** Reset confirm `failed_login_count = 0`, `locked_until = NULL` set eder. Lock'u atlatma yolu (kullanıcı şifresini hatırlamıyorsa).
3. **Force password reset (admin):** Admin tarafından da lock kalkar.
4. **Manual unlock (admin):** `manage_users` permission'lı user başkasının lock'unu manuel kaldırabilir. Endpoint: `POST /auth/account/unlock`. Reason zorunlu (audit). MVP'de bu endpoint olmayabilir — reset zaten lock'u kaldırıyor.

**IP-based throttling (account-based throttling'in üstünde ek katman):**

- IP-based rate limit login + reset request endpoint'lerinde.
- Threshold deployment config (örn. 30 attempt / dakika / IP).
- CAPTCHA invocation eşiği (örn. 10 attempt / dakika / IP).
- Bir IP'den çok başarısız attempt → security log + threshold alert (3.1.4.2 pattern).

**Audit log:**

- Başarılı login: audit log (`event = 'login_success'`).
- Başarısız login: **bireysel audit log yazılmaz** (brute-force senaryosunda şişer). Bunun yerine:
  - `users.failed_login_count` field'ı tracking yapar.
  - Lock event'i (`failed_login_count` threshold aşımı sonucu) audit log'a yazılır (`event = 'account_locked'`).
  - IP-based rate limit aşımları security log kanalına (rate-limited threshold alert).
- Manual unlock: audit log (`event = 'account_unlocked'`, reason, actor).

### 3.2.6 Aktif session etkisi — password change/reset/force-reset

Üç aksiyon da **aktif tüm session'ları sonlandırır**. Mekanizma 3.3 (refresh token) + 3.4 (JWT) + 3.7 (cache invalidation) detayında:

1. **Refresh token revoke:** User'ın tüm aktif refresh token'ları DB'de revoke edilir. Sonraki refresh attempt'leri başarısız olur.
2. **`auth_version` bump:** User-level `auth_version` artırılır. JWT payload'undaki `auth_version` ile DB'deki current `auth_version` uyuşmazsa access token reddedilir (max 15 dk geçici stale window — kabul edilebilir trade-off).
3. **Audit log:** Session termination event'leri (`event = 'session_terminated'`, reason = `password_changed` veya `password_reset` veya `force_reset`).

**Mevcut cihaz etkisi:**

- **Password change endpoint:** Aktif session'lardan biri bu endpoint'i çağırdı. Yeni token (access + refresh) response'da verilir → mevcut cihaz sorunsuz devam eder. Diğer cihazlar logout olur.
- **Password reset confirm:** Reset email link'ine tıklayan cihaz — login değildir (anonymous endpoint). Reset sonrası user re-login zorunda. Tüm cihazlar logout olur.
- **Force password reset:** Target user kendisi bu endpoint'i çağırmadı (admin çağırdı). Tüm cihazlardaki session'ları kapanır. Target user bir sonraki request'inde 401 alır, re-login akışına yönlendirilir.

**Mimari amaç:** Password değişimi credential rotation event'idir. Eski credential'a güvenen tüm session'lar otomatik invalidate olmalı.

### 3.2.7 Edge cases ve validation kuralları

**(a) Reset token race condition:**
- User aynı anda iki reset request yaptı (örn. iki tab'da).
- İkinci request birinciyi revoke eder. Sadece son token geçerli.
- User ilk email'deki link'e tıklarsa 400 ("Invalid or expired token"). İkincisindekine tıklarsa OK.

**(b) Account deactivated + password operations:**
- `users.is_active = false` user için:
  - Login: standart 401 (sızıntı yok).
  - Reset request: aynı 200 response (email enumeration koruması), ama email gönderilmez.
  - Reset confirm: token bulunsa bile (deactivate öncesi alınmış) 400 (`is_active = false` kontrolü).
  - Password change: bu endpoint authenticated, deactive user zaten login olamaz.
  - Force reset: hedef deactive user için anlamsız. Backend reddedebilir veya kabul edebilir; MVP'de **reddet** (`is_active = true` kontrolü, daha temiz).

**(c) Owner kendi password reset:**
- Normal flow çalışır. Owner kısıtlaması yok.
- Owner statüsü password reset'ten etkilenmez (`is_owner` flag korunur).
- Last active Owner invariant tetiklenmez (sadece deactivate/hard delete/revoke için).

**(d) Force reset edilen user'ın `password_must_change` etkisi:**
- Force reset sonrası `password_must_change = true`.
- User login olduğunda (yeni temp password ile veya email link sonrası), normal flow `password_must_change = true` kontrolü yapar:
  - Login successful + flag true → response'da JWT verilir ama UI user'ı password change endpoint'ine yönlendirir.
  - Password change endpoint'i `password_must_change = false` set eder.
  - Diğer endpoint'lere erişim — middleware `password_must_change = true` ise sadece /auth/password/change ve /auth/logout endpoint'lerine izin verir, diğer business endpoint'leri 403 ile reddeder.

**(e) Email change ile reset link ilişkisi:**
- Email change flow ayrı (3.10'a not — düşünme yapılacak).
- Bekleyen reset token email değişikliğinden etkilenmez (token user_id'ye bağlı, email'e değil).
- Ama yeni reset request her zaman güncel `users.email`'e gider.

**(f) Aynı password kabul edilir mi?**
- MVP'de password history tutulmuyor. Aynı password technically kabul edilir.
- UX guard: change endpoint'inde `current_password == new_password` ise warning. Reset endpoint'inde geçmiş password bilinmediği için kontrol edilmez.
- Phase 2 işareti: password history (örn. son 5 password) — compliance gerekliliği çıkarsa.

### 3.2.8 Audit log gereklilikleri

Kesin audit-worthy (Bölüm 5 sınıflandırma kararı bekliyor ama bu liste minimum):

| Event | Detay |
|---|---|
| `password_set_initial` | actor, target, method (admin_set/email_link) |
| `password_changed` | actor (=target), method (`self_change`) |
| `password_reset_requested` | target user (sadece var olan ve aktif user için) |
| `password_reset_completed` | target user, method (`user_initiated`) |
| `password_force_reset` | actor, target, reason, delivery_method |
| `account_locked` | target user, threshold reason (sayı bilgisi içerebilir) |
| `account_unlocked` | actor (sistem otomatik veya admin manual), target, method |
| `login_success` | user_id, IP, user_agent |

**Audit-NOT-worthy (security log + rate-limited threshold alert):**
- Bireysel başarısız login attempt'leri.
- Reset request rate limit aşımı.
- IP-based throttling tetiklemeleri.

**Reason field zorunluluğu (Bölüm 2 2.7.2 liste 13 — `force_password_reset`):**
- Force reset endpoint'inde reason body parameter zorunlu, audit log'a yazılır.

### 3.2.9 Bu alt bölümün kararları

| ID | Karar |
|---|---|
| **C13** | **Password lifecycle yalnızca User actor için.** Service actor service credential (3.6), Contractor token (Bölüm 1 1.5), Bot identity (3.11 opt-in flow). Password yönetimi 5 flow: (a) initial password set (admin set veya email link), (b) password change (kendi, authenticated, matrix dışı endpoint), (c) password forgot/reset (anonymous, email-based reset token), (d) force password reset (admin, `force_password_reset` permission), (e) password expire/rotation Phase 2. |
| **C14** | **NIST 800-63B password policy.** Minimum 12 karakter, maksimum 128. Karmaşıklık zorunluluğu yok (passphrase kabul). Yasaklı: user'ın email/full_name'ini içeren password, bilinen weak password listesi. Breached password check (HaveIBeenPwned) Phase 2. Hashing **Argon2id** (memory-hard); alternatif bcrypt cost ≥12. Pepper yok (key rotation karmaşıklığı; bunun yerine secret manager + encryption at rest). Policy initial set + change + reset confirm noktalarında enforce. |
| **C15** | **`password_reset_tokens` schema Bölüm 1 B4 pattern'ı aynısı:** HMAC-SHA256(token, server_secret_vN) + `hash_key_version` ile saklanır. Plain token DB'de yok. `purpose` field'ı (`user_initiated` / `admin_force_reset` / `initial_set`) audit ayrımı sağlar. Default TTL 1 saat (initial_set için 7 gün). Tek kullanımlık (`used_at` enforcement). Race condition'da yeni request öncekini revoke eder. `issued_by_actor_type` Bölüm 1 actor pattern ile tutarlı. |
| **C16** | **Password change endpoint matrix dışı** (Bölüm 2 B32 istisnası — user kendi password'ünü değiştirebilir). `current_password` re-authentication zorunlu. Policy validation. **Aktif session etkisi:** tüm refresh token revoke + `auth_version` bump + mevcut cihaza yeni token. Diğer cihazlar logout. |
| **C17** | **Password reset request endpoint email existence sızdırmaz** (C7 + 3.1 disiplin devamı). Hem var olan hem var olmayan email için aynı 200 response. Var olan ve aktif user için reset token yaratılır, önceki revoke edilir, email gönderilir. Var olmayan/deactive için response aynı ama email gönderilmez. Audit log var olan user için tutulur; var olmayan attempt security log + rate-limited threshold alert. Reset confirm endpoint başarılı reset'te `failed_login_count = 0`, `locked_until = NULL` set eder (lock'u atlatma yolu). |
| **C18** | **Force password reset (`force_password_reset` permission):** Registry'de `('__global__', 'force_password_reset')`, `scope_mode = 'global_capability'`, `reason_required = true`, default Owner only. **Self-target yasak** (`actor.id ≠ target.id` zorunlu — kendi password için change endpoint kullanılır). Reason body zorunlu, audit log'a yazılır. Delivery method enum: `email_link` veya `temporary_password`. **Atomic transaction:** `password_must_change = true` + (temp_password set veya reset token yaratım) + tüm refresh token revoke + `auth_version` bump + lock kaldır. **Target user'a notification email** (security awareness). Force reset Owner statüsünü değiştirmez; last active Owner invariant'ı tetiklemez. |
| **C19** | **Brute-force koruması iki katman:** (a) **Account-based** — `users.failed_login_count` + `locked_until` (Bölüm 1 1.3.1 field'ları). Threshold (default 5) aşımında lock (default 15 dakika). Lock duration eskalasyonu Phase 2. Lock çıkış: otomatik TTL, başarılı reset, force reset, admin manual unlock. (b) **IP-based** — login + reset request endpoint'lerinde IP rate limit + CAPTCHA invocation eşiği. IP threshold aşımı security log + threshold alert. **Bireysel başarısız login audit log'a yazılmaz** (brute-force senaryosunda şişer); `failed_login_count` field tracking yapar, lock event'i audit'lenir. Login response'da lock durumu specifically söylenmez (email enumeration + saldırgan info sızıntısı koruması). |
| **C20** | **Password değişikliği (change / reset confirm / force reset) sonrası aktif session etkisi:** Üç aksiyon da tüm refresh token'ları revoke eder + user-level `auth_version` bump tetikler. JWT payload `auth_version` ile DB current uyuşmazsa access token reddedilir (max 15 dk geçici stale window kabul edilir trade-off). Mekanizma 3.3 (refresh token revoke) + 3.4 (JWT auth_version) + 3.7 (cache invalidation propagation) detayında. Mimari amaç: password değişimi credential rotation event'idir; eski credential'a güvenen tüm session'lar otomatik invalidate olur. |
| **C21** | **`password_must_change = true` flag enforcement:** Login successful + flag true → JWT verilir ama middleware sadece `/auth/password/change` ve `/auth/logout` endpoint'lerine erişim verir, diğer business endpoint'leri 403. Flag user kendi password'ünü change endpoint'inde değiştirince `false` olur. Flag set'i: initial password set (otomatik), force password reset (otomatik), explicit admin set (yok — MVP'de gerekmez). |

### 3.2.10 Açık kalan (sonraki başlıklara)

- Refresh token schema, rotation, reuse detection → 3.3.
- JWT payload field detayı (`auth_version`, `permission_version`, `scope_version`, `aud`, `kid`) → 3.4.
- `auth_version` bump mekanizması (DB update + cache propagation atomic mi?) → 3.7.
- Cache invalidation timing (max 15 dk stale access token kabul edilebilir mi farklı kategorilerde?) → 3.7.
- Email change flow ve mevcut reset token'larla etkileşim → 3.10.
- 2FA / MFA → Phase 2.
- SSO / OAuth → Phase 2.
- Password breach check (HaveIBeenPwned) → Phase 2.
- Password history (compliance gerekliliği çıkarsa son N password tekrar yasağı) → Phase 2.
- Lock duration eskalasyonu (ilk lock 5 dk, ikinci 30 dk, üçüncü 24 saat) → Phase 2.
- IP-based rate limit + CAPTCHA invocation eşik değerleri → deployment config, mimari karar değil.
- Manual unlock endpoint (MVP'de gerekmez, reset zaten lock kaldırıyor) → Phase 2 veya operasyonel ihtiyaç.
- Audit-worthy classification full liste → Bölüm 5.

---

## 3.2 Bölüm özeti

Password lifecycle yalnızca User actor için. Beş flow: initial set (admin set veya email link), change (kendi, authenticated, matrix dışı), forgot/reset (anonymous, email-based token), force reset (admin, `force_password_reset` permission, reason zorunlu, self-target yasak), expire/rotation Phase 2. NIST 800-63B yaklaşımı: minimum 12 karakter, karmaşıklık zorunluluğu yok, email/full_name içeren reddedilir, breached check Phase 2. Hashing Argon2id (alternatif bcrypt ≥12). `password_reset_tokens` schema Bölüm 1 B4 pattern'ı aynısı (HMAC-SHA256 + hash_key_version, plain token DB'de yok). Email existence sızdırmaz, lock'u atlatma yolu olarak başarılı reset `failed_login_count` ve `locked_until` sıfırlar. Brute-force koruması iki katman: account-based (`failed_login_count` + `locked_until`, threshold 5, lock 15 dk default), IP-based (rate limit + CAPTCHA eşiği). Bireysel başarısız login audit'lenmez (şişme); lock event'i audit'lenir. Password değişikliği credential rotation event'i — tüm refresh token revoke + `auth_version` bump + diğer cihazlar logout. Force reset Owner statüsünü değiştirmez, last active Owner invariant'ı tetiklemez. `password_must_change = true` flag enforcement: sadece password change + logout endpoint'lerine erişim. Aktif session etkisi mekanizması 3.3 + 3.4 + 3.7'de detaylanır.

---

**Bu 3.2 v0.1 draft'ı. Self-review prep + bağımsız draft. Review için hazır.**

Self-review sonrası mimari Claude'un kendi yakaladığı potansiyel mayınlar:
- `actor.id ≠ target.id` force reset için (kendi password için change endpoint)
- `password_must_change = true` middleware enforcement
- Reset confirm'da lock kaldırma (lock'u atlatma yolu)
- Race condition reset token revoke (son request kazanır)
- Owner password reset'in Owner invariant'ı tetiklememesi
- Email enumeration koruması her endpoint'te (request, login, locked durum)

Tahmin: bu drafta 8-15 review patch'i gelir (Bölüm 1+2'ye göre daha az çünkü self-review aktif).
