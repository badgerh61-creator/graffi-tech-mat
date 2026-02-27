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

// ✅ 7.27 preview ghost
import { useGizmoPreview } from "../gizmo/gizmoPreviewStore";

// ✅ Step 6 — shared gizmo mode store
import { useGizmoMode } from "../gizmo/gizmoModeStore";

function makeRenderer(canvas) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true });
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

export default function ThreeSceneViewer({ sceneIndex, disabled = false }) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  const { selectedId } = useSelection();

  // ✅ 6G.6 layers state
  const layers = useSceneLayers();

  // ✅ 7.27 preview state
  const { preview } = useGizmoPreview();

  // ✅ shared gizmo mode (translate/rotate/scale)
  const { mode: gizmoMode } = useGizmoMode();

  const [err, setErr] = useState(null);
  const [loadingCount, setLoadingCount] = useState(0);

  const objects = useMemo(
    () => (sceneIndex?.objects || []).filter(Boolean),
    [sceneIndex]
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    // ✅ 6G.10: wipe mesh index whenever viewer remounts/rebinds
    clearMeshIndex();

    let disposed = false;

    const scene = new THREE.Scene();
    const renderer = makeRenderer(canvas);

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

    // camera
    const rect = container.getBoundingClientRect();
    const camera = makeCamera(rect.width || 800, rect.height || 500);

    // ✅ TransformControls (Step 1)
    const transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.setMode(gizmoMode); // translate | rotate | scale
    transformControls.enabled = !disabled;
    transformControls.visible = false; // becomes true once attached
    scene.add(transformControls);

    // orbit drag
    let isDragging = false,
      lastX = 0,
      lastY = 0;

    // while gizmo is dragging: disable orbit drag
    function onGizmoDraggingChanged(e) {
      const dragging = !!e?.value;
      if (dragging) isDragging = false;
    }
    transformControls.addEventListener("dragging-changed", onGizmoDraggingChanged);

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
      spherical.phi = Math.min(Math.max(0.2, spherical.phi - dy), Math.PI - 0.2);
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

    // picking sets
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let pickables = [];
    const meshToObjectId = new Map(); // Mesh -> objectId

    // ✅ 6G.7 object groups for framing + gizmo attach
    const objectGroups = new Map(); // objectId -> THREE.Group

    function resolveObjectIdFromHitMesh(hitMesh) {
      if (!hitMesh) return null;

      let objectId = meshToObjectId.get(hitMesh);
      if (objectId) return objectId;

      let p = hitMesh.parent;
      while (p && !objectId) {
        if (typeof p.name === "string" && p.name.startsWith("obj:")) {
          objectId = p.name.slice(4);
          break;
        }
        p = p.parent;
      }
      return objectId || null;
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
      if (!selectedId) {
        fitCameraToScene(camera, root);
        return;
      }

      const objectId = String(selectedId).split("::")[0];
      const group = objectGroups.get(objectId);

      if (group) fitCameraToObject(camera, group);
      else fitCameraToScene(camera, root);
    }

    // ✅ Attach gizmo to selected object group (UI-only)
    function syncTransformControlsToSelection() {
      transformControls.setMode(gizmoMode);

      if (disabled || !selectedId) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      const objectId = String(selectedId).split("::")[0];
      const group = objectGroups.get(objectId);

      if (!group) {
        transformControls.detach();
        transformControls.visible = false;
        return;
      }

      // If layer hides the object, don't show gizmo
      if (group.visible === false) {
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
      if (!preview) return;

      const targetId = preview.payload?.target_id || preview.target_id;
      if (!targetId) return;

      const objectId = String(targetId).split("::")[0];
      const group = objectGroups.get(objectId);
      if (!group) return;

      ghost = group.clone(true);
      ghost.name = `ghost:${group.name || objectId}`;

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

      const tool = preview.tool;
      const p = preview.payload || {};

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
      objectGroups.clear();
      setLoadingCount(0);

      // clear root
      clearGhost();
      transformControls.detach();
      transformControls.visible = false;

      while (root.children.length) root.remove(root.children[0]);

      if (!objects.length) return;

      const loader = new GLTFLoader();

      for (const obj of objects) {
        if (disposed) return;

        const objId = String(obj.id || "").trim();
        if (!objId) continue;

        const kind = String(obj.kind || "unknown");
        const cfg = layers.kinds[kind] || ensureKind(kind);

        const group = new THREE.Group();
        group.name = `obj:${objId}`;
        group.userData.kind = kind;

        group.visible = !!cfg.visible;

        root.add(group);
        objectGroups.set(objId, group);

        applyTransformToObject3D(group, obj.transform);

        const assetRef = obj.asset_ref ? String(obj.asset_ref).trim() : "";

        if (!assetRef) {
          const placeholder = makePlaceholderMesh(objId);
          group.add(placeholder);

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

          // ✅ 6G.10: placeholder still has a deterministic "mesh path"
          // It will appear as something like "placeholder:<id>" due to makePlaceholderMesh name.
          try {
            const mp = buildMeshPath(placeholder);
            if (mp) setMeshPathsForObject(objId, [mp]);
          } catch {}

          if (cfg.pickable) {
            pickables.push(placeholder);
            meshToObjectId.set(placeholder, objId);
          }
          continue;
        }

        setLoadingCount((c) => c + 1);
        try {
          const url = await resolveAssetRef(assetRef);
          if (!url) throw new Error("asset_ref could not be resolved");

          const gltf = await loader.loadAsync(url);
          if (disposed) return;

          const gltfRoot = gltf.scene;
          group.add(gltfRoot);

          // ✅ 6G.10: collect deterministic mesh paths for the tree panel
          const meshPaths = [];

          gltfRoot.traverse((node) => {
            if (!node || !node.isMesh) return;

            applyOpacityToMaterial(node.material, cfg.opacity);

            // publish mesh paths (stable, human readable)
            try {
              const mp = buildMeshPath(node);
              if (mp) meshPaths.push(mp);
            } catch {}

            if (cfg.pickable) {
              pickables.push(node);
              meshToObjectId.set(node, objId);
            }
          });

          setMeshPathsForObject(objId, meshPaths);
        } catch (e) {
          const placeholder = makePlaceholderMesh(`${objId} (failed)`);
          group.add(placeholder);

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

          try {
            const mp = buildMeshPath(placeholder);
            if (mp) setMeshPathsForObject(objId, [mp]);
          } catch {}

          if (cfg.pickable) {
            pickables.push(placeholder);
            meshToObjectId.set(placeholder, objId);
          }

          setErr((prev) => prev || String(e?.message || e));
        } finally {
          setLoadingCount((c) => Math.max(0, c - 1));
        }
      }

      fitCameraToScene(camera, root);

      // apply ghost if active
      applyPreviewGhost();

      // attach gizmo if selection exists
      syncTransformControlsToSelection();
    }

    loadAll();

    function onClick(e) {
      if (disabled) return;

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
      const objectId = resolveObjectIdFromHitMesh(hitMesh);

      if (!objectId) {
        clearSelection();
        return;
      }

      const idNode = pickIdNodeForMeshPath(hitMesh);

      const id = buildPickedTargetId({ objectId, mesh: idNode });
      if (!id) {
        clearSelection();
        return;
      }

      setSelectedId(id);
    }

    function onDoubleClick(e) {
      if (disabled) return;

      const r = canvas.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * 2 - 1;
      const y = -(((e.clientY - r.top) / r.height) * 2 - 1);
      mouse.set(x, y);

      raycaster.setFromCamera(mouse, camera);
      const hits = raycaster.intersectObjects(pickables, true);
      if (!hits.length) return;

      const hitMesh = hits[0].object;
      const objectId = resolveObjectIdFromHitMesh(hitMesh);
      if (!objectId) return;

      const idNode = pickIdNodeForMeshPath(hitMesh);
      const id = buildPickedTargetId({ objectId, mesh: idNode });
      if (!id) return;

      setSelectedId(id);

      const group = objectGroups.get(objectId);
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
      renderer.render(scene, camera);
    }
    tick();

    // keep gizmo synced when selection/mode changes
    syncTransformControlsToSelection();

    return () => {
      disposed = true;
      cancelAnimationFrame(raf);

      clearGhost();

      transformControls.removeEventListener("dragging-changed", onGizmoDraggingChanged);
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

      renderer.dispose();

      // ✅ Tier 6G.8 safety: some GPUs/drivers keep ghost contexts; guard-call if available
      try {
        renderer.forceContextLoss?.();
      } catch {}
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    JSON.stringify(objects),
    disabled,
    JSON.stringify(layers.kinds),
    selectedId,
    JSON.stringify(preview || null),
    gizmoMode,
  ]);

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
          No objects in scene index yet. Attach an asset (6G.2) or ensure body_state.scene.objects[] exists.
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
        Click mesh/placeholder to select. Double-click to focus. Press <b>F</b> to frame selected (or whole scene).
        Drag pads show ghost preview (UI-only). TransformControls mode is synced with the panel.
      </div>
    </div>
  );
}
