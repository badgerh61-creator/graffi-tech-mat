import { useEffect, useMemo, useState } from "react";
import { fetchDecalAssets } from "../../services/studio/decalAssetsApi";
import { useActiveDecal } from "./activeDecalStore";

export default function DecalAssetBrowserPanel({ canEdit, onCommitTool }) {
  const { decalId } = useActiveDecal();
  const [assets, setAssets] = useState([]);
  const [q, setQ] = useState("");
  const [err, setErr] = useState(null);

  useEffect(() => {
    let alive = true;
    fetchDecalAssets()
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
      <div className="text-sm font-semibold">Decal Assets</div>

      <div className="text-xs opacity-70">
        Active decal: <span className="font-mono">{decalId || "none"}</span>
      </div>

      <input
        className="border rounded px-2 py-1 text-sm w-full"
        placeholder="Search decals..."
        value={q}
        onChange={(e) => setQ(e.target.value)}
      />

      {err ? <div className="text-xs">Error: {err}</div> : null}

      <div className="grid grid-cols-2 gap-2">
        {filtered.map((a) => (
          <button
            key={a.id}
            className="border rounded p-2 text-left"
            disabled={!canEdit || !decalId}
            onClick={() =>
              onCommitTool?.({
                tool: "DECAL_SET_ASSET",
                station: "decor",
                payload: { decal_id: decalId, asset_id: a.id },
              })
            }
            title={!decalId ? "Select a decal first" : ""}
          >
            <div className="text-sm font-semibold">{a.name || a.id}</div>
            <div className="text-xs opacity-70 font-mono">{a.id}</div>
            <div className="text-xs opacity-70">{(a.tags || []).join(", ")}</div>
            <div className="text-xs opacity-50 mt-1">Assign to active decal</div>
          </button>
        ))}
      </div>

      <div className="text-[11px] opacity-60">
        Read-only registry. Upload comes later.
      </div>
    </div>
  );
}
