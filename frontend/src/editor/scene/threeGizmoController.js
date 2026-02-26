import * as THREE from "three";
import { TransformControls } from "three/examples/jsm/controls/TransformControls.js";

function cloneVec3(v) {
  return { x: v.x, y: v.y, z: v.z };
}

function radToDeg(r) {
  return (r * 180) / Math.PI;
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

  // call this when selection/mode changes
  function sync() {
    attachIfPossible();

    // optional snapping
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

  // When dragging begins/ends
  controls.addEventListener("dragging-changed", (e) => {
    dragging = !!e.value;

    // disable orbit drag while transforming (if you have it)
    // you can gate your orbit handlers using this flag externally.

    const obj = controls.object;
    if (!obj) return;

    if (dragging) {
      captureStart(obj);
    } else {
      // drag ended => commit once
      onPreview?.(null);

      const mode = controls.mode;
      const snap = getSnap?.() || {};

      // compute deltas
      if (mode === "translate") {
        const delta = obj.position.clone().sub(start.pos);
        const payload = {
          tool: "TRANSLATE",
          station: "geometry",
          payload: {
            target_id: null, // caller should fill if needed, but we assume selection already encodes it
            axis: "free",
            delta: cloneVec3(delta),
            snap: { enabled: !!snap.enabled, step: snap.step || 0 },
          },
        };
        onCommit?.(payload);
      }

      if (mode === "rotate") {
        const dx = radToDeg(obj.rotation.x - start.rot.x);
        const dy = radToDeg(obj.rotation.y - start.rot.y);
        const dz = radToDeg(obj.rotation.z - start.rot.z);

        // choose dominant axis change to keep payload canonical
        const ax = Math.abs(dx), ay = Math.abs(dy), az = Math.abs(dz);
        let axis = "y", degrees = dy;
        if (ax >= ay && ax >= az) { axis = "x"; degrees = dx; }
        else if (az >= ax && az >= ay) { axis = "z"; degrees = dz; }

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

      if (mode === "scale") {
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

        // clamp
        if (!Number.isFinite(factor)) factor = 1;
        factor = Math.max(0.01, Math.min(100, factor));

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
    }
  });

  // While dragging, emit preview updates
  controls.addEventListener("objectChange", () => {
    if (!dragging) return;
    const obj = controls.object;
    if (!obj) return;

    const mode = controls.mode;
    const snap = getSnap?.() || {};

    if (mode === "translate") {
      const delta = obj.position.clone().sub(start.pos);
      onPreview?.({
        tool: "TRANSLATE",
        payload: {
          target_id: null,
          axis: "free",
          delta: cloneVec3(delta),
          snap: { enabled: !!snap.enabled, step: snap.step || 0 },
        },
      });
    }

    if (mode === "rotate") {
      const dx = radToDeg(obj.rotation.x - start.rot.x);
      const dy = radToDeg(obj.rotation.y - start.rot.y);
      const dz = radToDeg(obj.rotation.z - start.rot.z);

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
  });

  return { controls, sync, detach };
}
