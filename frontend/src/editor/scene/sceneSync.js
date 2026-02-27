export function getObjectIdFromSelectedId(selectedId) {
  if (!selectedId) return null;
  const s = String(selectedId);
  const idx = s.indexOf("::");
  if (idx === -1) return null;
  return s.slice(0, idx);
}

export function sceneIndexObjectIds(sceneIndex) {
  const objs = sceneIndex?.objects || [];
  const out = [];
  for (const o of objs) {
    if (o && o.id != null) out.push(String(o.id));
  }
  return out;
}

export function isSelectionValidForSceneIndex(selectedId, sceneIndex) {
  if (!selectedId) return true; // nothing selected is always valid
  const oid = getObjectIdFromSelectedId(selectedId);
  if (!oid) return false;
  const ids = sceneIndexObjectIds(sceneIndex);
  return ids.includes(oid);
}

/**
 * Deterministic rebind key: changes whenever snapshot changes.
 * Can optionally include a stable hash later if you add it to the scene index.
 */
export function makeSceneRebindKey(snapshotId) {
  if (snapshotId == null) return "snap:none";
  return `snap:${snapshotId}`;
}
