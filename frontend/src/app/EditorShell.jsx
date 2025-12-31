import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

// ✅ IMPORTANT: use Phase G WorkspaceHost
import WorkspaceHost from "../workspaces/WorkspaceHost";

import PanelHost from "../panels/PanelHost";

export default function EditorShell() {
  return (
    <div className="editor-shell">
      <Topbar />
      <div className="editor-body">
        <Sidebar />
        <WorkspaceHost />
        <PanelHost />
      </div>
    </div>
  );
}

