import { mapDecorToPreview } from "@/engine/preview/DecorPreviewMapper"

test("invalid decor payload does not crash preview", () => {
  const snapshot = {
    decor: null,
  }

  const preview = mapDecorToPreview(snapshot)

  expect(preview).toEqual({})
})

