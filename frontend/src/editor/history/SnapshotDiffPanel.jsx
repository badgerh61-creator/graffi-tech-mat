import { useMemo } from "react";
import { summarizeSnapshotDiff } from "./snapshotDiff";

function Row({ label, v }) {
  if (!v) return null;
  const text = v.mode
    ? `+${v.added}  -${v.removed}  ~${v.changed}   (${v.aCount}→${v.bCount})`
    : `+${v.added}  -${v.removed}  ~${v.changed}   (keys ${v.aKeys}→${v.bKeys})`;
  return (
    <div className="flex items-center justify-between border rounded px-2 py-1 text-xs">
      <div className="opacity-80">{label}</div>
      <div className="font-mono">{text}</div>
    </div>
  );
}

export default function SnapshotDiffPanel({ baseSnapshot, targetSnapshot }) {
  const diff = useMemo(
    () => summarizeSnapshotDiff(baseSnapshot, targetSnapshot),
    [baseSnapshot, targetSnapshot]
  );

  if (!targetSnapshot) {
    return <div className="border rounded p-3 text-sm opacity-75">Diff: no target snapshot</div>;
  }

  if (!baseSnapshot) {
    return (
      <div className="border rounded p-3 space-y-2">
        <div className="text-sm font-semibold">Snapshot Diff</div>
        <div className="text-xs opacity-75">No base snapshot (no parent selected).</div>
      </div>
    );
  }

  if (!diff) {
    return <div className="border rounded p-3 text-sm opacity-75">Diff unavailable</div>;
  }

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="flex items-center justify-between">
        <div className="text-sm font-semibold">Snapshot Diff</div>
        <div className="text-xs opacity-70">
          {diff.base_id} → {diff.target_id}
        </div>
      </div>

      {diff.meta.statusChanged ? (
        <div className="text-xs border rounded p-2">
          <div className="font-semibold">Status changed</div>
          <div className="opacity-80">
            {String(diff.meta.fromStatus)} → {String(diff.meta.toStatus)}
          </div>
        </div>
      ) : (
        <div className="text-xs opacity-70">Status unchanged</div>
      )}

      <div className="text-xs font-semibold mt-2">Body</div>
      <div className="space-y-1">
        <Row label="panels" v={diff.body.panels} />
        <Row label="nodes" v={diff.body.nodes} />
        <Row label="curves" v={diff.body.curves} />
        <Row label="surfaces" v={diff.body.surfaces} />
      </div>

      <div className="text-xs font-semibold mt-2">Decor / Tuning</div>
      <div className="space-y-1">
        <Row label="decor_state keys" v={diff.decor} />
        <Row label="tuning_state keys" v={diff.tuning} />
      </div>

      <div className="text-[11px] opacity-60 mt-2">
        Diff is UI-only and deterministic. No snapshot writes.
      </div>
    </div>
  );
}
