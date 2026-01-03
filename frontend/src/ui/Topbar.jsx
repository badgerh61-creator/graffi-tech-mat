// src/ui/Topbar.jsx

import React from "react";

export default function Topbar({
  onToggleTheme,
  onToggleZen,
  onToggleFull,
}) {
  return (
    <header className="h-12 flex items-center justify-between px-4 border-b border-ui-border bg-ui-surface/70 backdrop-blur">
      
      {/* LEFT */}
      <div className="font-bold">Graffi Studio</div>

      {/* CENTER — UNDO / REDO (PHASE I.5) */}
      <div className="flex items-center gap-1">
        <button
          disabled
          title="Undo"
          className="px-2 py-1 rounded opacity-40 cursor-not-allowed"
        >
          Undo
        </button>
        <button
          disabled
          title="Redo"
          className="px-2 py-1 rounded opacity-40 cursor-not-allowed"
        >
          Redo
        </button>
      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-2">
        <button
          className="px-2 py-1 rounded hover:bg-ui-buttonHover"
          onClick={onToggleZen}
        >
          Zen
        </button>
        <button
          className="px-2 py-1 rounded hover:bg-ui-buttonHover"
          onClick={onToggleFull}
        >
          Full
        </button>
        <button
          className="px-2 py-1 rounded hover:bg-ui-buttonHover"
          onClick={onToggleTheme}
        >
          Theme
        </button>
      </div>
    </header>
  );
}

