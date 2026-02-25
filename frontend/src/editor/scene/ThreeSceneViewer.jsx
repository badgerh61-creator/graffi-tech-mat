// frontend/src/editor/scene/ThreeSceneViewer.jsx
import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

import { resolveAssetRef } from "./resolveAssetRef";
import { buildPickedTargetId } from "./pickingId";
import { applyTransformToObject3D, makePlaceholderMesh } from "./applyTransform";
import { clearSelection, setSelectedId, useSelection } from "../selection/selectionStore";

// ✅ 6G.6 layers
import { useSceneLayers, ensureKind } from "./layersStore";

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

  camera.position.set(center.x + distance, center.y + distance * 0.5, center.z + distance);
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

  camera.position.set(center.x + distance, center.y + distance * 0.5, center.z + distance);
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

  const [err, setErr] = useState(null);
  const [loadingCount, setLoadingCount] = useState(0);

  const objects = useMemo(() => (sceneIndex?.objects || []).filter(Boolean), [sceneIndex]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

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

    // orbit drag
    let isDragging = false,
      lastX = 0,
      lastY = 0;

    function onPointerDown(e) {
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

    // picking sets
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let pickables = [];
    const meshToObjectId = new Map(); // Mesh -> objectId

    // ✅ 6G.7 object groups for framing
    const objectGroups = new Map(); // objectId -> THREE.Group

    // ✅ helper: find objectId for a hit mesh
    function resolveObjectIdFromHitMesh(hitMesh) {
      if (!hitMesh) return null;

      let objectId = meshToObjectId.get(hitMesh);
      if (objectId) return objectId;

      // fallback: walk parents to find group name "obj:<id>"
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

    // ✅ 6G.5-friendly improvement: prefer named ancestor ONLY for ID-building
    function pickIdNodeForMeshPath(hitMesh) {
      if (!hitMesh) return null;

      // If the mesh already has a name, use it
      if (hitMesh.name && String(hitMesh.name).trim()) return hitMesh;

      // Otherwise climb until boundary; return first named node
      let p = hitMesh.parent;
      while (p) {
        if (typeof p.name === "string" && p.name.startsWith("obj:")) break;
        if (p.name && String(p.name).trim()) return p;
        p = p.parent;
      }
      return hitMesh;
    }

    // ✅ 6G.7: frame selected object or whole scene (no selection mutation)
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

    async function loadAll() {
      setErr(null);
      pickables = [];
      meshToObjectId.clear();
      objectGroups.clear();
      setLoadingCount(0);

      // clear root
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

        // ✅ layer visibility
        group.visible = !!cfg.visible;

        root.add(group);
        objectGroups.set(objId, group);

        // apply transform to group
        applyTransformToObject3D(group, obj.transform);

        const assetRef = obj.asset_ref ? String(obj.asset_ref).trim() : "";

        if (!assetRef) {
          const placeholder = makePlaceholderMesh(objId);
          group.add(placeholder);

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

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

          gltfRoot.traverse((node) => {
            if (!node || !node.isMesh) return;

            applyOpacityToMaterial(node.material, cfg.opacity);

            if (cfg.pickable) {
              pickables.push(node);
              meshToObjectId.set(node, objId);
            }
          });
        } catch (e) {
          const placeholder = makePlaceholderMesh(`${objId} (failed)`);
          group.add(placeholder);

          applyOpacityToMaterial(placeholder.material, cfg.opacity);

          if (cfg.pickable) {
            pickables.push(placeholder);
            meshToObjectId.set(placeholder, objId);
          }

          setErr((prev) => prev || String(e?.message || e));
        } finally {
          setLoadingCount((c) => Math.max(0, c - 1));
        }
      }

      // default framing after load
      fitCameraToScene(camera, root);
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

      // ✅ use named ancestor only for nicer mesh_path (6G.5)
      const idNode = pickIdNodeForMeshPath(hitMesh);

      const id = buildPickedTargetId({ objectId, mesh: idNode });
      if (!id) {
        clearSelection();
        return;
      }

      setSelectedId(id);
    }

    // ✅ 6G.7: double-click = select + frame object
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

    // ✅ 6G.7: F key framing (no selection mutation)
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

    return () => {
      disposed = true;
      cancelAnimationFrame(raf);

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
    };
    // ✅ re-run on objects/disabled/layers/selection (selection needed for F framing)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [JSON.stringify(objects), disabled, JSON.stringify(layers.kinds), selectedId]);

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

      <div ref={containerRef} className="border rounded overflow-hidden" style={{ height: 460 }}>
        <canvas ref={canvasRef} style={{ width: "100%", height: "100%", display: "block" }} />
      </div>

      <div className="text-xs opacity-70">
        Click mesh/placeholder to select. Double-click to focus. Press <b>F</b> to frame selected (or whole scene).
      </div>
    </div>
  );
}
