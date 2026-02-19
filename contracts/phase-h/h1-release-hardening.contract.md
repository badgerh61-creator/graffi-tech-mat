# Phase H.1 — Release Hardening & Deployment Topology (Ops-Grade)

## Purpose (LOCKED)
Make the platform deployable, observable, and recoverable without changing product behavior.

No feature work.
No kernel changes.
Only operational correctness.

---

## Deliverables

### 1) Environment Separation (fail-fast)
- REQUIRED env vars validated at startup
- Missing required vars must prevent app boot
- Provide `.env.example` with all required vars documented

### 2) Health & Readiness
- GET /health returns 200 always if process is alive
- GET /ready returns 200 only if DB connectivity is OK
- Readiness must not mutate DB

### 3) Structured Logging
- Logs emitted in structured JSON format
- Must include: level, message, logger name
- Request trace id propagation stays compatible with Phase P

### 4) Deployment Topology Definition
- Define runnable units:
  - API server
  - Worker (jobs)
  - Scheduler (cron/loop)
  - DB
- Provide `docker-compose.yml` or equivalent dev topology

### 5) Backup & Restore (documented + testable)
- Document: DB backup + restore commands
- Restore must preserve:
  - immutable snapshots
  - audit integrity

---

## Invariants (NON-NEGOTIABLE)
1. No changes to snapshot authority rules
2. No new mutation pathways
3. Hardening must not require UI changes
4. Readiness checks are safe and fast

---

## Exit Criteria (Freeze Conditions)
- App fails fast on missing required env vars
- /health works
- /ready detects DB down (fails) and DB up (passes)
- JSON logging enabled
- Docs + topology present in repo

