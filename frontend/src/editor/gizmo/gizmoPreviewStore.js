import { useSyncExternalStore } from "react";

const state = { preview: null };
const listeners = new Set();

function emit() {
  for (const l of listeners) l();
}

export function previewGetSnapshot() {
  return state;
}

export function previewSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function setGizmoPreview(preview) {
  state.preview = preview || null;
  emit();
}

export function clearGizmoPreview() {
  state.preview = null;
  emit();
}

export function useGizmoPreview() {
  return useSyncExternalStore(previewSubscribe, previewGetSnapshot, previewGetSnapshot);
}
