import { snapVec3, snapValue } from "./snap";

/**
 * Tier 7.22
 * Merge multi-select + pivot + bbox context into payload.
 */
function mergeContext(payload, ctx) {
  if (!ctx) return payload;

  return {
    ...payload,
    target_id: ctx.target_id,                 // enforce canonical primary
    selected_target_ids: ctx.selected_target_ids,
    pivot_mode: ctx.pivot_mode,
    pivot: ctx.pivot,
    selection_bbox: ctx.selection_bbox,
  };
}

export function buildTranslatePayload({ targetId, axis, rawDelta, snap, context }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step ?? 0;
  const delta = enabled ? snapVec3(rawDelta, step) : rawDelta;

  const payload = {
    target_id: targetId,
    axis,
    delta,
    snap: { enabled, step },
  };

  return {
    tool: "TRANSLATE",
    station: "geometry",
    payload: mergeContext(payload, context),
  };
}

export function buildRotatePayload({ targetId, axis, rawDegrees, snap, context }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step_degrees ?? 0;
  const degrees = enabled ? snapValue(rawDegrees, step) : rawDegrees;

  const payload = {
    target_id: targetId,
    axis,
    degrees,
    snap: { enabled, step_degrees: step },
  };

  return {
    tool: "ROTATE",
    station: "geometry",
    payload: mergeContext(payload, context),
  };
}

export function buildScalePayload({ targetId, axis, rawFactor, snap, context }) {
  const enabled = !!snap?.enabled;
  const step = snap?.step_factor ?? 0;
  const factor = enabled ? snapValue(rawFactor, step) : rawFactor;

  const payload = {
    target_id: targetId,
    axis,
    factor,
    snap: { enabled, step_factor: step },
  };

  return {
    tool: "SCALE",
    station: "geometry",
    payload: mergeContext(payload, context),
  };
}
