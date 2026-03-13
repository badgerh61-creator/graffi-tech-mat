function round(n, p = 6) {
  const f = Math.pow(10, p);
  const x = Number(n);
  if (!Number.isFinite(x)) return 0;
  return Math.round(x * f) / f;
}

function roundToStep(value, step) {
  const v = Number(value) || 0;
  const s = Number(step);
  if (!Number.isFinite(s) || s <= 0) return round(v, 6);
  return round(Math.round(v / s) * s, 6);
}

function finiteOrZero(v) {
  return Number.isFinite(Number(v)) ? Number(v) : 0;
}

export function snapTranslateDelta(delta, snap) {
  const d = delta || {};
  const enabled = !!snap?.enabled;
  const step = Number(snap?.step) || 0.1;
  const axis = String(snap?.axis_lock || "none");

  let x = finiteOrZero(d.x);
  let y = finiteOrZero(d.y);
  let z = finiteOrZero(d.z);

  if (axis === "x") {
    y = 0;
    z = 0;
  }
  if (axis === "y") {
    x = 0;
    z = 0;
  }
  if (axis === "z") {
    x = 0;
    y = 0;
  }

  if (enabled) {
    x = roundToStep(x, step);
    y = roundToStep(y, step);
    z = roundToStep(z, step);
  } else {
    x = round(x, 6);
    y = round(y, 6);
    z = round(z, 6);
  }

  return { x, y, z };
}

export function snapRotateDegrees(degrees, snap) {
  const enabled = !!snap?.enabled;
  const step = Number(snap?.step_degrees) || 5;
  const deg = finiteOrZero(degrees);
  return enabled ? roundToStep(deg, step) : round(deg, 6);
}

export function snapScaleFactor(factor, snap) {
  const enabled = !!snap?.enabled;
  const step = Number(snap?.step_factor) || 0.1;
  const f = finiteOrZero(factor) || 1;
  const out = enabled ? roundToStep(f, step) : round(f, 6);
  return Math.max(0.01, round(out, 6));
}

export function applyAxisLockToAxis(axis, snap) {
  const locked = String(snap?.axis_lock || "none");
  if (locked === "x" || locked === "y" || locked === "z") return locked;
  return axis || "free";
}
