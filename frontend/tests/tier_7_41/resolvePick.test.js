import { describe, it, expect } from "vitest";
import { resolvePick } from "../../src/editor/selection/resolvePick";

describe("resolvePick", () => {
  it("prioritizes decal over mesh over obj in all mode", () => {
    const r = resolvePick(["obj:a", "mesh:a::m1", "decal:dec-9"], "all");
    expect(r.kind).toBe("decal");
    expect(r.key).toBe("dec-9");
  });

  it("filters to meshes only", () => {
    const r = resolvePick(["obj:a", "mesh:a::m1", "decal:dec-9"], "meshes");
    expect(r.kind).toBe("mesh");
  });

  it("returns null if nothing matches filter", () => {
    const r = resolvePick(["decal:dec-1"], "objects");
    expect(r).toBe(null);
  });
});
