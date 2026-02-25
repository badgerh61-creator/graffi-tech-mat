import { useSyncExternalStore } from "react";

/**
 * UI-only scene layers state (deterministic defaults).
 */
const state = {
  kinds: {}, // kind -> { visible, pickable, opacity }
};

const listeners = new Set();
function emit() {
  for (const l of listeners) l();
}

export function layersGetSnapshot() {
  return state;
}

export function layersSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function ensureKind(kind) {
  const k = String(kind || "unknown");
  if (!state.kinds[k]) {
    const lower = k.toLowerCase();
    const isHelper =
      lower.includes("helper") || lower.includes("grid") || lower.includes("axis");

    state.kinds[k] = {
      visible: true,
      pickable: !isHelper,
      opacity: 1.0,
    };
  }
  return state.kinds[k];
}

export function setKindVisible(kind, visible) {
  ensureKind(kind).visible = !!visible;
  emit();
}

export function setKindPickable(kind, pickable) {
  ensureKind(kind).pickable = !!pickable;
  emit();
}

export function setKindOpacity(kind, opacity) {
  const v = Number(opacity);
  ensureKind(kind).opacity = Number.isFinite(v) ? Math.min(1, Math.max(0, v)) : 1.0;
  emit();
}

export function useSceneLayers() {
  return useSyncExternalStore(layersSubscribe, layersGetSnapshot, layersGetSnapshot);
}
