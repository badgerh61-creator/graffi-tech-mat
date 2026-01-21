export default function DraftStatusBadge({ snapshot }) {
  if (!snapshot) return null;

  if (snapshot.status === "draft") {
    return (
      <span style={{ color: "#b58900", fontWeight: 600 }}>
        ● Draft (autosaving)
      </span>
    );
  }

  return (
    <span style={{ color: "#777" }}>
      🔒 Completed
    </span>
  );
}

