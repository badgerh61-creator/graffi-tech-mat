import * as THREE from "three";
import { applyMaterialState } from "../../src/editor/scene/applyMaterialState";

test("applies color override", () => {
  const mesh = new THREE.Mesh(
    new THREE.BoxGeometry(),
    new THREE.MeshStandardMaterial({ color: 0xffffff })
  );

  const group = new THREE.Group();
  group.add(mesh);

  applyMaterialState(group, {
    paint: { color: "#ff0000" }
  });

  expect(mesh.material.color.getHexString()).toBe("ff0000");
});
