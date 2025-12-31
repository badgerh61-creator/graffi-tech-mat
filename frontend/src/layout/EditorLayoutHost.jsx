import React from "react";
import { DEFAULT_EDITOR_LAYOUT } from "./defaultEditorLayout";
import PanelHost from "../panels/PanelHost";
import WorkspaceHost from "../workspaces/WorkspaceHost";

export default function EditorLayoutHost() {
  const layout = DEFAULT_EDITOR_LAYOUT; // Week 6 = static

  return (
    <div className="editor-root">
      <aside className="dock dock-left">
        <PanelHost panelIds={layout.left} />
      </aside>

      <main className="dock dock-center">
        <WorkspaceHost />
      </main>

      <aside className="dock dock-right">
        <PanelHost panelIds={layout.right} />
      </aside>

      <footer className="dock dock-bottom">
        <PanelHost panelIds={layout.bottom} />
      </footer>
    </div>
  );
}

