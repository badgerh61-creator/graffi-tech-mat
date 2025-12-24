/**
 * Studio permission resolver
 * Mirrors backend RBAC semantics exactly
 *
 * role: "admin" | "owner" | "editor" | "viewer" | null
 */

export function resolveStudioPermissions(role) {
  return {
    canView: !!role,
    canEdit: role === "admin" || role === "owner" || role === "editor",
    canUpload: role === "admin" || role === "owner" || role === "editor",
    canDelete: role === "admin" || role === "owner",
    isReadOnly: role === "viewer",
  };
}

