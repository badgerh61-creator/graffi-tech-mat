// frontend/src/editor/materials/presetLibrary.js

export const PRESET_LIBRARY = {
  paint_gloss_red: {
    color: "#D00000",
    metalness: 0.1,
    roughness: 0.2
  },

  paint_gloss_black: {
    color: "#111111",
    metalness: 0.12,
    roughness: 0.18
  },

  paint_matte_black: {
    color: "#141414",
    metalness: 0.0,
    roughness: 0.9
  },

  paint_satin_silver: {
    color: "#A8A8A8",
    metalness: 0.3,
    roughness: 0.45
  },

  paint_metallic_blue: {
    color: "#1F4BA8",
    metalness: 0.75,
    roughness: 0.28
  },

  paint_chrome_like: {
    color: "#D8D8D8",
    metalness: 1.0,
    roughness: 0.12
  }
};

// 🔥 THIS IS THE RESOLVER (STEP 2)
export function resolvePreset(presetId) {
  return PRESET_LIBRARY[presetId] || null;
}
