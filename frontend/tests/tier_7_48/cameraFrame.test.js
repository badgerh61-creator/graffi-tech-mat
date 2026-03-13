import { describe, it, expect } from "vitest";
import * as THREE from "three";
import {
  computeCameraDistanceForBounds,
  presetDirection,
} from "../../src/editor/camera/cameraFrame";

describe("cameraFrame", () => {
  it("computes positive distance", () => {
    const d = computeCameraDistanceForBounds({
      radius: 2,
      fovDeg: 50,
      fitOffset: 1.3,
    });
    expect(d).toBeGreaterThan(0);
  });

  it("returns iso preset direction", () => {
    const v = presetDirection("iso");
    expect(v.x).toBeGreaterThan(0);
    expect(v.z).toBeGreaterThan(0);
  });

  it("returns top preset direction", () => {
    const v = presetDirection("top");
    expect(v.equals(new THREE.Vector3(0, 1, 0))).toBe(true);
  });
});
