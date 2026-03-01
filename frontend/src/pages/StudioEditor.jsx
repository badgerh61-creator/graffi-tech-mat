// frontend/src/pages/StudioEditor.jsx
import { useEffect, useState, useCallback, useMemo, useRef } from "react";

import EditorShell from "../app/EditorShell";
import EditorLayoutHost from "../layout/EditorLayoutHost";
import { CapabilityProvider } from "../capabilities";
import { getCurrentUser, getAccessToken } from "../utils/auth";

import SnapshotPreview from "../components/snapshots/SnapshotPreview";
import DraftStatusBadge from "../components/snapshots/DraftStatusBadge";
import { useDraftAutosave } from "../hooks/useDraftAutosave";

// ✅ Tier 7.35 ADD (READ ↔ EDIT mode bar)
import StudioModeBar from "../editor/modes/StudioModeBar";

// ✅ Tier 7.36 ADD (session header + lock status + reasons)
import EditSessionHeader from "../editor/modes/EditSessionHeader";
import { fetchDraftLockStatus } from "../services/studio/lockStatusApi";
import { useLockStatus, setLockStatus } from "../editor/modes/lockStatusStore";

// ✅ Tier 7.39 ADD (tool context bar)
import ToolContextBar from "../editor/toolbar/ToolContextBar";

// ✅ Tier 7.40 ADD (view modes dropdown)
import ViewModeSelect from "../editor/view/ViewModeSelect";

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

// ✅ Tier 6G.11 ADD (material override panel)
import MaterialOverridesPanel from "../editor/materials/MaterialOverridesPanel";

// ✅ Tier 7.42 ADD (material inspector: read + governed edit)
import MaterialInspectorPanel from "../editor/materials/MaterialInspectorPanel";

// ✅ Tier 7.43 ADD (paint params: color/roughness/metalness/opacity)
import PaintParamsPanel from "../editor/materials/PaintParamsPanel";

// ✅ Tier 7.28 ADD (Undo/Redo UI + local history)
import UndoRedoBar from "../editor/history/UndoRedoBar";
import { historyPush } from "../editor/history/historyStore";

// ✅ Tier 7.29 ADD (Snapshot History Graph Panel)
import SnapshotHistoryGraphPanel from "../editor/history/SnapshotHistoryGraphPanel";

// ✅ Tier 7.30 ADD (Snapshot Diff Preview Panel)
import SnapshotDiffPanel from "../editor/history/SnapshotDiffPanel";

// ✅ Tier 7.27/7.31 glue (clear ghost preview on snapshot change)
import { clearGizmoPreview } from "../editor/gizmo/gizmoPreviewStore";

// ✅ Tier 7.38/7.31 glue (clear decal preview + active decal on snapshot change)
import { clearAllDecalPreview } from "../editor/decals/decalPreviewStore";
import { clearActiveDecalId } from "../editor/decals/activeDecalStore";

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

const LOCK_POLL_MS = 1500;

function normalizeLock(data) {
  // Canonical: { state: "owned"|"taken"|"missing"|"unknown", owner_id?, owner_name? }
  if (!data) return { state: "unknown" };
  if (data.state) return data;

  // tolerant normalization for other backend shapes
  if (data.owned === true || data.is_owner === true) return { state: "owned" };
  if (data.owner_id != null)
    return { state: "taken", owner_id: data.owner_id, owner_name: data.owner_name };
  if (data.locked === false || data.exists === false) return { state: "missing" };

  return { state: "unknown" };
}

const WHY_ORDER = [
  "SNAPSHOT_MISSING",
  "LOADING",
  "NOT_DRAFT",
  "NO_LOCK",
  "ROLE_FORBIDDEN",
  "STATION_FORBIDDEN",
];

function sortWhy(rs) {
  const s = new Set(rs || []);
  return WHY_ORDER.filter((k) => s.has(k));
}

