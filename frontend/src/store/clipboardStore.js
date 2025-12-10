// src/store/clipboardStore.js
import { create } from "zustand";

export const useClipboardStore = create((set) => ({
  clipboard: null,
  copy: (data) => set({ clipboard: data }),
  clear: () => set({ clipboard: null }),
}));
