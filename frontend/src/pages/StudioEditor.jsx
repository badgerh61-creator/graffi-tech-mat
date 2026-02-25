// frontend/src/pages/StudioEditor.jsx

import { useEffect, useState, useCallback } from "react";

import EditorShell from "../app/EditorShell";
import EditorLayoutHost from "../layout/EditorLayoutHost";
import { CapabilityProvider } from "../capabilities";
import { getCurrentUser, getAccessToken } from "../utils/auth";

import SnapshotPreview from "../components/snapshots/SnapshotPreview";
import DraftStatusBadge from "../components/snapshots/DraftStatusBadge";
import FinalizeDraftButton from "../components/snapshots/FinalizeDraftButton";
import { useDraftAutosave } from "../hooks/useDraftAutosave";

// ✅ Tier 7.1 ADD (selection + transform toolbar)
import { useSelection } from "../editor/selection/useSelection";
import TransformToolbar from "../editor/tools/TransformToolbar";

// ✅ Tier 7.2 ADD (reference frames panel)
import ReferenceFramesPanel from "../editor/referenceFrames/ReferenceFramesPanel";

// ✅ Tier 7.8 ADD (gizmo commits via assistant proposals evaluate/apply)
import GizmoCommitController from "../editor/gizmo/GizmoCommitController";

/* ✅ Tier 7.9 ADD (canonical selection store + resolver)
   - Alias import names to avoid clashing with Tier 7.1 useSelection().
*/
import { useSelection as useSelectionStore } from "../editor/selection/selectionStore";
import { resolveSelectedTarget } from "../editor/selection/resolveSelectedTarget";

// ✅ Tier 7.10 ADD (viewport picking stub)
import ViewportSurface from "../editor/viewport/ViewportSurface";

// ✅ Tier 7.11 ADD (selection → tool payload binding panel)
import TransformToolPanel from "../editor/transform/TransformToolPanel";

// ✅ Tier 7.17 ADD (typed selection HUD)
import SelectionHud from "../editor/selection/SelectionHud";

// ✅ Tier 6G.1 ADD (scene index fetch + debug panel)
import { fetchScene } from "../services/studio/sceneApi";
import SceneIndexPanel from "../editor/scene/SceneIndexPanel";

// ✅ Tier 6G.2 ADD (attach asset panel)
import AttachAssetPanel from "../editor/scene/AttachAssetPanel";

