function isObject(x) {
  return x && typeof x === "object" && !Array.isArray(x);
}

function stableKeys(obj) {
  return Object.keys(obj || {}).sort();
}

/**
 * Array diff:
 * - if items have `id`, match by id
 * - else index-based
 */
function diffArray(a = [], b = []) {
  const aArr = Array.isArray(a) ? a : [];
  const bArr = Array.isArray(b) ? b : [];

  const hasId = (x) => x && typeof x === "object" && "id" in x;

  const aId = aArr.every(hasId);
  const bId = bArr.every(hasId);

  if (aId && bId) {
    const aMap = new Map(aArr.map((x) => [String(x.id), x]));
    const bMap = new Map(bArr.map((x) => [String(x.id), x]));

    let added = 0, removed = 0, changed = 0;

    for (const id of bMap.keys()) if (!aMap.has(id)) added++;
    for (const id of aMap.keys()) if (!bMap.has(id)) removed++;

    for (const id of bMap.keys()) {
      if (!aMap.has(id)) continue;
      const da = JSON.stringify(aMap.get(id));
      const db = JSON.stringify(bMap.get(id));
      if (da !== db) changed++;
    }

    return { mode: "id", added, removed, changed, aCount: aArr.length, bCount: bArr.length };
  }

  // index-based
  const max = Math.max(aArr.length, bArr.length);
  let changed = 0;
  for (let i = 0; i < max; i++) {
    const da = JSON.stringify(aArr[i]);
    const db = JSON.stringify(bArr[i]);
    if (da !== db) changed++;
  }
  const added = Math.max(0, bArr.length - aArr.length);
  const removed = Math.max(0, aArr.length - bArr.length);

  return { mode: "index", added, removed, changed, aCount: aArr.length, bCount: bArr.length };
}

/**
 * Shallow object diff counts (keys added/removed/changed).
 */
function diffObject(a = {}, b = {}) {
  const aObj = isObject(a) ? a : {};
  const bObj = isObject(b) ? b : {};

  const aKeys = new Set(stableKeys(aObj));
  const bKeys = new Set(stableKeys(bObj));

  let added = 0, removed = 0, changed = 0;

  for (const k of bKeys) if (!aKeys.has(k)) added++;
  for (const k of aKeys) if (!bKeys.has(k)) removed++;

  for (const k of bKeys) {
    if (!aKeys.has(k)) continue;
    const da = JSON.stringify(aObj[k]);
    const db = JSON.stringify(bObj[k]);
    if (da !== db) changed++;
  }

  return { added, removed, changed, aKeys: aKeys.size, bKeys: bKeys.size };
}

/**
 * High-level diff summary for RenderedSnapshot-ish payloads.
 * Works even if shape differs; always deterministic.
 */
export function summarizeSnapshotDiff(baseSnap, targetSnap) {
  if (!baseSnap || !targetSnap) return null;

  const aBody = baseSnap.body_state || {};
  const bBody = targetSnap.body_state || {};

  const aDecor = baseSnap.decor_state || {};
  const bDecor = targetSnap.decor_state || {};

  const aTuning = baseSnap.tuning_state || {};
  const bTuning = targetSnap.tuning_state || {};

  const panels = diffArray(aBody.panels || [], bBody.panels || []);
  const nodes = diffArray(aBody.nodes || [], bBody.nodes || []);
  const curves = diffArray(aBody.curves || [], bBody.curves || []);
  const surfaces = diffArray(aBody.surfaces || [], bBody.surfaces || []);

  const decor = diffObject(aDecor, bDecor);
  const tuning = diffObject(aTuning, bTuning);

  const statusA = baseSnap.status;
  const statusB = targetSnap.status;

  const meta = {
    statusChanged: String(statusA) !== String(statusB),
    fromStatus: statusA,
    toStatus: statusB,
    parentChanged: String(baseSnap.id) !== String(targetSnap.parent_snapshot_id || ""),
  };

  return {
    base_id: baseSnap.id,
    target_id: targetSnap.id,
    body: { panels, nodes, curves, surfaces },
    decor,
    tuning,
    meta,
  };
}
