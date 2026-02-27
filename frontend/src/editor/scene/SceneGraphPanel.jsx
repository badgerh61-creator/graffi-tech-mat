// frontend/src/editor/scene/SceneGraphPanel.jsx
import React from "react";
import { useMemo, useState, useEffect } from "react";
import { useMeshIndex } from "./meshIndexStore";
import { setSelectedId, clearSelection, useSelection } from "../selection/selectionStore";

function stableSortObjects(objects) {
  const arr = Array.isArray(objects) ? objects.slice() : [];
  return arr
    .filter(Boolean)
    .sort((a, b) => {
      const ak = String(a.kind || "");
      const bk = String(b.kind || "");
      if (ak !== bk) return ak.localeCompare(bk);
      const ai = String(a.id || "");
      const bi = String(b.id || "");
      return ai.localeCompare(bi);
    });
}

export default function SceneGraphPanel({ sceneIndex }) {
  const { selectedId } = useSelection();
  const meshIndex = useMeshIndex();

  const objects = useMemo(
    () => stableSortObjects(sceneIndex?.objects || []),
    [sceneIndex]
  );

  const [open, setOpen] = useState({}); // objectId -> boolean

  // keep open map deterministic: default closed
  useEffect(() => {
    const next = {};
    for (const o of objects) {
      const oid = String(o.id || "");
      if (!oid) continue;
      next[oid] = open[oid] ?? false;
    }
    setOpen(next);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [objects.map((o) => String(o.id)).join("|")]);

  if (!sceneIndex) {
    return (
      <div className="border rounded p-3 text-sm opacity-75">
        Scene Graph (loading…)
      </div>
    );
  }

  if (!objects.length) {
    return (
      <div className="border rounded p-3 text-sm opacity-75">
        Scene Graph (no objects)
      </div>
    );
  }

  const selectedObjId = selectedId ? String(selectedId).split("::")[0] : null;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Scene Graph</div>

      <div className="space-y-2">
        {objects.map((o) => {
          const oid = String(o.id || "");
          const kind = String(o.kind || "unknown");
          const name = String(o.name || oid);

          const isObjSelected = selectedObjId === oid;

          const meshPaths = meshIndex.meshPathsByObjectId?.[oid] || [];
          const isOpen = !!open[oid];

          return (
            <div key={oid} className="border rounded p-2 space-y-2">
              <div className="flex items-center justify-between gap-2">
                <button
                  className="text-xs border rounded px-2 py-1"
                  onClick={() => setOpen((m) => ({ ...m, [oid]: !m[oid] }))}
                  title="Expand/collapse"
                >
                  {isOpen ? "▾" : "▸"}
                </button>

                <button
                  className={`flex-1 text-left text-sm border rounded px-2 py-1 ${
                    isObjSelected ? "font-semibold" : ""
                  }`}
                  onClick={() => setSelectedId(`${oid}::`)}
                  title="Select object"
                >
                  {kind}: {name}
                </button>

                <button
                  className="text-xs border rounded px-2 py-1"
                  onClick={() => clearSelection()}
                  title="Clear selection"
                >
                  Clear
                </button>
              </div>

              {isOpen ? (
                <div className="pl-6 space-y-1">
                  {meshPaths.length ? (
                    meshPaths.map((mp) => {
                      const meshSel = `${oid}::${mp}`;
                      const isMeshSelected = selectedId === meshSel;
                      return (
                        <button
                          key={mp}
                          className={`block w-full text-left text-xs border rounded px-2 py-1 ${
                            isMeshSelected ? "font-semibold" : ""
                          }`}
                          onClick={() => setSelectedId(meshSel)}
                          title="Select mesh"
                        >
                          {mp}
                        </button>
                      );
                    })
                  ) : (
                    <div className="text-xs opacity-70">
                      No mesh index yet (load GLB in viewport).
                    </div>
                  )}
                </div>
              ) : null}
            </div>
          );
        })}
      </div>

      <div className="text-xs opacity-70">
        UI-only. Ordering is deterministic (kind → id). Mesh list appears after GLB load.
      </div>
    </div>
  );
}
