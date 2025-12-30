import Sidebar from "./Sidebar";
import Topbar from "./Topbar";
import WorkspaceHost from "./WorkspaceHost";

export default function EditorShell() {
  return (
    <div className="editor-shell">
      <Topbar />
      <div className="editor-body">
        <Sidebar />
        <WorkspaceHost />
      </div>
    </div>
  );
}

