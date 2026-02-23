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

  // ─────────────────────────────────────────
  // Tier 7.3 — Snapping state (UI-only)
  // ─────────────────────────────────────────
  const [snapEnabled, setSnapEnabled] = useState(false);
  const [snapStep, setSnapStep] = useState(0.25);
  const [frameId, setFrameId] = useState("world_xy");

  // ─────────────────────────────────────────
  // Tier 7.4 — Axis lock state (UI-only)
  // ─────────────────────────────────────────
  const [axisLock, setAxisLock] = useState("xyz"); // x|y|z|xy|xz|yz|xyz

  async function run(tool) {
    if (!isEditable) return;
    if (!activeSnapshot?.id) return;
    if (!selectedId) return;

    const baseParams =
      tool === "TRANSLATE"
        ? { x: 10, y: 0, z: 0 }
        : tool === "ROTATE"
        ? { axis: "y", degrees: 5 }
        : { factor: 1.05 };

    // IMPORTANT:
    // Because ToolExecutePayload only preserves target_id + params,
    // ALL transform metadata must live inside params.
    const payload = {
      target_id: selectedId,
      params: {
        ...baseParams,

        // Tier 7.3 — snapping
        snap: snapEnabled,
        snap_step: snapStep,
        frame_id: frameId,

        // Tier 7.4 — axis locks
        axis_lock: axisLock,
        drag_source: "gizmo",
      },
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
    <div
      style={{
        display: "flex",
        gap: 12,
        alignItems: "center",
        flexWrap: "wrap",
      }}
    >
      <button
        disabled={!isEditable || !selectedId}
        onClick={() => run("TRANSLATE")}
      >
        Move
      </button>

      <button
        disabled={!isEditable || !selectedId}
        onClick={() => run("ROTATE")}
      >
        Rotate
      </button>

      <button
        disabled={!isEditable || !selectedId}
        onClick={() => run("SCALE")}
      >
        Scale
      </button>

      {/* ───────────── Snapping UI (Tier 7.3) ───────────── */}
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

      {/* ───────────── Axis Lock UI (Tier 7.4) ───────────── */}
      <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
        Axis
        <select
          value={axisLock}
          onChange={(e) => setAxisLock(e.target.value)}
          disabled={!isEditable}
        >
          <option value="x">X</option>
          <option value="y">Y</option>
          <option value="z">Z</option>
          <option value="xy">XY</option>
          <option value="xz">XZ</option>
          <option value="yz">YZ</option>
          <option value="xyz">XYZ</option>
        </select>
      </label>

      {!selectedId && (
        <span style={{ opacity: 0.7 }}>
          Select a target to enable tools
        </span>
      )}
    </div>
  );
}
