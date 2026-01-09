# Phase L — Decor Preview Rendering Contract

## Status
PROOF MODE — READ ONLY

## Purpose
Define how decor data from a rendered snapshot is converted into
a temporary engine preview scene without any mutation or persistence.

## Inputs
- RenderedSnapshot.payload.decor.decals[]

## Outputs
- Ephemeral engine preview nodes
- No persistence
- No caching

## Guarantees
- Deterministic output for identical input
- Preview scene fully rebuilt on each call
- Snapshot switching clears prior preview
- Invalid decor payload fails safely

## Prohibited
- Writing snapshots
- Writing journal entries
- Modifying workspace state
- Caching preview nodes across calls

## Interface
DecorPreviewMapper:
- build(input) → preview nodes
- clear() → destroy all preview nodes

## Relationship to other phases
- Consumes Phase K.1 decor mutations
- Does not introduce new mutations
- Enables future material & bodykit previews

## Freeze Criteria
- All Phase L proof tests passing
- No backend changes required

