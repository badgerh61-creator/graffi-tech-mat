import React, { useState } from "react";

export default function EndurancePresetButton({ onApply }) {
  const [duration, setDuration] = useState(600);
  const [timestep, setTimestep] = useState(1);

  function apply() {
    onApply?.({
      engine_version: "pseudo-endurance-v1",
      scenario: {
        duration_s: Number(duration),
        timestep_s: Number(timestep),
        throttle: 0.65,
        gear_ratio: 9.0,
        mass_kg: 1200.0,
        thermal_ceiling_c: 130.0,
        degradation_rate: 0.0008,
      },
    });
  }

  return (
    <div className="border rounded p-2 space-y-2">
      <div className="text-xs font-semibold">Endurance Preset (6S.8)</div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        <label>
          Duration (s)
          <input
            className="border rounded w-full px-2 py-1"
            type="number"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
          />
        </label>

        <label>
          Timestep (s)
          <input
            className="border rounded w-full px-2 py-1"
            type="number"
            value={timestep}
            onChange={(e) => setTimestep(e.target.value)}
          />
        </label>
      </div>

      <div className="text-[11px] opacity-70">
        Warning: duration/timestep controls sample count. Keep it reasonable for UI.
      </div>

      <button className="border rounded px-3 py-1 text-sm" onClick={apply}>
        Use Endurance Settings
      </button>
    </div>
  );
}
