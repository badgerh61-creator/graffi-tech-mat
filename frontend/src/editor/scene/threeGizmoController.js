import * as THREE from "three";
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";

function cloneVec3(v) {
  return { x: v.x, y: v.y, z: v.z };
}

function radToDeg(r) {
  return (r * 180) / Math.PI;
}

/**
 * Deterministic rounding (helps diffs + avoids float jitter commits)
 */
function round(n, p = 6) {
  const f = Math.pow(10, p);
  const x = Number(n);
  if (!Number.isFinite(x)) return 0;
  return Math.round(x * f) / f;
}

function roundVec3(v, p = 6) {
  return { x: round(v.x, p), y: round(v.y, p), z: round(v.z, p) };
}

function roundDeg(n, p = 4) {
  return round(n, p);
}

/**
 * Small epsilon checks to avoid no-op commits caused by float noise.
 */
function isNearlyZeroVec3(d, eps = 1e-6) {
  return Math.abs(d.x) < eps && Math.abs(d.y) < eps && Math.abs(d.z) < eps;
}

function isNearlyZero(n, eps = 1e-6) {
  return Math.abs(n) < eps;
}

/**
 * Creates a TransformControls gizmo and wires it to:
 * - preview updates during drag
 * - commit callback on drag end
 *
 * Required callbacks:
 * - getTargetGroup(): THREE.Object3D | null  (selected obj group)
 * - getMode(): "translate"|"rotate"|"scale"
 * - getSnap(): { enabled, step, step_degrees, step_factor }
 * - onPreview(previewState|null)
 * - onCommit(toolPayload)   (single commit on release)
 */
