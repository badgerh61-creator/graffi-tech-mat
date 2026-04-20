import * as THREE from "three";

/**
 * Tier 6G.23 — basic LOD
 */
export function applyLOD(group, camera) {
  if (!group || !camera) return;

  const camPos = camera.position;

  group.traverse((node) => {
    if (!node.isMesh || !node.material) return;

    const worldPos = new THREE.Vector3();
    node.getWorldPosition(worldPos);

    const dist = worldPos.distanceTo(camPos);

    // far = cheaper shading
    if (dist > 20) {
      node.material.flatShading = true;
    } else {
      node.material.flatShading = false;
    }

    node.material.needsUpdate = true;
  });
}
