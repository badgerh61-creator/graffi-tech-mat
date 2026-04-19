import * as THREE from "three";

/**
 * Tier 6G.17 — Selection Outline System
 *
 * Applies emissive highlight to selected object
 * and restores original materials safely.
 */

/**
 * Apply highlight to group
 */
export function applySelectionOutline(group) {
  if (!group) return;

  group.traverse((node) => {
    if (!node.isMesh || !node.material) return;

    const materials = Array.isArray(node.material)
      ? node.material
      : [node.material];

    // store original material
    node.userData.__originalMaterial = materials;

    // clone + highlight
    const highlighted = materials.map((mat) => {
      const m = mat.clone();

      // add emissive highlight if supported
      if ("emissive" in m) {
        m.emissive = new THREE.Color("#00ffff");
        m.emissiveIntensity = 0.6;
      }

      m.needsUpdate = true;
      return m;
    });

    node.material = Array.isArray(node.material)
      ? highlighted
      : highlighted[0];
  });
}

/**
 * Clear highlight and restore original materials
 */
export function clearSelectionOutline(group) {
  if (!group) return;

  group.traverse((node) => {
    if (!node.isMesh) return;

    const original = node.userData.__originalMaterial;
    if (!original) return;

    node.material = original;

    delete node.userData.__originalMaterial;
  });
}
