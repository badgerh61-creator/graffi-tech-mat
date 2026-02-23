import { useSyncExternalStore } from "react";

/**
 * Minimal external store (no libs).
 * Deterministic, testable.
 */
const state = {
  selectedId: null,
};

const listeners = new Set();

function emit() {
  for (const l of listeners) l();
}

export function selectionGetSnapshot() {
  return state;
}

export function selectionSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function setSelectedId(id) {
  state.selectedId = id ?? null;
  emit();
}

export function clearSelection() {
  state.selectedId = null;
  emit();
}

export function useSelection() {
  return useSyncExternalStore(selectionSubscribe, selectionGetSnapshot, selectionGetSnapshot);
}
