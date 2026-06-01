# ELL Mimarisi — v1.0 Konsolide

**Sürüm:** v1.0 — Konsolide (implementation girdisi)
**Tarih:** 2026-06-01
**Onaylayan:** Suer (Owner)
**Hedef kitle:** Implementation team (insan veya AI feature builder)
**Statü:** **Konsolide doküman implementation'ın ana source of truth'udur.** Detay dokümanlar deep-dive ve karar justification arşividir. Çakışma durumunda **konsolide doküman kazanır**; gerçek bir mimari karar uyumsuzluğu varsa Owner veya Mimari Claude karara bağlar. Implementation team rastgele eski detay dokümandan karar çekmemelidir. Detaylı mimari dokümanlar (Aşama 1 topology, Bölüm 1-2, 3.1-3.4 detaylı versiyonları) GitHub `ell-docs/archive/` altında **referans** olarak kalır.

**Not — bu dokümanın doğuş hikâyesi:** Altı aylık mimari süreç, alt-başlık başına çok turlu review döngüleriyle yürüdü ve doğal sonucu olarak over-engineering eşiğine geldi. Bu konsolide doküman o detay tartışmalarının **distilasyonudur** — her kararın "ne + neden"i kalır, tur tur biriken edge-case/pseudocode/transaction-semantic detayı kanonik referans dokümanlara bırakılır. Implementation buradan başlar; bir karar için daha fazla derinlik gerekirse ilgili kanonik dokümana iner.

---

## 1. Sistem topolojisi

### 1.1 Üç servis, iki uygulama, bir çatı

ELL üç isimli bileşenden oluşur, ama mimari olarak **iki uygulama + bir branding çatısıdır**:

**LEENA — ana gövde (identity provider + operasyon + finance + intelligence).** Production'da çalışan sistem. Visitor management, floor plan, check-in, AI query engine, WhatsApp bot, finance, customer/contract dünyası burada. Aynı zamanda ELL'in **kimlik sağlayıcısı**: users, permissions, hierarchy, audit log, JWT üretimi LEENA'da merkezi. Tek PostgreSQL veritabanı; cross-modül sorgu yoğun (visitor + contract + revenue + floor plan) olduğu için tek DB zorunlu.

**LIFFY — sales workspace (API backend).** Sales rep'lerin günlük çalışma ekranı: lead follow-up, pipeline, quote modülü, mining/campaign altyapısı. Kendi ayrı veritabanı ve kendi SendGrid hesabı/domain'i var. LIFFY'nin ayrı uygulama olmasının somut sebebi **email deliverability izolasyonu** — LIFFY 80K+ mass marketing maili atar (yapısal spam riski yüksek), LEENA imzalı müşterilere operasyonel mail atar (risk düşük). İkisi aynı IP havuzunu paylaşamaz. Kod ayrımının ikincil sebebi LIFFY kodunun zaten ayrı ve port edilebilir olması.

**ELIZA — branding çatısı.** Ayrı servis **değil**, LEENA'nın bir alt modülü. Ürün adı + tek login sayfası + üst navigasyon + role-based landing. "ELIZA" markası kullanıcı yüzünde kalır; teknik olarak login ve navigation LEENA içinde yaşar, LIFFY'ye geçiş LEENA'nın yönlendirmesiyle olur. ELIZA'nın kendi DB'si veya iş mantığı yoktur.

### 1.2 İletişim modeli: REST + JWT

LIFFY artık kendi login sayfasını kaldırır ve **LEENA'nın ürettiği JWT'yi kabul eder**. Authorization role-based değil **matrix-based**'dir; LIFFY scope/permission bilgisini LEENA'dan okur (replikasyon + version-based cache invalidation, Bölüm 4).

İki sistem arası beş iş akışı köprüsü ve dört shared infrastructure bağı vardır. Kritik köprüler:

- **Köprü 1 (LIFFY → LEENA):** Quote "Signed" olunca quote'un tamamı snapshot fiyatlarla LEENA'ya push edilir; LEENA'da "pending convert" listesine düşer. Yetkili Project user (genellikle Yaprak) convert ederken customer_company/customer_contact yaratır veya eşleştirir.
- **Köprü 2 (LEENA → LIFFY):** Lead enrichment geri beslemesi. Quote signed / convert tamamlandı / disqualified / do-not-contact olaylarında LIFFY ilgili person/company'i kampanyalardan çıkarır. İki kademeli: "signed_pending_convert" (geçici) ve "customer" (kesin).
- **Köprü 3 (LEENA ↔ LIFFY):** Floor plan okuma + stand_reservation yazma. LIFFY floor plan geometry'sini **değiştirmez**; ayrı `stand_reservations` tablosuna satış niyeti yazar. Çoklu rezervasyon mümkün, zorunlu deadline (max 3 hafta), **otomatik kazanan yok** — convert anında karar tek mercii Project.
- **Köprü 4 (LIFFY → LEENA):** Nightly push ile `liffy_daily_metrics` aggregation; WhatsApp bot ve manager raporları bunu okur. Gün-içi olaylar notifications real-time stream üzerinden.

### 1.3 Aşama 1'in kritik kararları (özet)

