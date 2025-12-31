// frontend/src/layout/usePanelDrag.ts

import { useCallback, useRef } from "react";
import { PanelKey } from "../panels/_panelRegistry";
import { DockPosition, movePanel } from "./editorLayoutActions";
import { useEditorLayoutStore } from "./editorLayoutState";

/**
 * Thin intent layer for panel dragging.
 * Converts drag intent into legal layout mutations.
 */
export function usePanelDrag() {
  const draggingPanel = useRef<PanelKey | null>(null);

  const layout = useEditorLayoutStore((s) => s.layout);
  const setLayout = useEditorLayoutStore((s) => s.setLayout);

  /**
   * Called when user starts dragging a panel header.
   */
  const beginDrag = useCallback((panelId: PanelKey) => {
    draggingPanel.current = panelId;
  }, []);

  /**
   * Called when dragging is cancelled or aborted.
   */
  const cancelDrag = useCallback(() => {
    draggingPanel.current = null;
  }, []);

  /**
   * Called when user drops panel into a dock.
   */
  const dropPanel = useCallback(
    (targetDock: DockPosition, targetIndex?: number) => {
      if (!draggingPanel.current) {
        return;
      }

      const next = movePanel(
        layout,
        draggingPanel.current,
        targetDock,
        targetIndex
      );

      setLayout(next);
      draggingPanel.current = null;
    },
    [layout, setLayout]
  );

  return {
    beginDrag,
    dropPanel,
    cancelDrag,
    isDragging: draggingPanel.current !== null,
    draggingPanel: draggingPanel.current,
  };
}

