# Phase T-X — Studio Kernel Integration Tests

## Purpose
Verify combined enforcement of Stations, Tools, Flow Graph, and Modes.

---

## Kernel Gates (Execution Order)

1. Station validity
2. Tool registry validation
3. Flow graph legality
4. Mode enforcement
5. Capability check
6. Execution + audit

---

## Guarantees

- All gates are evaluated per command
- First failing gate blocks execution
- Rejection reason is explicit
- No audit on rejection
- Audit emitted exactly once on success

---

## Forbidden

- Gate bypass via composition
- Partial execution
- UI-driven gate resolution

