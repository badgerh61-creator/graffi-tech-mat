import { mapTuningToPreview } from "@/engine/preview/TuningPreviewMapper"

test("switching snapshot clears previous tuning preview", () => {
  const s1 = {
    tuning: {
      engine: { preset_id: "stage1" },
    },
  }

  const s2 = {}

  const p1 = mapTuningToPreview(s1)
  const p2 = mapTuningToPreview(s2)

  expect(p2.engine).toBeUndefined()
})

