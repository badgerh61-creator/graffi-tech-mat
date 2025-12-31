// src/ui/Sidebar.jsx

import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useCapabilities } from "../capabilities/useCapabilities";

function SidebarItem({ to, label, enabled }) {
  const loc = useLocation();
  const isActive = loc.pathname === to;

  if (!enabled) {
    return (
      <div
        className="text-sm text-ui-muted cursor-not-allowed opacity-60"
        title="You do not have permission to use this section"
      >
        {label}
      </div>
    );
  }

  return (
    <Link
      to={to}
      className={`text-sm ${
        isActive ? "text-ui-accent" : "text-ui-text"
      }`}
    >
      {label}
    </Link>
  );
}

export default function Sidebar({ compact = false }) {
  const base = compact ? "w-16" : "w-56";
  const { has } = useCapabilities();

  const canViewDesign = has("design.view");
  const canViewStudio = canViewDesign; // Studio = Design workspace host
  const canViewViewer = has("viewer.view"); // future-facing

  return (
    <aside
      className={`${base} bg-ui-surface border-r border-ui-border p-3 transition-all`}
    >
      <div className="mb-6 font-semibold">Menu</div>

      <nav className="flex flex-col gap-2">
        <SidebarItem
          to="/studio"
          label="Studio"
          enabled={canViewStudio}
        />

        <SidebarItem
          to="/viewer"
          label="Viewer"
          enabled={canViewViewer}
        />
      </nav>
    </aside>
  );
}

