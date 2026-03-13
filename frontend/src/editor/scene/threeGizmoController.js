import * as THREE from "three";
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";
import {
  snapTranslateDelta,
  snapRotateDegrees,
  snapScaleFactor,
  applyAxisLockToAxis,
} from "../transform/snapMath";

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

function safeSnapState(raw) {
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

function chooseDominantRotationAxis(dx, dy, dz) {
  const ax = Math.abs(dx);
  const ay = Math.abs(dy);
  const az = Math.abs(dz);

  let axis = "y";
  let degrees = dy;

  if (ax >= ay && ax >= az) {
    axis = "x";
    degrees = dx;
  } else if (az >= ax && az >= ay) {
    axis = "z";
    degrees = dz;
  }

  return { axis, degrees };
}

function chooseScaleAxisAndFactor(obj, start) {
  const sx = obj.scale.x / (start.scale.x || 1);
  const sy = obj.scale.y / (start.scale.y || 1);
  const sz = obj.scale.z / (start.scale.z || 1);

  const avg = (sx + sy + sz) / 3;
  const spread = Math.max(
    Math.abs(sx - avg),
    Math.abs(sy - avg),
    Math.abs(sz - avg)
  );

  let axis = "uniform";
  let factor = avg;

  if (spread > 0.05) {
    const ax = Math.abs(sx - 1);
    const ay = Math.abs(sy - 1);
    const az = Math.abs(sz - 1);

    axis = "x";
    factor = sx;

    if (ay >= ax && ay >= az) {
      axis = "y";
      factor = sy;
    } else if (az >= ax && az >= ay) {
      axis = "z";
      factor = sz;
    }
  }

  if (!Number.isFinite(factor)) factor = 1;
  factor = Math.max(0.01, Math.min(100, factor));

  return { axis, factor };
}

/**
 * Creates a TransformControls gizmo and wires it to:
 * - preview updates during drag
 * - commit callback on drag end
 *
 * Required callbacks:
 * - getTargetGroup(): THREE.Object3D | null  (selected obj group)
 * - getMode(): "translate"|"rotate"|"scale"
 * - getSnap(): { enabled, step, step_degrees, step_factor, axis_lock, orientation }
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
    const snap = safeSnapState(getSnap?.());

    controls.setSpace(snap.orientation === "world" ? "world" : "local");

    if (controls.mode === "translate") {
      controls.setTranslationSnap(snap.enabled ? snap.step : null);
    } else if (controls.mode === "rotate") {
      controls.setRotationSnap(
        snap.enabled ? (snap.step_degrees * Math.PI) / 180 : null
      );
    } else if (controls.mode === "scale") {
      controls.setScaleSnap(snap.enabled ? snap.step_factor : null);
    }
  }

  // call this when selection/mode/snap changes
  function sync() {
    controls.setMode(getMode?.() || "translate");
    attachIfPossible();
    applySnapFromState();
  }

  function commitTranslate(obj, snap) {
    const rawDelta = obj.position.clone().sub(start.pos);
    const snapped = snapTranslateDelta(
      { x: rawDelta.x, y: rawDelta.y, z: rawDelta.z },
      snap
    );
    const d = roundVec3(snapped, 6);

    if (isNearlyZeroVec3(d, 1e-6)) return;

    const axis = applyAxisLockToAxis("free", snap);

    const payload = {
      tool: "TRANSLATE",
      station: "geometry",
      payload: {
        target_id: null,
        axis,
        delta: d,
        orientation: snap.orientation || "local",
        snap: {
          enabled: !!snap.enabled,
          step: snap.step || 0.1,
          axis_lock: snap.axis_lock || "none",
          orientation: snap.orientation || "local",
        },
      },
    };
    onCommit?.(payload);
  }

  function commitRotate(obj, snap) {
    const dx = roundDeg(radToDeg(obj.rotation.x - start.rot.x), 4);
    const dy = roundDeg(radToDeg(obj.rotation.y - start.rot.y), 4);
    const dz = roundDeg(radToDeg(obj.rotation.z - start.rot.z), 4);

    const chosen = chooseDominantRotationAxis(dx, dy, dz);
    const axis = applyAxisLockToAxis(chosen.axis, snap);
    const rawDegreesForAxis =
      axis === "x" ? dx : axis === "y" ? dy : axis === "z" ? dz : chosen.degrees;

    const degrees = roundDeg(snapRotateDegrees(rawDegreesForAxis, snap), 4);

    if (isNearlyZero(degrees, 1e-6)) return;

    const payload = {
      tool: "ROTATE",
      station: "geometry",
      payload: {
        target_id: null,
        axis,
        degrees,
        orientation: snap.orientation || "local",
        snap: {
          enabled: !!snap.enabled,
          step_degrees: snap.step_degrees || 5,
          axis_lock: snap.axis_lock || "none",
          orientation: snap.orientation || "local",
        },
      },
    };
    onCommit?.(payload);
  }

  function commitScale(obj, snap) {
    const chosen = chooseScaleAxisAndFactor(obj, start);
    const axis = applyAxisLockToAxis(chosen.axis, snap);
    const factor = round(snapScaleFactor(chosen.factor, snap), 6);

    if (isNearlyZero(factor - 1, 1e-6)) return;

    const payload = {
      tool: "SCALE",
      station: "geometry",
      payload: {
        target_id: null,
        axis,
        factor,
        orientation: snap.orientation || "local",
        snap: {
          enabled: !!snap.enabled,
          step_factor: snap.step_factor || 0.1,
          axis_lock: snap.axis_lock || "none",
          orientation: snap.orientation || "local",
        },
      },
    };
    onCommit?.(payload);
  }

  const onDraggingChanged = (e) => {
    dragging = !!e.value;

    const obj = controls.object;
    if (!obj) return;

    if (dragging) {
      dragSessionId += 1;
      committedForSession = false;
      captureStart(obj);
    } else {
      if (committedForSession) return;
      committedForSession = true;

      onPreview?.(null);

      const mode = controls.mode;
      const snap = safeSnapState(getSnap?.());

      if (mode === "translate") commitTranslate(obj, snap);
      if (mode === "rotate") commitRotate(obj, snap);
      if (mode === "scale") commitScale(obj, snap);
    }
  };

  const onObjectChange = () => {
    if (!dragging) return;
    const obj = controls.object;
    if (!obj) return;

    const mode = controls.mode;
    const snap = safeSnapState(getSnap?.());

    if (mode === "translate") {
      const rawDelta = obj.position.clone().sub(start.pos);
      const snapped = snapTranslateDelta(
        { x: rawDelta.x, y: rawDelta.y, z: rawDelta.z },
        snap
      );
      const d = roundVec3(snapped, 6);
      const axis = applyAxisLockToAxis("free", snap);

      onPreview?.({
        tool: "TRANSLATE",
        payload: {
          target_id: null,
          axis,
          delta: d,
          orientation: snap.orientation || "local",
          snap: {
            enabled: !!snap.enabled,
            step: snap.step || 0.1,
            axis_lock: snap.axis_lock || "none",
            orientation: snap.orientation || "local",
          },
        },
      });
    }

    if (mode === "rotate") {
      const dx = roundDeg(radToDeg(obj.rotation.x - start.rot.x), 4);
      const dy = roundDeg(radToDeg(obj.rotation.y - start.rot.y), 4);
      const dz = roundDeg(radToDeg(obj.rotation.z - start.rot.z), 4);

      const chosen = chooseDominantRotationAxis(dx, dy, dz);
      const axis = applyAxisLockToAxis(chosen.axis, snap);
      const rawDegreesForAxis =
        axis === "x" ? dx : axis === "y" ? dy : axis === "z" ? dz : chosen.degrees;

      const degrees = roundDeg(snapRotateDegrees(rawDegreesForAxis, snap), 4);

      onPreview?.({
        tool: "ROTATE",
        payload: {
          target_id: null,
          axis,
          degrees,
          orientation: snap.orientation || "local",
          snap: {
            enabled: !!snap.enabled,
            step_degrees: snap.step_degrees || 5,
            axis_lock: snap.axis_lock || "none",
            orientation: snap.orientation || "local",
          },
        },
      });
    }

    if (mode === "scale") {
      const chosen = chooseScaleAxisAndFactor(obj, start);
      const axis = applyAxisLockToAxis(chosen.axis, snap);
      const factor = round(snapScaleFactor(chosen.factor, snap), 6);

      onPreview?.({
        tool: "SCALE",
        payload: {
          target_id: null,
          axis,
          factor,
          orientation: snap.orientation || "local",
          snap: {
            enabled: !!snap.enabled,
            step_factor: snap.step_factor || 0.1,
            axis_lock: snap.axis_lock || "none",
            orientation: snap.orientation || "local",
          },
        },
      });
    }
  };

  controls.addEventListener("dragging-changed", onDraggingChanged);
  controls.addEventListener("objectChange", onObjectChange);

  function dispose() {
    try {
      controls.removeEventListener("dragging-changed", onDraggingChanged);
    } catch {}
    try {
      controls.removeEventListener("objectChange", onObjectChange);
    } catch {}
    try {
      controls.detach();
    } catch {}
    try {
      scene.remove(controls);
    } catch {}
    try {
      controls.dispose?.();
    } catch {}
  }

  return { controls, sync, detach, dispose };
}
