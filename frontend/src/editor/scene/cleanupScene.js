import * as THREE from "three";

/**
 * Tier 6G.20 — full scene reset
 */
export function cleanupScene(root) {
  if (!root) return;

  root.traverse((node) => {
    // geometry
    if (node.geometry) {
      node.geometry.dispose();
    }

    // materials
    if (node.material) {
      const mats = Array.isArray(node.material)
        ? node.material
        : [node.material];

      mats.forEach((m) => {
        if (m.map) m.map.dispose();
        m.dispose();
      });
    }
  });

  // remove children
  while (root.children.length > 0) {
    root.remove(root.children[0]);
  }
}
