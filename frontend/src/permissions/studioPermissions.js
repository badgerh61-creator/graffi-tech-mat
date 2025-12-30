/**
 * Studio permission resolver
 * Phase F3 — SAFE frontend RBAC
 *
 * role: "owner" | "editor" | "viewer" | null
 * admin is handled via user.is_admin (global)
 */

export function resolveStudioPermissions(role, user = null) {
  const isAdmin = user?.is_admin === true;

  // 🔒 SAFE DEFAULT — no role = no privileges
  if (!role && !isAdmin) {
    return {
      canView: false,
      canEdit: false,
      canUpload: false,
      canDelete: false,
      isReadOnly: true,
    };
  }

  // 👑 Global admin
  if (isAdmin) {
    return {
      canView: true,
      canEdit: true,
      canUpload: true,
      canDelete: true,
      isReadOnly: false,
    };
  }

  // 🧑 Owner
  if (role === "owner") {
    return {
      canView: true,
      canEdit: true,
      canUpload: true,
      canDelete: true,
      isReadOnly: false,
    };
  }

  // 🧑‍🎨 Editor
  if (role === "editor") {
    return {
      canView: true,
      canEdit: true,
      canUpload: true,
      canDelete: false,
      isReadOnly: false,
    };
  }

  // 👀 Viewer (explicit + default)
  return {
    canView: true,
    canEdit: false,
    canUpload: false,
    canDelete: false,
    isReadOnly: true,
  };
}

