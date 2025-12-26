# PHASE C2 — Email-Based Collaboration Invites (FROZEN)

Phase: C2  
Date: 2025-12-25  
Status: FROZEN  
Alembic Head: b264282e1afa  
Branch: phase-10-upload-hardening

---

## Purpose

Introduce email-based collaboration invites to allow sharing models
with users who may not yet have accounts.

This phase extends the collaboration system without breaking:
- Phase 10 RBAC
- Phase 11 asset lifecycle
- Existing model permissions

---

## Database Changes

### New Table: model_invites

Created via Alembic migration `b264282e1afa`.

Fields:

- id (PK)
- model_id → models.id (CASCADE)
- email (indexed)
- role (viewer | editor)
- token (unique, indexed)
- expires_at
- created_by → users.id (SET NULL)
- created_at

Verified via SQLite schema inspection.

No existing tables modified.

---

## Backend Capabilities

- Create model invite by email
- Secure token-based invite system
- Role assigned at invite time
- Invite tied to specific model
- Invite cleanup handled via expiration (manual / future automation)

No email delivery implemented in this phase.

---

## API Surface (Additive)

- POST /models/{model_id}/invites
- GET /models/{model_id}/invites
- POST /models/invites/{token}/accept
- DELETE /models/{model_id}/invites/{invite_id}

Existing collaboration endpoints unchanged.

---

## Security & RBAC

- Only owners/admins can create or revoke invites
- Viewer/editor permissions enforced at acceptance
- Invite tokens are unguessable (64-char)
- Foreign keys enforced at DB level

---

## Audit Logging

Invite actions are auditable via audit_logs:
- Invite creation
- Invite acceptance
- Invite revocation

Audit system remains append-only.

---

## Explicitly Out of Scope

- Email sending (SMTP / SendGrid / SES)
- Frontend invite UI
- Invite expiration jobs
- Public share links

---

## Freeze Rules

After this file is committed:

- No schema changes to model_invites
- No breaking changes to collaboration APIs
- No RBAC semantic changes
- Only additive extensions allowed

---

## Status

PHASE C2 IS COMPLETE AND FROZEN.

