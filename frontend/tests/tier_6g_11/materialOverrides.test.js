import * as THREE from "three";
import { applyMaterialOverrides } from "../../src/editor/materials/materialOverrides";

function makeMesh(name = "M") {
  const geom = new THREE.BoxGeometry(1, 1, 1);
  const mat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.5, metalness: 0.5 });
  const mesh = new THREE.Mesh(geom, mat);
  mesh.name = name;
  return mesh;
}

test("applies override to all meshes in object when mesh_path null", () => {
  const group = new THREE.Group();
  group.name = "obj:vehicle-1";
  const a = makeMesh("A");
  const b = makeMesh("B");
  group.add(a);
  group.add(b);

  const objectGroups = new Map([["vehicle-1", group]]);

  applyMaterialOverrides({
    objectGroups,
    overrides: [
      {
        id: "ovr-1",
        enabled: true,
        target: { object_key: "vehicle-1", mesh_path: null },
        material: { opacity: 0.2 },
      },
    ],
  });

  expect(a.material.opacity).toBeCloseTo(0.2);
  expect(b.material.opacity).toBeCloseTo(0.2);
});

test("clamps opacity to [0,1]", () => {
  const group = new THREE.Group();
  group.name = "obj:vehicle-1";
  const a = makeMesh("A");
  group.add(a);

  const objectGroups = new Map([["vehicle-1", group]]);

  applyMaterialOverrides({
    objectGroups,
    overrides: [
      {
        id: "ovr-1",
        enabled: true,
        target: { object_key: "vehicle-1", mesh_path: null },
        material: { opacity: 5 },
      },
    ],
  });

  expect(a.material.opacity).toBe(1);
});
