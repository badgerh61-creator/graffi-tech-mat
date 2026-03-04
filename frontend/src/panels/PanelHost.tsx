// frontend/src/panels/PanelHost.tsx

import React from "react";
import { panelRegistry, PanelKey } from "./_panelRegistry";
import PanelErrorBoundary from "../errors/PanelErrorBoundary";
import PanelHeader from "./PanelHeader";
import { useCapability } from "../capabilities/useCapabilities";

export interface PanelContext {
  // HistoryPanel
  history?: any[];
  activeSnapshotId?: number | string | null;
  onNavigate?: (snapshotId: number | string) => void;

  // ConstraintPanel
  constraints?: any[];
}

interface PanelHostProps {
  panelIds: PanelKey[];
  panelContext?: PanelContext;
}

/**
 * Hook-safe child slot:
 * - useCapability() is called at the top level of this component
 * - never inside a loop in PanelHost
 */
function PanelSlot({
  panelId,
  panelContext,
}: {
  panelId: PanelKey;
  panelContext?: PanelContext;
}) {
  const panelDef = panelRegistry[panelId];
  if (!panelDef) return null;

  const allowed = useCapability(panelDef.requiredCapability);
  if (!allowed) return null;

  const PanelComponent = panelDef.component;

  // Resolve per-panel props (additive-safe)
  let panelProps: any = {};

  if (panelId === "history") {
    panelProps = {
      history: panelContext?.history ?? [],
      activeSnapshotId: panelContext?.activeSnapshotId ?? null,
      onNavigate: panelContext?.onNavigate,
    };
  }

  if (panelId === "constraints") {
    panelProps = {
      constraints: panelContext?.constraints ?? [],
    };
  }

  return (
    <section key={panelDef.id} className="panel">
      <PanelHeader panelId={panelDef.id} title={panelDef.title} />

      <PanelErrorBoundary panelId={panelDef.id} panelTitle={panelDef.title}>
        <div className="panel-content">
          <PanelComponent {...panelProps} />
        </div>
      </PanelErrorBoundary>
    </section>
  );
}

export default function PanelHost({ panelIds, panelContext }: PanelHostProps) {
  if (!panelIds || panelIds.length === 0) {
    return null;
  }

  return (
    <>
      {panelIds.map((panelId) => (
        <PanelSlot
          key={panelId}
          panelId={panelId}
          panelContext={panelContext}
        />
      ))}
    </>
  );
}
