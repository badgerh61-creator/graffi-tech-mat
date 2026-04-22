import * as THREE from "three";

/**
 * Tier 6G.25 — frame object in view
 */
export function frameObject(camera, controls, object) {
  if (!object) return;

  const box = new THREE.Box3().setFromObject(object);
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());

  const maxDim = Math.max(size.x, size.y, size.z);
  const distance = maxDim * 2;

  camera.position.copy(center.clone().add(new THREE.Vector3(0, 0, distance)));

  controls.target.copy(center);
  controls.update();
}
