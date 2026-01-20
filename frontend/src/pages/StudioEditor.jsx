// frontend/src/pages/StudioEditor.jsx

import { useEffect, useState } from "react";

import EditorShell from "../app/EditorShell";
import EditorLayoutHost from "../layout/EditorLayoutHost";
import { CapabilityProvider } from "../capabilities";
import { getCurrentUser, getAccessToken } from "../utils/auth";
import SnapshotPreview from "../components/snapshots/SnapshotPreview";

export default function StudioEditor() {
  const user = getCurrentUser();

  // 🔧 TEMPORARY (Phase J): active project
  // Later comes from router / workspace context
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);

  // =====================================================
  // SNAPSHOT FETCH (REUSABLE)
  // =====================================================
  const fetchSnapshots = () => {
    const token = getAccessToken();

    return fetch(
      `http://127.0.0.1:8000/projects/${projectId}/snapshots/`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Snapshot fetch failed: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Snapshots:", data);
        setSnapshots(data);
      });
  };

  // =====================================================
  // INITIAL LOAD (READ-ONLY)
  // =====================================================
  useEffect(() => {
    if (!projectId) return;

    fetchSnapshots().catch((err) => {
      console.error("Snapshot fetch failed", err);
    });
  }, [projectId]);

  // =====================================================
  // PHASE 3 — SNAPSHOT SELECTION (MANDATORY)
  //
  // RULES:
  // - Draft snapshot wins
  // - Completed snapshot is fallback
  // - No implicit "latest"
  // =====================================================
  const draftSnapshot = snapshots.find(
    (s) => s.status === "draft"
  );

  const activeSnapshot = draftSnapshot ?? snapshots[0];

  const isEditable = activeSnapshot?.status === "draft";

  console.log("Active snapshot:", activeSnapshot);
  console.log("Is editable:", isEditable);

  // =====================================================
  // RENDER
  // =====================================================
  return (
    <CapabilityProvider role={user?.role ?? "viewer"}>
      <EditorShell
        headerRight={
          <SnapshotPreview
            snapshot={activeSnapshot}
            onDraftCreated={fetchSnapshots}
          />
        }
      >
        <EditorLayoutHost />
      </EditorShell>
    </CapabilityProvider>
  );
}

