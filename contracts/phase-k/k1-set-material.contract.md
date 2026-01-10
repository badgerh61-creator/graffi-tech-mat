# Phase K.1 — Decor Mutation Contract
## Mutation: decor.exterior.set-material

### Status
DRAFT → FREEZABLE after tests pass

---

## Purpose

Apply or change a material on a specific exterior panel
in a deterministic, reversible, journaled way.

This mutation is visual-only.
It does not affect physics, simulation, or engine state.

---

## Endpoint

POST /mutations/decor/exterior/set-material

---

## Request Payload

```json
{
  "project_id": "uuid",
  "snapshot_base_id": "uuid",
  "panel": "string",
  "material": {
    "material_id": "uuid",
    "parameters": {
      "color": "#RRGGBB",
      "finish": "matte | gloss | metallic"
    }
  }
}

