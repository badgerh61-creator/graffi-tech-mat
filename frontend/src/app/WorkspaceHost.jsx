import { getActiveWorkspace } from "../state/editorStore";
import { workspaceRegistry } from "../workspaces/_registry";

export default function WorkspaceHost() {
  const workspaceId = getActiveWorkspace();
  const Workspace = workspaceRegistry[workspaceId];

  if (!Workspace) {
    return <div className="workspace-empty">No workspace</div>;
  }

  return (
    <main className="workspace-host">
      <Workspace />
    </main>
  );
}

