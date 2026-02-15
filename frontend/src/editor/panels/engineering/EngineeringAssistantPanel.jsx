import { useEffect, useState } from "react";
import { getAccessToken } from "../../../utils/auth";

export default function EngineeringAssistantPanel() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  // For now we derive projectId from URL or hardcode safely.
  // Later this should come from workspace context.
  const projectId = 1;

  useEffect(() => {
    if (!projectId) return;

    const token = getAccessToken();
    setLoading(true);

    fetch(`http://127.0.0.1:8000/tuning/read/${projectId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch tuning context");
        }
        return res.json();
      })
      .then((data) => {
        const result = {
          powerToWeight:
            data.weight && data.power
              ? (data.power / data.weight).toFixed(3)
              : "N/A",
          notes: "Read-only analysis. No mutation permitted.",
        };

        setAnalysis(result);
      })
      .catch((err) => {
        console.error("Assistant analysis failed", err);
        setAnalysis(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [projectId]);

  return (
    <div style={{ padding: 12 }}>
      <h3>Engineering Assistant</h3>

      {loading && <p>Analyzing tuning context…</p>}

      {!loading && analysis && (
        <>
          <p>
            <strong>Power-to-Weight:</strong> {analysis.powerToWeight}
          </p>
          <p style={{ fontSize: 12, opacity: 0.7 }}>
            {analysis.notes}
          </p>
        </>
      )}

      {!loading && !analysis && <p>No data available.</p>}
    </div>
  );
}

