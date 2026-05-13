# ELL Mimari — Aşama 2, Bölüm 2: Permission Matrix + Hierarchy + Scope

**Sürüm:** v1.0 — Final
**Onaylanma tarihi:** 2026-05-12
**Onaylayan:** Suer (Owner)
**Durum:** ✅ Approved — locked
**Doküman türü:** Mimari karar — Aşama 2 Bölüm 2
**Ön koşul:** Aşama 1 v1.1, Aşama 2 Bölüm 1 v1.0
**Kapsam:** permission_templates, user_permissions matrix, permission registry (sentinel namespace), special permission master listesi, protected system operations, module-specific scope resolver pattern (read + create), authorization order, scope composition, hierarchy enforcement, template apply pattern, registry enforcement pipeline, scope-aware capability iki aşamalı authorization.
**Kapsam dışı:** Auth/JWT/session (Bölüm 3), permission cache invalidation detayı (Bölüm 3+4), reference data sync (Bölüm 4), audit log entity references + redaction + audit-worthy actions sınıflandırması (Bölüm 5), notification dispatch (Bölüm 6).

**Bu doküman v1.0 olarak finalize edilmiştir. Aşama 2 sonraki bölümleri ve Aşama 3 bu dokümanı kanonik referans olarak kullanır. Bölüm 2'ye dönüş ancak resmi bir amendment (v1.1) ile mümkündür.**

---

## 2.0 Bu bölümün amacı

Bölüm 1 üç identity'yi netleştirdi. Authorization üç kaynaklı (matrix + scope + `is_owner` flag).

Bu bölüm o üç kaynağın **somut schema** ve **enforcement kurallarına** bağlar. Karar sırası, scope hesaplama (read ve create), hierarchy enforcement, sistem invariant'larının Owner bypass'ından korunması, permission metadata'nın merkezi registry ile config error'a karşı korunması, sentinel namespace ile global/protected permission'ların matrix'te tutarlı saklanması, registry enforcement pipeline (API + migration + startup), authorization ile business validation ayrımı, scope-aware capability iki aşamalı kontrol — hepsi burada.

Requirements 3.1 + 3.4 kanonik kaynak.

---

## 2.1 Authorization order

```
1. Action classification (registry lookup):
   - PERMISSION_REGISTRY.get((module, action)) — tek lookup, fallback yok
   - Yoksa → ConfigError (unknown module+action)
   - scope_mode == 'protected_system' ise → kod-level invariant check, return

2. Self-matrix-edit check (Owner dahil):
   - actor.id == target.id ise user_permissions DENY (B32)

3. owner_bypass_exempt check:
   - registry'de true ise Owner bypass uygulanmaz, adım 5'e geç

4. Owner bypass:
   - user.is_owner ve owner_bypass_exempt değilse
   - authorization matrix + scope BYPASS (business validation DEĞİL — 2.1.1)
   - reason check + audit + ALLOW

5. Matrix lookup:
   matrix_row = user_permissions.find(user.id, module, action)
   if not matrix_row or scope_type == 'none': DENY

6. Config validation (registry):
   matrix_row.scope_type registry allowed_scope_types listesinde mi?

7. Scope check:
   - Read/update/delete: resolver predicate
   - Create: payload validation
   - global scope: scope filter atla
   - Scope additions: applies_to_action = current_action filtreli

8. Reason check (registry reason_required true ise)

9. Audit + ALLOW
```

### 2.1.1 Owner bypass scope — authorization vs business validation

**Owner bypass yalnızca authorization katmanını bypass eder. Business validation Owner için de çalışır.**

**Authorization-level (Owner bypass eder):**
- Matrix lookup
- Scope filter (resolver predicate)

**Authorization-level invariant'lar (Owner bypass ETMEZ):**
- Protected system operations, owner_bypass_exempt aksiyonlar, self-matrix-edit yasağı, last active Owner invariant, hard delete second approver, reason zorunluluğu, WhatsApp channel restriction, secret masking, audit log.

**Business validation (Owner için DE aktif):**
- Same-org validation (B19)
- Domain validation (valid currency, valid category, valid tax rate)
- Required fields, FK integrity
- Finance invariants (Aşama 1 A27): frozen exchange rate, two-sided money, computed balances
- Pricing snapshot/freeze (A14)
- State machine kuralları
- Module-specific business constraints

Authorization (kim ne yapabilir) ile business validation (yapılan iş valid mi) **ayrı katmanlardır**.

---

## 2.2 Permission/Action Registry — sentinel namespace ile tek format

### 2.2.1 Sentinel namespace stratejisi

Registry **tek key formatı** kullanır: `(module, action)` tuple. Global ve protected permission'lar için sentinel modül adları:

- **`__global__`** — global_capability ve field_level_gate action'lar için.
- **`__protected__`** — protected_system action'lar için.

Bu sayede:
- Schema'da `user_permissions.module NOT NULL` ve `permission_template_entries.module NOT NULL` karşılanır.
- Registry lookup'u tek formatta — fallback yok.
- Unknown module veya unknown action her zaman ConfigError üretir.

### 2.2.2 Registry örnekleri

**CRUD ve record_bound (gerçek modül):**

```python
PERMISSION_REGISTRY[('contracts', 'view')] = {...}
PERMISSION_REGISTRY[('contracts', 'create')] = {...}
PERMISSION_REGISTRY[('contracts', 'update')] = {...}
PERMISSION_REGISTRY[('contracts', 'delete')] = {...}
PERMISSION_REGISTRY[('contracts', 'change_contract_status')] = {...}     # record_bound
PERMISSION_REGISTRY[('contracts', 'convert_quote_to_contract')] = {...}  # record_bound

PERMISSION_REGISTRY[('leads', 'view')] = {...}
PERMISSION_REGISTRY[('audit', 'view')] = {...}     # ayrı default (Owner only)
PERMISSION_REGISTRY[('audit', 'view_own')] = {...} # tüm template'lerde default
```

**Global capability ve field-level gate (`__global__` namespace):**

```python
PERMISSION_REGISTRY[('__global__', 'export_data')] = {...}
PERMISSION_REGISTRY[('__global__', 'approve_hard_delete')] = {...}    # owner_bypass_exempt=true
PERMISSION_REGISTRY[('__global__', 'view_sensitive_finance')] = {...}
PERMISSION_REGISTRY[('__global__', 'send_marketing_campaign')] = {...}
PERMISSION_REGISTRY[('__global__', 'run_bulk_import')] = {...}
PERMISSION_REGISTRY[('__global__', 'manage_users')] = {...}
PERMISSION_REGISTRY[('__global__', 'manage_user_permissions')] = {...}
PERMISSION_REGISTRY[('__global__', 'manage_permission_templates')] = {...}
PERMISSION_REGISTRY[('__global__', 'manage_sales_agents')] = {...}
PERMISSION_REGISTRY[('__global__', 'manage_data_entry_contractors')] = {...}
PERMISSION_REGISTRY[('__global__', 'force_password_reset')] = {...}
PERMISSION_REGISTRY[('__global__', 'system_integrity_alerts')] = {...}
PERMISSION_REGISTRY[('__global__', 'manual_create_contract')] = {...}
PERMISSION_REGISTRY[('__global__', 'edit_operational_email_templates')] = {...}
PERMISSION_REGISTRY[('__global__', 'edit_marketing_email_templates')] = {...}
PERMISSION_REGISTRY[('__global__', 'edit_reference_data')] = {...}
PERMISSION_REGISTRY[('__global__', 'use_whatsapp_bot')] = {...}
PERMISSION_REGISTRY[('__global__', 'configure_notifications')] = {...}
```

