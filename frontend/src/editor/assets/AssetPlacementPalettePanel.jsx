import React, { useEffect, useMemo, useState } from "react";
import { fetchModelAssets } from "../../services/studio/modelAssetsApi";
import {
  useAssetPalette,
  setActiveAssetId,
  toggleFavoriteAsset,
  pushRecentAsset,
} from "./assetPaletteStore";
import {
  filterAssets,
  listCategories,
} from "./assetPaletteFilters";

export default function AssetPlacementPalettePanel({
  canEdit,
  onCommitTool,
}) {
  const [assets, setAssets] = useState([]);
  const [err, setErr] = useState(null);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [mode, setMode] = useState("all");

  const { activeAssetId, favorites, recent } = useAssetPalette();

  useEffect(() => {
    let alive = true;
    fetchModelAssets()
      .then((a) => alive && setAssets(a))
      .catch((e) => alive && setErr(e?.message || String(e)));
    return () => {
      alive = false;
    };
  }, []);

  const categories = useMemo(() => listCategories(assets), [assets]);

  const filtered = useMemo(() => {
    return filterAssets({
      assets,
      query,
      category,
      favorites,
      mode,
      recent,
    });
  }, [assets, query, category, favorites, mode, recent]);

  const activeAsset = useMemo(
    () =>
      filtered.find((a) => String(a.id) === String(activeAssetId)) ||
      assets.find((a) => String(a.id) === String(activeAssetId)) ||
      null,
    [filtered, assets, activeAssetId]
  );

  return (
    <div className="border rounded p-3 space-y-3">
      <div className="text-sm font-semibold">Asset Placement Palette</div>

      {err ? <div className="text-xs">Error: {err}</div> : null}

      <div className="grid grid-cols-3 gap-2">
        <select
          className="border rounded px-2 py-1 text-sm"
          value={mode}
          onChange={(e) => setMode(e.target.value)}
        >
          <option value="all">All</option>
          <option value="favorites">Favorites</option>
          <option value="recent">Recent</option>
        </select>

        <select
          className="border rounded px-2 py-1 text-sm"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <input
          className="border rounded px-2 py-1 text-sm"
          placeholder="Search assets..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      <div className="text-xs opacity-70">
        Active asset: <span className="font-mono">{activeAsset?.id || "none"}</span>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {filtered.map((asset) => {
          const fav = favorites.includes(String(asset.id));
          const active = String(activeAssetId) === String(asset.id);

          return (
            <div
              key={asset.id}
              className={`border rounded p-2 space-y-2 ${active ? "bg-gray-50" : ""}`}
            >
              <button
                className="text-left w-full"
                onClick={() => setActiveAssetId(asset.id)}
              >
                <div className="text-sm font-semibold">{asset.name || asset.id}</div>
                <div className="text-xs opacity-70 font-mono">{asset.id}</div>
                <div className="text-xs opacity-70">
                  {asset.category || "uncategorized"} · {asset.kind || "asset"}
                </div>
                <div className="text-xs opacity-60">
                  {(asset.tags || []).join(", ")}
                </div>
              </button>

              <div className="flex items-center gap-2">
                <button
                  className="border rounded px-2 py-1 text-xs"
                  onClick={() => toggleFavoriteAsset(asset.id)}
                >
                  {fav ? "★ Favorite" : "☆ Favorite"}
                </button>

                <button
                  className="border rounded px-2 py-1 text-xs"
                  disabled={!canEdit}
                  onClick={() => {
                    pushRecentAsset(asset.id);
                    onCommitTool?.({
                      tool: "SCENE_ADD_MODEL_REF",
                      station: "geometry",
                      payload: {
                        asset_id: asset.id,
                        name: asset.name || asset.id,
                        transform: {
                          pos: { x: 0, y: 0, z: 0 },
                          rot: { x: 0, y: 0, z: 0 },
                          scale: { x: 1, y: 1, z: 1 },
                        },
                      },
                    });
                  }}
                >
                  Place
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {!filtered.length ? (
        <div className="text-xs opacity-70">No assets match current filters.</div>
      ) : null}

      <div className="text-[11px] opacity-60">
        Favorites and recent are UI-only. Placement is governed through SCENE_ADD_MODEL_REF.
      </div>
    </div>
  );
}