- **İki dünya ayrımı veri modeline iner:** LIFFY'nin `companies`/`persons` (prospect) ile LEENA'nın `customer_companies`/`customer_contacts` (müşteri) **farklı entity'lerdir**. Convert anında LEENA'da yeni customer entity yaratılır veya eşleştirilir.
- **Contract creation iki birinci-sınıf akış:** Akış A (signed quote'tan convert — Köprü 1) ve Akış B (Project'in quote-less manuel creation). Akış B "fallback" değil, gerçek operasyonel pattern — bugün Zoho'da da her sözleşmenin quote'u yok. Akış B'de LEENA, LIFFY companies'i fuzzy match ile arar (firma adı + ülke + sektör) ve data bifurcation'ı önler.
- **Sales attribution üç kategori:** (a) sales rep — system user, komisyonlu; (b) sales agent — system user **değil**, dış ajans/freelance, `sales_agents` tablosunda, contract bazında manuel komisyon; (c) Project department / Elan Expo — komisyonsuz. Sales agent auth/scope/hierarchy'de yer almaz.
- **Contract visibility explicit ownership ile kurulur:** Contract visibility/scope resolver `sales_agents.user_id` üzerinden **kurulamaz** — external sales agent'larda bu alan NULL'dur. Contract modülünde explicit ownership alanları zorunlu: `sales_owner` (system user), `account_owner` (account manager), `responsible_project_user` (operations). Scope resolver bu alanlar üzerinden çalışır. Sales agent attribution sadece commission ve raporlama için; visibility/permission kaynağı değildir.
- **Finance invariants (kodun yazım disiplini):** (1) Two-sided money movement — her para hareketi iki ayaklı, tek taraflı kayıt yasak. (2) Computed balances, not stored — bakiyeler transaction sum'ından hesaplanır, field olarak saklanmaz. (3) Frozen exchange rates per transaction — kur kaydedildikten sonra değişmez. Bu üçü Zoho'nun "para nereden geldi izlenemiyor" probleminin çözümüdür.
- **Pricing snapshot/freeze:** Quote line item'a fiyat snapshot olarak yazılır; `price_version_id` ile kaynak izlenebilir. Sonraki fiyat değişiklikleri eski quote'u etkilemez.
- **Tek-DB-değil kararının bilinen maliyetleri:** cross-DB join yok (logical reference), audit network call, ref data sync gecikmesi, JWT expiry penceresi. Bunlar bilinçli kabul edilmiş trade-off'lar.

---

## 2. Bölüm 1 — Identity

### 2.1 Üç identity tablosu, ortak parent yok

