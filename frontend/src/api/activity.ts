import { api } from "./client";

export const activityApi = {
  list: (params?: {
    page?: number;
    limit?: number;
  }) =>
    api.get("/activity/", {
      params: {
        page: params?.page ?? 1,
        limit: params?.limit ?? 50,
      },
    }),
};

