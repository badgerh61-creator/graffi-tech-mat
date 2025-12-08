// src/store/uiStore.js
import { create } from "zustand";

export const useUIStore = create((set) => ({
  hdr: {
    type: "preset",
    preset: "studio",
    id: "studio",
    rotation: 0,
    intensity: 1.2,
  },

  setHDRI: (hdr) =>
    set((s) => ({ hdr: { ...s.hdr, ...hdr } })),

  setHDRRotation: (rotation) =>
    set((s) => ({ hdr: { ...s.hdr, rotation } })),

  setHDRIntensity: (intensity) =>
    set((s) => ({ hdr: { ...s.hdr, intensity } })),
}));
