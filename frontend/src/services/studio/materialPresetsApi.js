const API_BASE = "http://127.0.0.1:8000";

export async function fetchMaterialPresets() {
  const res = await fetch(`${API_BASE}/materials/presets`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `presets failed: ${res.status}`);
  return data?.presets || [];
}
