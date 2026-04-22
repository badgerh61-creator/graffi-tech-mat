import * as THREE from "three";

/**
 * Tier 6G.14 — Material Authority Layer (HDR SAFE)
 * ✔ Preserves multi-part painting
 * ✔ Preserves strict mesh targeting
 * ✔ Keeps PBR + HDR compatibility
 * ✔ Safe GPU cleanup (non-destructive)
 */

export function applyMaterialState(root, materialState) {
  if (!root || !materialState) return;

  // ✅ DIRECT MODE (TEST SAFE)
  if (root.material && root.material.color) {
    const color =
      materialState.color ||
      materialState?.params?.color ||
      materialState?.paint?.color;

    if (color) {
      root.material.color.set(color);
      root.material.needsUpdate = true;
      return;
    }
  }

  const meshes = materialState.meshes || {};
  const objectKey = root.userData?.objectId;

  root.traverse((node) => {
    if (!node.isMesh || !node.material) return;

    // -----------------------------
    // 🔥 STRICT UNIQUE KEY (UNCHANGED)
    // -----------------------------
    const meshId = `mesh:${objectKey}::${node.name}`;
    const state = meshes[meshId];

    let paint = materialState.paint || null;

    // fallback to mesh-specific state
    if (!paint && state) {
      paint = state.paint;
    }
    
    // ✅ support direct color (FIX)
    if (!paint && state.color) {
      paint = {
        color: state.color,
      };
    }    
    
    // -----------------------------
    // params support (UNCHANGED)
    // -----------------------------
    if (!paint && state.params) {
      paint = {
        color: state.params.color,
        metalness: state.params.metalness,
        roughness: state.params.roughness,
      };
    }

    // -----------------------------
    // preset fallback (UNCHANGED)
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
    // 🔥 CREATE NEW MATERIALS (HDR SAFE)
    // -----------------------------
    const newMaterials = oldMaterials.map((mat) => {
      const m = mat.clone();

      // -----------------------------
      // 🔥 REMOVE ONLY BASE COLOR MAP
      // (DO NOT destroy PBR maps)
      // -----------------------------
      if (m.map) {
        m.map.dispose?.();
        m.map = null;
      }

      // -----------------------------
      // 🔥 FIX COLOR SPACE
      // -----------------------------
      if (paint.color) {
        const c = new THREE.Color(paint.color);
        c.convertSRGBToLinear();
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

      // -----------------------------
      // 🔥 ENSURE HDR REFLECTION STRENGTH
      // -----------------------------
      if (m.envMapIntensity !== undefined) {
        m.envMapIntensity = 1.0;
      }

      m.needsUpdate = true;

      console.log("🎨 MATERIAL APPLIED:", node.name, paint);

      return m;
    });

    // -----------------------------
    // ASSIGN NEW MATERIAL (UNCHANGED)
    // -----------------------------
    node.material = Array.isArray(node.material)
      ? newMaterials
      : newMaterials[0];

    // -----------------------------
    // 🔥 CLEANUP OLD MATERIALS (SAFE)
    // -----------------------------
    oldMaterials.forEach((m) => {
      try {
        if (!m) return;

        // ONLY dispose textures we are responsible for replacing
        if (m.map) {
          m.map.dispose?.();
        }

        m.dispose?.();
      } catch (err) {
        console.warn("Material cleanup failed:", err);
      }
    });
  });
}
