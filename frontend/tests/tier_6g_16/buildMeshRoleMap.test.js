import * as THREE from "three";
import { buildMeshRoleMap } from "../../src/editor/scene/buildMeshRoleMap";

describe("Tier 6G.16 — Mesh Role Mapping", () => {

  test("maps mesh roles correctly", () => {
    const group = new THREE.Group();

    const wheel = new THREE.Mesh();
    wheel.name = "Wheel_FL";

    group.add(wheel);

    const roleMap = buildMeshRoleMap(group, {
      wheel_fl: "Wheel_FL"
    });

    expect(roleMap.wheel_fl).toBe(wheel);
  });

  test("maps multiple roles", () => {
    const group = new THREE.Group();

    const body = new THREE.Mesh();
    body.name = "CarBody";

    const glass = new THREE.Mesh();
    glass.name = "Glass";

    group.add(body);
    group.add(glass);

    const roleMap = buildMeshRoleMap(group, {
      body: "CarBody",
      glass: "Glass"
    });

    expect(roleMap.body).toBe(body);
    expect(roleMap.glass).toBe(glass);
  });

  test("missing role returns undefined", () => {
    const group = new THREE.Group();

    const mesh = new THREE.Mesh();
    mesh.name = "SomethingElse";

    group.add(mesh);

    const roleMap = buildMeshRoleMap(group, {
      body: "CarBody"
    });

    expect(roleMap.body).toBeUndefined();
  });

  test("handles empty inputs", () => {
    const roleMap = buildMeshRoleMap(null, {});
    expect(Object.keys(roleMap).length).toBe(0);
  });

});
