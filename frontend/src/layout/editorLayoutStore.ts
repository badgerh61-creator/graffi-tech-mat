// frontend/src/layout/editorLayoutStore.ts

import { PanelKey } from "../panels/_panelRegistry";

export const EDITOR_LAYOUT_VERSION = 1;

/**
 * Editor layout state represents structural intent only.
 * No UI behavior or sizing data lives here.
 */
export interface EditorLayoutState {
  version: number;
  docks: {
    left: PanelKey[];
    right: PanelKey[];
    bottom: PanelKey[];
  };
}

/**
 * Default editor layout.
 * This is the ultimate safe fallback.
 */
export const DEFAULT_EDITOR_LAYOUT: EditorLayoutState = {
  version: EDITOR_LAYOUT_VERSION,
  docks: {
    left: [],
    right: [],
    bottom: [],
  },
};

/**
 * Validate a raw layout payload.
 * Never throws. Never mutates input.
 */
export function validateEditorLayout(
  raw: unknown
): EditorLayoutState | null {
  if (!raw || typeof raw !== "object") {
    return null;
  }

  const data = raw as Partial<EditorLayoutState>;

  if (data.version !== EDITOR_LAYOUT_VERSION) {
    return null;
  }

  if (
    !data.docks ||
    typeof data.docks !== "object"
  ) {
    return null;
  }

  const { left, right, bottom } = data.docks;

  if (
    !Array.isArray(left) ||
    !Array.isArray(right) ||
    !Array.isArray(bottom)
  ) {
    return null;
  }

  const isValidPanelArray = (arr: unknown[]) =>
    arr.every((p) => typeof p === "string");

  if (
    !isValidPanelArray(left) ||
    !isValidPanelArray(right) ||
    !isValidPanelArray(bottom)
  ) {
    return null;
  }

  return {
    version: EDITOR_LAYOUT_VERSION,
    docks: {
      left: left as PanelKey[],
      right: right as PanelKey[],
      bottom: bottom as PanelKey[],
    },
  };
}

