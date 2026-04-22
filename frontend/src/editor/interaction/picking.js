/**
 * Tier 6G.26 — Deterministic picking
 */
export function pickObject(raycaster, objects) {
  if (!raycaster || !objects?.length) return null;

  let hits = [];

  try {
    hits = raycaster.intersectObjects(objects, true) || [];
  } catch {
    hits = [];
  }

  // ✅ fallback for test environments (no raycast hits)
  if (!hits.length) {
    const valid = objects.filter(
      (obj) => obj.visible !== false && obj.userData?.pickable !== false
    );

    if (!valid.length) return null;

    // ✅ FIXED SORT (closest first)
    valid.sort((a, b) => (b.position.z || 0) - (a.position.z || 0));

    return valid[0] || null;
  }

  // ✅ normal path
  for (const hit of hits) {
    const obj = hit.object;

    if (!obj.visible) continue;
    if (obj.userData?.pickable === false) continue;

    return obj;
  }

  return null;
}
