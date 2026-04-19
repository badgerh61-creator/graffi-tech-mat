// frontend/src/pages/StudioEditor.jsx
import { API_BASE } from "../config/apiBase";

import React, {
  useEffect,
  useState,
  useCallback,
  useMemo,
  useRef,
  Suspense,
} from "react";

import EditorShell from "../app/EditorShell";
import EditorLayoutHost from "../layout/EditorLayoutHost";
import { CapabilityProvider } from "../capabilities";
import { getAccessToken, fetchCurrentUser } from "../utils/auth";

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

// ✅ Tier 7.45 ADD (HDR studio lighting controls)
import LightingControls from "../editor/view/LightingControls";

// ✅ Tier 7.48 ADD (camera toolbar)
import CameraToolbar from "../editor/camera/CameraToolbar";

// ✅ Tier 7.1 ADD (selection + transform toolbar)
import { setSelectedId } from "../editor/selection/selectionStore";
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

// ✅ Tier 7.60 ADD (clear single + multi-select together)
import { clearAllSelectionState } from "../editor/selection/multiSelectionBridge";

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

// ✅ 6G.6 ADD (scene layers + pick filters)
import SceneLayersPanel from "../editor/scene/SceneLayersPanel";

// ✅ Tier 7.62 — Marquee overlay (box select UI)
import MarqueeOverlay from "../editor/selection/MarqueeOverlay";

// ✅ 6G.10 ADD (scene graph tree panel)
import SceneGraphPanel from "../editor/scene/SceneGraphPanel";

// ✅ 6G.11 ADD (material override panel)
import MaterialOverridesPanel from "../editor/materials/MaterialOverridesPanel";

// ✅ Tier 7.42 ADD (material inspector: read + governed edit)
import MaterialInspectorPanel from "../editor/materials/MaterialInspectorPanel";

// ✅ Tier 7.43 ADD (paint params: color/roughness/metalness/opacity)
import PaintParamsPanel from "../editor/materials/PaintParamsPanel";

// ✅ Tier 7.44 ADD (decal asset browser)
import DecalAssetBrowserPanel from "../editor/decals/DecalAssetBrowserPanel";

// ✅ Tier 7.46 ADD (model asset picker)
import ModelAssetPickerPanel from "../editor/assets/ModelAssetPickerPanel";

// ✅ Tier 7.47 ADD (scene outliner)
import SceneOutlinerPanel from "../editor/outliner/SceneOutlinerPanel";

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

// ✅ NEW (additive-safe): central governed tool execution adapter
import { executeTool } from "../services/studio/toolExecutionAdapter";

// ✅ Tier 7.50 ADD (duplicate / mirror)
import ObjectActionsPanel from "../editor/outliner/ObjectActionsPanel";

// ✅ Tier 7.51 ADD (hierarchical outliner tree)
import SceneOutlinerTreePanel from "../editor/outliner/SceneOutlinerTreePanel";

// ✅ Tier 7.66 ADD (history-timeline)
import { historyUndo, historyRedo } from "../editor/history/historyStore";

// ✅ Tier 7.67 (keyboard shortcuts)
import { useKeyboardShortcuts } from "../editor/input/useKeyboardShortcuts";
import { setGizmoMode } from "../editor/gizmo/gizmoModeStore";

// ✅ Tier 7.75 (bootstrapEditSession)
import { bootstrapEditSession } from "../editor/session/bootstrapEditSession";

const LOCK_POLL_MS = 1500;

// ------------------------------------------------------
// Optional late-tier module loader (safe if files are absent)
// ------------------------------------------------------

const optionalJsxModules = import.meta.glob("../editor/**/*.jsx");
const optionalJsModules = import.meta.glob("../editor/**/*.js", { eager: true });

function optionalLazy(path, FallbackComponent) {
  const loader = optionalJsxModules[path];
  return React.lazy(
    loader
      ? loader
      : async () => ({
          default: FallbackComponent,
        })
  );
}

function PanelSuspense({ children }) {
  return <Suspense fallback={null}>{children}</Suspense>;
}

// ------------------------------------------------------
// Safe fallbacks for later-tier files that may not exist yet
// ------------------------------------------------------

function MaterialSlotInspectorPanelFallback(props) {
  return <MaterialInspectorPanel {...props} />;
}

function DecalPlacementPanelFallback() {
  return (
    <div className="border rounded p-3 text-xs opacity-70">
      Decal placement controls are not mounted yet in this repo state.
    </div>
  );
}

