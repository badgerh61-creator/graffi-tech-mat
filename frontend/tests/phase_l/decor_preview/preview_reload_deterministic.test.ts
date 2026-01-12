import { mapDecorToPreview } from "@/engine/preview/DecorPreviewMapper"

test("reloading same snapshot yields same preview", () => {
  const snapshot = {
    decor: {
      decals: [{ id: "d1", panel: "door_left" }],
    },
  }

  const first = mapDecorToPreview(snapshot)
  const second = mapDecorToPreview(snapshot)

  expect(first).toEqual(second)
})

