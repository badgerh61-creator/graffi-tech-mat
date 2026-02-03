# Phase E.1 — Studio State Awareness (Read-Only)

## Purpose
Expose authoritative studio state to the UI without granting control.

---

## Required State Fields

### Station
- Source: Phase T
- Values: geometry, curve, panel, validation, review

### Mode
- Source: Phase T
- Values: edit, review, read_only

### Snapshot State
- Source: Phase 4
- Values: draft, completed, failed

### Draft Ownership
- Source: Phase U
- Values:
  - owned_by_self
  - owned_by_other
  - unowned
  - not_applicable

### Block Reason (Optional)
- Source: Kernel rejection
- Must include:
  - code
  - human-readable explanation

---

## Guarantees

- State is read-only
- State is derived directly from kernel
- UI must not reinterpret or override values

---

## Forbidden

- UI-side authority logic
- Derived legality
- “Best guess” states
- Silent suppression of kernel reasons

