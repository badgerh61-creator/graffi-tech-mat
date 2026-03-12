import { API_BASE } from "../../config/apiBase";

export async function fetchDecalAssets() {
  const res = await fetch(`${API_BASE}/decor/decal-assets`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `decal-assets failed: ${res.status}`);
  return data?.assets || [];
}
