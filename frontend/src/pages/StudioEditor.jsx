// frontend/src/pages/StudioEditor.jsx
import { useEffect, useState, useCallback, useMemo, useRef } from "react";

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
import {
  useSelection as useSelectionStore,
  clearSelection,
} from "../editor/selection/selectionStore";
import { resolveSelectedTarget } from "../editor/selection/resolveSelectedTarget";

// ✅ Tier 7.10 ADD (viewport picking stub) — keep as fallback
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

// ✅ Tier 6G.3 ADD (real Three.js viewer + picking)
import ThreeSceneViewer from "../editor/scene/ThreeSceneViewer";

// ✅ Tier 6G.6 ADD (scene layers + pick filters)
import SceneLayersPanel from "../editor/scene/SceneLayersPanel";

// ✅ Tier 6G.10 ADD (scene graph tree panel)
import SceneGraphPanel from "../editor/scene/SceneGraphPanel";

// ✅ Tier 7.28 ADD (Undo/Redo UI + local history)
import UndoRedoBar from "../editor/history/UndoRedoBar";
import { historyPush } from "../editor/history/historyStore";

// ✅ Tier 7.29 ADD (Snapshot History Graph Panel)
import SnapshotHistoryGraphPanel from "../editor/history/SnapshotHistoryGraphPanel";

// ✅ Tier 7.30 ADD (Snapshot Diff Preview Panel)
import SnapshotDiffPanel from "../editor/history/SnapshotDiffPanel";

// ✅ Tier 7.27/7.31 glue (clear ghost preview on snapshot change)
import { clearGizmoPreview } from "../editor/gizmo/gizmoPreviewStore";

// ✅ Tier 6S.1 ADD (telemetry viewer panel)
import TelemetryViewerPanel from "../editor/telemetry/TelemetryViewerPanel";

// ✅ Tier 6S.3 ADD (advanced telemetry overlay + toggles)
import TelemetryAdvancedPanel from "../editor/telemetry/TelemetryAdvancedPanel";

// ✅ Tier 6S.4 ADD (compare + summary + CSV export panel)
import TelemetryComparePanel from "../editor/telemetry/TelemetryComparePanel";

// ✅ Tier 6S.5 ADD (lab mode: scenarios + runs + compare matrix)
import TelemetryLabPanel from "../editor/telemetry/TelemetryLabPanel";

// ✅ Tier 6S.6 ADD (scenario templates + presets)
import ScenarioTemplatesPanel from "../editor/telemetry/ScenarioTemplatesPanel";

// ✅ Tier 6S.7 ADD (batch runner panel)
import BatchRunnerPanel from "../editor/telemetry/BatchRunnerPanel";

