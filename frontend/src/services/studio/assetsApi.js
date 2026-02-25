const API_BASE = "http://127.0.0.1:8000";

export async function listAssets() {
  const res = await fetch(`${API_BASE}/assets/`);
  if (!res.ok) throw new Error(`Failed to list assets (${res.status})`);
  return await res.json(); // { items, total }
}

export async function attachAsset(projectId, snapshotId, payload) {
  const res = await fetch(
    `${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/tools/attach-asset`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }
  );
  if (!res.ok) throw new Error(`Failed to attach asset (${res.status})`);
  return await res.json();
}
