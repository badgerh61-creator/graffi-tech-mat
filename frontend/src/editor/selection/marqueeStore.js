import { useSyncExternalStore } from "react";

const state = {
  active: false,
  start: null,
  end: null,
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function startMarquee(point) {
  state.active = true;
  state.start = point;
  state.end = point;
  emit();
}

export function updateMarquee(point) {
  if (!state.active) return;
  state.end = point;
  emit();
}

export function endMarquee() {
  state.active = false;
  emit();
}

export function clearMarquee() {
  state.active = false;
  state.start = null;
  state.end = null;
  emit();
}

export function marqueeGetSnapshot() {
  return state;
}

export function marqueeSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useMarquee() {
  return useSyncExternalStore(
    marqueeSubscribe,
    marqueeGetSnapshot,
    marqueeGetSnapshot
  );
}
