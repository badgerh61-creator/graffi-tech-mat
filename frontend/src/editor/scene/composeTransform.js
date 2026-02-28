/**
 * Compose transforms (base ∘ localInstance) in a deterministic way.
 * Inputs: {position:{x,y,z}, rotation:{x,y,z}, scale:{x,y,z}}
 * Output: same shape
 *
 * Minimal Tier 6G.12:
 * - position: add
 * - rotation: add (Euler)
 * - scale: multiply
 *
 * (This is fine until you need full quaternion composition.)
 */
export function composeTransform(base, local) {
  const b = base || {};
  const l = local || {};

  const bp = b.position || {};
  const br = b.rotation || {};
  const bs = b.scale || {};

  const lp = l.position || {};
  const lr = l.rotation || {};
  const ls = l.scale || {};

  return {
    position: {
      x: (bp.x || 0) + (lp.x || 0),
      y: (bp.y || 0) + (lp.y || 0),
      z: (bp.z || 0) + (lp.z || 0),
    },
    rotation: {
      x: (br.x || 0) + (lr.x || 0),
      y: (br.y || 0) + (lr.y || 0),
      z: (br.z || 0) + (lr.z || 0),
    },
    scale: {
      x: (bs.x ?? 1) * (ls.x ?? 1),
      y: (bs.y ?? 1) * (ls.y ?? 1),
      z: (bs.z ?? 1) * (ls.z ?? 1),
    },
  };
}
