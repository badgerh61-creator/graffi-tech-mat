import { create } from "zustand";

export const useActivePaint = create((set) => ({
  active: null,

  setActivePaint: (paint) => set({ active: paint }),
  clearActivePaint: () => set({ active: null }),
}));