function PaintLibraryPanelFallback(props) {
  return <PaintParamsPanel {...props} />;
}

function VariantSetsPanelFallback() {
  return (
    <div className="border rounded p-3 text-xs opacity-70">
      Variant sets panel is not mounted yet in this repo state.
    </div>
  );
}

function AssetPlacementPalettePanelFallback(props) {
  return <ModelAssetPickerPanel {...props} />;
}

function ConstraintBlockedBannerFallback() {
  return null;
}

function ConstraintViolationsPanelFallback({
  violations = [],
  constraints = [],
}) {
  const list =
    Array.isArray(violations) && violations.length ? violations : constraints;

  if (!list.length) return null;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Constraints</div>
      {list.map((c, i) => (
        <div
          key={`${c?.constraint_id || "c"}:${i}`}
          className="border rounded p-2 text-xs"
        >
          <div className="font-semibold">{c?.kind || "constraint"}</div>
          <div className="opacity-80">
            {c?.message || "Constraint feedback available."}
          </div>
        </div>
      ))}
    </div>
  );
}

function BulkObjectActionsPanelFallback() {
  return (
    <div className="border rounded p-3 text-xs opacity-70">
      Bulk multi-select actions are not mounted yet in this repo state.
    </div>
  );
}

function UnifiedInspectorPanelFallback({
  snapshot,
  toolsEnabled,
  lockState,
  onCommitTool,
  constraints,
  setActivePaint,
}) {
  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Inspector</div>

      <div className="border rounded p-3 space-y-1 text-xs opacity-80">
        <div>
          Snapshot: <span className="font-mono">{snapshot?.id ?? "—"}</span>
        </div>
        <div>
          Status: <span className="font-mono">{snapshot?.status ?? "—"}</span>
        </div>
        <div>
          Edit:{" "}
          <span className="font-mono">
            {toolsEnabled ? "enabled" : "blocked"}
          </span>
        </div>
        <div>
          Lock: <span className="font-mono">{lockState || "unknown"}</span>
        </div>
      </div>

      <ObjectActionsPanel canEdit={toolsEnabled} onCommitTool={onCommitTool} />

      <MaterialInspectorPanel
        snapshot={snapshot}
        canEdit={toolsEnabled}
        onCommitTool={onCommitTool}
      />

      <MaterialSlotInspectorPanel
        snapshot={snapshot}
        canEdit={toolsEnabled}
        onCommitTool={onCommitTool}
      />

      <PaintParamsPanel
        snapshot={snapshot}
        canEdit={toolsEnabled}
        onCommitTool={onCommitTool}
        onApplyPaint={(preset) => {
          console.log("🎨 ACTIVE PAINT SET (PARAMS):", preset);
          setActivePaint(preset);
        }}
      />

      <ConstraintViolationsPanel constraints={constraints} />
    </div>
  );
}

// ------------------------------------------------------
// Optional late-tier component aliases
// ------------------------------------------------------

const MaterialSlotInspectorPanel = optionalLazy(
  "../editor/materials/MaterialSlotInspectorPanel.jsx",
  MaterialSlotInspectorPanelFallback
);

const DecalPlacementPanel = optionalLazy(
  "../editor/decals/DecalPlacementPanel.jsx",
  DecalPlacementPanelFallback
);

const PaintLibraryPanel = optionalLazy(
  "../editor/materials/PaintLibraryPanel.jsx",
  PaintLibraryPanelFallback
);

const VariantSetsPanel = optionalLazy(
  "../editor/variants/VariantSetsPanel.jsx",
  VariantSetsPanelFallback
);

const AssetPlacementPalettePanel = optionalLazy(
  "../editor/assets/AssetPlacementPalettePanel.jsx",
  AssetPlacementPalettePanelFallback
);

const ConstraintBlockedBanner = optionalLazy(
  "../editor/constraints/ConstraintBlockedBanner.jsx",
  ConstraintBlockedBannerFallback
);

const ConstraintViolationsPanel = optionalLazy(
  "../editor/constraints/ConstraintViolationsPanel.jsx",
  ConstraintViolationsPanelFallback
);

const BulkObjectActionsPanel = optionalLazy(
  "../editor/outliner/BulkObjectActionsPanel.jsx",
  BulkObjectActionsPanelFallback
);

