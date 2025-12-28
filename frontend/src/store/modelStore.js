// src/store/modelStores.js

import { create } from "zustand";
import { api } from "../api/client";
import { resolveStudioPermissions } from "../permissions/studioPermissions";

/* ================= INTERNAL TIMER ================= */
let refreshTimer = null;

export const useModelStore = create((set, get) => ({
  /* ================= STATE ================= */

  models: [],
  currentModelId: null,
  currentModelUrl: null,
  urlExpiresAt: null,

  // 🔒 Phase F3 — frontend authority only
  modelPermissions: resolveStudioPermissions(null),

  // 🟡 Phase 4.4
  modelStatus: "idle", // idle | loading | ready | failed

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
      if (refreshTimer) {
        clearTimeout(refreshTimer);
        refreshTimer = null;
      }

      set({ modelStatus: "loading" });

      const res = await api.get(`/models/${id}/url`);
      const { url, expires_in = 300 } = res.data;

      if (!url) {
        set({ modelStatus: "failed" });
        return;
      }

      const expiresAt = Date.now() + expires_in * 1000;
      localStorage.setItem("last_model_id", String(id));

      // ✅ PHASE-F3 FIX:
      // Backend does NOT return role yet.
      // If model opens, assume editor-level UI access.
      set({
        currentModelId: id,
        currentModelUrl: url,
        urlExpiresAt: expiresAt,
        modelPermissions: resolveStudioPermissions("editor"),
        modelStatus: "ready",
      });

      refreshTimer = setTimeout(() => {
        get().refreshModelUrl();
      }, Math.max(expires_in * 1000 - 30_000, 10_000));
    } catch (err) {
      console.error("Failed to open model", err);
      set({ modelStatus: "failed" });
    }
  },

  /* ================= REFRESH ================= */

  refreshModelUrl: async () => {
    const { currentModelId } = get();
    if (!currentModelId) return;

    try {
      const res = await api.get(`/models/${currentModelId}/url`);
      const { url, expires_in = 300 } = res.data;

      if (!url) {
        set({ modelStatus: "failed" });
        return;
      }

      set({
        currentModelUrl: url,
        urlExpiresAt: Date.now() + expires_in * 1000,
        modelStatus: "ready",
      });

      refreshTimer = setTimeout(() => {
        get().refreshModelUrl();
      }, Math.max(expires_in * 1000 - 30_000, 10_000));
    } catch (err) {
      console.warn("Failed to refresh model URL", err);
      set({ modelStatus: "failed" });
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
      modelPermissions: resolveStudioPermissions(null),
      modelStatus: "idle",
    });
  },
}));

