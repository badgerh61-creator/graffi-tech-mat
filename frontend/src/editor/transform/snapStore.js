import { useSyncExternalStore } from "react";

const state = {
  snap: {
    enabled: false,
    step: 0.1,         // translate snap units
    step_degrees: 5,   // rotate snap degrees
    step_factor: 0.1,  // scale snap step
  },
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setSnap(partial) {
  state.snap = { ...state.snap, ...(partial || {}) };
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
  return useSyncExternalStore(snapSubscribe, snapGetSnapshot, snapGetSnapshot);
}
