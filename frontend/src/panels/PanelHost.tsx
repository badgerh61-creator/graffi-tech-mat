import React from "react";
import { panelRegistry } from "./_panelRegistry";
import { useActiveWorkspace } from "../state/workspaceStore";

export default function PanelHost() {
  const workspace = useActiveWorkspace();

  if (!workspace) {
    return null;
  }

  return (
    <aside className="panel-host">
      {workspace.allowedPanels.map((panelId) => {
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
            <header className="panel-header">
              {panelDef.title}
            </header>

            <div className="panel-content">
              <PanelComponent />
            </div>
          </section>
        );
      })}
    </aside>
  );
}

