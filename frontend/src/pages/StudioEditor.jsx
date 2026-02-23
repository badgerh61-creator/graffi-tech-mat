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

/* ✅ Tier 7.9 ADD (canonical selection store + resolver + overlay)
   - Alias import names to avoid clashing with Tier 7.1 useSelection().
*/
import SelectionOverlay from "../editor/selection/SelectionOverlay";
import { useSelection as useSelectionStore } from "../editor/selection/selectionStore";
import { resolveSelectedTarget } from "../editor/selection/resolveSelectedTarget";

export default function StudioEditor() {
  const user = getCurrentUser();

  // 🔧 TEMPORARY (Phase J)
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);
  const [sceneStateHash, setSceneStateHash] = useState("__working__");

  // ===============================
  // DIRTY STATE (EDITOR-LOCAL)
  // ===============================
  const [isDirty, setIsDirty] = useState(false);

  // ✅ Tier 7.1 ADD (selection store)
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
        {/* ✅ Tier 7.9 ADD (Selection overlay; additive, does not remove Tier 7.1 button) */}
        <div style={{ padding: 12 }}>
          <SelectionOverlay />
        </div>

        {/* ✅ Tier 7.1 ADD (temporary selection + toolbar) */}
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
              // refresh list so UI sees the new draft snapshot
              fetchSnapshots().catch(console.error);
            }}
          />
        </div>

        {/* ✅ Tier 7.2 ADD (read-only reference frames) */}
        <div style={{ padding: 12 }}>
          <ReferenceFramesPanel
            activeSnapshotId={activeSnapshot?.id}
            disabled={!isEditable}
          />
        </div>

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
      </EditorShell>
    </CapabilityProvider>
  );
}
