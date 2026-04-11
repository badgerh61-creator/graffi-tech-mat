/**
 * Tier 7.76 — Snapshot Mutation (Material)
 * This is the ONLY place where snapshot is modified
 */
export function updateObjectMaterial(snapshot, objectId, materialState) {
  if (!snapshot) return snapshot;

  const nodes = snapshot.nodes || [];

  const nextNodes = nodes.map((node) => {
    if (node.id !== objectId) return node;

    return {
      ...node,
      material_state: {
        ...(node.material_state || {}),
        ...materialState,
      },
    };
  });

  return {
    ...snapshot,
    nodes: nextNodes,
  };
}
