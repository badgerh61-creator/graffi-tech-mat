const API_BASE = "http://127.0.0.1:8000";

/**
 * Resolve scene object's asset_ref into a loadable URL.
 * Supported:
 * - "asset:<id>" -> GET /assets/<id>/url
 * - "http(s)://..." passthrough
 * - "/path.glb" passthrough (dev)
 */
export async function resolveAssetRef(assetRef) {
  if (!assetRef) return null;

  const ref = String(assetRef).trim();
  if (!ref) return null;

  if (ref.startsWith("asset:")) {
    const idStr = ref.slice("asset:".length).trim();
    const assetId = Number(idStr);
    if (!Number.isFinite(assetId)) return null;

    const res = await fetch(`${API_BASE}/assets/${assetId}/url`);
    if (!res.ok) throw new Error(`Failed to resolve asset:${assetId} (${res.status})`);
    const data = await res.json();

    // Only GLB is supported by the viewer
    if (data.type && data.type !== "glb") {
      throw new Error(`Asset ${assetId} is not a GLB`);
    }
    return data.url;
  }

  if (ref.startsWith("http://") || ref.startsWith("https://")) return ref;
  return ref; // allow "/vehicles/x.glb" dev paths
}
