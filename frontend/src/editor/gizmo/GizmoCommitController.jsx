// frontend/src/editor/gizmo/GizmoCommitController.jsx
import React, { useMemo, useState } from "react";
import TransformGizmo from "./TransformGizmo";

import { useSelection } from "../selection/selectionStore";
import { toolPreflightGuard } from "../tools/toolPreflightGuard";
import { executeTool } from "../../services/studio/toolExecutionAdapter";
import { buildGizmoContext } from "./buildGizmoContext";
import { validatePivot } from "../transform/validatePivot"; // ✅ Tier 7.23

// ✅ Tier 7.24
import { validateSnap } from "../transform/validateSnap";

export default function GizmoCommitController({
  activeSnapshot,
  activeTargetId,
  enabled,
  reasonDisabled,
  onApplied,
  enablePreview = false,
}) {
  const [busy, setBusy] = useState(false);
  const [lastDecision, setLastDecision] = useState(null);
  const [lastError, setLastError] = useState(null);

  const selection = useSelection();

  const preflight = toolPreflightGuard({
    selection,
    uiDisabled: !enabled,
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
      const ui = toolInvocation.__ui || {};
      const pivotMode = ui.pivotMode || "bbox_center";
      const customPivot = ui.customPivot || { x: 0, y: 0, z: 0 };

      // ✅ Tier 7.23: block invalid custom pivot before hitting kernel
      const pv = validatePivot(pivotMode, customPivot);
      if (!pv.ok) {
        setLastDecision({ allowed: false, reason: pv.reason });
        throw new Error(pv.reason);
      }

      // ✅ Tier 7.24: block invalid snap step before hitting kernel
      const { snapEnabled, snapStep } = ui || {};
      const sv = validateSnap(!!snapEnabled, Number(snapStep));
      if (!sv.ok) {
        setLastDecision({ allowed: false, reason: sv.reason });
        // important: stop here (no backend call)
        return;
      }

      const ctx = buildGizmoContext({
        selection,
        pivotMode,
        customPivot,
      });

      const payload = {
        ...(toolInvocation?.payload || {}),
        ...(ctx || {}),
      };

      const res = await executeTool({
        snapshotId,
        station: toolInvocation.station,
        tool: toolInvocation.tool,
        payload,
        mode: "proposals",
        enablePreview: !!enablePreview,
      });

      if (!res.ok) {
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
            : reasonDisabled ||
              (activeTargetId || activeTargetIdResolved ? null : "select a target")
        }
        activeTargetId={activeTargetIdResolved || activeTargetId || null}
        onCommit={handleCommit}
      />

      {statusLine ? <div className="text-xs opacity-80">{statusLine}</div> : null}
    </div>
  );
}
