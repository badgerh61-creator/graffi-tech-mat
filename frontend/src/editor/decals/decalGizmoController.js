import * as THREE from "three";
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";
import { setDecalPreviewPatch, clearDecalPreviewPatch } from "./decalPreviewStore";

function round(n, p = 4) {
  const f = Math.pow(10, p);
  return Math.round((Number(n) || 0) * f) / f;
}

function vec3Patch(v, p = 4) {
  return { x: round(v.x, p), y: round(v.y, p), z: round(v.z, p) };
}

function eulerDegPatch(e, p = 2) {
  const radToDeg = 180 / Math.PI;
  return {
    x: round(e.x * radToDeg, p),
    y: round(e.y * radToDeg, p),
    z: round(e.z * radToDeg, p),
  };
}

/**
 * Decal gizmo:
 * - attaches to a THREE.Object3D proxy representing the decal
 * - emits preview patch while dragging
 * - on release, calls onCommitPatch(decalId, patch)
 */
export function createDecalGizmo({
  camera,
  domElement,
  scene,
  getActiveDecalId,
  getDecalProxy,      // (decalId) => Object3D | null
  getMode,            // translate|rotate|scale
  canEdit,            // () => boolean
  onCommitPatch,      // (decalId, patch) => void
}) {
  const controls = new TransformControls(camera, domElement);
  controls.setSpace("local");
  scene.add(controls);

  let dragging = false;
  let activeId = null;

  function detach() {
    controls.detach();
    activeId = null;
  }

  function sync() {
    const decalId = getActiveDecalId?.();
    if (!decalId) return detach();

    const ok = canEdit?.();
    if (!ok) return detach();

    const proxy = getDecalProxy?.(decalId);
    if (!proxy) return detach();

    activeId = String(decalId);
    controls.attach(proxy);
    controls.setMode(getMode?.() || "translate");
  }

  controls.addEventListener("dragging-changed", (e) => {
    dragging = !!e.value;
    if (!activeId) return;

    if (!dragging) {
      // commit once
      const obj = controls.object;
      if (!obj) return;

      const patch = {
        position: vec3Patch(obj.position, 4),
        rotation_euler: eulerDegPatch(obj.rotation, 2),
        scale: vec3Patch(obj.scale, 4),
      };

      clearDecalPreviewPatch(activeId);
      onCommitPatch?.(activeId, patch);
    }
  });

  controls.addEventListener("objectChange", () => {
    if (!dragging) return;
    if (!activeId) return;

    const obj = controls.object;
    if (!obj) return;

    const patch = {
      position: vec3Patch(obj.position, 4),
      rotation_euler: eulerDegPatch(obj.rotation, 2),
      scale: vec3Patch(obj.scale, 4),
    };

    setDecalPreviewPatch(activeId, patch);
  });

  return { controls, sync, detach };
}
