export default function SnappingControls({
  snap,
  setSnap,
  step,
  setStep,
  frameId,
  setFrameId,
  frames,
}) {
  return (
    <div style={{ padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Snapping</div>

      <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input type="checkbox" checked={snap} onChange={(e) => setSnap(e.target.checked)} />
        Enable snap
      </label>

      <div style={{ display: "flex", gap: 8, marginTop: 8, alignItems: "center" }}>
        <label>Step:</label>
        <input
          type="number"
          value={step}
          min="0.0001"
          step="0.01"
          onChange={(e) => setStep(Number(e.target.value))}
          style={{ width: 100 }}
        />
      </div>

      <div style={{ display: "flex", gap: 8, marginTop: 8, alignItems: "center" }}>
        <label>Frame:</label>
        <select value={frameId} onChange={(e) => setFrameId(e.target.value)}>
          {(frames ?? []).map((f) => (
            <option key={f.id} value={f.id}>
              {f.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
