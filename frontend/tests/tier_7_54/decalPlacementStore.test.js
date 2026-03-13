import { describe, it, expect } from "vitest";
import {
  setDecalPlacement,
  resetDecalPlacement,
  decalPlacementGetSnapshot,
} from "../../src/editor/decals/decalPlacementStore";

describe("decalPlacementStore", () => {
  it("stores canonical values", () => {
    setDecalPlacement({
      enabled: true,
      size: 2,
      rotation_deg: 30,
      opacity: 0.5,
      blend: "multiply",
      z_offset: 0.002,
    });

    const p = decalPlacementGetSnapshot().placement;
    expect(p.enabled).toBe(true);
    expect(p.size).toBe(2);
    expect(p.rotation_deg).toBe(30);
    expect(p.opacity).toBe(0.5);
    expect(p.blend).toBe("multiply");
  });

  it("resets defaults", () => {
    resetDecalPlacement();
    const p = decalPlacementGetSnapshot().placement;
    expect(p.enabled).toBe(false);
    expect(p.size).toBe(1);
    expect(p.blend).toBe("normal");
  });
});
