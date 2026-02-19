# Phase H.4 — HTTP Security Hardening (Ops-Grade)

## Purpose (LOCKED)
Harden the HTTP surface for deployment without changing business behavior.

## Scope (Additive Only)
- Security headers on all responses
- Optional strict CORS allowlist (env-driven)
- Optional rate limiting for /login only (env-driven)

## Invariants
- No endpoint names change
- No authentication logic changes
- No database schema changes
- Must not break existing tests: hardening is disabled by default

## Security Headers (Required)
Middleware MUST add these headers:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- Referrer-Policy: no-referrer
- Permissions-Policy: camera=(), microphone=(), geolocation=()
- Cache-Control: no-store  (for auth responses; optional global)

## CORS Allowlist (Optional)
When enabled, only configured origins are allowed.
When disabled, existing CORS behavior remains.

## Rate Limit (Optional)
When enabled:
- Applies ONLY to POST /login
- Returns 429 if exceeded
- Must be disable-able via env (default OFF)

## Exit Criteria
- Headers present in responses
- Rate limit works when enabled
- Existing suite passes when hardening disabled (default)

