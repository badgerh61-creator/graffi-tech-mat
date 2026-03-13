// frontend/src/editor/materials/MaterialSlotInspectorPanel.jsx
import React, { useEffect, useMemo, useState } from "react";
import { useSelection } from "../selection/selectionStore";
import { useMaterialSlots } from "./materialSlotStore";
import { fetchMaterialPresets } from "../../services/studio/materialPresetsApi";

function slotKey(targetId, slotName) {
  return `${targetId}::slot:${slotName}`;
}

export default function MaterialSlotInspectorPanel({
  snapshot,
  canEdit,
  onCommitTool,
}) {
  const { selectedId } = useSelection();
  const { slotsByTarget } = useMaterialSlots();
  const [presets, setPresets] = useState([]);

  useEffect(() => {
    let alive = true;

    fetchMaterialPresets()
      .then((p) => {
        if (!alive) return;
        setPresets(Array.isArray(p) ? p : []);
      })
      .catch(() => {
        if (!alive) return;
        setPresets([]);
      });

    return () => {
      alive = false;
    };
  }, []);

  const targetId =
    selectedId && String(selectedId).includes("::") ? String(selectedId) : null;

  const slots = targetId ? slotsByTarget[targetId] || [] : [];
  const overrides = snapshot?.decor_state?.material_overrides || {};

  const [selectedSlotName, setSelectedSlotName] = useState("");

  useEffect(() => {
    setSelectedSlotName(slots?.[0]?.name || "");
  }, [targetId, slots]);

  const slotOverride = useMemo(() => {
    if (!targetId || !selectedSlotName) return null;
    return overrides[slotKey(targetId, selectedSlotName)] || null;
  }, [overrides, targetId, selectedSlotName]);

  const [preset, setPreset] = useState("matte_black");

  useEffect(() => {
    if (slotOverride?.preset) {
      setPreset(slotOverride.preset);
    }
  }, [slotOverride?.preset]);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Material Slots</div>

      <div className="text-xs opacity-70">
        Target: <span className="font-mono">{targetId || "select a mesh"}</span>
      </div>

      {!targetId ? (
        <div className="text-xs opacity-70">
          Pick a mesh target to inspect its material slots.
        </div>
      ) : !slots.length ? (
        <div className="text-xs opacity-70">
          No slots discovered for this mesh.
        </div>
      ) : (
        <>
          <select
            className="border rounded px-2 py-1 text-sm w-full"
            value={selectedSlotName}
            onChange={(e) => setSelectedSlotName(e.target.value)}
          >
            {slots.map((slot) => (
              <option key={`${slot.name}:${slot.index}`} value={slot.name}>
                {slot.name} (#{slot.index})
              </option>
            ))}
          </select>

          <div className="text-xs opacity-70">
            Effective slot override:{" "}
            {slotOverride?.preset ? (
              <span className="font-mono">{slotOverride.preset}</span>
            ) : (
              "none"
            )}
          </div>

          <select
            className="border rounded px-2 py-1 text-sm w-full"
            value={preset}
            onChange={(e) => setPreset(e.target.value)}
            disabled={!selectedSlotName}
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
              disabled={!canEdit || !targetId || !selectedSlotName}
              onClick={() =>
                onCommitTool?.({
                  tool: "MATERIAL_SET_SLOT_PRESET",
                  station: "decor",
                  payload: {
                    target_id: targetId,
                    slot_name: selectedSlotName,
                    preset,
                  },
                })
              }
            >
              Apply Slot Preset
            </button>

            <button
              className="border rounded px-3 py-2 text-sm"
              disabled={!canEdit || !targetId || !selectedSlotName}
              onClick={() =>
                onCommitTool?.({
                  tool: "MATERIAL_CLEAR_SLOT_OVERRIDE",
                  station: "decor",
                  payload: {
                    target_id: targetId,
                    slot_name: selectedSlotName,
                  },
                })
              }
            >
              Clear Slot Override
            </button>
          </div>
        </>
      )}

      <div className="text-[11px] opacity-60">
        Slot override precedence: slot &gt; mesh &gt; object &gt; model default.
      </div>
    </div>
  );
}
