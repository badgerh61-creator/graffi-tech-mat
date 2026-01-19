# Phase O.3 — Automated Distribution Jobs

## Purpose
Execute authorized automation policies reliably and safely.

---

## Job Types (Initial)

- AUTO_EXPIRE_LINKS
- AUTO_REVOKE_ON_PROJECT_ARCHIVE
- WEBHOOK_DELIVERY

---

## Job Record Schema

```json
{
  "id": "uuid",
  "job_type": "string",
  "policy": "string",
  "project_id": "uuid",
  "payload": {},
  "status": "pending | running | succeeded | failed",
  "attempt": 1,
  "max_attempts": 3,
  "last_error": "string | null",
  "created_at": "iso-8601",
  "updated_at": "iso-8601"
}
```

---

## Execution Rules (LOCKED)

- Jobs are idempotent
- Jobs must respect Phase N invariants
- Retries are bounded and exponential
- Failures are recorded, not hidden
- Jobs never mutate exports
- Jobs never bypass audit

---

## Retry Policy (Canonical)

- Max attempts: 3
- Backoff: exponential (2ⁿ minutes)
- Permanent failure after exhaustion

---

## Forbidden

- Infinite retries
- Silent failures
- Job types outside allowlist
- Runtime policy changes

