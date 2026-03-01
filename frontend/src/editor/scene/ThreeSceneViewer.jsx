// frontend/src/editor/scene/ThreeSceneViewer.jsx
import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

// ✅ Step 1 — TransformControls (Three.js handles)
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";

import { resolveAssetRef } from "./resolveAssetRef";
import { buildPickedTargetId } from "./pickingId";
import { applyTransformToObject3D, makePlaceholderMesh } from "./applyTransform";
import {
  clearSelection,
  setSelectedId,
  useSelection,
} from "../selection/selectionStore";

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

// ✅ Tier 7.38 — active decal + preview patch store
import { useActiveDecal } from "../decals/activeDecalStore";
import {
  useDecalPreview,
  setDecalPreviewPatch,
  clearDecalPreviewPatch,
} from "../decals/decalPreviewStore";

function makeRenderer(canvas) {
  // Prefer WebGL2, fallback WebGL1. If neither exists, return null.
  const gl2 = canvas.getContext("webgl2", { antialias: true });
  const gl1 = gl2 ? null : canvas.getContext("webgl", { antialias: true });
  const gl = gl2 || gl1;
  if (!gl) return null;

  const r = new THREE.WebGLRenderer({
    canvas,
    context: gl,
    antialias: true,
  });

  r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  return r;
}

function makeCamera(width, height) {
  const cam = new THREE.PerspectiveCamera(45, width / height, 0.1, 5000);
  cam.position.set(3.0, 2.0, 3.0);
  cam.lookAt(0, 0.8, 0);
  return cam;
}

function fitCameraToScene(camera, root) {
  const box = new THREE.Box3().setFromObject(root);
  if (box.isEmpty()) return;

  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);

  const maxDim = Math.max(size.x, size.y, size.z) || 1;
  const fov = (camera.fov * Math.PI) / 180;
  const distance = (maxDim / (2 * Math.tan(fov / 2))) * 1.6;

  camera.position.set(
    center.x + distance,
    center.y + distance * 0.5,
    center.z + distance
  );
  camera.lookAt(center);
  camera.updateProjectionMatrix();
}

// ✅ 6G.7
function fitCameraToObject(camera, object3d) {
  const box = new THREE.Box3().setFromObject(object3d);
  if (box.isEmpty()) return;

  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);

  const maxDim = Math.max(size.x, size.y, size.z) || 1;
  const fov = (camera.fov * Math.PI) / 180;
  const distance = (maxDim / (2 * Math.tan(fov / 2))) * 1.6;

  camera.position.set(
    center.x + distance,
    center.y + distance * 0.5,
    center.z + distance
  );
  camera.lookAt(center);
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

// ✅ Tier 7.37 helper (builtin checker texture)
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

/**
 * ✅ ADDITIVE SAFE:
 * - canEdit gates ONLY TransformControls (gizmo).
 * - Picking/selection still works in READ.
 *
 * ✅ Tier 7.38:
 * - optional onCommitTool for DECAL_UPDATE on drag end
 */
