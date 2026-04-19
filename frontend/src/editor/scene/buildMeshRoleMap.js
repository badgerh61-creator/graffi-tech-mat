/**
 * Tier 6G.16 — build role map (FIXED HYBRID)
 */
export function buildMeshRoleMap(group, meshRoles = {}) {
  if (!group) return {};

  const roleMap = {
    body: [],
    wheels: [],
    glass: [],
    lights: [],
    doors: [],
    trim: [],
    interior: [],
    chassis: [],
    engine: [],
    _auto: []
  };

  const hasBackendRoles = meshRoles && Object.keys(meshRoles).length > 0;

  group.traverse((node) => {
    if (!node.isMesh) return;

    const name = (node.name || "").toLowerCase();

    // -----------------------------
    // 1. BACKEND-DRIVEN (if exists)
    // -----------------------------
    if (hasBackendRoles) {
      for (const [role, targets] of Object.entries(meshRoles)) {
        const list = Array.isArray(targets) ? targets : [targets];

        if (list.includes(node.name)) {
          roleMap[role]?.push(node);
          return;
        }
      }
    }

    // -----------------------------
    // 2. AUTO-DETECTION (fallback)
    // -----------------------------
    if (name.includes("wheel")) {
      roleMap.wheels.push(node);
    } else if (name.includes("glass") || name.includes("window")) {
      roleMap.glass.push(node);
    } else if (name.includes("light")) {
      roleMap.lights.push(node);
    } else if (name.includes("door")) {
      roleMap.doors.push(node);
    } else if (name.includes("interior")) {
      roleMap.interior.push(node);
    } else {
      roleMap.body.push(node);
    }

    roleMap._auto.push(node);
  });

  console.log("🔥 FINAL ROLE MAP:", roleMap);

  return roleMap;
}
