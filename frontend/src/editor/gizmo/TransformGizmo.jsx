import { useMemo, useState } from "react";
import { buildTranslatePayload } from "./payloadBuilders";

/**
 * Tier 7.7 — UI-only gizmo stub.
 * No rendering engine dependency yet.
 *
 * Props:
 * - enabled: boolean
 * - reasonDisabled?: string
 * - activeTargetId?: string|null
 * - onCommit(payload): called on "commit" action (authoritative execution elsewhere)
 */
export default function TransformGizmo({
  enabled,
  reasonDisabled,
  activeTargetId,
  onCommit,
}) {
  const [snapEnabled, setSnapEnabled] = useState(true);
  const [snapStep, setSnapStep] = useState(0.25);

  const canShow = !!activeTargetId;

  const statusText = useMemo(() => {
    if (!canShow) return "No target selected";
    if (enabled) return `Gizmo enabled (snap ${snapEnabled ? "on" : "off"})`;
    return `Gizmo disabled: ${reasonDisabled || "blocked"}`;
  }, [canShow, enabled, reasonDisabled, snapEnabled]);

  if (!canShow) return null;

  // Minimal "commit" buttons instead of drag handles for now:
  const commitNudgeX = (sign) => {
    const toolInvocation = buildTranslatePayload({
      targetId: activeTargetId,
      axis: "x",
      rawDelta: { x: 0.1 * sign, y: 0, z: 0 },
      snap: { enabled: snapEnabled, step: snapStep },
    });
    onCommit?.(toolInvocation);
  };

  return (
    <div className="rounded-xl border p-3 text-sm">
      <div className="font-semibold">Transform Gizmo</div>
      <div className="opacity-80 mt-1">{statusText}</div>

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
        UI-only: emits payloads. Kernel execution is wired in Tier 7.8.
      </div>
    </div>
  );
}
