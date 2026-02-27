const API_BASE = "http://127.0.0.1:8000";

export async function getTelemetrySummary({ artifactId, token }) {
  const res = await fetch(`${API_BASE}/simulation/artifacts/${artifactId}/summary`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `summary failed: ${res.status}`);
  return data;
}

export async function compareTelemetry({ aArtifactId, bArtifactId, token }) {
  const res = await fetch(`${API_BASE}/simulation/compare`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify({ a_artifact_id: aArtifactId, b_artifact_id: bArtifactId }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `compare failed: ${res.status}`);
  return data;
}

export async function exportTelemetryCsv({ artifactId, token }) {
  const res = await fetch(`${API_BASE}/simulation/artifacts/${artifactId}/export.csv`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error(`export failed: ${res.status}`);
  return await res.text();
}
