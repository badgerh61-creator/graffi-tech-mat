import { test, expect } from "vitest"
import { buildDecorPreview } from "@/engine/decor/DecorPreviewMapper"
import { hashPreview } from "@/engine/testing/hashPreview"

const SNAPSHOT = {
  snapshotId: "s1",
  decor: {
    decals: [
      {
        instance_id: "d1",
        asset_id: "decal_asset_1",
        panel: "roof",
        uv: { x: 0.1, y: 0.1, scale: 1.2, rotation: 15 },
      },
    ],
  },
}

test("same snapshot produces identical preview", () => {
  const a = buildDecorPreview(SNAPSHOT)
  const b = buildDecorPreview(SNAPSHOT)

  expect(hashPreview(a)).toEqual(hashPreview(b))
})

