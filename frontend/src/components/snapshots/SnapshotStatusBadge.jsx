export default function SnapshotStatusBadge({ status }) {
  if (!status || status === "completed") return null;

  const styles = {
    pending: { color: "#999" },
    running: { color: "#4fa3ff" },
    failed: { color: "#ff5c5c" },
  };

  const labels = {
    pending: "Queued",
    running: "Rendering…",
    failed: "Render failed",
  };

  return (
    <div
      style={{
        position: "absolute",
        bottom: 6,
        right: 6,
        fontSize: 11,
        padding: "2px 6px",
        borderRadius: 4,
        background: "#111",
        ...styles[status],
      }}
    >
      {labels[status]}
    </div>
  );
}

