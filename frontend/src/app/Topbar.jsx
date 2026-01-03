// frontend/src/app/Topbar.jsx

export default function Topbar() {
  return (
    <header className="editor-topbar">
      {/* LEFT */}
      <div className="project-name">Untitled Project</div>

      {/* CENTER — UNDO / REDO (Phase I.5) */}
      <div className="undo-redo-group">
        <button
          disabled
          className="undo-btn disabled"
          title="Undo"
        >
          Undo
        </button>
        <button
          disabled
          className="redo-btn disabled"
          title="Redo"
        >
          Redo
        </button>
      </div>

      {/* RIGHT */}
      <div className="project-status">Saved</div>
    </header>
  );
}

