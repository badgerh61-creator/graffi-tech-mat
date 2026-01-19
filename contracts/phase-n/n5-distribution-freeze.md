# Phase N.5 — Distribution & Sharing Freeze

## Status
FROZEN

## Effective Scope
Phase N (N.0 → N.4)

## Depends On
Phase M — Authoritative Exports

## Does Not Depend On
Editor
Engine
AI
Rendering
Snapshots

---

## 1. Purpose

Phase N governs **how exported artifacts leave the system safely**.

It defines:
- Who may distribute exports
- How access is granted
- How access is revoked
- How all actions are audited

Phase N is the **security boundary** between Graffi-Tech-Mat and the outside world.

---

## 2. Guaranteed Capabilities

Phase N guarantees the following, without exception:

1. Export artifacts are immutable
2. Distribution is capability-gated
3. Signed access is time-bound
4. Access can be revoked immediately
5. All distribution actions are audited
6. Audit records are append-only and immutable
7. Editor and snapshot access is never exposed

---

## 3. Frozen Sub-Phases

### N.0 — Distribution Authority & Capabilities
- Capabilities are server-derived only
- Admin vs Owner privileges are enforced
- Archived projects disable all distribution

### N.1 — Distribution Requests
- Explicit target contracts
- Export existence and completion enforced
- No implicit distribution paths

### N.2 — Signed URL Delivery
- Single-export scoped
- Time-limited
- Revocable
- HTTPS-only
- No directory or snapshot access

### N.3 — Access Revocation
- Immediate revocation
- No artifact deletion
- No partial revocation
- Idempotent behavior enforced

### N.4 — Distribution History & Audit
- Canonical audit events
- Append-only records
- ORM-level immutability enforcement
- Capability-gated read access

---

## 4. Explicit Non-Goals (LOCKED OUT)

Phase N explicitly does NOT:

- Stream files
- Render exports
- Modify export bytes
- Expose editor state
- Expose snapshots
- Provide permanent links
- Allow unaudited access
- Perform background automation

Any of the above belongs to **Phase O or later**.

---

## 5. Security Invariants (NON-NEGOTIABLE)

- All access is authenticated or cryptographically signed
- All access has a defined lifetime
- All revocations take effect immediately
- No distribution path bypasses audit
- No client-authored audit records
- No mutable audit state

Violating any invariant **breaks the Phase N freeze**.

---

## 6. Audit Guarantees

Phase N audit guarantees:

- Every distribution request is recorded
- Every signed URL creation is recorded
- Every revocation is recorded
- Audit records cannot be edited or deleted
- Audit visibility is capability-gated

Future access logging (`DISTRIBUTION_ACCESSED`) is explicitly deferred.

---

## 7. Extension Points (ALLOWED ONLY VIA PHASE O)

The following extensions are permitted **only** in Phase O or later:

- Automated distribution policies
- External system delivery
- Webhooks
- Access logging
- Scheduled expiration enforcement
- Compliance export bundles

Phase N code must not be modified to add these.

---

## 8. Change Control Policy

Any of the following actions **break the Phase N freeze**:

- Changing distribution capability semantics
- Allowing distribution without audit
- Making audit records mutable
- Adding new distribution targets
- Allowing permanent or multi-export links
- Exposing editor or snapshot access

Breaking the freeze requires:
1. New phase designation
2. New contracts
3. Explicit migration plan

---

## 9. Compliance Posture

Phase N is compatible with:
- SOC 2 (auditability, access control)
- ISO 27001 (least privilege, traceability)
- Enterprise client IP protection requirements

Phase N provides **defensible controls**, not policy automation.

---

## 10. Final Declaration

Phase N is hereby declared:

- Complete
- Frozen
- Auditable
- Security-bound
- Extension-safe

All future work must treat Phase N as **read-only** unless explicitly superseded.


