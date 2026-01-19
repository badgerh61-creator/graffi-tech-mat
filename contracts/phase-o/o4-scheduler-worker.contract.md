# Phase O.4 — Scheduler & Worker Execution

## Purpose
Execute authorized automation jobs safely and deterministically.

---

## Worker Responsibilities

- Fetch pending automation jobs
- Execute jobs using O.3 executor
- Enforce retry and backoff
- Record execution outcome
- Never bypass Phase N or audit

---

## Scheduler Responsibilities

- Trigger job execution at defined intervals
- Never execute jobs directly
- Never create jobs implicitly

---

## Execution Guarantees

- Jobs are executed at-least-once
- Idempotency guarantees correctness
- Failed jobs do not block others
- Worker crashes do not corrupt state

---

## Forbidden

- Inline execution in API handlers
- Infinite retry loops
- Dynamic job creation
- Silent job failure

