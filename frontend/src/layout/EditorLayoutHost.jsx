// frontend/src/layout/EditorLayoutHost.jsx
import React, { useMemo, useEffect } from "react";
import PanelHost from "../panels/PanelHost";
import WorkspaceHost from "../workspaces/WorkspaceHost";
import DockDropZone from "./DockDropZone";
import DragGhost from "./DragGhost";
import { DEFAULT_EDITOR_LAYOUT } from "./defaultEditorLayout";
import { loadEditorLayout, saveEditorLayout } from "./editorLayoutStorage";

export default function EditorLayoutHost({
  editable = false,
  onSceneChange,
  panelContext = null, // ✅ NEW
}) {
  // Hydrate once, always safe
  const layout = useMemo(() => {
    const stored = loadEditorLayout();

    const left =
      stored?.docks?.left?.length
        ? stored.docks.left
        : DEFAULT_EDITOR_LAYOUT.docks.left;

    const right =
      stored?.docks?.right?.length
        ? stored.docks.right
        : DEFAULT_EDITOR_LAYOUT.docks.right;

    const bottom =
      stored?.docks?.bottom?.length
        ? stored.docks.bottom
        : DEFAULT_EDITOR_LAYOUT.docks.bottom;

    return {
      version: 1,
      docks: { left, right, bottom },
      center: "workspace",
    };
  }, []);

  // Persist the hydrated intent (one-time)
  useEffect(() => {
    saveEditorLayout(layout);
  }, [layout]);

  useEffect(() => {
    if (!editable) return;
    if (typeof onSceneChange !== "function") return;
    // no-op until you wire layout change events
  }, [editable, onSceneChange]);

  return (
    <div className="editor-root">
      <DragGhost />

      <DockDropZone dock="left">
        <aside className="dock dock-left">
          <PanelHost panelIds={layout.docks.left} panelContext={panelContext} />
        </aside>
      </DockDropZone>

      <main className="dock dock-center">
        <WorkspaceHost />
      </main>

      <DockDropZone dock="right">
        <aside className="dock dock-right">
          <PanelHost panelIds={layout.docks.right} panelContext={panelContext} />
        </aside>
      </DockDropZone>

      <DockDropZone dock="bottom">
        <footer className="dock dock-bottom">
          <PanelHost panelIds={layout.docks.bottom} panelContext={panelContext} />
        </footer>
      </DockDropZone>
    </div>
  );
}
