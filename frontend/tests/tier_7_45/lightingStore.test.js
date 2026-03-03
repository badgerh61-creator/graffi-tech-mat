import { describe, it, expect } from "vitest";
import { lightingGetSnapshot, setLighting } from "../../src/editor/view/lightingStore";

describe("lightingStore", () => {
  it("updates exposure", () => {
    setLighting({ exposure: 1.7 });
    expect(lightingGetSnapshot().exposure).toBe(1.7);
  });
});
