// frontend/src/components/snapshots/SnapshotPreview.jsx

export default function SnapshotPreview({ snapshot }) {
  if (!snapshot) {
    return (
      <div
        style={{
          fontSize: 12,
          opacity: 0.6,
          padding: "0 8px",
        }}
      >
        No preview
      </div>
    );
  }

  return (
    <img
      src={snapshot.image_url}
      alt="Project snapshot"
      style={{
        width: 48,
        height: 48,
        objectFit: "cover",
        borderRadius: 6,
        border: "1px solid #ccc",
      }}
    />
  );
}

