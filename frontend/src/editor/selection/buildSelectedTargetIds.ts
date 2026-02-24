import type { SelectionState } from "./selectionTypes";

/**
 * Returns stable sorted ids (primary + secondary).
 * If no primary, returns [].
 */
export function buildSelectedTargetIds(selection: SelectionState): string[] {
  if (!selection.primary?.id) return [];

  const ids = new Set<string>();
  ids.add(selection.primary.id);

  for (const s of selection.secondary || []) {
    if (s?.id) ids.add(s.id);
  }

  return Array.from(ids).sort();
}
