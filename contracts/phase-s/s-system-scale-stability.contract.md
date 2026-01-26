# Phase S — System Scale & Stability

## Purpose
Guarantee correctness, recoverability, and audit integrity under scale and failure.

---

## Scope

Phase S governs:
- Snapshot lifecycle safety
- Job queue backpressure
- Retry ceilings
- Long-running drafts
- Startup & recovery behavior
- Corruption detection

---

## Snapshot Stability Rules

- Draft snapshots may expire (TTL)
- Expired drafts become "abandoned"
- Completed snapshots never expire
- Abandoned drafts cannot be finalized
- Draft expiration MUST NOT delete data

---

## Job System Rules

- All jobs declare max_retries
- Exceeding retries marks job as failed
- Failed jobs emit audit + metric
- No infinite retries allowed

---

## Backpressure Rules

- Queue depth thresholds enforced
- New jobs rejected when saturated
- Rejection emits audit + metric

---

## Startup & Recovery

On startup, system MUST:
- Detect incomplete jobs
- Mark orphaned jobs as failed
- Detect corrupted snapshots
- Prevent corrupted snapshots from finalization

---

## Corruption Handling

- Corruption is explicit state
- Corrupted snapshots are immutable
- Corruption blocks downstream phases

---

## Audit

Phase S MUST audit:
- draft.abandoned
- job.retry_exhausted
- queue.backpressure_triggered
- snapshot.corrupted_detected
- system.recovery_completed

---

## Forbidden

- Silent recovery
- Auto-repair of geometry
- Snapshot mutation during recovery
- Unbounded retries

