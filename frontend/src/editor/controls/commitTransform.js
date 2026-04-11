/**
 * Tier 7.76 — Commit transform to snapshot
 */
export function extractTransform(group) {
  return {
    position: {
      x: group.position.x,
      y: group.position.y,
      z: group.position.z,
    },
    rotation: {
      x: group.rotation.x,
      y: group.rotation.y,
      z: group.rotation.z,
    },
    scale: {
      x: group.scale.x,
      y: group.scale.y,
      z: group.scale.z,
    },
  };
}
