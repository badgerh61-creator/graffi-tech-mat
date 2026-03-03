// frontend/src/editor/materials/applyMaterialOverridesToScene.js
import * as THREE from "three";

/**
 * applyMaterialOverridesToScene({ root, objectGroups, meshToObjectKey, allMeshes, overrides })
 *
 * ADDITIVE-SAFE:
 * - If overrides is null/empty => no-op.
 * - If an override references unknown mesh/object => skip.
 * - Never throws intentionally; caller wraps in try/catch too.
 *
 * Expected override shapes (tolerant):
 * 1) overrides[objectKey][meshPath] = { color, roughness, metalness, opacity }
 * 2) overrides.materialsByMeshId["mesh:objectKey::meshPath"] = { ... }
 * 3) overrides[meshId] = { ... }  (meshId string)
 *
 * Notes:
 * - We only patch common MeshStandardMaterial properties when present.
 * - We do NOT mutate geometry.
 */
export function applyMaterialOverridesToScene({
  root,
  objectGroups,
  meshToObjectKey,
  allMeshes,
  overrides,
}) {
  if (!overrides) return;

  // helpers
  const isObj = (x) => x && typeof x === "object" && !Array.isArray(x);

  const clamp01 = (n) => {
    const v = Number(n);
    if (!Number.isFinite(v)) return null;
    return Math.max(0, Math.min(1, v));
  };

  const applyPatchToMaterial = (mat, patch) => {
    if (!mat || !patch || !isObj(patch)) return;

    // color
    if (patch.color != null) {
      try {
        // Accept "#rrggbb", "rgb()", number, THREE.Color-ish
        const c = new THREE.Color(patch.color);
        if ("color" in mat && mat.color) mat.color.copy(c);
      } catch {}
    }

    // roughness/metalness
    if (patch.roughness != null && "roughness" in mat) {
      const v = Number(patch.roughness);
      if (Number.isFinite(v)) mat.roughness = Math.max(0, Math.min(1, v));
    }
    if (patch.metalness != null && "metalness" in mat) {
      const v = Number(patch.metalness);
      if (Number.isFinite(v)) mat.metalness = Math.max(0, Math.min(1, v));
    }

    // opacity
    if (patch.opacity != null) {
      const o = clamp01(patch.opacity);
      if (o != null && "opacity" in mat) {
        mat.opacity = o;
        mat.transparent = o < 1;
      }
    }

    mat.needsUpdate = true;
  };

  const applyPatchToMesh = (mesh, patch) => {
    if (!mesh || !mesh.isMesh) return;
    const mat = mesh.material;
    if (Array.isArray(mat)) mat.forEach((m) => applyPatchToMaterial(m, patch));
    else applyPatchToMaterial(mat, patch);
  };

  // ---- Shape (2): materialsByMeshId
  const byMeshId = overrides.materialsByMeshId;
  if (isObj(byMeshId)) {
    for (const [meshId, patch] of Object.entries(byMeshId)) {
      // meshId is "mesh:objectKey::meshPath" in your viewer
      // We’ll find it by scanning allMeshes for matching userData.pickId.
      for (const m of allMeshes || []) {
        if (!m || !m.isMesh) continue;
        const pid = m.userData?.pickId;
        if (pid && String(pid) === String(meshId)) {
          applyPatchToMesh(m, patch);
        }
      }
    }
    return; // if this shape exists, treat it as authoritative
  }

  // ---- Shape (3): overrides keyed directly by meshId
  // e.g. overrides["mesh:obj::path"] = { ... }
  // If overrides has many keys, we do a quick pass.
  const keys = Object.keys(overrides || {});
  const looksLikeMeshId = (k) => typeof k === "string" && k.startsWith("mesh:");
  const hasDirectMeshIds = keys.some(looksLikeMeshId);

  if (hasDirectMeshIds) {
    const map = overrides;
    for (const k of keys) {
      if (!looksLikeMeshId(k)) continue;
      const patch = map[k];
      for (const m of allMeshes || []) {
        if (!m || !m.isMesh) continue;
        const pid = m.userData?.pickId;
        if (pid && String(pid) === String(k)) applyPatchToMesh(m, patch);
      }
    }
    return;
  }

  // ---- Shape (1): overrides[objectKey][meshPath]
  // We find meshPath by parsing userData.pickId = "mesh:objectKey::meshPath"
  // and looking up overrides[objectKey][meshPath].
  for (const m of allMeshes || []) {
    if (!m || !m.isMesh) continue;

    const pid = m.userData?.pickId;
    if (!pid || typeof pid !== "string") continue;
    if (!pid.startsWith("mesh:")) continue;

    // pid = "mesh:objectKey::meshPath"
    const rest = pid.slice("mesh:".length);
    const parts = rest.split("::");
    const objectKey = parts[0];
    const meshPath = parts.slice(1).join("::"); // if "::" appears inside path, keep it

    const o = overrides?.[objectKey];
    if (!isObj(o)) continue;

    const patch = o?.[meshPath];
    if (!patch) continue;

    applyPatchToMesh(m, patch);
  }
}
