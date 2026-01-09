// tests/phase_l/decor_preview/preview_deterministic.test.ts

import { test, expect } from "vitest"
import { buildDecorPreview } from "@/engine/decor/DecorPreviewMapper"
import { hashPreview } from "@/engine/testing/hashPreview"

const SNAPSHOT = {
  snapshotId: "s1",
  decor: {
    decals: [
      {
        instance_id: "d1",
        asset_id: "decal_1",
        panel: "roof",
        uv: { x: 0.1, y: 0.2, scale: 1, rotation: 0 },
      },
    ],
  },
}

test("same snapshot produces identical preview", () => {
  const a = buildDecorPreview(SNAPSHOT)
  const b = buildDecorPreview(SNAPSHOT)

  expect(hashPreview(a)).toEqual(hashPreview(b))
})

