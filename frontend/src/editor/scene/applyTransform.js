import * as THREE from "three";

export function applyTransformToObject3D(obj3d, transform) {
  const t = transform || {};

  const p = t.position || {};
  const r = t.rotation || {};
  const s = t.scale || {};

  obj3d.position.set(p.x || 0, p.y || 0, p.z || 0);
  obj3d.rotation.set(r.x || 0, r.y || 0, r.z || 0);
  obj3d.scale.set(s.x || 1, s.y || 1, s.z || 1);

  obj3d.updateMatrixWorld(true);
}

export function makePlaceholderMesh(label = "object") {
  const geom = new THREE.BoxGeometry(0.6, 0.3, 1.2);
  const mat = new THREE.MeshStandardMaterial({ metalness: 0.0, roughness: 0.9 });
  const mesh = new THREE.Mesh(geom, mat);
  mesh.name = `placeholder:${label}`;
  return mesh;
}
