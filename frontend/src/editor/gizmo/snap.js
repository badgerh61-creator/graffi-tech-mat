export function snapValue(value, step) {
  if (!step || step <= 0) return value;
  const k = Math.round(value / step);
  return k * step;
}

export function snapVec3(delta, step) {
  return {
    x: snapValue(delta.x ?? 0, step),
    y: snapValue(delta.y ?? 0, step),
    z: snapValue(delta.z ?? 0, step),
  };
}
