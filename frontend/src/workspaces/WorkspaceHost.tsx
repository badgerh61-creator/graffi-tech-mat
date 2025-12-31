// frontend/src/workspaces/WorkspaceHost.jsx

import React from "react";
import { useWorkspaceStore } from "../state/workspaceStore";
import { workspaceRegistry, workspaceComponents } from "./_registry";
import { useCapability } from "../capabilities/useCapabilities";
import EditorErrorBoundary from "../errors/EditorErrorBoundary";

export default function WorkspaceHost() {
  const activeWorkspaceId = useWorkspaceStore(
    (s) => s.activeWorkspaceId
  );

  const workspaceDef = activeWorkspaceId
    ? workspaceRegistry[activeWorkspaceId]
    : null;

  const WorkspaceComponent = activeWorkspaceId
    ? workspaceComponents[activeWorkspaceId]
    : null;

  const canView = useCapability("view");
  const canEdit = useCapability("edit");

  // 🔒 HARD BLOCK — no view capability
  if (!canView) {
    return (
      <main className="workspace-denied">
        Access denied
      </main>
    );
  }

  // 🧱 SAFETY — invalid registry entry
  if (
    !workspaceDef ||
    !WorkspaceComponent ||
    typeof WorkspaceComponent !== "function"
  ) {
    return (
      <main className="workspace-error">
        Invalid workspace: {activeWorkspaceId}
      </main>
    );
  }

  return (
    <EditorErrorBoundary scope={`workspace:${activeWorkspaceId}`}>
      <main
        className={`workspace-host ${
          canEdit ? "" : "workspace-readonly"
        }`}
      >
        <header className="workspace-header">
          {workspaceDef.title}
          {!canEdit && (
            <span className="workspace-readonly-badge">
              Read-only
            </span>
          )}
        </header>

        <section className="workspace-content">
          <WorkspaceComponent />
        </section>
      </main>
    </EditorErrorBoundary>
  );
}

