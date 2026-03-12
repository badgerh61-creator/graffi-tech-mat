import { API_BASE } from "../../config/apiBase";

function authHeaders(getAccessToken) {
  const token = getAccessToken?.();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function safeJson(res) {
  try {
    return await res.json();
  } catch {
    return {};
  }
}

export async function evaluateProposal({ snapshotId, proposal, getAccessToken }) {
  const res = await fetch(`${API_BASE}/assistant/proposals/evaluate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(getAccessToken),
    },
    body: JSON.stringify({ snapshot_id: snapshotId, proposal }),
  });

  const data = await safeJson(res);
  if (!res.ok) {
    const msg = data?.detail || `evaluate failed: ${res.status}`;
    throw new Error(msg);
  }
  return data; // expects {allowed:boolean, reason?:string, ...}
}

export async function previewProposal({ snapshotId, proposal, getAccessToken }) {
  const res = await fetch(`${API_BASE}/assistant/proposals/preview`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(getAccessToken),
    },
    body: JSON.stringify({ snapshot_id: snapshotId, proposal }),
  });

  const data = await safeJson(res);
  if (!res.ok) {
    const msg = data?.detail || `preview failed: ${res.status}`;
    throw new Error(msg);
  }
  return data; // expects optional payload_hash
}

export async function applyProposal({
  proposalId,
  snapshotId,
  payloadHash,
  getAccessToken,
}) {
  const res = await fetch(`${API_BASE}/assistant/proposals/apply`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(getAccessToken),
    },
    body: JSON.stringify({
      proposal_id: proposalId,
      snapshot_id: snapshotId,
      confirm: true,
      payload_hash: payloadHash, // ok if undefined
    }),
  });

  const data = await safeJson(res);
  if (!res.ok) {
    const msg = data?.detail || `apply failed: ${res.status}`;
    throw new Error(msg);
  }
  return data; // expects new_snapshot_id or similar
}
