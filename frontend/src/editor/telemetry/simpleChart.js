export function normalizeSeries(xs, ys) {
  const n = Math.min(xs?.length || 0, ys?.length || 0);
  const pts = [];
  for (let i = 0; i < n; i++) {
    const x = Number(xs[i]);
    const y = Number(ys[i]);
    if (Number.isFinite(x) && Number.isFinite(y)) pts.push({ x, y });
  }
  return pts;
}

export function toPolylinePoints(points, width, height, pad = 6) {
  if (!points.length) return "";

  let minX = points[0].x, maxX = points[0].x;
  let minY = points[0].y, maxY = points[0].y;
  for (const p of points) {
    minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x);
    minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y);
  }
  const dx = maxX - minX || 1;
  const dy = maxY - minY || 1;

  return points
    .map((p) => {
      const nx = (p.x - minX) / dx;
      const ny = (p.y - minY) / dy;
      const x = pad + nx * (width - pad * 2);
      const y = pad + (1 - ny) * (height - pad * 2);
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    })
    .join(" ");
}
