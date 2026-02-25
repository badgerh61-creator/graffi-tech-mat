// frontend/src/services/studio/sceneApi.js
import { getAccessToken } from "../../utils/auth";

const API_BASE = "http://127.0.0.1:8000";

export async function fetchScene(projectId, snapshotId) {
  const token = getAccessToken?.();

  const res = await fetch(
    `${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/scene`,
    {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }
  );

  if (!res.ok) throw new Error(`Failed to load scene (${res.status})`);
  return await res.json();
}
