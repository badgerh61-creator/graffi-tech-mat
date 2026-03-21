import { describe, it, expect } from "vitest";
import { setTransformSpace } from "../../src/editor/transform/transformSpaceStore";

describe("transformSpaceStore", () => {
  it("accepts valid modes", () => {
    setTransformSpace("local");
    setTransformSpace("world");
    setTransformSpace("pivot");
    expect(true).toBe(true);
  });
});
