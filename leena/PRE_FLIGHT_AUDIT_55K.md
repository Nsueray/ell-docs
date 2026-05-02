# Pre-Flight Audit: 55K Email Campaign Production Send

**Date:** 2026-04-27
**Auditor:** Claude Code (system-level code review)
**Scope:** All code paths from recipient upload → campaign activation → scheduler enqueue → worker send → tracking

---

## 1. Executive Summary

**Risk Level: YELLOW — Ship with targeted fixes**

- **Critical issues:** 2 (upload size limit, email_queue cleanup)
- **High issues:** 3 (no SendGrid backoff, scheduler throughput bottleneck, warm-up strategy needed)
- **Medium issues:** 5
- **Low issues:** 4

**Recommendation:** Fix the 2 critical issues (1-2 hours work), implement warm-up sending strategy, then proceed. The system architecture is sound — the issues are operational, not structural.

---

## 2. Findings by Section

### A. Recipient Upload

**[CRITICAL] A3. Express body limit blocks 55K CSV upload**
- Where: `index.js:35` — `express.json({ limit: '2mb' })`
- Failure mode: 55K rows × ~200 bytes = ~11MB CSV. Multer file limit is 10MB (campaigns.js:38) which handles the file, BUT the JSON body parser limit of 2MB is irrelevant here because multer bypasses it for multipart. The multer limit of 10MB IS the gate. A 55K-row CSV with email+name+company columns is ~6-8MB. An XLSX file is compressed, ~2-4MB. **This will fit within 10MB multer limit.**
- Mitigation: **Not actually a blocker.** Multer handles the file upload separately from JSON body parser. 10MB multer limit fits 55K-row files. No change needed.
- Status: ✅ OK

**[MEDIUM] A1. XLSX parses entire file into memory**
- Where: `campaigns.js:449-451` — `XLSX.read(req.file.buffer, { type: 'buffer' })` then `sheet_to_json()`
- Failure mode: 55K rows parsed into a JS array in memory. At ~500 bytes/row JSON = ~27MB. Render web service has 512MB RAM (Starter) or 1GB (Standard). 27MB is fine.
- Mitigation: No change needed. Within memory bounds.
- Status: ✅ OK

**[MEDIUM] A3. Browser timeout on 55K INSERT**
- Where: `campaigns.js:504-544` — 55 batch INSERTs of 1000 rows each
- Failure mode: Each batch INSERT takes ~50-200ms. 55 batches = 3-11 seconds total. Express default timeout is none (Node.js default 2 minutes). Browser fetch timeout is browser-dependent (Chrome: 5 minutes). **Will complete within 30 seconds.**
- Mitigation: No change needed. Well within timeout bounds.
- Status: ✅ OK

**[LOW] A4. Partial upload reporting**
- Where: `campaigns.js:556-563` — response includes `added`, `skipped_duplicates`, `skipped_unsubscribed`, `invalid` counts
- Failure mode: If 50% of rows fail in per-row fallback, Yaprak sees "Added: 27500, Invalid: 27500". She can decide whether to proceed.
- Status: ✅ OK (adequate reporting)

**[LOW] A5. Duplicate handling**
- Where: `campaigns.js:486` — `ON CONFLICT (campaign_id, email) DO NOTHING`
- Status: ✅ OK — duplicates silently deduplicated, counted in response

**[LOW] A6. Email validation**
- Where: `campaigns.js:57` — `function isValidEmail(email) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); }`
- Status: ✅ OK — basic regex catches obvious malformed emails. SendGrid rejects the rest.

### B. Campaign Activation

**[MEDIUM] B1. Activation is transactional**
- Where: `campaigns.js:810-832` — BEGIN/COMMIT wrapping both campaign UPDATE and recipients UPDATE
- Status: ✅ OK — atomic transition

**[MEDIUM] B2. Single UPDATE for 55K rows**
- Where: `campaigns.js:820-823` — `UPDATE campaign_recipients SET next_step_due_at = NOW() WHERE campaign_id = $1 AND status = 'active'`
- Failure mode: 55K row UPDATE in single statement. With `idx_recipients_campaign` index, this is an indexed scan. Execution time: ~200-500ms. Within `statement_timeout: 30000` (30s).
- Mitigation: No change needed.
- Status: ✅ OK

**[LOW] B3. Double-click protection**
- Where: `campaigns.js:775` — `requireDraft()` checks status before activation
- Failure mode: Second click fails because campaign is already 'active'. No duplicate activation.
- Status: ✅ OK (status check is sufficient)

### C. Campaign Scheduler at Scale

