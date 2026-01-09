import { test, expect } from "vitest"
import { buildDecorPreview } from "@/engine/decor/DecorPreviewMapper"

const SNAPSHOT_WITH_DECAL = {
  snapshotId: "s1",
  decor: {
    decals: [
      {
        instance_id: "d1",
        asset_id: "decal_asset_1",
        panel: "door_left",
        uv: { x: 0.2, y: 0.3, scale: 1.0, rotation: 0 },
      },
    ],
  },
}

test("decor preview loads decorated snapshot", () => {
  const result = buildDecorPreview(SNAPSHOT_WITH_DECAL)

  expect(result.nodes.length).toBe(1)
  expect(result.nodes[0].type).toBe("decal")
  expect(result.nodes[0].targetPanel).toBe("door_left")
})

