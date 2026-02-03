# Phase E.3 — Finalization & Review Experience

## Purpose
Expose authoritative finalization and review state to the user.

---

## Finalization Signals

When a snapshot becomes completed, the system MUST expose:

- snapshot.status == "completed"
- snapshot.immutable == true
- finalized_at timestamp
- finalized_by user_id

---

## Review Mode

When in review mode:

- station == ReviewStation
- mode == read-only
- no tools available for mutation
- audit history visible

---

## UX Guarantees

- Finalization moment is explicit
- Immutability is visually reinforced
- No affordance implies editability
- Review mode is unmistakable

---

## Forbidden

- Editing completed snapshots
- UI-only review mode
- Silent finalization
- Implicit immutability

