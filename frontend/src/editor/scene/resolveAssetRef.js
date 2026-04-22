import { API_BASE } from "../../config/apiBase";
import { getAccessToken } from "../../utils/auth"; // 🔥 FIX

const cache = new Map();

export async function resolveAssetRef(assetRef) {
  if (!assetRef) return null;

  const ref = String(assetRef).trim();
  if (!ref) return null;

  if (cache.has(ref)) return cache.get(ref);

  if (ref.startsWith("http://") || ref.startsWith("https://")) {
    cache.set(ref, ref);
    return ref;
  }

  if (ref.startsWith("asset:")) {
    const assetId = Number(ref.replace("asset:", "").trim());

    const base = API_BASE;
    const token = getAccessToken(); // ✅ FIXED

    console.log("🚀 FETCHING ASSET URL:", assetId);

    const res = await fetch(`${base}/assets/${assetId}/url`, {
      headers: token
        ? { Authorization: `Bearer ${token}` }
        : {},
    });

    console.log("📡 RESPONSE STATUS:", res.status);

    if (!res.ok) {
      console.error("❌ FAILED TO FETCH ASSET URL");
      return null;
    }

    const data = await res.json();

    console.log("📦 ASSET RESPONSE:", data);

    const url = data?.url;

    if (!url) {
      console.error("❌ NO URL RETURNED");
      return null;
    }

    cache.set(ref, url);
    return url;
  }

  return null;
}
