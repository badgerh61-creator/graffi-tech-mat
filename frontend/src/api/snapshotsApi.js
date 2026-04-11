import { getAccessToken } from "../utils/auth";

const API = "http://localhost:8000";

async function authFetch(url, options = {}) {
  const token = getAccessToken();

  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
      Authorization: token ? `Bearer ${token}` : undefined,
    },
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`${res.status} ${text}`);
  }

  return res.json();
}

export const snapshotsApi = {
  async getLockStatus(snapshotId) {
    return authFetch(`${API}/snapshots/${snapshotId}/lock-status`);
  },

  async lock(snapshotId) {
    return authFetch(`${API}/snapshots/${snapshotId}/lock`, {
      method: "POST",
    });
  },

  async unlock(snapshotId) {
    return authFetch(`${API}/snapshots/${snapshotId}/unlock`, {
      method: "POST",
    });
  },
};
