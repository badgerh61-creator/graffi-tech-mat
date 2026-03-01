import { describe, it, expect } from "vitest";
import { activeDecalGetSnapshot, setActiveDecalId, clearActiveDecalId } from "../../src/editor/decals/activeDecalStore";

describe("activeDecalStore", () => {
  it("sets and clears active decal id", () => {
    setActiveDecalId("dec-1");
    expect(activeDecalGetSnapshot().decalId).toBe("dec-1");
    clearActiveDecalId();
    expect(activeDecalGetSnapshot().decalId).toBe(null);
  });
});
