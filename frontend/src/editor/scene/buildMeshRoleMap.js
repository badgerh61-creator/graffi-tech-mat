/**
 * Tier 6G.16 — build role map
 */
export function buildMeshRoleMap(group, meshRoles = {}) {
  if (!group) return {};

  const roleMap = {};

  group.traverse((node) => {
    if (!node.isMesh) return;

    const name = node.name || "";

    for (const [role, target] of Object.entries(meshRoles)) {
      if (name === target) {
        roleMap[role] = node;
      }
    }
  });

  return roleMap;
}
