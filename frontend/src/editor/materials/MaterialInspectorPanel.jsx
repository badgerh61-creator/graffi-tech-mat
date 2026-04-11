// src/editor/materials/MaterialInspectorPanel.jsx
import React from "react";
import { useEffect, useMemo, useState } from "react";
import { useSelection } from "../selection/selectionStore";
import { fetchMaterialPresets } from "../../services/studio/materialPresetsApi";

export default function MaterialInspectorPanel({
  snapshot,
  canEdit,
  onCommitTool,
}) {
  const { selectedId } = useSelection();
  const [presets, setPresets] = useState([]);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let alive = true;
    fetchMaterialPresets()
      .then((p) => alive && setPresets(p))
      .catch((e) => alive && setErr(e?.message || String(e)));
    return () => {
      alive = false;
    };
  }, []);

  const overrides = snapshot?.decor_state?.material_overrides || {};

  const effective = useMemo(() => {
    if (!selectedId) return null;

    const tid = String(selectedId);
    const parts = tid.split("::");
    const obj = parts[0];

    return overrides[tid] || overrides[obj] || null;
  }, [overrides, selectedId]);

  const [chosen, setChosen] = useState("matte_black");

  useEffect(() => {
    if (effective?.preset) setChosen(effective.preset);
  }, [effective?.preset]);

  const commit = onCommitTool || null;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Materials</div>

      <div className="text-xs opacity-70">
        Target: <span className="font-mono">{selectedId || "none"}</span>
      </div>

      {err ? <div className="text-xs">Preset load error: {err}</div> : null}

      <div className="text-xs opacity-70">
        Effective override:{" "}
        {effective?.preset ? (
          <span className="font-mono">{effective.preset}</span>
        ) : (
          "none"
        )}
      </div>

      <select
        className="border rounded px-2 py-1 text-sm w-full"
        value={chosen}
        onChange={(e) => setChosen(e.target.value)}
        disabled={!selectedId}
      >
        {presets.map((p) => (
          <option key={p.id} value={p.id}>
            {p.id}
          </option>
        ))}
      </select>

      <div className="flex items-center gap-2">
        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !selectedId || !chosen}
          onClick={() =>
            commit?.({
              tool: "PAINT_APPLY_LIBRARY_PRESET",
              station: "decor",
              payload: {
                target_id: selectedId,
                preset: chosen,
              },
            })
          }
        >
          Apply Preset
        </button>

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !selectedId}
          onClick={() =>
            commit?.({
              tool: "MATERIAL_CLEAR_OVERRIDE",
              station: "decor",
              payload: { target_id: selectedId },
            })
          }
        >
          Clear Override
        </button>
      </div>

      <div className="text-[11px] opacity-60">
        Overrides are stored in decor_state.material_overrides. Mesh override
        beats object override.
      </div>
    </div>
  );
}
