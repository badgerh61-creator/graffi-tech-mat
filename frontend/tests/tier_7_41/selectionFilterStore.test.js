import { describe, it, expect } from "vitest";
import { selectionFilterGetSnapshot, setSelectionFilter } from "../../src/editor/selection/selectionFilterStore";

describe("selectionFilterStore", () => {
  it("clamps invalid values", () => {
    setSelectionFilter("nope");
    expect(selectionFilterGetSnapshot().filter).toBe("all");
  });
});
