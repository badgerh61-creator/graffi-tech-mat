import * as THREE from "three";
import { applyLOD } from "../../src/editor/scene/applyLOD";

test("applyLOD safe", () => {
  const mesh = new THREE.Mesh(
    new THREE.BoxGeometry(),
    new THREE.MeshStandardMaterial()
  );

  const group = new THREE.Group();
  group.add(mesh);

  const camera = new THREE.PerspectiveCamera();

  applyLOD(group, camera);

  expect(true).toBe(true);
});
