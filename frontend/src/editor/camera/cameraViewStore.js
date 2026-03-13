import { useSyncExternalStore } from "react";

const DEFAULT_CAMERA = {
  position: { x: 6, y: 5, z: 6 },
  target: { x: 0, y: 0, z: 0 },
  preset: "iso",
};

const state = {
  view: { ...DEFAULT_CAMERA },
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setCameraView(partial) {
  state.view = {
    ...state.view,
    ...(partial || {}),
    position: { ...state.view.position, ...(partial?.position || {}) },
    target: { ...state.view.target, ...(partial?.target || {}) },
  };
  emit();
}

export function resetCameraView() {
  state.view = { ...DEFAULT_CAMERA };
  emit();
}

export function cameraViewGetSnapshot() {
  return state;
}

export function cameraViewSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useCameraView() {
  return useSyncExternalStore(
    cameraViewSubscribe,
    cameraViewGetSnapshot,
    cameraViewGetSnapshot
  );
}
