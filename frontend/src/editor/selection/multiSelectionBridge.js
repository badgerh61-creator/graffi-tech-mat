import { setSelectedId, clearSelection } from "./selectionStore";
import { setPrimarySelection, clearMultiSelection } from "./multiSelectionStore";

export function syncPrimaryToSingleSelection(primaryId) {
  if (!primaryId) {
    clearSelection?.();
    return;
  }

  setSelectedId?.(primaryId);
}

export function clearAllSelectionState() {
  clearSelection?.();
  clearMultiSelection?.();
}

export function setSingleAsPrimary(id) {
  setPrimarySelection(id);
  syncPrimaryToSingleSelection(id);
}
