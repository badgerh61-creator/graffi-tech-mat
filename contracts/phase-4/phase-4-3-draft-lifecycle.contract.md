# Phase 4.3 — Draft Snapshot Lifecycle

## Snapshot States

- completed (immutable)
- draft (mutable, temporary)

---

## Draft Rules

- Only one draft per project
- Draft overwrites itself on save
- Draft blocks export & distribution

---

## Endpoints

### PATCH /snapshots/{id}/autosave

Autosave draft snapshot state.

Preconditions:
- Snapshot exists
- Snapshot.status == "draft"

Behavior:
- Replace scene_state_hash
- Update updated_at

---

### POST /snapshots/{id}/finalize

Finalize draft snapshot.

Preconditions:
- Snapshot exists
- Snapshot.status == "draft"

Behavior:
- Create new completed snapshot
- Copy scene_state_hash
- Delete draft snapshot

---

## Forbidden

- Editing completed snapshots
- Exporting while draft exists
- Multiple drafts per project

