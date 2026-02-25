import { snapVec3, snapValue } from "./snap";

/**
 * Tier 7.25 — Rotation + Scale parity (with Tier 7.22 context support)
 *
 * Guarantees:
 * - Deterministic payloads
 * - Numeric safety (no NaN propagation)
 * - Scale clamping
 * - Canonical target_id enforcement
 */

function safeNumber(v, fallback = 0) {
  return Number.isFinite(v) ? v : fallback;
}

function normalizeAxis(axis, fallback = "x") {
  if (!axis) return fallback;
  return String(axis).toLowerCase();
}

/**
 * Merge multi-select + pivot + bbox context into payload.
 * Canonical primary target enforced.
 */
function mergeContext(payload, ctx) {
  if (!ctx) return payload;

  return {
    ...payload,
    target_id: ctx.target_id, // canonical primary target
    selected_target_ids: ctx.selected_target_ids,
    pivot_mode: ctx.pivot_mode,
    pivot: ctx.pivot,
    selection_bbox: ctx.selection_bbox,
  };
}

/* =========================
   TRANSLATE
========================= */

export function buildTranslatePayload({
  targetId,
  axis,
  rawDelta,
  snap,
  context,
}) {
  const enabled = !!snap?.enabled;
  const step = safeNumber(snap?.step, 0);

  const sanitizedDelta = {
    x: safeNumber(rawDelta?.x, 0),
    y: safeNumber(rawDelta?.y, 0),
    z: safeNumber(rawDelta?.z, 0),
  };

  const delta = enabled ? snapVec3(sanitizedDelta, step) : sanitizedDelta;

  const payload = {
    target_id: targetId,
    axis: normalizeAxis(axis),
    delta,
    snap: { enabled, step },
  };

  return {
    tool: "TRANSLATE",
    station: "geometry",
    payload: mergeContext(payload, context),
  };
}

/* =========================
   ROTATE
========================= */

export function buildRotatePayload({
  targetId,
  axis,
  rawDegrees,
  snap,
  context,
}) {
  const enabled = !!snap?.enabled;
  const step = safeNumber(snap?.step_degrees, 0);

  const sanitized = safeNumber(rawDegrees, 0);
  const degrees = enabled ? snapValue(sanitized, step) : sanitized;

  const payload = {
    target_id: targetId,
    axis: normalizeAxis(axis),
    degrees,
    snap: { enabled, step_degrees: step },
  };

  return {
    tool: "ROTATE",
    station: "geometry",
    payload: mergeContext(payload, context),
  };
}

/* =========================
   SCALE
========================= */

export function buildScalePayload({
  targetId,
  axis,
  rawFactor,
  snap,
  context,
}) {
  const enabled = !!snap?.enabled;
  const step = safeNumber(snap?.step_factor, 0);

  let factor = safeNumber(rawFactor, 1);

  // Snap first
  if (enabled) {
    factor = snapValue(factor, step);
  }

  // Clamp to safe range
  factor = Math.max(0.01, Math.min(100, factor));

  const payload = {
    target_id: targetId,
    axis: normalizeAxis(axis, "uniform"),
    factor,
    snap: { enabled, step_factor: step },
  };

  return {
    tool: "SCALE",
    station: "geometry",
    payload: mergeContext(payload, context),
  };
}
