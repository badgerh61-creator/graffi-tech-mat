import { mapSnapshotToUnifiedPreview } from "@/engine/preview/UnifiedPreviewMapper"

test("switching snapshot clears previous preview data", () => {
  const s1 = {
    id: 1,
    model_id: 1,
    hash: "a",
    decor: { decals: [{ id: "d1" }] },
  }

  const s2 = {
    id: 2,
    model_id: 1,
    hash: "b",
    decor: { decals: [] },
  }

  const p1 = mapSnapshotToUnifiedPreview(s1)
  const p2 = mapSnapshotToUnifiedPreview(s2)

  expect(p1.decor.decals.length).toBe(1)
  expect(p2.decor.decals.length).toBe(0)
})

