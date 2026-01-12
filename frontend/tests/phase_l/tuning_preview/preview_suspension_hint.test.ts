import { mapTuningToPreview } from "@/engine/preview/TuningPreviewMapper"

test("sport_low suspension applies visual ride height hint", () => {
  const snapshot = {
    tuning: {
      suspension: { preset_id: "sport_low" },
    },
  }

  const preview = mapTuningToPreview(snapshot)

  expect(preview.suspension?.visualRideHeightOffset).toBeLessThan(0)
})

