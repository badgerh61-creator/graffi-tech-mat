/**
 * Tier 6G.27 — Scene normalization
 */
export function normalizeSceneObjects(objects) {
  if (!Array.isArray(objects)) return [];

  return objects.map((o, i) => ({
    id: String(o.id ?? i),

    kind: String(o.kind || "unknown"),

    asset_ref: o.asset_ref ?? null,

    transform: {
      position: {
        x: Number(o.transform?.position?.x || 0),
        y: Number(o.transform?.position?.y || 0),
        z: Number(o.transform?.position?.z || 0),
      },
      rotation: {
        x: Number(o.transform?.rotation?.x || 0),
        y: Number(o.transform?.rotation?.y || 0),
        z: Number(o.transform?.rotation?.z || 0),
      },
      scale: {
        x: Number(o.transform?.scale?.x ?? 1),
        y: Number(o.transform?.scale?.y ?? 1),
        z: Number(o.transform?.scale?.z ?? 1),
      },
    },

    material_overrides: o.material_overrides || {},

    decals: Array.isArray(o.decals) ? o.decals : [],
  }));
}
