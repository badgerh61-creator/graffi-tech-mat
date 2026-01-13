import { mapDecorToPreview } from "./DecorPreviewMapper"
import { mapTuningToPreview } from "./TuningPreviewMapper"

export function mapSnapshotToUnifiedPreview(snapshot: any) {
  if (!snapshot || typeof snapshot !== "object") {
    return {
      snapshot_id: null,
      vehicle: {},
      decor: { decals: [], materials: {} },
      tuning: {},
      meta: { deterministic_hash: "" },
    }
  }

  return {
    snapshot_id: snapshot.id,

    vehicle: {
      model_id: snapshot.model_id,
      bodykit: snapshot.bodykit ?? undefined,
    },

    decor: mapDecorToPreview(snapshot),
    tuning: mapTuningToPreview(snapshot),

    meta: {
      deterministic_hash: snapshot.hash,
    },
  }
}

