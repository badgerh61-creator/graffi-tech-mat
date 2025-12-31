import AssetListItem from "./AssetListItem";
import { useCapability } from "../../capabilities/useCapabilities";

const MOCK_ASSETS = [
  {
    id: "asset-1",
    name: "Placeholder Image",
    type: "image",
  },
  {
    id: "asset-2",
    name: "Placeholder Model",
    type: "model",
  },
];

export default function AssetBrowserPanel() {
  const canView = useCapability("assets.view");
  const canUse = useCapability("assets.use");

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
          View-only access. Asset modification is disabled.
        </p>
      )}

      {MOCK_ASSETS.map((asset) => (
        <AssetListItem
          key={asset.id}
          asset={asset}
          disabled={!canUse}
        />
      ))}
    </div>
  );
}