**Protected system operations (`__protected__` namespace):**

```python
PERMISSION_REGISTRY[('__protected__', 'grant_is_owner')] = {scope_mode='protected_system', ...}
PERMISSION_REGISTRY[('__protected__', 'revoke_is_owner')] = {scope_mode='protected_system', ...}
```

### 2.2.3 Registry lookup pattern

```python
def lookup_registry(module, action):
    entry = PERMISSION_REGISTRY.get((module, action))
    if not entry:
        raise ConfigError(f"Unknown module+action: {module}, {action}")
    return entry
```

**Fallback yok.** Tek format. `(__global__, export_data)` ile `(contracts, view)` aynı şekilde lookup edilir.

**Davranış:**
- `module='fake_module'`, `action='export_data'` → registry'de yok → ConfigError
- `module='__global__'`, `action='export_data'` → registry'de var → entry döner
- `module='contracts'`, `action='view'` → registry'de var → entry döner
- `module='contracts'`, `action='unknown_action'` → ConfigError
- `module='__protected__'`, `action='grant_is_owner'` → registry'de var, scope_mode='protected_system'

### 2.2.4 Protected ops'un matrix'e sızma koruması

`__protected__` namespace permission'ları **matrix tablolarına insert edilemez**. Backend + DB-level çift koruma:

**Schema-level enforcement (DB CHECK):**

```sql
ALTER TABLE user_permissions
  ADD CONSTRAINT user_permissions_no_protected
  CHECK (module != '__protected__');

ALTER TABLE permission_template_entries
  ADD CONSTRAINT template_entries_no_protected
  CHECK (module != '__protected__');
```

Bu CHECK migration script veya bulk SQL insert ile bile bypass edilemez. Protected ops sadece kod-level invariant olarak yaşar.

**Backend enforcement (registry):**

API endpoint'leri matrix insert'te scope_mode kontrolü yapar:
```python
if def_meta.scope_mode == 'protected_system':
    raise ConfigError("Protected system operations cannot be stored in matrix")
```

İki katman birlikte protected ops'un matrix'e sızmasını mutlak engeller.

### 2.2.5 `scope_mode` semantiği

