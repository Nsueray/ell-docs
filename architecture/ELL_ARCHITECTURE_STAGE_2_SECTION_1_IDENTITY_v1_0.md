# ELL Mimari — Aşama 2, Bölüm 1: Identity Model

**Sürüm:** v1.0 — Final
**Onaylanma tarihi:** 2026-05-12
**Onaylayan:** Suer (Owner)
**Durum:** ✅ Approved — locked
**Doküman türü:** Mimari karar — Aşama 2 Bölüm 1
**Ön koşul:** Aşama 1 v1.1 (kilitli, kanonik)
**Kapsam:** users, sales_agents, data_entry_contractors üçlemesinin schema modeli, lifecycle kuralları, organization aidiyeti, LEENA legacy login migration'ı, integration credentials izolasyonu, cross-organization tutarlılık disiplini.
**Kapsam dışı:** Permission matrix detayı (Bölüm 2), hierarchy mekaniği ve cycle enforcement (Bölüm 2), auth/JWT/session (Bölüm 3), reference data sync (Bölüm 4), audit log entity references (Bölüm 5).

**Bu doküman v1.0 olarak finalize edilmiştir. Aşama 2 sonraki bölümleri ve Aşama 3 bu dokümanı kanonik referans olarak kullanır. Bölüm 1'e dönüş ancak resmi bir amendment (v1.1) ile mümkündür; bu nadir bir durum olmalıdır.**

---

## 1.0 Bu bölümün amacı

Aşama 1 A28'de sales attribution üç kategori olarak çözüldü: sales rep (system user), sales agent (system user değil), Project department/Elan Expo (komisyonsuz). Aşama 1 ayrıca data entry contractor'ları "system user değil, attribution için var" olarak belirledi (D41 + requirements 3.2).

Bu bölüm o üç identity'yi **somut schema** ve **lifecycle kurallarına** bağlar. Her identity'nin kim olduğu, sisteme ne yaparken nasıl bağlandığı, ne zaman çıkarıldığı, ve nasıl korunduğu burada yazılır.

---

## 1.1 İsimlendirme kararı: `organization_id`

**Karar:** Schema'da tek tutarlı isim `organization_id`. `organizer_id` (LIFFY mevcut kullanım) terk edilir.

**Gerekçe:**
- "Organizer" kelimesi domain'de farklı bir anlam taşır — Elan Expo'nun *expo organizer* rolü vardır (fuar düzenleyicisi olarak). Tenant kavramı ile aynı kelimeyi paylaşırsa kavram karışıklığı doğar.
- "Organization" tenant kavramı için standart endüstri terminolojisi.
- LIFFY migration'ında `organizer_id` → `organization_id` rename'i mekanik bir iş (tek migration script).

**Pratik sonuç:**
- Tüm yeni tablolarda kolon adı `organization_id`.
- LIFFY rename migration'ı Aşama 2 implementation sırasında yapılır.
- LEENA'da yeni `organizations` tablosu LIFFY'nin eski `organizers` tablosunun yerini alır.

**Tek şirket bağlamı:** Bugün sadece "Elan Expo" var. Schema multi-tenant-ready kalır — her business entity `organization_id`'ye bağlı.

---

## 1.2 Üç entity, üç tablo — ortak parent yok

Üç tablo birbirinden bağımsız. Ortak `people` veya `parties` parent tablosu **yok**.

