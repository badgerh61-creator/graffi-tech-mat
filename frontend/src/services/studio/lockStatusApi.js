const API_BASE = "http://127.0.0.1:8000";

async function readJson(res) {
  try { return await res.json(); } catch { return {}; }
}

/**
 * Expected response shape (canonical for UI):
 * { state: "owned"|"taken"|"missing", owner_id?: number, owner_name?: string }
 *
 * If your backend returns a different shape, normalize it here.
 */
export async function fetchDraftLockStatus({ snapshotId, getAccessToken }) {
  const token = getAccessToken?.();
  const res = await fetch(`${API_BASE}/snapshots/${snapshotId}/lock-status`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  const data = await readJson(res);
  if (!res.ok) throw new Error(data?.detail || `lock-status failed: ${res.status}`);
  return data;
}
