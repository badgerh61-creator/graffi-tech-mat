// frontend/src/editor/scene/ThreeSceneViewer.jsx
import React, { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";

import { applyTransform } from "./applyTransform";
import { applyMaterialState } from "./applyMaterialState";
import { applyDecals } from "./applyDecals";

// ✅ 6G.16 — mesh role mapping
import { buildMeshRoleMap } from "./buildMeshRoleMap";

import {
  applySelectionOutline,
  clearSelectionOutline
} from "./applySelectionOutline";

const EMPTY_ARRAY = Object.freeze([]);

import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { useTransformSpace } from "../transform/transformSpaceStore";

// ✅ Step 1 — TransformControls (Three.js handles)
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";

// ✅ Tier 7.48 — Orbit camera controls
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

import { resolveAssetRef } from "./resolveAssetRef";
import { buildPickedTargetId } from "./pickingId";
import { applyTransformToObject3D, makePlaceholderMesh } from "./applyTransform";

import {
  clearSelection,
  useSelection as useSelectionStore,
  setSelectedId,
} from "../selection/selectionStore";

// ✅ Tier 7.60 — multi-select bridge/store
import {
  toggleMultiSelection,
  setPrimarySelection,
  setMultiSelection, // ✅ NEW (for marquee replace selection)
} from "../selection/multiSelectionStore";
import {
  syncPrimaryToSingleSelection,
  clearAllSelectionState,
} from "../selection/multiSelectionBridge";

// ✅ ✅ Tier 7.62 — marquee selection (NEW)
import {
  startMarquee,
  updateMarquee,
  endMarquee,
  clearMarquee,
  marqueeGetSnapshot,
} from "../selection/marqueeStore";

// ✅ 6G.6 layers
import { useSceneLayers, ensureKind } from "./layersStore";

// ✅ 6G.10 mesh index publishing
import { clearMeshIndex, setMeshPathsForObject } from "./meshIndexStore";
import { buildMeshPath } from "./meshPath";

// ✅ 6G.12 parseSelectedId (full) + mesh lookup helper
import { parseSelectedId, findNodeByMeshPath } from "./selectionResolve";

// ✅ 7.27 preview ghost
import { useGizmoPreview } from "../gizmo/gizmoPreviewStore";

// ✅ Step 6 — shared gizmo mode store
import { useGizmoMode } from "../gizmo/gizmoModeStore";

// ✅ Tier 7.49 — canonical snap store
import { useSnap } from "../transform/snapStore";

import { useViewMode } from "../view/viewModeStore";

// ✅ Tier 7.38 — active decal + preview patch store
import { useActiveDecal } from "../decals/activeDecalStore";
import {
  useDecalPreview,
  setDecalPreviewPatch,
  clearDecalPreviewPatch,
} from "../decals/decalPreviewStore";

// ✅ Tier 7.41 — selection filters + deterministic pick resolution
import { useSelectionFilter } from "../selection/selectionFilterStore";

// ✅ Tier 7.41 — set/clear active decal (optional, safe)
import { setActiveDecalId, clearActiveDecalId } from "../decals/activeDecalStore";

// ✅ Tier 7.42 — Material overrides (read + apply)
import { applyMaterialOverridesToScene } from "../materials/applyMaterialOverridesToScene";

// ✅ Tier 7.53 — material slot discovery store
import {
  clearMaterialSlots,
  setMaterialSlotsForTarget,
} from "../materials/materialSlotStore";

// ✅ Tier 7.48 — camera helpers
import { applyCameraPreset } from "../camera/applyCameraPreset";
import {
  computeVisibleSceneBounds,
  computeSelectedBounds,
} from "./sceneBounds";

// ✅ Tier 7.61 — Pivot preview
import { usePivotPreview } from "../transform/pivotPreviewStore";

import { useActivePaint } from "../materials/activePaintStore";
import { resolvePreset } from "../materials/presetLibrary";

import { cleanupScene } from "./cleanupScene";

// ✅ 6G.21 — asset load race protection
import {
  beginLoad,
  isLoadValid,
  clearLoad
} from "./assetManager";

import { pickObject } from "../interaction/picking";
import { normalizeSceneObjects } from "./sceneSerializer";

// --------------------------------------------------
// ✅ Renderer factory (WebGL safe)
// --------------------------------------------------

function makeRenderer(canvas) {
  try {
    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance",
    });

    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(
      canvas.clientWidth || 800,
      canvas.clientHeight || 500,
      false
    );

    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;
    renderer.physicallyCorrectLights = true;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    return renderer;
  } catch (err) {
    console.error("Renderer creation failed:", err);
    return null;
  }
}


function makeCamera(width, height) {
  const cam = new THREE.PerspectiveCamera(45, width / height, 0.1, 5000);
  cam.position.set(3.0, 2.0, 3.0);
  cam.lookAt(0, 0.8, 0);
  return cam;
}

function fitCameraToScene(camera, root, controls = null) {
  const box = new THREE.Box3().setFromObject(root);
  if (box.isEmpty()) return;

  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);

  const maxDim = Math.max(size.x, size.y, size.z) || 1;
  const fov = (camera.fov * Math.PI) / 180;
  const distance = (maxDim / (2 * Math.tan(fov / 2))) * 1.6;

  camera.position.set(center.x + distance, center.y + distance * 0.5, center.z + distance);

  if (controls) {
    controls.target.copy(center);
    controls.update();
  } else {
    camera.lookAt(center);
  }

  camera.updateProjectionMatrix();
}

// ✅ 6G.7
function fitCameraToObject(camera, object3d, controls = null) {
  const box = new THREE.Box3().setFromObject(object3d);
  if (box.isEmpty()) return;

  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);

  const maxDim = Math.max(size.x, size.y, size.z) || 1;
  const fov = (camera.fov * Math.PI) / 180;
  const distance = (maxDim / (2 * Math.tan(fov / 2))) * 1.6;

  camera.position.set(center.x + distance, center.y + distance * 0.5, center.z + distance);

  if (controls) {
    controls.target.copy(center);
    controls.update();
  } else {
    camera.lookAt(center);
  }

  camera.updateProjectionMatrix();
}

function applyOpacityToMaterial(material, opacity) {
  const op = Number.isFinite(Number(opacity)) ? Number(opacity) : 1.0;
  const clamped = Math.min(1, Math.max(0, op));
  if (!material) return;

  if (Array.isArray(material)) {
    material.forEach((m) => {
      if (!m) return;
      m.transparent = clamped < 1;
      m.opacity = clamped;
      m.needsUpdate = true;
    });
  } else {
    material.transparent = clamped < 1;
    material.opacity = clamped;
    material.needsUpdate = true;
  }
}

function makeCheckerTexture(size = 128, cells = 8) {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  if (!ctx) return null;

  const cell = Math.max(1, Math.floor(size / cells));
  for (let y = 0; y < cells; y++) {
    for (let x = 0; x < cells; x++) {
      const on = (x + y) % 2 === 0;
      ctx.fillStyle = on ? "#ffffff" : "#111111";
      ctx.fillRect(x * cell, y * cell, cell, cell);
    }
  }

  const tex = new THREE.CanvasTexture(canvas);
  tex.wrapS = THREE.ClampToEdgeWrapping;
  tex.wrapT = THREE.ClampToEdgeWrapping;
  tex.needsUpdate = true;
  return tex;
}

function clamp01(x) {
  const n = Number(x);
  if (!Number.isFinite(n)) return 1.0;
  return Math.max(0, Math.min(1, n));
}

function degToRad(d) {
  return (Number(d) * Math.PI) / 180;
}

function radToDeg(r) {
  return (Number(r) * 180) / Math.PI;
}

function round(n, p = 4) {
  const f = Math.pow(10, p);
  return Math.round((Number(n) || 0) * f) / f;
}

function vec3Patch(v, p = 4) {
  return { x: round(v.x, p), y: round(v.y, p), z: round(v.z, p) };
}

function eulerDegPatch(e, p = 2) {
  return {
    x: round(radToDeg(e.x), p),
    y: round(radToDeg(e.y), p),
    z: round(radToDeg(e.z), p),
  };
}

function boxToPivotPreset(box, preset) {
  const min = box.min;
  const max = box.max;
  const center = box.getCenter(new THREE.Vector3());

  switch (preset) {
    case "center":
      return { x: center.x, y: center.y, z: center.z };

    case "bottom":
      return { x: center.x, y: min.y, z: center.z };

    case "top":
      return { x: center.x, y: max.y, z: center.z };

    case "front":
      return { x: center.x, y: center.y, z: max.z };

    case "back":
      return { x: center.x, y: center.y, z: min.z };

    case "left":
      return { x: min.x, y: center.y, z: center.z };

    case "right":
      return { x: max.x, y: center.y, z: center.z };

    default:
      return { x: center.x, y: center.y, z: center.z };
  }
}

function addStudioLighting(scene) {
  const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
  hemi.name = "light:hemi";
  scene.add(hemi);

  const key = new THREE.DirectionalLight(0xffffff, 3.0);
  key.name = "light:key";
  key.position.set(6, 8, 5);
  key.castShadow = true;
  scene.add(key);

  const fill = new THREE.DirectionalLight(0xffffff, 1.2);
  fill.name = "light:fill";
  fill.position.set(-6, 5, -4);
  scene.add(fill);

  const rim = new THREE.DirectionalLight(0xffffff, 0.8);
  rim.name = "light:rim";
  rim.position.set(0, 6, -8);
  scene.add(rim);
}

function normalizeSnapState(raw) {
  const snap = raw || {};

  return {
    enabled: !!snap.enabled,

    // existing
    step: Number.isFinite(Number(snap.step)) && Number(snap.step) > 0 ? Number(snap.step) : 0.1,
    step_degrees:
      Number.isFinite(Number(snap.step_degrees)) && Number(snap.step_degrees) > 0
        ? Number(snap.step_degrees)
        : 5,
    step_factor:
      Number.isFinite(Number(snap.step_factor)) && Number(snap.step_factor) > 0
        ? Number(snap.step_factor)
        : 0.1,

    axis_lock: ["none", "x", "y", "z"].includes(String(snap.axis_lock))
      ? String(snap.axis_lock)
      : "none",

    orientation: ["local", "world"].includes(String(snap.orientation))
      ? String(snap.orientation)
      : "local",

    // ✅ Tier 7.65 — ADD THESE
    mode: ["step", "grid"].includes(String(snap.mode)) ? String(snap.mode) : "step",

    gridSize:
      Number.isFinite(Number(snap.gridSize)) && Number(snap.gridSize) > 0
        ? Number(snap.gridSize)
        : 1,
  };
}