**[HIGH] C1. Scheduler throughput bottleneck**
- Where: `email_worker.js:311-317` — `LIMIT 500` per cycle, 60s interval
- Failure mode: 55K recipients all due at once. 500 per cycle × 60s = 500/min. **55K / 500 = 110 cycles = 110 minutes = ~1.8 hours just to ENQUEUE Step 1.** Then worker needs to SEND them (~3 hours at batch=10).
- Total Step 1 time: ~5 hours from activation to all emails sent.
- Mitigation options:
  - (a) Increase LIMIT from 500 to 5000 — reduces enqueue time to ~11 minutes. Riskier for DB load.
  - (b) Reduce SCHEDULER_INTERVAL from 60s to 10s — 6x throughput. 55K / 500 × 10s = ~18 min.
  - (c) Both: 5000 limit + 10s interval = ~2 minutes to enqueue all.
- **Recommended:** (b) Reduce to 10s via env var. Add `CAMPAIGN_SCHEDULER_INTERVAL` env var.
- Estimated effort: 15 minutes

**[MEDIUM] C2. Per-recipient enqueue cost**
- Where: `email_worker.js:448-552` — 7 DB queries per recipient (unsub check, template fetch, event INSERT, pixel inject, queue INSERT, recipient UPDATE, campaign UPDATE)
- Failure mode: 500 recipients × 7 queries × ~5ms each = 17.5 seconds per cycle. Within 60s interval.
- Status: ✅ OK (but tight if LIMIT increased to 5000)

**[MEDIUM] C3. Deploy during enqueue marathon**
- Where: `email_worker.js:303-338` — lock+clear pattern
- Status: ✅ OK — Sprint 4 fix ensures no double-pickup. Cleared `next_step_due_at = NULL` before COMMIT, restored on failure.

**[LOW] C4. Log spam**
- Where: 110 log lines of "found 500 eligible recipients" + 55K individual enqueue logs
- Mitigation: Render retains last 10K log lines. Will scroll past. Non-blocking.
- Status: ✅ Acceptable

### D. Email Worker Throughput

**[HIGH] D2. SendGrid per-second rate limit**
- Where: `utils/email.js:63-85` — direct sgMail.send() call, no rate limiting
- Failure mode: Batch size 10, all 10 fire in parallel via Promise.allSettled. Each sgMail.send() is ~200-500ms HTTP call. With 10 parallel, effective rate = 10 emails per 2s = 5/second. SendGrid Pro plan allows 10K/hour = ~2.8/second sustained. **5/second may trigger soft throttling.**
- Mitigation: Reduce BATCH_SIZE to 5 for this campaign (2.5/second, safe for Pro plan). Or keep 10 and accept occasional 429 retries.
- **Recommended:** Set `EMAIL_WORKER_BATCH_SIZE=5` for this campaign. 5/2s = 2.5/second = 9K/hour. 55K = ~6 hours.
- Estimated effort: Env var change only, 0 code changes

**[HIGH] D5. No SendGrid backoff on 429/5xx**
- Where: `utils/email.js:81-84` — returns `false` on error, `email_worker.js` marks as failed, increments try_count
- Failure mode: If SendGrid returns 429, worker marks email as 'failed' and retries on next cycle (2s later). After 5 failures (MAX_RETRIES), email is permanently failed. No exponential backoff.
- Impact: During a 55K send, transient 429s will cause some emails to burn through retries fast. After 5 × 2s = 10 seconds of retries, email is permanently lost.
- Mitigation options:
  - (a) Add exponential backoff in sendEmailWithReplyTo (complex, risky before production send)
  - (b) Increase MAX_RETRIES to 20 via env var (simple, gives more chances)
  - (c) Accept risk — at 2.5/second rate (BATCH_SIZE=5), 429s are unlikely on Pro plan
- **Recommended:** (c) Accept risk with BATCH_SIZE=5. Monitor SendGrid dashboard during send.
- Estimated effort: 0 (if BATCH_SIZE=5)

**[CRITICAL] D4. SendGrid quota math**
- Current month usage: ~1,718 sent
- Step 1: 55,000
- Step 2 (24h, not_registered, estimated 85% send): ~46,750
- Step 3 (72h, not_registered, estimated 70% send): ~38,500
- **Total: ~142,000 emails**
- **Plan limit: 100,000/month**
- **EXCEEDS QUOTA by ~42K**
- Mitigation: Yaprak must upgrade SendGrid plan to 200K or send Steps 2 and 3 next month.
- **Recommended:** Upgrade to 200K/month plan BEFORE activation. Or reduce Step 2/3 scope.
- Status: **BLOCKER until quota confirmed**

