# Phase K.1 — Decor Mutation Contract
## Mutation: decor.exterior.remove-decal

### Status
DRAFT → FREEZABLE after tests pass

---

## Purpose

Remove an existing exterior decal instance from a snapshot
in a deterministic, reversible, journaled way.

This mutation is visual-only.
No engine state, physics, or simulation is affected.

---

## Endpoint

POST /mutations/decor/exterior/remove-decal

---

## Request Payload

```json
{
  "project_id": "uuid",
  "snapshot_base_id": "uuid",
  "decal_instance_id": "uuid"
}