function sortObjectsStable(list) {
  return [...(list || [])].sort((a, b) =>
    String(a?.id || "").localeCompare(String(b?.id || ""))
  );
}

function normalizeParentId(v) {
  const s = String(v || "").trim();
  return s || null;
}

function publishMaterialSlotsForMesh(objectKey, meshPath, material) {
  const ok = String(objectKey || "").trim();
  const mp = String(meshPath || "").trim();
  if (!ok || !mp) return;

  const targetId = `${ok}::${mp}`;
  const materials = Array.isArray(material) ? material : [material];

  const slots = materials.map((m, i) => ({
    name: String(m?.name || `slot_${i}`),
    index: i,
  }));

  setMaterialSlotsForTarget(targetId, slots);
}

/**
 * ✅ ADDITIVE SAFE:
 * - canEdit gates ONLY TransformControls (gizmo).
 * - Picking/selection still works in READ.
 *
 * ✅ Tier 7.38:
 * - optional onCommitTool for DECAL_UPDATE on drag end
 *
 * ✅ Tier 7.41:
 * - selection filter + deterministic pick resolution (objects/meshes/decals)
 *
 * ✅ Tier 7.42:
 * - optional materialOverrides prop to patch materials deterministically (read-only application on load + updates)
 *
 * ✅ Tier 7.46 / 7.47:
 * - supports authoritative body_state.objects model_ref entries
 * - respects object.enabled === false
 * - supports url fallback in addition to asset_ref
 *
 * ✅ Tier 7.48:
 * - optional onViewerApiReady exposes:
 *   - frameSelected()
 *   - frameScene()
 *   - applyPreset(preset)
 *
 * ✅ Tier 7.49:
 * - TransformControls snap + local/world orientation read from canonical snapStore
 * - no remount on snap changes
 *
 * ✅ Tier 7.51:
 * - parent/child scene construction from object.parent_id
 * - flat scenes still work unchanged
 *
 * ✅ Tier 7.53:
 * - viewer-derived material slot discovery published to materialSlotStore
 * - no backend mutation
 * - additive-safe for existing material override flows
 *
 * ✅ Tier 7.60:
 * - viewport supports additive multi-object selection
 * - plain click sets primary selection
 * - shift/ctrl/cmd click toggles object selection
 * - decal selection remains unchanged
 *
 * ✅ Tier 7.61:
 * - pivot preview support (no scene mutation yet in this section)
 */
