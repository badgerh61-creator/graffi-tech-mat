// frontend/src/editor/outliner/SceneOutlinerPanel.jsx
import React, { useMemo, useState } from "react";
import { setSelectedId } from "../selection/selectionStore";

const LAYER_OPTIONS = ["default", "garage", "hidden", "reference"];

function normalizeObjects(snapshot) {
  const objs = snapshot?.body_state?.objects || [];
  return [...objs].sort((a, b) => String(a?.id || "").localeCompare(String(b?.id || "")));
}

export default function SceneOutlinerPanel({
  snapshot,
  canEdit,
  onCommitTool,
}) {
  const [expandedId, setExpandedId] = useState(null);

  const objects = useMemo(() => normalizeObjects(snapshot), [snapshot]);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Scene Outliner</div>

      <div className="text-xs opacity-70">
        Objects: {objects.length}
      </div>

      {!objects.length ? (
        <div className="text-xs opacity-70">No scene objects.</div>
      ) : (
        <div className="space-y-2">
          {objects.map((obj) => {
            const expanded = expandedId === obj.id;
            const layers = Array.isArray(obj.layers) ? obj.layers : ["default"];

            return (
              <div key={obj.id} className="border rounded p-2 space-y-2">
                <div className="flex items-center gap-2">
                  <button
                    className="border rounded px-2 py-1 text-xs"
                    onClick={() => setExpandedId(expanded ? null : obj.id)}
                  >
                    {expanded ? "−" : "+"}
                  </button>

                  <button
                    className="text-left flex-1"
                    onClick={() => setSelectedId(obj.id)}
                    title="Select object"
                  >
                    <div className="text-sm font-semibold">{obj.name || obj.id}</div>
                    <div className="text-[11px] opacity-60 font-mono">
                      {obj.id} · {obj.kind || "object"}
                    </div>
                  </button>

                  <label className="text-xs flex items-center gap-1">
                    <input
                      type="checkbox"
                      aria-label="visible"
                      checked={!!obj.enabled}
                      disabled={!canEdit}
                      onChange={(e) =>
                        onCommitTool?.({
                          tool: "SCENE_SET_OBJECT_ENABLED",
                          station: "geometry",
                          payload: {
                            object_id: obj.id,
                            enabled: e.target.checked,
                          },
                        })
                      }
                    />
                    visible
                  </label>

                  <button
                    className="border rounded px-2 py-1 text-xs"
                    disabled={!canEdit}
                    onClick={() =>
                      onCommitTool?.({
                        tool: "SCENE_REMOVE_OBJECT",
                        station: "geometry",
                        payload: { object_id: obj.id },
                      })
                    }
                  >
                    Remove
                  </button>
                </div>

                {expanded ? (
                  <div className="border rounded p-2 space-y-2">
                    <div className="text-xs opacity-70">Layers</div>

                    <div className="flex flex-wrap gap-2">
                      {LAYER_OPTIONS.map((layer) => {
                        const checked = layers.includes(layer);
                        return (
                          <label key={layer} className="text-xs flex items-center gap-1">
                            <input
                              type="checkbox"
                              checked={checked}
                              disabled={!canEdit}
                              onChange={(e) => {
                                const next = e.target.checked
                                  ? [...new Set([...layers, layer])]
                                  : layers.filter((x) => x !== layer);

                                onCommitTool?.({
                                  tool: "SCENE_SET_OBJECT_LAYERS",
                                  station: "geometry",
                                  payload: {
                                    object_id: obj.id,
                                    layers: next.length ? next : ["default"],
                                  },
                                });
                              }}
                            />
                            {layer}
                          </label>
                        );
                      })}
                    </div>
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}



