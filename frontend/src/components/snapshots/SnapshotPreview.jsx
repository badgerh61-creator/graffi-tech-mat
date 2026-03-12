import { API_BASE } from "../../config/apiBase";

import { useState } from "react";
import { getAccessToken } from "../../utils/auth";

import SnapshotStatusBadge from "./SnapshotStatusBadge";
import SnapshotPlaceholder from "./SnapshotPlaceholder";
import SnapshotModal from "./SnapshotModal";

export default function SnapshotPreview({
  snapshot,
  onDraftCreated,
}) {
  const [open, setOpen] = useState(false);
  const [creatingDraft, setCreatingDraft] = useState(false);

  // ⏳ No snapshot yet
  if (!snapshot) {
    return (
      <div style={{ width: 48, height: 48 }}>
        <SnapshotPlaceholder />
      </div>
    );
  }

  const isCompleted = snapshot.status === "completed";
  const canCreateDraft = isCompleted;

  const handleCreateDraft = async () => {
    if (!canCreateDraft || creatingDraft) return;

    setCreatingDraft(true);

    try {
      const token = getAccessToken();

      const res = await fetch(
        `${API_BASE}/snapshots/${snapshot.id}/draft`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text);
      }

      onDraftCreated?.();
    } catch (err) {
      alert(`Failed to create draft: ${err.message}`);
    } finally {
      setCreatingDraft(false);
    }
  };

  return (
    <>
      <div
        style={{
          position: "relative",
          display: "flex",
          alignItems: "center",
          gap: 12,
        }}
      >
        {/* Snapshot thumbnail */}
        <div
          style={{
            position: "relative",
            width: 48,
            height: 48,
            cursor: isCompleted ? "pointer" : "default",
          }}
          onClick={() => {
            if (isCompleted) setOpen(true);
          }}
          title={
            isCompleted
              ? "Click to preview snapshot"
              : "Snapshot not ready"
          }
        >
          {isCompleted ? (
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
          ) : (
            <SnapshotPlaceholder />
          )}

          <SnapshotStatusBadge status={snapshot.status} />
        </div>

        {/* Create Draft action */}
        {canCreateDraft && (
          <button
            onClick={handleCreateDraft}
            disabled={creatingDraft}
            style={{ whiteSpace: "nowrap" }}
          >
            {creatingDraft ? "Creating…" : "Create Draft"}
          </button>
        )}
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

