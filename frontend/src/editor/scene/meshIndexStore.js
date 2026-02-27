// frontend/src/editor/scene/meshIndexStore.js

import { useSyncExternalStore } from "react";

/**
 * UI-only mesh index:
 * meshPathsByObjectId: { [objectId]: string[] }
 *
 * Populated by ThreeSceneViewer when GLBs load.
 */
const state = {
  meshPathsByObjectId: {},
};

const listeners = new Set();

function emit() {
  for (const l of listeners) l();
}

export function meshIndexGetSnapshot() {
  return state;
}

export function meshIndexSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function setMeshPathsForObject(objectId, meshPaths) {
  const oid = String(objectId || "");
  if (!oid) return;

  const arr = Array.isArray(meshPaths) ? meshPaths.map(String) : [];
  // deterministic: store sorted unique list
  const uniq = Array.from(new Set(arr)).sort((a, b) => a.localeCompare(b));
  state.meshPathsByObjectId = { ...state.meshPathsByObjectId, [oid]: uniq };
  emit();
}

export function clearMeshIndex() {
  state.meshPathsByObjectId = {};
  emit();
}

export function useMeshIndex() {
  return useSyncExternalStore(meshIndexSubscribe, meshIndexGetSnapshot, meshIndexGetSnapshot);
}
