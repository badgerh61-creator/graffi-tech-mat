import { snapValue, snapVec3 } from "./snap";

export function makeTranslatePreview({ targetId, axis, rawDeltaAxis, snap }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step ?? 0;

  const rawDelta =
    axis === "x"
      ? { x: rawDeltaAxis, y: 0, z: 0 }
      : axis === "y"
      ? { x: 0, y: rawDeltaAxis, z: 0 }
      : { x: 0, y: 0, z: rawDeltaAxis };

  const delta = enabled ? snapVec3(rawDelta, step) : rawDelta;

  return {
    target_id: targetId,
    tool: "TRANSLATE",
    payload: { target_id: targetId, axis, delta, snap: { enabled, step } },
  };
}

export function makeRotatePreview({ targetId, axis, rawDegrees, snap }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step_degrees ?? 0;
  const degrees = enabled ? snapValue(rawDegrees, step) : rawDegrees;

  return {
    target_id: targetId,
    tool: "ROTATE",
    payload: { target_id: targetId, axis, degrees, snap: { enabled, step_degrees: step } },
  };
}

export function makeScalePreview({ targetId, axis, rawFactor, snap }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step_factor ?? 0;

  let factor = enabled ? snapValue(rawFactor, step) : rawFactor;
  if (!Number.isFinite(factor)) factor = 1;
  factor = Math.max(0.01, Math.min(100, factor));

  return {
    target_id: targetId,
    tool: "SCALE",
    payload: { target_id: targetId, axis, factor, snap: { enabled, step_factor: step } },
  };
}
