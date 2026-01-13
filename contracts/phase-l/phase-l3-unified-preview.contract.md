# Phase L.3 — Unified Preview Contract (Decor + Tuning)

## Purpose
Define a single deterministic preview payload derived from a snapshot,
combining decor and tuning into one read-only engine input.

## Scope
- Read-only
- No mutations
- No engine state changes

## Input
RenderedSnapshot (completed, immutable)

## Output
UnifiedPreviewPayload

## UnifiedPreviewPayload

```ts
UnifiedPreviewPayload {
  snapshot_id: number

  vehicle: {
    model_id: number
    bodykit?: string
  }

  decor: {
    decals: Array<{
      id: string
      panel: string
      material: string
      uv_transform: {
        scale: number
        rotation: number
        offset: [number, number]
      }
    }>

    materials: Record<
      string,
      {
        material_id: string
        color?: string
      }
    >
  }

  tuning: {
    suspension?: {
      preset: string
      ride_height_hint?: number
    }

    wheels?: {
      preset: string
      diameter_hint?: number
    }

    brakes?: {
      preset: string
    }

    engine?: {
      preset: string
    }
  }

  meta: {
    deterministic_hash: string
  }
}

