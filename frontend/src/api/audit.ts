import { api } from "./client";

export const auditApi = {
  list: (params?: {
    page?: number;
    limit?: number;
  }) =>
    api.get("/admin/audit", {
      params,
    }),
};

