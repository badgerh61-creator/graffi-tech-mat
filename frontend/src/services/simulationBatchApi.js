import { API_BASE } from "../config/apiBase";
const auth = (token) => (token ? { Authorization: `Bearer ${token}` } : {});

export async function createBatch({ snapshotId, engineVersion, scenarioIds, templateKeys, templateOverrides, token }) {
  const res = await fetch(`${API_BASE}/simulation/batches`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...auth(token) },
    body: JSON.stringify({
      snapshot_id: snapshotId,
      engine_version: engineVersion || "pseudo-v1",
      scenario_ids: scenarioIds || [],
      template_keys: templateKeys || [],
      template_overrides: templateOverrides || {},
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `batch create failed: ${res.status}`);
  return data;
}

export async function getBatchStatus({ batchId, token }) {
  const res = await fetch(`${API_BASE}/simulation/batches/${batchId}`, { headers: auth(token) });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `batch status failed: ${res.status}`);
  return data;
}
