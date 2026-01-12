import { mapDecorToPreview } from "@/engine/preview/DecorPreviewMapper"

test("decor decals are exposed to preview layer", () => {
  const snapshot = {
    decor: {
      decals: [
        { id: "d1", panel: "hood" },
        { id: "d2", panel: "roof" },
      ],
    },
  }

  const preview = mapDecorToPreview(snapshot)

  expect(preview.decals).toHaveLength(2)
})

