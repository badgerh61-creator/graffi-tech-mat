import { API_BASE } from "../../config/apiBase";

import { getAccessToken } from "../../utils/auth";

export async function resolveSelectionRemote({ hitCandidates, modifiers, previousSelection }) {
  const token = getAccessToken();
  const res = await fetch(`${API_BASE}/selection/resolve`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      hit_candidates: hitCandidates,
      modifiers,
      previous_selection: previousSelection,
    }),
  });

  if (!res.ok) throw new Error(`selection resolve failed: ${res.status}`);
  return await res.json();
}
