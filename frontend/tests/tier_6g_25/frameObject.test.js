import * as THREE from "three";
import { frameObject } from "../../src/editor/scene/frameObject";

test("frameObject safe", () => {
  const camera = new THREE.PerspectiveCamera();
  const controls = { target: new THREE.Vector3(), update: () => {} };

  const mesh = new THREE.Mesh(new THREE.BoxGeometry());
  const group = new THREE.Group();
  group.add(mesh);

  frameObject(camera, controls, group);

  expect(camera.position).toBeDefined();
});
