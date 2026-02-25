import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

import { resolveAssetRef } from "./resolveAssetRef";
import { buildPickedTargetId } from "./pickingId";
import { clearSelection, setSelectedId, useSelection } from "../selection/selectionStore";

function makeRenderer(canvas) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true });
  r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  return r;
}

function makeCamera(width, height) {
  const cam = new THREE.PerspectiveCamera(45, width / height, 0.1, 5000);
  cam.position.set(2.5, 1.5, 2.5);
  cam.lookAt(0, 0.8, 0);
  return cam;
}

function fitCameraToObject(camera, object3d) {
  const box = new THREE.Box3().setFromObject(object3d);
  if (box.isEmpty()) return;

  const size = new THREE.Vector3();
  const center = new THREE.Vector3();
  box.getSize(size);
  box.getCenter(center);

  const maxDim = Math.max(size.x, size.y, size.z) || 1;
  const fov = (camera.fov * Math.PI) / 180;
  const distance = (maxDim / (2 * Math.tan(fov / 2))) * 1.4;

  camera.position.set(center.x + distance, center.y + distance * 0.5, center.z + distance);
  camera.lookAt(center);
  camera.updateProjectionMatrix();
}

export default function ThreeSceneViewer({ sceneIndex, disabled = false }) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  const { selectedId } = useSelection();
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  // Pick the first object with asset_ref
  const primaryObj = useMemo(() => {
    const objs = sceneIndex?.objects || [];
    return objs.find((o) => o?.asset_ref) || null;
  }, [sceneIndex]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    let disposed = false;

    const scene = new THREE.Scene();
    const renderer = makeRenderer(canvas);

    // lights + ground
    scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 1.0));
    const dir = new THREE.DirectionalLight(0xffffff, 1.0);
    dir.position.set(4, 6, 3);
    scene.add(dir);
    scene.add(new THREE.GridHelper(10, 10));

    // camera
    const rect = container.getBoundingClientRect();
    const camera = makeCamera(rect.width || 800, rect.height || 500);

    // orbit-like drag
    let isDragging = false, lastX = 0, lastY = 0;
    function onPointerDown(e) { isDragging = true; lastX = e.clientX; lastY = e.clientY; }
    function onPointerUp() { isDragging = false; }
    function onPointerMove(e) {
      if (!isDragging) return;
      const dx = (e.clientX - lastX) * 0.005;
      const dy = (e.clientY - lastY) * 0.005;
      lastX = e.clientX; lastY = e.clientY;

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

    // glb + picking
    let gltfRoot = null;
    let pickables = [];
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    async function load() {
      setErr(null);
      pickables = [];
      if (!primaryObj?.asset_ref) return;

      setLoading(true);
      try {
        const url = await resolveAssetRef(primaryObj.asset_ref);
        if (!url) throw new Error("asset_ref could not be resolved");

        const loader = new GLTFLoader();
        const gltf = await loader.loadAsync(url);
        if (disposed) return;

        gltfRoot = gltf.scene;
        scene.add(gltfRoot);

        // apply transform from scene index
        const t = primaryObj?.transform || {};
        const p = t.position || {};
        const r = t.rotation || {};
        const s = t.scale || {};

        gltfRoot.position.set(p.x || 0, p.y || 0, p.z || 0);
        gltfRoot.rotation.set(r.x || 0, r.y || 0, r.z || 0);
        gltfRoot.scale.set(s.x || 1, s.y || 1, s.z || 1);
        gltfRoot.updateMatrixWorld(true);

        // pickable meshes
        gltfRoot.traverse((node) => {
          if (node && node.isMesh) pickables.push(node);
        });

        fitCameraToObject(camera, gltfRoot);
      } catch (e) {
        setErr(String(e?.message || e));
      } finally {
        setLoading(false);
      }
    }

    load();

    function onClick(e) {
      if (disabled) return;
      if (!primaryObj?.id) return;

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

      const mesh = hits[0].object;
      const id = buildPickedTargetId({ objectId: primaryObj.id, mesh });
      if (!id) {
        clearSelection();
        return;
      }
      setSelectedId(id);
    }

    canvas.addEventListener("click", onClick);

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

      container.removeEventListener("pointerdown", onPointerDown);
      container.removeEventListener("pointerup", onPointerUp);
      container.removeEventListener("pointerleave", onPointerUp);
      container.removeEventListener("pointermove", onPointerMove);

      ro.disconnect();

      if (gltfRoot) {
        scene.remove(gltfRoot);
        gltfRoot.traverse((node) => {
          if (node?.isMesh) {
            node.geometry?.dispose?.();
            const mat = node.material;
            if (Array.isArray(mat)) mat.forEach((m) => m?.dispose?.());
            else mat?.dispose?.();
          }
        });
      }

      renderer.dispose();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [primaryObj?.asset_ref, primaryObj?.id, disabled]);

  const selectedShort = selectedId ? selectedId.split("::").slice(-1)[0] : "none";

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Viewport (Three.js)</div>
        <div className="text-xs opacity-75">Picked: {selectedShort}</div>
      </div>

      {err ? <div className="text-sm text-red-600">{err}</div> : null}
      {loading ? <div className="text-sm opacity-75">Loading GLB…</div> : null}

      {!primaryObj?.asset_ref ? (
        <div className="text-sm opacity-75">
          No asset_ref found in scene index. Use Attach Asset (6G.2) first.
        </div>
      ) : null}

      <div ref={containerRef} className="border rounded overflow-hidden" style={{ height: 420 }}>
        <canvas ref={canvasRef} style={{ width: "100%", height: "100%", display: "block" }} />
      </div>

      <div className="text-xs opacity-70">Click mesh to select. Click empty clears selection.</div>
    </div>
  );
}
