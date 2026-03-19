export function boxToPivotPreset(box, preset) {
  if (!box) return { x: 0, y: 0, z: 0 };

  const min = box.min;
  const max = box.max;

  const center = {
    x: (min.x + max.x) / 2,
    y: (min.y + max.y) / 2,
    z: (min.z + max.z) / 2,
  };

  if (preset === "center") {
    return center;
  }

  if (preset === "bounds_bottom_center") {
    return {
      x: center.x,
      y: min.y,
      z: center.z,
    };
  }

  return center;
}
