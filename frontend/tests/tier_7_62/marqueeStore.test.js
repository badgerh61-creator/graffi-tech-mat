import { describe, it, expect } from "vitest";
import {
  startMarquee,
  updateMarquee,
  clearMarquee,
  marqueeGetSnapshot,
} from "../../src/editor/selection/marqueeStore";

describe("marqueeStore", () => {
  it("tracks drag lifecycle", () => {
    startMarquee({ x: 10, y: 10 });
    updateMarquee({ x: 20, y: 20 });

    const s = marqueeGetSnapshot();
    expect(s.active).toBe(true);
    expect(s.end.x).toBe(20);

    clearMarquee();
    expect(marqueeGetSnapshot().active).toBe(false);
  });
});