export default function StudioEditor() {
  const user = getCurrentUser();

  // 🔧 TEMPORARY (Phase J)
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);
  const [sceneStateHash, setSceneStateHash] = useState("__working__");

  // ✅ Tier 6G.1 ADD (scene index state)
  const [sceneIndex, setSceneIndex] = useState(null);
  const [sceneErr, setSceneErr] = useState(null);

  // ✅ Tier 7.28 ADD — allow overriding which snapshot is active (for history jumps + mode transitions)
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

  // ✅ Tier 7.36 ADD (lock status store)
  const { lock } = useLockStatus();

  // -------------------------------
  // ✅ Safety: avoid overlapping snapshot fetches
  // -------------------------------
  const snapshotsFetchInFlight = useRef(false);

  // ✅ Safety: avoid updating state after unmount for async snapshot fetch
  const aliveRef = useRef(true);
  useEffect(() => {
    aliveRef.current = true;
    return () => {
      aliveRef.current = false;
    };
  }, []);

  // =====================================================
  // SNAPSHOT FETCH (AUTHORITATIVE)
  // =====================================================
  const fetchSnapshots = useCallback(() => {
    if (snapshotsFetchInFlight.current) return Promise.resolve();
    snapshotsFetchInFlight.current = true;

    const token = getAccessToken?.();
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    return fetch(`http://127.0.0.1:8000/projects/${projectId}/snapshots/`, { headers })
      .then((res) => {
        if (!res.ok) throw new Error(`Snapshot fetch failed: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        if (!aliveRef.current) return;
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

  // ✅ Tier 7.28 — if user navigated via undo/redo/mode change, honor override first
  const overrideSnapshot = activeSnapshotOverrideId
    ? snapshots.find((s) => s.id === activeSnapshotOverrideId)
    : null;

  const activeSnapshot = overrideSnapshot ?? (draftSnapshot ?? completedSnapshot);

  // ✅ Tier 7.35 — READ ↔ EDIT is derived from snapshot truth:
  // EDIT == draft snapshot (tools/gizmo only allowed here)
  const isEditMode = activeSnapshot?.status === "draft";
  const isEditable = isEditMode; // keep existing variable name for additive safety

  // ✅ Tier 7.30 — find base snapshot (parent) for diff preview
  const baseSnapshot = useMemo(() => {
    if (!activeSnapshot?.parent_snapshot_id) return null;
    return snapshots?.find((s) => s.id === activeSnapshot.parent_snapshot_id) || null;
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
        clearAllDecalPreview?.();
      } catch {}
      try {
        clearActiveDecalId?.();
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
        try {
          if (selectedId) {
            const left = String(selectedId).split("::")[0];
            const baseObjectId = String(left).split("@")[0];

            const ids =
              (idx?.objects || [])
                .filter(Boolean)
                .map((o) => String(o.id || "").trim())
                .filter(Boolean) || [];

            if (!ids.includes(baseObjectId)) {
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
  const { targetId: resolvedTargetId } = resolveSelectedTarget(activeSnapshot, selectedId);

  // =====================================================
  // ✅ Tier 7.37 ADD (viewer should always have decor_state)
  // If sceneIndex endpoint doesn’t include decor_state yet, we stitch it in
  // from the authoritative snapshot. (UI-only merge; no writes.)
  // =====================================================
  const sceneIndexForViewer = useMemo(() => {
    if (!sceneIndex) return sceneIndex;
    const decor_state =
      sceneIndex?.decor_state ??
      activeSnapshot?.decor_state ??
      activeSnapshot?.body_state?.decor_state ??
      null;

    // If nothing to merge, keep original reference.
    if (decor_state == null) return sceneIndex;

    return { ...sceneIndex, decor_state };
  }, [sceneIndex, activeSnapshot?.id]);

  // =====================================================
  // ✅ Tier 6G.11 / Tier 7.42 — material overrides (authoritative)
  // Prefer decor_state.material_overrides; fallback to legacy body_state material_overrides
  // =====================================================
  const materialOverrides = useMemo(() => {
    return (
      activeSnapshot?.decor_state?.material_overrides ??
      activeSnapshot?.body_state?.material_overrides ??
      {}
    );
  }, [activeSnapshot?.id]);

  // =====================================================
  // ✅ Tier 7.36 — Lock status polling (draft only)
  // =====================================================
  useEffect(() => {
    let alive = true;
    let t = null;

    async function tick() {
      if (!activeSnapshot?.id) return;

      // lock status only meaningful for draft snapshots
      if (activeSnapshot.status !== "draft") {
        setLockStatus({ state: "unknown" });
        return;
      }

      try {
        const token = getAccessToken?.();
        const data = await fetchDraftLockStatus({
          snapshotId: activeSnapshot.id,
          getAccessToken: () => token,
        });
        if (!alive) return;
        setLockStatus(normalizeLock(data));
      } catch {
        if (!alive) return;
        setLockStatus({ state: "unknown" });
      }
    }

    tick();
    t = setInterval(tick, LOCK_POLL_MS);

    return () => {
      alive = false;
      if (t) clearInterval(t);
    };
  }, [activeSnapshot?.id, activeSnapshot?.status]);

  // =====================================================
  // TIER 7.8 — GIZMO GATE (now uses lock status)
  // =====================================================
  // ✅ Prefer Tier 7.9 resolved target; fallback to Tier 7.1 selection if still used by old UI.
  const activeTargetId = resolvedTargetId ?? sel.selectedId ?? null;

  // ✅ Tier 7.36: real lock state (owned => edit allowed)
  const hasDraftLock = lock?.state === "owned";

  // TODO: replace when station state is visible in UI
  const station = "geometry";

  // simple role gate (additive-safe; can be replaced by real capabilities)
  const canEditByRole = (user?.role ?? "viewer") !== "viewer";
  const canEditByStation = station === "geometry";

  const toolsEnabled =
    isEditMode &&
    hasDraftLock &&
    canEditByRole &&
    canEditByStation &&
    activeSnapshot?.status === "draft";

  const gizmoEnabled = toolsEnabled && !!activeTargetId;

  const gizmoReason = !activeTargetId
    ? "select a target"
    : !isEditMode
    ? "studio in READ mode"
    : activeSnapshot?.status !== "draft"
    ? "snapshot not draft"
    : !hasDraftLock
    ? "draft lock required"
    : !canEditByRole
    ? "role forbidden"
    : !canEditByStation
    ? "wrong station"
    : null;

  // ✅ Tier 7.36/7.39: deterministic why-blocked reasons
  const whyBlockedReasons = useMemo(() => {
    const rs = [];

    if (!activeSnapshot?.id) rs.push("SNAPSHOT_MISSING");
    if (sceneIndex == null && !!activeSnapshot?.id) rs.push("LOADING");

    if (activeSnapshot?.id && activeSnapshot?.status !== "draft") rs.push("NOT_DRAFT");

    if (activeSnapshot?.status === "draft") {
      if (lock?.state !== "owned") rs.push("NO_LOCK");
    }

    if (!canEditByRole) rs.push("ROLE_FORBIDDEN");
    if (!canEditByStation) rs.push("STATION_FORBIDDEN");

    return sortWhy(rs);
  }, [
    activeSnapshot?.id,
    activeSnapshot?.status,
    sceneIndex,
    lock?.state,
    canEditByRole,
    canEditByStation,
  ]);

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
  // Commit helper (shared by panels like MaterialInspector / PaintParamsPanel)
  // =====================================================
  const commitToolPayload = useCallback(
    async (payload) => {
      // Reuse GizmoCommitController pattern indirectly by emitting through it if you have a bus.
      // If you already have a central "toolExecutionAdapter", wire it here.
      // For now, keep this additive-safe: just log to avoid breaking runtime.
      console.log("commitToolPayload:", payload);
    },
    []
  );

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
              <span style={{ color: "#d33682", marginLeft: 8, fontSize: 12 }}>
                Unsaved changes
              </span>
            )}

            <SnapshotPreview snapshot={activeSnapshot} onDraftCreated={fetchSnapshots} />
          </>
        }
      >
        {/* ✅ Tier 7.36 — Session header (mode + lock + reasons) */}
        <div className="p-3 pt-3 pb-0">
          <EditSessionHeader
            project={{ id: projectId, name: "Project" }}
            activeSnapshot={activeSnapshot}
            lockStatus={lock}
            loading={sceneIndex == null && !!activeSnapshot?.id}
            canEditByRole={canEditByRole}
            canEditByStation={canEditByStation}
          />
        </div>

        {/* ✅ Tier 7.39/7.40 — Tool Context Bar + View Modes */}
        <div className="p-3 pt-2 pb-0 flex items-center gap-2">
          <div className="flex-1">
            <ToolContextBar
              canEdit={toolsEnabled}
              reasons={whyBlockedReasons}
              lockLabelText={lock?.state === "owned" ? "LOCK: Owned" : ""}
            />
          </div>
          <ViewModeSelect />
        </div>

        {/* ✅ Tier 7.35 — Mode bar (READ ↔ EDIT) */}
        <div className="p-3 pt-2 pb-0">
          <StudioModeBar
            activeSnapshot={activeSnapshot}
            onSetActiveSnapshotId={(id) => {
              // Use canonical navigation so selection/ghost never carries over
              navigateToSnapshot(id);
            }}
          />
        </div>

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
              <SnapshotDiffPanel baseSnapshot={baseSnapshot} targetSnapshot={activeSnapshot} />
            </div>

            {/* ✅ Tier 6G.1 ADD (Scene Index debug panel) */}
            <div style={{ padding: 12 }}>
              {sceneErr ? <div className="text-red-600 text-sm">{sceneErr}</div> : null}
              <SceneIndexPanel sceneIndex={sceneIndex} snapshotId={activeSnapshot?.id} />
            </div>

            {/* ✅ Tier 6G.6 ADD (Scene layers + pick filters + opacity) */}
            <div style={{ padding: 12 }}>
              <SceneLayersPanel sceneIndex={sceneIndex} />
            </div>

            {/* ✅ Tier 6G.10 ADD (Scene Graph tree panel) */}
            <div style={{ padding: 12 }}>
              <SceneGraphPanel sceneIndex={sceneIndex} />
            </div>

            {/* ✅ Tier 6G.11 ADD (Material Overrides list panel) */}
            <div style={{ padding: 12 }}>
              <MaterialOverridesPanel snapshot={activeSnapshot} />
            </div>

            {/* ✅ Tier 7.42 ADD (Material Inspector: read + governed edit) */}
            <div style={{ padding: 12 }}>
              <MaterialInspectorPanel
                snapshot={activeSnapshot}
                canEdit={toolsEnabled}
                onCommitTool={(payload) => {
                  // If you already have a real commit path, wire it here:
                  // toolExecutionAdapter.evaluate/apply OR your GizmoCommitController bridge.
                  commitToolPayload(payload);
                }}
              />
            </div>

            {/* ✅ Tier 7.43 ADD (Paint Params: color/roughness/metalness/opacity) */}
            <div style={{ padding: 12 }}>
              <PaintParamsPanel
                snapshot={activeSnapshot}
                canEdit={toolsEnabled}
                onCommitTool={(payload) => {
                  commitToolPayload(payload);
                }}
              />
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
                disabled={!toolsEnabled}
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
                disabled={false} // read-only panel; safe in READ
              />
            </div>
          </div>

          {/* RIGHT: viewport + editor host */}
          <div className="space-y-3">
            {/* ✅ Tier 6G.8: key forces clean remount on snapshot change (prevents ghosting) */}
            <div style={{ padding: 12 }}>
              <ThreeSceneViewer
                key={sceneRebindKey}
                sceneIndex={sceneIndexForViewer} // ✅ Tier 7.37 merge decor_state if needed
                materialOverrides={materialOverrides} // ✅ Tier 6G.11 / 7.42
                disabled={!activeSnapshot?.id}
                canEdit={toolsEnabled} // ✅ draft + lock + role + station
              />
            </div>

            {/* ✅ Keep Tier 7.10 stub viewport as a fallback/debug surface */}
            <ViewportSurface disabled={!activeSnapshot} />

            {/* ===============================
                SCENE CHANGE SIGNAL
               =============================== */}
            <EditorLayoutHost
              editable={isEditMode}
              onSceneChange={() => {
                if (!isEditMode) return;
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
