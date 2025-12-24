import { api } from "./client";

/* ---------- ADMIN ---------- */
export const adminApi = {
  listUsers: () => api.get("/admin/users"),

  setUserRole: (userId: number, role: string) =>
    api.post(`/admin/users/${userId}/role`, { role }),

  setUserActive: (userId: number, is_active: boolean) =>
    api.post(`/admin/users/${userId}/active`, { is_active }),

  revokeSessions: (userId: number) =>
    api.post(`/admin/users/${userId}/revoke-sessions`),
};

