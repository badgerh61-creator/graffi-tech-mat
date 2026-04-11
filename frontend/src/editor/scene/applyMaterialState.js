import * as THREE from "three";

/**
 * Tier 7.42 — Material Authority (FINAL — preset + paint)
 */
export function applyMaterialState(root, materialState) {
  if (!root || !materialState) return;

  let paint = materialState.paint || null;

  // ✅ NEW — preset support
  if (!paint && materialState.preset) {
    const preset = materialState.preset;

    // preset already normalized by backend
    paint = {
      color: preset.color,
      metalness: preset.metalness,
      roughness: preset.roughness,
    };
  }

  if (!paint) return;

  root.traverse((node) => {
    if (!node.isMesh || !node.material) return;

    const oldMaterials = Array.isArray(node.material)
      ? node.material
      : [node.material];

    const newMaterials = oldMaterials.map((mat) => {
      if (!mat) return mat;

      const m = mat.clone();

      // 🔥 IMPORTANT — remove texture so color override works
      if (m.map) {
        m.map.dispose();
        m.map = null;
      }

      // color
      if (paint.color && m.color) {
        try {
          m.color = new THREE.Color(paint.color);
        } catch (e) {
          console.warn("Invalid color:", paint.color);
        }
      }

      // metalness
      if (
        typeof paint.metalness === "number" &&
        m.metalness !== undefined
      ) {
        m.metalness = paint.metalness;
      }

      // roughness
      if (
        typeof paint.roughness === "number" &&
        m.roughness !== undefined
      ) {
        m.roughness = paint.roughness;
      }

      m.needsUpdate = true;

      console.log("🎨 MATERIAL APPLIED:", node.name);

      return m;
    });

    node.material = Array.isArray(node.material)
      ? newMaterials
      : newMaterials[0];

    oldMaterials.forEach((m) => {
      if (!m) return;

      if (m.map) m.map.dispose();
      m.dispose();
    });
  });
}
