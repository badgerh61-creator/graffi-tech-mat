import { mapSnapshotToUnifiedPreview } from "@/engine/preview/UnifiedPreviewMapper"

test("unified preview is deterministic", () => {
  const snapshot = {
    id: 1,
    model_id: 10,
    hash: "abc123",
    decor: { decals: [] },
    tuning: { suspension: { preset: "sport_low" } },
  }

  const a = mapSnapshotToUnifiedPreview(snapshot)
  const b = mapSnapshotToUnifiedPreview(snapshot)

  expect(a).toEqual(b)
})

