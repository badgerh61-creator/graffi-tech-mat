import React, { useEffect, useState } from "react";

export default function VariantSetsPanel({
  snapshot,
  canEdit,
  onCommitTool,
}) {
  const variants = snapshot?.decor_state?.variant_sets || [];
  const [name, setName] = useState("New Variant");
  const [selectedId, setSelectedId] = useState(variants?.[0]?.id || "");

  useEffect(() => {
    setSelectedId(variants?.[0]?.id || "");
  }, [variants.length]);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Variant Sets</div>

      <div className="text-xs opacity-70">
        Save and restore appearance combinations (paint / decals / visibility).
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">Save Current State</div>

        <input
          className="border rounded px-2 py-1 text-sm w-full"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Variant name"
        />

        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !name.trim()}
          onClick={() =>
            onCommitTool?.({
              tool: "VARIANT_SAVE",
              station: "decor",
              payload: { name: name.trim() },
            })
          }
        >
          Save Variant
        </button>
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs font-semibold opacity-80">Existing Variants</div>

        <select
          className="border rounded px-2 py-1 text-sm w-full"
          value={selectedId}
          onChange={(e) => setSelectedId(e.target.value)}
        >
          <option value="">(select variant)</option>
          {variants.map((v) => (
            <option key={v.id} value={v.id}>
              {v.name} — {v.id}
            </option>
          ))}
        </select>

        <div className="flex items-center gap-2">
          <button
            className="border rounded px-3 py-2 text-sm"
            disabled={!canEdit || !selectedId}
            onClick={() =>
              onCommitTool?.({
                tool: "VARIANT_APPLY",
                station: "decor",
                payload: { variant_id: selectedId },
              })
            }
          >
            Apply Variant
          </button>

          <button
            className="border rounded px-3 py-2 text-sm"
            disabled={!canEdit || !selectedId}
            onClick={() =>
              onCommitTool?.({
                tool: "VARIANT_DELETE",
                station: "decor",
                payload: { variant_id: selectedId },
              })
            }
          >
            Delete Variant
          </button>
        </div>
      </div>

      <div className="text-[11px] opacity-60">
        Tier 7.56 captures material overrides, decals, and object visibility only.
      </div>
    </div>
  );
}
