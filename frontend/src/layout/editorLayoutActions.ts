// frontend/src/layout/editorLayoutActions.ts

import {
  EditorLayoutState,
  EDITOR_LAYOUT_VERSION,
} from "./editorLayoutStore";
import { PanelKey } from "../panels/_panelRegistry";

export type DockPosition = "left" | "right" | "bottom";

/**
 * Move a panel to a different dock or reorder within a dock.
 * Returns a NEW layout state. Never mutates input.
 */
export function movePanel(
  layout: EditorLayoutState,
  panelId: PanelKey,
  targetDock: DockPosition,
  targetIndex?: number
): EditorLayoutState {
  // Defensive copy
  const next: EditorLayoutState = {
    version: EDITOR_LAYOUT_VERSION,
    docks: {
      left: [...layout.docks.left],
      right: [...layout.docks.right],
      bottom: [...layout.docks.bottom],
    },
  };

  // Remove panel from all docks
  (Object.keys(next.docks) as DockPosition[]).forEach(
    (dock) => {
      const idx = next.docks[dock].indexOf(panelId);
      if (idx !== -1) {
        next.docks[dock].splice(idx, 1);
      }
    }
  );

  const target = next.docks[targetDock];

  // Clamp insertion index
  const insertAt =
    typeof targetIndex === "number" &&
    targetIndex >= 0 &&
    targetIndex <= target.length
      ? targetIndex
      : target.length;

  target.splice(insertAt, 0, panelId);

  return next;
}

/**
 * Remove a panel from layout entirely.
 * Used when capability is lost or panel is unregistered.
 */
export function removePanel(
  layout: EditorLayoutState,
  panelId: PanelKey
): EditorLayoutState {
  return {
    version: EDITOR_LAYOUT_VERSION,
    docks: {
      left: layout.docks.left.filter(
        (id) => id !== panelId
      ),
      right: layout.docks.right.filter(
        (id) => id !== panelId
      ),
      bottom: layout.docks.bottom.filter(
        (id) => id !== panelId
      ),
    },
  };
}

/**
 * Normalize layout against allowed panels.
 * Used when capabilities or registry change.
 */
export function normalizeLayout(
  layout: EditorLayoutState,
  allowedPanels: PanelKey[]
): EditorLayoutState {
  const filterDock = (dock: PanelKey[]) =>
    dock.filter((id) => allowedPanels.includes(id));

  return {
    version: EDITOR_LAYOUT_VERSION,
    docks: {
      left: filterDock(layout.docks.left),
      right: filterDock(layout.docks.right),
      bottom: filterDock(layout.docks.bottom),
    },
  };
}

