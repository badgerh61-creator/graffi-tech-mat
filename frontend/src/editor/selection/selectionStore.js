import { useSyncExternalStore } from "react";

/**
 * Minimal external store (no libs).
 * Deterministic, testable.
 *
 * v1 (existing): selectedId
 * v2 (Tier 7.13): primary/secondary/hovered/lastUpdatedAt
 *
 * NOTE: We keep v1 API and bridge it to v2 so nothing breaks.
 */
const state = {
  // v1 legacy
  selectedId: null,

  // v2 typed selection (Tier 7.13)
  primary: null,     // { kind: "panel"|"curve"|"surface"|"vertex"|"edge", id: string } | null
  secondary: [],     // array of { kind, id }
  hovered: null,     // { kind, id } | null
  lastUpdatedAt: Date.now(),
};

const listeners = new Set();

function emit() {
  state.lastUpdatedAt = Date.now();
  for (const l of listeners) l();
}

export function selectionGetSnapshot() {
  return state;
}

export function selectionSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

// --------------------
// v1 API (keep)
// --------------------
export function setSelectedId(id) {
  state.selectedId = id ?? null;

  // Bridge: keep primary in sync (kind is stubbed to "panel" for now)
  state.primary = state.selectedId ? { kind: "panel", id: state.selectedId } : null;

  emit();
}

export function clearSelection() {
  state.selectedId = null;

  // Bridge: clear v2 too
  state.primary = null;
  state.secondary = [];
  state.hovered = null;

  emit();
}

// --------------------
// v2 API (Tier 7.13 add)
// --------------------
export function setPrimarySelection(item) {
  // item: { kind, id } | null
  state.primary = item ?? null;

  // Bridge: keep selectedId in sync for legacy code
  state.selectedId = state.primary?.id ?? null;

  emit();
}

export function setHoveredSelection(item) {
  state.hovered = item ?? null;
  emit();
}

export function toggleSecondarySelection(item) {
  const exists = state.secondary.some((x) => x.kind === item.kind && x.id === item.id);
  state.secondary = exists
    ? state.secondary.filter((x) => !(x.kind === item.kind && x.id === item.id))
    : [...state.secondary, item];

  emit();
}

export function clearTypedSelection() {
  state.primary = null;
  state.secondary = [];
  state.hovered = null;

  // Bridge: clear legacy too
  state.selectedId = null;

  emit();
}

export function useSelection() {
  return useSyncExternalStore(
    selectionSubscribe,
    selectionGetSnapshot,
    selectionGetSnapshot
  );
}
