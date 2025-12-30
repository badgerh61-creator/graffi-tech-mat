import AssetListItem from "./AssetListItem";

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
  return (
    <div className="asset-browser-panel">
      <h3>Assets</h3>

      {MOCK_ASSETS.map((asset) => (
        <AssetListItem key={asset.id} asset={asset} />
      ))}
    </div>
  );
}

