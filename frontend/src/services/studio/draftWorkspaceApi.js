const API_BASE = "http://127.0.0.1:8000";

function authHeaders(getAccessToken) {
  const token = getAccessToken?.();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function readJson(res) {
  try { return await res.json(); } catch { return {}; }
}

export async function startEdit({ snapshotId, getAccessToken }) {
  const res = await fetch(`${API_BASE}/snapshots/${snapshotId}/start-edit`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders(getAccessToken) },
  });
  const data = await readJson(res);
  if (!res.ok) throw new Error(data?.detail || `start-edit failed: ${res.status}`);
  return data;
}

export async function completeDraft({ snapshotId, getAccessToken }) {
  const res = await fetch(`${API_BASE}/snapshots/${snapshotId}/complete-draft`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders(getAccessToken) },
  });
  const data = await readJson(res);
  if (!res.ok) throw new Error(data?.detail || `complete-draft failed: ${res.status}`);
  return data;
}

export async function discardDraft({ snapshotId, getAccessToken }) {
  const res = await fetch(`${API_BASE}/snapshots/${snapshotId}/discard-draft`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders(getAccessToken) },
  });
  const data = await readJson(res);
  if (!res.ok) throw new Error(data?.detail || `discard-draft failed: ${res.status}`);
  return data;
}
