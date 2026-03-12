import { API_BASE } from "../../config/apiBase";

import { getAccessToken } from "../../utils/auth";

export default function FinalizeDraftButton({ snapshot, onFinalized }) {
  if (!snapshot || snapshot.status !== "draft") return null;

  const finalize = async () => {
    if (!confirm("Finalize this draft? Editing will lock.")) return;

    const token = getAccessToken();

    const res = await fetch(
      `${API_BASE}/snapshots/${snapshot.id}/finalize`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!res.ok) {
      alert("Finalize failed");
      return;
    }

    onFinalized();
  };

  return (
    <button onClick={finalize}>
      Finalize Design
    </button>
  );
}