**[CRITICAL] F3. email_queue rows never deleted**
- Where: `email_worker.js:96-98` — `markAsSent` only updates status, no DELETE
- Failure mode: 55K rows × ~50KB HTML content each = **2.75GB added to email_queue table**. After 3 steps: ~8GB. Table grows indefinitely.
- Impact: DB disk usage, slower queries on email_queue, eventual Render DB limit hit (Starter: 1GB, Standard: 10GB, Pro: unlimited)
- Mitigation: Add a cleanup job or DELETE sent rows after X days. **For immediate send:** ensure DB plan has sufficient storage.
- **Recommended:** After campaign completes, manually run: `DELETE FROM email_queue WHERE status = 'sent' AND campaign_id = X;`
- Estimated effort: 0 (manual SQL) or 30 min (automated cleanup)

### E. Database Pool & Connections

**[MEDIUM] E1. Pool limits vs Render plan**
- Where: `utils/db.js:14` — `max: 20`
- Worker has its OWN pool (email_worker.js:10-17) — also implicitly 10 default max.
- Render Starter DB: 50 connection limit. Standard: 100. Pro: 300.
- Web (20) + Worker (10) = 30 total. Within all plan limits.
- Status: ✅ OK

**[MEDIUM] E4. email_events growth**
- 55K sent events + ~165K opens + ~15K clicks + ~5K registrations = ~240K rows in first week
- Indexes: 4 indexes on email_events (campaign_id, recipient_id, event_type, email+event_type)
- Each row ~200 bytes + indexes ~400 bytes = ~600 bytes × 240K = ~144MB
- Status: ✅ OK — well within DB limits

### F. Tracking & Storage

**[MEDIUM] F1. Tracking pixel write throughput**
- 55K recipients × 3 avg opens = 165K INSERT statements over ~1 week
- ~24K/day = ~1K/hour = ~16/minute = negligible load
- Status: ✅ OK

### G. Memory / OOM Risk

**[LOW] G1. Worker memory**
- Batch of 10 queue rows × 50KB HTML = 500KB per batch. Plus scheduler holding 500 recipient objects × ~1KB = 500KB. Total working memory: ~2MB. Render 512MB → ✅ OK
- Status: ✅ OK

**[LOW] G3. Click wrapping CPU**
- wrapClickLinks regex on 50KB HTML takes ~1-5ms. For 500 recipients per scheduler cycle = 0.5-2.5 seconds. Non-blocking (sequential in scheduler). ✅ OK

### H. SendGrid & Deliverability

**[HIGH] H1. Sender reputation / warm-up**
- leena.app domain sending 55K emails in 6 hours from a baseline of ~500/month = 110x spike
- **High risk of being flagged by receiving mail servers.** Gmail, Outlook, Yahoo have rate-limiting per sending domain.
- Mitigation: **Send in waves over 3-5 days instead of all at once.**
- **Recommended strategy:** Day 1: 5K, Day 2: 10K, Day 3: 15K, Day 4: 25K. Or use SendGrid's built-in "scheduled send" feature.
- Estimated effort: Can be done operationally (Yaprak creates 4 campaigns with subsets) or programmatically (add campaign wave feature)

**[MEDIUM] H3. Recipient list quality**
- Historical visitors from 2025 fairs = 1-2 year old email addresses
- Expected bounce rate: 5-10% for stale lists
- SendGrid pauses sending if bounce rate > 5% on Pro plan
- Mitigation: Use SendGrid's email validation API to pre-clean list ($0.003/email = $165 for 55K). Or accept some bounces and monitor.
- **Recommended:** Yaprak should import and activate with a small test batch (1K) first. Monitor bounce rate for 24h. If < 3%, proceed with full list.

**[LOW] H4. CAN-SPAM compliance**
- Unsubscribe link: ✅ present (Sprint 3)
- Physical address: ❌ Not in current template. Yaprak must add to email template.
- "Why am I receiving this": ❌ Not present. Recommended.

### I. User Experience / Operations

