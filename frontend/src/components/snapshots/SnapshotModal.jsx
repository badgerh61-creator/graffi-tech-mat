export default function SnapshotModal({ imageUrl, onClose }) {
  if (!imageUrl) return null;

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.8)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 9999,
        cursor: "zoom-out",
      }}
    >
      <img
        src={imageUrl}
        alt="Snapshot preview"
        style={{
          maxWidth: "90%",
          maxHeight: "90%",
          borderRadius: 8,
          boxShadow: "0 0 40px rgba(0,0,0,0.6)",
        }}
      />
    </div>
  );
}

