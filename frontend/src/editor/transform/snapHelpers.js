import * as THREE from "three";

function roundToGrid(v, size) {
  return Math.round(v / size) * size;
}

export function applyGridSnap(position, gridSize) {
  return new THREE.Vector3(
    roundToGrid(position.x, gridSize),
    roundToGrid(position.y, gridSize),
    roundToGrid(position.z, gridSize)
  );
}

export function applySurfaceSnap(object, scene) {
  const raycaster = new THREE.Raycaster();
  const down = new THREE.Vector3(0, -1, 0);

  raycaster.set(object.position, down);

  const intersects = raycaster.intersectObjects(scene.children, true);

  if (!intersects.length) return object.position;

  const hit = intersects[0];
  return new THREE.Vector3(
    object.position.x,
    hit.point.y,
    object.position.z
  );
}

export function applyObjectSnap(object, objects, threshold = 0.5) {
  let closest = null;
  let minDist = Infinity;

  objects.forEach((other) => {
    if (other === object) return;

    const d = object.position.distanceTo(other.position);
    if (d < threshold && d < minDist) {
      minDist = d;
      closest = other;
    }
  });

  if (!closest) return object.position;

  return closest.position.clone();
}
