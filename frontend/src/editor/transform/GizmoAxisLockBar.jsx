export default function GizmoAxisLockBar({ axisLock, setAxisLock }) {
  const options = [
    { id: "x", label: "X" },
    { id: "y", label: "Y" },
    { id: "z", label: "Z" },
    { id: "xy", label: "XY" },
    { id: "xz", label: "XZ" },
    { id: "yz", label: "YZ" },
    { id: "xyz", label: "XYZ" },
  ];

  return (
    <div style={{ display: "flex", gap: 8, padding: 10, border: "1px solid #ddd", borderRadius: 8 }}>
      <div style={{ fontWeight: 600 }}>Axis Lock:</div>
      {options.map((o) => (
        <button
          key={o.id}
          onClick={() => setAxisLock(o.id)}
          style={{
            padding: "6px 10px",
            borderRadius: 8,
            border: "1px solid #ccc",
            background: axisLock === o.id ? "#eee" : "#fff",
            cursor: "pointer",
          }}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}
