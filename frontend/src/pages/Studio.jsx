// frontend/src/pages/Studio.jsx
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
import ShareModal from "../ui/ShareModal";
import {
  getInviteContext,
  clearInviteContext,
} from "../utils/inviteContext";

export default function Studio() {
  const sceneRef = useRef(null);
  const navigate = useNavigate();

  const undo = useHistoryStore((s) => s.undo);
  const redo = useHistoryStore((s) => s.redo);

  const activeModelId = useModelStore((s) => s.currentModelId);
  const modelPermissions = useModelStore((s) => s.modelPermissions);
  const modelStatus = useModelStore((s) => s.modelStatus);
  const loadModel = useModelStore((s) => s.openModel);

  const isReadOnly = !!modelPermissions?.isReadOnly;

  const [inviteInfo, setInviteInfo] = useState(null);
  const [showShare, setShowShare] = useState(false);

  const inviteHandledRef = useRef(false);

  /* ================= INVITE CONTEXT ================= */

  useEffect(() => {
    if (inviteHandledRef.current) return;

    const ctx = getInviteContext();
    if (!ctx) return;

    inviteHandledRef.current = true;
    setInviteInfo(ctx);

    if (ctx.modelId) loadModel(ctx.modelId);

    clearInviteContext();
  }, [loadModel]);

  /* ================= LOGOUT ================= */

  function handleLogout() {
    clearTokens();
    navigate("/login", { replace: true });
  }

  /* ================= STATUS TEXT ================= */

  const statusText =
    modelStatus === "loading"
      ? "Processing model…"
      : modelStatus === "failed"
      ? "Model failed to process"
      : isReadOnly
      ? "Read-only mode (viewer access)"
      : "Editing enabled";

  /* ================= RENDER ================= */

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col">
      <AppShortcuts undo={undo} redo={redo} />

      {inviteInfo && (
        <InviteBanner
          role={inviteInfo.role}
          onDismiss={() => setInviteInfo(null)}
        />
      )}

      {isReadOnly && (
        <div className="bg-amber-50 border-b px-4 py-2 text-sm text-amber-800">
          Viewer access — editing disabled
        </div>
      )}

      {/* ================= HEADER ================= */}
      <header className="flex items-center justify-between px-4 py-3 bg-white border-b">
        <h1 className="text-lg font-semibold">
          Graffi Studio — Ultra
        </h1>

        <div className="flex gap-2">
          {/* 🔒 SHARE — permission-aware */}
          <button
            disabled={!activeModelId || !modelPermissions?.canEdit}
            onClick={() => setShowShare(true)}
            className={`
              px-3 py-1 text-sm rounded text-white transition
              ${
                activeModelId && modelPermissions?.canEdit
                  ? "bg-slate-800 hover:bg-slate-700"
                  : "bg-slate-400 cursor-not-allowed"
              }
            `}
          >
            Share
          </button>

          <button
            onClick={handleLogout}
            className="px-3 py-1 text-sm bg-rose-600 text-white rounded hover:bg-rose-500"
          >
            Logout
          </button>
        </div>
      </header>

      {/* ================= MAIN ================= */}
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
            {isReadOnly ? (
              <div className="text-xs text-slate-500">
                Upload disabled
              </div>
            ) : (
              <UploadPanel />
            )}
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

      {/* ================= SHARE MODAL ================= */}
      {showShare && activeModelId && modelPermissions?.canEdit && (
        <ShareModal
          modelId={activeModelId}
          onClose={() => setShowShare(false)}
        />
      )}
    </div>
  );
}

