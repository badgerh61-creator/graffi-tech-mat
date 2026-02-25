import * as THREE from "three";
import { applyTransformToObject3D } from "../../src/editor/scene/applyTransform";

test("applies position rotation scale with safe defaults", () => {
  const g = new THREE.Group();

  applyTransformToObject3D(g, {
    position: { x: 1, y: 2, z: 3 },
    rotation: { x: 0.1, y: 0.2, z: 0.3 },
    scale: { x: 2, y: 2, z: 2 },
  });

  expect(g.position.x).toBe(1);
  expect(g.position.y).toBe(2);
  expect(g.position.z).toBe(3);

  expect(g.rotation.x).toBeCloseTo(0.1);
  expect(g.rotation.y).toBeCloseTo(0.2);
  expect(g.rotation.z).toBeCloseTo(0.3);

  expect(g.scale.x).toBe(2);
  expect(g.scale.y).toBe(2);
  expect(g.scale.z).toBe(2);
});

test("defaults when transform missing", () => {
  const g = new THREE.Group();
  applyTransformToObject3D(g, null);

  expect(g.position.x).toBe(0);
  expect(g.scale.x).toBe(1);
});
