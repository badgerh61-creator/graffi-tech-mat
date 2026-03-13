import { useSyncExternalStore } from "react";

const AXES = new Set(["none", "x", "y", "z"]);
const ORIENTATIONS = new Set(["local", "world"]);

function clampPositive(n, fallback) {
  const x = Number(n);
  if (!Number.isFinite(x) || x <= 0) return fallback;
  return x;
}

const DEFAULT_SNAP = {
  enabled: false,
  step: 0.1,
  step_degrees: 5,
  step_factor: 0.1,
  axis_lock: "none",
  orientation: "local",
};

const state = {
  snap: { ...DEFAULT_SNAP },
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setSnap(partial) {
  const next = { ...state.snap, ...(partial || {}) };

  next.enabled = !!next.enabled;
  next.step = clampPositive(next.step, 0.1);
  next.step_degrees = clampPositive(next.step_degrees, 5);
  next.step_factor = clampPositive(next.step_factor, 0.1);
  next.axis_lock = AXES.has(String(next.axis_lock))
    ? String(next.axis_lock)
    : "none";
  next.orientation = ORIENTATIONS.has(String(next.orientation))
    ? String(next.orientation)
    : "local";

  state.snap = next;
  emit();
}

export function resetSnap() {
  state.snap = { ...DEFAULT_SNAP };
  emit();
}

export function snapGetSnapshot() {
  return state;
}

export function snapSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useSnap() {
  return useSyncExternalStore(
    snapSubscribe,
    snapGetSnapshot,
    snapGetSnapshot
  );
}
