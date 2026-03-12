import { API_BASE } from "../config/apiBase";

import { API_BASE } from "../config/apiBase";

// frontend/src/studio/useStudioState.js

import { useEffect, useState } from "react";
import { getAccessToken } from "../utils/auth";

export function useStudioState(projectId) {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!projectId) return;

    const token = getAccessToken();

    fetch(`${API_BASE}/studio/state?project_id=${projectId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        if (!res.ok) {
          throw new Error(`Studio state fetch failed: ${res.status}`);
        }
        return res.json();
      })
      .then(setState)
      .catch(setError);
  }, [projectId]);

  return {
    state,
    error,
    isLoading: state === null && error === null,
  };
}

