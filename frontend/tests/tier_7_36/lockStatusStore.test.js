import { describe, it, expect } from "vitest";
import { lockStatusGetSnapshot, setLockStatus } from "../../src/editor/modes/lockStatusStore";

describe("lockStatusStore", () => {
  it("defaults to unknown", () => {
    expect(lockStatusGetSnapshot().lock.state).toBe("unknown");
  });

  it("sets lock status", () => {
    setLockStatus({ state: "owned" });
    expect(lockStatusGetSnapshot().lock.state).toBe("owned");
  });
});
