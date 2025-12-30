export default function AssetListItem({ asset }) {
  return (
    <div className="asset-list-item">
      <strong>{asset.name}</strong>
      <span style={{ marginLeft: 8 }}>({asset.type})</span>
    </div>
  );
}

