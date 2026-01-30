# Phase U.3 — Conflict Detection & Resolution

## Purpose
Detect and resolve conflicting draft snapshots during multi-user editing.

---

## Conflict Definition

A conflict exists if:
- A draft snapshot's parent no longer matches the user's base snapshot
- Another completed or draft snapshot descends from the same parent
- The user attempts mutation on a stale draft

---

## Detection Rules

- Conflict detection occurs BEFORE tool execution
- Conflicted drafts are blocked from mutation
- Conflicts are resolved explicitly

---

## Resolution Modes

- abandon: discard local draft
- rebase: create new draft from latest snapshot
- force (admin only): override and proceed

---

## API

POST /snapshots/{snapshot_id}/conflicts/check  
POST /snapshots/{snapshot_id}/conflicts/resolve  

---

## Failure Modes

| Condition | HTTP |
|---------|------|
| Conflict detected | 409 |
| Resolve without conflict | 400 |
| Unauthorized resolution | 403 |

---

## Audit Events

- draft.conflict.detected
- draft.conflict.resolved
- draft.conflict.forced

---

## Forbidden

- Automatic merge
- Implicit rebasing
- Conflict ignored by UI

