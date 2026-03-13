import { describe, it, expect } from "vitest";
import {
  setMaterialSlotsForTarget,
  materialSlotGetSnapshot,
  clearMaterialSlots,
} from "../../src/editor/materials/materialSlotStore";

describe("materialSlotStore", () => {
  it("stores slots by target", () => {
    setMaterialSlotsForTarget("obj-1::MeshA", [{ name: "BodyPaint", index: 0 }]);
    expect(materialSlotGetSnapshot().slotsByTarget["obj-1::MeshA"][0].name).toBe("BodyPaint");
  });

  it("clears slots", () => {
    clearMaterialSlots();
    expect(Object.keys(materialSlotGetSnapshot().slotsByTarget)).toHaveLength(0);
  });
});
