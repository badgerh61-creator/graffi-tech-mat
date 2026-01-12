import { mapTuningToPreview } from "@/engine/preview/TuningPreviewMapper"

test("missing tuning does not crash preview", () => {
  const snapshot = {}

  const preview = mapTuningToPreview(snapshot)

  expect(preview).toEqual({})
})

