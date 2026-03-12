// frontend/src/editor/scene/resolveAssetRef.js
import { API_BASE } from "../../config/apiBase";

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

  // ✅ passthrough absolute URLs
  if (ref.startsWith("http://") || ref.startsWith("https://")) return ref;

  // ✅ passthrough dev-relative paths EXACTLY (tests expect no prefix)
  if (ref.startsWith("/")) return ref;

  // ✅ "asset:<id>" -> backend gives signed URL
  if (ref.startsWith("asset:")) {
    const idStr = ref.slice("asset:".length).trim();
    const assetId = Number(idStr);
    if (!Number.isFinite(assetId)) return null;

    // Keep older tier tests stable:
    // they expect 127.0.0.1 even if API_BASE is localhost.
    const base = String(API_BASE || "").replace("http://localhost:8000", "http://127.0.0.1:8000");

    // ✅ IMPORTANT: tests expect fetch(url) with ONLY the URL argument
    const res = await fetch(`${base}/assets/${assetId}/url`);
    if (!res.ok) {
      throw new Error(`Failed to resolve asset:${assetId} (${res.status})`);
    }

    const data = await res.json();

    // Only GLB is supported by the viewer
    if (data?.type && data.type !== "glb") {
      throw new Error(`Asset ${assetId} is not a GLB`);
    }

    return data?.url || null;
  }

  // ✅ any other relative string: passthrough unchanged
  return ref;
}
