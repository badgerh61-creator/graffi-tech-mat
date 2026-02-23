import { useState } from "react";
import { useToolExecute } from "./useToolExecute";

export default function TransformToolbar({
  activeSnapshot,
  isEditable,
  selectedId,
  station = "geometry",
  onNewSnapshot,
}) {
  const { execute } = useToolExecute();

  // ✅ Tier 7.3 snapping controls (UI-only)
  const [snapEnabled, setSnapEnabled] = useState(false);
  const [snapStep, setSnapStep] = useState(0.25);
  const [frameId, setFrameId] = useState("world_xy"); // must be known by backend registry

  async function run(tool) {
    if (!isEditable) return;
    if (!activeSnapshot?.id) return;
    if (!selectedId) return;

    const payload = {
      target_id: selectedId,

      // existing params (unchanged)
      params:
        tool === "TRANSLATE"
          ? { x: 10, y: 0, z: 0 }
          : tool === "ROTATE"
          ? { axis: "y", degrees: 5 }
          : { factor: 1.05 },

      // ✅ Tier 7.3 additions (top-level in payload)
      snap: snapEnabled,
      snap_step: snapStep,
      frame_id: frameId,
    };

    const result = await execute({
      snapshotId: activeSnapshot.id,
      station,
      tool,
      payload,
    });

    onNewSnapshot?.(result.new_snapshot_id);
  }

  return (
    <div style={{ display: "flex", gap: 12, alignItems: "center", flexWrap: "wrap" }}>
      <button disabled={!isEditable || !selectedId} onClick={() => run("TRANSLATE")}>
        Move
      </button>
      <button disabled={!isEditable || !selectedId} onClick={() => run("ROTATE")}>
        Rotate
      </button>
      <button disabled={!isEditable || !selectedId} onClick={() => run("SCALE")}>
        Scale
      </button>

      {/* ✅ Tier 7.3 snapping UI */}
      <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
        <input
          type="checkbox"
          checked={snapEnabled}
          onChange={(e) => setSnapEnabled(e.target.checked)}
          disabled={!isEditable}
        />
        Snap
      </label>

      <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
        Step
        <input
          type="number"
          min="0.0001"
          step="0.05"
          value={snapStep}
          onChange={(e) => setSnapStep(Number(e.target.value))}
          disabled={!isEditable || !snapEnabled}
          style={{ width: 90 }}
        />
      </label>

      <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
        Frame
        <select
          value={frameId}
          onChange={(e) => setFrameId(e.target.value)}
          disabled={!isEditable || !snapEnabled}
        >
          <option value="world_xy">World XY</option>
          <option value="world_yz">World YZ</option>
          <option value="world_xz">World XZ</option>
        </select>
      </label>

      {!selectedId && (
        <span style={{ opacity: 0.7 }}>Select a target to enable tools</span>
      )}
    </div>
  );
}
