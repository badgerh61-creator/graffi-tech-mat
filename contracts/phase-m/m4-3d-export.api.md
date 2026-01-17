# Phase M.4 — 3D Asset Export

## Purpose
Produce deterministic 3D asset files from completed snapshots.

---

## Supported Formats

- glb
- gltf

(FBX / USD explicitly deferred to future phases)

---

## Inputs

- export_request_id
- snapshot_id
- export_type: 3d
- validated options (Phase M.1)

---

## 3D Export Options

```json
{
  "format": "glb | gltf",
  "include_materials": true,
  "include_textures": true
}

