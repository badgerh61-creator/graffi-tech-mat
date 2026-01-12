import { mapDecorToPreview } from "@/engine/preview/DecorPreviewMapper"

test("decor preview mapping is deterministic", () => {
  const snapshot = {
    decor: {
      decals: [
        {
          id: "decal_1",
          panel: "door_left",
          uv: { x: 0.2, y: 0.3, scale: 1, rotation: 0 },
        },
      ],
    },
  }

  const a = mapDecorToPreview(snapshot)
  const b = mapDecorToPreview(snapshot)

  expect(a).toEqual(b)
})

