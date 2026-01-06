# Phase I.5.A — Project Rename (API Contract)

## Purpose
Rename a project without affecting snapshots, scenes, or jobs.

---

## Endpoint

POST /projects/{project_id}/mutations/rename

---

## Authorization

Required capability:
- canRenameProject

Allowed roles:
- Owner
- Admin

---

## Preconditions

1. Project exists
2. Project is not archived
3. Name is non-empty
4. Name differs from current name

---

## Request

```json
{
  "name": "New Project Name"
}

