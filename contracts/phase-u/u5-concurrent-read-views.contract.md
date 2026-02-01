# Phase U.5 — Concurrent Read Views

## Purpose
Enable concurrent, non-mutating access to draft snapshots.

---

## Definitions

- Read View:
  A session-bound, non-owning view of a snapshot.

- Writer:
  The single draft owner (U.2).

---

## Read View Rules

- Any authorized user may open a read view
- Read views do NOT acquire locks
- Read views do NOT block ownership
- Read views cannot execute mutating tools

---

## API Semantics

GET /snapshots/{id}/view

Returns:
- snapshot metadata
- scene state hash
- read-only flag

---

## Enforcement

- Mutating tools invoked from read view → 403
- Read view never escalates authority
- Session expiration closes read view

---

## Audit

- snapshot.view.opened
- snapshot.view.closed
- snapshot.view.violation (mutation attempt)

---

## Forbidden

- Implicit ownership via viewing
- Lock upgrades from read view
- UI-only read-only enforcement

