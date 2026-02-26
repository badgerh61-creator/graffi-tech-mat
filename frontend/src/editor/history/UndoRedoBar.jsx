import { useState } from "react";
import { redoSnapshot, undoSnapshot } from "../../services/studio/historyApi";

export default function UndoRedoBar({ projectId, activeSnapshotId, onNavigate }) {
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  async function doUndo() {
    if (!projectId || !activeSnapshotId) return;
    setErr(null);
    setBusy(true);
    try {
      const res = await undoSnapshot(projectId, activeSnapshotId);
      onNavigate?.(res.active_snapshot_id);
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  async function doRedo() {
    if (!projectId || !activeSnapshotId) return;
    setErr(null);
    setBusy(true);
    try {
      const res = await redoSnapshot(projectId, activeSnapshotId);
      onNavigate?.(res.active_snapshot_id);
    } catch (e) {
      setErr(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">History</div>
        <div className="text-xs opacity-70">
          {busy ? "Working…" : `Active: ${activeSnapshotId ?? "-"}`}
        </div>
      </div>

      {err ? <div className="text-xs text-red-600">{err}</div> : null}

      <div className="flex gap-2">
        <button className="border rounded px-3 py-2 text-sm" disabled={busy || !projectId || !activeSnapshotId} onClick={doUndo}>
          Undo
        </button>
        <button className="border rounded px-3 py-2 text-sm" disabled={busy || !projectId || !activeSnapshotId} onClick={doRedo}>
          Redo
        </button>
      </div>

      <div className="text-xs opacity-70">Undo/Redo navigates snapshot lineage only (read-only).</div>
    </div>
  );
}
