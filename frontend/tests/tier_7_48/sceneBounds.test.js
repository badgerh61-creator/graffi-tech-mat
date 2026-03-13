import { describe, it, expect } from "vitest";
import * as THREE from "three";
import {
  computeVisibleSceneBounds,
} from "../../src/editor/scene/sceneBounds";

describe("sceneBounds", () => {
  it("computes visible bounds for meshes", () => {
    const root = new THREE.Group();

    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(1, 1, 1),
      new THREE.MeshBasicMaterial()
    );
    root.add(mesh);

    const box = computeVisibleSceneBounds(root);
    expect(box.isEmpty()).toBe(false);
  });
});
