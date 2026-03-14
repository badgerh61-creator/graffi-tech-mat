import React from "react";
import { useConstraintViolations } from "./constraintViolationStore";

export default function ConstraintBlockedBanner() {
  const { violations } = useConstraintViolations();

  if (!violations?.length) return null;

  return (
    <div className="border rounded p-2 flex items-center gap-2">
      <div className="text-sm font-semibold">Apply blocked</div>
      <div className="text-xs opacity-75">
        {violations.length} constraint{" "}
        {violations.length === 1 ? "violation" : "violations"} must be resolved.
      </div>
    </div>
  );
}
