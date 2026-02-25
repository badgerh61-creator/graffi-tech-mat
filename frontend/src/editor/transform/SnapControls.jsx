import React from "react";

// frontend/src/editor/transform/SnapControls.jsx
export default function SnapControls({
  enabled,
  setEnabled,
  step,
  setStep,
  label = "Snap",
  stepLabel = "Step",
  stepMin = 0.0001,
  stepInputStep = 0.05,
  disabled,
}) {
  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">{label}</div>

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={!!enabled}
          onChange={(e) => setEnabled(e.target.checked)}
          disabled={disabled}
        />
        Enable snap
      </label>

      <div className="flex items-center gap-2">
        <span className="text-xs opacity-70">{stepLabel}</span>
        <input
          className="border rounded px-2 py-1 text-sm w-28"
          type="number"
          value={step}
          min={stepMin}
          step={stepInputStep}
          onChange={(e) => setStep(Number(e.target.value))}
          disabled={disabled || !enabled}
        />
      </div>

      <div className="text-xs opacity-70">
        Snap is explicit metadata; kernel may accept/reject.
      </div>
    </div>
  );
}
