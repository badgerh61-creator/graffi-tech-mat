import { useState } from "react";
import SnapshotPlaceholder from "./SnapshotPlaceholder";
import SnapshotStatusBadge from "./SnapshotStatusBadge";
import SnapshotModal from "./SnapshotModal";

export default function SnapshotImage({ snapshot }) {
  const [open, setOpen] = useState(false);

  if (!snapshot) {
    return <SnapshotPlaceholder />;
  }

  const isCompleted = snapshot.status === "completed";

  return (
    <>
      <div
        style={{
          position: "relative",
          cursor: isCompleted ? "pointer" : "default",
        }}
        onClick={() => {
          if (isCompleted) setOpen(true);
        }}
      >
        {isCompleted ? (
          <img
            src={snapshot.image_url}
            alt="Rendered snapshot"
            style={{
              width: "100%",
              aspectRatio: "1 / 1",
              objectFit: "cover",
              borderRadius: 6,
            }}
          />
        ) : (
          <SnapshotPlaceholder />
        )}

        <SnapshotStatusBadge status={snapshot.status} />
      </div>

      {open && (
        <SnapshotModal
          imageUrl={snapshot.image_url}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  );
}