| `scope_mode` | Anlamı | `allowed_scope_types` | Namespace |
|---|---|---|---|
| `crud` | Standart CRUD | own, team, office, all, none | gerçek modül |
| `global_capability` | Cross-cutting capability | global, none | `__global__` |
| `record_bound` | Specific record'a bağlı | own, team, office, all, none | gerçek modül |
| `field_level_gate` | Field-level görünürlük | global, none | `__global__` |
| `protected_system` | Matrix dışı, kod-level | (matrix'te yazılamaz) | `__protected__` |

### 2.2.6 Registry entry alanları

```
{
    category: 'identity' | 'finance' | 'operational' | 'reporting' | 'bot',
    scope_mode: 'crud' | 'global_capability' | 'record_bound' | 'field_level_gate' | 'protected_system',
    allowed_scope_types: list of valid scope_type values,
    owner_bypass_exempt: boolean (default false),
    reason_required: boolean,
    default_template_keys: list of template_keys,
    audit_worthy: boolean (Bölüm 5 ile birlikte tanımlanır)
}
```

### 2.2.7 Authorization engine pseudocode

```python
def authorize(user, module, action, target_record_id_or_payload):
    # Tek format lookup, fallback yok
    def_meta = PERMISSION_REGISTRY.get((module, action))
    if not def_meta:
        raise ConfigError(f"Unknown module+action: {module}, {action}")
    
    # 1. Protected system check
    if def_meta.scope_mode == 'protected_system':
        return enforce_invariant(action, user, target_record_id_or_payload)
    
    # 2. Self-matrix-edit check (Owner dahil — B32)
    if action_modifies_user_permissions(action):
        target_user_id = extract_target_user_id(target_record_id_or_payload)
        if actor.id == target_user_id:
            return DENY
    
    # 3. Owner bypass (exempt değilse)
    if user.is_owner and not def_meta.owner_bypass_exempt:
        if def_meta.reason_required and not reason_provided():
            return DENY
        if def_meta.audit_worthy:
            audit_log(user, action, target_record_id_or_payload)
        return ALLOW
    
    # 4. Matrix lookup
    matrix_row = user_permissions.find(user.id, module, action)
    if not matrix_row or matrix_row.scope_type == 'none':
        return DENY
    
    # 5. Config validation
    if matrix_row.scope_type not in def_meta.allowed_scope_types:
        raise ConfigError("Invalid scope_type in matrix")
    
    # 6. Scope check
    if matrix_row.scope_type == 'global':
        pass  # capability check geçti, record-level scope yok
    elif action_is_create(action):
        if not validate_create_payload_scope(user, module, matrix_row.scope_type, payload):
            return DENY
    else:
        base_predicate = MODULE_RESOLVERS[module](user, matrix_row.scope_type)
        additions = active_scope_additions.filter(
            user_id=user.id,
            is_active=True,
            applies_to_module IN (None, module),
            applies_to_action=action,
            starts_at__lte=now(),
            (expires_at__isnull=True | expires_at__gt=now())
        )
        full_predicate = combine(base_predicate, additions)
        if not record_matches(target_record_id, full_predicate):
            return DENY
    
    # 7. Reason check
    if def_meta.reason_required and not reason_provided():
        return DENY
    
    # 8. Audit + ALLOW
    if def_meta.audit_worthy:
        audit_log(user, action, target_record_id_or_payload)
    return ALLOW
```

---

## 2.3 Protected System Operations

Backend kod-level invariant. Registry'de `__protected__` namespace'te, schema'da matrix tablolarına yazılamaz (CHECK constraint).

| Operasyon | Invariant kuralı |
|---|---|
| `grant_is_owner` | Sadece mevcut Owner. `actor.id ≠ target.id`. Reason + audit + notification. |
| `revoke_is_owner` | Sadece mevcut Owner. Son aktif Owner invariant. Reason. |
| Last active Owner invariant | Deactivate / hard delete / revoke_is_owner aktif Owner sayısı 1 ise reddedilir. |
| Hard delete second approver validation | Bölüm 1 B5 kuralları. |
| Self-escalation prevention | Self-matrix-edit yasağı, hierarchy self-promotion yasağı. |

**UI yeri:** User Profile > Security > Owner Status (matrix tablosunda görünmez).

---

## 2.4 `permission_templates` tablosu

### 2.4.1 Schema

```sql
CREATE TABLE permission_templates (
  id                          uuid PRIMARY KEY,
  organization_id             uuid NOT NULL REFERENCES organizations(id),
  
  template_key                text,                            -- system: NOT NULL + immutable, custom: NULL zorunlu
  name                        text NOT NULL,
  description                 text,
  
  version                     integer NOT NULL DEFAULT 1,
  
  is_system_template          boolean NOT NULL DEFAULT false,
  
  is_active                   boolean NOT NULL DEFAULT true,
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
  
  -- Sistem'de template_key NOT NULL, custom'da NULL zorunlu
  CHECK (
    (is_system_template = true AND template_key IS NOT NULL)
    OR (is_system_template = false AND template_key IS NULL)
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
  )
);

CREATE UNIQUE INDEX permission_templates_org_name_active
  ON permission_templates (organization_id, name)
  WHERE is_active = true;

CREATE UNIQUE INDEX permission_templates_org_key_active
  ON permission_templates (organization_id, template_key)
  WHERE is_active = true AND template_key IS NOT NULL;
```

**`template_key` immutable enforcement:** Backend update endpoint'i `template_key` değişikliğini reddeder. Sadece migration/seed sırasında set edilir.

**Sistem template key listesi:**
```
owner, project_department_lead, project_staff, sales_manager,
sales_team_lead, sales_rep, local_office_sales, local_office_project,
finance, admin
```

### 2.4.2 `permission_template_entries`

```sql
CREATE TABLE permission_template_entries (
  id                          uuid PRIMARY KEY,
  template_id                 uuid NOT NULL REFERENCES permission_templates(id),
  
  module                      text NOT NULL,
  action                      text NOT NULL,
  scope_type                  text NOT NULL
                              CHECK (scope_type IN ('own','team','office','all','none','global')),
  scope_rule                  text NOT NULL DEFAULT 'allow'
                              CHECK (scope_rule = 'allow'),       -- MVP: deny yasak (DB-level)
  
  -- Protected ops matrix'e sızamaz
  CHECK (module != '__protected__'),
  
  created_at                  timestamptz NOT NULL DEFAULT now(),
  
  UNIQUE (template_id, module, action)
);
```

**`scope_rule = 'allow'` DB-level CHECK:**

- MVP süresince schema-level enforcement: `scope_rule` yalnızca `'allow'` kabul eder. `'deny'` insert/update DB tarafından reddedilir.
- Migration script'leri veya seed bulk import bile bu CHECK'i bypass edemez.
- Phase 2'de deny aktive edilirken bu CHECK constraint DROP edilir, enforcement kod-level'a geçer.

**Entries actor pattern:** Bu tabloda actor field'ları yok. Değişiklikler **template version bump + audit event payload** üzerinden izlenir.

### 2.4.3 Sistem template'ler — hard delete + deactivate yasak

Sistem template'ler (`is_system_template = true`) **hard delete edilemez** ve **deactivate edilemez**. Sadece `name`, `description`, entries edit edilebilir. Core authorization vocabulary'sini korur.

Custom template'ler: deactivate edilebilir, hard delete için Bölüm 1 B5.

### 2.4.4 Template lifecycle

**Create custom:** `manage_permission_templates`. Audit.

**Edit (custom veya sistem):** Version++. Mevcut user matrix'leri etkilenmez. Audit log: entries payload diff.

**Deactivate custom:** Reason zorunlu. *Sistem template'ler için kapalı.*

**Hard delete custom:** B5 second approver. *Sistem template'ler için kapalı.*

---

## 2.5 `user_permissions` matrix

### 2.5.1 Schema

```sql
CREATE TABLE user_permissions (
  id                          uuid PRIMARY KEY,
  user_id                     uuid NOT NULL REFERENCES users(id),
  
  module                      text NOT NULL,
  action                      text NOT NULL,
  scope_type                  text NOT NULL
                              CHECK (scope_type IN ('own','team','office','all','none','global')),
  scope_rule                  text NOT NULL DEFAULT 'allow'
                              CHECK (scope_rule = 'allow'),
  
  source_template_id          uuid REFERENCES permission_templates(id),
  source_template_version     integer,
  is_exception                boolean NOT NULL DEFAULT false,
  
  created_at                  timestamptz NOT NULL DEFAULT now(),
  created_by                  uuid REFERENCES users(id),
  created_by_actor_type       text NOT NULL DEFAULT 'user'
                              CHECK (created_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  updated_at                  timestamptz NOT NULL DEFAULT now(),
  updated_by                  uuid REFERENCES users(id),
  updated_by_actor_type       text
                              CHECK (updated_by_actor_type IS NULL OR updated_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  -- Protected ops matrix'e sızamaz
  CHECK (module != '__protected__'),
  
  CHECK (
    (created_by_actor_type = 'user' AND created_by IS NOT NULL)
    OR (created_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    updated_by_actor_type IS NULL
    OR (updated_by_actor_type = 'user' AND updated_by IS NOT NULL)
    OR (updated_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  UNIQUE (user_id, module, action)
);

CREATE INDEX user_permissions_user_module
  ON user_permissions (user_id, module);
```

### 2.5.2 `scope_type` enum semantiği

| Değer | Anlamı |
|---|---|
| `own` | Kullanıcının kendi kayıtları (module resolver "own" predicate) |
| `team` | Own + recursive direct report'lar |
| `office` | Same-office user'lar; `office_id IS NULL` ise `own` fallback |
| `all` | Organization içindeki tüm kayıtlar |
| `none` | Hiç |
| `global` | Capability — registry'de `global_capability` / `field_level_gate` action'larda kabul edilir |

### 2.5.3 `global` semantiği

**`global` "her şeye erişim" demek DEĞİL.** Action'ın kendisinin record-level target'ı olmadığı anlamına gelir. Target data ilgili module resolver scope'undan geçer.

Backend registry üzerinden enforce eder: `global` yalnızca `scope_mode IN ('global_capability', 'field_level_gate')` olan action'larda kabul edilir. CRUD ve record_bound action'larda `global` config error olarak reddedilir.

### 2.5.4 Granular schema, sade UI

Backend full granular. UI **template + exception** sade gösterim:

1. **Default view:** "Bu kullanıcı `Sales Rep` template'inden yaratıldı."
2. **Exception list:** `is_exception = true` satırlar.
3. **"Tüm matrix'i göster" toggle:** Full granular, default kapalı.
4. **Exception ekleme:** Module → action → scope → `is_exception = true`.

**UI sentinel gizleme disiplini:**

`module = '__global__'` permission satırları normal modül listesinde gösterilmez (sentinel kullanıcıya görünmez technical detail). UI'da ayrı bir **"Capabilities"** veya **"Global Permissions"** bölümünde listelenir.

`module = '__protected__'` zaten matrix'te yazılamaz (schema CHECK); UI'da hiç görünmez. Protected ops User Profile > Security > Owner Status bölümünde yönetilir.

Detay UI tasarımı Aşama 3.

### 2.5.5 Template apply pattern

**Aksiyon A — "Apply latest template, preserve exceptions" (DEFAULT):**
- `is_exception = false` satırlar template yeni hale göre güncellenir.
- `is_exception = true` satırlar dokunulmaz.
- UI'da preview/diff.
- Audit.

**Aksiyon B — "Reset to template" (TEHLİKELİ):**
- **Diff preview zorunlu** (silinecek exception'lar + eklenenler + korunanlar).
- Reason field zorunlu.
- Confirmation modal.
- "Confirm" butonu diff preview'dan sonra aktif.
- Backend: tüm satırlar silinip template yeniden kopyalanır.
- Audit.

---

## 2.6 Special permission master listesi

Matrix'te saklanan special permission'lar. Protected system ops (2.3) bu listede değil.

### 2.6.1 Identity & system

| Permission | `scope_mode` | `owner_bypass_exempt` |
|---|---|---|
| `manage_users` | `global_capability` | false |
| `manage_sales_agents` | `global_capability` | false |
| `manage_data_entry_contractors` | `global_capability` | false |
| `manage_permission_templates` | `global_capability` | false |
| `manage_user_permissions` | `global_capability` | false |
| `approve_hard_delete` | `global_capability` | **true** |
| `force_password_reset` | `global_capability` | false |
| `system_integrity_alerts` | `global_capability` | false |

### 2.6.2 Finance

| Permission | `scope_mode` | Açıklama |
|---|---|---|
| `view_sensitive_finance` | `field_level_gate` | Field-level gate (2.6.7) |
| `view_other_users_commission` | `crud` (own/team/office/all) | Başka user commission |
| `approve_refund` | `record_bound` | Specific refund |
| `override_price_discount` | `record_bound` | Quote/contract override |
| `override_commission_rate` | `record_bound` | Contract bazında override |
| `change_contract_status` | `record_bound` | Status değiştirme |
| `edit_payment_after_save` | `record_bound` | Payment edit |

### 2.6.3 Operational

| Permission | `scope_mode` | Açıklama |
|---|---|---|
| `convert_quote_to_contract` | `record_bound` | Köprü 1 |
| `manual_create_contract` | `global_capability` | Akış B |
| `override_stand_reservation` | `record_bound` | Köprü 3 |
| `edit_operational_email_templates` | `global_capability` | Welcome, vb. |
| `edit_marketing_email_templates` | `global_capability` | Mass marketing |
| `send_marketing_campaign` | `global_capability` | Scope-aware (2.6.8) |
| `send_operational_email_chain_manually` | `record_bound` | 8-mail Announcement |
| `edit_reference_data` | `global_capability` | Countries, sectors |

### 2.6.4 Reporting & audit

| Permission | `scope_mode` | Açıklama |
|---|---|---|
| `view_audit_log` | `global_capability` | Audit log read (delegation redaction notu — 2.14) |
| `view_own_audit_log` | `crud` (own) | Self-audit |
| `export_data` | `global_capability` | Scope-aware (2.6.8) |
| `run_bulk_import` | `global_capability` | Migration / bulk |

### 2.6.5 Bot/notification

| Permission | `scope_mode` | Açıklama |
|---|---|---|
| `use_whatsapp_bot` | `global_capability` | WhatsApp bot erişimi |
| `configure_notifications` | `global_capability` | Sistem-wide notif default |

### 2.6.6 Sistem template default'ları — risky permission map

| Permission | Default (`template_key`) |
|---|---|
| `approve_hard_delete` | **Hiçbir template'e atanmaz** (Owner manuel verir) |
| `manage_user_permissions` | owner |
| `manage_users` | owner |
| `manage_permission_templates` | owner |
| `view_sensitive_finance` | finance, owner |
| `view_audit_log` | **owner only** (delegation redaction notu, 2.14) |
| `view_own_audit_log` | **Tüm template'lerde default** |
| `run_bulk_import` | owner |
| `export_data` | owner |
| `edit_reference_data` | owner (selective delegation) |
| `send_marketing_campaign` | sales_manager, owner — **sales_rep'e değil** |
| `edit_marketing_email_templates` | sales_manager, owner — **sales_rep'e değil** |
| `edit_operational_email_templates` | project_department_lead, owner |
| `convert_quote_to_contract` | project_department_lead (default), project_staff explicit delegation |
| `change_contract_status` | project_department_lead, owner |
| `manual_create_contract` | project_department_lead, owner |
| `override_stand_reservation` | project_department_lead (default), project_staff değil |
| `override_price_discount` | sales_manager, project_department_lead, owner |
| `override_commission_rate` | project_department_lead, owner |
| `approve_refund` | owner (sales_manager + project_department_lead opsiyonel) |
| `force_password_reset` | owner (delegated authorized user) |
| `system_integrity_alerts` | owner (delegated authorized user) |
| `use_whatsapp_bot` | owner (Phase 1) |
| `configure_notifications` | owner |

**Project Staff disiplini:** `convert_quote_to_contract` ve `override_stand_reservation` Project Staff default'unda **yok** — kalite gate'i kritik. Project Department Lead default, Staff'a Owner explicit delegate eder.

**Sales Rep marketing kısıtı:** `send_marketing_campaign` ve `edit_marketing_email_templates` sales_rep'te yok (deliverability/marka riski). Phase 2'de dar permission'lar düşünülebilir.

### 2.6.7 `view_sensitive_finance` — field-level gate

`view_sensitive_finance` permission'ı **field-level gate**'dir: zaten erişilebilen finance kayıtlarındaki hassas field'ları (salary, IBAN, bank account, tax_id) görme hakkı verir. **Record-level erişim vermez** — kullanıcı hangi finance kayıtlarına erişeceğini ilgili module resolver'dan (payments, contracts, expenses) öğrenir. Bu permission o resolver'ın **üstüne field-level ek katman**dır.

**Pratik:**
- Finance template + `view_sensitive_finance` + `payments view all scope` → tüm payment'lar + hassas field'lar görünür.
- Sales Manager (no sensitive) + `payments view team scope` → kendi takım payments'ları görünür ama IBAN/salary maskelidir.

WhatsApp channel restriction bu permission'lı user'lar için de geçerli (Bölüm 8).

### 2.6.8 `export_data` ve `send_marketing_campaign` — scope-aware capability + iki aşamalı authorization

**`export_data`:** Capability verir, kayıt seti ilgili module view scope ile sınırlı.

**`send_marketing_campaign`:** Capability verir, hedef kitle lead modülü view scope'undan.

**Endpoint enforcement pattern — iki aşamalı authorization:**

Scope-aware capability endpoint'leri **iki authorize() çağrısı** yapar:

**Aşama 1 — Capability check:**

```python
# Capability'nin kendisine sahip mi?
authorize(user, '__global__', 'export_data', payload=None)
# Registry: ('__global__', 'export_data')
# scope_mode = 'global_capability'
# User'da matrix satırı var mı? Yoksa DENY.
```

**Aşama 2 — Target data scope check:**

```python
# Hangi modüldeki data export edilecek?
target_module = payload.target_module   # 'contracts', 'leads', vb.

# Target module'de view yetkisi nedir?
authorize(user, target_module, 'view', target_record_id=None)
# Registry: (target_module, 'view')
# scope_mode = 'crud'
# User'ın target_module view scope'u: own/team/office/all/none

# Export query bu scope predicate ile filtrelenir
predicate = MODULE_RESOLVERS[target_module](user, view_scope_type)
return db.[target_module].findAll(where=predicate)
```

**Pratik örnekler:**

- **`export_data` + `target_module='contracts'`** → `__global__.export_data` capability + `contracts.view` scope resolver. Export edilen contract set'i kullanıcının contracts view scope'una göre filtrelenir.

- **`send_marketing_campaign` + `target_module='leads'`** → `__global__.send_marketing_campaign` capability + `leads.view` scope resolver. Campaign target lead set'i kullanıcının leads view scope'una göre filtrelenir.

**Net davranış:**

Hedef data seti her zaman target_module'un view scope'una göre filtrelenir. Organization-wide için kullanıcının target_module'da `all` scope'u veya `is_owner` flag'i gerekir.

Sales Manager `export_data` capability'sine sahip + `leads.view team` scope'una sahip → export sadece team lead'lerini içerir, organization-wide değil. `is_owner` veya `leads.view all` olmadıkça tüm leads'leri export edemez.

---

## 2.7 Override reason zorunlu aksiyonlar

Registry `reason_required = true` flag.

### 2.7.1 Enforcement pattern

Reason ilgili **action log / status history / audit event / override history** üzerinde zorunlu. Pattern aksiyon tipine göre:

- **Entity-bağlı** (deactivate, hard delete, token revoke): schema-level `NOT NULL` / CHECK.
- **Transaction-bağlı** (refund approval, status change, payment edit): transaction record'da `NOT NULL` / CHECK.
- **Permission değişikliği**: audit log event payload zorunlu.
- **Override**: `override_history` tablosunda zorunlu.

### 2.7.2 Liste

1. `override_price_discount`
2. `override_commission_rate`
3. `override_stand_reservation`
4. `approve_refund`
5. `change_contract_status`
6. `edit_payment_after_save`
7. `run_bulk_import`
8. `manage_user_permissions` (any change)
9. `grant_is_owner` / `revoke_is_owner`
10. `approve_hard_delete` (second approver action)
11. User / sales_agent / contractor deactivate
12. User / sales_agent / contractor hard delete
13. `force_password_reset`
14. Token revoke (contractor)
15. `permission_templates` deactivate/hard delete (custom)
16. Template "Reset to template"

---

## 2.8 Self-escalation prevention

**Genel kural:**

> **Hiçbir user kendi permission matrix'ini düzenleyemez, Owner dahil.**
> Backend: `actor.id = target.id` ise `user_permissions` üzerinde insert/update/delete her zaman **DENY** (authorization order adım 2 — Owner bypass'tan ÖNCE).

### 2.8.1 İstisnalar (matrix dışı, ayrı endpoint'ler)

User kendi profil alanlarını düzenleyebilir:
- `password`
- Notification preferences
- `preferred_language`
- `timezone`
- `display_name`
- `phone_e164` + WhatsApp opt-in flow

### 2.8.2 Diğer kurallar

1. `is_owner` self-grant yasak (protected op).
2. **Hierarchy self-promotion yasak:** User kendi `reports_to`, `profile_template_id`, `office_id`, `is_owner`'ı değiştiremez.
3. `grant_is_owner` / `revoke_is_owner`: sadece mevcut Owner, `actor.id ≠ target.id`.

---

## 2.9 Hierarchy: `reports_to` enforcement

### 2.9.1 Hierarchy kuralları (atomic)

1. **Self-report yasak.** `target.reports_to ≠ target.id`.

2. **Descendant-report yasak.** Recursive CTE cycle check:
   ```sql
   WITH RECURSIVE descendants AS (
     SELECT id FROM users WHERE reports_to = :target_id
     UNION ALL
     SELECT u.id FROM users u JOIN descendants d ON u.reports_to = d.id
   )
   SELECT 1 FROM descendants WHERE id = :new_manager_id;
   ```

3. **Same-org check** (Bölüm 1 B19).

4. **Active manager check.** `new_manager.is_active = true`.

5. **`is_owner = true` user için `reports_to = NULL` zorunlu.**

### 2.9.2 Hierarchy değişikliği etkileri

Anında etki. Audit + 3 notification (target, eski/yeni manager).

### 2.9.3 Direct report reassignment

User deactivate'te zorunlu reassign (Bölüm 1 B6). Reassignment 2.9.1 kurallarından geçer.

**Owner istisnası (Bölüm 1 B6 cross-reference):** `is_owner = true` user organizational debt bırakabilir — `reports_to = NULL` set edilir, audit'lenir. Bu istisna 2.9.1 madde 4 (active manager check) ve madde 2 (descendant) ile uyumlu — manager olmadığı için bu kurallar tetiklenmez. Diğer kullanıcılar için reassignment zorunlu.

---

## 2.10 Scope composition — module-specific resolver pattern

### 2.10.1 Resolver kavramı

Her modül kendi resolver'ı:

```
resolveScope(current_user, scope_type, module) → SQL predicate (read için)
validateCreatePayload(current_user, scope_type, payload) → boolean (create için)
```

### 2.10.2 Örnek read resolver'lar (illüstratif)

```
leads resolver:
  own → WHERE assigned_user_id = current_user.id
  team → WHERE assigned_user_id IN (recursive team user_ids)
  office → WHERE assigned_user_id IN (same-office user_ids)
  all → WHERE TRUE
  none → WHERE FALSE

contracts resolver (Aşama 3 prerequisite — 2.10.3):
  own → WHERE created_by = current_user.id
         OR sales_agent_id IN (SELECT id FROM sales_agents WHERE user_id = current_user.id)
  ...

payments resolver (inherit):
  WHERE contract_id IN (SELECT id FROM contracts WHERE <contracts resolver>)

catalogue resolver (inherit):
  WHERE expo_id IN (...) OR customer_company_id IN (...)

floor_plan resolver (inherit):
  WHERE expo_id IN (...)

stand_reservations resolver:
  own → WHERE sales_rep_user_id = current_user.id
  team → ...
```

### 2.10.3 Contract resolver — Aşama 3 PREREQUISITE

**Bu açık konu değil, Aşama 3 prerequisite'idir.**

Contract modülü tasarlanırken **explicit ownership alanları** tanımlanmadan contract resolver implement edilmemelidir:

- `sales_owner_user_id` — contract'ın sales tarafından sorumlu user'ı
- `account_owner_user_id` — müşteri sorumlusu
- `responsible_project_user_id` — operasyonel sorumlu

**Gerçek gediği:** External sales_agent user'a bağlı değil (`sales_agents.user_id = NULL`). Akış B'de Yaprak external agent adına contract yaratırsa, sadece `sales_agent.user_id` üzerinden visibility kurulması çatlar.

Bu Aşama 3 contract modülü tasarlanırken **kapatılmalıdır**, atlanmamalıdır.

### 2.10.4 List queries vs record-specific vs create

**List query (read):**
```sql
SELECT * FROM contracts WHERE <effective_predicate>
```

**Record-specific check (read/update/delete):**
```sql
SELECT 1 FROM contracts WHERE id = :target_id AND (<effective_predicate>)
```

**Create — payload validation (2.10.7):**
Create action'da henüz record yok. Resolver, payload'daki ownership alanlarını scope_type ile validate eder.

### 2.10.5 `office` scope + `office_id IS NULL`

HQ user için `own` fallback (DENY değil). HQ user kazara kilitlenmez.

### 2.10.6 `user_scope_additions` tablosu

```sql
CREATE TABLE user_scope_additions (
  id                          uuid PRIMARY KEY,
  user_id                     uuid NOT NULL REFERENCES users(id),
  
  scope_rule                  text NOT NULL DEFAULT 'allow'
                              CHECK (scope_rule = 'allow'),       -- MVP: deny yasak (DB-level)
  
  target_entity_type          text NOT NULL
                              CHECK (target_entity_type IN (
                                'user','expo','office','contract',
                                'sales_agent','customer_company','lead','quote'
                              )),
  target_entity_id            uuid NOT NULL,
  
  applies_to_module           text,                            -- NULL: all modules
  applies_to_action           text NOT NULL DEFAULT 'view',    -- B37 action-level
  
  reason                      text NOT NULL,
  
  starts_at                   timestamptz NOT NULL DEFAULT now(),
  expires_at                  timestamptz,
  
  is_active                   boolean NOT NULL DEFAULT true,
  revoked_at                  timestamptz,
  revoked_by                  uuid REFERENCES users(id),
  revoked_by_actor_type       text,
  revocation_reason           text,
  
  created_at                  timestamptz NOT NULL DEFAULT now(),
  created_by                  uuid REFERENCES users(id),                 -- nullable (system actor)
  created_by_actor_type       text NOT NULL DEFAULT 'user'
                              CHECK (created_by_actor_type IN ('user','system','migration','zoho_sync')),
  
  CHECK (
    (is_active = true AND revoked_at IS NULL)
    OR (is_active = false AND revoked_at IS NOT NULL AND revocation_reason IS NOT NULL)
  ),
  
  CHECK (
    (created_by_actor_type = 'user' AND created_by IS NOT NULL)
    OR (created_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (
    revoked_by_actor_type IS NULL
    OR (revoked_by_actor_type = 'user' AND revoked_by IS NOT NULL)
    OR (revoked_by_actor_type IN ('system','migration','zoho_sync'))
  ),
  
  CHECK (expires_at IS NULL OR expires_at > starts_at),
  
  -- Sentinel namespace yasağı: scope addition sadece gerçek business modüllerinde anlamlıdır.
  -- '__global__' ve '__protected__' sentinel'leri için scope addition kavramsal olarak geçersiz.
  CHECK (applies_to_module IS NULL
         OR applies_to_module NOT IN ('__global__', '__protected__'))
);

CREATE INDEX user_scope_additions_user_active
  ON user_scope_additions (user_id)
  WHERE is_active = true;
```

**`applies_to_action` davranışı:** Resolver scope addition'ı sadece query'nin action'ıyla eşleşen row'lar için uygular. "Bengü Polidoro'yu görsün" (view) ile "Bengü Polidoro'yu editlesin" (update) ayrı satırlar gerektirir.

**Module compatibility validation:** Her `target_entity_type + applies_to_module + applies_to_action` kombinasyonu geçerli değil. Application-layer validation:

```
target=user → leads, quotes, contracts modülleri
target=office → leads, quotes, contracts
target=expo → contracts, catalogue, floor_plan
target=contract → contracts, payments, catalogue
target=sales_agent → contracts, commission
```

Detay matrix Aşama 3'te.

**Same-organization validation** (Bölüm 1 B19 pattern, application-layer).

### 2.10.7 Create queries — payload validation

**Create action scope semantiği:**

Create action için resolver mevcut kayıt üzerinde değil, **oluşturulacak kaydın payload'ı** üzerinde çalışır. Resolver, payload'daki ownership alanlarının scope_type'a uyup uymadığını validate eder.

**Pattern (modül modül Aşama 3'te detay):**

```
leads.create own → payload.assigned_user_id == current_user.id zorunlu
leads.create team → payload.assigned_user_id IN team_user_ids
leads.create office → payload.assigned_user_id IN same-office user_ids
leads.create all → any valid user

contracts.create own → 
  sales_owner_user_id, account_owner_user_id, responsible_project_user_id
  alanları current_user'a uygun
contracts.create team → ownership alanları team_user_ids içinde
contracts.create all → organization içindeki herhangi geçerli ownership

quotes.create own → assigned_user_id veya owner_user_id current_user
```

**Sızıntı koruması:** Sales rep `leads.create own` ile başka birinin adına kayıt yaratamaz; payload validation `assigned_user_id`'yi `own` scope'a göre kontrol eder.

**Create resolver ve scope additions etkileşimi:**

Create resolver, payload validation sırasında **sadece `applies_to_action = 'create'` olan aktif scope addition'ları** dikkate alır. `applies_to_action = 'view'` veya `'update'` için verilmiş scope addition **create yetkisi yaratmaz**.

**Pratik örnek:**

1. Bengü'ye "Polidoro contract'ını görsün" exception verildi:
   - `applies_to_module = 'contracts'`
   - `applies_to_action = 'view'`
   - `target_entity_id = polidoro_contract_id`

2. Bengü'nün `contracts.create own` permission'ı var.

3. Bengü Polidoro adına yeni contract yaratmaya çalışırsa:
   - Create resolver scope additions'ı kontrol eder.
   - `applies_to_action = 'create'` filtreli arar.
   - Bulamaz (view addition'ı sayılmaz).
   - Sadece base `own` scope ile validate eder → payload ownership Bengü'ye uymalı.
   - Polidoro adına yaratım denemesi → DENY.

4. "Bengü Polidoro adına contract yaratsın" için ayrıca:
   - `applies_to_module = 'contracts'`
   - `applies_to_action = 'create'`
   - `target_entity_type = 'customer_company'` veya `'user'`
   - `target_entity_id = polidoro_owner_user_id`
   - satırı gerekir.

Bu B37 ile tam uyumlu: **view addition update/delete/create yetkisi vermez**. Her action için ayrı addition satırı zorunlu.

### 2.10.8 Query layer enforcement

Scope **query layer**, UI değil. Backend resolver helper kullanımı zorunlu (code review).

---

## 2.11 LIFFY matrix sync

### 2.11.1 Genel kural

> Access narrowing → immediate
> Access expanding → polling kabul + manuel force sync optional

### 2.11.2 Critical (immediate invalidation)

- User deactivation/reactivation
- Permission revoke (herhangi bir special permission)
- `is_owner` revoke
- `approve_hard_delete` revoke
- `view_sensitive_finance` revoke
- `manage_user_permissions` revoke
- WhatsApp bot access revoke
- `reports_to` değişikliği
- `office_id` değişikliği
- `user_scope_additions` revoke
- `user_scope_additions` expire (effective scope daralması)
- `sales_agents.user_id` link değişikliği
- `is_active` flag (sales_agent, user)

`permission_version` / `scope_version` bump üretir, LIFFY anında invalidate eder. Mekanizma Bölüm 3 + 4.

### 2.11.3 Non-critical (polling 15-30 dk)

- Yeni permission grant
- Template edit
- `user_scope_additions` ekleme (allow)
- Display field değişiklikleri
- `preferred_language`, `timezone`

Manuel "force sync" UI'da mevcut (Bölüm 4).

---

## 2.12 Registry enforcement pipeline

Permission registry **gerçek source of truth**. Schema CHECK'ler ile registry birlikte enforcement.

### 2.12.1 API/UI katmanı

- Registry lookup: `(module, action)` tuple, fallback yok. Unknown → 400.
- `allowed_scope_types` validation: invalid kombinasyon → 400.
- `scope_rule = 'deny'` MVP'de 400.
- `module = '__protected__'` insert → 400 (kod-level + DB CHECK).

### 2.12.2 Migration/seed/bulk import katmanı

Schema CHECK'ler:
- `scope_rule = 'allow'` (üç tabloda)
- `module != '__protected__'` (matrix tablolarında)
- `scope_type` enum
- `template_key` system/custom kombinasyonu
- `user_scope_additions.applies_to_module NOT IN ('__global__','__protected__')`

DB-level enforcement migration script veya bulk SQL bile bypass edemez.

Registry validation wrapper: permission seed/migration/bulk import script'leri registry'den geçer. CI/lint check + runtime validation.

### 2.12.3 Startup/deploy scan

Uygulama startup veya deploy sırasında `permission_template_entries` ve `user_permissions` tabloları registry'ye göre full scan.

**Strict mode (default):** Invalid config bulunursa deployment fail.

**Recovery mode:** Sistem safe-mode (authorization read-only), Owner alarm.

**Invalid config örnekleri:**
- `module = 'fake_module'`, `action = 'view'` (unknown module — registry tarafından yakalanır)
- `module = '__global__'`, `action = 'unknown_capability'` (unknown action)
- `module = 'contracts'`, `action = 'view'`, `scope_type = 'global'` (CRUD'a global)
- `scope_rule = 'deny'` (zaten DB CHECK yakalar, defense-in-depth)
- `module = '__protected__'` (zaten DB CHECK yakalar)

---

## 2.13 Bu bölümün kararları

| ID | Karar |
|---|---|
| **B21** | Authorization order: action classification → self-matrix-edit check → owner_bypass_exempt → Owner bypass → matrix lookup → config validation → resolver scope check (read predicate VEYA create payload validation) → reason check → audit + ALLOW. Self-matrix-edit Owner bypass'tan ÖNCE. |
| **B22** | **Permission/action registry tek key formatı `(module, action)` tuple. Fallback yok.** Global capability ve field-level gate permission'lar `__global__` sentinel modül namespace'inde. Protected system operations `__protected__` sentinel namespace'inde. Unknown module veya unknown action her zaman ConfigError. Registry alanları: category, scope_mode, allowed_scope_types, owner_bypass_exempt, reason_required, default_template_keys, audit_worthy. |
| **B23** | `scope_mode` beş kategori: crud, global_capability, record_bound, field_level_gate, protected_system. `scope_type = 'global'` yalnızca global_capability ve field_level_gate'te. Registry her query'de validation. |
| **B24** | Protected system operations matrix dışı, kod-level invariant. Registry'de `__protected__` namespace. **Matrix tablolarında DB-level CHECK `module != '__protected__'`** — protected ops'un matrix'e sızması mutlak engellenir, migration bile bypass edemez. UI yeri: User Profile > Security > Owner Status. |
| **B25** | **Owner bypass scope'u: authorization katmanı bypass, business validation DEĞİL.** Same-org (B19), domain validation, required fields, FK integrity, finance invariants (A27), pricing snapshot (A14), state machine, business constraints Owner için de aktif. |
| **B26** | `owner_bypass_exempt` metadata flag matrix-stored permission'larda. Şimdilik tek aday: `approve_hard_delete`. |
| **B27** | `permission_templates`: system'de `template_key` NOT NULL + immutable (backend update reject); custom'da NULL zorunlu (CHECK constraint). |
| **B28** | Sistem template'ler (`is_system_template = true`) hard delete + deactivate yasak. Custom: deactivate + Bölüm 1 B5 hard delete. |
| **B29** | `permission_template_entries` actor field'ları taşımaz; değişiklikler template version bump + audit event payload üzerinden. |
| **B30** | `user_permissions` matrix granular. Template apply: (A) preserve exceptions default, (B) reset to template tehlikeli — diff preview + reason. |
| **B31** | `scope_rule = 'deny'` **üç tabloda DB-level CHECK ile yasak** (`permission_template_entries`, `user_permissions`, `user_scope_additions`): `CHECK (scope_rule = 'allow')`. Migration script veya bulk SQL bypass edemez. Phase 2'de DROP edilir, enforcement kod-level (registry üzerinden). |
| **B32** | **Hiçbir user kendi permission matrix'ini düzenleyemez, Owner dahil.** `actor.id = target.id` ise `user_permissions` DENY. Authorization order'da Owner bypass'tan ÖNCE. İstisnalar matrix dışı ayrı endpoint'ler: password, notification prefs, preferred_language, timezone, display_name, phone_e164+WhatsApp opt-in. Hierarchy self-promotion da yasak. |
| **B33** | Hierarchy enforcement atomic: self/descendant/cross-org/inactive yasak, Owner için `reports_to = NULL`. Owner reassignment istisnası (Bölüm 1 B6 cross-reference): `is_owner = true` user organizational debt bırakabilir, audit'lenir. |
| **B34** | Scope composition module-specific resolver pattern. Her modül **read resolver** (SQL predicate) + **create resolver** (payload validation) sağlar. |
| **B35** | **Contract resolver — Aşama 3 PREREQUISITE:** explicit ownership alanları (`sales_owner_user_id`, `account_owner_user_id`, `responsible_project_user_id`) tanımlanmadan implement edilmez. External sales_agent gerçek gediği (`sales_agent.user_id = NULL`). |
| **B36** | `office` scope + `office_id IS NULL` → `own` fallback. HQ user kazara kilitlenmez. |
| **B37** | `user_scope_additions.applies_to_action` NOT NULL DEFAULT `'view'`. Scope addition default sadece view'ı genişletir; update/delete/create/override için ayrı satır. Resolver `applies_to_action = current_action` filtresi. **Create resolver de aynı filtre: scope additions sadece `applies_to_action = 'create'` olanları create payload validation'a dahil eder; view/update addition'ları create yetkisi yaratmaz.** **DB-level CHECK** `applies_to_module NOT IN ('__global__', '__protected__')` — sentinel namespace'lerin scope addition'a sızması engellenir. |
| **B38** | Create action scope semantiği — payload validation: resolver payload'daki ownership alanlarını scope_type'a göre validate eder. Sızıntı koruması: sales rep `leads.create own` ile başka birinin adına kayıt yaratamaz. Module-specific create resolver Aşama 3'te. |
| **B39** | Scope **query layer** enforce, UI değil. Backend resolver helper kullanımı zorunlu. |
| **B40** | LIFFY matrix sync: **access narrowing → immediate** (force sync + version bump + LIFFY invalidation), **access expanding → polling kabul** (~15-30 dk + manuel force sync). Critical liste: deactivation/reactivation, permission revoke, is_owner revoke, sensitive permission revoke, reports_to/office_id değişikliği, scope addition revoke/expire, sales_agents.user_id link değişikliği. |
| **B41** | Risky permission default'ları `template_key` ile bağlı (2.6.6). Project Staff'a `convert_quote_to_contract` ve `override_stand_reservation` default verilmez. Sales Rep'e marketing default verilmez. `view_audit_log` owner only default. `view_own_audit_log` tüm template'lerde default. |
| **B42** | `view_sensitive_finance` **field-level gate**. `export_data` ve `send_marketing_campaign` **scope-aware capability — iki aşamalı authorization pattern**: Aşama 1 `__global__.action` capability check, Aşama 2 target_module view scope check. Hedef data seti her zaman target_module view scope predicate ile filtrelenir. Organization-wide için target_module'da `all` scope veya `is_owner`. |
| **B43** | Registry enforcement pipeline üç katmanlı: (1) **API/UI** registry validation, (2) **migration/seed/bulk import** schema CHECK + registry wrapper, (3) **startup/deploy scan** (strict mode fail veya recovery mode safe). Registry gerçek source of truth. Sentinel namespace (`__global__`, `__protected__`) ile tek format. |
| **B44** | UI sentinel gizleme: `module = '__global__'` permission'ları normal modül listesinde gösterilmez, ayrı "Capabilities" / "Global Permissions" bölümünde. `__protected__` zaten matrix'te yazılamaz, UI'da hiç görünmez (protected ops User Profile > Security > Owner Status'ta yönetilir). Sentinel kullanıcıya görünmez technical detail. |

---

## 2.14 Açık kalan noktalar (sonraki bölümlere)

**Bölüm 3 (Auth/JWT/Session):**
- Permission cache invalidation strategy (LEENA içi + LIFFY replica).
- `permission_version` / `scope_version` bump mekanizması.
- Self-edit izin verilen field'lar implementation detayı (password, notification prefs, phone+WhatsApp opt-in flow).

**Bölüm 4 (Reference data sync):**
- **Scope cache expiry disiplini:** Cache TTL aktif `user_scope_additions.expires_at`'ı aşamaz. Tercih edilen: expired addition'lar her query'de application layer'da `WHERE expires_at IS NULL OR expires_at > now()` ile filtrelenir, cache'e güvenilmez.
- Force sync UI ve trigger.
- LIFFY-side resolver'ların LIFFY local schema'sıyla çalışma detayı.

**Bölüm 5 (Audit log):**
- **`view_audit_log` delegation redaction:** Owner dışında delegate edilen user için audit log UI filtreli/redacted olabilir — örn. is_owner flag değişiklikleri, view_sensitive_finance değişiklikleri delegate'e görünmez veya redacted.
- **Audit-worthy actions sınıflandırması:** "Her aksiyon audit'lenir" yerine kategorize edilmiş sınıflandırma. Kesin audit gerektirenler: permission changes, override actions, delete (deactivate + hard delete), export, status changes, sensitive access, is_owner grant/revoke, hard delete second approval. Audit gerekmeyenler: routine list/view queries. Permission registry'de `audit_worthy` flag ile bağlanır.

**Bölüm 6 (Notifications):**
- Notification preferences modeli (mandatory vs default-on vs mute).

**Bölüm 8 (WhatsApp bot):**
- Channel restriction layer (WhatsApp'tan hassas field dönmez).

**Aşama 3:**
- Permission registry implementation (kod-level constant + tüm `(module, action)` ve sentinel key'leri için metadata).
- Permission matrix UI mockup (sentinel gizleme + Capabilities bölümü ayrı).
- Sistem default 10 template'inin CRUD permission içeriği.
- **Module read resolver implementation** her modül için (özellikle contract resolver — B35 prerequisite).
- **Module create resolver implementation** her modül için (B38 pattern).
- `target_entity_type + applies_to_module + applies_to_action` compatibility matrix.
- `record_bound` scope semantiği detayı (resolver entegrasyonu).
- Scope-aware capability endpoint'lerinin (export_data, send_marketing_campaign) iki aşamalı authorization implementation.
- Migration framework için registry validation CI/lint hook.
- Startup scan implementation (strict vs recovery mode).

---

## 2.15 Bölüm özeti

Authorization order: action classification (registry tek format lookup) → self-matrix-edit (Owner dahil) → owner_bypass_exempt → Owner bypass → matrix → config validation → resolver scope (read predicate veya create payload validation) → reason → audit + ALLOW. **Permission registry tek key formatı `(module, action)` tuple, fallback yok**: global capability ve field-level gate permission'lar `__global__` sentinel namespace'inde, protected system ops `__protected__` sentinel namespace'inde. Sentinel sayesinde schema NOT NULL karşılanır, unknown module/action her zaman ConfigError. **Protected ops matrix'e sızamaz** — DB-level CHECK (`module != '__protected__'`) migration bile bypass edemez. **Owner bypass authorization layer'a özgü; business validation Owner için de aktif** (same-org, domain, required fields, FK, finance invariants, pricing snapshot, state machine). `approve_hard_delete` matrix'te ama `owner_bypass_exempt = true`. Sistem template'ler hard delete + deactivate yasak; `template_key` system'de NOT NULL + immutable, custom'da NULL zorunlu. `scope_rule = 'deny'` üç tabloda DB-level CHECK ile yasak (MVP). Hiçbir user kendi matrix'ini düzenleyemez (Owner dahil). Module-specific resolver pattern + action-level scope additions + create payload validation: `applies_to_action` NOT NULL DEFAULT `'view'`, view addition update/create yetkisi yaratmaz, create resolver `applies_to_action = 'create'` filtreli scope additions ile çalışır. `user_scope_additions.applies_to_module` sentinel yasağı (`__global__`/`__protected__` reddedilir). Contract resolver Aşama 3 prerequisite (explicit ownership alanları). **Scope-aware capability iki aşamalı authorization**: Aşama 1 `__global__.action` capability check, Aşama 2 target_module view scope predicate ile filter. LIFFY sync: narrow → immediate, expand → polling. Registry enforcement üç katmanlı: API/UI + migration schema CHECK + startup scan. **UI sentinel gizleme**: `__global__` ayrı "Capabilities" bölümünde, `__protected__` hiç görünmez (Security panel'de). Risky permission default'ları `template_key` ile bağlı; Sales Rep marketing'ten, Project Staff convert/override'dan çıkarıldı. `view_sensitive_finance` field-level gate, `view_audit_log` Owner only (delegation redaction Bölüm 5'e), `view_own_audit_log` tüm template'lerde. Audit-worthy actions sınıflandırması Bölüm 5'te (registry `audit_worthy` flag ile bağlanır).

---

*Bu doküman Aşama 2 Bölüm 2 olarak finalize edilmiştir. Aşama 2 sonraki bölümleri ve Aşama 3 bu dokümanı kanonik referans olarak kullanır. Bölüm 2'ye dönüş ancak resmi bir amendment (v1.1) ile mümkündür.*
