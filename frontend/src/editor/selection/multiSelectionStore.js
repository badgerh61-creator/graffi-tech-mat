import { useSyncExternalStore } from "react";

const state = {
  primaryId: null,
  selectedIds: [],
};

const listeners = new Set();

function emit() {
  listeners.forEach((l) => l());
}

function normalizeObjectId(id) {
  const s = String(id || "").trim();
  if (!s) return null;
  return s.split("::")[0] || null;
}

function uniqueOrdered(ids) {
  const seen = new Set();
  const out = [];

  for (const raw of ids || []) {
    const id = normalizeObjectId(raw);
    if (!id || seen.has(id)) continue;
    seen.add(id);
    out.push(id);
  }

  return out;
}

export function setMultiSelection(ids, primaryId = null) {
  const selectedIds = uniqueOrdered(ids);
  const normPrimary = normalizeObjectId(primaryId);

  state.selectedIds = selectedIds;
  state.primaryId =
    normPrimary && selectedIds.includes(normPrimary)
      ? normPrimary
      : (selectedIds[0] || null);

  emit();
}

export function clearMultiSelection() {
  state.selectedIds = [];
  state.primaryId = null;
  emit();
}

export function addToMultiSelection(id, makePrimary = false) {
  const norm = normalizeObjectId(id);
  if (!norm) return;

  const next = uniqueOrdered([...state.selectedIds, norm]);
  state.selectedIds = next;
  state.primaryId = makePrimary
    ? norm
    : (state.primaryId && next.includes(state.primaryId) ? state.primaryId : norm);

  emit();
}

export function removeFromMultiSelection(id) {
  const norm = normalizeObjectId(id);
  if (!norm) return;

  const next = state.selectedIds.filter((x) => x !== norm);
  state.selectedIds = next;
  state.primaryId = next.includes(state.primaryId)
    ? state.primaryId
    : (next[0] || null);

  emit();
}

export function toggleMultiSelection(id, makePrimaryOnAdd = true) {
  const norm = normalizeObjectId(id);
  if (!norm) return;

  if (state.selectedIds.includes(norm)) {
    removeFromMultiSelection(norm);
    return;
  }

  addToMultiSelection(norm, makePrimaryOnAdd);
}

export function setPrimarySelection(id) {
  const norm = normalizeObjectId(id);
  if (!norm) return;

  if (!state.selectedIds.includes(norm)) {
    state.selectedIds = uniqueOrdered([...state.selectedIds, norm]);
  }

  state.primaryId = norm;
  emit();
}

export function multiSelectionGetSnapshot() {
  return state;
}

export function multiSelectionSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useMultiSelection() {
  return useSyncExternalStore(
    multiSelectionSubscribe,
    multiSelectionGetSnapshot,
    multiSelectionGetSnapshot
  );
}
