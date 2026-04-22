import * as THREE from "three";
import { pickObject } from "../../src/editor/interaction/picking";

test("returns closest visible pickable object", () => {
  const raycaster = new THREE.Raycaster();

  const a = new THREE.Mesh(new THREE.BoxGeometry(), new THREE.MeshBasicMaterial());
  const b = new THREE.Mesh(new THREE.BoxGeometry(), new THREE.MeshBasicMaterial());

  a.position.z = -1;
  b.position.z = -5;

  a.userData.pickable = true;
  b.userData.pickable = true;

  const scene = new THREE.Scene();
  scene.add(a);
  scene.add(b);

  raycaster.set(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -1));

  const picked = pickObject(raycaster, [a, b]);

  expect(picked).toBe(a);
});

test("ignores non-pickable objects", () => {
  const raycaster = new THREE.Raycaster();

  const mesh = new THREE.Mesh(
    new THREE.BoxGeometry(),
    new THREE.MeshBasicMaterial()
  );

  mesh.userData.pickable = false;

  const picked = pickObject(raycaster, [mesh]);

  expect(picked).toBe(null);
});

test("ignores invisible objects", () => {
  const raycaster = new THREE.Raycaster();

  const mesh = new THREE.Mesh(
    new THREE.BoxGeometry(),
    new THREE.MeshBasicMaterial()
  );

  mesh.visible = false;
  mesh.userData.pickable = true;

  const picked = pickObject(raycaster, [mesh]);

  expect(picked).toBe(null);
});