Sisteme bağlanan üç tür kimlik var ve **üçü bağımsız tablodur** — ortak `people`/`parties` parent tablosu yoktur. Gerekçe: üçü gerçekten farklı dünyalar (user'ın email login için zorunlu, sales agent'ınki opsiyonel, contractor'ın kalıcı kimliği opsiyonel); ortak parent zorla benzerlik üretir veya anlamsız NULL'larla dolar. İlişkiler tablolar arası referanslarla kurulur.

- **`users`** — sisteme login eden gerçek kişiler (~25 aktif).
- **`sales_agents`** — system user olmayan dış ajans/freelance acenteler; commission attribution için. Banka detayları ayrı `sales_agent_payment_profiles` tablosunda (`view_sensitive_finance` ile korunur).
- **`data_entry_contractors`** — public form submission attribution için; HMAC-SHA256 hash'li token (`hash_key_version` ile rotation), ayrı `data_entry_contractor_tokens` tablosu.

Tek tutarlı tenant kolonu adı **`organization_id`** (LIFFY'nin eski `organizer_id`'si emekli). Bugün tek tenant ("Elan Expo") var ama schema multi-tenant-ready kalır.

### 2.2 `users` tablosu (final v1.1 hâli)

Kritik kolonlar ve amendment batch ile gelen alanlar:

```sql
CREATE TABLE users (
  id                          uuid PRIMARY KEY,
  organization_id             uuid NOT NULL REFERENCES organizations(id),

  email                       citext NOT NULL,           -- case-insensitive native
  full_name                   text NOT NULL,
  display_name                text,

  phone_e164                  text,                       -- regex: ^\+[1-9][0-9]{7,14}$
  whatsapp_opt_in             boolean NOT NULL DEFAULT false,
  whatsapp_verified_at        timestamptz,

  preferred_language          text REFERENCES core_languages(code),
  timezone                    text NOT NULL DEFAULT 'Europe/Istanbul',

  -- Credential alanları (Bölüm 3.2 + v1.1 amendment batch)
  password_hash               text,                       -- Argon2id PHC string; nullable (SSO Phase 2)
  password_set_at             timestamptz,
  password_must_change        boolean NOT NULL DEFAULT false,
  primary_password_login_disabled boolean NOT NULL DEFAULT false,  -- v1.1 amendment (force reset email_link)
  temporary_password_hash     text,                       -- v1.1 amendment (force reset temp delivery)
  temporary_password_expires_at timestamptz,              -- v1.1 amendment

  -- Session invalidation epoch (Bölüm 3.3 + v1.1 amendment batch)
  auth_version                integer NOT NULL DEFAULT 1, -- v1.1 amendment; bump = tüm token invalidation

  reports_to                  uuid REFERENCES users(id),  -- hierarchy; cycle/same-org guard Bölüm 2
  office_id                   uuid REFERENCES offices(id),

  profile_template_id         uuid REFERENCES permission_templates(id),
  profile_template_version    integer,                    -- yaratım anı snapshot

  display_role                text,                       -- DISPLAY ONLY; authorization'da kullanılmaz
  is_owner                    boolean NOT NULL DEFAULT false,  -- protected sistem flag

  is_active                   boolean NOT NULL DEFAULT true,
  activated_at                timestamptz NOT NULL DEFAULT now(),
  deactivated_at              timestamptz,
  deactivated_by              uuid REFERENCES users(id),
  deactivated_by_actor_type   text,
  deactivation_reason         text,

  last_login_at               timestamptz,
  last_active_at              timestamptz,
  failed_login_count          integer NOT NULL DEFAULT 0, -- brute-force (Bölüm 3.2)
  locked_until                timestamptz,                -- brute-force lock

  created_at                  timestamptz NOT NULL DEFAULT now(),
  created_by                  uuid REFERENCES users(id),
  created_by_actor_type       text NOT NULL DEFAULT 'user',
  updated_at                  timestamptz NOT NULL DEFAULT now(),
  updated_by                  uuid REFERENCES users(id),
  updated_by_actor_type       text,                       -- nullable until first update

  UNIQUE (organization_id, email)
);
```

**v1.1 amendment batch (Bölüm 3 sürecinde biriken, Bölüm 3 final commit'inde uygulanan):**

1. `*_by_actor_type` enum'larına **`'integration'`** eklenir: `('user','system','migration','zoho_sync','integration')`. (Service-to-service / entegrasyon kaynaklı yazımlar için.)
2. Üç credential kolonu eklenir: `primary_password_login_disabled`, `temporary_password_hash`, `temporary_password_expires_at`.
3. `auth_version integer NOT NULL DEFAULT 1` eklenir — session invalidation epoch. Bu **credential state CHECK kapsamına girmez**; ayrı bir session-invalidation mekanizmasıdır, NOT NULL DEFAULT 1 dışında kendi CHECK'i yoktur.
4. Credential state CHECK invariant'ı (7 geçerli satır) — aşağıda 2.4.

**`*_by_actor_type` pattern (üç identity tablosunda + payment_profiles'da tutarlı):** `created_by_actor_type` NOT NULL DEFAULT 'user' (create anında zorunlu); `updated_by_actor_type` ve `deactivated_by_actor_type` nullable (henüz olmadıysa NULL). Her birinde CHECK: actor_type `'user'` ise ilgili `*_by` id NOT NULL; `system`/`migration`/`zoho_sync`/`integration` ise id NULL kabul. Bu pattern, "bu kaydı kim/ne değiştirdi" sorusunu her tabloda tutarlı cevaplar.

### 2.3 `organizations` ve `integration_credentials`

`organizations` multi-tenant root, non-sensitive metadata. Sensitive secret'lar (API key vb.) ayrı `integration_credentials` tablosunda. **Plain text secret yasak** — XOR constraint: `secret_ref` (secret manager referansı) veya `encrypted_value` tam olarak biri dolu olur, hibrit yasak. `app_scope` ile LEENA/LIFFY izole edilir; LEENA secret'ı LIFFY'ye asla replicate edilmez.

### 2.4 Deactivate disiplini ve credential state

**Lifecycle prensibi: deactivate default, hard delete istisna.** Hard delete sadece Owner + ayrı bir aktif user'ın (`approve_hard_delete` protected permission'lı) çift onayıyla mümkün; permission'lı kimse yoksa hard delete kapalıdır. Her deactivate/delete'te `reason` zorunlu.

**Deactivation davranışları entity-spesifik:**
- **User →** login kapanır, tüm refresh token revoke + `auth_version` bump, historical attribution korunur, **direct report'lar zorunlu olarak yeni manager'a reassign** edilir (Owner istisna verip organizational debt bırakabilir, audit'lenir).
- **Sales agent →** yeni attribution dropdown'ında seçilemez, eski contract bozulmaz. Dropdown filter'ı bağlı user'ın `is_active`'ini de kontrol eder.
- **Contractor →** token'lar otomatik revoke.

**Owner invariant:** Aktif Owner sayısı 1'in altına indirilemez — deactivate, hard delete ve `is_owner` revoke üç aksiyonu da bu invariant'ı tetikler; backend her aksiyon öncesi aktif Owner sayısını sorgular. `is_owner` self-grant yasak; sadece mevcut Owner verebilir.

**Credential state — 7 geçerli durum (CHECK invariant ile garanti edilir).** Bir user'ın credential durumu daima şu yedi geçerli kombinasyondan biridir: (1) initial setup pending; (2) initial admin-set temp aktif; (3) force reset email_link pending; (4) force reset temp aktif; (5) temp password expired; (6) primary credential must-change (LEENA migration paterni); (7) normal credential active. Yalnızca **satır 7 (normal credential active)** login'de normal access + refresh token çifti üretir; satır 2/4/6 restricted auth stage token üretir (aşağıda 4.5); satır 1/3/5 login'i reddeder. DB CHECK bu yedi satır dışındaki kombinasyonları engeller.

### 2.5 `display_role` ve authorization ayrımı

`users.display_role` sadece görüntü amaçlıdır; **authorization kararlarında kullanılmaz**. Authorization üç kaynaktan gelir: permission matrix + scope + `is_owner` flag (Bölüm 2). Eski LIFFY `role` enum'ı migration'da `display_role`'a kopyalanır, gerçek authorization call site'ları matrix'e taşınır.

### 2.6 Standart audit kolonları (tüm ana tablolarda)

Tüm ana tablolar (`customer_companies`, `contracts`, `quotes`, `sales_agents`, `data_entry_contractors`, `integration_credentials`, vb.) standart audit kolon setini taşır: `created_at` + `created_by` + `created_by_actor_type` (NOT NULL DEFAULT 'user'), `updated_at` + `updated_by` + `updated_by_actor_type` (nullable). Soft-delete destekleyenler ek olarak `deactivated_at` + `deactivated_by` + `deactivated_by_actor_type` taşır. Her `*_by_actor_type` CHECK invariant'ı: actor_type='user' ise id NOT NULL; system/migration/zoho_sync/integration ise id NULL kabul.

---

## 3. Bölüm 2 — Permissions

### 3.1 Authorization üç kaynaklı

Her yetki kararı **matrix + scope + `is_owner` flag** üçlüsünden çıkar. Karar sırası (authorization order) sabittir:

1. **Action classification** — permission registry'den `(module, action)` tuple lookup; fallback yok, unknown → ConfigError. `scope_mode == 'protected_system'` ise kod-level invariant check ile döner (matrix'e girmez).
2. **Self-matrix-edit check** — `actor.id == target.id` ise `user_permissions` DENY (Owner dahil). Bu, Owner bypass'tan **önce** gelir.
3. **owner_bypass_exempt check** — registry'de true ise Owner bypass uygulanmaz.
4. **Owner bypass** — `is_owner` ve exempt değilse authorization matrix + scope bypass edilir (business validation **değil**), reason + audit ile ALLOW.
5. **Matrix lookup** — yoksa veya `scope_type == 'none'` ise DENY.
6. **Config validation** — matrix satırının `scope_type`'ı registry'nin `allowed_scope_types`'ında mı.
7. **Scope check** — read/update/delete için resolver predicate; create için payload validation; global scope filtreyi atlar.
8. **Reason check** (registry `reason_required` true ise) → **Audit + ALLOW**.

### 3.2 Permission registry ve sentinel namespace

Permission metadata'sının **tek source of truth'u** permission registry'dir; anahtar formatı `(module, action)` tuple, fallback yok. İki sentinel namespace:

- **`__global__`** — global capability ve field-level gate permission'lar (cross-cutting). Örn. `export_data`, `send_marketing_campaign`, `force_logout`.
- **`__protected__`** — protected system operations (örn. `grant_is_owner`, `revoke_is_owner`). Matrix'e **asla** girmez; DB-level CHECK (`module != '__protected__'`) migration'ın bile bunu bypass etmesini engeller.

Registry alanları: `category`, `scope_mode`, `allowed_scope_types`, `owner_bypass_exempt`, `reason_required`, `default_template_keys`, `audit_worthy`.

### 3.3 Scope mode'ları

`scope_mode` beş kategori:

| `scope_mode` | Anlam | `allowed_scope_types` | Namespace |
|---|---|---|---|
| `crud` | Standart modül CRUD | own, team, office, all, none | gerçek modül |
| `global_capability` | Cross-cutting capability | global, none | `__global__` |
| `record_bound` | Belirli record'a bağlı aksiyon | own, team, office, all, none | gerçek modül |
| `field_level_gate` | Field-level görünürlük (örn. `view_sensitive_finance`) | global, none | `__global__` |
| `protected_system` | Sistem invariant (matrix dışı) | — | `__protected__` |

`scope_type = 'global'` yalnızca `global_capability` ve `field_level_gate`'te kabul edilir; CRUD/record_bound'da global config error'dur. Scope hesaplaması **module-specific resolver pattern** ile yapılır: her modül bir **read resolver** (SQL predicate) ve bir **create resolver** (payload validation) sağlar. Resolver implementasyonları Aşama 3'e ait.

**Önemli nüans:** `global_capability` (örn. `export_data`, `send_marketing_campaign`) endpoint/capability kullanım iznidir; **data scope'u otomatik 'all' yapmaz**. Export veya campaign hedefindeki data set her zaman ilgili module'ün view scope resolver'ı ile filtrelenir (user'ın 'all leads' permission'ı yoksa `export_data` çağırsa bile yalnızca kendi scope'undaki lead'leri export eder).

### 3.4 Owner bypass disiplini

Owner bypass **yalnızca authorization katmanını** bypass eder, **business validation'ı değil**. Same-org kuralı, domain validation, required fields, FK integrity, finance invariants, pricing snapshot, state machine kuralları Owner için de aktiftir. Owner "her şeyi yapabilir" değil, "authorization matrix'in iznine takılmaz" demektir.

`approve_hard_delete` permission'ı matrix'te tutulur ama `owner_bypass_exempt = true` taşır — yani Owner bile bu permission olmadan hard delete'i tek başına onaylayamaz (çift onay disiplini korunur).

### 3.5 `permission_version` + `scope_version` mekanizması

Authorization değişiklikleri iki yöne ayrılır:

- **Access narrowing → immediate invalidation.** User deactivation, herhangi bir special permission revoke, `is_owner` revoke, `view_sensitive_finance` revoke, `reports_to`/`office_id` değişikliği, scope addition revoke/expire, `sales_agents.user_id` link değişikliği — bunlar `permission_version` / `scope_version` bump üretir ve LIFFY replica'sını **anında** invalidate eder.
- **Access expanding → polling kabul.** Yeni permission grant, template edit, scope addition ekleme — ~15-30 dk polling ile yayılır; manuel "force sync" UI'da mevcut.

`permission_version` ve `scope_version` JWT payload'ında taşınır (Bölüm 3.4). **Bu version'ların authoritative storage'ı (users tablosunda kolon mu, ayrı tablo mu, replica mı), update mekanizması ve freshness contract'ı Bölüm 3.7'de tanımlanır** — bu konsolidasyon noktasında 3.7 henüz kilitlenmedi; auth implementation final olmadan 3.7'nin tamamlanması gerekir (aşağıda Bölüm 7 scope cümlesi).

### 3.6 `force_logout` permission entry (v1.1 amendment batch)

Bölüm 3.3'te gündeme gelen admin force-logout endpoint'i için permission registry'ye eklenen entry (Bölüm 2 v1.1 amendment, Bölüm 3 final commit'inde uygulanır):

| Property | Value |
|---|---|
| `module` | `__global__` |
| `action` | `force_logout` |
| `scope_mode` | `global_capability` |
| `allowed_scope_types` | `[global]` |
| `reason_required` | `true` |
| `default_template_keys` | `[owner]` |
| `owner_bypass_exempt` | `false` |
| `audit_worthy` | `true` |
| `self_target_forbidden` | `true` (endpoint-level invariant) |

---

## 4. Bölüm 3 — Auth + Session

### 4.1 3.1 — Auth boundary ve actor model

Auth katmanı dört actor tipi tanır ve aralarına net sınır koyar: **user** (login eden kişi, JWT), **service** (service-to-service, ayrı audience — Bölüm 3.6), **contractor** (public form token, HMAC — Bölüm 1), **bot** (WhatsApp identity — Bölüm 3.11+). Her actor'ın kendi credential/token mekanizması vardır; bir actor tipinin token'ı başka bir actor'ın endpoint'inde **kabul edilmez** (cross-actor JWT yasağı). JWT minimal payload disiplini buradan gelir: token sadece **identity + session + version** taşır; mutable authorization fact'leri (is_owner, role, permission satırları, scope) taşımaz — bunlar her zaman source-of-truth'tan okunur.

**Service-to-service ve bridge çağrı auth (MVP minimum).** LEENA ↔ LIFFY arası bridge çağrıları (Köprü 1-5) ve internal service çağrıları için MVP auth modeli:

- **Service credential ayrı audience:** Internal service çağrıları `aud = 'service'` JWT veya pre-shared service token taşır; `aud = 'normal_access'` user JWT bu endpoint'lerde **kabul edilmez**.
- **Service permission matrix'e girmez:** Service capability whitelist / endpoint allowlist (statik config) ile yetkilendirilir. Permission registry user matrix'ine service satırı eklenmez.
- **Synchronous user-initiated call (örn. Köprü 1 quote push):** Çağıran service kendi credential'ı ile authenticate olur; user context `source_user_id` body field'ında **audit context olarak** taşınır. User JWT forward edilmez.
- **Async / event-driven call:** User authority taşınmaz; yalnızca `source_user_id` ve `source_event_id` audit metadata olarak iletilir.
- **External integration webhook'ları (Zoho sync, payment provider, vb.):** Service actor'dan **ayrı** kategoride. Provider signature validation + endpoint-bound registry (`integration_credentials` tablosu, Bölüm 2.3). Organization context webhook payload'ından kör alınmaz — trusted provider context'ten resolve edilir.

Detaylı service token issuance, rotation ve scope mekanizması Aşama 2 Bölüm 3.6'da netleşir.

### 4.2 3.2 — Credential lifecycle ve password reset

**Password policy NIST 800-63B yaklaşımı:** minimum 12 karakter, maksimum 128 (DoS koruması), karmaşıklık zorunluluğu yok (passphrase kabul), user'ın email/full_name'ini içeren ve bilinen weak password'ler yasak. Breached password check (HaveIBeenPwned) Phase 2 işareti.

**Hashing: Argon2id** (memory-hard); alternatif bcrypt (cost ≥12). PHC string format (algorithm + parametre + salt + hash) `password_hash`'te. Application-level pepper kullanılmaz (key rotation karmaşıklığı); secret manager + DB encryption-at-rest tercih edilir.

**Beş password flow:** initial set, change, forgot/reset, force reset, expire (Phase 2). Force reset iki delivery method destekler: (a) email_link — `primary_password_login_disabled = true` set edilir, primary hash korunur (same-password reuse check için); (b) temporary password — ayrı `temporary_password_hash` + `temporary_password_expires_at`, primary korunur.

**Password reset token'ları:** ayrı tabloda, HMAC-SHA256 + `hash_key_version` + `token_prefix` + `purpose` enum. Tek kullanımlık; kullanım sonrası `used_at` set.

**Brute-force koruması:** `failed_login_count` + `locked_until`. Credential verify başarısız olursa sayaç artar (eşik aşılırsa lock). Önemli transaction disiplini: verify başarısızlığında sayaç güncellemesi **commit edilir** (rollback edilmez — yoksa brute-force koruması fiilen çalışmaz).

**Restricted auth stage token (3.2 → 3.4):** Credential state satır 2/4/6'da (temp veya must-change), login başarılı credential verify sonrası dar yetkili bir "auth stage" token üretir. Bu token refresh üretmez, `sid` taşımaz, kısa TTL'lidir ve yalnızca password change + logout endpoint'lerinde geçerlidir.

### 4.3 3.3 — Session lifecycle ve refresh token

Bu, auth tasarımının merkezi parçasıdır. Access token kısa ömürlü JWT (default 15 dk); refresh token uzun ömürlü opaque random (default 30 gün).

**Token family ve rotation.** Bir login session = bir `token_family_id`. Her refresh kullanımında rotation zorunlu: eski token `used_at` ile işaretlenir, aynı family içinde yeni token üretilir (`parent_token_id` ile chain). Refresh token opaque storage HMAC-SHA256 + `hash_key_version` + `token_prefix` ile.

**Family absolute expiry.** `expires_at` family'nin mutlak son kullanma tarihidir — rotation parent'ın `expires_at`'ini **inherit eder**, ömrü uzatmaz. Yalnızca yeni family yaratan akışlar (login, password change) `now() + ttl` set eder. Bu, "30 günde bir refresh ile sonsuza kadar oturum" senaryosunu engeller (sliding expiration Phase 2 işareti).

**`auth_version_at_issue` ve session invalidation.** Her refresh token üretildiği andaki `users.auth_version` değerini taşır. `auth_version` bump'ı (password change, reset, force-logout, deactivate, reuse detection vb.) tüm eski token'ları geçersiz kılar: refresh sırasında `auth_version_at_issue != users.auth_version` ise token reddedilir + family revoke edilir. Access JWT de `auth_version` claim'i taşır; verify sırasında mismatch → reject.

**Reuse detection — üç branch.** Bir refresh token `used_at` set olduğu hâlde tekrar sunulursa (replay): (1) **Active family + family hâlâ aktif token taşıyor →** gerçek saldırı sinyali; family revoke + `auth_version` bump + audit + kullanıcıya/Owner'a bildirim. (2) **Active family ama family zaten kapanmış (repeat-reuse) →** ilk reuse'de zaten revoke edildi; bump yok, sadece security log (DoS koruması — saldırgan repeated trigger ile kullanıcıyı sürekli atamasın). (3) **Expired family replay →** bump yok, security log. Ayrımın özü: `auth_version` bump pahalı bir aksiyon (tüm session invalidate), yalnızca ilk gerçek tehditte tetiklenir.

**`sid` authoritative logout.** Access JWT `sid` claim'i (= `token_family_id`) taşır. Logout endpoint `sid`'i authoritative kabul eder: kullanıcının kendi session identifier'ıdır, logout her durumda `sid` family'sini revoke eder. Submitted refresh token cross-check için kullanılır (same-user + same-family); mismatch'te foreign family **asla** revoke edilmez (cross-user DoS koruması) ama actor'ın kendi `sid`'i yine revoke edilir. Single logout `auth_version` bump **yapmaz** (sadece o family); logout-all ve force-logout bump yapar.

**HMAC key retention (unexpired-row bazlı).** Bir `hash_key_version`, o key ile üretilmiş `expires_at > now()` token row'u var olduğu sürece verification set'inde tutulur — row state'i (active/used/revoked) önemli değil. Used+unexpired row'lar reuse detection için, revoked+unexpired row'lar forensics için lookup edilebilmelidir. Refresh token cleanup job da aynı disipline tabidir: used/revoked row'lar en az `expires_at`'a kadar tutulur, yoksa reuse detection bozulur. (Reset token retention'dan farklıdır: reset token kısa TTL'li ve tek kullanımlık olduğu için daha hızlı key rotation mümkün.)

**Üç logout endpoint'i:** `/auth/logout` (single session = family revoke, bump yok, iki mode — normal access vs restricted stage); `/auth/logout-all` (tüm family revoke + bump); `/auth/users/{id}/force-logout` (admin, `force_logout` permission, self-target yasak, reason zorunlu, target'ın tüm family revoke + bump + bildirim).