**Gerekçe:**
- Üçü gerçekten farklı dünyalar: user'ın email zorunlu (login için), sales_agent'ın opsiyonel (telefonla çalışan ajans), contractor'ın kalıcı kimliği opsiyonel.
- Ortak parent zorla benzerlik üretir (anlamsız NULL'lar) veya parent tablo neredeyse boş kalır.

İlişkiler tablolar arası referanslar ile kurulur, parent ile değil.

---

## 1.3 `users` tablosu

Sisteme login eden gerçek kişiler. Bugün ~25 aktif.

### 1.3.1 Schema

```sql
CREATE TABLE users (
  id                          uuid PRIMARY KEY,
  organization_id             uuid NOT NULL REFERENCES organizations(id),
  
  email                       citext NOT NULL,
  full_name                   text NOT NULL,
  display_name                text,
  
  phone_e164                  text,
  whatsapp_opt_in             boolean NOT NULL DEFAULT false,
  whatsapp_verified_at        timestamptz,
  
  preferred_language          text REFERENCES core_languages(code),
  timezone                    text NOT NULL DEFAULT 'Europe/Istanbul',
  
  password_hash               text,
  password_set_at             timestamptz,
  password_must_change        boolean NOT NULL DEFAULT false,
  
  reports_to                  uuid REFERENCES users(id),
  -- NOTE: cycle guard ve same-org check Bölüm 2'de hierarchy mekaniğinde enforce edilir.
  -- Kurallar: (a) self-report yasak, (b) descendant-report yasak,
  -- (c) reassignment cycle check zorunlu, (d) yeni manager aktif ve aynı organization'da.
  
  office_id                   uuid REFERENCES offices(id),
  
  profile_template_id         uuid REFERENCES permission_templates(id),
  profile_template_version    integer,
  
  display_role                text,                            -- display only
  
  is_owner                    boolean NOT NULL DEFAULT false,  -- protected sistem flag
  
  is_active                   boolean NOT NULL DEFAULT true,
  activated_at                timestamptz NOT NULL DEFAULT now(),
  deactivated_at              timestamptz,
  deactivated_by              uuid REFERENCES users(id),
  deactivated_by_actor_type   text,
  deactivation_reason         text,
  
  last_login_at               timestamptz,
  last_active_at              timestamptz,
  failed_login_count          integer NOT NULL DEFAULT 0,
  locked_until                timestamptz,
  
  created_at                  timestamptz NOT NULL DEFAULT now(),
  created_by                  uuid REFERENCES users(id),
  created_by_actor_type       text NOT NULL DEFAULT 'user'
                              CHECK (created_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  updated_at                  timestamptz NOT NULL DEFAULT now(),
  updated_by                  uuid REFERENCES users(id),
  updated_by_actor_type       text                              -- nullable until first update
                              CHECK (updated_by_actor_type IS NULL OR updated_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  UNIQUE (organization_id, email),
  
  CHECK (
    (is_active = true AND deactivated_at IS NULL)
    OR (is_active = false AND deactivated_at IS NOT NULL AND deactivation_reason IS NOT NULL)
  ),
  
  CHECK (
    (created_by_actor_type = 'user' AND created_by IS NOT NULL)
    OR (created_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    updated_by_actor_type IS NULL
    OR (updated_by_actor_type = 'user' AND updated_by IS NOT NULL)
    OR (updated_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    (deactivated_at IS NULL AND deactivated_by IS NULL AND deactivated_by_actor_type IS NULL)
    OR (
      deactivated_at IS NOT NULL
      AND (
        (deactivated_by_actor_type = 'user' AND deactivated_by IS NOT NULL)
        OR (deactivated_by_actor_type IN ('system','migration','zoho_sync'))
      )
    )
  ),
  
  CHECK (
    phone_e164 IS NULL
    OR phone_e164 ~ '^\+[1-9][0-9]{7,14}$'
  )
);

CREATE UNIQUE INDEX users_org_phone_e164_unique
  ON users (organization_id, phone_e164)
  WHERE phone_e164 IS NOT NULL;
```

**Notlar:**

- **`email` citext.** Case-insensitive native. Ek `email_normalized` field gerekmez.
- **`phone_e164`.** E.164 endüstri standardı: "+" + country code + national number, tek string. Schema-level regex validation. ISO 3166 ülke kodundan farklı, karıştırılmaz.
- **`whatsapp_opt_in` + `whatsapp_verified_at`.** Bot lookup şartı: `WHERE phone_e164 = ? AND whatsapp_opt_in = true AND whatsapp_verified_at IS NOT NULL`.
- **`password_hash` nullable.** SSO/OAuth ileride (Phase 2). MVP'de zorunlu.
- **`profile_template_id`, `profile_template_version`.** Yaratım anında snapshot. Detay Bölüm 2.
- **`display_role`.** Authorization kararlarında kullanılmaz (1.3.4).
- **`is_owner`.** Owner statüsünün korunan sistem invariant'ı. Profile template'ten bağımsız.
- **`*_by_actor_type` pattern.** `created_by_actor_type` NOT NULL (create anında zorunlu), `updated_by_actor_type` nullable (kayıt henüz update edilmediyse her ikisi de NULL), `deactivated_by_actor_type` nullable (deactivate olmamışsa NULL).

### 1.3.2 User lifecycle

**Create:**
- Yetki: `manage_users` special permission (default Owner profile; başkalarına delegasyon mümkün).
- Zorunlu: `organization_id`, `email`, `full_name`, `profile_template_id`, `reports_to` (is_owner=true user hariç).
- Password: admin geçici password oluşturur veya "set password" email tetiklenir. `password_must_change = true`.
- `updated_by`, `updated_by_actor_type` create anında NULL kalır; ilk update'te dolar.
- Audit log.

**Deactivate:**
- Yetki: `manage_users`. Reason zorunlu.
- **Direct report kontrolü (zorunlu reassignment):**
  - Deactivate edilmek istenen user'ın altında direct report'lar varsa, UI zorunlu manager reassignment yapar.
  - Reassignment olmadan deactivate backend tarafından reddedilir.
  - **İstisna:** `is_owner = true` user "geçici olarak boş bırak" seçeneği sunabilir (organizational debt explicit accept, audit'lenir).
  - Reassignment cycle check kapsamına girer (Bölüm 2).
- Etkiler (atomic transaction):
  1. Direct report'lar yeni manager'a re-attach edilir.
  2. `is_active = false`, deactivation alanları set edilir.
  3. Tüm aktif refresh token'lar revoke edilir (Bölüm 3).
  4. Aktif access token'lar bir sonraki expiry'de sonlanır (max 15 dk).
  5. **Historical attribution korunur.**
  6. **Bağlı sales_agent davranışı:** Yeni attribution dropdown filter'ı `users.is_active`'i de kontrol eder: `WHERE sales_agents.is_active = true AND (sales_agents.user_id IS NULL OR users.is_active = true)`. Eski contract'larda attribution değişmez.

**Reactivate:**
- Yetki: `manage_users`. Reason zorunlu.
- Password reset zorlanır.
- Permission matrix deactivation öncesi haliyle.

**Hard delete:**
- Default davranış **deactivate**.
- Hard delete sadece teknik hatalı kayıtlar için, çift onaylı.
- **Second approver kuralları (hepsi backend double-check):**
  1. Active user olmalı (`approver.is_active = true`).
  2. Aynı organization içinde olmalı (`approver.organization_id = target.organization_id`).
  3. `approve_hard_delete` protected special permission'a sahip olmalı.
  4. Requesting Owner ile farklı kişi olmalı (`approver.id ≠ requester.id`).
  5. Hard delete edilmek istenen target user ile farklı kişi olmalı (`approver.id ≠ target.id`).
  6. Hard delete edilen entity başka bir user'a bağlıysa (örn. internal sales_agent kaydı bir user'a bağlı), second approver o bağlı user da olamaz (`approver.id ≠ target.user_id`).
  7. Onay anında approver'ın session'ı aktif olmalı — yeni login + reason zorunlu, "passive approval" yok.
- `approve_hard_delete` permission default hiçbir template'e atanmaz; Owner manuel olarak güvendiği user'a verir.
- Hiçbir aktif user'da bu permission yoksa hard delete kapalı, UI disabled.
- Hard delete sadece hiçbir FK referansı yoksa mümkün.
- Audit log: delete event (kalıcı).

### 1.3.3 Owner security rules — `is_owner` flag

Owner statüsü `users.is_owner boolean` üzerinden korunur. Profile template adından bağımsız.

**Kurallar (backend double-check + UI disabled state):**

1. **Aktif Owner sayısı 1'in altına indirilemez.** Bu invariant şu aksiyonların hepsi için geçerlidir:
   - User deactivate
   - Hard delete of `is_owner = true` user
   - `is_owner = true` → `is_owner = false` revoke
   
   Backend her üç aksiyonun commit öncesinde şu sorguyu çalıştırır:
   ```sql
   SELECT count(*) FROM users WHERE is_owner = true AND is_active = true;
   ```
   Sonuç 1 ise ve aksiyon bu son Owner'ı etkileyecekse, işlem reddedilir. UI disabled state + tooltip.

2. **`is_owner` self-grant yasak.** actor user_id ≠ target user_id koşulu.

3. **`is_owner` sadece mevcut bir Owner tarafından verilebilir.**

4. **`is_owner = true` user'ın matrix'ini sadece başka bir Owner veya kendisi düzenleyebilir.** Bu permission `manage_user_permissions`'tan farklı bir kontrol katmanıdır.

5. **`is_owner` revoke:** Bir Owner başka bir Owner'ın is_owner'ını false yapabilir. Audit + notification + reason zorunlu.

`profile_template_id = 'Owner template'` displaydir, authorization değildir. Gerçek koruma `is_owner` flag'inden gelir.

### 1.3.4 `display_role` — authorization değil, sadece display

LIFFY mevcut `users.role` enum'ı (`owner|admin|manager|sales_rep`) yeni mimaride **yetki kaynağı olarak kullanılmaz**. Authorization: permission matrix + scope + `is_owner` flag.

**Kullanım:**
- UI'da user listesinde "rol" kolonu
- Raporlama kolaylığı
- Hierarchy graph görsel etiket

**Kullanılmayan:**
- `if (user.role === 'owner') { ... }` koşulları **yasak**.
- Backend middleware'lerde `req.user.role` kontrolü yok.

**Migration:**
- LIFFY'deki `role` değeri `display_role`'a kopyalanır.
- 25 mevcut authorization call site Bölüm 2'de matrix + scope + `is_owner` sorgusuna geçirilir.

### 1.3.5 LEENA legacy login migration (cutover)

**Adım 1 — Hazırlık:**
- Yeni `users` tablosu inşa edilir.
- Mevcut `organizers.password_hash` kaydından ilk Owner user oluşturulur:
  - `email`, `password_hash` (kopya), `profile_template_id` (Owner), `is_owner = true`, `full_name`
  - `password_must_change = true`
  - `created_by_actor_type = 'migration'`, `created_by = NULL`
  - `updated_by`, `updated_by_actor_type` NULL kalır.

**Adım 2 — Cutover:**
- Yeni auth servisi devreye alınır.
- Eski LEENA login endpoint kapatılır; yeni adrese yönlendirme.
- Cutover noktası kayda alınır.

**Adım 3 — Migration sonrası:**
- `organizers.password_hash` deprecated, 30 gün read-only.
- 30 gün sonra arşivlenir ve kolon kaldırılır.
- `organizers` → `organizations` rename.

**LIFFY mevcut kullanıcılar — email-based dedup:**

Migration sırasında **email üzerinden dedup** yapılır. LEENA `organizers.email` ile LIFFY `users.email` aynıysa **iki ayrı kayıt yaratılmaz**; tek canonical user oluşturulur.

**Çakışma çözümü:**
- `password_hash`: **LEENA wins** (organizer'ın hash'i).
- `is_owner = true` (LEENA'dan gelir, ilk Owner).
- LIFFY'deki ek metadata (last_login_at, last_active_at, display_role, vb.) bu canonical kayda merge edilir.
- Çakışan başka field varsa LEENA tarafı kazanır.

**Suer için özel:** Tek user kaydı, `is_owner = true`, eski LIFFY kullanım izleri (last_active_at, last_login_at) korunur.

**Diğer LIFFY kullanıcılar (elif, bengu):**
- Yeni `users` tablosuna aktarılır.
- `password_hash` LIFFY'den aynen taşınır.
- `password_must_change = false`.
- `profile_template_id`: LIFFY role default template'e map edilir.
- LIFFY `role` değeri `display_role`'a kopyalanır.
- `created_by_actor_type = 'migration'`.
- `is_owner = false`.

---

## 1.4 `sales_agents` tablosu

Commission attribution entity'si. Bugün ~150 aktif kayıt.

### 1.4.1 Schema

```sql
CREATE TABLE sales_agents (
  id                          uuid PRIMARY KEY,
  organization_id             uuid NOT NULL REFERENCES organizations(id),
  user_id                     uuid REFERENCES users(id) UNIQUE,
  
  full_name                   text NOT NULL,
  agent_type                  text NOT NULL CHECK (agent_type IN ('internal','external_agency','external_freelance')),
  
  email                       text,
  phone_e164                  text,
  country_code                text REFERENCES core_countries(code),
  
  default_commission_rate     numeric(5,2) CHECK (default_commission_rate IS NULL OR (default_commission_rate >= 0 AND default_commission_rate <= 100)),
  
  -- Banka/IBAN bilgileri burada DEĞİL → sales_agent_payment_profiles
  
  tax_status                  text,
  notes                       text,
  
  is_active                   boolean NOT NULL DEFAULT true,
  activated_at                timestamptz NOT NULL DEFAULT now(),
  deactivated_at              timestamptz,
  deactivated_by              uuid REFERENCES users(id),
  deactivated_by_actor_type   text,
  deactivation_reason         text,
  
  created_at                  timestamptz NOT NULL DEFAULT now(),
  created_by                  uuid REFERENCES users(id),
  created_by_actor_type       text NOT NULL DEFAULT 'user'
                              CHECK (created_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  updated_at                  timestamptz NOT NULL DEFAULT now(),
  updated_by                  uuid REFERENCES users(id),
  updated_by_actor_type       text
                              CHECK (updated_by_actor_type IS NULL OR updated_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  CHECK (
    (agent_type = 'internal' AND user_id IS NOT NULL)
    OR (agent_type <> 'internal' AND user_id IS NULL)
  ),
  
  CHECK (
    (is_active = true AND deactivated_at IS NULL)
    OR (is_active = false AND deactivated_at IS NOT NULL AND deactivation_reason IS NOT NULL)
  ),
  
  CHECK (
    (created_by_actor_type = 'user' AND created_by IS NOT NULL)
    OR (created_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    updated_by_actor_type IS NULL
    OR (updated_by_actor_type = 'user' AND updated_by IS NOT NULL)
    OR (updated_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    (deactivated_at IS NULL AND deactivated_by IS NULL AND deactivated_by_actor_type IS NULL)
    OR (
      deactivated_at IS NOT NULL
      AND (
        (deactivated_by_actor_type = 'user' AND deactivated_by IS NOT NULL)
        OR (deactivated_by_actor_type IN ('system','migration','zoho_sync'))
      )
    )
  ),
  
  CHECK (
    phone_e164 IS NULL
    OR phone_e164 ~ '^\+[1-9][0-9]{7,14}$'
  )
);
```

**Banka bilgileri ayrı tablo:**

```sql
CREATE TABLE sales_agent_payment_profiles (
  id                          uuid PRIMARY KEY,
  sales_agent_id              uuid NOT NULL REFERENCES sales_agents(id) UNIQUE,
  
  encrypted_iban              text,
  encrypted_swift             text,
  bank_name                   text,                            -- non-sensitive
  account_name                text,                            -- semi-sensitive
  payment_currency            text REFERENCES core_currencies(code),
  tax_id                      text,                            -- view_sensitive_finance gerekli
  
  updated_at                  timestamptz NOT NULL DEFAULT now(),
  updated_by                  uuid REFERENCES users(id),
  updated_by_actor_type       text
                              CHECK (updated_by_actor_type IS NULL OR updated_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  CHECK (
    updated_by_actor_type IS NULL
    OR (updated_by_actor_type = 'user' AND updated_by IS NOT NULL)
    OR (updated_by_actor_type IN ('system','migration','zoho_sync'))
  )
);
```

**Notlar:**

- `user_id` nullable UNIQUE — bir user en fazla bir sales_agent kaydına bağlı.
- CHECK constraint: internal → user_id dolu, external → NULL.
- `default_commission_rate` range CHECK: 0-100.
- **Banka/IBAN ayrı tabloda**, `view_sensitive_finance` permission ile sınırlı. WhatsApp channel restriction listesi bu tabloyu kapsar.
- **Payment profile = current.** `sales_agent_payment_profiles` bugünkü banka bilgisini taşır. Commission payment yapılırken (Bölüm 6 finance), payment transaction record'unda banka/IBAN bilgileri **snapshot olarak ayrıca saklanır**. Bu sayede payment profile değişse bile eski payment'ların hangi hesaba gittiği audit trail'inde korunur. Detay Bölüm 6.
- `notes` audit edilir (B15).

### 1.4.2 Sales agent lifecycle

**Create:**
- Yetki: `manage_sales_agents` special permission. Default: Project Department Lead profile + Owner profile. Sales Manager profile'a delegate edilebilir.
- Zorunlu: `full_name`, `agent_type`.
- `internal` ise: `user_id` zorunlu, UNIQUE check.
- Authorized user yaratır — mimari kişiye bağlı değil.
- Audit log.

**Internal agent oluşturma:**
- Bengü için user kaydı oluşturulur.
- Authorized user sales_agent kaydı oluşturur, `user_id = bengü.id`, `agent_type = 'internal'`.

**External agent oluşturma:**
- Authorized user sales_agent kaydı oluşturur, `user_id = NULL`, `agent_type = 'external_agency'`.
- Login yok; commission ödemesi `sales_agent_payment_profiles.encrypted_iban`'a.

**Deactivate:**
- Yetki: `manage_sales_agents`. Reason zorunlu.
- Yeni attribution'da seçilemez (dropdown filter).
- Eski contract'lar bozulmaz.
- Bağlı user otomatik deaktive olmaz; Owner'a notification.

**Reactivate:** Yeni attribution'da seçilebilir.

**Hard delete:** Default deactivate. Çift onaylı (1.3.2'deki second approver kuralları aynen geçerli). `approve_hard_delete` permission'lı kimse yoksa kapalı. FK referans varsa reddedilir.

---

## 1.5 `data_entry_contractors` tablosu

Public form üzerinden submission yapan external workers. Login yok, commission yok.

### 1.5.1 Schema

```sql
CREATE TABLE data_entry_contractors (
  id                          uuid PRIMARY KEY,
  organization_id             uuid NOT NULL REFERENCES organizations(id),
  
  full_name                   text NOT NULL,
  email                       text,
  phone_e164                  text,
  country_code                text REFERENCES core_countries(code),
  
  payment_terms               text,
  payment_rate                numeric(10,2) CHECK (payment_rate IS NULL OR payment_rate >= 0),
  payment_currency            text REFERENCES core_currencies(code),
  
  notes                       text,
  
  is_active                   boolean NOT NULL DEFAULT true,
  activated_at                timestamptz NOT NULL DEFAULT now(),
  deactivated_at              timestamptz,
  deactivated_by              uuid REFERENCES users(id),
  deactivated_by_actor_type   text,
  deactivation_reason         text,
  
  created_at                  timestamptz NOT NULL DEFAULT now(),
  created_by                  uuid REFERENCES users(id),
  created_by_actor_type       text NOT NULL DEFAULT 'user'
                              CHECK (created_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  updated_at                  timestamptz NOT NULL DEFAULT now(),
  updated_by                  uuid REFERENCES users(id),
  updated_by_actor_type       text
                              CHECK (updated_by_actor_type IS NULL OR updated_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  CHECK (
    (is_active = true AND deactivated_at IS NULL)
    OR (is_active = false AND deactivated_at IS NOT NULL AND deactivation_reason IS NOT NULL)
  ),
  
  CHECK (
    (created_by_actor_type = 'user' AND created_by IS NOT NULL)
    OR (created_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    updated_by_actor_type IS NULL
    OR (updated_by_actor_type = 'user' AND updated_by IS NOT NULL)
    OR (updated_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    (deactivated_at IS NULL AND deactivated_by IS NULL AND deactivated_by_actor_type IS NULL)
    OR (
      deactivated_at IS NOT NULL
      AND (
        (deactivated_by_actor_type = 'user' AND deactivated_by IS NOT NULL)
        OR (deactivated_by_actor_type IN ('system','migration','zoho_sync'))
      )
    )
  ),
  
  CHECK (
    phone_e164 IS NULL
    OR phone_e164 ~ '^\+[1-9][0-9]{7,14}$'
  )
);

CREATE TABLE data_entry_contractor_tokens (
  id                          uuid PRIMARY KEY,
  contractor_id               uuid NOT NULL REFERENCES data_entry_contractors(id),
  
  token_hash                  text NOT NULL UNIQUE,            -- HMAC-SHA256(token, server_secret_vN)
  hash_key_version            text NOT NULL,                   -- "v1", "v2", ...
  token_prefix                text NOT NULL,                   -- ilk 8 karakter, UI display
  
  issued_at                   timestamptz NOT NULL DEFAULT now(),
  issued_by                   uuid NOT NULL REFERENCES users(id),
  expires_at                  timestamptz,
  
  revoked_at                  timestamptz,
  revoked_by                  uuid REFERENCES users(id),
  revocation_reason           text,
  
  last_used_at                timestamptz,
  use_count                   integer NOT NULL DEFAULT 0,
  
  CHECK (
    (revoked_at IS NULL AND revocation_reason IS NULL)
    OR (revoked_at IS NOT NULL AND revocation_reason IS NOT NULL)
  )
);
```

### 1.5.2 Token kriptografisi

- **Token üretimi:** Cryptographically secure random, 32 byte → base64url (43 karakter).
- **Hash yöntemi:** `HMAC-SHA256(token, server_secret_vN)`. Server secret production secret manager'da.
  - Deterministic lookup: `WHERE token_hash = HMAC(submitted_token, server_secret_v[matching_version])` — tek query.
  - DB dump alan attacker rainbow table ile token bulamaz.
  - bcrypt **kullanılmaz** (salted, lookup imkânsız).
  - Plain SHA-256 **kullanılmaz** (server secret yok, rainbow'a açık).
- **Plain token DB'de asla saklanmaz.** Sadece bir kez UI'da gösterilir.
- **`hash_key_version`:** Token hangi server secret version ile üretildi kayda saklanır. Verify sırasında doğru key version kullanılır. Key rotation sonrası eski version key bir süre tutulur (eski token'lar geçerli), sonra eski token'lar revoke veya doğal expire'a bırakılır. Aynı pattern ileride refresh token hash için de geçerli.

### 1.5.3 URL token leak koruması

İki katman birlikte:

1. **HTTP response header (primary):** Public form endpoint response'unda `Referrer-Policy: no-referrer` header set edilir.
2. **HTML meta tag (fallback):** Form HTML'inde `<meta name="referrer" content="no-referrer">`.

Ek olarak:
- Request log'larında token maskelenir (örn. `/intake/abc1****`).
- Analytics event'lerinde maskeleme.
- Error tracking'de maskeleme.

### 1.5.4 Contractor lifecycle

**Create contractor:**
- Yetki: `manage_data_entry_contractors` special permission. Default: Sales Manager + Project Department Lead + Owner.
- Audit log.

**Issue token:**
- Sistem random token üretir, HMAC ile hash'lenir, `hash_key_version` ile DB'ye yazılır.
- Plain token sadece bir kez UI'da gösterilir.
- Public form URL: `https://forms.elanfairs.com/intake/{token}`.
- Audit log.

**Public form submission:**
- Backend submitted token'ı HMAC ile hash'leyip eşleştirir.
- Eşleşme yoksa, revoked, expired → 401.
- Eşleşirse:
  - `last_used_at`, `use_count` güncellenir.
  - Submission `contractor_id`'ye bağlanır (token id'ye değil).
  - Lead/contact yaratılır, LIFFY'ye forward (cross-DB logical reference).
  - Audit log.

**Rotate token / Revoke token:** Reason zorunlu.

**Deactivate contractor:** Tüm aktif token'lar otomatik revoke.

**Hard delete:** Default deactivate. Çift onaylı (1.3.2'deki second approver kuralları aynen).

---

## 1.6 `organizations` tablosu ve `integration_credentials`

### 1.6.1 `organizations` — non-sensitive metadata

```sql
CREATE TABLE organizations (
  id                          uuid PRIMARY KEY,
  name                        text NOT NULL,
  legal_name                  text,
  country_code                text REFERENCES core_countries(code),
  default_timezone            text NOT NULL DEFAULT 'Europe/Istanbul',
  default_currency            text REFERENCES core_currencies(code),
  
  reply_forward_emails        text[],                          -- non-sensitive
  logo_url                    text,
  
  is_active                   boolean NOT NULL DEFAULT true,
  created_at                  timestamptz NOT NULL DEFAULT now(),
  updated_at                  timestamptz NOT NULL DEFAULT now()
);
```

API key'ler, secret'lar burada **değil**. Bu tablo LIFFY'ye read-only replica olarak gönderilebilir.

### 1.6.2 `integration_credentials` — sensitive secret'lar

```sql
CREATE TABLE integration_credentials (
  id                          uuid PRIMARY KEY,
  organization_id             uuid NOT NULL REFERENCES organizations(id),
  
  app_scope                   text NOT NULL CHECK (app_scope IN ('leena','liffy')),
  provider                    text NOT NULL,                   -- 'sendgrid'|'zerobounce'|'twilio'
  credential_type             text NOT NULL,                   -- 'api_key'|'webhook_secret'|'oauth_token'
  
  secret_ref                  text,                            -- secret manager ARN
  encrypted_value             text,                            -- alternatif: app-layer encrypted
  
  is_active                   boolean NOT NULL DEFAULT true,
  rotated_at                  timestamptz,
  expires_at                  timestamptz,
  
  created_at                  timestamptz NOT NULL DEFAULT now(),
  created_by                  uuid REFERENCES users(id),
  updated_at                  timestamptz NOT NULL DEFAULT now(),
  
  -- XOR: tam olarak biri dolu olmalı
  CHECK (
    (secret_ref IS NOT NULL AND encrypted_value IS NULL)
    OR
    (secret_ref IS NULL AND encrypted_value IS NOT NULL)
  )
);

CREATE UNIQUE INDEX active_integration_credentials_unique
  ON integration_credentials (organization_id, app_scope, provider, credential_type)
  WHERE is_active = true;
```

**Prensipler:**

- **İki saklama modu, XOR:** Bir row için **tam olarak biri** dolu — `secret_ref` veya `encrypted_value`. İkisi aynı anda dolu olamaz; hibrit durum yasak. Organization seçer ve tutarlı uygular.
- **Plain text saklama yasak.**
- **`app_scope` izolasyonu:** LEENA secret'ı LIFFY'ye **asla** replicate edilmez. Replication mekaniği `app_scope`'a göre filtreler.
- **Audit log:** Her credential create/rotate/revoke event'i. Secret değeri asla audit log'a yazılmaz.

---

## 1.7 Cross-DB referanslar: gerçek FK vs logical reference

LEENA tek DB, LIFFY ayrı DB (A5). Aynı DB içi referanslar **gerçek FK**, cross-DB **logical reference**.

**Gerçek FK (LEENA içi):**
```
sales_agents.user_id REFERENCES users(id)
sales_agents.organization_id REFERENCES organizations(id)
data_entry_contractor_tokens.contractor_id REFERENCES data_entry_contractors(id)
```

**Logical reference (LIFFY → LEENA):**
```sql
-- LIFFY DB içinde
leads.source_contractor_id    uuid  -- logical reference to LEENA.data_entry_contractors.id
leads.assigned_user_id        uuid  -- logical reference to LEENA.users.id
leads.organization_id         uuid  -- logical reference to LEENA.organizations.id
```

**Disiplin:**
- Schema yorumu: `-- logical reference to LEENA.<table>.<column>, not enforced by FK`.
- Validation application layer'da.
- Integrity LEENA replica üzerinden korunur (ilgili tablo LIFFY'de read-only replica olarak yaşıyorsa).

**Orphan reference yönetimi — detect/report/manual repair:**

Periodic detection job orphan logical reference'ları tespit eder ve **Owner + ilgili protected special permission'a sahip authorized user'lara** (örn. `system_integrity_alerts` veya `view_audit_log` permission'lı user'lar) rapor eder. **Otomatik silme yapılmaz** — lead, quote, contract attribution gibi yerlerde otomatik delete edilemez veri vardır. Repair manuel:
- Silinmiş kayıt restore edilir, veya
- Orphan reference NULL'a set edilir, veya
- Reference deactive olarak işaretlenir.

Her durumda audit'lenir. Historical attribution otomatik silinmez.

---

## 1.8 Cross-organization tutarlılık

UUID global olduğu için teorik olarak başka tenant'ın user'ına referans verme riski var. Bugün tek tenant olduğumuz için pratik risk yok, ama multi-tenant-ready iddiamız var.

**Karar (MVP):** Application-layer validation. API endpoint middleware'lerinde insert/update sırasında `organization_id` eşleşmesi explicit kontrol edilir. Schema serbest kalır (composite FK overkill), trigger ileride Phase 2'de eklenir.

**Validation noktaları:**
- `sales_agents.user_id` insert/update: `assertSameOrganization(sales_agent.organization_id, user.organization_id)`.
- `users.reports_to` insert/update: `assertSameOrganization(user.organization_id, manager.organization_id)` + cycle check (Bölüm 2).
- `users.office_id` insert/update: `assertSameOrganization(user.organization_id, office.organization_id)`.

Test edilebilir, kolay, tek noktada toplanır. Phase 2'de DB trigger'a geçilirse application-layer kontrolü redundancy olarak kalır.

---

## 1.9 Identity'ler arası ilişki diyagramı

```
                organizations (LEENA master)
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
     users     sales_agents    data_entry_contractors
       │              │              │
       │              │              ▼
       │              │    data_entry_contractor_tokens
       │              │
       │              ▼
       └──────► sales_agents.user_id (nullable, unique)
                  (sadece internal agent_type için dolu)

       sales_agents ─────► sales_agent_payment_profiles (1:0..1)
                            (banka detayları; commission payment'ta snapshot alınır)

       organizations ─────► integration_credentials (1:N)
                             (API key'ler; app_scope ile LEENA/LIFFY izole)
```

**Cross-DB logical references (LIFFY → LEENA):** LIFFY tablolarındaki `organization_id`, `user_id`, `contractor_id` referansları logical reference olarak işaretlenir.

---

## 1.10 Bu bölümün kararları

| ID | Karar |
|---|---|
| **B1** | Schema'da tek isim: `organization_id`. `organizer_id` (LIFFY mevcut) emekli. |
| **B2** | Üç ayrı identity tablosu: `users`, `sales_agents`, `data_entry_contractors`. Ortak parent yok. |
| **B3** | `sales_agents.user_id` nullable UNIQUE. CHECK constraint agent_type ile tutarlılığı garanti eder. |
| **B4** | Data entry contractor token: ayrı `data_entry_contractor_tokens` tablosu. **HMAC-SHA256(token, server_secret_vN)** hash. `hash_key_version` field key rotation'a izin verir. bcrypt veya plain SHA-256 değil. Submission `contractor_id`'ye bağlanır (token id'ye değil). |
| **B5** | Üç entity için lifecycle prensibi: **deactivate default, hard delete istisna**. Hard delete sadece Owner + ayrı aktif user'ın birlikte onayıyla; ikinci user'da `approve_hard_delete` protected special permission bulunmalı. **Second approver kuralları:** aktif user, aynı organization, requester'dan farklı, target'tan farklı, hard delete edilen entity başka user'a bağlıysa o bağlı user da olamaz, onay anında aktif session + yeni login + reason. `approve_hard_delete` default hiçbir template'e atanmaz; Owner manuel olarak güvendiği user'a verir. Permission'lı aktif kimse yoksa hard delete kapalı, UI disabled. Her deactivate/delete reason field zorunlu. |
| **B6** | Deactivation davranışları entity-spesifik: (a) user → login kapanır, refresh token revoke, historical attribution korunur, **direct report'lar zorunlu yeni manager'a reassign** (Owner istisna verebilir, audit'lenir); (b) sales_agent → yeni attribution'da seçilemez, eski contract bozulmaz; (c) contractor → token'lar otomatik revoke. **Sales_agent dropdown filter'ı bağlı user.is_active'i de kontrol eder.** |
| **B7** | LEENA legacy `organizers.password_hash` migration: cutover'da ilk Owner user oluşturulur (`is_owner = true`, `created_by_actor_type = 'migration'`), password_hash kopyalanır, `password_must_change = true`. 30 gün deprecated, sonra silinir. **LIFFY mevcut user'larla email-based dedup:** aynı email'e iki kayıt yaratılmaz; LEENA wins password_hash çakışmasında; LIFFY metadata canonical kayda merge edilir. |
| **B8** | LEENA `organizers` → `organizations` tablosuna dönüşür (multi-tenant root, non-sensitive metadata). API key'ler ve secret'lar ayrı `integration_credentials` tablosuna alınır. **Plain text secret yasak; XOR constraint:** `secret_ref` veya `encrypted_value` tam olarak biri dolu, hibrit yasak. `app_scope` ile LEENA/LIFFY izole — LEENA secret'ı LIFFY'ye asla replicate edilmez. |
| **B9** | `users.display_role` text field display amaçlı; authorization kararlarında **kullanılmaz**. Authorization: permission matrix + scope + `is_owner` flag. Eski LIFFY `role` enum'ı migration'da `display_role`'a kopyalanır, 25 authorization call site Bölüm 2'de matrix'e geçirilir. |
| **B10** | Owner statüsü `users.is_owner boolean` flag'i, profile_template adından bağımsız. Kurallar: **(a) aktif Owner sayısı 1'in altına indirilemez — deactivate, hard delete, is_owner revoke üç aksiyonu da bu invariant'ı tetikler**, (b) self-grant yasak, (c) sadece mevcut Owner verebilir, (d) `is_owner = true` user'ın matrix'ini sadece başka Owner veya kendisi düzenleyebilir, (e) is_owner revoke audit + reason zorunlu. Backend her aksiyonun commit öncesinde aktif Owner sayısını sorgular. UI disabled state. |
| **B11** | Sales agent ve data entry contractor creation **permission-bazlı**, kişi-bazlı değil: `manage_sales_agents`, `manage_data_entry_contractors`. |
| **B12** | Tüm critical aksiyonlarda reason field zorunlu (deactivate, hard delete, token revoke, password reset, is_owner revoke). Schema CHECK + UI validation + backend enforcement. |
| **B13** | Sales agent banka/IBAN bilgileri ayrı tabloda (`sales_agent_payment_profiles`), `view_sensitive_finance` permission. Encrypted columns. **Payment profile current; commission payment yapılırken transaction record'unda banka/IBAN snapshot olarak ayrıca saklanır** (audit trail için). Detay Bölüm 6. |
| **B14** | Phone field formatı: **E.164** tek string (`phone_e164`). Schema-level regex validation: `^\+[1-9][0-9]{7,14}$`. WhatsApp opt-in + verified_at; bot lookup için `whatsapp_opt_in = true AND whatsapp_verified_at IS NOT NULL`. |
| **B15** | `notes` ve serbest metin field'ları **audit edilir** (update event log). Content opsiyonel redacted; event'in kendisi kayda geçer. |
| **B16** | `*_by_actor_type` pattern üç identity tablosunda + `sales_agent_payment_profiles`'da tutarlı: `created_by_actor_type` NOT NULL DEFAULT 'user' (create anında zorunlu), `updated_by_actor_type` nullable (kayıt henüz update edilmediyse her ikisi de NULL), `deactivated_by_actor_type` nullable (deactivate olmamışsa NULL). Her birinde CHECK: actor_type set'se by_id zorunlu (user için) veya by_id NULL kabul (system/migration/sync). |
| **B17** | Cross-DB referanslar **logical reference**, gerçek FK kurulamaz. Schema yorumunda explicit. Validation application layer'da. **Orphan reference yönetimi: detect/report/manual repair** — otomatik silme yapılmaz, periodic job tespit eder, Owner + ilgili protected permission'lı user'lara rapor, manuel onarım audit'lenir. |
| **B18** | Yüzde alanları için schema-level range CHECK: `CHECK (value >= 0 AND value <= 100)`. Tutarlı pattern (commission_rate, discount_percent, vb.). |
| **B19** | **Cross-organization tutarlılık: application-layer validation (MVP).** UUID global; aynı organization sınırı API middleware'lerinde explicit check edilir (`assertSameOrganization`). Schema'da composite FK overkill; trigger Phase 2'de eklenebilir. Validation noktaları: `sales_agents.user_id`, `users.reports_to`, `users.office_id` insert/update. |
| **B20** | Public form token leak koruması iki katman: (a) HTTP response header `Referrer-Policy: no-referrer` (primary), (b) HTML meta tag (client-side fallback). Ek olarak request log/analytics/error tracking'de token maskelenir. |

---

## 1.11 Açık kalan noktalar (sonraki bölümlere)

- `manage_users`, `manage_sales_agents`, `manage_data_entry_contractors`, `view_sensitive_finance`, `approve_hard_delete`, `system_integrity_alerts`, `view_audit_log`, `is_owner` grant/revoke gibi special permission'ların master listesi → Bölüm 2.
- `permission_templates` tablosu schema'sı ve "Owner template" tanımı → Bölüm 2.
- **Hierarchy cycle guard enforcement** (reports_to kuralları: self-report yasak, descendant-report yasak, reassignment cycle check, same-org check) → Bölüm 2.
- `offices` tablosu schema'sı → Bölüm 4 (reference data).
- Password policy (uzunluk, karmaşıklık, history) → Bölüm 3.
- 2FA / MFA → Bölüm 3 (Phase 2 işareti).
- Login throttling, brute-force koruması (`failed_login_count`, `locked_until`) → Bölüm 3.
- WhatsApp opt-in verification flow → Bölüm 3 veya 7.
- WhatsApp bot user identification + channel restriction layer → Bölüm 8.
- **LIFFY read-only replica adayları:** `users` (subset), `organizations` (non-sensitive), `data_entry_contractors`. `sales_agents` replica olur mu? → Bölüm 4.
- `integration_credentials` saklama yöntemi (secret manager reference vs application-layer encryption) — MVP'de hangisi? → Bölüm 3 veya operations.
- Commission payment'ta banka/IBAN snapshot mekaniği → Bölüm 6.
- **Audit log entity references logical reference olarak tasarlanır.** Strict FK kurulursa hard delete neredeyse imkânsız hale gelir (FK constraint engeller). Audit log immutable kalmalı; hard delete istisnası audit log ile çakışmayacak şekilde tasarlanır. 1.7 cross-DB logical reference pattern'inin audit versiyonu. Detay Bölüm 5.

---

## 1.12 Bölüm özeti

Üç identity tablosu birbirinden bağımsız: `users` login için (`is_owner` flag ile sistem-korumalı Owner statüsü, profile_template'ten bağımsız), `sales_agents` commission attribution için (banka detayları `sales_agent_payment_profiles` tablosunda izole, payment yapıldığında transaction record'unda snapshot alınır), `data_entry_contractors` public form submission attribution için (HMAC-SHA256 hashed token, `hash_key_version` ile rotation, Referrer-Policy + meta tag ile leak koruması). LEENA'nın eski tek-noktalı `organizers.password_hash` login'i `users` tablosuna migrate edilir, secret'lar ayrı `integration_credentials` tablosuna alınır (XOR constraint: secret_ref veya encrypted_value, hibrit yasak) ve `app_scope` ile LEENA/LIFFY arası izole tutulur. Default lifecycle aksiyonu deactivate; hard delete sadece Owner + `approve_hard_delete` permission'lı ayrı bir aktif user'ın çift onayıyla mümkün (second approver kuralları explicit), permission'lı kimse yoksa kapalıdır. Aktif Owner sayısı 1'in altına indirilemez — deactivate, hard delete, is_owner revoke üç aksiyonu da bu invariant'ı tetikler. Cross-DB referanslar logical reference olarak işaretlenir, orphan'lar detect/report/manual repair ile yönetilir, otomatik silme yapılmaz. Cross-organization tutarlılık MVP'de application-layer validation ile sağlanır. `*_by_actor_type` pattern üç tabloda + payment_profiles'da tutarlı (updated_by_actor_type nullable until first update). Phone E.164 schema-level regex ile validate edilir.

---

*Bu doküman Aşama 2 Bölüm 1 olarak finalize edilmiştir. Aşama 2 sonraki bölümleri ve Aşama 3 bu dokümanı kanonik referans olarak kullanır. Bölüm 1'e dönüş ancak resmi bir amendment (v1.1) ile mümkündür.*
