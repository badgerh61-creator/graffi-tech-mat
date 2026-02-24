// frontend/src/editor/gizmo/TransformGizmo.jsx
import { useMemo, useState } from "react";
import { buildTranslatePayload } from "./payloadBuilders";
import PivotControls from "../transform/PivotControls";

export default function TransformGizmo({
  enabled,
  reasonDisabled,
  activeTargetId,
  onCommit,
}) {
  const [snapEnabled, setSnapEnabled] = useState(true);
  const [snapStep, setSnapStep] = useState(0.25);

  // Tier 7.22/7.23 — pivot state (UI-only, shared controls)
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
      // context will be injected by controller (Tier 7.22)
    });

    onCommit?.({
      ...toolInvocation,
      __ui: { pivotMode, customPivot }, // UI metadata for controller (Tier 7.22/7.23)
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

      {/* Pivot Controls (shared) */}
      <div className="mt-3">
        <PivotControls
          pivotMode={pivotMode}
          setPivotMode={setPivotMode}
          customPivot={customPivot}
          setCustomPivot={setCustomPivot}
          disabled={!enabled}
        />
      </div>

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
