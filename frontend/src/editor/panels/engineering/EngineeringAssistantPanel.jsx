import { API_BASE } from "../../../config/apiBase";

import { useEffect, useState } from "react";
import { getAccessToken } from "../../../utils/auth";

export default function EngineeringAssistantPanel() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const projectId = 1;

  useEffect(() => {
    if (!projectId) return;

    const token = getAccessToken?.();
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    setLoading(true);
    setError(null);

    fetch(`${API_BASE}/tuning/read/${projectId}`, { headers })
      .then((res) => {
        if (res.status === 401) {
          throw new Error("Sign in required.");
        }
        if (!res.ok) {
          throw new Error(`Failed to fetch tuning context (${res.status})`);
        }
        return res.json();
      })
      .then((data) => {
        const result = {
          powerToWeight:
            data.weight && data.power ? (data.power / data.weight).toFixed(3) : "N/A",
          notes: "Read-only analysis. No mutation permitted.",
        };
        setAnalysis(result);
      })
      .catch((err) => {
        console.error("Assistant analysis failed", err);
        setAnalysis(null);
        setError(String(err?.message || err));
      })
      .finally(() => {
        setLoading(false);
      });
  }, [projectId]);

  return (
    <div style={{ padding: 12 }}>
      <h3>Engineering Assistant</h3>

      {loading && <p>Analyzing tuning context…</p>}

      {!loading && error && (
        <p style={{ fontSize: 12, color: "#b00020" }}>
          {error}
        </p>
      )}

      {!loading && !error && analysis && (
        <>
          <p>
            <strong>Power-to-Weight:</strong> {analysis.powerToWeight}
          </p>
          <p style={{ fontSize: 12, opacity: 0.7 }}>{analysis.notes}</p>
        </>
      )}

      {!loading && !error && !analysis && <p>No data available.</p>}
    </div>
  );
}
