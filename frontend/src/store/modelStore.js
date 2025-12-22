import { create } from "zustand";
import { api } from "../api/client";

/* ================= INTERNAL TIMER ================= */
let refreshTimer = null;

export const useModelStore = create((set, get) => ({
  /* ================= STATE ================= */

  models: [],
  currentModelId: null,
  currentModelUrl: null,
  urlExpiresAt: null,

  /* ================= MODELS ================= */

  fetchModels: async () => {
    try {
      const res = await api.get("/models/");
      set({ models: res.data });
    } catch (err) {
      console.error("Failed to fetch models", err);
    }
  },

  /* ================= OPEN MODEL ================= */

  openModel: async (id) => {
    try {
      // clear previous timer
      if (refreshTimer) {
        clearTimeout(refreshTimer);
        refreshTimer = null;
      }

      const res = await api.get(`/models/${id}/url`);
      const { url, expires_in = 300 } = res.data;

      const expiresAt = Date.now() + expires_in * 1000;

      localStorage.setItem("last_model_id", String(id));

      set({
        currentModelId: id,
        currentModelUrl: url,
        urlExpiresAt: expiresAt,
      });

      // refresh 30s before expiry
      refreshTimer = setTimeout(() => {
        get().refreshModelUrl();
      }, Math.max(expires_in * 1000 - 30_000, 10_000));
    } catch (err) {
      console.error("Failed to open model", err);
    }
  },

  /* ================= REFRESH ================= */

  refreshModelUrl: async () => {
    const { currentModelId } = get();
    if (!currentModelId) return;

    try {
      const res = await api.get(`/models/${currentModelId}/url`);
      const { url, expires_in = 300 } = res.data;

      set({
        currentModelUrl: url,
        urlExpiresAt: Date.now() + expires_in * 1000,
      });

      refreshTimer = setTimeout(() => {
        get().refreshModelUrl();
      }, Math.max(expires_in * 1000 - 30_000, 10_000));
    } catch (err) {
      console.warn("Failed to refresh model URL", err);
    }
  },

  /* ================= RESTORE ================= */

  restoreLastModel: async () => {
    const id = localStorage.getItem("last_model_id");
    if (id) {
      await get().openModel(Number(id));
    }
  },

  /* ================= CLEAR ================= */

  clearModel: () => {
    if (refreshTimer) {
      clearTimeout(refreshTimer);
      refreshTimer = null;
    }

    localStorage.removeItem("last_model_id");

    set({
      currentModelId: null,
      currentModelUrl: null,
      urlExpiresAt: null,
    });
  },
}));

