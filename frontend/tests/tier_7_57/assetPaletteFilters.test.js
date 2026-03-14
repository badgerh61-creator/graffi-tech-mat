import { describe, it, expect } from "vitest";
import { filterAssets, listCategories } from "../../src/editor/assets/assetPaletteFilters";

describe("assetPaletteFilters", () => {
  const assets = [
    { id: "asset-b", name: "Wheel", category: "wheels", kind: "wheel", tags: ["sport"] },
    { id: "asset-a", name: "Vehicle", category: "vehicles", kind: "vehicle", tags: ["demo"] },
  ];

  it("lists categories deterministically", () => {
    expect(listCategories(assets)).toEqual(["all", "vehicles", "wheels"]);
  });

  it("filters by category", () => {
    const out = filterAssets({ assets, category: "wheels" });
    expect(out).toHaveLength(1);
    expect(out[0].id).toBe("asset-b");
  });

  it("filters favorites mode", () => {
    const out = filterAssets({
      assets,
      mode: "favorites",
      favorites: ["asset-a"],
    });
    expect(out).toHaveLength(1);
    expect(out[0].id).toBe("asset-a");
  });
});
