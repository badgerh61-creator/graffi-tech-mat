// src/ui/Sidebar.jsx
import React from "react";
import { Link, useLocation } from "react-router-dom";

export default function Sidebar({ compact = false }) {
  const base = compact ? "w-16" : "w-56";
  const loc = useLocation();

  return (
    <aside className={`${base} bg-ui-surface border-r border-ui-border p-3 transition-all`}>
      <div className="mb-6 font-semibold">Menu</div>
      <nav className="flex flex-col gap-2">
        <Link to="/studio" className={`text-sm ${loc.pathname === "/studio" ? "text-ui-accent" : ""}`}>Studio</Link>
        <Link to="/viewer" className={`text-sm ${loc.pathname === "/viewer" ? "text-ui-accent" : ""}`}>Viewer</Link>
      </nav>
    </aside>
  );
}
