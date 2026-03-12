// src/api/client.ts
import axios from "axios";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "../utils/auth";

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_BASE,
});

/* ================= REQUEST ================= */
api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/* ================= RESPONSE ================= */

let isRefreshing = false;
let queue: {
  resolve: (token: string) => void;
  reject: (err: any) => void;
}[] = [];

function resolveQueue(error: any, token: string | null) {
  queue.forEach((p) =>
    error ? p.reject(error) : p.resolve(token!)
  );
  queue = [];
}

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;

    if (
      error.response?.status === 401 &&
      !original._retry &&
      original.url !== "/login" &&
      original.url !== "/refresh"
    ) {
      original._retry = true;

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject });
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`;
          return api(original);
        });
      }

      isRefreshing = true;

      try {
        const refreshToken = getRefreshToken();
        if (!refreshToken) throw error;

        const res = await axios.post(
          `${API_BASE}/refresh`,
          { refresh_token: refreshToken }
        );

        setTokens(res.data.access_token, res.data.refresh_token);
        resolveQueue(null, res.data.access_token);

        original.headers.Authorization = `Bearer ${res.data.access_token}`;
        return api(original);
      } catch (err) {
        resolveQueue(err, null);
        clearTokens();
        window.location.href = "/login";
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

