import axios from "axios";

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

// 🚫 NO interceptors, NO auth, NO refresh
const activityClient = axios.create({
  baseURL: API_BASE,
});

export const activityApi = {
  list: (params?: { page?: number; limit?: number }) =>
    activityClient.get("/activity", {
      params: {
        page: params?.page ?? 1,
        limit: params?.limit ?? 50,
      },
    }),
};

