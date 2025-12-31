// frontend/src/layout/EditorLayoutHost.jsx

import React, { useMemo, useEffect } from "react";
import PanelHost from "../panels/PanelHost";
import WorkspaceHost from "../workspaces/WorkspaceHost";
import DockDropZone from "./DockDropZone";
import DragGhost from "./DragGhost";
import { DEFAULT_EDITOR_LAYOUT } from "./defaultEditorLayout";
import {
  loadEditorLayout,
  saveEditorLayout,
} from "./editorLayoutStorage";

export default function EditorLayoutHost() {
  /**
   * 🔁 Week 10: hydrate layout safely
   */
  const layout = useMemo(() => {
    const stored = loadEditorLayout();

    return {
      left: stored.docks.left.length
        ? stored.docks.left
        : DEFAULT_EDITOR_LAYOUT.left,
      right: stored.docks.right.length
        ? stored.docks.right
        : DEFAULT_EDITOR_LAYOUT.right,
      bottom: stored.docks.bottom.length
        ? stored.docks.bottom
        : DEFAULT_EDITOR_LAYOUT.bottom,
    };
  }, []);

  /**
   * 🔁 Persist layout intent
   * (no UI mutation yet)
   */
  useEffect(() => {
    saveEditorLayout({
      version: 1,
      docks: {
        left: layout.left,
        right: layout.right,
        bottom: layout.bottom,
      },
    });
  }, [layout]);

  return (
    <div className="editor-root">
      {/* 🎨 Week 12: visual drag preview */}
      <DragGhost />

      <DockDropZone dock="left">
        <aside className="dock dock-left">
          <PanelHost panelIds={layout.left} />
        </aside>
      </DockDropZone>

      <main className="dock dock-center">
        <WorkspaceHost />
      </main>

      <DockDropZone dock="right">
        <aside className="dock dock-right">
          <PanelHost panelIds={layout.right} />
        </aside>
      </DockDropZone>

      <DockDropZone dock="bottom">
        <footer className="dock dock-bottom">
          <PanelHost panelIds={layout.bottom} />
        </footer>
      </DockDropZone>
    </div>
  );
}

