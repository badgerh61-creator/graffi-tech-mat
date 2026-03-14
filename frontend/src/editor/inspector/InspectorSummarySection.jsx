import React from "react";

export default function InspectorSummarySection({
  selectedId,
  activeDecalId,
  selectionKind,
  activeSnapshot,
  toolsEnabled,
  lockState,
}) {
  const target = activeDecalId
    ? `decal:${activeDecalId}`
    : (selectedId || "none");

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Summary</div>

      <div className="text-xs opacity-70">
        Target: <span className="font-mono">{target}</span>
      </div>

      <div className="text-xs opacity-70">
        Kind: <span className="font-mono">{selectionKind}</span>
      </div>

      <div className="text-xs opacity-70">
        Snapshot:{" "}
        <span className="font-mono">
          {activeSnapshot?.id ?? "—"} ({String(activeSnapshot?.status ?? "—")})
        </span>
      </div>

      <div className="text-xs opacity-70">
        Edit: <span className="font-mono">{toolsEnabled ? "enabled" : "blocked"}</span>
      </div>

      <div className="text-xs opacity-70">
        Lock: <span className="font-mono">{lockState || "unknown"}</span>
      </div>
    </div>
  );
}
