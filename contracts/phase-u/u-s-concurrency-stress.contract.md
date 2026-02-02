# Phase U-S — Concurrency & Invariant Stress Tests

## Purpose
Validate collaboration and authority invariants under concurrent access.

---

## Scope

- Concurrent sessions
- Simultaneous tool execution
- Ownership races
- Read/write contention
- Session expiration races
- Handoff collisions

---

## Guarantees

- At most one writer per draft
- No lost updates
- No implicit authority escalation
- No silent failures
- All violations audited

---

## Failure Semantics

- Violations must raise explicit errors
- System must remain consistent after failure
- Partial execution is forbidden

---

## Forbidden

- Flaky tests
- Timing-based assertions without guards
- UI-driven authority assumptions

