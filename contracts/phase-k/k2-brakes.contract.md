# Phase K.2 — Brakes Preset Contract

## Mutation
POST /mutations/tuning/set-brakes

## Purpose
Apply a brake configuration preset to a vehicle in a deterministic,
journaled, snapshot-immutable way.

## Capability
Requires: canTune

Viewer: ❌
Editor: ❌ unless explicitly allowed
Owner/Admin: ✅

## Inputs
- project_id (int)
- snapshot_base_id (int)
- preset_id (string)

## Rules
- Snapshot base must be completed and non-obsolete
- Preset must exist
- No scene mutation
- Produces new snapshot or reuses deterministic match
- Writes journal entry

## Output
200 OK
{
  "status": "ok",
  "snapshot_id": <int>
}

## Guarantees
- Deterministic hashing
- Snapshot immutability
- Capability enforcement
- Full audit trail

