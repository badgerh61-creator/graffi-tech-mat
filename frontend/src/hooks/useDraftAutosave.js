import { API_BASE } from "../config/apiBase";

import { useEffect } from "react";
import { getAccessToken } from "../utils/auth";

export function useDraftAutosave({
  snapshot,
  sceneStateHash,
  isDirty,
  onSaved,
}) {
  useEffect(() => {
    if (!snapshot || snapshot.status !== "draft") return;
    if (!isDirty) return;

    const token = getAccessToken();

    const id = setInterval(() => {
      fetch(
        `${API_BASE}/snapshots/${snapshot.id}/autosave`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            scene_state_hash: sceneStateHash,
          }),
        }
      )
        .then((res) => {
          if (!res.ok) throw new Error("Autosave failed");
          onSaved();
        })
        .catch(console.error);
    }, 5000);

    return () => clearInterval(id);
  }, [snapshot, sceneStateHash, isDirty, onSaved]);
}

