import { useSyncExternalStore } from "react";

const DEFAULTS = {
  enabled: false,
  asset_id: null,
  asset_ref: null,
  size: 1,
  rotation_deg: 0,
  opacity: 1,
  blend: "normal",
  z_offset: 0.001,
};

const state = {
  placement: { ...DEFAULTS },
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

function clamp01(v) {
  const n = Number(v);
  if (!Number.isFinite(n)) return 1;
  return Math.max(0, Math.min(1, n));
}

function positive(v, fallback) {
  const n = Number(v);
  if (!Number.isFinite(n) || n <= 0) return fallback;
  return n;
}

export function setDecalPlacement(partial) {
  const next = { ...state.placement, ...(partial || {}) };
  next.enabled = !!next.enabled;
  next.size = positive(next.size, 1);
  next.rotation_deg = Number.isFinite(Number(next.rotation_deg)) ? Number(next.rotation_deg) : 0;
  next.opacity = clamp01(next.opacity);
  next.blend = ["normal", "multiply", "add"].includes(String(next.blend)) ? String(next.blend) : "normal";
  next.z_offset = positive(next.z_offset, 0.001);

  state.placement = next;
  emit();
}

export function resetDecalPlacement() {
  state.placement = { ...DEFAULTS };
  emit();
}

export function decalPlacementGetSnapshot() {
  return state;
}

export function decalPlacementSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useDecalPlacement() {
  return useSyncExternalStore(
    decalPlacementSubscribe,
    decalPlacementGetSnapshot,
    decalPlacementGetSnapshot
  );
}
