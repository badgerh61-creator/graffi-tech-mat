import { describe, it, expect, vi } from "vitest";
import * as THREE from "three";
import { cleanupScene } from "@/editor/scene/cleanupScene";

describe("Tier 6G.20 — cleanupScene", () => {
  
  it("removes all children from root", () => {
    const root = new THREE.Group();

    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(),
      new THREE.MeshStandardMaterial()
    );

    root.add(mesh);

    cleanupScene(root);

    expect(root.children.length).toBe(0);
  });

  it("disposes geometry and material", () => {
    const root = new THREE.Group();

    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshStandardMaterial();

    const geoDispose = vi.spyOn(geometry, "dispose");
    const matDispose = vi.spyOn(material, "dispose");

    const mesh = new THREE.Mesh(geometry, material);
    root.add(mesh);

    cleanupScene(root);

    expect(geoDispose).toHaveBeenCalled();
    expect(matDispose).toHaveBeenCalled();
  });

  it("disposes material arrays correctly", () => {
    const root = new THREE.Group();

    const geometry = new THREE.BoxGeometry();
    const mat1 = new THREE.MeshStandardMaterial();
    const mat2 = new THREE.MeshStandardMaterial();

    const spy1 = vi.spyOn(mat1, "dispose");
    const spy2 = vi.spyOn(mat2, "dispose");

    const mesh = new THREE.Mesh(geometry, [mat1, mat2]);
    root.add(mesh);

    cleanupScene(root);

    expect(spy1).toHaveBeenCalled();
    expect(spy2).toHaveBeenCalled();
  });

  it("disposes textures inside materials", () => {
    const root = new THREE.Group();

    const texture = new THREE.Texture();
    const texDispose = vi.spyOn(texture, "dispose");

    const material = new THREE.MeshStandardMaterial({
      map: texture,
    });

    const mesh = new THREE.Mesh(new THREE.BoxGeometry(), material);
    root.add(mesh);

    cleanupScene(root);

    expect(texDispose).toHaveBeenCalled();
  });

  it("safe on empty scene", () => {
    const root = new THREE.Group();

    expect(() => cleanupScene(root)).not.toThrow();
    expect(root.children.length).toBe(0);
  });

  it("safe on repeated cleanup calls", () => {
    const root = new THREE.Group();

    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(),
      new THREE.MeshStandardMaterial()
    );

    root.add(mesh);

    cleanupScene(root);
    cleanupScene(root);

    expect(root.children.length).toBe(0);
  });

});