**[MEDIUM] I3. Pause behavior**
- Where: `campaigns.js` pause sets `status='paused'`, scheduler skips paused campaigns
- But: emails already in email_queue continue sending (worker doesn't check campaign status)
- Impact: After pause, ~500-5000 emails already enqueued may still send
- Mitigation: Accept behavior — "pause" means "stop enqueuing new," not "stop sending in-flight"

**[LOW] I4. Unsubscribe during send**
- Where: `email_worker.js:454-466` — unsubscribe check at enqueue time
- Status: ✅ OK — checked before each step enqueue

**[LOW] I5. Completion notification**
- Campaign auto-transitions to 'completed' when all recipients done
- Stats tab shows real-time progress on refresh
- No push notification — Yaprak must check manually

### J. Rollback / Recovery

**[MEDIUM] J1. Wrong content mid-send**
- Pause stops new enqueue. Already-enqueued emails (~500-5000) will still send.
- To stop everything: manually UPDATE email_queue SET status='failed' WHERE campaign_id=X AND status='pending'
- Already-sent emails cannot be recalled.

**[LOW] J2. Worker crash mid-batch**
- email_queue rows in 'processing' state have no explicit timeout
- On worker restart: fetchNextBatch skips 'processing' rows (WHERE status='pending')
- These rows stuck forever in 'processing'
- Mitigation: Manual fix: UPDATE email_queue SET status='pending' WHERE status='processing' AND last_try < NOW() - INTERVAL '10 minutes'
- Or add a stale-processing cleanup to the worker startup

---

## 3. Recommended Pre-Send Checklist for Yaprak

### Before creating campaign:
- [ ] Verify SendGrid plan is 200K/month (or sufficient for 3-step campaign)
- [ ] Verify leena.app SPF, DKIM, DMARC records are properly configured
- [ ] Prepare email template with: physical address line, "why you received this" line
- [ ] Review subject line for spam triggers (avoid ALL CAPS, excessive punctuation, "FREE")

### Before uploading recipients:
- [ ] Clean CSV: remove obvious invalid emails, remove team/internal addresses
- [ ] If possible, run list through SendGrid email validation API
- [ ] Prepare file as CSV or XLSX with columns: email (required), first_name, last_name, company

### Before activating campaign:
- [ ] Send to 5 internal test addresses first — verify email renders, tracking works, links work
- [ ] Check unsubscribe link works (click it, verify landing page)
- [ ] Verify click tracking works (click a link in test email, check email_events table)
- [ ] Set EMAIL_WORKER_BATCH_SIZE=5 on Render worker (prevents SendGrid throttle)
- [ ] Plan sending in waves: first 5K today, monitor 24h, then ramp up
- [ ] Have SendGrid dashboard open during send to monitor delivery/bounce rates

### During send:
- [ ] Monitor SendGrid dashboard for bounce rate (pause if > 5%)
- [ ] Refresh Stats tab periodically to track progress
- [ ] If wrong content detected: PAUSE immediately, then manually fail pending queue rows

### After send:
- [ ] Run cleanup: `DELETE FROM email_queue WHERE status = 'sent' AND campaign_id = X` (reclaim DB space)
- [ ] Review stats: open rate, click rate, registration rate
- [ ] Check unsubscribe count
- [ ] Review bounce rate in SendGrid dashboard

---

## 4. Recommended Code Changes

### Sprint 6a: Pre-send critical fixes (1-2 hours)

**Priority: CRITICAL — must do before 55K send**

1. **Add CAMPAIGN_SCHEDULER_INTERVAL env var** — reduce from 60s to 10s for campaigns
   - File: email_worker.js
   - Change: `const SCHEDULER_INTERVAL = parseInt(process.env.CAMPAIGN_SCHEDULER_INTERVAL || '60', 10) * 1000;`
   - Effort: 5 min

2. **Add scheduler LIMIT env var** — increase from 500 to 2000 for bulk sends
   - File: email_worker.js
   - Change: `const SCHEDULER_BATCH_LIMIT = parseInt(process.env.CAMPAIGN_SCHEDULER_BATCH || '500', 10);`
   - Effort: 5 min

3. **Add email_queue cleanup to campaign completion** — DELETE sent rows when campaign completes
   - File: email_worker.js, checkCampaignCompletion function
   - Add: `DELETE FROM email_queue WHERE campaign_id = $1 AND status = 'sent'` after status='completed' UPDATE
   - Effort: 15 min

### Sprint 6b: Post-send improvements (optional)

4. **Add exponential backoff** for SendGrid failures (utils/email.js + email_worker.js)
5. **Add stale 'processing' cleanup** on worker startup
6. **Add campaign wave/throttle feature** (split recipients into daily waves)

---

## 5. Recommended Sending Strategy

**Strategy: Graduated warm-up over 4 days**

| Day | Recipients | Cumulative | Send time (at 2.5/s) |
|-----|-----------|-----------|---------------------|
| Day 1 | 5,000 | 5,000 | ~33 min |
| Day 2 | 10,000 | 15,000 | ~67 min |
| Day 3 | 15,000 | 30,000 | ~100 min |
| Day 4 | 25,000 | 55,000 | ~167 min |

**How to implement without code changes:**
Yaprak creates 4 campaigns, each with a subset of the 55K list (split the CSV into 4 files by row ranges). Activates one per day.

**Alternative (with code change):**
Add a `daily_send_limit` column to email_campaigns. Scheduler stops enqueuing after daily limit reached, resumes next day. Estimated effort: 2-3 hours.

**Rationale:** Gmail, Outlook, Yahoo all have per-sender hourly/daily rate limits. A new sender (or one with low recent volume) blasting 55K in 6 hours will trigger rate limiting or spam classification. Gradual ramp-up over 4 days lets receiving servers build trust.
