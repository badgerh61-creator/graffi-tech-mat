import { useSyncExternalStore } from "react";

const state = {
  mode: "world", // "world" | "local" | "pivot"
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setTransformSpace(mode) {
  if (!["world", "local", "pivot"].includes(mode)) return;
  state.mode = mode;
  emit();
}

export function useTransformSpace() {
  return useSyncExternalStore(
    (listener) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    () => state,
    () => state
  );
}