export default function ThreeSceneViewer({
  sceneIndex,
  activeSnapshot = null,
  disabled = false,
  canEdit = true,
  onCommitTool = null,
  materialOverrides = null,
  onViewerApiReady = null,
  activePaint,
}) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const pickablesRef = useRef([]);
  const hasBuiltSceneRef = useRef(false);

  const { selectedId } = useSelectionStore();

  useEffect(() => {
    if (!sceneRef.current) return;

    if (!selectedId) {
      clearSelectionOutline();
      return;
    }

    applySelectionOutline({
      scene: sceneRef.current,
      selectedId,
    });

    updateSelectionBox();
    updateSelectionHighlight();

  }, [selectedId]);

  const layers = useSceneLayers();
  const { preview } = useGizmoPreview();
  const { mode: gizmoMode } = useGizmoMode();
  const { mode: transformSpace } = useTransformSpace();
  
  // ✅ Tier 7.69
  const viewMode = useViewMode();

  // ✅ Tier 7.49
  const snapState = useSnap().snap;

  const { decalId: activeDecalId } = useActiveDecal();
  const decalPreview = useDecalPreview();

  const { filter: selectionFilter } = useSelectionFilter();

  // ✅ ✅ Tier 7.61 — pivot preview (NEW)
  const { preview: pivotPreview } = usePivotPreview();

  const [err, setErr] = useState(null);
  const [loadingCount, setLoadingCount] = useState(0);

  const lastGoodObjectsRef = useRef([]);
  const loadedObjectsRef = useRef({});
  const lastValidSceneRef = useRef(null);

  console.log("🔥 RAW sceneIndex:", sceneIndex);

  if (sceneIndex && sceneIndex.objects) {
    lastValidSceneRef.current = sceneIndex;
  }

  const safeSceneIndex =
    sceneIndex && sceneIndex.objects
      ? sceneIndex
      : lastValidSceneRef.current;

  if (!safeSceneIndex) {
    console.warn("🚫 No valid scene yet");
  }

  const objects = useMemo(() => {
    const src = safeSceneIndex || sceneIndex;

    const a = src?.objects;
    const b = src?.body_state?.scene?.objects;
    const c = src?.snapshot?.body_state?.scene?.objects;
    const d = activeSnapshot?.body_state?.scene?.objects;

    const list =
      (Array.isArray(a) && a.length ? a :
      Array.isArray(b) && b.length ? b :
      Array.isArray(c) && c.length ? c :
      Array.isArray(d) && d.length ? d :
      []);

    if (list.length) {
      lastGoodObjectsRef.current = list;
    }

    const finalList = list.length ? list : lastGoodObjectsRef.current;

    console.log("🔥 RESOLVED OBJECT SOURCE:", finalList);

    return normalizeSceneObjects(finalList);
  }, [sceneIndex, activeSnapshot]);

  console.log("🔥 USING OBJECTS:", objects);
  
  const selectedIdRef = useRef(selectedId);
  const previewRef = useRef(preview);
  const appliedObjectsRef = useRef(new Set());
  const appliedMeshesRef = useRef(new Set());
  const gizmoModeRef = useRef(gizmoMode);
  const viewModeRef = useRef(viewMode);
  const meshIndexRef = useRef(new Map());
  
  // ✅ Tier 7.62 — marquee drag state
  const isDraggingRef = useRef(false);
  const dragStartRef = useRef(null);

  const activePaintRef = useRef(activePaint);

  useEffect(() => {
    activePaintRef.current = activePaint;
    console.log("🎨 ACTIVE PAINT (PROP):", activePaint);
  }, [activePaint]);
  
  // ✅ NEW — Tier 7.64
  const transformSpaceRef = useRef(transformSpace);

  useEffect(() => {
    transformSpaceRef.current = transformSpace;
  }, [transformSpace]);

  // ✅ Tier 7.49 snap ref
  const snapRef = useRef(normalizeSnapState(snapState));

  // ✅ ✅ Tier 7.61 pivot ref (NEW)
  const pivotPreviewRef = useRef(pivotPreview);

  const canEditRef = useRef(!!canEdit);
  const decalsRef = useRef([]);
  const activeDecalIdRef = useRef(activeDecalId);
  const decalPreviewRef = useRef(decalPreview);
  const onCommitToolRef = useRef(onCommitTool);
  const selectionFilterRef = useRef(selectionFilter);
  const materialOverridesRef = useRef(materialOverrides);
  const onViewerApiReadyRef = useRef(onViewerApiReady);

  const decalsSyncNonceRef = useRef(0);

  useEffect(() => {
    selectedIdRef.current = selectedId;
  }, [selectedId]);

  useEffect(() => {
    previewRef.current = preview;
  }, [preview]);

  useEffect(() => {
    gizmoModeRef.current = gizmoMode;
  }, [gizmoMode]);

  useEffect(() => {
    snapRef.current = normalizeSnapState(snapState);
  }, [snapState]);

  // ✅ ✅ Tier 7.61 pivot sync (NEW)
  useEffect(() => {
    pivotPreviewRef.current = pivotPreview || null;
  }, [pivotPreview]);

  useEffect(() => {
    canEditRef.current = !!canEdit;
  }, [canEdit]);

  useEffect(() => {
    decalsRef.current = objects.flatMap(
      (obj) => obj.decal_state || []
    );
  }, [objects]);

  useEffect(() => {
    activeDecalIdRef.current = activeDecalId ? String(activeDecalId) : null;
  }, [activeDecalId]);

  useEffect(() => {
    decalPreviewRef.current = decalPreview;
  }, [decalPreview]);

  useEffect(() => {
    onCommitToolRef.current = onCommitTool;
  }, [onCommitTool]);

  useEffect(() => {
    selectionFilterRef.current = selectionFilter || "all";
  }, [selectionFilter]);

  useEffect(() => {
    materialOverridesRef.current = materialOverrides;
  }, [materialOverrides]);

  useEffect(() => {
    onViewerApiReadyRef.current = onViewerApiReady;
  }, [onViewerApiReady]);
  
  // ✅ Tier 7.69 — sync view mode ref
  useEffect(() => {
    viewModeRef.current = viewMode;
  }, [viewMode]);
  
  useEffect(() => {
    appliedObjectsRef.current.clear();
    appliedMeshesRef.current.clear();
  }, [activeSnapshot?.id]);

  const viewerApiRef = useRef({
    syncSelection: null,
    syncPreview: null,
    syncMode: null,
    syncEditGate: null,
    syncDecals: null,
    syncDecalPreview: null,
    syncDecalTarget: null,
    syncPickFilter: null,
    syncMaterials: null,
    syncSnap: null,
    frameSelected: null,
    frameScene: null,
    applyPreset: null,

    // ✅ ✅ Tier 7.61 (placeholder, implemented in Part 3)
    getPivotPresetForObject: null,
  });

  useEffect(() => {
    if (!objects.length) {
      console.warn("⚠️ No objects, but still initializing viewer");
    }

    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    clearMeshIndex();
    clearMaterialSlots();

    let disposed = false;

    const scene = new THREE.Scene();

    let renderer = rendererRef.current;

    if (!renderer) {
      renderer = makeRenderer(canvas);
      rendererRef.current = renderer;
    }

    if (!renderer) {
      setErr("WebGL is not available (context creation failed).");
      return () => {};
    }
    
    let contextLost = false;

    function onContextLost(e) {
      e.preventDefault();
      contextLost = true;
      setErr("WebGL context was lost. Refresh the page if it doesn’t recover.");
    }

    function onContextRestored() {
      contextLost = false;
      setErr("WebGL context restored. If blank, refresh the page.");
    }

    canvas.addEventListener("webglcontextlost", onContextLost, false);
    canvas.addEventListener("webglcontextrestored", onContextRestored, false);

    addStudioLighting(scene);    
    const grid = new THREE.GridHelper(20, 20);
    grid.name = "grid";
    scene.add(grid);

    const root = new THREE.Group();
    root.name = "scene-root";
    scene.add(root);

    const decalsRoot = new THREE.Group();
    decalsRoot.name = "decals-root";
    root.add(decalsRoot);

    const rect = canvas.getBoundingClientRect();;
    const camera = makeCamera(rect.width || 800, rect.height || 500);

    const controls = new OrbitControls(camera, renderer.domElement);

    // smooth motion
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;

    controls.screenSpacePanning = true;

    // limits (prevent bad camera behavior)
    controls.minDistance = 1.5;
    controls.maxDistance = 100;
    controls.maxPolarAngle = Math.PI / 2;

    // feel tuning
    controls.rotateSpeed = 0.8;
    controls.zoomSpeed = 1.2;
    controls.panSpeed = 0.8;

    controls.update();

    const transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.setMode(gizmoModeRef.current);

    const gizmoEnabled = !disabled && !!canEditRef.current;
    transformControls.enabled = gizmoEnabled;
    transformControls.visible = false;
    scene.add(transformControls);

    function applySnapToTransformControls() {
      const snap = normalizeSnapState(snapRef.current);

      const mode = transformSpaceRef.current;
      transformControls.setSpace(mode === "world" ? "world" : "local");
      
      if (transformControls.mode === "translate") {
        transformControls.setTranslationSnap(snap.enabled ? snap.step : null);
        transformControls.setRotationSnap(null);
        transformControls.setScaleSnap(null);
        return;
      }

      if (transformControls.mode === "rotate") {
        transformControls.setTranslationSnap(null);
        transformControls.setRotationSnap(
          snap.enabled ? THREE.MathUtils.degToRad(snap.step_degrees) : null
        );
        transformControls.setScaleSnap(null);
        return;
      }

      if (transformControls.mode === "scale") {
        transformControls.setTranslationSnap(null);
        transformControls.setRotationSnap(null);
        transformControls.setScaleSnap(snap.enabled ? snap.step_factor : null);
        return;
      }

      transformControls.setTranslationSnap(null);
      transformControls.setRotationSnap(null);
      transformControls.setScaleSnap(null);
    }

    let gizmoDragging = false;
    let dragSession = 0;
    let committedForSession = false;

let selectionBoxHelper = null;

function clearSelectionBox() {
  if (!selectionBoxHelper) return;
  scene.remove(selectionBoxHelper);
  selectionBoxHelper.geometry?.dispose?.();
  selectionBoxHelper.material?.dispose?.();
  selectionBoxHelper = null;
}

// --------------------------------------------------
// ✅ Tier 7.61 — Pivot preview helper (FINAL)
// --------------------------------------------------

let pivotHelper = null;
let lastPivotKey = null;

function clearPivotHelper() {
  if (!pivotHelper) return;

  if (pivotHelper.parent) {
    pivotHelper.parent.remove(pivotHelper);
  }

  pivotHelper.geometry?.dispose?.();
  pivotHelper.material?.dispose?.();
  pivotHelper = null;
  lastPivotKey = null;
}

function updatePivotPreview() {
  const pv = pivotPreviewRef.current;
  if (!pv || !pv.object_id || !pv.pivot) {
    clearPivotHelper();
    return;
  }

  const group = objectGroups.get(String(pv.object_id));
  if (!group || group.visible === false) {
    clearPivotHelper();
    return;
  }

  const { x, y, z } = pv.pivot;

  const key = `${pv.object_id}:${x}:${y}:${z}`;
  if (pivotHelper && key === lastPivotKey) return;

  clearPivotHelper();

  const geom = new THREE.SphereGeometry(0.05, 12, 12);
  const mat = new THREE.MeshBasicMaterial({
    color: 0xffaa00,
    depthTest: false,
    depthWrite: false,
  });

  pivotHelper = new THREE.Mesh(geom, mat);
  pivotHelper.position.set(x, y, z);
  pivotHelper.renderOrder = 2000;

  scene.add(pivotHelper);

  lastPivotKey = key;
}

// ✅ KEEP ORIGINAL (ONLY ONCE)
const objectGroups = new Map();
const pivotGroups = new Map();
const allMeshes = new Set();
let selectedGroup = null;

function updateSelectionBox() {
  clearSelectionBox();

  const sid = selectedIdRef.current;
  if (!sid) return;

  // 🔥 mesh selection
  // 🔥 mesh selection
  if (sid.startsWith("mesh:")) {
    console.log("🧪 selection id:", sid);
    
    const mesh =
      meshIndexRef.current.get(sid) ||
      meshIndexRef.current.get(sid.replace(/^mesh:/, ""));
    
    console.log("🧪 meshIndex result:", mesh);
    
    if (!mesh) return;
    if (mesh.visible === false) return;

    const box = new THREE.Box3().setFromObject(mesh);
    console.log("🧪 mesh box:", box);
    
    if (box.isEmpty()) return;

    const size = new THREE.Vector3();
    const center = new THREE.Vector3();

    box.getSize(size);
    box.getCenter(center);

    const geom = new THREE.BoxGeometry(size.x, size.y, size.z);
    const edges = new THREE.EdgesGeometry(geom);

    selectionBoxHelper = new THREE.LineSegments(
      edges,
      new THREE.LineBasicMaterial({ color: 0x00ffff })
    );

    // 🔥 correct world-space placement
    selectionBoxHelper.position.set(0, 0, 0);
    selectionBoxHelper.geometry.translate(
      center.x,
      center.y,
      center.z
    );

    scene.add(selectionBoxHelper);
    return;
  }
  
  // 🔥 object selection (fallback)
  const { objectKey } = parseSelectedId(sid);
  if (!objectKey) return;

  const group = objectGroups.get(String(objectKey));
  if (!group) return;
  if (group.visible === false) return;

  const box = new THREE.Box3();

  group.traverse((node) => {
    if (node.isMesh) {
      box.expandByObject(node);
    }
  });

  if (box.isEmpty()) return;

  const size = new THREE.Vector3();
  const center = new THREE.Vector3();

  box.getSize(size);
  box.getCenter(center);

  const geom = new THREE.BoxGeometry(size.x, size.y, size.z);
  const edges = new THREE.EdgesGeometry(geom);

  selectionBoxHelper = new THREE.LineSegments(
    edges,
    new THREE.LineBasicMaterial({ color: 0x00ffff })
  );

  selectionBoxHelper.position.copy(center);
  scene.add(selectionBoxHelper);
}

function updateSelectionHighlight() {

  // clear previous highlight
  if (selectedGroup) {
    selectedGroup.traverse((node) => {
      if (!node.isMesh) return;

      const mat = node.material;
      if (!mat) return;

      if (Array.isArray(mat)) {
        mat.forEach((m) => {
          if (m.userData?.__origEmissive) {
            m.emissive.copy(m.userData.__origEmissive);
            delete m.userData.__origEmissive;
          }
        });
      } else {
        if (mat.userData?.__origEmissive) {
          mat.emissive.copy(mat.userData.__origEmissive);
          delete mat.userData.__origEmissive;
        }
      }
    });
    selectedGroup = null;
  }

  const sid = selectedIdRef.current;
  if (!sid) return;

  const { objectKey, meshPath } = parseSelectedId(sid);
  if (!objectKey) return;

  const group = objectGroups.get(String(objectKey));
  if (!group) return;
  if (group.visible === false) return;

  let target = group;

  if (meshPath) {
    const parts = String(meshPath).split("/");
    const node = findNodeByMeshPath(group, parts);
    if (node) target = node;
  }

  target.traverse((node) => {
    if (!node.isMesh) return;

    const mat = node.material;
    if (!mat) return;

    if (Array.isArray(mat)) {
      mat.forEach((m) => {
        if (!m.emissive) return;

        if (!m.userData.__origEmissive) {
          m.userData.__origEmissive = m.emissive.clone();
        }

        m.emissive.set(0x00ffff);
        m.emissiveIntensity = 0.35;
      });
    } else {
      if (!mat.emissive) return;

      if (!mat.userData.__origEmissive) {
        mat.userData.__origEmissive = mat.emissive.clone();
      }

      mat.emissive.set(0x00ffff);
      mat.emissiveIntensity = 0.35;
    }
  });

  selectedGroup = target;
}

let decalPlanes = [];
const textureLoader = new THREE.TextureLoader();
const decalTextureCache = new Map();
const checkerTex = makeCheckerTexture(128, 8);

const decalProxyById = new Map();
const decalBaseById = new Map();

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

const meshToObjectKey = new Map();
const meshToObjectId = new Map();

function resolveObjectKeyFromHitMesh(hitMesh) {
  if (!hitMesh) return null;

  const direct = meshToObjectKey.get(hitMesh);
  if (direct) return direct;

  const legacy = meshToObjectId.get(hitMesh);
  if (legacy) return legacy;

  let p = hitMesh.parent;
  while (p) {
    if (typeof p.name === "string" && p.name.startsWith("obj:")) {
      return p.name.slice(4);
    }
    p = p.parent;
  }
  return null;
}

function pickIdNodeForMeshPath(hitMesh) {
  if (!hitMesh) return null;
  if (hitMesh.name && String(hitMesh.name).trim()) return hitMesh;

  let p = hitMesh.parent;
  while (p) {
    if (typeof p.name === "string" && p.name.startsWith("obj:")) break;
    if (p.name && String(p.name).trim()) return p;
    p = p.parent;
  }
  return hitMesh;
}

    function frameScene() {
      const bounds = computeVisibleSceneBounds(root);
      if (bounds.isEmpty()) {
        fitCameraToScene(camera, root, controls);
        return;
      }

      applyCameraPreset({
        camera,
        controls,
        bounds,
        preset: "iso",
      });
    }

    function frameSelected() {
      const bounds = computeSelectedBounds(root, selectedIdRef.current);
      if (bounds.isEmpty()) {
        frameScene();
        return;
      }

      applyCameraPreset({
        camera,
        controls,
        bounds,
        preset: "iso",
      });
    }

    function applyPreset(preset) {
      const selectedBounds = computeSelectedBounds(root, selectedIdRef.current);
      const bounds = selectedBounds.isEmpty()
        ? computeVisibleSceneBounds(root)
        : selectedBounds;

      if (bounds.isEmpty()) {
        fitCameraToScene(camera, root, controls);
        return;
      }

      applyCameraPreset({
        camera,
        controls,
        bounds,
        preset,
      });
    }

    function frameSelectedOrScene() {
      const sid = selectedIdRef.current;
      if (!sid) {
        frameScene();
        return;
      }

      const objectKey = String(sid).split("::")[0];
      const group = objectGroups.get(objectKey);

      if (group) frameSelected();
      else frameScene();
    }

    let ghost = null;

    function clearGhost() {
      if (!ghost) return;

      root.remove(ghost);
      ghost.traverse((n) => {
        if (n?.isMesh) {
          n.geometry?.dispose?.();
          const mat = n.material;
          if (Array.isArray(mat)) mat.forEach((m) => m?.dispose?.());
          else mat?.dispose?.();
        }
      });

      ghost = null;
    }

    function clearDecals() {
      for (const item of decalPlanes) {
        try {
          if (item?.proxy?.parent) item.proxy.parent.remove(item.proxy);
          if (item?.mesh?.parent) item.mesh.parent.remove(item.mesh);
          item.geometry?.dispose?.();
          item.material?.dispose?.();
        } catch {}
      }
      decalPlanes = [];

      for (const proxy of decalProxyById.values()) {
        try {
          if (proxy?.parent) proxy.parent.remove(proxy);
        } catch {}
      }

      decalProxyById.clear();
      decalBaseById.clear();

      while (decalsRoot.children.length) decalsRoot.remove(decalsRoot.children[0]);
    }

    function normalizeDecal(d) {
      const id = String(d?.id || "");
      const enabled = d?.enabled !== false;
      const targetId = String(d?.target_id || "");
      const assetRef = String(d?.asset_ref || d?.url || "");

      const pos = d?.position || {};
      const rot = d?.rotation_euler || {};
      const scl = d?.scale || {};

      const opacity = clamp01(d?.opacity ?? 1.0);
      const zOff = Number.isFinite(Number(d?.z_offset)) ? Number(d.z_offset) : 0.001;

      const sx = Number.isFinite(Number(scl.x)) ? Number(scl.x) : 1;
      const sy = Number.isFinite(Number(scl.y)) ? Number(scl.y) : 1;
      const sz = Number.isFinite(Number(scl.z)) ? Number(scl.z) : 1;

      return {
        id,
        enabled,
        targetId,
        assetRef,
        position: {
          x: Number.isFinite(Number(pos.x)) ? Number(pos.x) : 0,
          y: Number.isFinite(Number(pos.y)) ? Number(pos.y) : 0,
          z: Number.isFinite(Number(pos.z)) ? Number(pos.z) : 0,
        },
        rotation_euler: {
          x: Number.isFinite(Number(rot.x)) ? Number(rot.x) : 0,
          y: Number.isFinite(Number(rot.y)) ? Number(rot.y) : 0,
          z: Number.isFinite(Number(rot.z)) ? Number(rot.z) : 0,
        },
        scale: { x: sx, y: sy, z: sz },
        opacity,
        z_offset: zOff,
      };
    }

    async function getDecalTexture(assetRef) {
      if (!assetRef) return null;
      if (decalTextureCache.has(assetRef)) return decalTextureCache.get(assetRef);

      if (assetRef === "builtin://checker") {
        if (checkerTex) decalTextureCache.set(assetRef, checkerTex);
        return checkerTex;
      }

      let url = assetRef;
      if (!/^https?:\/\//i.test(assetRef)) {
        try {
          const resolved = await resolveAssetRef(assetRef);
          if (resolved) url = resolved;
        } catch {}
      }

      try {
        const tex = await textureLoader.loadAsync(url);
        tex.wrapS = THREE.ClampToEdgeWrapping;
        tex.wrapT = THREE.ClampToEdgeWrapping;
        tex.colorSpace = THREE.SRGBColorSpace;
        tex.needsUpdate = true;
        decalTextureCache.set(assetRef, tex);
        return tex;
      } catch (e) {
        console.warn("[ThreeSceneViewer] decal texture load failed:", {
          assetRef,
          url,
          error: String(e?.message || e),
        });
        if (checkerTex) {
          decalTextureCache.set(assetRef, checkerTex);
          return checkerTex;
        }
        return null;
      }
    }

    function applyDecalTransformFromBaseOrPreview(decalId) {
      const id = String(decalId || "");
      const proxy = decalProxyById.get(id);
      if (!proxy) return;

      const pv = decalPreviewRef.current?.patchById?.[id] || null;
      const base = decalBaseById.get(id) || null;

      const pos = pv?.position || base?.position;
      const rot = pv?.rotation_euler || base?.rotation_euler;
      const scl = pv?.scale || base?.scale;

      if (pos) proxy.position.set(Number(pos.x || 0), Number(pos.y || 0), Number(pos.z || 0));
      if (rot) {
        proxy.rotation.set(
          degToRad(Number(rot.x || 0)),
          degToRad(Number(rot.y || 0)),
          degToRad(Number(rot.z || 0))
        );
      }
      if (scl) proxy.scale.set(Number(scl.x || 1), Number(scl.y || 1), Number(scl.z || 1));
    }

    function applyAllDecalPreviewPatches() {
      for (const id of decalProxyById.keys()) {
        applyDecalTransformFromBaseOrPreview(id);
      }
    }

    function applyMaterialOverridesNow() {
      const overrides = materialOverridesRef.current;
      if (!overrides) return;
      try {
        Object.entries(objectGroups).forEach(([objectId, group]) => {
          if (!group) return;

          const override = overrides[objectId];
          if (!override) return;

          applyMaterialState(group, override, selectedIdRef.current);
        });
      } catch (e) {
        console.warn("[ThreeSceneViewer] material override apply failed:", String(e?.message || e));
      }
    }
    
// --------------------------------------------------
// ✅ Tier 7.69 — View Modes (paint-safe)
// --------------------------------------------------

function applyViewMode() {
  const vm = viewModeRef.current?.mode || "studio";

  // View modes must NEVER override materials.
  // Materials are controlled by:
  // - applyMaterialState()
  // - applyMaterialOverridesNow()
  // This keeps multi-part paint working.
}

    
    async function syncDecals() {
      const myNonce = ++decalsSyncNonceRef.current;

      clearDecals();

      const raw = decalsRef.current || [];
      if (!raw.length) return;

      const sorted = raw
        .map(normalizeDecal)
        .filter((d) => d.id && d.enabled && d.targetId)
        .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

      for (const d of sorted) {
        if (disposed) return;
        if (myNonce !== decalsSyncNonceRef.current) return;

        const objectKey = String(d.targetId).split("::")[0];
        const group = objectGroups.get(objectKey);
        if (!group) continue;
        if (group.visible === false) continue;

        const tex = await getDecalTexture(d.assetRef);
        if (disposed) return;
        if (myNonce !== decalsSyncNonceRef.current) return;

        const proxy = new THREE.Object3D();
        proxy.name = `decal-proxy:${d.id}`;

        proxy.position.set(d.position.x, d.position.y, d.position.z);
        proxy.rotation.set(
          degToRad(d.rotation_euler.x),
          degToRad(d.rotation_euler.y),
          degToRad(d.rotation_euler.z)
        );
        proxy.scale.set(d.scale.x, d.scale.y, d.scale.z);

        const geom = new THREE.PlaneGeometry(0.5, 0.5);
        const mat = new THREE.MeshBasicMaterial({
          map: tex || null,
          transparent: true,
          opacity: d.opacity,
          depthWrite: false,
        });

        const plane = new THREE.Mesh(geom, mat);
        plane.name = `decal:${d.id}`;
        plane.renderOrder = 1000;
        plane.position.set(0, 0, d.z_offset);
        plane.userData.pickId = `decal:${d.id}`;

        proxy.add(plane);
        group.add(proxy);

        pickablesRef.current.push(plane);

        decalPlanes.push({ proxy, mesh: plane, geometry: geom, material: mat });

        decalProxyById.set(d.id, proxy);
        decalBaseById.set(d.id, d);
      }

      if (disposed) return;
      if (myNonce !== decalsSyncNonceRef.current) return;

      applyAllDecalPreviewPatches();
    }

    function syncTransformControlsToTarget() {
      const mode = gizmoModeRef.current;
      transformControls.setMode(mode);
      applySnapToTransformControls();

      const gizmoEnabledNow = !disabled && !!canEditRef.current;
      transformControls.enabled = gizmoEnabledNow;

      if (!gizmoEnabledNow) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      const activeId = activeDecalIdRef.current;
      if (activeId) {
        const proxy = decalProxyById.get(String(activeId));
        if (proxy) {
          transformControls.attach(proxy);
          transformControls.visible = true;
          return;
        }
      }

      const sid = selectedIdRef.current;
      if (!sid) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      const { objectKey, meshPath } = parseSelectedId(sid);

      const group = objectGroups.get(String(objectKey));
      const pivotGroup = pivotGroups.get(String(objectKey));

      if (!group || group.visible === false) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      // ✅ mesh-level attach (correct pivot-safe)
      if (meshPath) {
        const parts = String(meshPath).split("/");
        const node = findNodeByMeshPath(group, parts);
        if (node) {
          const target = node;
          transformControls.attach(target);
          transformControls.visible = true;
          return;
        }
      }
            
      // fallback to object pivot
      if (!pivotGroup) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      transformControls.attach(pivotGroup);
      transformControls.visible = true;
    }
            
    function onGizmoDraggingChanged(e) {
      const dragging = !!e?.value;
      gizmoDragging = dragging;

      controls.enabled = !dragging;

      if (dragging) {
        dragSession += 1;
        committedForSession = false;
      }

      if (!dragging) {
        if (committedForSession) return;
        committedForSession = true;

        const activeId = activeDecalIdRef.current;
        const obj = transformControls.object;
        if (!activeId || !obj) return;

        const proxy = decalProxyById.get(String(activeId));
        if (!proxy) return;
        if (obj !== proxy) return;

        clearDecalPreviewPatch(activeId);

        const patch = {
          position: vec3Patch(proxy.position, 4),
          rotation_euler: eulerDegPatch(proxy.rotation, 2),
          scale: vec3Patch(proxy.scale, 4),
        };

        const commit = onCommitToolRef.current;
        if (typeof commit === "function") {
          commit({
            tool: "DECAL_UPDATE",
            station: "decor",
            payload: { decal_id: activeId, patch },
          });
        }
      }
    }
    transformControls.addEventListener("dragging-changed", onGizmoDraggingChanged);

    function onGizmoObjectChange() {
      const obj = transformControls.object;
      if (!obj) return;

      const activeId = activeDecalIdRef.current;
      if (!activeId) return;

      const proxy = decalProxyById.get(String(activeId));
      if (!proxy) return;
      if (obj !== proxy) return;

      if (!gizmoDragging) return;

      const space = transformSpaceRef.current;

      if (space === "pivot") {
        const sid = selectedIdRef.current;
        if (!sid) return;

        const primaryId = String(sid).split("::")[0];
        const pivotGroup = objectGroups.get(primaryId);
        if (!pivotGroup) return;

        if (gizmoModeRef.current === "translate") {
          const delta = obj.position.clone().sub(pivotGroup.position);
          obj.position.copy(pivotGroup.position.clone().add(delta));
        }

        if (gizmoModeRef.current === "rotate") {
          obj.quaternion.premultiply(pivotGroup.quaternion);
        }
      }

      // --------------------------------------------------
      // ✅ Tier 7.65 — GRID SNAP (FINAL, AFTER PIVOT)
      // --------------------------------------------------
      const snap = snapRef.current;

      if (
        snap.enabled &&
        snap.mode === "grid" &&
        gizmoModeRef.current === "translate"
      ) {
        const g = Number(snap.gridSize || 1);

        if (g > 0) {
          if (snap.axis_lock === "none" || snap.axis_lock === "x") {
            obj.position.x = Math.round(obj.position.x / g) * g;
          }
          if (snap.axis_lock === "none" || snap.axis_lock === "y") {
            obj.position.y = Math.round(obj.position.y / g) * g;
          }
          if (snap.axis_lock === "none" || snap.axis_lock === "z") {
            obj.position.z = Math.round(obj.position.z / g) * g;
          }
        }
      }

      setDecalPreviewPatch(activeId, {
        position: vec3Patch(proxy.position, 4),
        rotation_euler: eulerDegPatch(proxy.rotation, 2),
        scale: vec3Patch(proxy.scale, 4),
      });

      updatePivotPreview();
    }
    transformControls.addEventListener("objectChange", onGizmoObjectChange);
        
    function resize() {
      const r = container.getBoundingClientRect();
      const w = Math.max(1, Math.floor(r.width));
      const h = Math.max(1, Math.floor(r.height));
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      controls.update();
    }
    resize();
    const ro = new ResizeObserver(() => resize());
    ro.observe(container);

    function applyPreviewGhost() {
      clearGhost();
      const pv = previewRef.current;
      if (!pv) return;

      const targetId = pv.payload?.target_id || pv.target_id;
      if (!targetId) return;

      const objectKey = String(targetId).split("::")[0];
      const group = objectGroups.get(objectKey);
      if (!group) return;

      ghost = group.clone(true);
      ghost.name = `ghost:${group.name || objectKey}`;

      const ghostOpacity = 0.35;

      ghost.traverse((node) => {
        if (node?.isMesh && node.material) {
          const mats = Array.isArray(node.material) ? node.material : [node.material];
          const cloned = mats.map((m) => {
            const mm = m.clone();
            mm.transparent = true;
            mm.opacity = ghostOpacity;
            mm.depthWrite = false;
            mm.needsUpdate = true;
            return mm;
          });
          node.material = Array.isArray(node.material) ? cloned : cloned[0];
        }
      });

      const tool = pv.tool;
      const p = pv.payload || {};

      if (tool === "TRANSLATE") {
        const d = p.delta || {};
        ghost.position.x += Number(d.x || 0);
        ghost.position.y += Number(d.y || 0);
        ghost.position.z += Number(d.z || 0);
      } else if (tool === "ROTATE") {
        const degrees = Number(p.degrees || 0);
        const rad = (degrees * Math.PI) / 180;
        const axis = String(p.axis || "y");
        if (axis === "x") ghost.rotation.x += rad;
        else if (axis === "y") ghost.rotation.y += rad;
        else ghost.rotation.z += rad;
      } else if (tool === "SCALE") {
        const factor = Number(p.factor || 1);
        const axis = String(p.axis || "uniform");
        if (axis === "uniform") ghost.scale.multiplyScalar(factor);
        else if (axis === "x") ghost.scale.x *= factor;
        else if (axis === "y") ghost.scale.y *= factor;
        else ghost.scale.z *= factor;
      }
    }

    async function loadAll() {
      if (disposed) return;
      
      // ✅ USE RESOLVED OBJECTS FROM useMemo
      const objectsLocal = objects;

      // 🔥 FIRST — do NOT touch anything if no objects
      if (!objectsLocal.length) {
        console.log("⏸ waiting for objects...");
        return;
      }

      // 🔥 ONLY AFTER objects are valid — safe to reset
      setErr(null);

      if (!hasBuiltSceneRef.current) {
        if (!pickablesRef.current) {
          pickablesRef.current = [];
        }
        meshToObjectId.clear();
        meshToObjectKey.clear();
        objectGroups.clear();
        allMeshes.clear();
        pivotGroups.clear();
      }

      clearMaterialSlots();
      
      const sortedObjects = sortObjectsStable(objectsLocal);

      setLoadingCount(0);
      
      // 🔧 detach gizmo BEFORE cleanup
      transformControls.detach();
      transformControls.visible = false;

      // 🔥 HARD RESET — Tier 6G.20
      cleanupScene(root);

      // reattach persistent roots
      root.add(decalsRoot);

      const loader = new GLTFLoader();
      
      // 🚀 USE sortedObjects BELOW — DO NOT redeclare
      // --------------------------------------------------
      // PASS 1 — create all object groups deterministically
      // --------------------------------------------------
      for (const obj of sortedObjects) {
        if (disposed) return;

        const objId = String(obj?.id || "").trim();
        if (!objId) continue;

        if (obj?.enabled === false) {
          continue;
        }

        const kind = String(obj?.kind || "unknown");
        const cfg = layers.kinds[kind] || ensureKind(kind);

        const objectKey = objId;

      // ---------------------------------------
      // OUTER GROUP (world transform)
      // ---------------------------------------
      const outer = new THREE.Group();
      outer.name = `obj:${objectKey}`;
      outer.userData.kind = kind;
      outer.userData.pickId = `obj:${objectKey}`;
      outer.userData.objectId = objectKey;
      outer.visible = !!cfg.visible && obj?.enabled !== false;
      
      meshToObjectKey.set(outer, objectKey);
      meshToObjectId.set(outer, objId);

      applyTransformToObject3D(outer, obj.transform);

     // ---------------------------------------
     // PIVOT GROUP (local offset)
     // ---------------------------------------
     const pivotGroup = new THREE.Group();

     // snapshot pivot
     let pivot = obj?.pivot || null;

     // preview pivot overrides snapshot
     const preview = pivotPreviewRef.current;
     if (preview && preview.object_id === objectKey) {
       pivot = preview.pivot;
     }

     const px = Number(pivot?.x || 0);
     const py = Number(pivot?.y || 0);
     const pz = Number(pivot?.z || 0);

     // IMPORTANT: negative offset
     pivotGroup.position.set(-px, -py, -pz);

     // attach pivot inside outer
     outer.add(pivotGroup);
     
     // add to scene root
     root.add(outer);

     // store both
     objectGroups.set(objectKey, outer);
     pivotGroups.set(objectKey, pivotGroup);
   }

      // --------------------------------------------------
      // PASS 2 — attach hierarchy (Tier 7.51)
      // --------------------------------------------------
      for (const obj of sortedObjects) {
        if (disposed) return;

        const objId = String(obj?.id || "").trim();
        if (!objId) continue;
        if (obj?.enabled === false) continue;

        const group = objectGroups.get(objId);
        if (!group) continue;

        const parentId = normalizeParentId(obj?.parent_id);
        const parentGroup = parentId ? objectGroups.get(parentId) : null;

        if (parentGroup && parentGroup !== group) {
          parentGroup.add(group);
        } else {
          root.add(group);
        }
      }

      // keep decals root attached at root level
      if (decalsRoot.parent !== root) {
        root.add(decalsRoot);
      }

      // --------------------------------------------------
      // PASS 3 — load model refs / placeholders into groups
      // --------------------------------------------------
      for (const obj of sortedObjects) {
        if (disposed) return;

        const objId = String(obj?.id || "").trim();
        if (!objId) continue;

        const kind = String(obj?.kind || "unknown");
        const cfg = layers.kinds[kind] || ensureKind(kind);

        const objectKey = objId;
        const group = objectGroups.get(objectKey);
        if (!group) continue;

        const pivotGroup = pivotGroups.get(objectKey) || group;

        const assetRefRaw = obj?.asset_ref ?? obj?.url ?? null;

        const assetRef =
          typeof assetRefRaw === "string"
            ? assetRefRaw.trim()
            : assetRefRaw != null
              ? String(assetRefRaw).trim()
              : "";

        console.log("🧱 OBJECT ASSET CHECK:", {
          objectKey,
          raw: obj?.asset_ref,
          final: assetRef,
        });

        if (!assetRef) {
          const placeholder = makePlaceholderMesh(objectKey);
          placeholder.userData.objectId = objectKey;
          pivotGroup.add(placeholder);
          
          // ✅ APPLY SNAPSHOT MATERIAL
          applyMaterialState(placeholder, obj?.material_state || {});

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

          try {
            const mp = buildMeshPath(placeholder);
            if (mp) {
              setMeshPathsForObject(objectKey, [mp]);
              placeholder.userData.pickId = `mesh:${objectKey}::${mp}`;
              placeholder.userData.meshPath = mp;

              publishMaterialSlotsForMesh(objectKey, mp, placeholder.material);
            }
          } catch {}

          allMeshes.add(placeholder);

          if (cfg.pickable) {
            pickablesRef.current.push(placeholder);
            meshToObjectId.set(placeholder, objId);
            meshToObjectKey.set(placeholder, objectKey);
          }
          continue;
        }

        setLoadingCount((c) => c + 1);

        let finalUrl = null;

        try {

          // 🔥 detect asset change and clear old model
          const prev = loadedObjectsRef.current[objId];

          if (prev && prev.userData.assetRef !== assetRef) {          
            // 🔥 clear lifecycle tracking
            clearLoad(objectKey);
            if (prev) {
              pivotGroup.remove(prev);

              prev.traverse((n) => {
                if (n.isMesh) {
                  n.geometry?.dispose?.();

                  const mat = n.material;
                  if (Array.isArray(mat)) mat.forEach((m) => m?.dispose?.());
                  else mat?.dispose?.();
                }
              });
            }
            delete loadedObjectsRef.current[objId];
          }

          // 🔥 prevent reloading same object
        if (loadedObjectsRef.current[objId]) {
          console.log("⏭️ already loaded:", objId);

          const modelGroup = loadedObjectsRef.current[objId];

          // 🔥 ALWAYS reattach (viewer rebuild safe)
          pivotGroup.add(modelGroup);

          // 🔥 ensure visible
          modelGroup.visible = true;

          if (obj?.material_state) {

            applyMaterialState(
              modelGroup,
              obj.material_state
            );

            console.log("🎨 APPLY OBJECT (ALWAYS):", objId);

          }
          
          continue;
        }
          
          finalUrl = await resolveAssetRef(assetRef);
                              
          console.log("🧩 AFTER resolveAssetRef:", finalUrl);
          
          console.log("🧩 RESOLVE RESULT:", {
            assetRef,
            finalUrl,
          });

          if (!finalUrl) {
            throw new Error("asset_ref could not be resolved");
          }
          
          console.log("[ThreeSceneViewer] Loading GLB:", {
            assetRef,
            finalUrl,
          });

          const requestId = beginLoad(objectKey);

          const gltf = await loader.loadAsync(finalUrl);

          // 🚨 CRITICAL GUARD
          if (!isLoadValid(objectKey, requestId)) {
            console.warn("🧹 Discarding stale load:", objectKey);
            continue;
          }

          // 🔎 DEBUG — list meshes + ENABLE SHADOWS
          gltf.scene.traverse((n) => {
            if (n.isMesh) {
              console.log("MESH:", n.name);
              
              // ✅ PERFORMANCE FIXES
              n.frustumCulled = true;
              n.castShadow = false; 
              n.receiveShadow = true;
            }
          });

          console.log("✅ GLB LOADED SUCCESSFULLY:", {
            objId,
            finalUrl,
          });
          
          if (disposed) return;

          // 🔥 Tier 6G — authoritative group wrapper
          const modelGroup = new THREE.Group();
          modelGroup.name = `model:${objectKey}`;  
          modelGroup.userData.assetRef = assetRef;        
          
          pivotGroup.add(modelGroup);
          
          loadedObjectsRef.current[objId] = modelGroup;

          // ✅ CRITICAL — selection identity
          modelGroup.userData.objectId = objectKey;
          modelGroup.userData.pickId = `obj:${objectKey}`;

          modelGroup.add(gltf.scene);

          // 🔥 6G.16 — mesh role mapping
          const roleMap = buildMeshRoleMap(
            modelGroup,
            obj?.mesh_roles || {}
          );

          modelGroup.userData.roleMap = roleMap;

          // ✅ CRITICAL — store body mesh fallback
          modelGroup.userData.bodyMesh =
            roleMap.body ||
            modelGroup;

          console.log("ROLE MAP:", roleMap);         

          // 🔥 6G.15 — decals (object-level)
          await applyDecals(modelGroup, obj?.decal_state);   

          const meshPaths = [];

          modelGroup.traverse((node) => {
            if (!node || !node.isMesh) return;

            console.log("TRAVERSE NODE:", node);

            node.userData.objectId = objectKey;

            const meshName =
              node.name && node.name.trim()
                ? node.name
                : `mesh_${meshIndexRef.current.size}`;

            const meshId = `mesh:${objectKey}::${meshName}`;

            node.userData.pickId = meshId;
            node.userData.meshPath = meshName;

            // 🔥 register mesh index (ONLY ONCE)
            meshIndexRef.current.set(meshId, node);
            
            console.log("🔥 OBJECT MATERIAL STATE:", obj?.material_state);
            
            // --------------------------------------------------
            // 🔥 ROLE-BASED MATERIAL APPLY (NEW — MUST BE FIRST)
            // --------------------------------------------------

            const roleState = obj?.material_state?.roles || {};
            const roleMap = modelGroup.userData.roleMap;

            if (roleMap && Object.keys(roleState).length) {

              for (const [role, nodes] of Object.entries(roleMap)) {

                if (!nodes.includes(node)) continue;

                const state = roleState[role];
                if (!state) continue;

                console.log("🎯 ROLE APPLY:", role, "→", node.name);

                const resolved = resolvePreset(state.preset);

                if (!resolved) {
                  console.warn("❌ UNKNOWN ROLE PRESET:", state.preset);
                  continue;
                }

                applyMaterialState(node, {
                  paint: {
                    ...resolved,
                    ...state.params
                  }
                });

                if (node.material) {
                  const mats = Array.isArray(node.material)
                    ? node.material
                    : [node.material];

                  mats.forEach((m) => {
                    if (!m) return;

                    m.userData = m.userData || {};

                    if (!m.userData.__compiled) {
                      m.needsUpdate = true;
                      m.userData.__compiled = true;
                    }
                  });
                }

                console.log("🎨 ROLE MATERIAL APPLIED:", role);

                break; // ✅ exit role loop only
              }

            }         
            
            if (obj?.material_state?.meshes) {

              const meshes = obj.material_state.meshes;

              const expected = `mesh:${objectKey}::${meshName}`;

              console.log("CHECKING:", expected);
              console.log("AVAILABLE:", meshes);

              const exactKey = `mesh:${objectKey}::${meshName}`;

              const normalize = (s) =>
                String(s || "").toLowerCase().trim();

              const state =
                meshes[exactKey] ||                         // exact match
                Object.entries(meshes).find(([k]) => {      // strict normalized match
                  const keyMeshName =
                    normalize(k).split("::")[1] || "";

                  const nodeName = normalize(meshName);

                  return keyMeshName === nodeName;
                })?.[1];
              
              if (state) {
              
                console.log("🎯 APPLYING TO NODE:", node.name);

                console.log("🎯 APPLYING (ALWAYS):", exactKey, state);

                const resolved = resolvePreset(state.preset);

                if (!resolved) {
                  console.warn("❌ UNKNOWN PRESET:", state.preset);
                  return;
                }

                applyMaterialState(node, {
                  paint: {
                    ...resolved,
                    ...state.params
                  }
                });

                if (node.material) {
                  const mats = Array.isArray(node.material)
                    ? node.material
                    : [node.material];

                  mats.forEach((m) => {
                    if (!m) return;

                    m.userData = m.userData || {};

                    if (!m.userData.__compiled) {
                      m.needsUpdate = true;
                      m.userData.__compiled = true;
                    }
                  });
                }

                console.log("🎨 MATERIAL APPLIED:", exactKey);

              }

            } // ✅ CLOSE material_state.meshes BLOCK

            // 🔥 APPLY OPACITY SAFELY
            if (node.material) {
              applyOpacityToMaterial(node.material, cfg.opacity);
            }

            // ✅ register mesh
            allMeshes.add(node);

            // 🔥 ADD PICKABLE (MUST BE INSIDE)
            if (!pickablesRef.current.includes(node)) {
              pickablesRef.current.push(node);
            }
            meshToObjectKey.set(node, objectKey);
            meshToObjectId.set(node, objId);

            console.log("✅ ADDING PICKABLE:", node);

            // 🔥 BUILD MESH PATHS (INSIDE)
            try {
              const mp = node.name;

              meshPaths.push(mp);

              publishMaterialSlotsForMesh(
                objectKey,
                mp,
                node.material
              );
            } catch (err) {
              console.warn("mesh path build failed:", err);
            }

            console.log("✅ MESH FOUND:", node);

          });

          // ✅ publish mesh paths AFTER traverse
          if (meshPaths.length) {
            setMeshPathsForObject(objectKey, meshPaths);
          }

          const placeholder = makePlaceholderMesh(`${objectKey} (failed)`);
          placeholder.userData.objectId = objectKey;
          pivotGroup.add(placeholder);

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

          try {
            const mp = buildMeshPath(placeholder);
            if (mp) {
              setMeshPathsForObject(objectKey, [mp]);
              placeholder.userData.pickId = `mesh:${objectKey}::${mp}`;
              placeholder.userData.meshPath = mp;

              publishMaterialSlotsForMesh(
                objectKey,
                mp,
                placeholder.material
              );
            }
          } catch {}

          allMeshes.add(placeholder);

          if (cfg.pickable) {
            pickablesRef.current.push(placeholder);
            meshToObjectId.set(placeholder, objId);
            meshToObjectKey.set(placeholder, objectKey);
          }

          setErr((prev) => prev || String(err?.message || err));
          
        } finally {
          if (!disposed) {
            setLoadingCount((c) => Math.max(0, c - 1));
          }
        }
      }
      applyMaterialOverridesNow();
      applyViewMode();
      applyPreviewGhost();
      frameScene();

      await syncDecals();

      syncTransformControlsToTarget();
      applySnapToTransformControls();

      requestAnimationFrame(() => {
        viewerApiRef.current?.syncSelection?.();
      });
      
      console.log("📦 FINAL PICKABLES:", pickablesRef.current.length);
    }

    if (objects.length) {
      loadAll();
    }  
        
// --------------------------------------------------
// ✅ Tier 7.62 — Marquee selection computation
// --------------------------------------------------

function computeMarqueeSelection(start, end) {
  const rect = {
    minX: Math.min(start.x, end.x),
    maxX: Math.max(start.x, end.x),
    minY: Math.min(start.y, end.y),
    maxY: Math.max(start.y, end.y),
  };

  const results = new Set();

  const width = renderer.domElement.clientWidth;
  const height = renderer.domElement.clientHeight;

  root?.traverse((obj) => {
    if (!obj || !obj.isMesh) return;
    if (!obj.visible) return;

    const objectId = obj.userData?.objectId;
    if (!objectId) return;

    const pos = obj.getWorldPosition(new THREE.Vector3());
    pos.project(camera);

    const x = (pos.x * 0.5 + 0.5) * width;
    const y = (-pos.y * 0.5 + 0.5) * height;

    if (
      x >= rect.minX &&
      x <= rect.maxX &&
      y >= rect.minY &&
      y <= rect.maxY
    ) {
      results.add(String(objectId));
    }
  });

  return Array.from(results).sort();
}
    function buildPickIdListFromIntersects(intersects) {
      const ids = [];

      for (const h of intersects || []) {
        const obj = h?.object;
        if (!obj) continue;

        const direct = obj.userData?.pickId;
        if (direct) ids.push(String(direct));

        const objectKey = resolveObjectKeyFromHitMesh(obj);
        if (objectKey) ids.push(`obj:${String(objectKey)}`);

        try {
          const ok = objectKey ? String(objectKey) : null;
          if (ok) {
            const idNode = pickIdNodeForMeshPath(obj);
            const legacySelectedId = buildPickedTargetId({
              objectId: ok,
              mesh: idNode,
              includeMesh: true,
            });
            if (legacySelectedId && String(legacySelectedId).includes("::")) {
              ids.push(`mesh:${String(legacySelectedId)}`);
            }
          }
        } catch {}

        if (obj.userData?.pickId && String(obj.userData.pickId).startsWith("decal:")) {
          ids.push(String(obj.userData.pickId));
        }
      }

      return ids.filter(Boolean);
    }

    function setPrimaryObjectSelection(objectId) {
      const oid = String(objectId || "").trim();
      if (!oid) return;
      setPrimarySelection(oid);
      syncPrimaryToSingleSelection(oid);
      setSelectedId(oid);
      console.log("🔥 FINAL SELECTED ID:", oid);
    }

    function toggleObjectSelection(objectId) {
      const oid = String(objectId || "").trim();
      if (!oid) return;
      toggleMultiSelection(oid, true);
      syncPrimaryToSingleSelection(oid);
      setSelectedId(oid);
      console.log("🔥 TOGGLED SELECTED ID:", oid);
    }
    
// --------------------------------------------------
// ✅ Tier 7.62 — Marquee (Box Select)
// --------------------------------------------------

function handleMouseDown(e) {
  console.log("🧪 MOUSEDOWN FIRED");
  if (contextLost) return;
  if (e.button !== 0) return;

  isDraggingRef.current = true;

  const point = {
    x: e.clientX,
    y: e.clientY,
  };

  dragStartRef.current = point;

  startMarquee(point);
}

function handleMouseMove(e) {
  if (!isDraggingRef.current) return;

  updateMarquee({
    x: e.clientX,
    y: e.clientY,
  });
}

function handleMouseUp(e) {
  if (!isDraggingRef.current) return;

  isDraggingRef.current = false;

  const snap = marqueeGetSnapshot();
  const start = snap.start;
  const end = snap.end;

  endMarquee();

  if (!start || !end) return;

  // ignore tiny drags (treat as click)
  const dx = Math.abs(end.x - start.x);
  const dy = Math.abs(end.y - start.y);
  if (dx < 4 && dy < 4) {
    onClick(e); // 🔥 MANUAL CLICK
    return;
  }

  const selected = computeMarqueeSelection(start, end);

  const additive = !!(e.shiftKey || e.ctrlKey || e.metaKey);

  if (additive) {
    selected.forEach((id) => toggleMultiSelection(id, false));
  } else {
    setMultiSelection(selected, selected[0] || null);
    if (selected[0]) {
      syncPrimaryToSingleSelection(selected[0]);
    }
  }
}

function onClick(e) {
  console.log("🔥 CLICK EVENT FIRED", e.clientX, e.clientY);
  console.log("🧪 SELECTED ID STATE:", selectedIdRef.current);

  if (contextLost) return;

  const rect = canvas.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
  const y = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
  mouse.set(x, y);

  raycaster.setFromCamera(mouse, camera);

  console.log("🧪 PICKABLES COUNT:", pickablesRef.current.length);

  const mesh = pickObject(raycaster, pickablesRef.current);
  
  if (!mesh) {
    clearAllSelectionState?.();
    clearActiveDecalId?.();

    requestAnimationFrame(() => {
      updateSelectionBox();
      updateSelectionHighlight?.();
      syncTransformControlsToTarget();
    });

    return;
  }

  const additive = !!(e.shiftKey || e.ctrlKey || e.metaKey);

  if (mesh?.userData?.pickId?.startsWith("mesh:")) {

    // ✅ ALWAYS USE FIRST HIT (REAL CLICK TARGET)
    if (!mesh) return;

    const meshId = mesh.userData?.pickId;

    // 🔥 FIX — derive objectKey from mesh FIRST
    const objectKey = resolveObjectKeyFromHitMesh(mesh);

    if (!objectKey) {
      console.warn("❌ Failed to resolve objectKey from mesh");
      return;
    }
    
    const group = objectGroups.get(objectKey);
    const roleMap = group?.userData?.roleMap;

    // 🔥 find role
    let matchedRole = null;

    if (roleMap) {
      for (const [role, meshes] of Object.entries(roleMap)) {
        if (meshes.includes(mesh)) {
          matchedRole = role;
          break;
        }
      }
    }

    console.log("🎯 ROLE DETECTED:", matchedRole);

    console.log("🧪 ACTIVE PAINT:", activePaintRef.current);
    console.log("🧪 CLICKED MESH:", meshId);

    if (!meshId) return;

    setSelectedId(meshId);
    selectedIdRef.current = meshId;

    // 🔥 APPLY PAINT ON CLICK
    const paint = activePaintRef.current;

    console.log("🧪 CLICK PAINT REF:", paint);

    if (!paint) {
      console.warn("⚠️ NO ACTIVE PAINT — skipping paint");
    } else {
      const presetId =
        paint.id ||
        paint.preset_id ||
        paint?.presetId ||
        paint?.key ||
        paint?.name;

      if (!presetId) {
        console.warn("❌ INVALID PAINT OBJECT:", paint);
      } else if (!meshId || !meshId.startsWith("mesh:")) {
        console.warn("❌ INVALID MESH ID:", meshId);
      } else {
        console.log("🔥 APPLYING PAINT:", presetId, "→", meshId);

        onCommitToolRef.current?.({
          tool: "PAINT_APPLY_LIBRARY_PRESET",
          station: "materials",
          payload: {
            target_id: matchedRole
              ? `role:${objectKey}::${matchedRole}`
              : meshId,
            preset_id: presetId,
          },
        });

        // 🔥 FORCE MATERIAL REFRESH
        appliedMeshesRef.current.clear();
        appliedObjectsRef.current.clear();

        viewerApiRef.current?.syncMaterials?.();

        // 🔥 REBUILD PICKABLES AFTER MATERIAL UPDATE
        requestAnimationFrame(() => {
          pickablesRef.current = [];

          objectGroups.forEach((group) => {
            group.traverse((node) => {
              if (node.isMesh) {
                pickablesRef.current.push(node);
              }
            });
          });

          console.log("📦 REBUILT PICKABLES:", pickablesRef.current.length);
       });
      }
    }
    
    if (additive) {
      toggleMultiSelection(meshId, true);
    } else {
      setPrimarySelection(meshId);
    }

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        updateSelectionBox();
        updateSelectionHighlight?.();
        syncTransformControlsToTarget();
      });
    });

    console.log("✅ SELECTED (mesh):", meshId);
    return;
  }
  
  const objectKey = resolveObjectKeyFromHitMesh(mesh);
  if (!objectKey) return;
  
  // fallback (object selection)
  setSelectedId(objectKey);
  selectedIdRef.current = objectKey;

  setPrimarySelection(objectKey);
  syncPrimaryToSingleSelection(objectKey);

  requestAnimationFrame(() => {
    updateSelectionBox();
    updateSelectionHighlight?.();
    syncTransformControlsToTarget();
  });

  console.log("✅ SELECTED (object):", objectKey);
}
    
    function onDoubleClick(e) {
      if (contextLost) return;
      
      const r = canvas.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 2 - 1;
      const y = -(((e.clientY - r.top) / r.height) * 2 - 1);
      mouse.set(x, y);

      raycaster.setFromCamera(mouse, camera);

      const mesh = pickObject(raycaster, pickablesRef.current);

      if (!mesh) {
        frameScene();
        return;
      }

      const pickId = mesh.userData?.pickId;

      if (pickId?.startsWith("decal:")) {
        const decalId = pickId.replace("decal:", "");

        setActiveDecalId?.(decalId);
        clearAllSelectionState?.();

        const base = decalBaseById.get(decalId);
        const ownerKey = base?.targetId ? String(base.targetId).split("::")[0] : null;
        const group = ownerKey ? objectGroups.get(ownerKey) : null;

        if (group) frameSelected();
        else frameScene();

        return;
      }

      clearActiveDecalId?.();

      const objectKey = resolveObjectKeyFromHitMesh(mesh);
      if (!objectKey) {
        frameScene();
        return;
      }

      const meshId = mesh.userData?.pickId;

      if (meshId && meshId.startsWith("mesh:")) {
        setSelectedId(meshId);
        selectedIdRef.current = meshId;

        frameSelected();
        return;
      }
            
      setPrimaryObjectSelection(objectKey);

      const group = objectGroups.get(objectKey);
      if (group) frameSelected();
      else frameScene();
    }

    function onKeyDown(e) {
      const key = String(e.key || "").toLowerCase();

      // Tier 7.77 — gizmo mode switching
      if (key === "w") {
        e.preventDefault();
        transformControls.setMode("translate");
        viewerApiRef.current?.syncMode?.();
        return;
      }

      if (key === "e") {
        e.preventDefault();
        transformControls.setMode("rotate");
        viewerApiRef.current?.syncMode?.();
        return;
      }

      if (key === "r") {
        e.preventDefault();
        transformControls.setMode("scale");
        viewerApiRef.current?.syncMode?.();
        return;
      }

      if (key === "f" && !e.shiftKey) {
        e.preventDefault();
        frameSelected();
      } else if (key === "f" && e.shiftKey) {
        e.preventDefault();
        frameScene();
      }
    }
    
    canvas.addEventListener("mousedown", handleMouseDown);
    canvas.addEventListener("mousemove", handleMouseMove);
    canvas.addEventListener("mouseup", handleMouseUp);

    canvas.addEventListener("click", onClick);  
    canvas.addEventListener("dblclick", onDoubleClick);
    window.addEventListener("keydown", onKeyDown);   
    
    let raf = 0;
    function tick() {
      raf = requestAnimationFrame(tick);
      if (contextLost) return;
      
      updatePivotPreview();
      
      controls.update();
      renderer.render(scene, camera);
    }
    tick();

    // --------------------------------------------------
    // ✅ Tier 7.61 — Pivot preset computation (FINAL)
    // --------------------------------------------------

    function computeObjectBoundsById(objectId) {
      const id = String(objectId || "").trim();
      if (!id) return new THREE.Box3().makeEmpty();

      const group = objectGroups.get(id);
      if (!group || group.visible === false) {
        return new THREE.Box3().makeEmpty();
      }

      const box = new THREE.Box3();
      box.setFromObject(group);

      return box;
    }

    function getPivotPresetForObject(objectId, preset) {
      try {
        const box = computeObjectBoundsById(objectId);

        if (!box || box.isEmpty()) {
          return { x: 0, y: 0, z: 0 };
        }

        return boxToPivotPreset(box, preset);
      } catch (e) {
        console.warn("[ThreeSceneViewer] pivot preset failed:", {
          objectId,
          preset,
          error: String(e?.message || e),
        });
        return { x: 0, y: 0, z: 0 };
      }
    }

    // --------------------------------------------------
    // Viewer API wiring
    // --------------------------------------------------

    viewerApiRef.current.syncSelection = () => {   
      updateSelectionBox();
      updateSelectionHighlight();
      syncTransformControlsToTarget();
    };

    viewerApiRef.current.syncPreview = () => {
      applyPreviewGhost();
    };

    viewerApiRef.current.syncMode = () => {
      syncTransformControlsToTarget();
      applySnapToTransformControls();
    };

    viewerApiRef.current.syncEditGate = () => {
      syncTransformControlsToTarget();
      applySnapToTransformControls();
    };

    viewerApiRef.current.syncDecals = () => {
      syncDecals().then(() => {
        syncTransformControlsToTarget();
        applySnapToTransformControls();
      });
    };

    viewerApiRef.current.syncDecalPreview = () => {
      applyAllDecalPreviewPatches();
    };

    viewerApiRef.current.syncDecalTarget = () => {
      syncTransformControlsToTarget();
      applySnapToTransformControls();
    };

    viewerApiRef.current.syncPickFilter = () => {};

    viewerApiRef.current.syncMaterials = () => {

      // 🔥 ALWAYS RESET (no caching)
      appliedMeshesRef.current.clear();
      appliedObjectsRef.current.clear();

      applyMaterialOverridesNow();

      // 🔥 REAPPLY SNAPSHOT MATERIAL (FORCE EVERY TIME)
      objectGroups.forEach((group, objectId) => {
        const obj = objects.find(
          (o) => String(o.id) === String(objectId)
        );

        if (!obj) return;

        if (obj.material_state) {

          applyMaterialState(
            group,
            obj.material_state,
            selectedIdRef.current
          );

          console.log("🎨 APPLY OBJECT (FORCED):", objectId);
        }

      });

      updateSelectionHighlight();
      updateSelectionBox();
      syncTransformControlsToTarget();
    };
        
    viewerApiRef.current.syncSnap = () => {
      applySnapToTransformControls();
    };
    
    viewerApiRef.current.syncViewMode = () => {
      applyViewMode();
    };
    
    viewerApiRef.current.syncPivotPreview = () => {
      updatePivotPreview();
    };

    viewerApiRef.current.frameSelected = () => {
      frameSelected();
    };

    viewerApiRef.current.frameScene = () => {
      frameScene();
    };

    viewerApiRef.current.applyPreset = (preset) => {
      applyPreset(preset);
    };

    // ✅ Tier 7.61 — expose pivot API
    viewerApiRef.current.getPivotPresetForObject = (objectId, preset) =>
      getPivotPresetForObject(objectId, preset);

    // --------------------------------------------------
    // Expose viewer API (FULL)
    // --------------------------------------------------

    onViewerApiReadyRef.current?.({
      frameSelected: viewerApiRef.current.frameSelected,
      frameScene: viewerApiRef.current.frameScene,
      applyPreset: viewerApiRef.current.applyPreset,
      getPivotPresetForObject: viewerApiRef.current.getPivotPresetForObject,
    });

    // --------------------------------------------------
    // Initial sync
    // --------------------------------------------------

    viewerApiRef.current.syncSelection?.();
    viewerApiRef.current.syncPreview?.();
    viewerApiRef.current.syncDecals?.();
    viewerApiRef.current.syncMaterials?.();
    viewerApiRef.current.syncSnap?.();

    // --------------------------------------------------
    // Cleanup
    // --------------------------------------------------

    return () => {
      disposed = true;
      Object.keys(loadedObjectsRef.current).forEach((objectId) => {
        clearLoad(objectId);    
      });
      
      cancelAnimationFrame(raf);

      viewerApiRef.current.syncSelection = null;
      viewerApiRef.current.syncPreview = null;
      viewerApiRef.current.syncMode = null;
      viewerApiRef.current.syncEditGate = null;
      viewerApiRef.current.syncDecals = null;
      viewerApiRef.current.syncDecalPreview = null;
      viewerApiRef.current.syncDecalTarget = null;
      viewerApiRef.current.syncPickFilter = null;
      viewerApiRef.current.syncMaterials = null;
      viewerApiRef.current.syncSnap = null;
      viewerApiRef.current.frameSelected = null;
      viewerApiRef.current.frameScene = null;
      viewerApiRef.current.applyPreset = null;

      // ✅ Tier 7.61 cleanup
      viewerApiRef.current.getPivotPresetForObject = null;

      onViewerApiReadyRef.current?.(null);

      clearGhost();
      clearSelectionBox();
      clearDecals();
      clearMaterialSlots();

      for (const [k, tex] of decalTextureCache.entries()) {
        if (k === "builtin://checker") continue;
        try {
          tex?.dispose?.();
        } catch {}
      }

      try {
        checkerTex?.dispose?.();
      } catch {}

      transformControls.removeEventListener("dragging-changed", onGizmoDraggingChanged);
      transformControls.removeEventListener("objectChange", onGizmoObjectChange);
      transformControls.detach();
      scene.remove(transformControls);

      controls.dispose();

      canvas.removeEventListener("mousedown", handleMouseDown);
      canvas.removeEventListener("mousemove", handleMouseMove);
      canvas.removeEventListener("mouseup", handleMouseUp);

      canvas.removeEventListener("click", onClick);
      canvas.removeEventListener("dblclick", onDoubleClick);
      
      window.removeEventListener("keydown", onKeyDown);

      ro.disconnect();

      root.traverse((node) => {
        if (node?.isMesh) {
          node.geometry?.dispose?.();
          const mat = node.material;
          if (Array.isArray(mat)) mat.forEach((m) => m?.dispose?.());
          else mat?.dispose?.();
        }
      });

      canvas.removeEventListener("webglcontextlost", onContextLost);
      canvas.removeEventListener("webglcontextrestored", onContextRestored);

      if (rendererRef.current) {
        rendererRef.current.dispose();
        rendererRef.current = null;
      }
    };

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [objects, disabled, layers.kinds, materialOverrides]);
    
  // -----------------------------------------
  // NEXT EFFECT (MUST START CLEAN)
  // -----------------------------------------
  useEffect(() => {
    viewerApiRef.current?.syncSelection?.();
  }, [selectedId]);

  useEffect(() => {
    viewerApiRef.current?.syncMode?.();
  }, [gizmoMode, transformSpace]);

  useEffect(() => {
    viewerApiRef.current?.syncSnap?.();
  }, [snapState, transformSpace]);

  useEffect(() => {
    viewerApiRef.current?.syncPreview?.();
  }, [preview]);

  useEffect(() => {
    viewerApiRef.current?.syncEditGate?.();
  }, [canEdit]);

  useEffect(() => {
    viewerApiRef.current?.syncDecals?.();
  }, [objects]);

  useEffect(() => {
    viewerApiRef.current?.syncDecalTarget?.();
  }, [activeDecalId]);

  useEffect(() => {
    viewerApiRef.current?.syncDecalPreview?.();
  }, [decalPreview]);

  useEffect(() => {
    viewerApiRef.current?.syncPickFilter?.();
  }, [selectionFilter]);

  useEffect(() => {
    viewerApiRef.current?.syncMaterials?.();
  }, [materialOverrides]);
  
  useEffect(() => {
    viewerApiRef.current?.syncViewMode?.();
  }, [viewMode]);
  
  useEffect(() => {
    viewerApiRef.current?.syncPivotPreview?.();
  }, [pivotPreview]);

