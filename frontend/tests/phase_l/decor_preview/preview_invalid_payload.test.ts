import { test, expect } from "vitest"
import { buildDecorPreview } from "@/engine/decor/DecorPreviewMapper"

test("invalid decor payload fails safely", () => {
  const invalidSnapshot = {
    snapshotId: "bad",
    decor: {
      decals: "not-an-array" as any
    },
  }

  expect(() => buildDecorPreview(invalidSnapshot)).toThrow()
})

