import * as THREE from "three";

/**
 * Safe number conversion
 */
function n(v, fallback) {
  return typeof v === "number" && !Number.isNaN(v) ? v : fallback;
}

/**
 * Existing system (FIXED)
 */
export function applyTransformToObject3D(obj3d, transform) {
  if (!obj3d) return;

  // 🔥 STRICT GUARD (6G.27 compliance)
  if (!transform) {
    console.warn("Missing transform — skipping object");
    return;
  }

  const p = transform.position || {};
  const r = transform.rotation || {};
  const s = transform.scale || {};

  obj3d.position.set(
    n(p.x, 0),
    n(p.y, 0),
    n(p.z, 0)
  );

  obj3d.rotation.set(
    n(r.x, 0),
    n(r.y, 0),
    n(r.z, 0)
  );

  obj3d.scale.set(
    n(s.x, 1),
    n(s.y, 1),
    n(s.z, 1)
  );

  obj3d.updateMatrixWorld(true);
}

/**
 * 🔥 6G.18 compatibility layer
 */
export function applyTransform(obj3d, transform) {
  applyTransformToObject3D(obj3d, transform);
}

/**
 * Placeholder (unchanged)
 */
export function makePlaceholderMesh(label = "object") {
  const geom = new THREE.BoxGeometry(0.6, 0.3, 1.2);
  const mat = new THREE.MeshStandardMaterial({
    metalness: 0.0,
    roughness: 0.9
  });

  const mesh = new THREE.Mesh(geom, mat);
  mesh.name = `placeholder:${label}`;
  return mesh;
}
