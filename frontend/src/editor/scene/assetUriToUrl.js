const API_BASE = "http://127.0.0.1:8000";

export function assetUriToUrl(ref) {
  if (!ref) return null;

  if (ref.startsWith("asset:")) {
    const id = ref.split(":")[1];
    return `${API_BASE}/assets/${id}/url`;
  }

  return ref;
}
