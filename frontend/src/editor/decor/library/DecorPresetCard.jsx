export function DecorPresetCard({ preset }) {
  return (
    <div className="decor-preset-card">
      <h4>{preset.name}</h4>
      <p>{preset.culture_pack}</p>
      <small>v{preset.version}</small>
    </div>
  );
}

