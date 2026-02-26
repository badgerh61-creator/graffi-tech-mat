// frontend/src/editor/history/historyStore.js

import { useSyncExternalStore } from "react";

/**
 * Tier 7.28 — UI-only snapshot history store.
 * stack: array of snapshot ids (strings)
 * cursor: index of currently active snapshot in stack
 */
const state = {
  stack: [],
  cursor: -1,
};

const listeners = new Set();

function emit() {
  for (const l of listeners) l();
}

export function historyGetSnapshot() {
  return state;
}

export function historySubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function historyPush(snapshotId) {
  const id = String(snapshotId);

  // If we are not at the end, cut off "future" branch
  if (state.cursor >= 0 && state.cursor < state.stack.length - 1) {
    state.stack = state.stack.slice(0, state.cursor + 1);
  }

  state.stack.push(id);
  state.cursor = state.stack.length - 1;
  emit();
}

export function historySetActive(snapshotId) {
  const id = String(snapshotId);
  const idx = state.stack.indexOf(id);
  if (idx >= 0) {
    state.cursor = idx;
  } else {
    state.stack.push(id);
    state.cursor = state.stack.length - 1;
  }
  emit();
}

export function historyCanUndo() {
  return state.cursor > 0;
}

export function historyCanRedo() {
  return state.cursor >= 0 && state.cursor < state.stack.length - 1;
}

export function historyUndo() {
  if (!historyCanUndo()) return null;
  state.cursor -= 1;
  emit();
  return state.stack[state.cursor];
}

export function historyRedo() {
  if (!historyCanRedo()) return null;
  state.cursor += 1;
  emit();
  return state.stack[state.cursor];
}

export function useHistory() {
  return useSyncExternalStore(historySubscribe, historyGetSnapshot, historyGetSnapshot);
}
