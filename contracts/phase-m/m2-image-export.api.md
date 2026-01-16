# Phase M.2 — Deterministic Image Export

## Purpose
Produce deterministic raster images from completed snapshots.

---

## Inputs

- export_request_id
- snapshot_id
- image options (validated in Phase M.1)

---

## Supported Formats

- png
- jpg
- tiff

---

## Determinism Guarantees

- Same snapshot + same options → identical bytes
- No randomness
- No editor state
- No wall-clock influence

---

## Camera Rules

- camera_id must exist in snapshot
- If omitted, snapshot default camera is used
- Camera transforms are immutable

---

## Execution Rules

- Runs only inside export job
- Reads snapshot scene only
- Writes output artifact only

---

## Forbidden

- Reading editor state
- Modifying snapshot
- Random seeds
- Time-based naming

