// src/store/searchStore.js
import { create } from "zustand";

export const useSearchStore = create((set) => ({
  query: "",
  setQuery: (q) => set({ query: q }),
  clear: () => set({ query: "" }),
}));
