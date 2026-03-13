import React from "react";
import {
  useDecalPlacement,
  setDecalPlacement,
  resetDecalPlacement,
} from "./decalPlacementStore";

export default function DecalPlacementPanel() {
  const { placement } = useDecalPlacement();

  return (
    <div className="border rounded p-3 space-y-2">
      <h3 className="text-sm font-semibold">Decal Placement</h3>

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={!!placement.enabled}
          onChange={(e) => setDecalPlacement({ enabled: e.target.checked })}
        />
        <span>Placement Mode</span>
      </label>

      <label className="text-sm flex items-center justify-between gap-2">
        <span>Asset ID</span>
        <input
          className="border rounded px-2 py-1 flex-1"
          value={placement.asset_id || ""}
          onChange={(e) => setDecalPlacement({ asset_id: e.target.value || null })}
          placeholder="asset-flame"
        />
      </label>

      <label className="text-sm flex items-center justify-between gap-2">
        <span>Size</span>
        <input
          className="border rounded px-2 py-1 w-28"
          type="number"
          step="0.05"
          value={placement.size}
          onChange={(e) => setDecalPlacement({ size: Number(e.target.value || 1) })}
        />
      </label>

      <label className="text-sm flex items-center justify-between gap-2">
        <span>Rotation °</span>
        <input
          className="border rounded px-2 py-1 w-28"
          type="number"
          step="1"
          value={placement.rotation_deg}
          onChange={(e) => setDecalPlacement({ rotation_deg: Number(e.target.value || 0) })}
        />
      </label>

      <label className="text-sm flex items-center justify-between gap-2">
        <span>Opacity</span>
        <input
          className="border rounded px-2 py-1 w-28"
          type="number"
          step="0.05"
          value={placement.opacity}
          onChange={(e) => setDecalPlacement({ opacity: Number(e.target.value || 1) })}
        />
      </label>

      <label className="text-sm flex items-center justify-between gap-2">
        <span>Blend</span>
        <select
          className="border rounded px-2 py-1"
          value={placement.blend}
          onChange={(e) => setDecalPlacement({ blend: e.target.value })}
        >
          <option value="normal">normal</option>
          <option value="multiply">multiply</option>
          <option value="add">add</option>
        </select>
      </label>

      <label className="text-sm flex items-center justify-between gap-2">
        <span>Z offset</span>
        <input
          className="border rounded px-2 py-1 w-28"
          type="number"
          step="0.0005"
          value={placement.z_offset}
          onChange={(e) => setDecalPlacement({ z_offset: Number(e.target.value || 0.001) })}
        />
      </label>

      <button
        className="border rounded px-3 py-2 text-sm"
        onClick={() => resetDecalPlacement()}
      >
        Reset Placement Tool
      </button>

      <div className="text-[11px] opacity-60">
        Hover a mesh, preview appears. Click to commit one decal.
      </div>
    </div>
  );
}
