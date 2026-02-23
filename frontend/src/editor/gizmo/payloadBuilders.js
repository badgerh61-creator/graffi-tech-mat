import { snapVec3, snapValue } from "./snap";

export function buildTranslatePayload({ targetId, axis, rawDelta, snap }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step ?? 0;
  const delta = enabled ? snapVec3(rawDelta, step) : rawDelta;

  return {
    tool: "TRANSLATE",
    station: "geometry",
    payload: {
      target_id: targetId,
      axis,
      delta,
      snap: { enabled, step },
    },
  };
}

export function buildRotatePayload({ targetId, axis, rawDegrees, snap }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step_degrees ?? 0;
  const degrees = enabled ? snapValue(rawDegrees, step) : rawDegrees;

  return {
    tool: "ROTATE",
    station: "geometry",
    payload: {
      target_id: targetId,
      axis,
      degrees,
      snap: { enabled, step_degrees: step },
    },
  };
}

export function buildScalePayload({ targetId, axis, rawFactor, snap }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step_factor ?? 0;
  const factor = enabled ? snapValue(rawFactor, step) : rawFactor;

  return {
    tool: "SCALE",
    station: "geometry",
    payload: {
      target_id: targetId,
      axis, // x|y|z|uniform
      factor,
      snap: { enabled, step_factor: step },
    },
  };
}
