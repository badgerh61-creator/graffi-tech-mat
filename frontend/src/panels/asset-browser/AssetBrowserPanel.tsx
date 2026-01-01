// frontend/src/panels/asset-browser/AssetBrowserPanel.tsx

import { useEffect, useState } from "react";
import AssetListItem from "./AssetListItem";
import { useCapability } from "../../capabilities/useCapabilities";
import { useAssetPreview } from "./useAssetPreview";
import { fetchAssets } from "../../services/assetService";
import type { EditorAsset } from "../../engine-bridge/AssetAdapter";

export default function AssetBrowserPanel() {
  const canView = useCapability("assets.view");
  const canUse = useCapability("assets.use");

  const { selectedAsset, setSelectedAsset } =
    useAssetPreview();

  const [assets, setAssets] =
    useState<EditorAsset[]>([]);
  const [loading, setLoading] =
    useState(false);
  const [error, setError] =
    useState<string | null>(null);

  /**
   * H1 — READ-ONLY asset ingestion
   */
  useEffect(() => {
    if (!canView) return;

    let alive = true;
    setLoading(true);
    setError(null);

    fetchAssets()
      .then((res) => {
        if (!alive) return;
        setAssets(res.items);
      })
      .catch((err) => {
        if (!alive) return;
        setError(
          err?.message ??
            "Failed to load assets"
        );
      })
      .finally(() => {
        if (!alive) return;
        setLoading(false);
      });

    return () => {
      alive = false;
    };
  }, [canView]);

  // 🚫 No access at all
  if (!canView) {
    return (
      <div className="asset-browser-panel asset-browser--disabled">
        <h3>Assets</h3>
        <p className="panel-disabled-reason">
          You do not have permission to view assets.
        </p>
      </div>
    );
  }

  return (
    <div
      className={`asset-browser-panel ${
        canUse ? "" : "asset-browser--read-only"
      }`}
    >
      <h3>Assets</h3>

      {!canUse && (
        <p className="panel-readonly-hint">
          View-only access. Asset modification
          is disabled.
        </p>
      )}

      {/* Loading */}
      {loading && (
        <p className="panel-loading">
          Loading assets…
        </p>
      )}

      {/* Error */}
      {!loading && error && (
        <p className="panel-error">
          {error}
        </p>
      )}

      {/* Empty */}
      {!loading &&
        !error &&
        assets.length === 0 && (
          <p className="panel-empty">
            No assets available.
          </p>
        )}

      {/* Asset list */}
      {!loading &&
        !error &&
        assets.map((asset) => {
          const isSelected =
            selectedAsset?.id === asset.id;

          return (
            <AssetListItem
              key={asset.id}
              asset={asset}
              disabled={!canUse}
              selected={isSelected}
              onClick={() => {
                // ✅ SELECTION ONLY (H1 COMPLIANT)
                setSelectedAsset(asset);
              }}
            />
          );
        })}
    </div>
  );
}

