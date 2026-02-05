// frontend/src/app/Topbar.jsx

import React from "react";

export default function Topbar({ rightSlot }) {
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
      <div
        className="topbar-right"
        style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        <div className="project-status">Saved</div>
        {rightSlot}
      </div>
    </header>
  );
}

