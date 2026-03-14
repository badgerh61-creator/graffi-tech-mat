// frontend/src/editor/scene/ThreeSceneViewer.jsx
import React, { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

// ✅ Step 1 — TransformControls (Three.js handles)
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";

// ✅ Tier 7.48 — Orbit camera controls
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

import { resolveAssetRef } from "./resolveAssetRef";
import { buildPickedTargetId } from "./pickingId";
import { applyTransformToObject3D, makePlaceholderMesh } from "./applyTransform";
import { clearSelection, setSelectedId, useSelection } from "../selection/selectionStore";

// ✅ Tier 7.60 — multi-select bridge/store
import {
  toggleMultiSelection,
  setPrimarySelection,
} from "../selection/multiSelectionStore";
import {
  syncPrimaryToSingleSelection,
  clearAllSelectionState,
} from "../selection/multiSelectionBridge";

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

// ✅ Tier 7.38 — active decal + preview patch store
import { useActiveDecal } from "../decals/activeDecalStore";
import {
  useDecalPreview,
  setDecalPreviewPatch,
  clearDecalPreviewPatch,
} from "../decals/decalPreviewStore";

// ✅ Tier 7.41 — selection filters + deterministic pick resolution
import { useSelectionFilter } from "../selection/selectionFilterStore";
import { resolvePick } from "../selection/resolvePick";

// ✅ Tier 7.41 — set/clear active decal (optional, safe)
import { setActiveDecalId, clearActiveDecalId } from "../decals/activeDecalStore";

// ✅ Tier 7.42 — Material overrides (read + apply) (optional, additive-safe)
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

function makeRenderer(canvas) {
  const gl2 = canvas.getContext("webgl2", { antialias: true });
  const gl1 = gl2 ? null : canvas.getContext("webgl", { antialias: true });
  const gl = gl2 || gl1;
  if (!gl) return null;

  const r = new THREE.WebGLRenderer({
    canvas,
    context: gl,
    antialias: true,
    alpha: true,
    preserveDrawingBuffer: false,
  });

  r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  r.outputColorSpace = THREE.SRGBColorSpace;
  r.toneMapping = THREE.ACESFilmicToneMapping;
  r.toneMappingExposure = 1.0;
  r.physicallyCorrectLights = true;

  return r;
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

function addStudioLighting(scene) {
  const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 0.9);
  hemi.name = "light:hemi";
  scene.add(hemi);

  const key = new THREE.DirectionalLight(0xffffff, 1.1);
  key.name = "light:key";
  key.position.set(6, 8, 5);
  scene.add(key);

  const fill = new THREE.DirectionalLight(0xffffff, 0.35);
  fill.name = "light:fill";
  fill.position.set(-6, 5, -4);
  scene.add(fill);

  const rim = new THREE.DirectionalLight(0xffffff, 0.25);
  rim.name = "light:rim";
  rim.position.set(0, 6, -8);
  scene.add(rim);
}

function normalizeSnapState(raw) {
  const snap = raw || {};
  return {
    enabled: !!snap.enabled,
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
 */
export default function ThreeSceneViewer({
  sceneIndex,
  disabled = false,
  canEdit = true,
  onCommitTool = null,
  materialOverrides = null,
  onViewerApiReady = null,
}) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  const { selectedId } = useSelection();

  const layers = useSceneLayers();
  const { preview } = useGizmoPreview();
  const { mode: gizmoMode } = useGizmoMode();

  // ✅ Tier 7.49
  const snapState = useSnap().snap;

  const { decalId: activeDecalId } = useActiveDecal();
  const decalPreview = useDecalPreview();

  const { filter: selectionFilter } = useSelectionFilter();

  const [err, setErr] = useState(null);
  const [loadingCount, setLoadingCount] = useState(0);

  const objects = useMemo(() => {
    const a = sceneIndex?.objects;
    const b = sceneIndex?.body_state?.objects;
    const c = sceneIndex?.snapshot?.body_state?.objects;
    const d = sceneIndex?.activeSnapshot?.body_state?.objects;
    const list = a || b || c || d || [];
    return Array.isArray(list) ? list.filter(Boolean) : [];
  }, [sceneIndex]);

  const decals = useMemo(() => {
    const d1 = sceneIndex?.decor_state?.decals;
    const d2 = sceneIndex?.snapshot?.decor_state?.decals;
    const d3 = sceneIndex?.activeSnapshot?.decor_state?.decals;
    const list = d1 || d2 || d3 || [];
    return Array.isArray(list) ? list.filter(Boolean) : [];
  }, [sceneIndex]);

  const selectedIdRef = useRef(selectedId);
  const previewRef = useRef(preview);
  const gizmoModeRef = useRef(gizmoMode);

  // ✅ Tier 7.49 snap ref
  const snapRef = useRef(normalizeSnapState(snapState));

  const canEditRef = useRef(!!canEdit);
  const decalsRef = useRef(decals);
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

  useEffect(() => {
    canEditRef.current = !!canEdit;
  }, [canEdit]);

  useEffect(() => {
    decalsRef.current = decals;
  }, [decals]);

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
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    clearMeshIndex();
    clearMaterialSlots();

    let disposed = false;

    const scene = new THREE.Scene();

    const renderer = makeRenderer(canvas);
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

    const rect = container.getBoundingClientRect();
    const camera = makeCamera(rect.width || 800, rect.height || 500);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.screenSpacePanning = true;
    controls.target.set(0, 0.8, 0);
    controls.update();

    const transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.setMode(gizmoModeRef.current);

    const gizmoEnabled = !disabled && !!canEditRef.current;
    transformControls.enabled = gizmoEnabled;
    transformControls.visible = false;
    scene.add(transformControls);

    function applySnapToTransformControls() {
      const snap = normalizeSnapState(snapRef.current);

      transformControls.setSpace(snap.orientation === "world" ? "world" : "local");

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

    const objectGroups = new Map();
    const allMeshes = new Set();

    function updateSelectionBox() {
      clearSelectionBox();

      const sid = selectedIdRef.current;
      if (!sid) return;

      const { objectKey, meshPath } = parseSelectedId(sid);
      if (!objectKey) return;

      const group = objectGroups.get(String(objectKey));
      if (!group) return;
      if (group.visible === false) return;

      let target = group;

      if (meshPath) {
        const node = findNodeByMeshPath(group, meshPath);
        if (node) target = node;
      }

      const box = new THREE.Box3().setFromObject(target);
      if (box.isEmpty()) return;

      selectionBoxHelper = new THREE.Box3Helper(box);
      selectionBoxHelper.name = "selection-box-helper";
      scene.add(selectionBoxHelper);
    }

    let decalPlanes = [];
    const textureLoader = new THREE.TextureLoader();
    const decalTextureCache = new Map();
    const checkerTex = makeCheckerTexture(128, 8);

    const decalProxyById = new Map();
    const decalBaseById = new Map();

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let pickables = [];

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
      const ov = materialOverridesRef.current;
      if (!ov) return;
      try {
        if (typeof applyMaterialOverridesToScene === "function") {
          applyMaterialOverridesToScene({
            root,
            objectGroups,
            meshToObjectKey,
            allMeshes,
            overrides: ov,
          });
        }
      } catch (e) {
        console.warn("[ThreeSceneViewer] material override apply failed:", String(e?.message || e));
      }
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

        pickables.push(plane);

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

      const objectKey = String(sid).split("::")[0];
      const group = objectGroups.get(objectKey);

      if (!group || group.visible === false) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      transformControls.attach(group);
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
      const activeId = activeDecalIdRef.current;
      const obj = transformControls.object;
      if (!activeId || !obj) return;

      const proxy = decalProxyById.get(String(activeId));
      if (!proxy) return;
      if (obj !== proxy) return;

      if (!gizmoDragging) return;

      setDecalPreviewPatch(activeId, {
        position: vec3Patch(proxy.position, 4),
        rotation_euler: eulerDegPatch(proxy.rotation, 2),
        scale: vec3Patch(proxy.scale, 4),
      });
    }
    transformControls.addEventListener("objectChange", onGizmoObjectChange);

    function resize() {
      const r = container.getBoundingClientRect();
      const w = Math.max(1, Math.floor(r.width));
      const h = Math.max(1, Math.floor(r.height));
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
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

      root.add(ghost);
    }

    async function loadAll() {
      if (disposed) return;

      setErr(null);
      pickables = [];
      meshToObjectId.clear();
      meshToObjectKey.clear();
      objectGroups.clear();
      allMeshes.clear();

      clearMaterialSlots();

      setLoadingCount(0);

      clearGhost();
      clearSelectionBox();
      clearDecals();

      transformControls.detach();
      transformControls.visible = false;

      while (root.children.length) root.remove(root.children[0]);
      root.add(decalsRoot);

      if (!objects.length) return;

      const loader = new GLTFLoader();
      const sortedObjects = sortObjectsStable(objects);

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

        const group = new THREE.Group();
        group.name = `obj:${objectKey}`;
        group.userData.kind = kind;
        group.userData.pickId = `obj:${objectKey}`;
        group.userData.objectId = objectKey;
        group.visible = !!cfg.visible && obj?.enabled !== false;

        applyTransformToObject3D(group, obj?.transform);

        objectGroups.set(objectKey, group);
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
        if (obj?.enabled === false) continue;

        const kind = String(obj?.kind || "unknown");
        const cfg = layers.kinds[kind] || ensureKind(kind);

        const objectKey = objId;
        const group = objectGroups.get(objectKey);
        if (!group) continue;

        const assetRef = obj?.asset_ref
          ? String(obj.asset_ref).trim()
          : obj?.url
            ? String(obj.url).trim()
            : "";

        if (!assetRef) {
          const placeholder = makePlaceholderMesh(objectKey);
          placeholder.userData.objectId = objectKey;
          group.add(placeholder);

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
            pickables.push(placeholder);
            meshToObjectId.set(placeholder, objId);
            meshToObjectKey.set(placeholder, objectKey);
          }
          continue;
        }

        setLoadingCount((c) => c + 1);
        try {
          const url = /^https?:\/\//i.test(assetRef) ? assetRef : await resolveAssetRef(assetRef);
          if (!url) throw new Error("asset_ref could not be resolved");

          console.log("[ThreeSceneViewer] Loading GLB:", {
            objId,
            assetRef,
            url,
          });

          const gltf = await loader.loadAsync(url);
          if (disposed) return;

          const gltfRoot = gltf.scene;
          group.add(gltfRoot);

          const meshPaths = [];

          gltfRoot.traverse((node) => {
            if (!node || !node.isMesh) return;

            node.userData.objectId = objectKey;
            applyOpacityToMaterial(node.material, cfg.opacity);

            allMeshes.add(node);

            try {
              const mp = buildMeshPath(node);
              if (mp) {
                meshPaths.push(mp);
                node.userData.pickId = `mesh:${objectKey}::${mp}`;
                node.userData.meshPath = mp;

                publishMaterialSlotsForMesh(objectKey, mp, node.material);
              }
            } catch {}

            if (cfg.pickable) {
              pickables.push(node);
              meshToObjectId.set(node, objId);
              meshToObjectKey.set(node, objectKey);
            }
          });

          setMeshPathsForObject(objectKey, meshPaths);
        } catch (e) {
          console.error("[ThreeSceneViewer] GLB load failed:", {
            objId,
            assetRef,
            error: String(e?.message || e),
          });

          const placeholder = makePlaceholderMesh(`${objectKey} (failed)`);
          placeholder.userData.objectId = objectKey;
          group.add(placeholder);

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
            pickables.push(placeholder);
            meshToObjectId.set(placeholder, objId);
            meshToObjectKey.set(placeholder, objectKey);
          }

          setErr((prev) => prev || String(e?.message || e));
        } finally {
          if (!disposed) setLoadingCount((c) => Math.max(0, c - 1));
        }
      }

      applyMaterialOverridesNow();
      frameScene();
      applyPreviewGhost();
      updateSelectionBox();

      await syncDecals();

      syncTransformControlsToTarget();
      applySnapToTransformControls();
    }

    loadAll();

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
    }

    function toggleObjectSelection(objectId) {
      const oid = String(objectId || "").trim();
      if (!oid) return;
      toggleMultiSelection(oid, true);
      syncPrimaryToSingleSelection(oid);
    }

    function onClick(e) {
      if (contextLost) return;

      const r = canvas.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 2 - 1;
      const y = -(((e.clientY - r.top) / r.height) * 2 - 1);
      mouse.set(x, y);

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(pickables, true);

      if (!intersects.length) {
        clearAllSelectionState?.();
        clearActiveDecalId?.();
        return;
      }

      const hitIds = buildPickIdListFromIntersects(intersects);
      const chosen = resolvePick(hitIds, selectionFilterRef.current || "all");

      if (!chosen) {
        clearAllSelectionState?.();
        clearActiveDecalId?.();
        return;
      }

      if (chosen.kind === "decal") {
        setActiveDecalId?.(chosen.key);
        clearAllSelectionState?.();
        return;
      }

      clearActiveDecalId?.();

      const additive = !!(e.shiftKey || e.ctrlKey || e.metaKey);

      if (chosen.kind === "mesh") {
        const objectId = String(chosen.key || "").split("::")[0];
        if (additive) {
          toggleObjectSelection(objectId);
        } else {
          setPrimaryObjectSelection(objectId);
        }
        return;
      }

      if (chosen.kind === "obj") {
        const objectId = String(chosen.key || "").split("::")[0];
        if (additive) {
          toggleObjectSelection(objectId);
        } else {
          setPrimaryObjectSelection(objectId);
        }
        return;
      }

      clearAllSelectionState?.();
    }

    function onDoubleClick(e) {
      if (contextLost) return;

      const r = canvas.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 2 - 1;
      const y = -(((e.clientY - r.top) / r.height) * 2 - 1);
      mouse.set(x, y);

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(pickables, true);
      if (!intersects.length) return;

      const hitIds = buildPickIdListFromIntersects(intersects);
      const chosen = resolvePick(hitIds, selectionFilterRef.current || "all");
      if (!chosen) return;

      if (chosen.kind === "decal") {
        setActiveDecalId?.(chosen.key);
        clearAllSelectionState?.();

        const base = decalBaseById.get(String(chosen.key));
        const ownerKey = base?.targetId ? String(base.targetId).split("::")[0] : null;
        const group = ownerKey ? objectGroups.get(ownerKey) : null;
        if (group) fitCameraToObject(camera, group, controls);
        else frameScene();

        return;
      }

      clearActiveDecalId?.();

      if (chosen.kind === "mesh") {
        const objectId = String(chosen.key || "").split("::")[0];
        setPrimaryObjectSelection(objectId);
        frameSelected();
        return;
      }

      if (chosen.kind === "obj") {
        const objectId = String(chosen.key || "").split("::")[0];
        setPrimaryObjectSelection(objectId);
        const group = objectGroups.get(objectId);
        if (group) fitCameraToObject(camera, group, controls);
        else frameScene();
        return;
      }
    }

    function onKeyDown(e) {
      const key = String(e.key || "").toLowerCase();

      if (key === "f" && !e.shiftKey) {
        e.preventDefault();
        frameSelected();
      } else if (key === "f" && e.shiftKey) {
        e.preventDefault();
        frameScene();
      }
    }

    canvas.addEventListener("click", onClick);
    canvas.addEventListener("dblclick", onDoubleClick);
    window.addEventListener("keydown", onKeyDown);

    let raf = 0;
    function tick() {
      raf = requestAnimationFrame(tick);
      if (contextLost) return;
      controls.update();
      renderer.render(scene, camera);
    }
    tick();

    viewerApiRef.current.syncSelection = () => {
      updateSelectionBox();
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
      applyMaterialOverridesNow();
    };
    viewerApiRef.current.syncSnap = () => {
      applySnapToTransformControls();
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

    onViewerApiReadyRef.current?.({
      frameSelected: viewerApiRef.current.frameSelected,
      frameScene: viewerApiRef.current.frameScene,
      applyPreset: viewerApiRef.current.applyPreset,
    });

    viewerApiRef.current.syncSelection?.();
    viewerApiRef.current.syncPreview?.();
    viewerApiRef.current.syncDecals?.();
    viewerApiRef.current.syncMaterials?.();
    viewerApiRef.current.syncSnap?.();

    return () => {
      disposed = true;
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

      renderer.dispose();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(objects), disabled, JSON.stringify(layers.kinds)]);

  useEffect(() => {
    viewerApiRef.current?.syncSelection?.();
  }, [selectedId]);

  useEffect(() => {
    viewerApiRef.current?.syncMode?.();
  }, [gizmoMode]);

  useEffect(() => {
    viewerApiRef.current?.syncSnap?.();
  }, [snapState]);

  useEffect(() => {
    viewerApiRef.current?.syncPreview?.();
  }, [preview]);

  useEffect(() => {
    viewerApiRef.current?.syncEditGate?.();
  }, [canEdit]);

  useEffect(() => {
    viewerApiRef.current?.syncDecals?.();
  }, [decals]);

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
    onViewerApiReadyRef.current?.({
      frameSelected: viewerApiRef.current?.frameSelected || null,
      frameScene: viewerApiRef.current?.frameScene || null,
      applyPreset: viewerApiRef.current?.applyPreset || null,
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

      <div ref={containerRef} className="border rounded overflow-hidden" style={{ height: 460 }}>
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
