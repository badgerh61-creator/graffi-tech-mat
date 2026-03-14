import React from "react";
import { setSelectedId } from "../selection/selectionStore";
import { useConstraintViolations } from "./constraintViolationStore";

function extractTargetId(v) {
  if (v?.target_id) return String(v.target_id);
  if (v?.data?.target_id) return String(v.data.target_id);
  return null;
}

export default function ConstraintViolationsPanel({ violations: violationsProp }) {
  const storeState = useConstraintViolations?.();
  const violations =
    Array.isArray(violationsProp) ? violationsProp : storeState?.violations || [];

  if (!violations?.length) return null;

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold text-red-700">
        Constraint Violations
      </div>

      <div className="space-y-2">
        {violations.map((v, i) => {
          const targetId = extractTargetId(v);

          return (
            <div
              key={`${v?.constraint_id || "violation"}:${i}`}
              className="border rounded p-2 space-y-1"
            >
              <div className="flex items-center justify-between gap-2">
                <div className="text-sm font-semibold">
                  {v?.kind || "violation"}
                </div>

                {v?.constraint_id ? (
                  <div className="text-[11px] opacity-60 font-mono">
                    {v.constraint_id}
                  </div>
                ) : null}
              </div>

              <div className="text-xs opacity-80">
                {v?.message || "Constraint blocked this action."}
              </div>

              {targetId ? (
                <div className="flex items-center gap-2">
                  <div className="text-[11px] opacity-70 font-mono">
                    {targetId}
                  </div>
                  <button
                    className="border rounded px-2 py-1 text-xs"
                    onClick={() => setSelectedId(targetId)}
                  >
                    Select Target
                  </button>
                </div>
              ) : null}

              {v?.data ? (
                <pre className="text-[11px] opacity-75 overflow-auto mt-1 border rounded p-2">
{JSON.stringify(v.data, null, 2)}
                </pre>
              ) : null}
            </div>
          );
        })}
      </div>
    </div>
  );
}
