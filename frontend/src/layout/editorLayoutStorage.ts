// frontend/src/layout/editorLayoutStorage.ts

import {
  EditorLayoutState,
  DEFAULT_EDITOR_LAYOUT,
  validateEditorLayout,
} from "./editorLayoutStore";

const STORAGE_KEY = "graffi.editor.layout";

/**
 * Load editor layout from storage.
 * Always returns a safe layout.
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
      console.warn(
        "[EditorLayout] Invalid layout data, falling back to default"
      );
      return DEFAULT_EDITOR_LAYOUT;
    }

    return validated;
  } catch (err) {
    console.error("[EditorLayout] Failed to load layout", err);
    return DEFAULT_EDITOR_LAYOUT;
  }
}

/**
 * Save editor layout to storage.
 * Never throws.
 */
export function saveEditorLayout(
  layout: EditorLayoutState
): void {
  try {
    const payload: EditorLayoutState = {
      ...layout,
      version: layout.version,
    };

    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(payload)
    );
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

