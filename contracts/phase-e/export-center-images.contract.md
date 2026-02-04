# Export Center — Images Only

## Purpose
Allow users to export raster images from completed snapshots.

---

## Scope

Supported formats:
- PNG
- JPEG

Unsupported (explicitly forbidden):
- SVG
- PDF
- GLB / GLTF
- Video

---

## Preconditions

- User authenticated
- User has export capability
- Snapshot exists
- Snapshot.status == "completed"

---

## API Endpoints

POST /exports/images
GET  /exports/{export_id}

---

## POST Payload

```json
{
  "snapshot_id": "uuid",
  "format": "png | jpeg",
  "resolution": "low | medium | high"
}

