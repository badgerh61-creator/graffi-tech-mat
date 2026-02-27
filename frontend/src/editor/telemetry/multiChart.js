export function normalizeRuns(runs, curveName) {
  const series = [];

  for (const art of runs || []) {
    const t = art?.curves?.time_s || [];
    const y = art?.curves?.[curveName] || [];

    const n = Math.min(t.length, y.length);
    const pts = [];

    for (let i = 0; i < n; i++) {
      const x = Number(t[i]);
      const v = Number(y[i]);
      if (Number.isFinite(x) && Number.isFinite(v)) pts.push({ x, y: v });
    }

    series.push({ artifact_id: art.artifact_id, points: pts });
  }

  return series.sort((a, b) => a.artifact_id - b.artifact_id);
}

export function toPolyline(points, width, height, pad = 8) {
  if (!points?.length) return "";

  let minX = points[0].x, maxX = points[0].x;
  let minY = points[0].y, maxY = points[0].y;

  for (const p of points) {
    minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x);
    minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y);
  }

  const dx = maxX - minX || 1;
  const dy = maxY - minY || 1;

  return points.map((p) => {
    const nx = (p.x - minX) / dx;
    const ny = (p.y - minY) / dy;

    const x = pad + nx * (width - pad * 2);
    const y = pad + (1 - ny) * (height - pad * 2);

    return `${x.toFixed(2)},${y.toFixed(2)}`;
  }).join(" ");
}
