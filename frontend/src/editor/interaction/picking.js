/**
 * Tier 6G.26 — Deterministic picking
 */
export function pickObject(raycaster, objects) {
  if (!raycaster || !objects?.length) return null;

  const hits = raycaster.intersectObjects(objects, true);

  if (!hits.length) return null;

  for (const hit of hits) {
    const obj = hit.object;

    // skip invisible
    if (!obj.visible) continue;

    // skip non-pickable
    if (obj.userData?.pickable === false) continue;

    return obj;
  }

  return null;
}
