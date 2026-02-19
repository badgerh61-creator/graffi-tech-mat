# Phase H.3 — Job Reliability & Recovery (Ops-Grade)

## Purpose (LOCKED)
Make async jobs survivable under crashes, restarts, duplicate deliveries, and partial failures.

No product features.
No kernel behavior changes.

---

## Definitions
- "Job": async background task persisted in DB.
- "Idempotent": running the same job multiple times yields the same final outcome.
- "Stuck job": job left in "running" past a timeout threshold.

---

## Required Behavior

### 1) Bounded retries
- Every job has:
  - attempts (int)
  - max_attempts (int)
  - next_run_at (datetime nullable)
- Failures:
  - increment attempts
  - if attempts < max_attempts: schedule retry with backoff
  - if attempts >= max_attempts: mark job failed

### 2) Idempotency key
- Every job has idempotency_key (string, unique)
- Creating a job with an existing idempotency_key must return the existing job (no duplicates)

### 3) Stuck job recovery
- On scheduler tick, any job:
  - status == "running"
  - started_at older than STUCK_JOB_SECONDS
  becomes "queued" again OR "failed" depending on attempts remaining
- Recovery emits an audit event

### 4) Safe restart semantics
- Worker crash must not corrupt job state.
- A recovered job must not re-apply side effects beyond idempotency guarantees.

---

## API (internal/service-level)
- enqueue_job(name, payload, idempotency_key, max_attempts) -> Job
- run_job_once(job_id) -> Job
- recover_stuck_jobs(now) -> int recovered_count

---

## Observability
- Emit metrics:
  - job.retry_scheduled
  - job.failed_final
  - job.recovered_stuck

---

## Exit Criteria (Freeze)
✅ Duplicate enqueue returns same job
✅ Retries backoff and cap enforced
✅ Stuck jobs recovered deterministically
✅ Recovery is audited + emits metric
✅ Tests are deterministic (no sleep)

