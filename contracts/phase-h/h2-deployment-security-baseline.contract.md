# Phase H.2 — Deployment & Security Baseline (Ops-Grade)

## Purpose (LOCKED)
Make the system runnable as real deployment units with minimum security posture.

No product features.
No kernel behavior changes.
Only operational and security baseline.

---

## Deliverables

### 1) Process Topology (runnable units)
Define and run:
- API server (uvicorn)
- Worker (jobs)
- Scheduler (O.4)
- DB (postgres)
Deliver:
- docker-compose.yml (dev topology acceptable)
- each unit has health behavior

### 2) HTTP Security Baseline
- Secure headers middleware enabled:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Referrer-Policy: no-referrer
  - Permissions-Policy: minimal (deny by default)
- CORS allowlist is env-driven (no "*")

### 3) Auth Endpoint Rate Limiting (minimum viable)
- Rate limit applied to POST /login
- Default: 10 requests / minute / IP (configurable by env)
- Returns 429 when exceeded

### 4) Migration / Bootstrap Commands
Provide command entrypoints:
- make migrate  (create revision)
- make upgrade  (apply migrations)
- make seed     (optional; creates dev users)

### 5) Configuration Hardening
- ENV must be one of: development|staging|production
- production requires:
  - strict CORS allowlist
  - secrets length checks (basic)

---

## Invariants
1. No changes to snapshot immutability rules
2. No hidden mutation through ops endpoints
3. Security middleware must not break API semantics

---

## Exit Criteria (Freeze)
- docker compose boots API + worker + scheduler + DB
- /health ok, /ready ok in composed environment
- /login is rate limited
- secure headers present on responses
- ENV validation enforced

