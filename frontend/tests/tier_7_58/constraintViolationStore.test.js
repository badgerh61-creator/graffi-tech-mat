import { describe, it, expect } from "vitest";
import {
  setConstraintViolations,
  clearConstraintViolations,
  constraintViolationGetSnapshot,
} from "../../src/editor/constraints/constraintViolationStore";

describe("constraintViolationStore", () => {
  it("stores sorted violations", () => {
    setConstraintViolations([
      { constraint_id: "b", kind: "bounds", target_id: "obj-2", message: "B" },
      { constraint_id: "a", kind: "bounds", target_id: "obj-1", message: "A" },
    ]);

    const vs = constraintViolationGetSnapshot().violations;
    expect(vs[0].target_id).toBe("obj-1");
    expect(vs[1].target_id).toBe("obj-2");
  });

  it("clears violations", () => {
    clearConstraintViolations();
    expect(constraintViolationGetSnapshot().violations).toHaveLength(0);
  });
});
