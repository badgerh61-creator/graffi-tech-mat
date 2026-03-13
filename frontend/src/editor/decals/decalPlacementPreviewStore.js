import { useSyncExternalStore } from "react";

const state = {
  preview: null,
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setDecalPlacementPreview(preview) {
  state.preview = preview || null;
  emit();
}

export function clearDecalPlacementPreview() {
  state.preview = null;
  emit();
}

export function decalPlacementPreviewGetSnapshot() {
  return state;
}

export function decalPlacementPreviewSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useDecalPlacementPreview() {
  return useSyncExternalStore(
    decalPlacementPreviewSubscribe,
    decalPlacementPreviewGetSnapshot,
    decalPlacementPreviewGetSnapshot
  );
}
