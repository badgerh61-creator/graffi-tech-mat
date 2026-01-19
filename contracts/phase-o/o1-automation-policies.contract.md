# Phase O.1 — Automation Policies

## Purpose
Define the allowed automation behaviors and enforce policy boundaries.

Automation policies describe **what MAY happen automatically**, not how.

---

## Policy Types (Initial)

```ts
type AutomationPolicy =
  | "auto_expire_links"
  | "auto_revoke_on_project_archive"
  | "auto_notify_external_system"
  | "log_distribution_access";
```

---

## Policy Rules

### auto_expire_links
- Allowed only for signed URLs
- Expiration must already exist (cannot create permanent access)
- Cannot extend expiration
- Cannot affect revoked links

### auto_revoke_on_project_archive
- Revokes all active distribution requests
- Does not delete exports
- Does not delete audit history

### auto_notify_external_system
- Notification only
- No file transfer
- No credential sharing
- Must be capability-gated

### log_distribution_access
- Read-only logging
- Append-only audit events
- No access control decisions

---

## Policy Evaluation Contract

```json
{
  "policy": "auto_expire_links",
  "enabled": true,
  "scope": {
    "project_id": "uuid"
  }
}
```

---

## Enforcement Rules

- Policies are evaluated server-side only
- Policies cannot weaken Phase N guarantees
- Policies require Phase O.0 authorization
- Policies are explicit and opt-in

---

## Forbidden

- Policies that create permanent access
- Policies that bypass audit
- Policies that mutate export bytes
- Policies that grant editor or snapshot access

