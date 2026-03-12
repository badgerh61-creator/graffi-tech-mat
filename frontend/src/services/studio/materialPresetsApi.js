import { API_BASE } from "../../config/apiBase";

export async function fetchMaterialPresets() {
  const res = await fetch(`${API_BASE}/materials/presets`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `presets failed: ${res.status}`);
  return data?.presets || [];
}
