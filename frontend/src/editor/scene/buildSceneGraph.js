/**
 * Tier 6G.19 — build hierarchy
 */
export function buildSceneGraph(objects = []) {
  const map = new Map();
  const roots = [];

  // map id → group
  for (const obj of objects) {
    if (obj.__group) {
      map.set(obj.id, obj.__group);
    }
  }

  // attach children
  for (const obj of objects) {
    const group = map.get(obj.id);
    const parent = map.get(obj.parent_id);

    if (parent) {
      parent.add(group);
    } else {
      roots.push(group);
    }
  }

  return roots;
}
