# Phase K.0 — Write Capability Gate (Contract)

## Status
DRAFT → FREEZE TARGET

## Purpose
Define the authoritative capability model that controls all
write-enabled vehicle modification in Phase K.

No Phase K mutation may exist or execute without passing this gate.

---

## Capability Source of Truth

- Capabilities are derived **server-side only**
- Evaluated per user, per project
- Returned only via the workspace payload
- Client input is ignored

---

## Capability Flags (FROZEN NAMES)

```json
{
  "canDecorateExterior": false,
  "canDecorateInterior": false,
  "canTuneParameters": false,
  "canModifyBody": false,
  "canOverrideValidation": false
}

