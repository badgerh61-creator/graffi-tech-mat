import * as THREE from "three";
import { cleanupScene } from "../../src/editor/scene/cleanupScene";

describe("cleanupScene (Tier 6G.22)", () => {

  test("removes all children and disposes safely", () => {
    const root = new THREE.Group();

    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(),
      new THREE.MeshStandardMaterial()
    );

    root.add(mesh);

    cleanupScene(root);

    expect(root.children.length).toBe(0);
  });

  test("does not crash on multiple calls", () => {
    const root = new THREE.Group();

    cleanupScene(root);
    cleanupScene(root);
    cleanupScene(root);

    expect(true).toBe(true);
  });

});
