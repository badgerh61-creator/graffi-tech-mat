const API_BASE = "http://127.0.0.1:8000";

export async function fetchScene(projectId, snapshotId) {
  const res = await fetch(`${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/scene`);
  if (!res.ok) throw new Error(`Failed to load scene (${res.status})`);
  return await res.json();
}
