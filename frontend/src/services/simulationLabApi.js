const API_BASE = "http://127.0.0.1:8000";

function auth(token) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function createScenario({ projectId, name, scenario, token }) {
  const res = await fetch(`${API_BASE}/simulation/scenarios`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...auth(token) },
    body: JSON.stringify({ project_id: projectId, name, scenario }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `create scenario failed: ${res.status}`);
  return data;
}

export async function listScenarios({ projectId, token }) {
  const res = await fetch(`${API_BASE}/simulation/scenarios?project_id=${projectId}`, {
    headers: auth(token),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `list scenarios failed: ${res.status}`);
  return data;
}

export async function runScenario({ snapshotId, engineVersion, scenarioId, scenario, token }) {
  const res = await fetch(`${API_BASE}/simulation/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...auth(token) },
    body: JSON.stringify({
      snapshot_id: snapshotId,
      engine_version: engineVersion,
      scenario_id: scenarioId ?? null,
      scenario: scenario ?? null,
    }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `run failed: ${res.status}`);
  return data;
}

export async function listRuns({ projectId, token }) {
  const res = await fetch(`${API_BASE}/simulation/runs?project_id=${projectId}`, {
    headers: auth(token),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `list runs failed: ${res.status}`);
  return data;
}

export async function compareMatrix({ artifactIds, token }) {
  const res = await fetch(`${API_BASE}/simulation/compare/matrix`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...auth(token) },
    body: JSON.stringify({ artifact_ids: artifactIds }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `matrix failed: ${res.status}`);
  return data;
}