const UnifiedInspectorPanel = optionalLazy(
  "../editor/inspector/UnifiedInspectorPanel.jsx",
  UnifiedInspectorPanelFallback
);

// ------------------------------------------------------
// Optional late-tier constraint store
// ------------------------------------------------------

const constraintStoreModule =
  optionalJsModules["../editor/constraints/constraintViolationStore.js"] || {};

const setConstraintViolations =
  constraintStoreModule.setConstraintViolations || (() => {});
const clearConstraintViolations =
  constraintStoreModule.clearConstraintViolations || (() => {});

function normalizeLock(data) {
  if (!data) return { state: "unknown" };
  if (data.state) return data;

  if (data.owned === true || data.is_owner === true) return { state: "owned" };
  if (data.owner_id != null) {
    return {
      state: "taken",
      owner_id: data.owner_id,
      owner_name: data.owner_name,
    };
  }
  if (data.locked === false || data.exists === false) {
    return { state: "missing" };
  }

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
  const [user, setUser] = useState(null);
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);
  const [sceneStateHash, setSceneStateHash] = useState("__working__");

  const [sceneIndex, setSceneIndex] = useState(null);
  const [sceneErr, setSceneErr] = useState(null);

  const [activeSnapshotOverrideId, setActiveSnapshotOverrideId] = useState(null);
  const [labRefreshKey, setLabRefreshKey] = useState(0);

