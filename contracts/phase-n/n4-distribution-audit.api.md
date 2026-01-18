# Phase N.4 — Distribution History & Audit

## Purpose
Provide an immutable, auditable record of all distribution activity.

---

## Audit Events (Canonical)

- DISTRIBUTION_REQUESTED
- SIGNED_URL_CREATED
- DISTRIBUTION_REVOKED
- DISTRIBUTION_ACCESSED (future)

---

## Audit Record Schema

```json
{
  "id": "uuid",
  "event_type": "string",
  "export_id": "uuid",
  "distribution_request_id": "uuid",
  "actor_user_id": "uuid",
  "metadata": {},
  "created_at": "iso-8601"
}