export function createThreeGizmoController({
  camera,
  domElement,
  scene,
  getTargetGroup,
  getMode,
  getSnap,
  onPreview,
  onCommit,
}) {
  const controls = new TransformControls(camera, domElement);
  controls.setSpace("local");
  scene.add(controls);

  let dragging = false;

  // Guards against duplicate drag-end commits.
  let dragSessionId = 0;
  let committedForSession = false;

  let start = {
    pos: new THREE.Vector3(),
    rot: new THREE.Euler(),
    scale: new THREE.Vector3(),
  };

  function captureStart(obj) {
    start.pos.copy(obj.position);
    start.rot.copy(obj.rotation);
    start.scale.copy(obj.scale);
  }

  function detach() {
    controls.detach();
  }

  function attachIfPossible() {
    const target = getTargetGroup?.();
    if (!target) {
      detach();
      return;
    }
    controls.attach(target);
    controls.setMode(getMode?.() || "translate");
  }

  function applySnapFromState() {
    const snap = getSnap?.() || {};
    if (controls.mode === "translate") {
      controls.setTranslationSnap(snap.enabled ? snap.step || null : null);
    } else if (controls.mode === "rotate") {
      // rotate snap is in radians
      controls.setRotationSnap(
        snap.enabled ? ((snap.step_degrees || 0) * Math.PI) / 180 : null
      );
    } else if (controls.mode === "scale") {
      controls.setScaleSnap(snap.enabled ? snap.step_factor || null : null);
    }
  }

  // call this when selection/mode/snap changes
  function sync() {
    // Always update mode first (important if selection didn't change)
    controls.setMode(getMode?.() || "translate");

    // Ensure attachment is correct (selection might have changed)
    attachIfPossible();

    // Optional snapping (always refresh; avoids stale snap when toggled)
    applySnapFromState();
  }

  function commitTranslate(obj, snap) {
    const delta = obj.position.clone().sub(start.pos);
    const d = roundVec3(delta, 6);

    // prevent no-op commits
    if (isNearlyZeroVec3(d, 1e-6)) return;

    const payload = {
      tool: "TRANSLATE",
      station: "geometry",
      payload: {
        target_id: null, // caller should fill
        axis: "free",
        delta: d,
        snap: { enabled: !!snap.enabled, step: snap.step || 0 },
      },
    };
    onCommit?.(payload);
  }

  function commitRotate(obj, snap) {
    const dx = roundDeg(radToDeg(obj.rotation.x - start.rot.x), 4);
    const dy = roundDeg(radToDeg(obj.rotation.y - start.rot.y), 4);
    const dz = roundDeg(radToDeg(obj.rotation.z - start.rot.z), 4);

    // choose dominant axis change to keep payload canonical
    const ax = Math.abs(dx), ay = Math.abs(dy), az = Math.abs(dz);
    let axis = "y", degrees = dy;
    if (ax >= ay && ax >= az) { axis = "x"; degrees = dx; }
    else if (az >= ax && az >= ay) { axis = "z"; degrees = dz; }

    // prevent no-op commits
    if (isNearlyZero(degrees, 1e-6)) return;

    const payload = {
      tool: "ROTATE",
      station: "geometry",
      payload: {
        target_id: null,
        axis,
        degrees,
        snap: { enabled: !!snap.enabled, step_degrees: snap.step_degrees || 0 },
      },
    };
    onCommit?.(payload);
  }

  function commitScale(obj, snap) {
    const sx = obj.scale.x / (start.scale.x || 1);
    const sy = obj.scale.y / (start.scale.y || 1);
    const sz = obj.scale.z / (start.scale.z || 1);

    // choose uniform if nearly uniform
    const avg = (sx + sy + sz) / 3;
    const spread = Math.max(Math.abs(sx - avg), Math.abs(sy - avg), Math.abs(sz - avg));

    let axis = "uniform";
    let factor = avg;

    if (spread > 0.05) {
      // dominant axis scaling
      const ax = Math.abs(sx - 1), ay = Math.abs(sy - 1), az = Math.abs(sz - 1);
      axis = "x"; factor = sx;
      if (ay >= ax && ay >= az) { axis = "y"; factor = sy; }
      else if (az >= ax && az >= ay) { axis = "z"; factor = sz; }
    }

    // clamp + round
    if (!Number.isFinite(factor)) factor = 1;
    factor = Math.max(0.01, Math.min(100, factor));
    factor = round(factor, 6);

    // prevent no-op commits
    if (isNearlyZero(factor - 1, 1e-6)) return;

    const payload = {
      tool: "SCALE",
      station: "geometry",
      payload: {
        target_id: null,
        axis,
        factor,
        snap: { enabled: !!snap.enabled, step_factor: snap.step_factor || 0 },
      },
    };
    onCommit?.(payload);
  }

  // When dragging begins/ends
  const onDraggingChanged = (e) => {
    dragging = !!e.value;

    const obj = controls.object;
    if (!obj) return;

    if (dragging) {
      // New drag session
      dragSessionId += 1;
      committedForSession = false;

      captureStart(obj);
    } else {
      // drag ended => commit once
      if (committedForSession) return;
      committedForSession = true;

      onPreview?.(null);

      const mode = controls.mode;
      const snap = getSnap?.() || {};

      // compute deltas
      if (mode === "translate") commitTranslate(obj, snap);
      if (mode === "rotate") commitRotate(obj, snap);
      if (mode === "scale") commitScale(obj, snap);
    }
  };

  // While dragging, emit preview updates
  const onObjectChange = () => {
    if (!dragging) return;
    const obj = controls.object;
    if (!obj) return;

    const mode = controls.mode;
    const snap = getSnap?.() || {};

    if (mode === "translate") {
      const delta = obj.position.clone().sub(start.pos);
      const d = roundVec3(delta, 6);

      onPreview?.({
        tool: "TRANSLATE",
        payload: {
          target_id: null,
          axis: "free",
          delta: d,
          snap: { enabled: !!snap.enabled, step: snap.step || 0 },
        },
      });
    }

    if (mode === "rotate") {
      const dx = roundDeg(radToDeg(obj.rotation.x - start.rot.x), 4);
      const dy = roundDeg(radToDeg(obj.rotation.y - start.rot.y), 4);
      const dz = roundDeg(radToDeg(obj.rotation.z - start.rot.z), 4);

      const ax = Math.abs(dx), ay = Math.abs(dy), az = Math.abs(dz);
      let axis = "y", degrees = dy;
      if (ax >= ay && ax >= az) { axis = "x"; degrees = dx; }
      else if (az >= ax && az >= ay) { axis = "z"; degrees = dz; }

      onPreview?.({
        tool: "ROTATE",
        payload: {
          target_id: null,
          axis,
          degrees,
          snap: { enabled: !!snap.enabled, step_degrees: snap.step_degrees || 0 },
        },
      });
    }

    if (mode === "scale") {
      const sx = obj.scale.x / (start.scale.x || 1);
      const sy = obj.scale.y / (start.scale.y || 1);
      const sz = obj.scale.z / (start.scale.z || 1);

      const avg = (sx + sy + sz) / 3;
      const spread = Math.max(Math.abs(sx - avg), Math.abs(sy - avg), Math.abs(sz - avg));

      let axis = "uniform";
      let factor = avg;

      if (spread > 0.05) {
        const ax = Math.abs(sx - 1), ay = Math.abs(sy - 1), az = Math.abs(sz - 1);
        axis = "x"; factor = sx;
        if (ay >= ax && ay >= az) { axis = "y"; factor = sy; }
        else if (az >= ax && az >= ay) { axis = "z"; factor = sz; }
      }

      if (!Number.isFinite(factor)) factor = 1;
      factor = Math.max(0.01, Math.min(100, factor));
      factor = round(factor, 6);

      onPreview?.({
        tool: "SCALE",
        payload: {
          target_id: null,
          axis,
          factor,
          snap: { enabled: !!snap.enabled, step_factor: snap.step_factor || 0 },
        },
      });
    }
  };

  controls.addEventListener("dragging-changed", onDraggingChanged);
  controls.addEventListener("objectChange", onObjectChange);

  /**
   * Optional: full cleanup (recommended for React unmount)
   * - does NOT remove your detach()
   * - does NOT remove anything else
   */
  function dispose() {
    try { controls.removeEventListener("dragging-changed", onDraggingChanged); } catch {}
    try { controls.removeEventListener("objectChange", onObjectChange); } catch {}
    try { controls.detach(); } catch {}
    try { scene.remove(controls); } catch {}
    try { controls.dispose?.(); } catch {}
  }

  return { controls, sync, detach, dispose };
}
