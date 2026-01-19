# Phase O.2 — Webhooks & External Integrations

## Purpose
Notify external systems of distribution lifecycle events without exposing artifacts.

---

## Supported Events (Initial)

- DISTRIBUTION_REQUESTED
- SIGNED_URL_CREATED
- DISTRIBUTION_REVOKED
- DISTRIBUTION_ACCESSED (future)

---

## Webhook Configuration

```json
{
  "id": "uuid",
  "project_id": "uuid",
  "url": "https://example.com/webhook",
  "events": ["SIGNED_URL_CREATED", "DISTRIBUTION_REVOKED"],
  "secret_ref": "vault://graffi/webhooks/abc",
  "enabled": true
}
```

---

## Delivery Rules (LOCKED)

- HTTPS only
- JSON payloads only
- Notification-only (no links required)
- Signed payload (HMAC)
- Time-bound retries
- Append-only delivery audit

---

## Payload Shape (Canonical)

```json
{
  "event_type": "SIGNED_URL_CREATED",
  "occurred_at": "iso-8601",
  "project_id": "uuid",
  "export_id": "uuid",
  "distribution_request_id": "uuid",
  "metadata": {}
}
```

---

## Enforcement

- Admin-only configuration
- Policy-gated (Phase O.1)
- Project state enforced (archived/suspended disabled)
- Revocation does not affect history

---

## Forbidden

- File transfer
- Permanent secrets in DB
- Webhooks granting access
- Unauthenticated delivery