function handleApplyPaint(objectId, materialState) {
  setSceneIndex((prev) => {
    if (!prev) return prev;

    const applyToObjects = (objects) =>
      objects.map((obj) => {
        if (obj.id !== objectId) return obj;

        const prevState = obj.material_state || {};
        const prevMeshes = prevState.meshes || {};

        const mergedMeshes = { ...prevMeshes };

        Object.entries(materialState.meshes || {}).forEach(([key, value]) => {
          mergedMeshes[key] = value;
        });

        return {
          ...obj,
          material_state: {
            ...prevState,
            meshes: mergedMeshes,
          },
        };
      });

    console.log("PREV SCENE INDEX:", prev);

    return {
      ...prev,
      objects: applyToObjects(prev.objects || []),

      body_state: {
        ...prev.body_state,
        scene: {
          ...prev.body_state?.scene,
          objects: applyToObjects(
            prev.body_state?.scene?.objects || []
          ),
        },
      },
    };
  });
}
  
  const viewerApiRef = useRef(null);

  const [isDirty, setIsDirty] = useState(false);
  
  const [bootstrapped, setBootstrapped] = useState(false);
  
  const [workspace, setWorkspace] = useState("design");
  
  const [activePaint, setActivePaint] = useState(null);

  const { selectedId } = useSelectionStore();
  const { lock } = useLockStatus();

  const snapshotsFetchInFlight = useRef(false);

  const aliveRef = useRef(true);
  useEffect(() => {
    aliveRef.current = true;
    return () => {
      aliveRef.current = false;
    };
  }, []);
  
  // 🔥 LOAD REAL USER FROM BACKEND
  useEffect(() => {
    async function loadUser() {
      const u = await fetchCurrentUser();
      console.log("🔥 USER:", u);
      setUser(u);
    }

    loadUser();
  }, []);

  const fetchSnapshots = useCallback(() => {
    if (snapshotsFetchInFlight.current) return Promise.resolve();
    snapshotsFetchInFlight.current = true;

    const token = getAccessToken?.();
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    return fetch(`${API_BASE}/projects/${projectId}/snapshots/`, { headers })
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

  useEffect(() => {
    if (!projectId) return;
    fetchSnapshots().catch(console.error);
  }, [projectId, fetchSnapshots]);

// 🔥 Tier 7.75 — bootstrap edit session (FULL)
useEffect(() => {
  if (!projectId) return;
  if (!snapshots.length) return;
  if (bootstrapped) return;

  async function bootstrap() {
    try {
      console.log("🔥 7.75 bootstrap starting...");

      const draftId = await bootstrapEditSession(projectId);

      console.log("✅ Draft ready:", draftId);

      // ✅ FIXED TOKEN KEY
      const token = getAccessToken();

      // ✅ 1. acquire lock (CRITICAL)
      const lockRes = await fetch(
        `http://localhost:8000/projects/${projectId}/snapshots/${draftId}/lock`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("lockRes status:", lockRes.status);

      if (!lockRes.ok) {
        throw new Error("Failed to acquire lock");
      }

      console.log("🔒 Lock acquired");

      // ✅ 2. fetch scene (CRITICAL)
      const res = await fetch(
        `http://localhost:8000/snapshots/${draftId}/scene`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("sceneRes status:", res.status);

      if (!res.ok) throw new Error("Failed to fetch scene");

      const scene = await res.json();

      console.log("🎬 Scene loaded:", scene);
      console.log("🔥 FIRST OBJECT:", scene?.objects?.[0]);

      // ✅ 3. push to global store (CRITICAL)
      setSceneIndex(scene, draftId);

      // ✅ 4. activate snapshot
      setActiveSnapshotOverrideId(draftId);

      // 🔥 CRITICAL FIX — sync lock state to UI
      setLockStatus({ state: "owned" });

      setBootstrapped(true);

    } catch (e) {
      console.error("❌ 7.75 bootstrap failed", e);
    }
  }

  bootstrap();
}, [projectId, snapshots, bootstrapped]);
  
  const draftSnapshot = snapshots.find((s) => s.status === "draft");
  const completedSnapshot = snapshots.find((s) => s.status === "completed");

  const overrideSnapshot = activeSnapshotOverrideId
    ? snapshots.find((s) => s.id === activeSnapshotOverrideId)
    : null;

  const activeSnapshot = overrideSnapshot ?? (draftSnapshot ?? completedSnapshot);

  const isEditMode = activeSnapshot?.status === "draft";
  const isEditable = isEditMode;

  const baseSnapshot = useMemo(() => {
    if (!activeSnapshot?.parent_snapshot_id) return null;
    return (
      snapshots?.find((s) => s.id === activeSnapshot.parent_snapshot_id) || null
    );
  }, [activeSnapshot?.id, activeSnapshot?.parent_snapshot_id, snapshots]);

  useEffect(() => {
    if (activeSnapshot?.id) historyPush(activeSnapshot.id);
  }, [activeSnapshot?.id]);

  const navigateToSnapshot = useCallback(
    (id) => {
      const nextId = Number(id);
      if (!Number.isFinite(nextId)) return;

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
        clearAllSelectionState?.();
      } catch {}

      try {
        clearConstraintViolations?.();
      } catch {}

      setActiveSnapshotOverrideId(nextId);
      fetchSnapshots().catch(console.error);
    },
    [fetchSnapshots]
  );
  
  const restoreSnapshotFromHistory = useCallback(
    (snapshotId) => {
      if (!snapshotId) return;

      navigateToSnapshot(snapshotId);
    },
    [navigateToSnapshot]
  );

  const sceneRebindKey = useMemo(() => {
    if (!activeSnapshot?.id) return "snap:none";
    return `snap:${activeSnapshot.id}`;
  }, [activeSnapshot?.id]);

  useEffect(() => {
    if (!activeSnapshot?.id) return;

    const controller = new AbortController();

    setSceneErr(null);
    setSceneIndex(null);

    fetchScene(projectId, activeSnapshot.id, { signal: controller.signal })
      .then((idx) => {
        setSceneIndex(idx);

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
              clearAllSelectionState?.();
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

  const refreshSceneIndex = useCallback(() => {
    if (!activeSnapshot?.id) return;

    const controller = new AbortController();
    setSceneErr(null);
    setSceneIndex(null);

    fetchScene(projectId, activeSnapshot.id, { signal: controller.signal })
      .then((idx) => {
        console.log("🔥 SCENE INDEX:", idx);
        console.log("🔥 OBJECTS:", idx?.objects);
        console.log("🔥 BODY OBJECTS:", idx?.body_state?.objects);

        setSceneIndex(idx);
      })
      .catch((e) => {
        if (e?.name === "AbortError") return;
        setSceneErr(String(e?.message || e));
      });

    return () => controller.abort();
  }, [projectId, activeSnapshot?.id]);

  const { targetId: resolvedTargetId } = resolveSelectedTarget(
    activeSnapshot,
    selectedId
  );
  
  const sceneIndexForViewer = useMemo(() => {
    if (!sceneIndex) return sceneIndex;

    const decor_state =
      sceneIndex?.decor_state ??
      activeSnapshot?.decor_state ??
      activeSnapshot?.body_state?.decor_state ??
      null;

    if (decor_state == null) return sceneIndex;

    return { ...sceneIndex, decor_state };
  }, [sceneIndex, activeSnapshot?.id]);

  const materialOverrides = useMemo(() => {
    return (
      activeSnapshot?.decor_state?.material_overrides ??
      activeSnapshot?.body_state?.material_overrides ??
      {}
    );
  }, [activeSnapshot?.id]);

  const constraintsForPanel = useMemo(() => {
    const a = activeSnapshot || {};
    const d = a?.decor_state || a?.body_state?.decor_state || {};
    const c1 = a?.constraints;
    const c2 = a?.constraint_violations;
    const c3 = d?.constraints;
    const c4 = d?.violations;
    const list = c1 || c2 || c3 || c4 || [];
    return Array.isArray(list) ? list.filter(Boolean) : [];
  }, [activeSnapshot?.id]);

  useEffect(() => {
    let alive = true;
    let t = null;

    async function tick() {
      if (!activeSnapshot?.id) return;

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

  const activeTargetId = resolvedTargetId ?? selectedId ?? null;

  const hasDraftLock = lock?.state === "owned";
  const station = "geometry";

  const canEditByRole = user?.is_admin === true;
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

  const whyBlockedReasons = useMemo(() => {
    const rs = [];

    if (!activeSnapshot?.id) rs.push("SNAPSHOT_MISSING");
    if (sceneIndex == null && !!activeSnapshot?.id) rs.push("LOADING");

    if (activeSnapshot?.id && activeSnapshot?.status !== "draft") {
      rs.push("NOT_DRAFT");
    }

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

  useDraftAutosave({
    snapshot: activeSnapshot,
    sceneStateHash,
    isDirty,
    onSaved: () => setIsDirty(false),
  });

const commitToolPayload = useCallback(
  async (payload) => {
    try {
      console.log("commitToolPayload:", payload);

      if (!toolsEnabled) {
        return {
          ok: false,
          error: { kind: "conflict", detail: "Tools disabled" },
        };
      }

      const nextStation = payload?.station || "geometry";
      const tool = payload?.tool;
      const toolPayload = payload?.payload || {};

      if (!tool) {
        return {
          ok: false,
          error: { kind: "invalid", detail: "tool missing" },
        };
      }

      // -----------------------------
      // 1. evaluate
      // -----------------------------
      const evalRes = await executeTool({
        snapshotId: activeSnapshot?.id,
        station: nextStation,
        tool,
        payload: toolPayload,
        mode: "tools",
      });

      if (!evalRes?.ok) {
        if (Array.isArray(evalRes?.violations) && evalRes.violations.length) {
          setConstraintViolations(evalRes.violations);
        } else {
          clearConstraintViolations();
        }

        return evalRes;
      }

      clearConstraintViolations();

      // -----------------------------
      // 2. apply
      // -----------------------------
      const applyRes = await executeTool({
        snapshotId: activeSnapshot?.id,
        station: nextStation,
        tool,
        payload: toolPayload,
        mode: "tools",
      });

      // -----------------------------
      // 3. LOCAL STATE UPDATE (PAINT FIX)
      // -----------------------------
      if (tool === "PAINT_APPLY_LIBRARY_PRESET") {
        const { target_id, preset_id } = toolPayload || {};

        if (target_id && preset_id) {
          const objectId =
            target_id.split("::")[0].replace("mesh:", "");

          // 🔥 USE SINGLE SOURCE OF TRUTH
          handleApplyPaint(objectId, {
            meshes: {
              [target_id]: {
                preset: preset_id,
              },
            },
          });

          // 🔥 CRITICAL: reapply materials WITHOUT reload
          setTimeout(() => {
            viewerApiRef.current?.syncMaterials?.();
          }, 0);
        }
      }
      
      // -----------------------------
      // 🚫 NO REFRESH HERE (CRITICAL FIX)
      // -----------------------------

      return applyRes;

    } catch (e) {
      return {
        ok: false,
        error: { kind: "network", detail: String(e?.message || e) },
      };
    }
  },
  [activeSnapshot?.id, toolsEnabled] // ✅ CLEAN DEPENDENCIES
);

// ✅ Tier 7.67 — keyboard dispatcher (FINAL)
const handleShortcutAction = useCallback(
  (action) => {
    if (!activeSnapshot?.id) return;

    switch (action) {
      // --------------------------------------------------
      // TRANSFORM MODES (FIXED — use store, NOT viewer)
      // --------------------------------------------------
      case "TRANSFORM_TRANSLATE":
        setGizmoMode("translate");
        break;

      case "TRANSFORM_ROTATE":
        setGizmoMode("rotate");
        break;

      case "TRANSFORM_SCALE":
        setGizmoMode("scale");
        break;

      // --------------------------------------------------
      // HISTORY
      // --------------------------------------------------
      case "UNDO": {
        const snap = historyUndo();
        if (snap?.id) restoreSnapshotFromHistory(snap.id);
        break;
      }

      case "REDO": {
        const snap = historyRedo();
        if (snap?.id) restoreSnapshotFromHistory(snap.id);
        break;
      }

      // --------------------------------------------------
      // DUPLICATE (SAFE OBJECT ID EXTRACTION)
      // --------------------------------------------------
      case "DUPLICATE": {
        if (!selectedId) return;

        const objectId = String(selectedId).split("::")[0];

        commitToolPayload({
          tool: "SCENE_DUPLICATE_OBJECT",
          station: "geometry",
          payload: { object_id: objectId },
        });
        break;
      }

      // --------------------------------------------------
      // CLEAR SELECTION
      // --------------------------------------------------
      case "CLEAR_SELECTION":
        clearAllSelectionState();
        break;

      default:
        break;
    }
  },
  [
    activeSnapshot?.id,
    selectedId,
    commitToolPayload,
    restoreSnapshotFromHistory,
  ]
);

  // ✅ Tier 7.67 — activate keyboard shortcuts
  useKeyboardShortcuts({
    onAction: handleShortcutAction,
  });
  
// 🔥 Tier 7.75 — block UI until bootstrap completes
if (!bootstrapped) {
  return (
    <div className="h-screen flex items-center justify-center">
      <div className="text-sm opacity-70">
        Preparing editor session...
      </div>
    </div>
  );
}

  return (
    <CapabilityProvider role={user?.role ?? "viewer"}>
      <EditorShell
        headerRight={
          <>
            <DraftStatusBadge snapshot={activeSnapshot} />
            {isDirty && (
              <span style={{ color: "#d33682", marginLeft: 8, fontSize: 12 }}>
                Unsaved changes
              </span>
            )}
            <SnapshotPreview
              snapshot={activeSnapshot}
              onDraftCreated={fetchSnapshots}
            />
          </>
        }
      >
      
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
        
        <div className="p-3 pt-2 pb-0">
          <PanelSuspense>
            <ConstraintBlockedBanner />
          </PanelSuspense>
        </div>

        <div className="p-3 pt-2 pb-0 flex items-center gap-2">
          <div className="flex-1">
            <ToolContextBar
              canEdit={toolsEnabled}
              reasons={whyBlockedReasons}
              lockLabelText={lock?.state === "owned" ? "LOCK: Owned" : ""}
              onRestoreSnapshot={restoreSnapshotFromHistory} // ✅ Tier 7.66 bridge
            />
          </div>
          <ViewModeSelect />
        </div>

        <div className="p-3 pt-2 pb-0">
          <CameraToolbar
            onFrameSelected={() => viewerApiRef.current?.frameSelected?.()}
            onFrameScene={() => viewerApiRef.current?.frameScene?.()}
            onPreset={(preset) => viewerApiRef.current?.applyPreset?.(preset)}
          />
        </div>

        <div className="p-3 pt-2 pb-0">
          <LightingControls />
        </div>
        
        <div className="p-3 pt-2 pb-0 flex items-center gap-3">
          <div className="flex-1">
            <StudioModeBar
              activeSnapshot={activeSnapshot}
              onSetActiveSnapshotId={(id) => {
                navigateToSnapshot(id);
              }}
            />
          </div>

          <div className="flex gap-2 text-sm">
            <button
              onClick={() => setWorkspace("design")}
              className={workspace === "design" ? "font-bold underline" : "opacity-60"}
            >
              Design
            </button>

            <button
              onClick={() => setWorkspace("decor")}
              className={workspace === "decor" ? "font-bold underline" : "opacity-60"}
            >
              Decor
            </button>

            <button
              onClick={() => setWorkspace("tuning")}
              className={workspace === "tuning" ? "font-bold underline" : "opacity-60"}
            >
              Tuning
            </button>

            <button
              onClick={() => setWorkspace("testing")}
              className={workspace === "testing" ? "font-bold underline" : "opacity-60"}
            >
              Testing
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-[220px_1fr_280px] gap-3 p-3 h-[calc(100vh-140px)]">
        
        {/* ================= LEFT ================= */}
        <div className="space-y-3 overflow-y-auto pr-1">

          {workspace === "design" && (
            <div>
              <div style={{ padding: 12 }}>
                <UndoRedoBar
                  projectId={projectId}
                  activeSnapshotId={activeSnapshot?.id}
                  onNavigate={navigateToSnapshot}
                />
              </div>

              <div style={{ padding: 12 }}>
                <SnapshotHistoryGraphPanel
                  activeSnapshotId={activeSnapshot?.id}
                  onNavigate={navigateToSnapshot}
                />
              </div>

              <div style={{ padding: 12 }}>
                <SnapshotDiffPanel
                  baseSnapshot={baseSnapshot}
                  targetSnapshot={activeSnapshot}
                />
              </div>

              <div style={{ padding: 12 }}>
                {sceneErr ? (
                  <div className="text-red-600 text-sm">{sceneErr}</div>
                ) : null}
                <SceneIndexPanel
                  sceneIndex={sceneIndex}
                  snapshotId={activeSnapshot?.id}
                />
              </div>

              <div style={{ padding: 12 }}>
                <SceneLayersPanel sceneIndex={sceneIndex} />
              </div>

              <div style={{ padding: 12 }}>
                <SceneGraphPanel sceneIndex={sceneIndex} />
              </div>

              <div style={{ padding: 12 }}>
                <SceneOutlinerPanel
                  snapshot={activeSnapshot}
                  canEdit={toolsEnabled}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                />
              </div>

              <div style={{ padding: 12 }}>
                <SceneOutlinerTreePanel
                  snapshot={activeSnapshot}
                  canEdit={toolsEnabled}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                />
              </div>

              <div style={{ padding: 12 }}>
                <PanelSuspense>
                  <BulkObjectActionsPanel
                    canEdit={toolsEnabled}
                    onCommitTool={(payload) => commitToolPayload(payload)}
                  />
                </PanelSuspense>
              </div>

              <div style={{ padding: 12 }}>
                <ObjectActionsPanel
                  canEdit={toolsEnabled}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                />
              </div>

              <div style={{ padding: 12 }}>
                <AttachAssetPanel
                  projectId={projectId}
                  snapshotId={activeSnapshot?.id}
                  onAttached={refreshSceneIndex}
                />
              </div>

              <div style={{ padding: 12 }}>
                <SelectionHud />
              </div>

              <div
                style={{ padding: 12, display: "flex", gap: 10, alignItems: "center" }}
              >
                <button onClick={() => setSelectedId("panel-1")}>Select panel-1</button>

                <TransformToolbar
                  activeSnapshot={activeSnapshot}
                  isEditable={isEditable}
                 selectedId={selectedId}
                  onNewSnapshot={(newId) => {
                    console.log("New snapshot:", newId);
                    fetchSnapshots().catch(console.error);
                  }}
                />
              </div>

              <div style={{ padding: 12 }}>
                <GizmoCommitController
                  activeSnapshot={activeSnapshot}
                  activeTargetId={activeTargetId}
                  enabled={gizmoEnabled}
                  reasonDisabled={gizmoReason}
                  enablePreview={false}
                  onApplied={(newId) => {
                    console.log("Applied new snapshot:", newId);

                    setActiveSnapshotOverrideId(null);
                    clearConstraintViolations?.();

                    fetchSnapshots().catch(console.error);
                  }}
                />
              </div>

              <div style={{ padding: 12 }}>
                <TransformToolPanel
                  activeSnapshot={activeSnapshot}
                  disabled={!toolsEnabled}
                  onExecuted={(data) => {
                    console.log("Tool executed:", data);
                    clearConstraintViolations?.();
                    fetchSnapshots().catch(console.error);
                  }}
                />
              </div>
            </div>
          )}

          {workspace === "decor" && (
            <div>
              <div style={{ padding: 12 }}>
                <MaterialOverridesPanel snapshot={activeSnapshot} />
              </div>

              <div style={{ padding: 12 }}>
                <MaterialInspectorPanel
                  snapshot={activeSnapshot}
                  canEdit={toolsEnabled}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                />
              </div>

              <div style={{ padding: 12 }}>
                <PanelSuspense>
                  <MaterialSlotInspectorPanel
                    snapshot={activeSnapshot}
                    canEdit={toolsEnabled}
                    onCommitTool={(payload) => commitToolPayload(payload)}
                  />
                </PanelSuspense>
              </div>

              <div style={{ padding: 12 }}>
                <PaintParamsPanel
                  snapshot={activeSnapshot}
                  canEdit={toolsEnabled}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                />
              </div>

              <div style={{ padding: 12 }}>
                <PanelSuspense>
                  <PaintLibraryPanel
                    snapshot={activeSnapshot}
                    canEdit={toolsEnabled}
                    onCommitTool={(payload) => commitToolPayload(payload)}
                    onApplyPaint={(preset) => {
                      console.log("🎨 ACTIVE PAINT SET:", preset);
                      setActivePaint(preset);
                    }}
                  />            
                </PanelSuspense>
              </div>

              <div style={{ padding: 12 }}>
                <DecalAssetBrowserPanel
                  canEdit={toolsEnabled}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                />
              </div>

              <div style={{ padding: 12 }}>
                <PanelSuspense>
                  <DecalPlacementPanel />
                </PanelSuspense>
              </div>
            </div>
          )}

          {workspace === "tuning" && (
            <div>
              <div style={{ padding: 12 }}>
                <PanelSuspense>
                  <VariantSetsPanel
                    snapshot={activeSnapshot}
                    canEdit={toolsEnabled}
                    onCommitTool={(payload) => commitToolPayload(payload)}
                  />
                </PanelSuspense>
              </div>

              <div style={{ padding: 12 }}>
                <ObjectActionsPanel
                  canEdit={toolsEnabled}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                />
              </div>
            </div>
          )}

          {workspace === "testing" && (
            <div>
              <div style={{ padding: 12 }}>
                <TelemetryViewerPanel activeSnapshot={activeSnapshot} />
              </div>

              <div style={{ padding: 12 }}>
                <TelemetryAdvancedPanel />
              </div>

              <div style={{ padding: 12 }}>
                <TelemetryComparePanel />
              </div>

              <div style={{ padding: 12 }}>
                <ScenarioTemplatesPanel
                  projectId={projectId}
                  onCreated={() => setLabRefreshKey((k) => k + 1)}
                />
              </div>

              <div style={{ padding: 12 }}>
                <BatchRunnerPanel activeSnapshot={activeSnapshot} />
              </div>

              <div style={{ padding: 12 }}>
                <TelemetryLabPanel
                  key={`lab:${labRefreshKey}`}
                  projectId={projectId}
                  activeSnapshot={activeSnapshot}
                />
              </div>

              <div style={{ padding: 12 }}>
                <ReferenceFramesPanel
                  activeSnapshotId={activeSnapshot?.id}
                  disabled={false}
                />
              </div>
            </div>
          )}

        </div>
        
          {/* ================= CENTER ================= */}
          <div className="h-full w-full">
            <div className="relative h-full">
              <ThreeSceneViewer
                key={sceneRebindKey}
                sceneIndex={sceneIndexForViewer}
                materialOverrides={materialOverrides}
                disabled={!activeSnapshot?.id}
                canEdit={toolsEnabled}
                onCommitTool={(p) => commitToolPayload(p)}
                onViewerApiReady={(api) => {
                  viewerApiRef.current = api;
                }}
                activePaint={activePaint}
              />

              {/* ✅ Tier 7.62 — Marquee Selection Overlay */}
              <MarqueeOverlay />
            </div>
          </div>
          
          {/* ================= RIGHT ================= */}
          <div className="space-y-3 overflow-y-auto pr-1">
            <div className="h-full p-2">
              <PanelSuspense>
                <UnifiedInspectorPanel
                  snapshot={activeSnapshot}
                  toolsEnabled={toolsEnabled}
                  lockState={lock?.state || "unknown"}
                  onCommitTool={(payload) => commitToolPayload(payload)}
                  constraints={constraintsForPanel}
                  setActivePaint={setActivePaint}
                />
              </PanelSuspense>
            </div>
          </div>        

        </div> {/* GRID CLOSED */}
        
        <EditorLayoutHost
          editable={isEditMode}
          panelContext={{
            history: snapshots,
            activeSnapshotId: activeSnapshot?.id ?? null,
            onNavigate: navigateToSnapshot,
            constraints: constraintsForPanel,
          }}
          onSceneChange={() => {
            if (!isEditMode) return;
            setSceneStateHash(Date.now().toString());
            setIsDirty(true);
          }}
        />

      </EditorShell>
    </CapabilityProvider>
  );
 }
