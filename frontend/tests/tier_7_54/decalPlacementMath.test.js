import { describe, it, expect } from "vitest";
import * as THREE from "three";
import { computeDecalPlacementTransform } from "../../src/editor/decals/decalPlacementMath";

describe("computeDecalPlacementTransform", () => {
  it("builds deterministic placement transform", () => {
    const r = computeDecalPlacementTransform({
      point: new THREE.Vector3(1, 2, 3),
      normal: new THREE.Vector3(0, 0, 1),
      size: 2,
      rotationDeg: 45,
      zOffset: 0.01,
    });

    expect(r.position.x).toBe(1);
    expect(r.position.y).toBe(2);
    expect(r.position.z).toBe(3.01);
    expect(r.scale.x).toBe(2);
    expect(r.scale.y).toBe(2);
  });
});