useEffect(() => {
  onViewerApiReadyRef.current?.({
    frameSelected: viewerApiRef.current?.frameSelected || null,
    frameScene: viewerApiRef.current?.frameScene || null,
    applyPreset: viewerApiRef.current?.applyPreset || null,

    // ✅ FIX: keep Tier 7.61 API alive
    getPivotPresetForObject:
      viewerApiRef.current?.getPivotPresetForObject || null,
  });
}, [onViewerApiReady, selectedId]);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Viewport (Three.js)</div>
        <div className="text-xs opacity-75">Selected: {selectedId || "none"}</div>
      </div>

      {err ? <div className="text-sm text-red-600">{err}</div> : null}
      {loadingCount > 0 ? (
        <div className="text-sm opacity-75">Loading assets… ({loadingCount})</div>
      ) : null}

      {!objects.length ? (
        <div className="text-sm opacity-75">
          No objects in scene index yet. Attach an asset (6G.2) or ensure body_state.scene.objects[]
          exists.
        </div>
      ) : null}

      <div
        ref={containerRef}
        className="border rounded overflow-hidden h-full w-full"
      >
        <canvas ref={canvasRef} style={{ width: "100%", height: "100%", display: "block" }} />
      </div>

      <div className="text-xs opacity-70">
        Click to select (Tier 7.41 filter applies). Double-click to focus. Press <b>F</b> to frame
        selected and <b>Shift+F</b> to frame the full scene. Orbit/pan/zoom now use{" "}
        <code>OrbitControls</code> (7.48). TransformControls mode is synced with the panel.
        Bounding box shows selection target (6G.9). If an active decal is selected (7.38), the
        gizmo targets the decal proxy first. Decals are pickable (7.41) via deterministic pick
        resolution. If <code>materialOverrides</code> are provided (7.42), they are applied after
        load and on updates (viewer-safe, no remount). Scene outliner visibility is respected via{" "}
        <code>object.enabled</code> (7.47). Model refs can load from <code>asset_ref</code> or{" "}
        <code>url</code> (7.46). Snap settings now also drive TransformControls space and snap
        increments (7.49) without remounting the viewer. Parent/child object transforms are now
        respected through scene graph attachment when <code>parent_id</code> exists (7.51). Material
        slot metadata is now also discovered per mesh and published to the slot inspector store
        without mutating snapshots (7.53). Viewport picking now supports additive multi-object
        selection with shift/ctrl/cmd while keeping primary single-selection flows compatible (7.60).
      </div>
    </div>
  );
}
