import type { SelectableKind } from "./selectionTypes";

// Unified store: contains BOTH v1 + v2 APIs
import { setPrimarySelection, clearSelection } from "./selectionStore";

/**
 * Canonical selection entrypoints (typed-first).
 * Legacy selectedId is updated automatically by selectionStore bridges.
 */
export function selectPrimaryById(opts: { kind: SelectableKind; id: string }) {
  const { kind, id } = opts;
  setPrimarySelection({ kind, id });
}

export function clearAllSelection() {
  // clears both typed + legacy via your bridged clearSelection()
  clearSelection();
}
