import { useSyncExternalStore } from "react";

const state = { filter: "all" }; // all|objects|meshes|decals
const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setSelectionFilter(filter) {
  const f = String(filter);
  state.filter = ["all", "objects", "meshes", "decals"].includes(f) ? f : "all";
  emit();
}

export function selectionFilterGetSnapshot() {
  return state;
}

export function selectionFilterSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useSelectionFilter() {
  return useSyncExternalStore(selectionFilterSubscribe, selectionFilterGetSnapshot, selectionFilterGetSnapshot);
}
