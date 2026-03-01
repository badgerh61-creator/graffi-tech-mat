import { useSyncExternalStore } from "react";

const state = { patchById: {} };
const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setDecalPreviewPatch(decalId, patch) {
  if (!decalId) return;
  state.patchById = { ...state.patchById, [String(decalId)]: patch || null };
  emit();
}

export function clearDecalPreviewPatch(decalId) {
  if (!decalId) return;
  const next = { ...state.patchById };
  delete next[String(decalId)];
  state.patchById = next;
  emit();
}

export function clearAllDecalPreview() {
  state.patchById = {};
  emit();
}

export function decalPreviewGetSnapshot() {
  return state;
}

export function decalPreviewSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useDecalPreview() {
  return useSyncExternalStore(decalPreviewSubscribe, decalPreviewGetSnapshot, decalPreviewGetSnapshot);
}
