import { useSyncExternalStore } from "react";

/**
 * Shared gizmo mode store (UI-only).
 * Keeps TransformControls + UI panel in sync.
 */
const state = { mode: "translate" }; // translate | rotate | scale
const listeners = new Set();

function emit() {
  for (const l of listeners) l();
}

export function gizmoModeGetSnapshot() {
  return state;
}

export function gizmoModeSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function setGizmoMode(mode) {
  const m = String(mode || "").toLowerCase();
  state.mode = m === "rotate" || m === "scale" ? m : "translate";
  emit();
}

export function useGizmoMode() {
  return useSyncExternalStore(gizmoModeSubscribe, gizmoModeGetSnapshot, gizmoModeGetSnapshot);
}
