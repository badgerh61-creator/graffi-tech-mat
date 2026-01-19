# Phase M — Immutable Outputs

## Purpose
Generate deterministic, immutable export artifacts from validated geometry.

---

## Preconditions

- Geometry MUST pass Phase L validation
- Snapshot MUST be completed
- Snapshot MUST be immutable

---

## Export Artifact Schema

```json
{
  "id": "uuid",
  "snapshot_id": "uuid",
  "format": "png | svg | pdf | glb | gltf | zip",
  "hash": "sha256",
  "created_at": "iso-8601",
  "status": "completed | failed"
}

