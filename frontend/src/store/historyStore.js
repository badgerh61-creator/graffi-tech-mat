// src/store/historyStore.js
import { create } from "zustand";

export const useHistoryStore = create((set, get) => ({
  past: [],
  present: null,
  future: [],

  init: (state) => set({ past: [], present: state, future: [] }),

  undo: () => {
    const { past, present, future } = get();
    if (past.length === 0) return;
    const prev = past[past.length - 1];
    set({ past: past.slice(0, -1), present: prev, future: [present, ...future] });
  },

  redo: () => {
    const { past, present, future } = get();
    if (future.length === 0) return;
    const next = future[0];
    set({ past: [...past, present], present: next, future: future.slice(1) });
  },

  push: (state) => set((s) => ({ past: [...s.past, s.present].slice(-50), present: state, future: [] })),

  clear: () => set({ past: [], present: null, future: [] }),
}));
