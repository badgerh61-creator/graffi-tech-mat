import { useSyncExternalStore } from "react";

const state = { mode: "studio" }; // studio|solid|clay|wireframe
const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setViewMode(mode) {
  const m = String(mode);
  state.mode = ["studio", "solid", "clay", "wireframe"].includes(m) ? m : "studio";
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
  return useSyncExternalStore(viewModeSubscribe, viewModeGetSnapshot, viewModeGetSnapshot);
}
