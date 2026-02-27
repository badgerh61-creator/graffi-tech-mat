const API_BASE = "http://127.0.0.1:8000";
const auth = (token) => (token ? { Authorization: `Bearer ${token}` } : {});

export async function listTemplates({ token }) {
  const res = await fetch(`${API_BASE}/simulation/templates`, {
    headers: auth(token),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.detail || `templates failed: ${res.status}`);
  return data;
}

export async function createScenarioFromTemplate({
  projectId,
  name,
  templateKey,
  engineVersion,
  overrides,
  token,
}) {
  const res = await fetch(`${API_BASE}/simulation/scenarios/from-template`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...auth(token) },
    body: JSON.stringify({
      project_id: projectId,
      name,
      template_key: templateKey,
      engine_version: engineVersion || "pseudo-v1",
      overrides: overrides || {},
    }),
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok)
    throw new Error(data?.detail || `create from template failed: ${res.status}`);
  return data;
}
