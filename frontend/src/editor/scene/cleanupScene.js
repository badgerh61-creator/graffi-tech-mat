import * as THREE from "three";

/**
 * Tier 6G.22 — FULL GPU cleanup (safe + complete)
 */
export function cleanupScene(root) {
  if (!root) return;

  root.traverse((node) => {
    // -------------------
    // Geometry
    // -------------------
    if (node.geometry) {
      node.geometry.dispose();
    }

    // -------------------
    // Materials + ALL textures
    // -------------------
    if (node.material) {
      const materials = Array.isArray(node.material)
        ? node.material
        : [node.material];

      materials.forEach((mat) => {
        if (!mat) return;

        // 🔥 Dispose ALL texture slots (not just .map)
        Object.keys(mat).forEach((key) => {
          const value = mat[key];

          if (value && value.isTexture) {
            value.dispose();
          }
        });

        // Dispose material itself
        mat.dispose();
      });
    }
  });

  // -------------------
  // Remove all children safely
  // -------------------
  while (root.children.length > 0) {
    const child = root.children[0];

    // optional extra safety: clear references
    root.remove(child);
  }
}
