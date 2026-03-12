import { API_BASE } from "../config/apiBase";
const auth = (token) => (token ? { Authorization: `Bearer ${token}` } : {});

export async function getRunRepro({ runId, token }) {
  const res = await fetch(`${API_BASE}/simulation/runs/${runId}/repro`, { headers: auth(token) });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `repro failed: ${res.status}`);
  return data;
}
