export async function fetchSnapshotState(token, snapshotId) {
  const res = await fetch(
    `http://localhost:8000/studio/snapshots/${snapshotId}/state`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.json();
}

export async function fetchStudioContext(token, snapshotId) {
  const res = await fetch(
    `http://localhost:8000/studio/context?snapshot_id=${snapshotId}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return res.json();
}

