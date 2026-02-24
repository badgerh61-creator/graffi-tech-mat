function hash32(s: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

function idToPoint(id: string) {
  const h = hash32(id);
  const x = ((h & 0xff) / 255) * 10;
  const y = (((h >>> 8) & 0xff) / 255) * 5;
  const z = (((h >>> 16) & 0xff) / 255) * 2;
  return { x, y, z };
}

export type Vec3 = { x: number; y: number; z: number };
export type BBox = { min: Vec3; max: Vec3 };

export function computeSelectionBboxStub(ids: string[]): BBox | null {
  if (!ids || ids.length === 0) return null;

  const pts = ids.map(idToPoint);

  const min = { ...pts[0] };
  const max = { ...pts[0] };

  for (const p of pts) {
    if (p.x < min.x) min.x = p.x;
    if (p.y < min.y) min.y = p.y;
    if (p.z < min.z) min.z = p.z;

    if (p.x > max.x) max.x = p.x;
    if (p.y > max.y) max.y = p.y;
    if (p.z > max.z) max.z = p.z;
  }

  const round = (v: number) => Math.round(v * 1000) / 1000;

  return {
    min: { x: round(min.x), y: round(min.y), z: round(min.z) },
    max: { x: round(max.x), y: round(max.y), z: round(max.z) },
  };
}
