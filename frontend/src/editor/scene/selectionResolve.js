// frontend/src/editor/scene/selectionResolve.js

/**
 * Parse selectedId into { objectId, meshPath|null }.
 * Accepts "{objectId}::" or "{objectId}::{meshPath}".
 */
export function parseSelectedId(selectedId) {
  if (!selectedId) return { objectId: null, meshPath: null };

  const s = String(selectedId);
  const idx = s.indexOf("::");
  if (idx === -1) return { objectId: null, meshPath: null };

  const objectId = s.slice(0, idx) || null;
  const rest = s.slice(idx + 2);
  const meshPath = rest ? rest : null;

  return { objectId, meshPath };
}

/**
 * Resolve a node by mesh_path within an object group.
 * mesh_path format: "A/B/C" where node names or "unnamed-x" are used.
 * Deterministic assuming mesh_path was built by buildMeshPath().
 */
export function findNodeByMeshPath(objectGroup, meshPath) {
  if (!objectGroup || !meshPath) return null;

  const parts = String(meshPath).split("/").filter(Boolean);
  if (!parts.length) return null;

  let current = objectGroup;

  for (const part of parts) {
    if (!current?.children?.length) return null;

    // direct name match first
    let next =
      current.children.find((c) => String(c.name || "") === part) || null;

    // fallback: unnamed-x
    if (!next && part.startsWith("unnamed-")) {
      const n = Number(part.replace("unnamed-", ""));
      if (Number.isFinite(n) && n >= 0 && n < current.children.length) {
        next = current.children[n];
      }
    }

    if (!next) return null;
    current = next;
  }

  return current;
}
