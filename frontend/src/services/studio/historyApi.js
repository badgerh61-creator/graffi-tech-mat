// frontend/src/services/studio/historyApi.ts

const API_BASE = "http://127.0.0.1:8000";

export async function undoSnapshot(projectId, snapshotId) {
  const res = await fetch(`${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/undo`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Undo failed (${res.status})`);
  return await res.json();
}

export async function redoSnapshot(projectId, snapshotId) {
  const res = await fetch(`${API_BASE}/projects/${projectId}/snapshots/${snapshotId}/redo`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Redo failed (${res.status})`);
  return await res.json();
}
