import { mapSnapshotToUnifiedPreview } from "@/engine/preview/UnifiedPreviewMapper"

test("unified preview combines decor, tuning, and body", () => {
  const snapshot = {
    id: 3,
    model_id: 42,
    hash: "abc-body",
    decor: {
      decals: [{ id: "d1", panel: "door", material: "vinyl" }],
    },
    tuning: {
      suspension: {
        preset_id: "sport_low",
      },
    },
    body: {
      preset_id: "widebody_v1",
      parameters: {
        width_factor: 1.2,
      },
    },
  }

  const preview = mapSnapshotToUnifiedPreview(snapshot)

  // Decor
  expect(preview.decor.decals.length).toBe(1)

  // Tuning
  expect(preview.tuning.suspension?.visualRideHeightOffset).toBe(-0.04)

  // Body
  expect(preview.body?.preset_id).toBe("widebody_v1")
})

