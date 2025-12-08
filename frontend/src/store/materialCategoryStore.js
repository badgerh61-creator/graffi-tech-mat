// src/store/materialCategoryStore.js
import { create } from "zustand";

/**
 * Pure serializable store — UI maps iconKey => real icon.
 */
export const useMaterialCategoryStore = create((set, get) => ({
  selectedCategory: "all",

  categories: [
    { id: "all", name: "All", iconKey: "star" },
    { id: "metals", name: "Metals", iconKey: "cube" },
    { id: "plastics", name: "Plastics", iconKey: "leaf" },
    { id: "paints", name: "Paints", iconKey: "palette" },
    { id: "glass", name: "Glass", iconKey: "glass" },
    { id: "custom", name: "Custom", iconKey: "custom" },
  ],

  setSelectedCategory: (id) => set({ selectedCategory: id }),

  getCategory: (id) => {
    const s = get();
    return s.categories.find((c) => c.id === id) || null;
  },
}));
