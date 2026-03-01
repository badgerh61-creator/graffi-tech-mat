/**
 * hits: array of raw pick ids from raycast, like:
 * - "decal:<id>"
 * - "mesh:<objectId>::<mesh_path>"
 * - "obj:<objectId>"
 */
function parsePickId(id) {
  const s = String(id || "");
  if (s.startsWith("decal:")) return { kind: "decal", key: s.slice(6), raw: s };
  if (s.startsWith("mesh:")) return { kind: "mesh", key: s.slice(5), raw: s };
  if (s.startsWith("obj:")) return { kind: "obj", key: s.slice(4), raw: s };
  return { kind: "unknown", key: s, raw: s };
}

function stableSort(parsed) {
  // Deterministic: sort by kind priority then key lexicographically
  return [...parsed].sort((a, b) => {
    if (a.kind !== b.kind) return a.kind.localeCompare(b.kind);
    return a.key.localeCompare(b.key);
  });
}

const PRIORITY_ALL = ["decal", "mesh", "obj"];
const PRIORITY_DECALS = ["decal"];
const PRIORITY_MESHES = ["mesh"];
const PRIORITY_OBJECTS = ["obj"];

function priorityForFilter(filter) {
  if (filter === "decals") return PRIORITY_DECALS;
  if (filter === "meshes") return PRIORITY_MESHES;
  if (filter === "objects") return PRIORITY_OBJECTS;
  return PRIORITY_ALL;
}

export function resolvePick(hits, filter = "all") {
  const parsed = (hits || []).map(parsePickId).filter((p) => p.kind !== "unknown");
  if (!parsed.length) return null;

  // group by kind, pick smallest key for determinism
  const sorted = stableSort(parsed);

  const pr = priorityForFilter(filter);
  for (const kind of pr) {
    const first = sorted.find((x) => x.kind === kind);
    if (first) return first; // {kind, key, raw}
  }
  return null;
}
