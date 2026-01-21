// frontend/src/pages/StudioEditor.jsx

import { useEffect, useState, useCallback } from "react";

import EditorShell from "../app/EditorShell";
import EditorLayoutHost from "../layout/EditorLayoutHost";
import { CapabilityProvider } from "../capabilities";
import { getCurrentUser, getAccessToken } from "../utils/auth";

import SnapshotPreview from "../components/snapshots/SnapshotPreview";
import DraftStatusBadge from "../components/snapshots/DraftStatusBadge";
import FinalizeDraftButton from "../components/snapshots/FinalizeDraftButton";
import { useDraftAutosave } from "../hooks/useDraftAutosave";

export default function StudioEditor() {
  const user = getCurrentUser();

  // 🔧 TEMPORARY (Phase J)
  const projectId = 1;

  const [snapshots, setSnapshots] = useState([]);
  const [sceneStateHash, setSceneStateHash] = useState("__working__");

  // ===============================
  // DIRTY STATE (EDITOR-LOCAL)
  // ===============================
  const [isDirty, setIsDirty] = useState(false);

  // =====================================================
  // SNAPSHOT FETCH (AUTHORITATIVE)
  // =====================================================
  const fetchSnapshots = useCallback(() => {
    const token = getAccessToken();

    return fetch(
      `http://127.0.0.1:8000/projects/${projectId}/snapshots/`,
      {
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
  }, [projectId]);

  // =====================================================
  // INITIAL LOAD
  // =====================================================
  useEffect(() => {
    if (!projectId) return;
    fetchSnapshots().catch(console.error);
  }, [projectId, fetchSnapshots]);

  // =====================================================
  // PHASE 3 — SNAPSHOT SELECTION (MANDATORY)
  // =====================================================
  const draftSnapshot = snapshots.find((s) => s.status === "draft");
  const completedSnapshot = snapshots.find(
    (s) => s.status === "completed"
  );

  const activeSnapshot = draftSnapshot ?? completedSnapshot;
  const isEditable = activeSnapshot?.status === "draft";

  // =====================================================
  // PHASE 4.4 — AUTOSAVE (DRAFT ONLY)
  // =====================================================
  useDraftAutosave({
    snapshot: activeSnapshot,
    sceneStateHash,
    isDirty,
    onSaved: () => setIsDirty(false),
  });

  // =====================================================
  // RENDER
  // =====================================================
  return (
    <CapabilityProvider role={user?.role ?? "viewer"}>
      <EditorShell
        headerRight={
          <>
            <DraftStatusBadge snapshot={activeSnapshot} />

            {/* ===============================
                UI INDICATOR (HEADER)
               =============================== */}
            {isDirty && (
              <span
                style={{
                  color: "#d33682",
                  marginLeft: 8,
                  fontSize: 12,
                }}
              >
                Unsaved changes
              </span>
            )}

            <SnapshotPreview
              snapshot={activeSnapshot}
              onDraftCreated={fetchSnapshots}
            />

            <FinalizeDraftButton
              snapshot={activeSnapshot}
              onFinalized={fetchSnapshots}
            />
          </>
        }
      >
        {/* ===============================
            SCENE CHANGE SIGNAL
           =============================== */}
        <EditorLayoutHost
          editable={isEditable}
          onSceneChange={() => {
            if (!isEditable) return;
            setSceneStateHash(Date.now().toString());
            setIsDirty(true);
          }}
        />
      </EditorShell>
    </CapabilityProvider>
  );
}

