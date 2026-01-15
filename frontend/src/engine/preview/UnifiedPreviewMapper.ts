// frontend/src/engine/preview/UnifiedPreviewMapper.ts

import { mapDecorToPreview } from "./DecorPreviewMapper"
import { mapTuningToPreview } from "./TuningPreviewMapper"

export function mapSnapshotToUnifiedPreview(snapshot: any) {
  if (!snapshot || typeof snapshot !== "object") {
    return {
      snapshot_id: null,
      vehicle: {},
      decor: { decals: [], materials: {} },
      tuning: {},
      body: undefined,
      meta: { deterministic_hash: "" },
    }
  }

  return {
    snapshot_id: snapshot.id,

    vehicle: {
      model_id: snapshot.model_id,
    },

    decor: mapDecorToPreview(snapshot),
    tuning: mapTuningToPreview(snapshot),

    // ✅ ADD THIS BLOCK
    body: snapshot.body
      ? {
          preset_id: snapshot.body.preset_id,
          parameters: snapshot.body.parameters ?? {},
        }
      : undefined,

    meta: {
      deterministic_hash: snapshot.hash,
    },
  }
}

