// src/pages/Studio.jsx
import React, { useRef, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import SceneCanvas from "../engine/SceneCanvas";
import CanvasBoundary from "../engine/CanvasBoundary";
import UIPanel from "../ui/UIPanel";
import ModelLibrary from "../ui/ModelLibrary";
import UploadPanel from "../widgets/UploadPanel";
import ActivityFeed from "../ui/ActivityFeed";

import { useHistoryStore } from "../store/historyStore";
import { useModelStore } from "../store/modelStore";
import { clearTokens } from "../utils/auth";
import AppShortcuts from "../AppShortcuts";

import InviteBanner from "../ui/InviteBanner";
import {
  getInviteContext,
  clearInviteContext,
} from "../utils/inviteContext";

export default function Studio() {
  const sceneRef = useRef(null);
  const navigate = useNavigate();

  const undo = useHistoryStore?.((s) => s.undo) ?? (() => {});
  const redo = useHistoryStore?.((s) => s.redo) ?? (() => {});

  const permissions = useModelStore((s) => s.modelPermissions);
  const modelStatus = useModelStore((s) => s.modelStatus);

  const selectModel =
    useModelStore((s) => s.selectModel) ??
    useModelStore((s) => s.loadModel) ??
    useModelStore((s) => s.setActiveModel);

  const [inviteInfo, setInviteInfo] = useState(null);

  useEffect(() => {
    const ctx = getInviteContext();
    if (!ctx) return;

    setInviteInfo(ctx);

    if (ctx.modelId && selectModel) {
      selectModel(ctx.modelId);
    }

    clearInviteContext();
  }, [selectModel]);

  function handleLogout() {
    clearTokens();
    navigate("/login", { replace: true });
  }

  const statusText =
    modelStatus === "loading"
      ? "Processing model…"
      : modelStatus === "failed"
      ? "Model failed to process"
      : permissions.isReadOnly
      ? "Read-only mode"
      : "Editing enabled";

  return (
    <div className="studio-page min-h-screen bg-slate-100 flex flex-col">
      <AppShortcuts undo={undo} redo={redo} />

      {/* 🔵 ADD: dismissable invite banner */}
      {inviteInfo && (
        <InviteBanner
          role={inviteInfo.role}
          onDismiss={() => setInviteInfo(null)}
        />
      )}

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

      <main
        className="flex-1 grid gap-3 p-3"
        style={{ gridTemplateColumns: "3fr 1fr" }}
      >
        <section className="bg-white rounded border overflow-hidden">
          <CanvasBoundary>
            <SceneCanvas ref={sceneRef} />
          </CanvasBoundary>
        </section>

        <aside className="space-y-3">
          <UIPanel title="Upload">
            <UploadPanel />
          </UIPanel>

          <UIPanel title="Models">
            <ModelLibrary />
          </UIPanel>

          <UIPanel title="Status">
            <div className="text-sm text-slate-600">
              {statusText}
            </div>
          </UIPanel>

          <UIPanel title="Activity">
            <ActivityFeed />
          </UIPanel>
        </aside>
      </main>
    </div>
  );
}

