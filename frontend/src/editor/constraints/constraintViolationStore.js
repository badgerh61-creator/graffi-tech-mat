import { useSyncExternalStore } from "react";

const state = {
  violations: [],
};

const listeners = new Set();

function emit() {
  for (const l of listeners) {
    try {
      l();
    } catch (err) {
      console.error("constraintViolationStore listener error", err);
    }
  }
}

function stableSort(violations = []) {
  return [...violations].sort((a, b) => {
    const at = String(a?.target_id || "");
    const bt = String(b?.target_id || "");
    if (at !== bt) return at.localeCompare(bt);

    const ak = String(a?.kind || "");
    const bk = String(b?.kind || "");
    if (ak !== bk) return ak.localeCompare(bk);

    const ac = String(a?.constraint_id || "");
    const bc = String(b?.constraint_id || "");
    return ac.localeCompare(bc);
  });
}

export function setConstraintViolations(violations) {
  if (!Array.isArray(violations)) {
    state.violations = [];
  } else {
    state.violations = stableSort(violations);
  }
  emit();
}

export function clearConstraintViolations() {
  state.violations = [];
  emit();
}

export function constraintViolationGetSnapshot() {
  return state;
}

export function constraintViolationSubscribe(listener) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

export function useConstraintViolations() {
  return useSyncExternalStore(
    constraintViolationSubscribe,
    constraintViolationGetSnapshot,
    constraintViolationGetSnapshot
  );
}
