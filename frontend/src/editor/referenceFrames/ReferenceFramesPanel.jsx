import { useMemo, useState } from "react";
import { useReferenceFrames } from "./useReferenceFrames";

export default function ReferenceFramesPanel({ activeSnapshotId, disabled }) {
  const { data, err } = useReferenceFrames(activeSnapshotId);
  const [activePlaneId, setActivePlaneId] = useState(null);

  const planes = data?.planes ?? [];
  const defaultPlane = data?.defaults?.active_plane_id ?? "world_xy";
  const chosen = activePlaneId ?? defaultPlane;

  const chosenPlane = useMemo(
    () => planes.find((p) => p.id === chosen),
    [planes, chosen]
  );

  if (err) return <div>Reference frames error: {String(err.message || err)}</div>;
  if (!data) return <div>Loading reference frames…</div>;

  return (
    <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Reference Frames</div>

      <div style={{ marginBottom: 8, opacity: 0.85 }}>
        Axes: X / Y / Z (unit: m)
      </div>

      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <label>Active plane:</label>
        <select
          disabled={!!disabled}
          value={chosen}
          onChange={(e) => setActivePlaneId(e.target.value)}
        >
          {planes.map((p) => (
            <option key={p.id} value={p.id}>
              {p.label}
            </option>
          ))}
        </select>
      </div>

      {chosenPlane && (
        <div style={{ marginTop: 10, fontSize: 13, opacity: 0.9 }}>
          <div>Normal: [{chosenPlane.normal.join(", ")}]</div>
          <div>Origin: [{chosenPlane.origin.join(", ")}]</div>
          <div style={{ marginTop: 6, fontStyle: "italic" }}>
            (Tier 7.2 is read-only — snapping comes next.)
          </div>
        </div>
      )}
    </div>
  );
}
