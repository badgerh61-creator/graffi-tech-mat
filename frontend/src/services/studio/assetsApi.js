// frontend/src/services/studio/assetsApi.js

import { getAccessToken } from "../../utils/auth";

const API_BASE = "http://127.0.0.1:8000";

function authHeaders(extra = {}) {
  const token = getAccessToken();
  return {
    ...extra,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function listAssets() {
  const res = await fetch(`${API_BASE}/assets/`, {
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(`Failed to list assets (${res.status})`);
  return await res.json(); // { items, total }
}

export async function attachAsset(projectId, snapshotId, payload) {
  const res = await fetch(
    `${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/tools/attach-asset`,
    {
      method: "POST",
      headers: authHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify(payload),
    }
  );

  const text = await res.text();
  if (!res.ok) throw new Error(text || `Failed to attach asset (${res.status})`);

  try {
    return JSON.parse(text);
  } catch {
    return { ok: true };
  }
}
