# Phase K.2 — Tuning Mutation Contract
## Mutation: tuning.set-wheels

### Status
DRAFT → FREEZABLE once tests pass

---

## Purpose

Update wheel parameters (diameter, width, offset) for a vehicle snapshot
in a deterministic, reversible, journaled manner.

This mutation is **data-only**.
No physics, simulation, or engine evaluation is performed.

---

## Endpoint

POST /mutations/tuning/set-wheels

---

## Request Payload

```json
{
  "project_id": "uuid",
  "snapshot_base_id": "uuid",
  "diameter": 19,
  "width": 9.5,
  "offset": 35
}

