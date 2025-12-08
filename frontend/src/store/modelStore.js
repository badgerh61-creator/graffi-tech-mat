// src/store/modelStore.js
import { create } from "zustand";
import { nanoid } from "nanoid";

export const useModelStore = create((set, get) => ({
  models: [],               // [{ id, name, url, size }]
  currentModelId: null,

  addModelFromAsset(asset) {
    // Only accept actual 3D model file types
    const valid = ["glb", "gltf", "fbx", "obj", "usdz"];
    if (!valid.includes(asset.meta.ext)) return;

    const id = asset.id || nanoid();

    const model = {
      id,
      name: asset.name,
      url: asset.url,
      size: asset.size
    };

    set((s) => ({
      models: [...s.models.filter((m) => m.id !== id), model],
      currentModelId: id
    }));
  },

  setCurrentModel(id) {
    const exists = get().models.find((m) => m.id === id);
    if (exists) set({ currentModelId: id });
  },

  removeModel(id) {
    set((s) => {
      const filtered = s.models.filter((m) => m.id !== id);
      return {
        models: filtered,
        currentModelId:
          s.currentModelId === id ? (filtered[0]?.id || null) : s.currentModelId
      };
    });
  },

  getCurrentModel() {
    return get().models.find((m) => m.id === get().currentModelId) || null;
  },

  clear() {
    set({ models: [], currentModelId: null });
  }
}));
