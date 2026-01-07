# Phase I.7 — Scene Save (API Contract)

## Purpose
Persist full editor scene state in a deterministic, auditable manner.

---

## Endpoint

POST /scenes/{scene_id}/mutations/save

---

## Authorization

Required capability:
- canSaveScene

Allowed roles:
- Editor
- Owner
- Admin

---

## Preconditions

1. Scene exists
2. Project is not archived
3. Payload is valid
4. Hash computation succeeds

---

## Request

```json
{
  "scene_state": { ... }
}

