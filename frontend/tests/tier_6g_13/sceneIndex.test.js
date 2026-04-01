import { describe, it, expect } from "vitest";

function buildSceneIndexMock(snapshot) {
  const nodes = snapshot.body_state?.nodes || [];

  return {
    objects: nodes.map((n) => ({
      id: n.id,
      asset_ref: n.asset_id ? `asset:${n.asset_id}` : null,
    })),
  };
}

describe("Tier 6G.13 — scene index asset binding", () => {
  it("adds asset_ref when asset_id exists", () => {
    const snapshot = {
      body_state: {
        nodes: [{ id: "car", asset_id: 42 }],
      },
    };

    const result = buildSceneIndexMock(snapshot);

    expect(result.objects[0].asset_ref).toBe("asset:42");
  });

  it("returns null when no asset_id", () => {
    const snapshot = {
      body_state: {
        nodes: [{ id: "box" }],
      },
    };

    const result = buildSceneIndexMock(snapshot);

    expect(result.objects[0].asset_ref).toBe(null);
  });
});
