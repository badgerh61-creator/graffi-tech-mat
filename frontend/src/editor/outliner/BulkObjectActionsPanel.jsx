import React, { useMemo, useState } from "react";
import { useMultiSelection } from "../selection/multiSelectionStore";

const LAYER_OPTIONS = ["default", "garage", "hidden", "reference"];

function uniqueNonEmptyStrings(values) {
  const seen = new Set();
  const out = [];

  for (const raw of values || []) {
    const s = String(raw || "").trim();
    if (!s || seen.has(s)) continue;
    seen.add(s);
    out.push(s);
  }

  return out;
}

export default function BulkObjectActionsPanel({
  canEdit,
  onCommitTool,
}) {
  const selection = useMultiSelection() || {};
  const selectedIds = Array.isArray(selection.selectedIds)
    ? uniqueNonEmptyStrings(selection.selectedIds)
    : [];
  const primaryId = selection.primaryId ? String(selection.primaryId) : null;

  const [selectedLayers, setSelectedLayers] = useState(["default"]);

  const count = selectedIds.length;
  const canRunBulk = !!canEdit && count > 0;

  const normalizedLayers = useMemo(() => {
    const layers = uniqueNonEmptyStrings(selectedLayers);
    return layers.length ? layers : ["default"];
  }, [selectedLayers]);

  function commitEnabled(enabled) {
    if (!canRunBulk) return;

    onCommitTool?.({
      tool: "SCENE_BULK_SET_ENABLED",
      station: "geometry",
      payload: {
        object_ids: selectedIds,
        enabled: !!enabled,
      },
    });
  }

  function commitLayers() {
    if (!canRunBulk) return;

    onCommitTool?.({
      tool: "SCENE_BULK_SET_LAYERS",
      station: "geometry",
      payload: {
        object_ids: selectedIds,
        layers: normalizedLayers,
      },
    });
  }

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Bulk Actions</div>

      <div className="text-xs opacity-70">
        Primary: <span className="font-mono">{primaryId || "none"}</span>
      </div>

      <div className="text-xs opacity-70">
        Selected objects: {count}
      </div>

      <div className="flex items-center gap-2">
        <button
          type="button"
          className="border rounded px-3 py-2 text-sm"
          disabled={!canRunBulk}
          onClick={() => commitEnabled(true)}
        >
          Show Selected
        </button>

        <button
          type="button"
          className="border rounded px-3 py-2 text-sm"
          disabled={!canRunBulk}
          onClick={() => commitEnabled(false)}
        >
          Hide Selected
        </button>
      </div>

      <div className="border rounded p-2 space-y-2">
        <div className="text-xs opacity-70">Assign Layers</div>

        <div className="flex flex-wrap gap-2">
          {LAYER_OPTIONS.map((layer) => {
            const checked = normalizedLayers.includes(layer);

            return (
              <label key={layer} className="text-xs flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={(e) => {
                    const next = e.target.checked
                      ? [...normalizedLayers, layer]
                      : normalizedLayers.filter((x) => x !== layer);

                    const unique = uniqueNonEmptyStrings(next);
                    setSelectedLayers(unique.length ? unique : ["default"]);
                  }}
                />
                {layer}
              </label>
            );
          })}
        </div>

        <button
          type="button"
          className="border rounded px-3 py-2 text-sm"
          disabled={!canRunBulk}
          onClick={commitLayers}
        >
          Apply Layers To Selected
        </button>
      </div>

      <div className="text-[11px] opacity-60">
        Tier 7.60 bulk actions operate on object ids only.
      </div>
    </div>
  );
}
