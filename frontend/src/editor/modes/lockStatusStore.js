import { useSyncExternalStore } from "react";

const state = {
  lock: { state: "unknown" }, // owned|taken|missing|unknown
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setLockStatus(lock) {
  state.lock = lock || { state: "unknown" };
  emit();
}

export function lockStatusGetSnapshot() {
  return state;
}

export function lockStatusSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useLockStatus() {
  return useSyncExternalStore(lockStatusSubscribe, lockStatusGetSnapshot, lockStatusGetSnapshot);
}
