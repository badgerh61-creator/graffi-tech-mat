// frontend/src/session/editorSessionStore.ts

import { PanelKey } from "../panels/_panelRegistry";

export const EDITOR_SESSION_VERSION = 1;

/**
 * Editor session state represents editor intent,
 * not engine or model data.
 */
export interface EditorSessionState {
  version: number;

  /**
   * Currently active workspace ID
   */
  activeWorkspaceId: string | null;

  /**
   * Panels that should be open (by key)
   */
  openPanels: PanelKey[];
}

/**
 * Default, safe session state.
 * Used when no session exists or validation fails.
 */
export const DEFAULT_EDITOR_SESSION: EditorSessionState = {
  version: EDITOR_SESSION_VERSION,
  activeWorkspaceId: null,
  openPanels: [],
};

/**
 * Validate session payload shape and version.
 * Never throws.
 */
export function validateEditorSession(
  raw: unknown
): EditorSessionState | null {
  if (!raw || typeof raw !== "object") {
    return null;
  }

  const data = raw as Partial<EditorSessionState>;

  if (data.version !== EDITOR_SESSION_VERSION) {
    return null;
  }

  if (
    data.activeWorkspaceId !== null &&
    typeof data.activeWorkspaceId !== "string"
  ) {
    return null;
  }

  if (
    !Array.isArray(data.openPanels) ||
    !data.openPanels.every((p) => typeof p === "string")
  ) {
    return null;
  }

  return {
    version: EDITOR_SESSION_VERSION,
    activeWorkspaceId: data.activeWorkspaceId ?? null,
    openPanels: data.openPanels as PanelKey[],
  };
}

