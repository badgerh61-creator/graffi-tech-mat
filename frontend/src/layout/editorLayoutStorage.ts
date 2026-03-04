// frontend/src/layout/editorLayoutStorage.ts

import {
  EditorLayoutState,
  DEFAULT_EDITOR_LAYOUT,
  validateEditorLayout,
} from "./editorLayoutStore";

const STORAGE_KEY = "graffi.editor.layout";

/**
 * Merge helper:
 * - keep user's dock order
 * - append any missing default panels
 * - remove duplicates
 */
function mergeDock(userDock: any, defaultDock: any): string[] {
  const u = Array.isArray(userDock) ? userDock.map(String) : [];
  const d = Array.isArray(defaultDock) ? defaultDock.map(String) : [];

  const out: string[] = [];
  const seen = new Set<string>();

  for (const id of u) {
    if (!id) continue;
    if (seen.has(id)) continue;
    out.push(id);
    seen.add(id);
  }

  for (const id of d) {
    if (!id) continue;
    if (seen.has(id)) continue;
    out.push(id);
    seen.add(id);
  }

  return out;
}

/**
 * Migration / normalization:
 * Always returns a safe layout and ensures new default panels appear.
 */
function migrateLayout(layout: EditorLayoutState): EditorLayoutState {
  // Always ensure docks exist
  const docks: any = (layout as any).docks || (layout as any);

  const left = mergeDock(docks.left, DEFAULT_EDITOR_LAYOUT.left);
  const right = mergeDock(docks.right, DEFAULT_EDITOR_LAYOUT.right);
  const bottom = mergeDock(docks.bottom, DEFAULT_EDITOR_LAYOUT.bottom);

  return {
    ...DEFAULT_EDITOR_LAYOUT,
    ...layout,
    version: (layout as any).version ?? DEFAULT_EDITOR_LAYOUT.version ?? 1,
    docks: {
      left,
      right,
      bottom,
    },
  } as any;
}

/**
 * Load editor layout from storage.
 * Always returns a safe layout.
 * Also auto-migrates older layouts to include new default panels.
 */
export function loadEditorLayout(): EditorLayoutState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return DEFAULT_EDITOR_LAYOUT;
    }

    const parsed = JSON.parse(raw);
    const validated = validateEditorLayout(parsed);

    if (!validated) {
      console.warn("[EditorLayout] Invalid layout data, falling back to default");
      return DEFAULT_EDITOR_LAYOUT;
    }

    return migrateLayout(validated);
  } catch (err) {
    console.error("[EditorLayout] Failed to load layout", err);
    return DEFAULT_EDITOR_LAYOUT;
  }
}

/**
 * Save editor layout to storage.
 * Never throws.
 */
export function saveEditorLayout(layout: EditorLayoutState): void {
  try {
    const payload: EditorLayoutState = migrateLayout({
      ...layout,
      version: layout.version,
    } as any);

    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch (err) {
    console.error("[EditorLayout] Failed to save layout", err);
  }
}

/**
 * Clear editor layout from storage.
 * Useful for debugging and resets.
 */
export function clearEditorLayout(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (err) {
    console.error("[EditorLayout] Failed to clear layout", err);
  }
}