export default function StudioEditor() {
  const user = getCurrentUser();

  // 🔧 TEMPORARY (Phase J)
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);
  const [sceneStateHash, setSceneStateHash] = useState("__working__");

  // ✅ Tier 6G.1 ADD (scene index state)
  const [sceneIndex, setSceneIndex] = useState(null);
  const [sceneErr, setSceneErr] = useState(null);

  // ===============================
  // DIRTY STATE (EDITOR-LOCAL)
  // ===============================
  const [isDirty, setIsDirty] = useState(false);

  // ✅ Tier 7.1 ADD (legacy selection store)
  const sel = useSelection();

  // ✅ Tier 7.9 ADD (canonical selection state)
  const { selectedId } = useSelectionStore();

  // =====================================================
  // SNAPSHOT FETCH (AUTHORITATIVE)
  // =====================================================
  const fetchSnapshots = useCallback(() => {
    const token = getAccessToken();

    return fetch(`http://127.0.0.1:8000/projects/${projectId}/snapshots/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Snapshot fetch failed: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Snapshots:", data);
        setSnapshots(data);
      });
  }, [projectId]);

  // =====================================================
  // INITIAL LOAD
  // =====================================================
  useEffect(() => {
    if (!projectId) return;
    fetchSnapshots().catch(console.error);
  }, [projectId, fetchSnapshots]);

  // =====================================================
  // PHASE 3 — SNAPSHOT SELECTION (MANDATORY)
  // =====================================================
  const draftSnapshot = snapshots.find((s) => s.status === "draft");
  const completedSnapshot = snapshots.find((s) => s.status === "completed");

  const activeSnapshot = draftSnapshot ?? completedSnapshot;
  const isEditable = activeSnapshot?.status === "draft";

  const refreshSceneIndex = useCallback(() => {
    if (!activeSnapshot?.id) return;

    setSceneErr(null);
    setSceneIndex(null);

    fetchScene(projectId, activeSnapshot.id)
      .then(setSceneIndex)
      .catch((e) => setSceneErr(String(e?.message || e)));
  }, [projectId, activeSnapshot?.id]);

  // ✅ Tier 6G.1 ADD (fetch scene index for active snapshot)
  useEffect(() => {
    refreshSceneIndex();
  }, [refreshSceneIndex]);

  // ✅ Tier 7.9 ADD (resolve active target deterministically)
  const { targetId: resolvedTargetId } = resolveSelectedTarget(activeSnapshot, selectedId);

  // =====================================================
  // TIER 7.8 — GIZMO GATE (TEMP stubs for lock/station)
  // =====================================================
  // ✅ Prefer Tier 7.9 resolved target; fallback to Tier 7.1 selection if still used by old UI.
  const activeTargetId = resolvedTargetId ?? sel.selectedId ?? null;

  const hasDraftLock = true; // TODO: replace with real lock state from Phase U UI
  const station = "geometry"; // TODO: replace when station state is visible in UI

  const gizmoEnabled =
    isEditable &&
    hasDraftLock &&
    station === "geometry" &&
    activeSnapshot?.status === "draft" &&
    !!activeTargetId;

  const gizmoReason = !activeTargetId
    ? "select a target"
    : !isEditable
    ? "insufficient role"
    : activeSnapshot?.status !== "draft"
    ? "snapshot not draft"
    : !hasDraftLock
    ? "draft lock required"
    : station !== "geometry"
    ? "wrong station"
    : null;

  // =====================================================
  // PHASE 4.4 — AUTOSAVE (DRAFT ONLY)
  // =====================================================
  useDraftAutosave({
    snapshot: activeSnapshot,
    sceneStateHash,
    isDirty,
    onSaved: () => setIsDirty(false),
  });

  // =====================================================
  // RENDER
  // =====================================================
  return (
    <CapabilityProvider role={user?.role ?? "viewer"}>
      <EditorShell
        headerRight={
          <>
            <DraftStatusBadge snapshot={activeSnapshot} />

            {/* ===============================
                UI INDICATOR (HEADER)
               =============================== */}
            {isDirty && (
              <span
                style={{
                  color: "#d33682",
                  marginLeft: 8,
                  fontSize: 12,
                }}
              >
                Unsaved changes
              </span>
            )}

            <SnapshotPreview snapshot={activeSnapshot} onDraftCreated={fetchSnapshots} />

            <FinalizeDraftButton snapshot={activeSnapshot} onFinalized={fetchSnapshots} />
          </>
        }
      >
        {/* ✅ Tier 7.10 layout: left tools, right viewport + editor host */}
        <div className="grid grid-cols-[360px_1fr] gap-3 p-3">
          {/* LEFT: tool controls */}
          <div className="space-y-3">
            {/* ✅ Tier 6G.1 ADD (Scene Index debug panel) */}
            <div style={{ padding: 12 }}>
              {sceneErr ? <div className="text-red-600 text-sm">{sceneErr}</div> : null}
              <SceneIndexPanel sceneIndex={sceneIndex} snapshotId={activeSnapshot?.id} />
            </div>

            {/* ✅ Tier 6G.2 ADD (Attach asset to object, then refresh scene) */}
            <div style={{ padding: 12 }}>
              <AttachAssetPanel
                projectId={projectId}
                snapshotId={activeSnapshot?.id}
                onAttached={refreshSceneIndex}
              />
            </div>

            {/* ✅ Tier 7.17 ADD (typed selection HUD) */}
            <div style={{ padding: 12 }}>
              <SelectionHud />
            </div>

            {/* ✅ Tier 7.1 ADD (temporary selection + toolbar) — kept additive-safe */}
            <div style={{ padding: 12, display: "flex", gap: 10, alignItems: "center" }}>
              <button onClick={() => sel.select("panel-1")}>Select panel-1</button>

              <TransformToolbar
                activeSnapshot={activeSnapshot}
                isEditable={isEditable}
                selectedId={sel.selectedId}
                onNewSnapshot={(newId) => {
                  console.log("New snapshot:", newId);
                  fetchSnapshots().catch(console.error);
                }}
              />
            </div>

            {/* ✅ Tier 7.8 ADD (gizmo commit wiring via /assistant/proposals/*) */}
            <div style={{ padding: 12 }}>
              <GizmoCommitController
                activeSnapshot={activeSnapshot}
                activeTargetId={activeTargetId}
                enabled={gizmoEnabled}
                reasonDisabled={gizmoReason}
                enablePreview={false} // set true only if /assistant/proposals/preview exists
                onApplied={(newId) => {
                  console.log("Applied new snapshot:", newId);
                  fetchSnapshots().catch(console.error);
                }}
              />
            </div>

            {/* ✅ Tier 7.11 ADD (transform tool panel binds target_id from selectionStore) */}
            <div style={{ padding: 12 }}>
              <TransformToolPanel
                activeSnapshot={activeSnapshot}
                disabled={!isEditable}
                onExecuted={(data) => {
                  console.log("Tool executed:", data);
                  fetchSnapshots().catch(console.error);
                }}
              />
            </div>

            {/* ✅ Tier 7.2 ADD (read-only reference frames) */}
            <div style={{ padding: 12 }}>
              <ReferenceFramesPanel activeSnapshotId={activeSnapshot?.id} disabled={!isEditable} />
            </div>
          </div>

          {/* RIGHT: viewport picking + editor host */}
          <div className="space-y-3">
            <ViewportSurface disabled={!activeSnapshot} />

            {/* ===============================
                SCENE CHANGE SIGNAL
               =============================== */}
            <EditorLayoutHost
              editable={isEditable}
              onSceneChange={() => {
                if (!isEditable) return;
                setSceneStateHash(Date.now().toString());
                setIsDirty(true);
              }}
            />
          </div>
        </div>
      </EditorShell>
    </CapabilityProvider>
  );
}
