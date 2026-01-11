# Phase K.1 — Decor Mutation Contract
## Mutation: decor.exterior.swap-bodykit

### Status
DRAFT → FREEZABLE after tests pass

---

## Purpose

Apply a predefined exterior bodykit preset to a vehicle snapshot
in a deterministic, reversible, journaled manner.

This mutation is **visual-structural only**.
No physics, simulation, or mesh editing is performed.

---

## Endpoint

POST /mutations/decor/exterior/swap-bodykit

---

## Request Payload

```json
{
  "project_id": "uuid",
  "snapshot_base_id": "uuid",
  "bodykit_id": "uuid"
}

