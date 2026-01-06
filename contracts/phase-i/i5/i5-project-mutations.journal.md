
---

## 📄 FILE 3  
### `contracts/phase-i/i5/i5-project-mutations.journal.md`

```md
# Phase I.5 — Project Mutations (Journal Contract)

## Journal Entry Types

- RENAME_PROJECT
- ARCHIVE_PROJECT

---

## Rename Entry Schema

```json
{
  "type": "RENAME_PROJECT",
  "project_id": "uuid",
  "from_name": "string",
  "to_name": "string",
  "actor_user_id": "uuid",
  "timestamp": "iso-8601"
}

