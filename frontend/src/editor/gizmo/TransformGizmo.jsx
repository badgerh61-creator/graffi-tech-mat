import { useMemo, useState } from "react";
import { buildTranslatePayload } from "./payloadBuilders";

export default function TransformGizmo({
  enabled,
  reasonDisabled,
  activeTargetId,
  onCommit,
}) {
  const [snapEnabled, setSnapEnabled] = useState(true);
  const [snapStep, setSnapStep] = useState(0.25);

  // Tier 7.22 — pivot state (UI-only)
  const [pivotMode, setPivotMode] = useState("bbox_center");
  const [customPivot, setCustomPivot] = useState({ x: 0, y: 0, z: 0 });

  const canShow = !!activeTargetId;

  const statusText = useMemo(() => {
    if (!canShow) return "No target selected";
    if (enabled) return `Gizmo enabled (snap ${snapEnabled ? "on" : "off"})`;
    return `Gizmo disabled: ${reasonDisabled || "blocked"}`;
  }, [canShow, enabled, reasonDisabled, snapEnabled]);

  if (!canShow) return null;

  const commitNudgeX = (sign) => {
    const toolInvocation = buildTranslatePayload({
      targetId: activeTargetId,
      axis: "x",
      rawDelta: { x: 0.1 * sign, y: 0, z: 0 },
      snap: { enabled: snapEnabled, step: snapStep },
      // context will be injected by controller
    });

    onCommit?.({
      ...toolInvocation,
      __ui: { pivotMode, customPivot }, // UI metadata for controller
    });
  };

  return (
    <div className="rounded-xl border p-3 text-sm">
      <div className="font-semibold">Transform Gizmo</div>
      <div className="opacity-80 mt-1">{statusText}</div>

      {/* Snap Controls */}
      <div className="mt-2 flex items-center gap-2">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={snapEnabled}
            onChange={(e) => setSnapEnabled(e.target.checked)}
            disabled={!enabled}
          />
          Snap
        </label>

        <label className="flex items-center gap-2">
          <span>Step</span>
          <input
            type="number"
            value={snapStep}
            min={0}
            step={0.05}
            onChange={(e) => setSnapStep(parseFloat(e.target.value || "0"))}
            disabled={!enabled || !snapEnabled}
            className="border rounded px-2 py-1 w-24"
          />
        </label>
      </div>

      {/* Pivot Controls */}
      <div className="mt-3 flex items-center gap-2">
        <span className="text-xs opacity-70">Pivot</span>
        <select
          className="border rounded px-2 py-1 text-sm"
          value={pivotMode}
          onChange={(e) => setPivotMode(e.target.value)}
          disabled={!enabled}
        >
          <option value="bbox_center">BBox</option>
          <option value="world_origin">World</option>
          <option value="custom">Custom</option>
        </select>
      </div>

      {pivotMode === "custom" ? (
        <div className="mt-2 grid grid-cols-3 gap-2">
          {["x", "y", "z"].map((k) => (
            <input
              key={k}
              className="border rounded px-2 py-1 text-sm"
              type="number"
              value={customPivot[k]}
              onChange={(e) =>
                setCustomPivot({ ...customPivot, [k]: Number(e.target.value) })
              }
              disabled={!enabled}
            />
          ))}
        </div>
      ) : null}

      {/* Nudge */}
      <div className="mt-3 flex gap-2">
        <button
          className="border rounded px-3 py-1"
          onClick={() => commitNudgeX(-1)}
          disabled={!enabled}
        >
          Nudge -X
        </button>
        <button
          className="border rounded px-3 py-1"
          onClick={() => commitNudgeX(+1)}
          disabled={!enabled}
        >
          Nudge +X
        </button>
      </div>

      <div className="text-xs opacity-70 mt-2">
        UI-only: emits payloads. Kernel execution wired via controller.
      </div>
    </div>
  );
}
