# Phase M.3 — Vector & Print Export

## Purpose
Produce deterministic vector and print-ready artifacts from completed snapshots.

---

## Supported Export Types

### Vector
- svg
- pdf
- eps

### Print
- tiff (CMYK)
- pdf (print)

---

## Inputs

- export_request_id
- snapshot_id
- export_type: vector | print
- validated options (Phase M.1)

---

## Vector Options

```json
{
  "format": "svg | pdf | eps",
  "include_layers": true
}

