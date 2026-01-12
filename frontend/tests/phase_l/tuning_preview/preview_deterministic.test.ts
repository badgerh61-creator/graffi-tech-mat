import { mapTuningToPreview } from "@/engine/preview/TuningPreviewMapper"

test("tuning preview mapping is deterministic", () => {
  const snapshot = {
    tuning: {
      wheels: { diameter: 19, width: 9.5, offset: 35 },
    },
  }

  const a = mapTuningToPreview(snapshot)
  const b = mapTuningToPreview(snapshot)

  expect(a).toEqual(b)
})

