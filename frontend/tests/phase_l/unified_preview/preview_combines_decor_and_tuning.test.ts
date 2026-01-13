import { mapSnapshotToUnifiedPreview } from "@/engine/preview/UnifiedPreviewMapper"

test("decor and tuning are both present in unified preview", () => {
  const snapshot = {
    id: 2,
    model_id: 20,
    hash: "xyz789",
    decor: {
      decals: [{ id: "d1", panel: "door", material: "vinyl" }],
    },
    tuning: {
      suspension: {
        preset_id: "sport_low", // ✅ FIX: must be preset_id
      },
    },
  }

  const preview = mapSnapshotToUnifiedPreview(snapshot)

  expect(preview.decor.decals.length).toBe(1)
  expect(preview.tuning.suspension?.visualRideHeightOffset).toBe(-0.04)
})

