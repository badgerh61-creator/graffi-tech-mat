export async function fetchToolGuidance(token) {
  const res = await fetch("http://localhost:8000/studio/tools", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function fetchFlowGuidance(token) {
  const res = await fetch("http://localhost:8000/studio/flow", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

