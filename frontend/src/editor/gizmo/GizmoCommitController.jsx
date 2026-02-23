import { useMemo, useState } from "react";
import TransformGizmo from "./TransformGizmo";
import { newProposalId } from "../../services/studio/proposalId";
import {
  evaluateProposal,
  previewProposal,
  applyProposal,
} from "../../services/studio/assistantProposalsApi";
import { getAccessToken } from "../../utils/auth";

/**
 * Props:
 * - activeSnapshot: object (must include id, status)
 * - activeTargetId: string|null
 * - enabled: boolean
 * - reasonDisabled: string|null
 * - onApplied(newSnapshotId): callback
 * - enablePreview: boolean (safe default false if preview not present)
 */
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

  const effectiveEnabled = enabled && !busy;

  const statusLine = useMemo(() => {
    if (busy) return "Executing...";
    if (lastError) return `Error: ${lastError}`;
    if (lastDecision?.allowed === false) return `Blocked: ${lastDecision.reason || "rejected"}`;
    return null;
  }, [busy, lastError, lastDecision]);

  const handleCommit = async (toolInvocation) => {
    setLastError(null);
    setLastDecision(null);

    const snapshotId = activeSnapshot?.id;
    if (!snapshotId) {
      setLastError("No active snapshot");
      return;
    }
    if (!activeTargetId) {
      setLastError("No active target");
      return;
    }

    // proposal shape expected by backend
    const proposal = {
      station: toolInvocation.station,
      tool: toolInvocation.tool,
      payload: toolInvocation.payload,
    };

    setBusy(true);
    try {
      // 1) Evaluate (kernel gate, read-only)
      const decision = await evaluateProposal({
        snapshotId,
        proposal,
        getAccessToken,
      });
      setLastDecision(decision);

      if (!decision.allowed) return;

      // 2) Preview (optional, non-blocking)
      let payloadHash = undefined;
      if (enablePreview) {
        try {
          const preview = await previewProposal({
            snapshotId,
            proposal,
            getAccessToken,
          });
          payloadHash = preview.payload_hash || preview.payloadHash;
        } catch (e) {
          // preview is optional
          console.warn("preview failed (non-blocking):", e);
        }
      }

      // 3) Apply (authoritative execution)
      const proposalId = newProposalId();
      const applied = await applyProposal({
        proposalId,
        snapshotId,
        payloadHash,
        getAccessToken,
      });

      const newSnapshotId =
        applied.new_snapshot_id || applied.newSnapshotId || applied.snapshot_id;

      if (!newSnapshotId) throw new Error("apply succeeded but no new snapshot id returned");

      onApplied?.(newSnapshotId);
    } catch (e) {
      setLastError(e?.message || String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-2">
      <TransformGizmo
        enabled={effectiveEnabled}
        reasonDisabled={reasonDisabled}
        activeTargetId={activeTargetId}
        onCommit={handleCommit}
      />

      {statusLine ? <div className="text-xs opacity-80">{statusLine}</div> : null}
    </div>
  );
}
