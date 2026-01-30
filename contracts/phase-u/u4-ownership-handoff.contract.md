# Phase U.4 — Ownership Handoff Protocol

## Purpose
Define safe transfer of draft snapshot ownership between users.

---

## Handoff Rules

- Only the current draft owner may initiate handoff
- Target user must have an active session
- Draft must be conflict-free
- Ownership transfer is atomic
- Previous owner immediately loses mutation rights

---

## API

POST /snapshots/{snapshot_id}/handoff

Body:
{
  "to_user_id": "<uuid>"
}

---

## Preconditions

- User authenticated
- Active session (U.1)
- Snapshot exists
- Snapshot.status == "draft"
- Caller owns the draft
- No unresolved conflicts (U.3)

---

## Failure Modes

| Condition | HTTP |
|---------|------|
| Not owner | 403 |
| Target not present | 409 |
| Conflict exists | 409 |
| Snapshot not draft | 409 |

---

## Audit Events

- draft.handoff.initiated
- draft.handoff.completed
- draft.handoff.denied

---

## Forbidden

- Implicit handoff
- Multi-owner drafts
- UI-only authority transfer

