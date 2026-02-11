export function MaterialCard({ material }) {
  return (
    <div className="material-card">
      <h4>{material.name}</h4>
      <p>{material.category}</p>
      <small>v{material.version}</small>
    </div>
  );
}

