// frontend/src/panels/PanelHost.tsx

import React from "react";
import { panelRegistry, PanelKey } from "./_panelRegistry";
import PanelErrorBoundary from "../errors/PanelErrorBoundary";
import PanelHeader from "./PanelHeader";
import { useCapability } from "../capabilities/useCapabilities";

interface PanelHostProps {
  panelIds: PanelKey[];
}

export default function PanelHost({ panelIds }: PanelHostProps) {
  if (!panelIds || panelIds.length === 0) {
    return null;
  }

  return (
    <>
      {panelIds.map((panelId) => {
        const panelDef = panelRegistry[panelId];
        if (!panelDef) return null;

        const allowed = useCapability(
          panelDef.requiredCapability
        );
        if (!allowed) return null;

        const PanelComponent = panelDef.component;

        return (
          <section key={panelDef.id} className="panel">
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
    </>
  );
}

