# Phase M.5 — ZIP Packaging

## Purpose
Assemble validated export artifacts into a deterministic ZIP package.

---

## Inputs

- export_request_id
- list of export artifacts (image / print / vector / 3d)
- manifest required

---

## Determinism Rules

- File ordering is stable
- ZIP metadata normalized
- No timestamps inside ZIP
- Same inputs → identical ZIP hash

---

## Manifest Requirements

Manifest must include:
- export_request_id
- snapshot_id
- list of files
- sha256 hash per file
- generator version

---

## Execution Rules

- Runs only inside export job
- Reads artifacts only
- Writes ZIP artifact only

---

## Forbidden

- Rendering inside packager
- Snapshot mutation
- Editor state access
- Time-based file names

