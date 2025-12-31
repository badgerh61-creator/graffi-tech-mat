import React from "react";
import { useWorkspaceStore } from "../state/workspaceStore";
import { workspaceRegistry, workspaceComponents } from "./_registry";

export default function WorkspaceHost() {
  const activeWorkspaceId = useWorkspaceStore(
    (s) => s.activeWorkspaceId
  );

  const workspaceDef = workspaceRegistry[activeWorkspaceId];

  // 🔒 THIS IS THE ONLY SAFE WAY
  const WorkspaceComponent =
    workspaceComponents[activeWorkspaceId];

  if (!workspaceDef || typeof WorkspaceComponent !== "function") {
    return (
      <main className="workspace-error">
        Invalid workspace: {activeWorkspaceId}
      </main>
    );
  }

  return (
    <main className="workspace-host">
      <header className="workspace-header">
        {workspaceDef.title}
      </header>

      <section className="workspace-content">
        <WorkspaceComponent />
      </section>
    </main>
  );
}

