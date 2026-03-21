import { useSyncExternalStore } from "react";

const VALID_MODES = ["studio", "solid", "clay", "wireframe"];

const state = {
  mode: "studio",        // shading mode
  showBounds: false,     // overlay
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setViewMode(mode) {
  const m = String(mode || "").toLowerCase();
  state.mode = VALID_MODES.includes(m) ? m : "studio";
  emit();
}

export function toggleBounds() {
  state.showBounds = !state.showBounds;
  emit();
}

export function setBoundsEnabled(v) {
  state.showBounds = !!v;
  emit();
}

export function viewModeGetSnapshot() {
  return state;
}

export function viewModeSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useViewMode() {
  return useSyncExternalStore(
    viewModeSubscribe,
    viewModeGetSnapshot,
    viewModeGetSnapshot
  );
}
