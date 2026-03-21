import { describe, it, expect } from "vitest";
import * as THREE from "three";
import { applyGridSnap } from "../../src/editor/transform/snapHelpers";

describe("snapHelpers", () => {
  it("snaps to grid", () => {
    const v = new THREE.Vector3(1.2, 2.7, 3.1);
    const r = applyGridSnap(v, 1);
    expect(r.x).toBe(1);
    expect(r.y).toBe(3);
    expect(r.z).toBe(3);
  });
});
