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
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);

  useEffect(() => {
    if (!projectId) return;

    const token = getAccessToken();
    console.log("Snapshot auth token:", token);

    fetch(`http://127.0.0.1:8000/projects/${projectId}/snapshots/`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (res) => {
        if (!res.ok) {
          throw new Error(`Snapshot fetch failed: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log("Snapshots:", data);
        setSnapshots(data);
      })
      .catch((err) => {
        console.error("Snapshot fetch failed", err);
      });
  }, [projectId]);

  const latestSnapshot = snapshots.find(
    (s) => s.status === "completed"
  );

  console.log("Latest snapshot:", latestSnapshot);

  return (
    <CapabilityProvider role={user?.role ?? "viewer"}>
      <EditorShell
        headerRight={
          <SnapshotPreview snapshot={latestSnapshot} />
        }
      >
        <EditorLayoutHost />
      </EditorShell>
    </CapabilityProvider>
  );
}

