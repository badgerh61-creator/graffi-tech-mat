import * as THREE from "three";

/**
 * Tier 6G.14 — Material Authority Layer (FINAL FIXED)
 * - Supports multi-part painting
 * - Uses exact mesh targeting (no cross-bleed)
 * - No normalization collisions
 * - Safe material replacement + cleanup
 * - FIXED: correct color space (SRGB → Linear)
 */

export function applyMaterialState(root, materialState) {
  if (!root || !materialState) return;

  const meshes = materialState.meshes || {};
  const objectKey = root.userData?.objectId;

  root.traverse((node) => {
    if (!node.isMesh || !node.material) return;

    // -----------------------------
    // 🔥 STRICT UNIQUE KEY
    // -----------------------------
    const meshId = `mesh:${objectKey}::${node.name}`;
    const state = meshes[meshId];

    if (!state) return;

    let paint = state.paint;

    // -----------------------------
    // params support
    // -----------------------------
    if (!paint && state.params) {
      paint = {
        color: state.params.color,
        metalness: state.params.metalness,
        roughness: state.params.roughness,
      };
    }

    // -----------------------------
    // preset object fallback
    // -----------------------------
    if (!paint && state.preset && typeof state.preset === "object") {
      paint = {
        color: state.preset.color,
        metalness: state.preset.metalness,
        roughness: state.preset.roughness,
      };
    }

    if (!paint) return;

    const oldMaterials = Array.isArray(node.material)
      ? node.material
      : [node.material];

    // -----------------------------
    // 🔥 CREATE NEW MATERIALS
    // -----------------------------
    const newMaterials = oldMaterials.map((mat) => {
      let m = mat.clone();

      // -----------------------------
      // 🔥 REMOVE TEXTURE INFLUENCE
      // -----------------------------
      if (m.map) {
        m.map.dispose?.();
        m.map = null;
      }

      // -----------------------------
      // 🔥 FIX COLOR SPACE (CRITICAL)
      // -----------------------------
      if (paint.color) {
        const c = new THREE.Color(paint.color);
        c.convertSRGBToLinear(); // ✅ THIS FIXES GREY COLORS
        m.color.copy(c);
      }

      // -----------------------------
      // APPLY MATERIAL PROPERTIES
      // -----------------------------
      if (paint.metalness !== undefined) {
        m.metalness = paint.metalness;
      }

      if (paint.roughness !== undefined) {
        m.roughness = paint.roughness;
      }

      m.needsUpdate = true;

      console.log("🎨 MATERIAL APPLIED:", node.name, paint);

      return m;
    });

    // -----------------------------
    // ASSIGN NEW MATERIAL
    // -----------------------------
    node.material = Array.isArray(node.material)
      ? newMaterials
      : newMaterials[0];

    // -----------------------------
    // 🔥 CLEANUP OLD MATERIALS
    // -----------------------------
    oldMaterials.forEach((m) => {
      try {
        if (!m) return;

        if (m.map) m.map.dispose?.();
        m.dispose?.();
      } catch {}
    });
  });
}
