import React from "react";

export default function PivotControls({
  pivotMode,
  setPivotMode,
  customPivot,
  setCustomPivot,
  disabled,
}) {
  const modeId = "pivot-mode-select";

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Pivot</div>

      <div className="flex items-center gap-2">
        <label className="text-xs opacity-70" htmlFor={modeId}>
          Mode
        </label>
        <select
          id={modeId}
          className="border rounded px-2 py-1 text-sm"
          value={pivotMode}
          onChange={(e) => setPivotMode(e.target.value)}
          disabled={disabled}
        >
          <option value="bbox_center">BBox Center</option>
          <option value="world_origin">World Origin</option>
          <option value="custom">Custom</option>
        </select>
      </div>

      {pivotMode === "custom" ? (
        <div className="grid grid-cols-3 gap-2">
          {["x", "y", "z"].map((k) => {
            const inputId = `pivot-${k}`;
            return (
              <div key={k} className="space-y-1">
                <label className="text-xs opacity-70" htmlFor={inputId}>
                  {k.toUpperCase()}
                </label>
                <input
                  id={inputId}
                  className="border rounded px-2 py-1 text-sm w-full"
                  type="number"
                  value={customPivot[k]}
                  onChange={(e) =>
                    setCustomPivot({ ...customPivot, [k]: Number(e.target.value) })
                  }
                  disabled={disabled}
                />
              </div>
            );
          })}
        </div>
      ) : null}

      <div className="text-xs opacity-70">
        Pivot is UI metadata; kernel remains authoritative.
      </div>
    </div>
  );
}
