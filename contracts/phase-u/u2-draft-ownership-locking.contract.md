# Phase U.2 — Draft Ownership & Locking

## Purpose
Define exclusive ownership and locking rules for draft snapshots.

---

## Draft Ownership

- Draft snapshots may have at most one owner
- Ownership grants exclusive mutation rights
- Ownership is scoped to (user_id, snapshot_id)
- Completed snapshots cannot be owned

---

## Locking Rules

- Acquiring ownership implicitly locks the draft
- Only the owner may execute mutation tools
- Non-owners attempting mutation are rejected
- Ownership may be released explicitly
- Ownership may be force-released by admin

---

## API

POST /snapshots/{snapshot_id}/lock  
POST /snapshots/{snapshot_id}/unlock  

---

## Preconditions

- User authenticated
- Active session (Phase U.1)
- Snapshot exists
- Snapshot.status == "draft"

---

## Failure Modes

| Condition | HTTP |
|--------|------|
| Snapshot not draft | 409 |
| Already owned | 409 |
| Not owner on unlock | 403 |
| No active session | 403 |

---

## Audit Events

- draft.locked
- draft.unlocked
- draft.lock.denied
- draft.lock.forced

---

## Forbidden

- Implicit ownership
- Multiple owners
- UI-enforced locking
- Mutating without ownership