export default function StudioEditor() {
  const user = getCurrentUser();

  // 🔧 TEMPORARY (Phase J)
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);
  const [sceneStateHash, setSceneStateHash] = useState("__working__");

  // ✅ Tier 6G.1 ADD (scene index state)
  const [sceneIndex, setSceneIndex] = useState(null);
  const [sceneErr, setSceneErr] = useState(null);

  // ✅ Tier 7.28 ADD — allow overriding which snapshot is active (for history jumps)
  const [activeSnapshotOverrideId, setActiveSnapshotOverrideId] = useState(null);

  // ✅ Tier 6S.6 ADD — force refresh/re-mount of lab panel after scenario creation
  const [labRefreshKey, setLabRefreshKey] = useState(0);

  // ===============================
  // DIRTY STATE (EDITOR-LOCAL)
  // ===============================
  const [isDirty, setIsDirty] = useState(false);

  // ✅ Tier 7.1 ADD (legacy selection store)
  const sel = useSelection();

  // ✅ Tier 7.9 ADD (canonical selection state)
  const { selectedId } = useSelectionStore();

  // -------------------------------
  // ✅ Safety: avoid overlapping snapshot fetches
  // -------------------------------
  const snapshotsFetchInFlight = useRef(false);

  // =====================================================
  // SNAPSHOT FETCH (AUTHORITATIVE)
  // =====================================================
  const fetchSnapshots = useCallback(() => {
    // Prevent overlap (helps during rapid navigation / HMR / rerenders)
    if (snapshotsFetchInFlight.current) return Promise.resolve();
    snapshotsFetchInFlight.current = true;

    const token = getAccessToken?.();
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    return fetch(`http://127.0.0.1:8000/projects/${projectId}/snapshots/`, {
      headers,
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Snapshot fetch failed: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        console.log("Snapshots:", data);
        setSnapshots(Array.isArray(data) ? data : []);
      })
      .finally(() => {
        snapshotsFetchInFlight.current = false;
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

  // ✅ Tier 7.28 — if user navigated via undo/redo, honor override first
  const overrideSnapshot = activeSnapshotOverrideId
    ? snapshots.find((s) => s.id === activeSnapshotOverrideId)
    : null;

  const activeSnapshot = overrideSnapshot ?? (draftSnapshot ?? completedSnapshot);
  const isEditable = activeSnapshot?.status === "draft";

  // ✅ Tier 7.30 — find base snapshot (parent) for diff preview
  const baseSnapshot = useMemo(() => {
    if (!activeSnapshot?.parent_snapshot_id) return null;
    return (
      snapshots?.find((s) => s.id === activeSnapshot.parent_snapshot_id) || null
    );
  }, [activeSnapshot?.id, activeSnapshot?.parent_snapshot_id, snapshots]);

  // ✅ Tier 7.28 — whenever activeSnapshot changes, push into local history stack
  useEffect(() => {
    if (activeSnapshot?.id) historyPush(activeSnapshot.id);
  }, [activeSnapshot?.id]);

  // =====================================================
  // Tier 7.31 — SAFE SNAPSHOT NAVIGATION (UI-only)
  // =====================================================
  const navigateToSnapshot = useCallback(
    (id) => {
      const nextId = Number(id);
      if (!Number.isFinite(nextId)) return;

      // Clear volatile UI state (must never drift across snapshot boundaries)
      try {
        clearGizmoPreview?.();
      } catch {}
      try {
        clearSelection?.();
      } catch {}

      // allow jumping even if a draft exists
      setActiveSnapshotOverrideId(nextId);

      // keep snapshot list/status in sync after navigation
      fetchSnapshots().catch(console.error);
    },
    [fetchSnapshots]
  );

  // =====================================================
  // ✅ Tier 6G.8 — Deterministic rebind key (forces viewer remount)
  // =====================================================
  const sceneRebindKey = useMemo(() => {
    if (!activeSnapshot?.id) return "snap:none";
    return `snap:${activeSnapshot.id}`;
  }, [activeSnapshot?.id]);

  // =====================================================
  // ✅ Tier 6G.1 — Scene Index fetch (race-safe)
  // ✅ Tier 6G.8 — Enforce selection validity after snapshot switch
  // =====================================================
  useEffect(() => {
    if (!activeSnapshot?.id) return;

    const controller = new AbortController();

    setSceneErr(null);
    setSceneIndex(null);

    fetchScene(projectId, activeSnapshot.id, { signal: controller.signal })
      .then((idx) => {
        setSceneIndex(idx);

        // ✅ Tier 6G.8 selection validity:
        // if selectedId exists but its object_id is not present in the new scene, clear selection
        try {
          if (selectedId) {
            const objectId = String(selectedId).split("::")[0];
            const ids =
              (idx?.objects || [])
                .filter(Boolean)
                .map((o) => String(o.id || "").trim())
                .filter(Boolean) || [];

            if (!ids.includes(objectId)) {
              clearSelection?.();
            }
          }
        } catch {}
      })
      .catch((e) => {
        if (e?.name === "AbortError") return;
        setSceneErr(String(e?.message || e));
      });

    return () => controller.abort();
  }, [projectId, activeSnapshot?.id, selectedId]);

  // ✅ Tier 6G.2: allow attach panel to refresh the current snapshot’s scene index
  const refreshSceneIndex = useCallback(() => {
    if (!activeSnapshot?.id) return;

    const controller = new AbortController();

    setSceneErr(null);
    setSceneIndex(null);

    fetchScene(projectId, activeSnapshot.id, { signal: controller.signal })
      .then(setSceneIndex)
      .catch((e) => {
        if (e?.name === "AbortError") return;
        setSceneErr(String(e?.message || e));
      });

    return () => controller.abort();
  }, [projectId, activeSnapshot?.id]);

  // ✅ Tier 7.9 ADD (resolve active target deterministically)
  const { targetId: resolvedTargetId } = resolveSelectedTarget(
    activeSnapshot,
    selectedId
  );

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
  // RENDER  (⚠️ NO TIER BLOCKS MOVED/REMOVED)
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

            <SnapshotPreview
              snapshot={activeSnapshot}
              onDraftCreated={fetchSnapshots}
            />

            <FinalizeDraftButton
              snapshot={activeSnapshot}
              onFinalized={fetchSnapshots}
            />
          </>
        }
      >
        {/* ✅ Tier 7.10 layout: left tools, right viewport + editor host */}
        <div className="grid grid-cols-[360px_1fr] gap-3 p-3">
          {/* LEFT: tool controls */}
          <div className="space-y-3">
            {/* ✅ Tier 7.28 ADD (Undo/Redo bar) */}
            <div style={{ padding: 12 }}>
              <UndoRedoBar
                projectId={projectId}
                activeSnapshotId={activeSnapshot?.id}
                onNavigate={navigateToSnapshot}
              />
            </div>

            {/* ✅ Tier 7.29 ADD (Snapshot History Graph Panel) */}
            <div style={{ padding: 12 }}>
              <SnapshotHistoryGraphPanel
                activeSnapshotId={activeSnapshot?.id}
                onNavigate={navigateToSnapshot}
              />
            </div>

            {/* ✅ Tier 7.30 ADD (Snapshot Diff Preview Panel) */}
            <div style={{ padding: 12 }}>
              <SnapshotDiffPanel
                baseSnapshot={baseSnapshot}
                targetSnapshot={activeSnapshot}
              />
            </div>

            {/* ✅ Tier 6G.1 ADD (Scene Index debug panel) */}
            <div style={{ padding: 12 }}>
              {sceneErr ? (
                <div className="text-red-600 text-sm">{sceneErr}</div>
              ) : null}
              <SceneIndexPanel
                sceneIndex={sceneIndex}
                snapshotId={activeSnapshot?.id}
              />
            </div>

            {/* ✅ Tier 6G.6 ADD (Scene layers + pick filters + opacity) */}
            <div style={{ padding: 12 }}>
              <SceneLayersPanel sceneIndex={sceneIndex} />
            </div>

            {/* ✅ Tier 6G.10 ADD (Scene Graph tree panel) */}
            <div style={{ padding: 12 }}>
              <SceneGraphPanel sceneIndex={sceneIndex} />
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
            <div
              style={{
                padding: 12,
                display: "flex",
                gap: 10,
                alignItems: "center",
              }}
            >
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

                  // after commit, clear override so normal draft/complete selection rules apply again
                  setActiveSnapshotOverrideId(null);

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

            {/* ✅ Tier 6S.1 ADD (telemetry viewer panel) */}
            <div style={{ padding: 12 }}>
              <TelemetryViewerPanel activeSnapshot={activeSnapshot} />
            </div>

            {/* ✅ Tier 6S.3 ADD (advanced telemetry overlay + toggles) */}
            <div style={{ padding: 12 }}>
              <TelemetryAdvancedPanel />
            </div>

            {/* ✅ Tier 6S.4 ADD (telemetry compare + summary + CSV export) */}
            <div style={{ padding: 12 }}>
              <TelemetryComparePanel />
            </div>

            {/* ✅ Tier 6S.6 ADD (scenario templates + presets) */}
            <div style={{ padding: 12 }}>
              <ScenarioTemplatesPanel
                projectId={projectId}
                onCreated={() => setLabRefreshKey((k) => k + 1)}
              />
            </div>

            {/* ✅ Tier 6S.7 ADD (batch runner: N templates/scenarios -> N artifacts + runs) */}
            <div style={{ padding: 12 }}>
              <BatchRunnerPanel activeSnapshot={activeSnapshot} />
            </div>

            {/* ✅ Tier 6S.5 ADD (lab mode: scenarios + runs + compare matrix) */}
            <div style={{ padding: 12 }}>
              <TelemetryLabPanel
                key={`lab:${labRefreshKey}`}
                projectId={projectId}
                activeSnapshot={activeSnapshot}
              />
            </div>

            {/* ✅ Tier 7.2 ADD (read-only reference frames) */}
            <div style={{ padding: 12 }}>
              <ReferenceFramesPanel
                activeSnapshotId={activeSnapshot?.id}
                disabled={!isEditable}
              />
            </div>
          </div>

          {/* RIGHT: viewport + editor host */}
          <div className="space-y-3">
            {/* ✅ Tier 6G.8: key forces clean remount on snapshot change (prevents ghosting) */}
            <div style={{ padding: 12 }}>
              <ThreeSceneViewer
                key={sceneRebindKey}
                sceneIndex={sceneIndex}
                disabled={!activeSnapshot?.id}
              />
            </div>

            {/* ✅ Keep Tier 7.10 stub viewport as a fallback/debug surface */}
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
