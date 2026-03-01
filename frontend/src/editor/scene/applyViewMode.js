import * as THREE from "three";

const CLAY_MAT = new THREE.MeshStandardMaterial({ roughness: 1, metalness: 0 });
const SOLID_MAT = new THREE.MeshStandardMaterial({ roughness: 0.8, metalness: 0 });

/**
 * Applies view mode to a scene subtree.
 * Stores originals in mesh.userData.__origMat
 */
export function applyViewMode(root, mode) {
  if (!root) return;

  root.traverse((obj) => {
    if (!obj || !obj.isMesh) return;

    // Save original
    if (!obj.userData.__origMat) obj.userData.__origMat = obj.material;

    if (mode === "studio") {
      // Restore original
      if (obj.userData.__origMat) obj.material = obj.userData.__origMat;
      // clear wireframe flag if it was applied
      if (obj.material && obj.material.wireframe != null) obj.material.wireframe = false;
      return;
    }

    if (mode === "wireframe") {
      // Prefer wireframe on original (keeps color)
      const mat = obj.userData.__origMat || obj.material;
      obj.material = mat;
      if (obj.material && obj.material.wireframe != null) obj.material.wireframe = true;
      return;
    }

    if (mode === "clay") {
      obj.material = CLAY_MAT;
      return;
    }

    if (mode === "solid") {
      obj.material = SOLID_MAT;
      return;
    }
  });
}
