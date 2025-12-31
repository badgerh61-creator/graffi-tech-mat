import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

import WorkspaceHost from "../workspaces/WorkspaceHost";
import PanelHost from "../panels/PanelHost";

import { useCapabilities } from "../capabilities";

function CapabilityDebug() {
  const caps = useCapabilities();

  return (
    <div style={{ fontSize: 12, padding: "4px 8px", background: "#111", color: "#0f0" }}>
      edit: {caps.edit ? "YES" : "NO"} ·
      upload: {caps.upload ? "YES" : "NO"} ·
      admin: {caps.admin ? "YES" : "NO"}
    </div>
  );
}

export default function EditorShell() {
  return (
    <div className="editor-shell">
      <Topbar />
      <CapabilityDebug />
      <div className="editor-body">
        <Sidebar />
        <WorkspaceHost />
        <PanelHost />
      </div>
    </div>
  );
}

