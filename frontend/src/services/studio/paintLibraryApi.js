const API_BASE = "http://127.0.0.1:8000";

export async function fetchPaintLibrary() {
  const res = await fetch(`${API_BASE}/materials/paint-library`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `paint-library failed: ${res.status}`);
  return data?.presets || [];
}
