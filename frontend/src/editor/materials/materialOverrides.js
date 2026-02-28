import * as THREE from "three";
import { findNodeByMeshPath } from "../scene/selectionResolve";

function clamp01(v) {
  const n = Number(v);
  if (!Number.isFinite(n)) return null;
  return Math.min(1, Math.max(0, n));
}

function parseHexColor(hex) {
  if (!hex) return null;
  const s = String(hex).trim();
  if (!s.startsWith("#")) return null;
  if (!(s.length === 7)) return null;
  return s;
}

function ensureClonedMaterial(mesh) {
  if (!mesh || !mesh.isMesh) return null;

  const mat = mesh.material;
  if (Array.isArray(mat)) {
    const cloned = mat.map((m) => (m ? m.clone() : m));
    mesh.material = cloned;
    return cloned;
  }

  if (mat && typeof mat.clone === "function") {
    const cloned = mat.clone();
    mesh.material = cloned;
    return cloned;
  }

  return null;
}

function applyToMaterial(mat, spec) {
  if (!mat || !spec) return;

  const color = parseHexColor(spec.color);
  if (color && mat.color) mat.color = new THREE.Color(color);

  const emissive = parseHexColor(spec.emissive);
  if (emissive && mat.emissive) mat.emissive = new THREE.Color(emissive);

  const opacity = clamp01(spec.opacity);
  if (opacity != null) {
    mat.transparent = opacity < 1;
    mat.opacity = opacity;
  }

  const metalness = clamp01(spec.metalness);
  if (metalness != null && "metalness" in mat) mat.metalness = metalness;

  const roughness = clamp01(spec.roughness);
  if (roughness != null && "roughness" in mat) mat.roughness = roughness;

  mat.needsUpdate = true;
}

function applyOverrideToMesh(mesh, materialSpec) {
  const cloned = ensureClonedMaterial(mesh);
  if (!cloned) return;

  if (Array.isArray(mesh.material)) {
    mesh.material.forEach((m) => applyToMaterial(m, materialSpec));
  } else {
    applyToMaterial(mesh.material, materialSpec);
  }
}

/**
 * Apply overrides to a loaded Three.js scene.
 *
 * @param {Map<string, THREE.Group>} objectGroups - map of objectKey -> group (obj:<objectKey>)
 * @param {Array} overrides - snapshot.body_state.material_overrides
 */
export function applyMaterialOverrides({ objectGroups, overrides }) {
  const list = Array.isArray(overrides) ? overrides.slice() : [];
  list
    .filter((o) => o && o.enabled !== false && o.id)
    .sort((a, b) => String(a.id).localeCompare(String(b.id)));

  for (const o of list) {
    const target = o.target || {};
    const objectKey = String(target.object_key || "").trim();
    if (!objectKey) continue;

    const group = objectGroups.get(objectKey);
    if (!group) continue;

    const meshPath = target.mesh_path ? String(target.mesh_path) : null;
    const spec = o.material || {};

    if (!meshPath) {
      // apply to all meshes under group
      group.traverse((node) => {
        if (node && node.isMesh) applyOverrideToMesh(node, spec);
      });
    } else {
      const node = findNodeByMeshPath(group, meshPath);
      if (!node) continue;

      if (node.isMesh) {
        applyOverrideToMesh(node, spec);
      } else {
        // if it's a group, apply to meshes under it
        node.traverse((n) => {
          if (n && n.isMesh) applyOverrideToMesh(n, spec);
        });
      }
    }
  }
}
