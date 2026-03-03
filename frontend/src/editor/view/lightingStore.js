import { useSyncExternalStore } from "react";

const state = {
  hdrUrl: "/hdr/studio_small_08_1k.hdr", // put your file here later
  exposure: 1.0,
  envIntensity: 1.0,
  enabled: true,
};
const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setLighting(partial) {
  Object.assign(state, partial || {});
  emit();
}

export function lightingGetSnapshot() {
  return state;
}

export function lightingSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useLighting() {
  return useSyncExternalStore(lightingSubscribe, lightingGetSnapshot, lightingGetSnapshot);
}
