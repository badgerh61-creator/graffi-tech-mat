// src/store/modelTransformStore.js
import { create } from "zustand";

export const useModelTransformStore = create((set) => ({
  position: { x: 0, y: 0.6, z: 0 },
  rotation: { x: 0, y: 0, z: 0 },
  scale: 1,

  setPosition: (axis, value) =>
    set((s) => ({
      position: { ...s.position, [axis]: Number(value) }
    })),

  setRotation: (axis, value) =>
    set((s) => ({
      rotation: { ...s.rotation, [axis]: Number(value) }
    })),

  setScale: (v) => set({ scale: Number(v) }),

  reset: () =>
    set({
      position: { x: 0, y: 0.6, z: 0 },
      rotation: { x: 0, y: 0, z: 0 },
      scale: 1
    })
}));
