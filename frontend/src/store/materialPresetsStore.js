// src/store/materialPresetsStore.js
import { create } from "zustand";
import { nanoid } from "nanoid";
import createMaterialThumbnail from "../utils/createMaterialThumbnail";

export const useMaterialPresetsStore = create((set, get) => ({
  presets: [],

  async addPreset(preset) {
    const id = nanoid();

    // generate material thumbnail if missing
    let thumb = preset.thumbnail || null;
    if (!thumb) {
      try {
        thumb = await createMaterialThumbnail(preset.material);
      } catch (e) {
        thumb = null;
      }
    }

    const item = {
      id,
      name: preset.name,
      category: preset.category || "custom",
      material: preset.material,
      thumbnail: thumb,
      createdAt: Date.now(),
    };

    set((s) => ({ presets: [item, ...s.presets] }));
    return id;
  },

  deletePreset(id) {
    set((s) => ({
      presets: s.presets.filter((p) => p.id !== id),
    }));
  },

  getPreset(id) {
    return get().presets.find((p) => p.id === id) || null;
  }
}));
