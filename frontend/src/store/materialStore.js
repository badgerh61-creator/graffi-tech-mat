// src/store/materialStore.js
import { create } from "zustand"

export const useMaterialStore = create((set, get) => ({
  material: {
    color: "#9da7b1",
    roughness: 0.5,
    metalness: 0,
    clearcoat: 0,
    clearcoatRoughness: 0,
    envIntensity: 1.0,
  },

  textures: {
    albedo: null,
    normal: null,
    roughness: null,
    metalness: null
  },

  setMaterial: (patch) => set((s) => ({ material: { ...s.material, ...patch } })),
  setTexture: (k, v) => set((s) => ({ textures: { ...s.textures, [k]: v } })),
  reset: () => set({
    material: {
      color: "#9da7b1",
      roughness: 0.5,
      metalness: 0,
      clearcoat: 0,
      clearcoatRoughness: 0,
      envIntensity: 1.0,
    },
    textures: { albedo: null, normal: null, roughness: null, metalness: null }
  })
}));
