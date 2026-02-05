// frontend/src/app/EditorShell.jsx

import React from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

import ConstraintPanel from "../editor/panels/ConstraintPanel";
import { useConstraints } from "../editor/kernel/useConstraints";

export default function EditorShell({ children, headerRight }) {
  const { constraints } = useConstraints();

  return (
    <div className="editor-shell">
      <Topbar rightSlot={headerRight} />

      <div className="editor-body">
        <Sidebar />

        <main className="editor-main">
          {/* 🔒 Tier 2.2 — Read-only constraint awareness */}
          <ConstraintPanel constraints={constraints} />

          {children}
        </main>
      </div>
    </div>
  );
}

