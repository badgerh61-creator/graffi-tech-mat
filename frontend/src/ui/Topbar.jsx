// src/ui/Topbar.jsx
import React from "react";

export default function Topbar({ onToggleTheme, onToggleZen, onToggleFull }) {
  return (
    <header className="h-12 flex items-center justify-between px-4 border-b border-ui-border bg-ui-surface/70 backdrop-blur">
      <div className="font-bold">Graffi Studio</div>
      <div className="flex items-center gap-2">
        <button className="px-2 py-1 rounded hover:bg-ui-buttonHover" onClick={onToggleZen}>Zen</button>
        <button className="px-2 py-1 rounded hover:bg-ui-buttonHover" onClick={onToggleFull}>Full</button>
        <button className="px-2 py-1 rounded hover:bg-ui-buttonHover" onClick={onToggleTheme}>Theme</button>
      </div>
    </header>
  );
}
