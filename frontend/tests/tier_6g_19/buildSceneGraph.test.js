import * as THREE from "three";
import { buildSceneGraph } from "../../src/editor/scene/buildSceneGraph";

test("child attaches to parent", () => {
  const parent = { id: "p" };
  const child = { id: "c", parent_id: "p" };

  parent.__group = new THREE.Group();
  child.__group = new THREE.Group();

  const roots = buildSceneGraph([parent, child]);

  expect(parent.__group.children.includes(child.__group)).toBe(true);
});

test("objects without parent become roots", () => {
  const obj = { id: "a" };
  obj.__group = new THREE.Group();

  const roots = buildSceneGraph([obj]);

  expect(roots.length).toBe(1);
});
