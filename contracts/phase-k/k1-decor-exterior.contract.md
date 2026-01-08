# Phase K.1 — Exterior Decor Mutations (Contract)

## Status
DRAFT → FREEZE TARGET

## Depends on
- Phase I (Mutation & Snapshot Law)
- Phase J (Workspace Assembly)
- Phase K.0 (Write Capability Gate)

---

## 1. Purpose

Phase K.1 introduces **controlled, reversible, journaled exterior decoration**
for vehicles while preserving all previously frozen guarantees.

Exterior decor is **visual-only** and must not affect physics, simulation,
or engine authority.

---

## 2. Non-Negotiable Rules

1. No direct engine writes
2. No in-place snapshot mutation
3. One mutation affects exactly one domain
4. One mutation produces exactly one new snapshot
5. Every mutation is journaled
6. Undo is performed via snapshot switching (Phase I.3)
7. Workspace remains read-only

Violating any rule invalidates Phase K.1.

---

## 3. Capability Gate (Mandatory)

All K.1 mutations require:

```json
{
  "canDecorateExterior": true
}

