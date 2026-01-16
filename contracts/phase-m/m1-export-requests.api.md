# Phase M.1 — Export Request Contracts

## Purpose
Define and validate export requests independently of execution.

---

## Endpoint

POST /exports/requests

---

## Request Shape

```json
{
  "project_id": "uuid",
  "snapshot_id": "uuid",
  "export_type": "image | print | vector | 3d | package",
  "options": {}
}

