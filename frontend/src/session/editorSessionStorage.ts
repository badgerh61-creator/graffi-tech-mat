// frontend/src/session/editorSessionStorage.ts

import {
  EditorSessionState,
  DEFAULT_EDITOR_SESSION,
  validateEditorSession,
} from "./editorSessionStore";

const STORAGE_KEY = "graffi.editor.session";

/**
 * Load editor session from storage.
 * Always returns a safe value.
 */
export function loadEditorSession(): EditorSessionState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return DEFAULT_EDITOR_SESSION;
    }

    const parsed = JSON.parse(raw);
    const validated = validateEditorSession(parsed);

    if (!validated) {
      console.warn(
        "[EditorSession] Invalid session data, falling back to default"
      );
      return DEFAULT_EDITOR_SESSION;
    }

    return validated;
  } catch (err) {
    console.error("[EditorSession] Failed to load session", err);
    return DEFAULT_EDITOR_SESSION;
  }
}

/**
 * Save editor session to storage.
 * Never throws.
 */
export function saveEditorSession(
  session: EditorSessionState
): void {
  try {
    const payload: EditorSessionState = {
      ...session,
      version: session.version,
    };

    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(payload)
    );
  } catch (err) {
    console.error("[EditorSession] Failed to save session", err);
  }
}

/**
 * Clear editor session from storage.
 * Useful for debugging and resets.
 */
export function clearEditorSession(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (err) {
    console.error("[EditorSession] Failed to clear session", err);
  }
}

