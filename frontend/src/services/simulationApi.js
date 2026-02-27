const API_BASE = "http://127.0.0.1:8000";

export async function createSimulationJob({ snapshotId, scenario, engineVersion, token }) {
  const res = await fetch(`${API_BASE}/simulation/jobs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({
      snapshot_id: snapshotId,
      scenario: scenario || {},
      engine_version: engineVersion || "pseudo-v1",
    }),
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `create sim job failed: ${res.status}`);
  return data;
}

export async function getTelemetryArtifact({ artifactId, token }) {
  const res = await fetch(`${API_BASE}/simulation/artifacts/${artifactId}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `get artifact failed: ${res.status}`);
  return data;
}
