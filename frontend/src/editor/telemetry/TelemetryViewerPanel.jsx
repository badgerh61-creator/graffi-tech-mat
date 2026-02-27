import React, { useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import {
  createSimulationJob,
  getTelemetryArtifact,
} from "../../services/simulationApi";
import { normalizeSeries, toPolylinePoints } from "./simpleChart";

export default function TelemetryViewerPanel({ activeSnapshot }) {
  const [busy, setBusy] = useState(false);
  const [artifact, setArtifact] = useState(null);
  const [err, setErr] = useState(null);

  async function run() {
    if (!activeSnapshot?.id) return;

    setBusy(true);
    setErr(null);

    try {
      const token = getAccessToken?.();

      const job = await createSimulationJob({
        snapshotId: activeSnapshot.id,
        scenario: { duration_s: 10, timestep_s: 0.1, throttle: 0.6 },
        engineVersion: "pseudo-v1",
        token,
      });

      const artifactId = job.artifact_id;

      const a = await getTelemetryArtifact({
        artifactId,
        token,
      });

      setArtifact(a);
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  const points = useMemo(() => {
    const c = artifact?.curves || {};
    return normalizeSeries(c.time_s, c.speed_mps);
  }, [artifact]);

  const poly = useMemo(() => {
    return toPolylinePoints(points, 360, 140);
  }, [points]);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Telemetry (6S.1)</div>
        <button
          className="border rounded px-3 py-1 text-sm"
          onClick={run}
          disabled={busy || !activeSnapshot?.id}
        >
          {busy ? "Running..." : "Run Sim"}
        </button>
      </div>

      {err ? (
        <div className="text-xs border rounded p-2">
          Error: {err}
        </div>
      ) : null}

      {!artifact ? (
        <div className="text-xs opacity-75">
          No artifact yet. Run a sim.
        </div>
      ) : (
        <div className="space-y-2">
          <div className="text-xs opacity-75">
            artifact #{artifact.artifact_id} • engine {artifact.engine_version}
          </div>

          <div className="border rounded p-2">
            <div className="text-xs font-semibold mb-1">
              Speed vs Time
            </div>
            <svg
              width="360"
              height="140"
              role="img"
              aria-label="speed-chart"
            >
              <polyline
                points={poly}
                fill="none"
                stroke="currentColor"
                strokeWidth="1"
              />
            </svg>
          </div>

          <div className="text-xs opacity-75">
            Samples: {artifact?.curves?.time_s?.length || 0}
          </div>
        </div>
      )}
    </div>
  );
}
