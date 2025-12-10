// src/store/studioTabsStore.js
import { create } from "zustand";

export const useStudioTabsStore = create((set) => ({
  tabs: ["default"],
  active: "default",

  addTab: (id) =>
    set((s) => {
      if (s.tabs.includes(id)) return s; // prevent duplicates
      return { tabs: [...s.tabs, id], active: id };
    }),

  setActive: (id) => set({ active: id }),

  removeTab: (id) =>
    set((s) => {
      const filtered = s.tabs.filter((t) => t !== id);
      return {
        tabs: filtered,
        active: s.active === id ? filtered[0] || null : s.active,
      };
    }),
}));
