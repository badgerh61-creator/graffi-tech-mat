import React, { useEffect, useMemo, useState } from "react";
import { fetchModelAssets } from "../../services/studio/modelAssetsApi";

export default function ModelAssetPickerPanel({ canEdit, onCommitTool }) {
  const [assets, setAssets] = useState([]);
  const [q, setQ] = useState("");
  const [err, setErr] = useState(null);

  useEffect(() => {
    let alive = true;
    fetchModelAssets()
      .then((a) => alive && setAssets(a))
      .catch((e) => alive && setErr(e?.message || String(e)));
    return () => { alive = false; };
  }, []);

  const filtered = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return assets;
    return assets.filter((a) =>
      String(a.id).toLowerCase().includes(s) ||
      String(a.name || "").toLowerCase().includes(s) ||
      (a.tags || []).join(" ").toLowerCase().includes(s)
    );
  }, [assets, q]);

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Model Assets</div>

      <input
        className="border rounded px-2 py-1 text-sm w-full"
        placeholder="Search models..."
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />

      {err ? <div className="text-xs">Error: {err}</div> : null}

      <div className="grid grid-cols-2 gap-2">
        {filtered.map((a) => (
          <button
            key={a.id}
            className="border rounded p-2 text-left"
            disabled={!canEdit}
            onClick={() =>
              onCommitTool?.({
                tool: "SCENE_ADD_MODEL_REF",
                station: "geometry",
                payload: {
                  asset_id: a.id,
                  name: a.name || a.id,
                  transform: {
                    pos: { x: 0, y: 0, z: 0 },
                    rot: { x: 0, y: 0, z: 0 },
                    scale: { x: 1, y: 1, z: 1 },
                  },
                },
              })
            }
          >
            <div className="text-sm font-semibold">{a.name || a.id}</div>
            <div className="text-xs opacity-70 font-mono">{a.id}</div>
            <div className="text-xs opacity-70">{(a.tags || []).join(", ")}</div>
            <div className="text-xs opacity-50 mt-1">Add to scene</div>
          </button>
        ))}
      </div>
    </div>
  );
}