export default function ThreeSceneViewer({
  sceneIndex,
  disabled = false,
  canEdit = true, // ✅ NEW (default true so older callers behave the same)
  onCommitTool = null, // ✅ Tier 7.38 (optional)
}) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  const { selectedId } = useSelection();

  // ✅ 6G.6 layers state
  const layers = useSceneLayers();

  // ✅ 7.27 preview state
  const { preview } = useGizmoPreview();

  // ✅ shared gizmo mode (translate/rotate/scale)
  const { mode: gizmoMode } = useGizmoMode();

  // ✅ Tier 7.38 active decal + preview patches
  const { decalId: activeDecalId } = useActiveDecal();
  const decalPreview = useDecalPreview();

  const [err, setErr] = useState(null);
  const [loadingCount, setLoadingCount] = useState(0);

  const objects = useMemo(
    () => (sceneIndex?.objects || []).filter(Boolean),
    [sceneIndex]
  );

  // ✅ Tier 7.37: read decals (support a few possible shapes safely)
  const decals = useMemo(() => {
    const d1 = sceneIndex?.decor_state?.decals;
    const d2 = sceneIndex?.snapshot?.decor_state?.decals;
    const d3 = sceneIndex?.activeSnapshot?.decor_state?.decals;
    const list = d1 || d2 || d3 || [];
    return Array.isArray(list) ? list.filter(Boolean) : [];
  }, [sceneIndex]);

  // -------------------------------
  // ✅ Prevent WebGL churn:
  // keep rapidly-changing values in refs,
  // so the main WebGL effect does NOT remount.
  // -------------------------------
  const selectedIdRef = useRef(selectedId);
  const previewRef = useRef(preview);
  const gizmoModeRef = useRef(gizmoMode);

  // ✅ NEW: canEdit ref (no remount)
  const canEditRef = useRef(!!canEdit);

  // ✅ Tier 7.37 decals ref (no remount)
  const decalsRef = useRef(decals);

  // ✅ Tier 7.38 active decal + preview refs (no remount)
  const activeDecalIdRef = useRef(activeDecalId);
  const decalPreviewRef = useRef(decalPreview);
  const onCommitToolRef = useRef(onCommitTool);

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

  // Expose minimal internal sync hooks for secondary effects (no remount).
  const viewerApiRef = useRef({
    syncSelection: null,
    syncPreview: null,
    syncMode: null,
    syncEditGate: null, // ✅ NEW
    syncDecals: null, // ✅ Tier 7.37
    syncDecalPreview: null, // ✅ Tier 7.38 (preview patch application)
    syncDecalTarget: null, // ✅ Tier 7.38 (active decal -> gizmo attach)
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    // ✅ 6G.10: wipe mesh index whenever viewer remounts/rebinds
    clearMeshIndex();

    let disposed = false;

    const scene = new THREE.Scene();

    const renderer = makeRenderer(canvas);
    if (!renderer) {
      setErr("WebGL is not available (context creation failed).");
      return () => {};
    }

    // WebGL context loss safety
    let contextLost = false;

    function onContextLost(e) {
      e.preventDefault();
      contextLost = true;
      setErr("WebGL context was lost. Refresh the page if it doesn’t recover.");
    }

    function onContextRestored() {
      contextLost = false;
      // keep message light; reloading is often safest
      setErr("WebGL context restored. If blank, refresh the page.");
    }

    canvas.addEventListener("webglcontextlost", onContextLost, false);
    canvas.addEventListener("webglcontextrestored", onContextRestored, false);

    // lighting + ground
    scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 1.0));
    const dir = new THREE.DirectionalLight(0xffffff, 1.0);
    dir.position.set(4, 6, 3);
    scene.add(dir);
    scene.add(new THREE.GridHelper(20, 20));

    // root group for all objects
    const root = new THREE.Group();
    root.name = "scene-root";
    scene.add(root);

    // ✅ Tier 7.37: decals root (always deterministic)
    const decalsRoot = new THREE.Group();
    decalsRoot.name = "decals-root";
    root.add(decalsRoot);

    // camera
    const rect = container.getBoundingClientRect();
    const camera = makeCamera(rect.width || 800, rect.height || 500);

    // ✅ TransformControls (Step 1)
    const transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.setMode(gizmoModeRef.current); // translate | rotate | scale

    // ✅ NEW: effective gizmo enabled gate
    const gizmoEnabled = !disabled && !!canEditRef.current;
    transformControls.enabled = gizmoEnabled;

    transformControls.visible = false; // becomes true once attached
    scene.add(transformControls);

    // ✅ selection bounding box helper
    let selectionBoxHelper = null;

    function clearSelectionBox() {
      if (!selectionBoxHelper) return;
      scene.remove(selectionBoxHelper);
      selectionBoxHelper.geometry?.dispose?.();
      selectionBoxHelper.material?.dispose?.();
      selectionBoxHelper = null;
    }

    function updateSelectionBox() {
      clearSelectionBox();

      const sid = selectedIdRef.current;
      if (!sid) return;

      // ✅ 6G.12 canonical parse shape
      const { objectKey, meshPath } = parseSelectedId(sid);
      if (!objectKey) return;

      const group = objectGroups.get(String(objectKey));
      if (!group) return;

      // If hidden by layers, don't draw the box.
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

    // orbit drag
    let isDragging = false,
      lastX = 0,
      lastY = 0;

    // while gizmo is dragging: disable orbit drag
    function onGizmoDraggingChanged(e) {
      const dragging = !!e?.value;
      if (dragging) isDragging = false;

      // ✅ Tier 7.38: commit DECAL_UPDATE once on release (if the gizmo is attached to an active decal proxy)
      if (!dragging) {
        const activeId = activeDecalIdRef.current;
        const obj = transformControls.object;
        if (!activeId || !obj) return;

        const proxy = decalProxyById.get(String(activeId));
        if (!proxy) return;

        // only commit if we are actually attached to the decal proxy
        if (obj !== proxy) return;

        // clear preview patch and emit commit
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
    transformControls.addEventListener(
      "dragging-changed",
      onGizmoDraggingChanged
    );

    // ✅ Tier 7.38: while dragging, emit decal preview patch (UI-only)
    function onGizmoObjectChange() {
      const activeId = activeDecalIdRef.current;
      const obj = transformControls.object;
      if (!activeId || !obj) return;

      const proxy = decalProxyById.get(String(activeId));
      if (!proxy) return;
      if (obj !== proxy) return;

      // only if actually dragging
      if (!transformControls.dragging) return;

      setDecalPreviewPatch(activeId, {
        position: vec3Patch(proxy.position, 4),
        rotation_euler: eulerDegPatch(proxy.rotation, 2),
        scale: vec3Patch(proxy.scale, 4),
      });
    }
    transformControls.addEventListener("objectChange", onGizmoObjectChange);

    function onPointerDown(e) {
      // ignore orbit start if clicking on gizmo handles
      if (transformControls.dragging) return;
      isDragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
    }
    function onPointerUp() {
      isDragging = false;
    }
    function onPointerMove(e) {
      if (!isDragging) return;
      const dx = (e.clientX - lastX) * 0.005;
      const dy = (e.clientY - lastY) * 0.005;
      lastX = e.clientX;
      lastY = e.clientY;

      const offset = camera.position.clone();
      const spherical = new THREE.Spherical().setFromVector3(offset);
      spherical.theta -= dx;
      spherical.phi = Math.min(
        Math.max(0.2, spherical.phi - dy),
        Math.PI - 0.2
      );
      offset.setFromSpherical(spherical);
      camera.position.copy(offset);
      camera.lookAt(0, 0.8, 0);
    }

    container.addEventListener("pointerdown", onPointerDown);
    container.addEventListener("pointerup", onPointerUp);
    container.addEventListener("pointerleave", onPointerUp);
    container.addEventListener("pointermove", onPointerMove);

    // resize
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

    // ✅ 7.27 ghost holder
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

    // ✅ Tier 7.37: decals holder + textures cache (lifetime = viewer mount)
    let decalPlanes = []; // { mesh, material, geometry, texture? }
    const textureLoader = new THREE.TextureLoader();
    const decalTextureCache = new Map(); // asset_ref -> THREE.Texture
    const checkerTex = makeCheckerTexture(128, 8);

    // ✅ Tier 7.38: decal proxy maps (so gizmo can attach deterministically)
    const decalProxyById = new Map(); // decal_id -> THREE.Object3D proxy
    const decalBaseById = new Map(); // decal_id -> normalized decal (for restoring when preview cleared)

    function clearDecals() {
      // Remove planes and dispose safely
      for (const item of decalPlanes) {
        try {
          if (item?.mesh?.parent) item.mesh.parent.remove(item.mesh);
          item.geometry?.dispose?.();
          item.material?.dispose?.();
          // Textures in cache are disposed at unmount (below), not per-plane
        } catch {}
      }
      decalPlanes = [];

      decalProxyById.clear();
      decalBaseById.clear();

      // Clear decalsRoot children (defensive)
      while (decalsRoot.children.length)
        decalsRoot.remove(decalsRoot.children[0]);
    }

    function normalizeDecal(d) {
      const id = String(d?.id || "");
      const enabled = d?.enabled !== false;
      const targetId = String(d?.target_id || "");
      const assetRef = String(d?.asset_ref || "");

      const pos = d?.position || {};
      const rot = d?.rotation_euler || {};
      const scl = d?.scale || {};

      const opacity = clamp01(d?.opacity ?? 1.0);
      const zOff = Number.isFinite(Number(d?.z_offset))
        ? Number(d.z_offset)
        : 0.001;

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

      // builtin checker
      if (assetRef === "builtin://checker") {
        if (checkerTex) decalTextureCache.set(assetRef, checkerTex);
        return checkerTex;
      }

      // If assetRef looks like a URL, use it directly. Otherwise try resolveAssetRef.
      let url = assetRef;
      if (!/^https?:\/\//i.test(assetRef)) {
        try {
          const resolved = await resolveAssetRef(assetRef);
          if (resolved) url = resolved;
        } catch {
          // keep url as assetRef
        }
      }

      // Load texture (async)
      try {
        const tex = await textureLoader.loadAsync(url);
        tex.wrapS = THREE.ClampToEdgeWrapping;
        tex.wrapT = THREE.ClampToEdgeWrapping;
        tex.needsUpdate = true;
        decalTextureCache.set(assetRef, tex);
        return tex;
      } catch (e) {
        console.warn("[ThreeSceneViewer] decal texture load failed:", {
          assetRef,
          url,
          error: String(e?.message || e),
        });
        // fall back to checker if available
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

      if (pos) proxy.position.set(pos.x, pos.y, pos.z);
      if (rot)
        proxy.rotation.set(degToRad(rot.x), degToRad(rot.y), degToRad(rot.z));
      if (scl) proxy.scale.set(scl.x, scl.y, scl.z);
    }

    function applyAllDecalPreviewPatches() {
      for (const id of decalProxyById.keys()) {
        applyDecalTransformFromBaseOrPreview(id);
      }
    }

    // ✅ Tier 7.37: render decals deterministically (stable order by id)
    async function syncDecals() {
      clearDecals();

      const raw = decalsRef.current || [];
      if (!raw.length) return;

      // deterministic ordering
      const sorted = raw
        .map(normalizeDecal)
        .filter((d) => d.id && d.enabled && d.targetId)
        .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

      for (const d of sorted) {
        if (disposed) return;

        const objectKey = String(d.targetId).split("::")[0];
        const group = objectGroups.get(objectKey);
        if (!group) continue;
        if (group.visible === false) continue;

        const tex = await getDecalTexture(d.assetRef);
        if (disposed) return;

        // ✅ Tier 7.38: proxy object that the gizmo attaches to
        const proxy = new THREE.Object3D();
        proxy.name = `decal-proxy:${d.id}`;

        // base transform (preview may override later)
        proxy.position.set(d.position.x, d.position.y, d.position.z);
        proxy.rotation.set(
          degToRad(d.rotation_euler.x),
          degToRad(d.rotation_euler.y),
          degToRad(d.rotation_euler.z)
        );
        proxy.scale.set(d.scale.x, d.scale.y, d.scale.z);

        // ✅ visual plane under proxy
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

        proxy.add(plane);
        group.add(proxy);

        decalPlanes.push({ mesh: plane, geometry: geom, material: mat });

        decalProxyById.set(d.id, proxy);
        decalBaseById.set(d.id, d);
      }

      // apply preview patches (if any) after build
      applyAllDecalPreviewPatches();
    }

    // picking sets
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let pickables = [];

    // ✅ 6G.12: primary mapping is Mesh -> objectKey (object or object@instance)
    const meshToObjectKey = new Map(); // Mesh -> objectKey
    // ✅ Legacy fallback (optional, safe)
    const meshToObjectId = new Map(); // Mesh -> objectId

    // ✅ 6G.7 object groups for framing + gizmo attach
    const objectGroups = new Map(); // objectKey -> THREE.Group

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

    function frameSelectedOrScene() {
      const sid = selectedIdRef.current;
      if (!sid) {
        fitCameraToScene(camera, root);
        return;
      }

      const objectKey = String(sid).split("::")[0];
      const group = objectGroups.get(objectKey);

      if (group) fitCameraToObject(camera, group);
      else fitCameraToScene(camera, root);
    }

    // ✅ Attach gizmo:
    // Priority: active decal proxy (7.38) -> selected object group (7.34)
    function syncTransformControlsToTarget() {
      const mode = gizmoModeRef.current;
      transformControls.setMode(mode);

      const gizmoEnabledNow = !disabled && !!canEditRef.current;
      transformControls.enabled = gizmoEnabledNow;

      if (!gizmoEnabledNow) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      // 1) active decal
      const activeId = activeDecalIdRef.current;
      if (activeId) {
        const proxy = decalProxyById.get(String(activeId));
        if (proxy) {
          transformControls.attach(proxy);
          transformControls.visible = true;
          return;
        }
      }

      // 2) selected object
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

    // ✅ 7.27 apply ghost from preview
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
          const mats = Array.isArray(node.material)
            ? node.material
            : [node.material];
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
      setErr(null);
      pickables = [];
      meshToObjectId.clear();
      meshToObjectKey.clear();
      objectGroups.clear();
      setLoadingCount(0);

      // clear root
      clearGhost();
      clearSelectionBox();
      clearDecals();

      transformControls.detach();
      transformControls.visible = false;

      while (root.children.length) root.remove(root.children[0]);

      // ✅ re-add decals root after clearing root
      root.add(decalsRoot);

      if (!objects.length) return;

      const loader = new GLTFLoader();

      for (const obj of objects) {
        if (disposed) return;

        const objId = String(obj.id || "").trim();
        if (!objId) continue;

        const kind = String(obj.kind || "unknown");
        const cfg = layers.kinds[kind] || ensureKind(kind);

        // ✅ 6G.12-ready: objectKey is what lives left of "::"
        // For now non-instance == objectId. Instances will become "objId@instId".
        const objectKey = objId;

        const group = new THREE.Group();
        group.name = `obj:${objectKey}`;
        group.userData.kind = kind;

        group.visible = !!cfg.visible;

        root.add(group);
        objectGroups.set(objectKey, group);

        applyTransformToObject3D(group, obj.transform);

        const assetRef = obj.asset_ref ? String(obj.asset_ref).trim() : "";

        if (!assetRef) {
          const placeholder = makePlaceholderMesh(objectKey);
          group.add(placeholder);

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

          try {
            const mp = buildMeshPath(placeholder);
            if (mp) setMeshPathsForObject(objectKey, [mp]);
          } catch {}

          if (cfg.pickable) {
            pickables.push(placeholder);
            meshToObjectId.set(placeholder, objId); // legacy
            meshToObjectKey.set(placeholder, objectKey); // new
          }
          continue;
        }

        setLoadingCount((c) => c + 1);
        try {
          const url = await resolveAssetRef(assetRef);
          if (!url) throw new Error("asset_ref could not be resolved");

          console.log("[ThreeSceneViewer] Loading GLB:", { objId, assetRef, url });

          const gltf = await loader.loadAsync(url);
          if (disposed) return;

          const gltfRoot = gltf.scene;
          group.add(gltfRoot);

          const meshPaths = [];

          gltfRoot.traverse((node) => {
            if (!node || !node.isMesh) return;

            applyOpacityToMaterial(node.material, cfg.opacity);

            try {
              const mp = buildMeshPath(node);
              if (mp) meshPaths.push(mp);
            } catch {}

            if (cfg.pickable) {
              pickables.push(node);
              meshToObjectId.set(node, objId); // legacy
              meshToObjectKey.set(node, objectKey); // new
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
          group.add(placeholder);

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

          try {
            const mp = buildMeshPath(placeholder);
            if (mp) setMeshPathsForObject(objectKey, [mp]);
          } catch {}

          if (cfg.pickable) {
            pickables.push(placeholder);
            meshToObjectId.set(placeholder, objId); // legacy
            meshToObjectKey.set(placeholder, objectKey); // new
          }

          setErr((prev) => prev || String(e?.message || e));
        } finally {
          setLoadingCount((c) => Math.max(0, c - 1));
        }
      }

      fitCameraToScene(camera, root);

      applyPreviewGhost();
      updateSelectionBox();

      // ✅ Tier 7.37/7.38: render decals after objects exist
      await syncDecals();

      // ✅ ensure gizmo attaches to correct target after decals created
      syncTransformControlsToTarget();
    }

    loadAll();

    function onClick(e) {
      // IMPORTANT: keep selection available even in READ mode.
      // Only the gizmo is gated by canEdit/disabled.
      const r = canvas.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 2 - 1;
      const y = -(((e.clientY - r.top) / r.height) * 2 - 1);
      mouse.set(x, y);

      raycaster.setFromCamera(mouse, camera);
      const hits = raycaster.intersectObjects(pickables, true);

      if (!hits.length) {
        clearSelection();
        return;
      }

      const hitMesh = hits[0].object;
      const objectKey = resolveObjectKeyFromHitMesh(hitMesh);

      if (!objectKey) {
        clearSelection();
        return;
      }

      const idNode = pickIdNodeForMeshPath(hitMesh);

      // ✅ IMPORTANT: pickingId currently expects { objectId, mesh }.
      // objectKey is the correct left side of "::" for 6G.12,
      // so pass it through as objectId (backward compatible).
      const id = buildPickedTargetId({ objectId: objectKey, mesh: idNode });
      if (!id) {
        clearSelection();
        return;
      }

      setSelectedId(id);
    }

    function onDoubleClick(e) {
      // Keep focus feature available in READ too.
      const r = canvas.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 2 - 1;
      const y = -(((e.clientY - r.top) / r.height) * 2 - 1);
      mouse.set(x, y);

      raycaster.setFromCamera(mouse, camera);
      const hits = raycaster.intersectObjects(pickables, true);
      if (!hits.length) return;

      const hitMesh = hits[0].object;
      const objectKey = resolveObjectKeyFromHitMesh(hitMesh);
      if (!objectKey) return;

      const idNode = pickIdNodeForMeshPath(hitMesh);
      const id = buildPickedTargetId({ objectId: objectKey, mesh: idNode });
      if (!id) return;

      setSelectedId(id);

      const group = objectGroups.get(objectKey);
      if (group) fitCameraToObject(camera, group);
      else fitCameraToScene(camera, root);
    }

    function onKeyDown(e) {
      if (String(e.key || "").toLowerCase() === "f") {
        frameSelectedOrScene();
      }
    }

    canvas.addEventListener("click", onClick);
    canvas.addEventListener("dblclick", onDoubleClick);
    window.addEventListener("keydown", onKeyDown);

    // render loop
    let raf = 0;
    function tick() {
      raf = requestAnimationFrame(tick);
      if (contextLost) return;
      renderer.render(scene, camera);
    }
    tick();

    viewerApiRef.current.syncSelection = () => {
      updateSelectionBox();
      // attach gizmo could depend on selection when no decal active
      syncTransformControlsToTarget();
    };
    viewerApiRef.current.syncPreview = () => {
      applyPreviewGhost();
    };
    viewerApiRef.current.syncMode = () => {
      syncTransformControlsToTarget();
    };
    // ✅ NEW: sync canEdit gate without remount
    viewerApiRef.current.syncEditGate = () => {
      syncTransformControlsToTarget();
    };
    // ✅ Tier 7.37: sync decals without remount
    viewerApiRef.current.syncDecals = () => {
      syncDecals().then(() => {
        // ensure attach after rebuild
        syncTransformControlsToTarget();
      });
    };
    // ✅ Tier 7.38: apply preview patches without rebuilding decals
    viewerApiRef.current.syncDecalPreview = () => {
      applyAllDecalPreviewPatches();
    };
    // ✅ Tier 7.38: active decal changes (reattach)
    viewerApiRef.current.syncDecalTarget = () => {
      syncTransformControlsToTarget();
    };

    viewerApiRef.current.syncSelection?.();
    viewerApiRef.current.syncPreview?.();
    viewerApiRef.current.syncDecals?.();

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

      clearGhost();
      clearSelectionBox();
      clearDecals();

      // dispose cached textures
      for (const [k, tex] of decalTextureCache.entries()) {
        if (k === "builtin://checker") continue; // checkerTex disposed below (or kept)
        try {
          tex?.dispose?.();
        } catch {}
      }
      try {
        checkerTex?.dispose?.();
      } catch {}

      transformControls.removeEventListener(
        "dragging-changed",
        onGizmoDraggingChanged
      );
      transformControls.removeEventListener("objectChange", onGizmoObjectChange);
      transformControls.detach();
      scene.remove(transformControls);

      canvas.removeEventListener("click", onClick);
      canvas.removeEventListener("dblclick", onDoubleClick);
      window.removeEventListener("keydown", onKeyDown);

      container.removeEventListener("pointerdown", onPointerDown);
      container.removeEventListener("pointerup", onPointerUp);
      container.removeEventListener("pointerleave", onPointerUp);
      container.removeEventListener("pointermove", onPointerMove);

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

  // Secondary sync effects: do NOT remount WebGL
  useEffect(() => {
    viewerApiRef.current?.syncSelection?.();
  }, [selectedId]);

  useEffect(() => {
    viewerApiRef.current?.syncMode?.();
  }, [gizmoMode]);

  useEffect(() => {
    viewerApiRef.current?.syncPreview?.();
  }, [preview]);

  // ✅ NEW: when canEdit changes, just re-sync gizmo state
  useEffect(() => {
    viewerApiRef.current?.syncEditGate?.();
  }, [canEdit]);

  // ✅ Tier 7.37: when decals change, re-sync decals (no remount)
  useEffect(() => {
    viewerApiRef.current?.syncDecals?.();
  }, [decals]);

  // ✅ Tier 7.38: when active decal changes, reattach gizmo target
  useEffect(() => {
    viewerApiRef.current?.syncDecalTarget?.();
  }, [activeDecalId]);

  // ✅ Tier 7.38: when preview patches change, apply transforms (no rebuild)
  useEffect(() => {
    viewerApiRef.current?.syncDecalPreview?.();
  }, [decalPreview]);

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
          No objects in scene index yet. Attach an asset (6G.2) or ensure
          body_state.scene.objects[] exists.
        </div>
      ) : null}

      <div
        ref={containerRef}
        className="border rounded overflow-hidden"
        style={{ height: 460 }}
      >
        <canvas
          ref={canvasRef}
          style={{ width: "100%", height: "100%", display: "block" }}
        />
      </div>

      <div className="text-xs opacity-70">
        Click mesh/placeholder to select. Double-click to focus. Press <b>F</b> to
        frame selected (or whole scene). TransformControls mode is synced with the
        panel. Bounding box shows selection target (6G.9). If an active decal is
        selected (7.38), the gizmo targets the decal proxy first.
      </div>
    </div>
  );
}
