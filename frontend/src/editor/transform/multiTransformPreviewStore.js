import { useSyncExternalStore } from "react";

const state = {
  active: false,
  delta: null,
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function startTransformPreview() {
  state.active = true;
  state.delta = null;
  emit();
}

export function updateTransformPreview(delta) {
  state.delta = delta;
  emit();
}

export function endTransformPreview() {
  state.active = false;
  state.delta = null;
  emit();
}

export function useTransformPreview() {
  return useSyncExternalStore(
    (l) => {
      listeners.add(l);
      return () => listeners.delete(l);
    },
    () => state,
    () => state
  );
}
