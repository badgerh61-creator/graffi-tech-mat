export default function SceneIndexPanel({ sceneIndex, snapshotId }) {
  if (!snapshotId)
    return <div className="text-sm opacity-70">No snapshot selected.</div>;

  if (!sceneIndex)
    return <div className="text-sm opacity-70">Loading scene…</div>;

  return (
    <div className="border rounded p-3 text-sm space-y-2">
      <div className="font-semibold">Scene Objects</div>
      {sceneIndex.objects?.map((o) => (
        <div key={o.id} className="opacity-80">
          {o.kind}: {o.id} {o.asset_ref ? `(${o.asset_ref})` : "(no asset)"}
        </div>
      ))}
    </div>
  );
}
