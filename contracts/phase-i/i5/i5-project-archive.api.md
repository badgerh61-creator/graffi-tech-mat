
---

## 📄 FILE 2  
### `contracts/phase-i/i5/i5-project-archive.api.md`

```md
# Phase I.5.B — Project Archive (API Contract)

## Purpose
Archive a project, making it permanently read-only.

---

## Endpoint

POST /projects/{project_id}/mutations/archive

---

## Authorization

Required capability:
- canArchiveProject

Allowed roles:
- Owner
- Admin

---

## Preconditions

1. Project exists
2. Project is not already archived

---

## Success Response

```json
{
  "project_id": "uuid",
  "archived": true
}

