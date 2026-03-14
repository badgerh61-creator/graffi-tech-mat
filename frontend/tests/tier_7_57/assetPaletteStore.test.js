import { describe, it, expect } from "vitest";
import {
  setActiveAssetId,
  toggleFavoriteAsset,
  pushRecentAsset,
  assetPaletteGetSnapshot,
} from "../../src/editor/assets/assetPaletteStore";

describe("assetPaletteStore", () => {
  it("sets active asset", () => {
    setActiveAssetId("asset-1");
    expect(assetPaletteGetSnapshot().activeAssetId).toBe("asset-1");
  });

  it("toggles favorite asset", () => {
    toggleFavoriteAsset("asset-fav");
    expect(assetPaletteGetSnapshot().favorites).toContain("asset-fav");
    toggleFavoriteAsset("asset-fav");
    expect(assetPaletteGetSnapshot().favorites).not.toContain("asset-fav");
  });

  it("tracks recent asset ids", () => {
    pushRecentAsset("asset-r1");
    pushRecentAsset("asset-r2");
    expect(assetPaletteGetSnapshot().recent[0]).toBe("asset-r2");
  });
});
