// frontend/src/app/EditorShell.jsx

import React from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

import ConstraintPanel from "../editor/panels/ConstraintPanel";
import { useConstraints } from "../editor/kernel/useConstraints";

/* 🆕 Tier 2.3 — Graph-aware history */
import HistoryPanel from "../editor/panels/HistoryPanel";
import SnapshotHistoryGraph from "@/editor/history/SnapshotHistoryGraph";
import { useSnapshotHistory } from "@/editor/kernel/useSnapshotHistory";

export default function EditorShell({
  children,
  headerRight,

  /* 🧪 injected by tests / tooling */
  history: injectedHistory,
  activeSnapshotId: injectedActiveSnapshotId,
  onNavigate: injectedNavigate,
}) {
  const { constraints } = useConstraints();

  /* 🔒 Tier 2.3 — kernel-backed snapshot history */
  const kernelHistory = useSnapshotHistory();

  const history = injectedHistory ?? kernelHistory.history;
  const activeSnapshotId =
    injectedActiveSnapshotId ?? kernelHistory.activeSnapshotId;
  const navigateTo = injectedNavigate ?? kernelHistory.navigateTo;

  return (
    <div className="editor-shell">
      <Topbar rightSlot={headerRight} />

      <div className="editor-body">
        <Sidebar />

        <main className="editor-main">
          {/* 🔒 Tier 2.2 — Read-only constraint awareness */}
          <ConstraintPanel constraints={constraints} />

          {/* 🔒 Tier 2.3 — Read-only undo / redo (graph-aware) */}
          {history?.length > 0 && (
            <HistoryPanel
              history={history}
              activeSnapshotId={activeSnapshotId}
              onNavigate={navigateTo}
            />
          )}

          {children}
        </main>
      </div>
    </div>
  );
}

