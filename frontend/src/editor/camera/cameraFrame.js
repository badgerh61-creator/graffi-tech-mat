import * as THREE from "three";

function clamp(n, lo, hi) {
  return Math.max(lo, Math.min(hi, n));
}

export function computeCameraDistanceForBounds({
  radius,
  fovDeg = 50,
  fitOffset = 1.3,
}) {
  const safeRadius = Math.max(0.001, Number(radius) || 1);
  const fov = THREE.MathUtils.degToRad(clamp(fovDeg, 1, 179));
  return (safeRadius * fitOffset) / Math.sin(fov / 2);
}

export function frameSphereWithDirection({
  center,
  radius,
  direction,
  fovDeg = 50,
  fitOffset = 1.3,
}) {
  const dist = computeCameraDistanceForBounds({ radius, fovDeg, fitOffset });

  const dir = direction.clone().normalize();
  const position = center.clone().add(dir.multiplyScalar(dist));

  return {
    position,
    target: center.clone(),
  };
}

export function presetDirection(name) {
  switch (String(name || "").toLowerCase()) {
    case "front":
      return new THREE.Vector3(0, 0, 1);
    case "back":
      return new THREE.Vector3(0, 0, -1);
    case "left":
      return new THREE.Vector3(-1, 0, 0);
    case "right":
      return new THREE.Vector3(1, 0, 0);
    case "top":
      return new THREE.Vector3(0, 1, 0);
    case "bottom":
      return new THREE.Vector3(0, -1, 0);
    case "iso":
    default:
      return new THREE.Vector3(1, 0.8, 1);
  }
}

export function boundsToSphere(box) {
  const sphere = new THREE.Sphere();
  box.getBoundingSphere(sphere);
  return sphere;
}
