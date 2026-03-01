import { useSyncExternalStore } from "react";

const state = { decalId: null };
const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setActiveDecalId(decalId) {
  state.decalId = decalId ? String(decalId) : null;
  emit();
}

export function clearActiveDecalId() {
  state.decalId = null;
  emit();
}

export function activeDecalGetSnapshot() {
  return state;
}

export function activeDecalSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useActiveDecal() {
  return useSyncExternalStore(activeDecalSubscribe, activeDecalGetSnapshot, activeDecalGetSnapshot);
}
