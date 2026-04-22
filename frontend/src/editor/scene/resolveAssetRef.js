const cache = new Map();

/**
 * Tier 6G.3 — resolve asset reference
 */
export async function resolveAssetRef(assetRef) {
  if (!assetRef) return null;

  const ref = String(assetRef).trim();
  if (!ref) return null;

  // ✅ cache hit
  if (cache.has(ref)) return cache.get(ref);

  // ✅ pass-through relative paths
  if (ref.startsWith("/")) {
    cache.set(ref, ref);
    return ref;
  }

  // ✅ pass-through absolute URLs
  if (ref.startsWith("http://") || ref.startsWith("https://")) {
    cache.set(ref, ref);
    return ref;
  }

  // ✅ resolve asset:<id>
  if (ref.startsWith("asset:")) {
    const assetId = Number(ref.replace("asset:", "").trim());

    const res = await fetch(`http://127.0.0.1:8000/assets/${assetId}/url`);

    if (!res.ok) return null;

    const data = await res.json();
    const url = data?.url;

    if (!url) return null;

    cache.set(ref, url);
    return url;
  }

  return null;
}
