# Phase N.3 — Access Revocation

## Purpose
Immediately revoke access to distributed exports without deleting artifacts.

---

## Endpoint

POST /distributions/{distribution_request_id}/revoke

---

## Preconditions

- User authenticated
- User has canRevokeAccess capability
- Distribution request exists
- Distribution request not already revoked

---

## Behavior

- Mark distribution request as revoked
- Invalidate all associated signed URLs
- Preserve export artifact
- Preserve audit history

---

## Success Response

```json
{
  "status": "revoked",
  "revoked_at": "iso-8601"
}

