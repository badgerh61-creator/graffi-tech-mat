import * as THREE from "three";
import { applyTransform } from "../../src/editor/scene/applyTransform";

test("applies position correctly", () => {
  const group = new THREE.Group();

  applyTransform(group, {
    position: { x: 1, y: 2, z: 3 }
  });

  expect(group.position.x).toBe(1);
  expect(group.position.y).toBe(2);
  expect(group.position.z).toBe(3);
});

test("does not accumulate transforms", () => {
  const group = new THREE.Group();

  applyTransform(group, { position: { x: 1 } });
  applyTransform(group, { position: { x: 1 } });

  expect(group.position.x).toBe(1);
});
