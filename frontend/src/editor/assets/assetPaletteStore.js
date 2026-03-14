import { useSyncExternalStore } from "react";

const state = {
  activeAssetId: null,
  favorites: [],
  recent: [],
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

function uniqueOrdered(ids) {
  const seen = new Set();
  const out = [];
  for (const id of ids || []) {
    const s = String(id || "").trim();
    if (!s || seen.has(s)) continue;
    seen.add(s);
    out.push(s);
  }
  return out;
}

export function setActiveAssetId(assetId) {
  state.activeAssetId = assetId ? String(assetId) : null;
  emit();
}

export function toggleFavoriteAsset(assetId) {
  const id = String(assetId || "").trim();
  if (!id) return;

  const has = state.favorites.includes(id);
  state.favorites = has
    ? state.favorites.filter((x) => x !== id)
    : uniqueOrdered([...state.favorites, id]);
  emit();
}

export function pushRecentAsset(assetId) {
  const id = String(assetId || "").trim();
  if (!id) return;

  state.recent = uniqueOrdered([id, ...state.recent]).slice(0, 12);
  emit();
}

export function assetPaletteGetSnapshot() {
  return state;
}

export function assetPaletteSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useAssetPalette() {
  return useSyncExternalStore(
    assetPaletteSubscribe,
    assetPaletteGetSnapshot,
    assetPaletteGetSnapshot
  );
}
