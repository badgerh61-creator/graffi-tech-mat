// frontend/src/panels/PanelHost.jsx

import React, { useMemo, useEffect } from "react";
import { panelRegistry } from "./_panelRegistry";
import { useActiveWorkspace } from "../state/workspaceStore";
import PanelErrorBoundary from "../errors/PanelErrorBoundary";
import PanelHeader from "./PanelHeader";
import {
  loadEditorSession,
  saveEditorSession,
} from "../session/editorSessionStorage";
import { EDITOR_SESSION_VERSION } from "../session/editorSessionStore";

export default function PanelHost() {
  const workspace = useActiveWorkspace();

  if (!workspace) {
    return null;
  }

  /**
   * 🔁 Week 9: restore panel intent safely
   */
  const session = loadEditorSession();

  const visiblePanels = useMemo(() => {
    const allowed = workspace.allowedPanels;

    if (!session.openPanels.length) {
      return allowed;
    }

    return session.openPanels.filter(
      (id) =>
        allowed.includes(id) &&
        Boolean(panelRegistry[id])
    );
  }, [workspace.allowedPanels]);

  /**
   * 🔁 Persist open panels when workspace changes
   */
  useEffect(() => {
    saveEditorSession({
      version: EDITOR_SESSION_VERSION,
      activeWorkspaceId: workspace.id,
      openPanels: visiblePanels,
    });
  }, [workspace.id, visiblePanels]);

  return (
    <aside className="panel-host">
      {visiblePanels.map((panelId) => {
        const panelDef = panelRegistry[panelId];

        if (!panelDef) {
          return (
            <div key={panelId} className="panel-error">
              Unknown panel: {panelId}
            </div>
          );
        }

        const PanelComponent = panelDef.component;

        return (
          <section key={panelDef.id} className="panel">
            {/* 🔧 Week 11: draggable panel header */}
            <PanelHeader
              panelId={panelDef.id}
              title={panelDef.title}
            />

            <PanelErrorBoundary
              panelId={panelDef.id}
              panelTitle={panelDef.title}
            >
              <div className="panel-content">
                <PanelComponent />
              </div>
            </PanelErrorBoundary>
          </section>
        );
      })}
    </aside>
  );
}

