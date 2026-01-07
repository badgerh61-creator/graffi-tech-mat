
---

## 📄 FILE 2  
### `contracts/phase-i/i7/i7-scene-save.journal.md`

```md
# Phase I.7 — Scene Save (Journal Contract)

## Journal Entry Type

SAVE_SCENE

---

## Schema

```json
{
  "type": "SAVE_SCENE",
  "scene_id": "uuid",
  "project_id": "uuid",
  "scene_hash": "sha256",
  "snapshot_id": "uuid",
  "actor_user_id": "uuid",
  "timestamp": "iso-8601"
}

