import * as THREE from "three";
import {
  applySelectionOutline,
  clearSelectionOutline
} from "../../src/editor/scene/applySelectionOutline";

test("highlight apply + clear", () => {

  const mesh = new THREE.Mesh(
    new THREE.BoxGeometry(),
    new THREE.MeshStandardMaterial()
  );

  const group = new THREE.Group();
  group.add(mesh);

  applySelectionOutline(group);

  expect(mesh.material.emissiveIntensity).toBeGreaterThan(0);

  clearSelectionOutline(group);

  expect(mesh.userData.__originalMaterial).toBeUndefined();
});
