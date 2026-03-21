// frontend/src/editor/history/historyStore.js

import { useSyncExternalStore } from "react";

/**
 * Tier 7.66 — History Timeline (Undo / Redo)
 *
 * Backward compatible with Tier 7.28:
 * - still supports stack (array of snapshot ids)
 * - still supports push/undo/redo
 *
 * New:
 * - supports full snapshot objects
 * - deterministic timeline sync
 * - jump + restore support
 */

const state = {
  stack: [],          // array of snapshot ids (legacy)
  snapshots: [],      // array of snapshot objects (new)
  cursor: -1,
};

const listeners = new Set();

function emit() {
  for (const l of listeners) l();
}

/* -----------------------------
 * Core getters / subscribe
 * ----------------------------- */

export function historyGetSnapshot() {
  return state;
}

export function historySubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

/* -----------------------------
 * Tier 7.66 — Timeline Sync
 * ----------------------------- */

export function setTimelineSnapshots(snaps, activeId) {
  const list = Array.isArray(snaps) ? [...snaps] : [];

  state.snapshots = list;
  state.stack = list.map((s) => String(s.id));

  const idx = state.stack.indexOf(String(activeId));
  state.cursor = idx >= 0 ? idx : list.length - 1;

  emit();
}

/* -----------------------------
 * Tier 7.28 — Push / Active
 * ----------------------------- */

export function historyPush(snapshotId) {
  const id = String(snapshotId);

  // cut future branch if needed
  if (state.cursor >= 0 && state.cursor < state.stack.length - 1) {
    state.stack = state.stack.slice(0, state.cursor + 1);
    state.snapshots = state.snapshots.slice(0, state.cursor + 1);
  }

  state.stack.push(id);

  // keep snapshots in sync (fallback object)
  state.snapshots.push({ id, status: "unknown" });

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
    state.snapshots.push({ id, status: "unknown" });
    state.cursor = state.stack.length - 1;
  }

  emit();
}

/* -----------------------------
 * Undo / Redo
 * ----------------------------- */

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

  return getCurrentSnapshot();
}

export function historyRedo() {
  if (!historyCanRedo()) return null;

  state.cursor += 1;
  emit();

  return getCurrentSnapshot();
}

/* -----------------------------
 * Tier 7.66 — Jump / Cursor Move
 * ----------------------------- */

export function historyJumpTo(snapshotId) {
  const id = String(snapshotId);
  const idx = state.stack.indexOf(id);
  if (idx < 0) return null;

  state.cursor = idx;
  emit();

  return getCurrentSnapshot();
}

/**
 * ✅ Backward compatibility alias (used by panels/tests)
 */
export const jumpToSnapshot = historyJumpTo;

export function historyMoveCursor(delta) {
  const next = Math.max(
    0,
    Math.min(state.stack.length - 1, state.cursor + delta)
  );

  if (next === state.cursor) return null;

  state.cursor = next;
  emit();

  return getCurrentSnapshot();
}

/* -----------------------------
 * Helpers
 * ----------------------------- */

export function getCurrentSnapshot() {
  if (state.cursor < 0) return null;

  return (
    state.snapshots[state.cursor] ||
    { id: state.stack[state.cursor], status: "unknown" }
  );
}

/* -----------------------------
 * React hook
 * ----------------------------- */

export function useHistory() {
  return useSyncExternalStore(
    historySubscribe,
    historyGetSnapshot,
    historyGetSnapshot
  );
}
