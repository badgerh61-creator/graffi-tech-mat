// frontend/src/editor/modes/EditSessionHeader.jsx
import React from "react";

function lockLabel(lockStatus) {
  const s = lockStatus?.state || "unknown";
  if (s === "owned") return "LOCK: OWNED";
  if (s === "taken") return "LOCK: TAKEN";
  if (s === "missing") return "LOCK: MISSING";
  return "LOCK: UNKNOWN";
}

function modeLabel(snapshot) {
  if (!snapshot) return "READ";
  return snapshot.status === "draft" ? "EDIT (DRAFT)" : "READ";
}

/**
 * Tier 7.36 — EditSessionHeader
 *
 * Test tokens must appear as their own text nodes:
 * - NOT_DRAFT
 * - NO_LOCK
 */
export default function EditSessionHeader({
  project,
  activeSnapshot,
  lockStatus,
  loading = false,
  canEditByRole = true,
  canEditByStation = true,
}) {
  const reasons = [];

  const hasSnapshot = !!activeSnapshot?.id;
  const isDraft = activeSnapshot?.status === "draft";
  const hasLockOwned = lockStatus?.state === "owned";

  if (!hasSnapshot) reasons.push("NO_SNAPSHOT");

  // Only evaluate draft-ness if a snapshot exists
  if (hasSnapshot && !isDraft) reasons.push("NOT_DRAFT");

  // Only require lock when draft exists
  if (isDraft && !hasLockOwned) reasons.push("NO_LOCK");

  if (!canEditByRole) reasons.push("ROLE_FORBIDDEN");
  if (!canEditByStation) reasons.push("WRONG_STATION");

  // Only show LOADING when we actually have a snapshot we’re loading around
  if (hasSnapshot && loading) reasons.push("LOADING");

  const blocked = reasons.length > 0;

  return (
    <div className="border rounded p-2 flex items-center gap-2">
      <div className="text-sm font-semibold">
        {project?.name ? project.name : "Project"}
      </div>

      <div className="text-xs opacity-75">
        Snapshot:{" "}
        <span className="font-mono">
          {activeSnapshot?.id != null ? String(activeSnapshot.id) : "none"}
        </span>
      </div>

      <div className="text-xs opacity-75">
        Mode: <span className="font-semibold">{modeLabel(activeSnapshot)}</span>
      </div>

      <div className="text-xs opacity-75">
        {lockLabel(lockStatus)}
        {lockStatus?.owner_id != null ? (
          <span className="ml-1 font-mono">({lockStatus.owner_id})</span>
        ) : null}
      </div>

      <div className="flex-1" />

      <div className="text-xs">
        <span className={blocked ? "text-red-600" : "text-green-700"}>
          {blocked ? "BLOCKED" : "READY"}
        </span>
      </div>

      {/* ✅ IMPORTANT: each reason is its own text node so tests can find it */}
      {reasons.length ? (
        <div className="text-xs opacity-80 ml-2 flex items-center gap-1">
          <span>Reasons:</span>
          {reasons.map((r) => (
            <span key={r} className="font-mono">
              {r}
            </span>
          ))}
        </div>
      ) : null}
    </div>
  );
}
