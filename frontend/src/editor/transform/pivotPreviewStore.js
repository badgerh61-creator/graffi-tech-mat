import { create } from "zustand";

const store = create((set) => ({
  preview: null,
  setPivotPreview: (preview) => set({ preview }),
  clearPivotPreview: () => set({ preview: null }),
}));

// hook
export const usePivotPreview = store;

// ✅ REQUIRED FOR TESTS
export const setPivotPreview = (preview) =>
  store.setState({ preview });

export const clearPivotPreview = () =>
  store.setState({ preview: null });

export const pivotPreviewGetSnapshot = () =>
  store.getState();
