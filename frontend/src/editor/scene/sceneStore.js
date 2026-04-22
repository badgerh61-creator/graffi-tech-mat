import { useSyncExternalStore } from "react";

const state = {
  sceneIndex: null,
  snapshotId: null,
};

const listeners = new Set();

function emit() {
  listeners.forEach((l) => l());
}

export function setSceneIndex(sceneIndex, snapshotId) {
  state.sceneIndex = sceneIndex;
  state.snapshotId = snapshotId;
  emit();
}

export function getSceneSnapshot() {
  return state;
}

export function subscribeScene(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useScene() {
  return useSyncExternalStore(
    subscribeScene,
    getSceneSnapshot,
    getSceneSnapshot
  );
}
