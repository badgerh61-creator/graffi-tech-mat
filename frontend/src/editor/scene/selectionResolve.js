// frontend/src/editor/scene/selectionResolve.js

/**
 * Selection ID formats (canonical, forward-compatible):
 *
 * Non-instance:
 *   "{objectId}::"
 *   "{objectId}::{meshPath}"
 *
 * Instance (6G.12):
 *   "{objectId}@{instanceId}::"
 *   "{objectId}@{instanceId}::{meshPath}"
 *
 * Where meshPath is "A/B/C" using buildMeshPath() rules.
 */

/**
 * 6G.9-compatible parser (minimal):
 * Returns only { objectId, meshPath }.
 *
 * NOTE:
 * - For instance keys, objectId returns the FULL objectKey (e.g. "wheel@inst-02")
 *   because 6G.9 doesn’t need instance splitting.
 */
export function parseSelectedIdLite(selectedId) {
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
 * 6G.12 parser (full):
 * Returns:
 *  - objectKey: "wheel@inst-02" or "vehicle-1"
 *  - objectId: "wheel" or "vehicle-1"
 *  - instanceId: "inst-02" or null
 *  - meshPath: "A/B/C" or null
 *
 * This becomes the canonical parseSelectedId export for 6G.12+.
 */
export function parseSelectedId(selectedId) {
  if (!selectedId) {
    return { objectKey: null, objectId: null, instanceId: null, meshPath: null };
  }

  const s = String(selectedId);
  const idx = s.indexOf("::");
  if (idx === -1) {
    return { objectKey: null, objectId: null, instanceId: null, meshPath: null };
  }

  const objectKey = s.slice(0, idx) || null;
  const rest = s.slice(idx + 2);
  const meshPath = rest ? rest : null;

  if (!objectKey) {
    return { objectKey: null, objectId: null, instanceId: null, meshPath };
  }

  const at = objectKey.indexOf("@");
  if (at === -1) {
    return {
      objectKey,
      objectId: objectKey,
      instanceId: null,
      meshPath,
    };
  }

  const objectId = objectKey.slice(0, at) || null;
  const instanceId = objectKey.slice(at + 1) || null;

  return {
    objectKey,
    objectId,
    instanceId,
    meshPath,
  };
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
