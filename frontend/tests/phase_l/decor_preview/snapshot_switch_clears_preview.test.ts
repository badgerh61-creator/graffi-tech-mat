import { test, expect } from "vitest"
import { DecorPreviewMapper } from "@/engine/decor/DecorPreviewMapper"

const SNAPSHOT_A = {
  snapshotId: "a",
  decor: {
    decals: [
      {
        instance_id: "d1",
        asset_id: "decal_asset_1",
        panel: "hood",
        uv: { x: 0.4, y: 0.4, scale: 1.0, rotation: 0 },
      },
    ],
  },
}

const SNAPSHOT_B = {
  snapshotId: "b",
  decor: { decals: [] },
}

test("switching snapshots clears previous decor", () => {
  const mapper = new DecorPreviewMapper()

  mapper.build(SNAPSHOT_A)
  expect(mapper.currentNodes().length).toBe(1)

  mapper.clear()
  mapper.build(SNAPSHOT_B)

  expect(mapper.currentNodes().length).toBe(0)
})

