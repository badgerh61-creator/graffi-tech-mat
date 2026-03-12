// frontend/src/services/studio/draftWorkspaceApi.js

import { API_BASE } from "../../config/apiBase";

async function postJson(path, { getAccessToken } = {}) {
  const token = typeof getAccessToken === "function" ? getAccessToken() : null;

  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}), // backend doesn't require payload, but keep shape stable
  });

  // ✅ Avoid "Cannot read properties of undefined (reading 'ok')"
  if (!res) {
    throw new Error("Network error: no response");
  }

  // Best-effort parse for readable errors
  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    const msg =
      (data && (data.detail || data.message)) ||
      `Request failed: ${res.status}`;
    throw new Error(String(msg));
  }

  return data || {};
}

// ✅ Tier 7.35 endpoints (must match backend OpenAPI exactly)
export function startEdit({ snapshotId, getAccessToken }) {
  return postJson(`/snapshots/${snapshotId}/start-edit`, { getAccessToken });
}

export function completeDraft({ snapshotId, getAccessToken }) {
  return postJson(`/snapshots/${snapshotId}/complete-draft`, { getAccessToken });
}

export function discardDraft({ snapshotId, getAccessToken }) {
  return postJson(`/snapshots/${snapshotId}/discard-draft`, { getAccessToken });
}
