import { mapDecorToPreview } from "@/engine/preview/DecorPreviewMapper"

test("switching snapshots clears previous decor preview", () => {
  const snapshotA = {
    decor: {
      decals: [{ id: "d1", panel: "door_left" }],
    },
  }

  const snapshotB = {
    decor: {},
  }

  const previewA = mapDecorToPreview(snapshotA)
  const previewB = mapDecorToPreview(snapshotB)

  expect(previewA.decals?.length).toBe(1)
  expect(previewB.decals).toBeUndefined()
})

