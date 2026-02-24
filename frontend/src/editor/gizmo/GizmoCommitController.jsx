import React, { useMemo, useState } from "react";
import TransformGizmo from "./TransformGizmo";

// Tier 7.15: use typed selection + preflight + adapter
import { useSelection as useSelectionStore } from "../selection/selectionStore";
import { toolPreflightGuard } from "../tools/toolPreflightGuard";
import { executeTool } from "../../services/studio/toolExecutionAdapter";

/**
 * Props:
 * - activeSnapshot: object (must include id, status)
 * - activeTargetId: string|null   (legacy prop; kept additive-safe)
 * - enabled: boolean              (already gated by parent: draft/lock/role/station)
 * - reasonDisabled: string|null
 * - onApplied(newSnapshotId): callback
 * - enablePreview: boolean (optional; adapter handles non-blocking preview)
 */
export default function GizmoCommitController({
  activeSnapshot,
  activeTargetId, // legacy; kept, but typed selection is canonical now
  enabled,
  reasonDisabled,
  onApplied,
  enablePreview = false,
}) {
  const [busy, setBusy] = useState(false);
  const [lastDecision, setLastDecision] = useState(null);
  const [lastError, setLastError] = useState(null);

  // Canonical selection (Tier 7.13)
  const selection = useSelectionStore();

  // Preflight (Tier 7.14) — do not execute unless ok
  const preflight = toolPreflightGuard({
    selection,
    uiDisabled: !enabled, // parent already computed eligibility
    activeSnapshotId: activeSnapshot?.id,
  });

  const activeTargetIdResolved = preflight.ok ? preflight.target_id : null;

  const reasonText = !preflight.ok
    ? preflight.reason === "no_selection"
      ? "select a target"
      : preflight.reason === "no_snapshot"
      ? "no active snapshot"
      : "disabled"
    : null;

  const effectiveEnabled = enabled && !busy && preflight.ok;

  const statusLine = useMemo(() => {
    if (busy) return "Executing...";
    if (!preflight.ok) return `Blocked: ${reasonText || "blocked"}`;
    if (lastError) return `Error: ${lastError}`;
    if (lastDecision?.allowed === false)
      return `Blocked: ${lastDecision.reason || "rejected"}`;
    return null;
  }, [busy, preflight.ok, reasonText, lastError, lastDecision]);

  const handleCommit = async (toolInvocation) => {
    setLastError(null);
    setLastDecision(null);

    // Preflight first: never call backend if blocked
    if (!preflight.ok) {
      setLastError(reasonText || "blocked");
      return;
    }

    const snapshotId = activeSnapshot?.id;
    if (!snapshotId) {
      setLastError("no active snapshot");
      return;
    }

    setBusy(true);
    try {
      // Force canonical target_id from typed selection primary
      const payload = {
        ...(toolInvocation?.payload || {}),
        target_id: preflight.target_id,
      };

      const res = await executeTool({
        snapshotId,
        station: toolInvocation.station,
        tool: toolInvocation.tool,
        payload,
        mode: "proposals",        // ✅ canonical execution path
        enablePreview: !!enablePreview,
      });

      if (!res.ok) {
        // Keep decision if adapter surfaced it (optional)
        setLastDecision(res.data?.decision || null);
        throw new Error(res.error?.detail || res.error?.kind || "rejected");
      }

      const applied = res.data || {};
      const newSnapshotId =
        applied.new_snapshot_id || applied.newSnapshotId || applied.snapshot_id;

      if (!newSnapshotId)
        throw new Error("apply succeeded but no new snapshot id returned");

      onApplied?.(newSnapshotId);
    } catch (e) {
      setLastError(String(e?.message || e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-2">
      <TransformGizmo
        enabled={effectiveEnabled}
        reasonDisabled={
          !preflight.ok
            ? reasonText
            : reasonDisabled || (activeTargetId || activeTargetIdResolved ? null : "select a target")
        }
        activeTargetId={activeTargetIdResolved || activeTargetId || null}
        onCommit={handleCommit}
      />

      {statusLine ? <div className="text-xs opacity-80">{statusLine}</div> : null}
    </div>
  );
}
