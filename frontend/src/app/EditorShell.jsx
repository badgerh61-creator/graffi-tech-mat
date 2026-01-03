// frontend/src/app/EditorShell.jsx
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function EditorShell({ children }) {
  return (
    <div className="editor-shell">
      <Topbar />
      <div className="editor-body">
        <Sidebar />
        {children}
      </div>
    </div>
  );
}

