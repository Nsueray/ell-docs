# ADR-020: Shared Frontend Component Pattern

> ℹ️ **CONTEXT NOTE — 2026-05-11**
>
> Bu ADR Aşama 1 mimarisi yazılmadan önce karara bağlandı,
> ama içeriği LEENA implementasyonuna özgü ve yeni mimariyle
> uyumlu. Geçerlidir.
>
> **Master karar referansı:**
> [/architecture/ELL_ARCHITECTURE_STAGE_1_TOPOLOGY_v1.1.md]
>
> ---

## Status
DECIDED (7 May 2026)

## Context
Leena EMS admin panel consists of 21+ separate HTML pages, each with inline CSS and JavaScript. This architecture led to systematic duplication problems:

1. **Toast notifications:** Each page defined its own `.toast` or `.app-toast` CSS and `showToast()` function. When Bootstrap 5 was loaded (for icons), its `.toast` class silently overrode the custom toast — causing 0×0 invisible toasts on pages like email-campaigns.html (discovered in Sprint B).

2. **Authentication headers:** Every `fetch()` call manually constructed `{ headers: { 'Authorization': 'Bearer ' + token } }`. When JWT expired (30-day lifetime), most pages showed generic errors instead of redirecting to login. Only 3 of 21 pages had explicit 401 handling.

3. **Error patterns:** 73 `alert()` calls across 19 pages blocked the UI with native browser dialogs instead of non-blocking toasts.

4. **Bug propagation:** Fixing a pattern in one page (e.g., Bootstrap toast conflict) required touching all 21 pages individually. Sprint B's fix only covered 2 pages, leaving the rest vulnerable.

The root cause: no mechanism for sharing frontend code across pages in a vanilla JS + static HTML architecture (no bundler, no framework, no build step).

## Decision
Introduce shared components as self-contained JavaScript files in `public/leena-*.js`, following IIFE (Immediately Invoked Function Expression) pattern.

### Component 1: `leena-toast.js`
- **API:** `window.showToast(message, type, duration)`
- **Types:** success (default), error, warning, info
- **Self-contained:** Auto-injects CSS via `<style>` tag (idempotent — checks for existing element by ID)
- **Auto-creates** toast container DOM element if missing
- **Bootstrap-safe:** Uses `.app-toast` prefix to avoid class name conflicts
- **Include:** `<script src="/leena-toast.js"></script>`

### Component 2: `leena-fetch.js`
- **API:** `window.leenaFetch(url, options)` — returns `Promise<Response>`
- **Auto-auth:** Reads token from localStorage, attaches Authorization header
- **401/403 handling:** Shows "Session expired" toast, schedules logout after 1500ms
- **Concurrent protection:** `_loggingOut` flag prevents 5x toast on parallel requests
- **15s timeout:** AbortController-based, caller handles error toast
- **Login loop protection:** Skips redirect if already on login page
- **Include:** `<script src="/leena-fetch.js"></script>` (after leena-toast.js)

### Component Principles
1. IIFE wrapper — no global pollution beyond explicit API (`window.showToast`, `window.leenaFetch`)
2. CSS auto-injection — idempotent via element ID check
3. Auto-create DOM elements if missing (defensive)
4. Defensive cross-component references (`typeof showToast === 'function'`)
5. Single `<script src>` include per page — no build step needed

### Caller Responsibility Pattern
- **401/403:** Component handles (toast + redirect). Caller skips contextual error:
  ```
  catch (err) {
    if (err.status === 401 || err.status === 403) return;
    showToast('Failed to load X', 'error');
  }
  ```
- **Timeout/network errors:** Component throws silently. Caller shows contextual message.
- **Success:** Caller handles entirely.

## Consequences
- Positive: Toast Bootstrap conflict fixed in ONE place, applies to all 21 pages immediately.
- Positive: Auth handling (401/403 → logout) consistent across all migrated pages without per-page code.
- Positive: New pages get correct behavior with 2 script tags — no boilerplate.
- Positive: 73 alert() calls eliminated, replaced with non-blocking toasts.
- Trade-off: Migration is incremental. leena-fetch.js migrated in 3 pages (visitorlog, email-campaigns, dashboard_new); 16+ remaining pages deferred to post-fair backlog.
- Risk: Component bugs affect all consuming pages. Mitigated via diff review process (Suer approves every change before push).
- Operational: No build step added — components are raw JS files served statically. This matches existing architecture and avoids bundler complexity.

## Alternatives Considered
1. **Per-page implementations (status quo):** Rejected — caused Sprint A/B bugs, 73 alert() instances, inconsistent 401 handling.
2. **Full SPA refactor (Vue/React):** Rejected — scope too large for 11-days-to-fair stability requirement. Would require build tooling, routing, state management.
3. **Bundler-based imports (webpack/vite):** Rejected — vanilla JS sufficient at current scale (21 pages). Bundler adds deployment complexity on Render.
4. **CSS-only shared file (leena.css):** Partially exists but inconsistently used. Toast/fetch components need JS, not just CSS.

## Related
- ADR-017: Email queue logging — Bootstrap toast conflict was a symptom of duplicated toast CSS
- ADR-019: Bulk email send — leenaFetch used in bulk-email modal
- `public/leena-toast.js` — commit a5bf93c
- `public/leena-fetch.js` — commit 2e233f0
- Post-fair backlog: remaining 16+ page migrations, refresh token mechanism