**Production davranış disiplinleri:** Rotation strict — eski token tek kullanımlık, client tek in-flight refresh ile serialize eder, response kaybında re-login akışına düşer (eski token ile retry reuse detection tetikler); MVP'de grace window yok. Post-commit issuance failure (signing/response construction commit sonrası fail) → ilgili family'nin newly-issued active token'ı best-effort revoke (`revocation_reason = 'issuance_failed'`), `login_success` audit yazılmaz, security log + client re-login.

### 4.4 3.4 — JWT detay

**Signing: RS256** (asymmetric). LEENA private key ile sign, LIFFY (ve gelecek consumer'lar) JWKS'ten public key ile verify. Asymmetric zorunlu — LIFFY'nin signing secret'ı paylaşması imkânsız. Algorithm whitelist disiplini: verifier yalnızca `RS256` kabul eder, `none`/HS256/diğer reddedilir (algorithm confusion koruması). RSA minimum 2048-bit (tercih 3072). ES256 Phase 2 işareti.

**Normal access JWT payload (closed schema — yalnızca şu key'ler):** `iss` (environment-specific issuer, exact match), `sub` (user_id), `org` (organization_id — cross-check; authoritative tenant context her zaman `users.organization_id`), `sid` (token_family_id), `auth_version`, `permission_version`, `scope_version`, `aud` (`"normal_access"`), `exp`, `iat`, `nbf`. Liste dışı claim reddedilir. **Mutable authorization fact'leri (is_owner, role, permissions, scopes, office_id vb.) JWT'de YASAK** — closed schema bunu enforce eder. `jti` taşınmaz (revocation `auth_version` bump üzerinden). Access `exp`, refresh family'nin `expires_at`'ini aşamaz (`exp = min(iat + ttl, family_expires_at)`).

**Restricted auth stage JWT (closed schema):** `iss`, `sub`, `org`, `aud` (`"auth_stage:password_change_only"`), `auth_version`, `exp`, `iat`, `nbf`. `sid`/`permission_version`/`scope_version` **taşımaz** (authorization matrix'e hiç girmez). Kısa TTL (5-10 dk). Yalnızca `/auth/password/change` + `/auth/logout` endpoint'lerinde geçerli.

**JWKS endpoint:** `GET /.well-known/jwks.json` public, RFC 7517 format, yalnızca public key material expose eder (private key/secret asla). LIFFY cache'ler (default TTL 1 saat). Key source-of-truth bir key registry'dir (`kid`, public key, `private_key_secret_ref`, `status` state machine: prepublished → signing → verifying_only → retired, timestamps). Header'da `jku`/`x5u`/`x5c`/`jwk` gibi key-source alanları **kesin yasak** (key confusion koruması); verifier yalnızca configured JWKS'i kullanır.

**Key rotation (graceful):** yeni keypair → JWKS'e ekle (prepublished) → cache convergence için bekle (>= cache max-age + buffer) → signing switch → eski kid `verifying_only` → doğal expire sonrası retire. Acil rotation (key compromise) immediate retire + verifier/CDN cache out-of-band invalidation; blast-radius response (global `auth_version` bump dahil) Bölüm 3.9 kapsamı.

**Verification disiplini (özet):** JWT lib'in standart RS256 + RFC 7519 verification'ı temel alınır. Ek mimari disiplinler: (1) closed schema enforce — mutable authorization fact'leri payload'da yasak, listenin dışındaki claim'ler reject; (2) `users` + `organizations` is_active check + org cross-check + `auth_version` mismatch verify-time'da uygulanır; (3) tüm verify failure'lar security_log'a düşer, audit_log'a yazılmaz; (4) trust boundary — signature verify edilmeden payload claim'leri authoritative loglanmaz. `permission_version` / `scope_version` mismatch handling Bölüm 7'de. Detay (pre-parse guard, type strictness, key rotation operasyonel detayları) implementation + code review kapsamında.

### 4.5 Restricted auth stage flow (uçtan uca)

Bir user temp password veya must-change state'inde (credential state satır 2/4/6) login olduğunda: credential verify başarılı olur ama normal access + refresh çifti **verilmez**; bunun yerine restricted auth stage JWT verilir. Bu token yalnızca password change ve logout yapabilir. User yeni password'ünü set ettiğinde: credential state satır 7'ye (normal active) geçer, `auth_version` bump olur (eski restricted token anında geçersizleşir), ve normal access + refresh çifti verilir. İki katmanlı güvenlik: (1) `auth_version` mismatch verify-time'da eski restricted token'ı keser; (2) password change transaction'ı state re-check yapar — state geçişi sonrası replay zaten reddedilir. Server-side restricted token invalidation MVP'de yok (stateless, kısa TTL); çalınmış restricted token kısa pencerede password change tetikleyebilir — **high-impact narrow-window risk**, MVP'de kabul edilmiş (token persist edilmez, TTL çok kısa, scope dar, bump + state re-check replay'i keser). Phase 2'de denylist opsiyonu. Bu MVP kararıdır — threat model değişirse veya compliance gerektirirse Phase 2'de stateful denylist (`jti` claim + `restricted_token_denylist` tablosu) eklenir.

---

## 5. Bölüm 5 — Audit

### 5.1 `audit_log` tablosu (yüksek seviye)

Audit log immutable bir kayıt akışıdır; kritik aksiyonları ve gerçek güvenlik olaylarını tutar. Entity referansları **logical reference** olarak tutulur (strict FK kurulmaz — yoksa hard delete FK constraint'e takılır ve audit log immutability'si bozulur). Yazım resilient: outbox + retry pattern (Aşama 1 A16), LEENA'nın kendi DB'sine yazar, LIFFY olayları köprü üzerinden akar.

`actor_type` enum'u (3.1-3.3 boyunca biriken koordinasyon): `user`, `system`, `migration`, `zoho_sync`, `integration`, `anonymous` (örn. password reset confirm — henüz authenticated olmayan aktör).

### 5.2 Audit-worthy vs security_log ayrımı

İki ayrı kanal, iki ayrı amaç:

- **`audit_log` (audit-worthy)** — kalıcı, kritik aksiyon ve gerçek güvenlik olayı kaydı. Örnekler: permission değişiklikleri, override aksiyonları, deactivate + hard delete, export, status değişiklikleri, sensitive data access, `is_owner` grant/revoke, hard delete second approval, `login_success`, `logout`/`logout_all`/`force_logout`, `refresh_token_reuse_detected` (yalnızca ilk gerçek active-family reuse), `session_terminated`, key rotation / emergency rotation / suspected key compromise. Permission registry'deki `audit_worthy` flag ile bağlanır.

- **`security_log` (audit-NOT-worthy, threshold alert kanalı)** — yüksek hacimli, beklenen veya gürültülü olaylar. Örnekler: tüm JWT verify failure'ları (invalid signature, expired, unknown kid, aud/iss mismatch, shape malformed, alg mismatch, vb.), `auth_version_mismatch` (beklenen durum — ana audit event zaten bump tetikleyicidir), `reuse_replay_after_family_closed`, `expired_used_token_replay_attempt`, `cross_user_or_family_logout_mismatch`, `login_denied_state`, `inactive_user_access_attempt`, `organization_inactive_access_attempt`, `token_issuance_failed`, `login_verify_failed`. Bu olaylar rate-limited/aggregated yazılır (yüksek-kardinalite alanlar — kid, IP, token fingerprint — cap'lenir); raw JWT veya credential asla loglanmaz.

Ayrımın özü: audit_log volume şişmesini önlemek + gerçek forensics değeri olan olayları izole etmek. Beklenen/gürültülü olaylar security_log'a düşer ve threshold alert pattern'i ile (örn. invalid webhook disiplini paraleli) anomali tespitine bağlanır.

---

## 6. Aşama 2 Bölüm 4, 6, 7, 8 — Açık alt bölümler (scope cümleleri)

Bu mimari bölümler (Aşama 2'nin kendi bölüm numaralandırması) henüz detaylı tasarlanmadı; implementation sırasında veya sonraki mimari turlarında netleşecek. Not: aşağıdaki "Bölüm N" etiketleri **Aşama 2 mimari bölüm numaralarıdır**, bu konsolide dokümanın `##` başlık numaralarıyla karıştırılmamalıdır. Scope tanımları:

**Aşama 2 Bölüm 4 — Reference data + LIFFY replikasyon.** Master reference tabloları (offices, countries, sectors, currencies, languages) LEENA'da merkezi tutulur; LIFFY'ye replikasyon mekanizması (read-only replica adayları: `users` subset, `organizations` non-sensitive, `data_entry_contractors`) ve version-based cache invalidation burada tanımlanır. Force sync UI/trigger ve scope cache expiry disiplini (TTL aktif scope addition expiry'sini aşamaz) bu bölümde.

**Aşama 2 Bölüm 6 — Finance + commission.** İki ayaklı para hareketi, computed balance, frozen exchange rate invariant'larının somut schema'sı (revenue, expense, multi-account ledger, owner's current account, commission engine). Sales agent banka/IBAN snapshot mekaniği (payment anında transaction record'una snapshot). Commission hem sales rep hem sales agent için (preset + override).

**Aşama 2 Bölüm 7 — Cache invalidation + propagation (auth implementation'ın ön koşulu).** `permission_version` / `scope_version` / `auth_version` mismatch'in propagation davranışı: immediate reject vs max-TTL stale window, LIFFY replica freshness contract, fail-open/fail-closed stratejisi. **Bu version'ların authoritative storage'ı ve update mekanizması burada kesinleşir** — JWT (4.4) bu claim'leri "required logical field" olarak işaretler ama fiziksel schema'sını varsaymaz. **Orkestrasyon kararı: önerilen sıra 3.4 (kilit) → 3.7 → 3.5 (LIFFY cross-app session) → 3.6 (service-to-service) → 3.8-3.13.** Aşama 2 Bölüm 7 kilitlenmeden auth implementation final olamaz çünkü JWT verification version mismatch handling'i buna bağlı. (Bölüm 3.4 ve 3.5 metnindeki "Bölüm 7" / "Bölüm 3.7" referansları bu mimari bölümü işaret eder.)

**Aşama 2 Bölüm 7 MVP minimum kararı.** Auth implementation'ın final olabilmesi için bu blok 3.7 detay tasarımından önce karar verir; detay tasarım sonradan revize edebilir:

- **Storage:** `permission_version` ve `scope_version` integer kolon olarak `users` tablosunda tutulur (NOT NULL DEFAULT 0). Ayrı tablo veya replica state mekanizması Phase 2 değerlendirmesi.
- **Bump events:** Bölüm 3.5'teki "access narrowing" listesindeki herhangi bir olay LEENA'da ilgili user'ın `permission_version` veya `scope_version` integer'ını +1 artırır (atomic UPDATE, transaction içinde).
- **LIFFY mismatch davranışı:** JWT verify'da `token.permission_version != users.permission_version` veya `token.scope_version != users.scope_version` durumunda LIFFY: (1) authoritative LEENA'dan fresh permission/scope state'i re-fetch eder, (2) cache'i invalidate eder, (3) request'i fresh state ile **continue** eder. Force-logout veya re-auth gerekmez — bu narrowing/expanding ayrımının "access narrowing" tarafıdır ve `auth_version` bump zaten oradan tetiklenmiştir (token o yolla reddedilir).
- **Max stale window:** Push-based bump kullanılırsa < 5 saniye; polling fallback için < 30 saniye (deployment config). Security-narrowing kritik olaylar (deactivate, `is_owner` revoke) `auth_version` bump ile zaten immediate kapatılır.

Detaylı freshness contract, replica replication mechanism, fail-open vs fail-closed edge case'leri Aşama 2 Bölüm 7 tasarımında netleşir.

**Aşama 2 Bölüm 8 — WhatsApp bot + channel restriction.** Bot user identification (phone_e164 + opt-in + verified_at lookup), WhatsApp opt-in verification flow, ve channel restriction layer (hassas field'lar WhatsApp kanalından dönmez). WhatsApp bot LEENA içinde yaşar, LIFFY verilerini `liffy_daily_metrics` + notifications stream üzerinden okur.

---

## 7. Implementation defaults (öneri, zorunlu değil)

Bu doküman implementation karar fazını başlatır. Önerilen baseline:

- **Database:** PostgreSQL 15+ (citext, uuid, jsonb desteği için)
- **Backend dilleri:** Node.js/TypeScript veya Python (FastAPI); takım uzmanlığına göre.
- **LEENA-LIFFY iletişim:** REST + JWT (gRPC Phase 2 değerlendirmesi).
- **Identity provider seçeneği:** İki yol açıktır — (a) sıfırdan LEENA yazımı (Bölüm 3'teki tüm detaylı disiplinleri kendiniz implement edersiniz), veya (b) hazır çözüm (Keycloak self-hosted, Supabase Auth, Auth0) üzerine ELL-spesifik permission matrix + organization isolation + restricted stage flow katmanı. Karar implementation kickoff'unda alınır; bu doküman her iki yöne de uygundur, ana mimari kararları (RS256, JWKS, refresh rotation, sid authoritative, auth_version, permission_version, scope_version) iki yolda da korunur — sadece kim implement ediyor değişir. **Sprint-0 kararı:** Auth provider seçimi (custom vs hazır çözüm) auth implementation başlamadan önce sprint-0'da kapatılmalıdır. ELL'in spesifik kuralları (`auth_version` bump kuralları, `__protected__` sentinel namespace, owner bypass'ın self-matrix-edit önceliği, restricted auth stage flow) hazır çözüme adapte edilirken trade-off analizini sprint-0'da değerlendir.
- **Repo yapısı:** Monorepo (LEENA + LIFFY + shared/ klasörleri) veya iki ayrı repo. Takım yapısına göre.

---

## Ek — Kanonik referans dokümanlar

Bu konsolide doküman aşağıdaki kilitli kanonik dokümanların distilasyonudur. Daha derin detay (tam schema, CHECK constraint formülasyonları, pseudocode, edge-case enumeration, karar gerekçelerinin tam tartışması) için bunlara inilir:

- `ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1_1.md` (A1-A29)
- `ELL_ARCHITECTURE_STAGE_2_SECTION_1_IDENTITY_v1_0.md` (B1-B20) + v1.1 amendment batch
- `ELL_ARCHITECTURE_STAGE_2_SECTION_2_PERMISSIONS_v1_0.md` (B21-B44) + v1.1 amendment batch
- 3.1 Auth boundary (C1-C12), 3.2 Credential lifecycle (C13-C25), 3.3 Session lifecycle (C26-C32), 3.4 JWT (C33-C39) — Bölüm 3 detaylı versiyonları

Implementation bu konsolide dokümandan başlar; bir karar için ek derinlik gerektiğinde ilgili kanonik dokümana iner.
