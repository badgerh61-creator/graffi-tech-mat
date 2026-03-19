import { describe, it, expect } from "vitest";
import * as THREE from "three";
import { boxToPivotPreset } from "../../src/editor/transform/pivotBounds";

describe("pivotBounds", () => {
  it("computes center pivot", () => {
    const box = new THREE.Box3(
      new THREE.Vector3(-1, 0, -2),
      new THREE.Vector3(3, 4, 2)
    );

    expect(boxToPivotPreset(box, "center")).toEqual({
      x: 1,
      y: 2,
      z: 0,
    });
  });

  it("computes bottom center pivot", () => {
    const box = new THREE.Box3(
      new THREE.Vector3(-1, 0, -2),
      new THREE.Vector3(3, 4, 2)
    );

    expect(boxToPivotPreset(box, "bounds_bottom_center")).toEqual({
      x: 1,
      y: 0,
      z: 0,
    });
  });
});
