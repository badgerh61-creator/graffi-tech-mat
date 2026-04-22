// frontend/src/editor/selection/selectionStore.js
import { useSyncExternalStore } from "react";

/**
 * Minimal external store (no libs).
 * Deterministic, testable.
 */

const state = {
  // v1 legacy
  selectedId: null,

  // v2 typed selection
  primary: null,
  secondary: [],
  hovered: null,
  lastUpdatedAt: Date.now(),
};

const listeners = new Set();

// ✅ CRITICAL: stable snapshot reference
let cachedSnapshot = { ...state };

function emit() {
  state.lastUpdatedAt = Date.now();

  // ✅ ONLY update snapshot when state changes
  cachedSnapshot = { ...state };

  for (const l of listeners) l();
}

// --------------------
// SNAPSHOT
// --------------------
export function selectionGetSnapshot() {
  return cachedSnapshot;
}

export function selectionSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

// --------------------
// v1 API (legacy)
// --------------------
export function setSelectedId(id) {
  state.selectedId = id ?? null;

  state.primary = state.selectedId
    ? { kind: "panel", id: state.selectedId }
    : null;

  emit();
}

export function clearSelection() {
  state.selectedId = null;
  state.primary = null;
  state.secondary = [];
  state.hovered = null;

  emit();
}

// --------------------
// v2 API
// --------------------
export function setPrimarySelection(item) {
  state.primary = item ?? null;
  state.selectedId = state.primary?.id ?? null;

  emit();
}

export function setHoveredSelection(item) {
  state.hovered = item ?? null;
  emit();
}

export function toggleSecondarySelection(item) {
  const exists = state.secondary.some(
    (x) => x.kind === item.kind && x.id === item.id
  );

  state.secondary = exists
    ? state.secondary.filter(
        (x) => !(x.kind === item.kind && x.id === item.id)
      )
    : [...state.secondary, item];

  emit();
}

export function clearTypedSelection() {
  state.primary = null;
  state.secondary = [];
  state.hovered = null;
  state.selectedId = null;

  emit();
}

// --------------------
// Resolver bridge
// --------------------
export function applyResolvedSelectionToStore(resolved) {
  const ids = resolved?.selected_target_ids ?? [];
  const active = resolved?.active_target_id ?? null;

  if (!ids.length || !active) {
    clearSelection();
    return;
  }

  clearSelection();

  setPrimarySelection({ kind: "panel", id: active });

  for (const id of ids) {
    if (id === active) continue;
    toggleSecondarySelection({ kind: "panel", id });
  }
}

// --------------------
// HOOK
// --------------------
export function useSelection() {
  return useSyncExternalStore(
    selectionSubscribe,
    selectionGetSnapshot,
    selectionGetSnapshot
  );
}
