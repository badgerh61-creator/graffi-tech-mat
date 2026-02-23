import { getAccessToken } from "../../utils/auth";

export async function resolveSelectionRemote({ hitCandidates, modifiers, previousSelection }) {
  const token = getAccessToken();
  const res = await fetch("http://127.0.0.1:8000/selection/resolve", {
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
