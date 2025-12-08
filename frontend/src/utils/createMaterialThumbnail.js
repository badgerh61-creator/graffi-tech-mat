// src/utils/createMaterialThumbnail.js
import * as THREE from "three";

/**
 * Render a 256x256 material preview cube and return data URL.
 */
export default async function createMaterialThumbnail(mat = {}, size = 256) {
  return new Promise((resolve) => {
    const canvas = document.createElement("canvas");
    canvas.width = size;
    canvas.height = size;

    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true
    });

    renderer.setSize(size, size);
    renderer.setClearColor(0x000000, 0);

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
    camera.position.set(1.5, 0.8, 2.0);
    camera.lookAt(0, 0, 0);

    // lights
    scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 0.8));
    const dir = new THREE.DirectionalLight(0xffffff, 0.8);
    dir.position.set(3, 3, 2);
    scene.add(dir);

    // box
    const geo = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({
      color: mat.color || "#9da7b1",
      roughness: mat.roughness ?? 0.5,
      metalness: mat.metalness ?? 0,
      clearcoat: mat.clearcoat ?? 0,
      clearcoatRoughness: mat.clearcoatRoughness ?? 0,
    });

    const mesh = new THREE.Mesh(geo, material);
    mesh.rotation.set(0.4, 0.6, 0.1);
    scene.add(mesh);

    // render
    renderer.render(scene, camera);

    // output
    try {
      resolve(canvas.toDataURL("image/webp", 0.9));
    } catch (e) {
      resolve(null);
    }

    renderer.dispose?.();
  });
}
