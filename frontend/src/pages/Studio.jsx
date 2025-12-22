import React, { useRef } from "react";
import { useNavigate } from "react-router-dom";

import SceneCanvas from "../engine/SceneCanvas";
import CanvasBoundary from "../engine/CanvasBoundary";
import UIPanel from "../ui/UIPanel";
import ModelLibrary from "../ui/ModelLibrary";
import UploadPanel from "../widgets/UploadPanel";

import { useHistoryStore } from "../store/historyStore";
import { clearToken } from "../utils/auth";
import AppShortcuts from "../AppShortcuts";

export default function Studio() {
  const sceneRef = useRef(null);
  const navigate = useNavigate();

  // ✅ Safe access (prevents white screen if store not ready)
  const undo = useHistoryStore?.((s) => s.undo) ?? (() => {});
  const redo = useHistoryStore?.((s) => s.redo) ?? (() => {});

  function handleLogout() {
    clearToken();
    navigate("/login", { replace: true });
  }

  return (
    <div className="studio-page min-h-screen bg-slate-100 flex flex-col">
      {/* Keyboard shortcuts */}
      <AppShortcuts undo={undo} redo={redo} />

      {/* ===== TOP BAR ===== */}
      <header className="flex items-center justify-between px-4 py-3 bg-white border-b">
        <h1 className="text-lg font-semibold">
          Graffi Studio — Ultra
        </h1>

        <button
          onClick={handleLogout}
          className="px-3 py-1 text-sm bg-rose-600 text-white rounded hover:bg-rose-700"
        >
          Logout
        </button>
      </header>

      {/* ===== MAIN CONTENT ===== */}
      <main
        className="flex-1 grid gap-3 p-3"
        style={{ gridTemplateColumns: "3fr 1fr" }}
      >
        {/* ===== CANVAS ===== */}
        <section className="bg-white rounded border overflow-hidden">
          <CanvasBoundary>
            <SceneCanvas ref={sceneRef} />
          </CanvasBoundary>
        </section>

        {/* ===== SIDEBAR ===== */}
        <aside className="space-y-3">
          <UIPanel title="Upload">
            <UploadPanel />
          </UIPanel>

          <UIPanel title="Models">
            <ModelLibrary />
          </UIPanel>

          <UIPanel title="Status">
            <div className="text-sm text-slate-600">
              Studio loaded successfully.
            </div>
          </UIPanel>
        </aside>
      </main>
    </div>
  );
}

