const API_BASE = "http://127.0.0.1:8000";

export async function fetchDecalAssets() {
  const res = await fetch(`${API_BASE}/decor/decal-assets`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `decal-assets failed: ${res.status}`);
  return data?.assets || [];
}
