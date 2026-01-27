# Phase U — Multi-User Collaboration Kernel

## Purpose
Define multi-actor interaction rules inside the Studio Kernel.

---

## Ownership

- Draft snapshots have exactly one owner
- Ownership is exclusive
- Ownership is auditable

---

## Locking

- Draft snapshot must be locked to mutate
- Only owner may execute tools
- Lock loss immediately blocks execution

---

## Forking

POST /projects/{project_id}/snapshots/{snapshot_id}/fork

- Creates new draft snapshot
- New snapshot owner = requesting user
- Parent snapshot remains unchanged

---

## Conflict Prevention

- Concurrent mutation is forbidden
- No optimistic merging
- Conflicts produce explicit fork paths

---

## Audit Events

- snapshot.locked
- snapshot.unlocked
- snapshot.forked
- snapshot.access_denied

---

## Forbidden

- Shared draft editing
- Silent merges
- Lock stealing
- UI-driven authority


