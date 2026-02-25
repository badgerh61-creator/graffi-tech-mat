import * as THREE from "three";

test("bounding box from object is not empty", () => {
  const boxMesh = new THREE.Mesh(
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.MeshBasicMaterial()
  );

  const group = new THREE.Group();
  group.add(boxMesh);

  const b = new THREE.Box3().setFromObject(group);
  expect(b.isEmpty()).toBe(false);
});
