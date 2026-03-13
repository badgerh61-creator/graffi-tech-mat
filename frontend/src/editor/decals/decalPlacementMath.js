import * as THREE from "three";

function round(n, p = 4) {
  const f = Math.pow(10, p);
  return Math.round((Number(n) || 0) * f) / f;
}

export function vecToObj(v, p = 4) {
  return {
    x: round(v.x, p),
    y: round(v.y, p),
    z: round(v.z, p),
  };
}

export function eulerToDegObj(e, p = 2) {
  const d = 180 / Math.PI;
  return {
    x: round(e.x * d, p),
    y: round(e.y * d, p),
    z: round(e.z * d, p),
  };
}

export function computeDecalPlacementTransform({
  point,
  normal,
  size = 1,
  rotationDeg = 0,
  zOffset = 0.001,
}) {
  const p = point.clone();
  const n = normal.clone().normalize();

  const pos = p.add(n.clone().multiplyScalar(zOffset));

  const quat = new THREE.Quaternion();
  quat.setFromUnitVectors(new THREE.Vector3(0, 0, 1), n);

  const spin = new THREE.Quaternion();
  spin.setFromAxisAngle(n, THREE.MathUtils.degToRad(rotationDeg));

  quat.multiply(spin);

  const euler = new THREE.Euler().setFromQuaternion(quat, "XYZ");

  return {
    position: vecToObj(pos, 4),
    rotation_euler: eulerToDegObj(euler, 2),
    scale: {
      x: round(size, 4),
      y: round(size, 4),
      z: round(size, 4),
    },
  };
}
