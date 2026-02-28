import React, { useMemo, useState } from "react";
import { getAccessToken } from "../../utils/auth";
import {
  startEdit,
  completeDraft,
  discardDraft,
} from "../../services/studio/draftWorkspaceApi";

export default function StudioModeBar({ activeSnapshot, onSetActiveSnapshotId }) {
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  // Tier 7.35 truth: mode derives ONLY from snapshot status
  const mode = useMemo(() => {
    if (!activeSnapshot) return "read";
    return activeSnapshot.status === "draft" ? "edit" : "read";
  }, [activeSnapshot]);

  // Tier 7.35 gates: ONLY snapshot status (lock gating is Tier 7.36 elsewhere)
  const canEnterEdit = !!activeSnapshot && mode === "read";
  const canComplete = !!activeSnapshot && mode === "edit";
  const canDiscard = !!activeSnapshot && mode === "edit";

  async function doStartEdit() {
    if (!activeSnapshot?.id) return;
    setBusy(true);
    setErr(null);
    try {
      const res = await startEdit({
        snapshotId: activeSnapshot.id,
        getAccessToken,
      });
      onSetActiveSnapshotId?.(res.draft_snapshot_id);
    } catch (e) {
      setErr(e?.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  async function doComplete() {
    if (!activeSnapshot?.id) return;
    setBusy(true);
    setErr(null);
    try {
      const res = await completeDraft({
        snapshotId: activeSnapshot.id,
        getAccessToken,
      });
      onSetActiveSnapshotId?.(res.completed_snapshot_id);
    } catch (e) {
      setErr(e?.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  async function doDiscard() {
    if (!activeSnapshot?.id) return;
    setBusy(true);
    setErr(null);
    try {
      const res = await discardDraft({
        snapshotId: activeSnapshot.id,
        getAccessToken,
      });
      onSetActiveSnapshotId?.(res.parent_snapshot_id);
    } catch (e) {
      setErr(e?.message || String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-2 flex items-center gap-2">
      <div className="text-sm font-semibold">
        Mode:{" "}
        <span className="opacity-90">{mode === "edit" ? "EDIT (DRAFT)" : "READ"}</span>
      </div>

      <div className="flex-1" />

      <button
        className="border rounded px-3 py-1 text-sm"
        disabled={!canEnterEdit || busy}
        onClick={doStartEdit}
        title={!canEnterEdit ? "Only completed snapshots can enter edit" : ""}
      >
        {busy ? "..." : "Enter Edit"}
      </button>

      <button
        className="border rounded px-3 py-1 text-sm"
        disabled={!canComplete || busy}
        onClick={doComplete}
      >
        Complete Draft
      </button>

      <button
        className="border rounded px-3 py-1 text-sm"
        disabled={!canDiscard || busy}
        onClick={doDiscard}
      >
        Discard Draft
      </button>

      {err ? <div className="text-xs opacity-80 ml-2">Error: {err}</div> : null}
    </div>
  );
}
