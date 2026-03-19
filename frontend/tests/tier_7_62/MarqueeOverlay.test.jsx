import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render } from "@testing-library/react";
import MarqueeOverlay from "../../src/editor/selection/MarqueeOverlay";

// ✅ Stable snapshot (IMPORTANT — prevents infinite re-render)
const SNAPSHOT = {
  active: true,
  start: { x: 10, y: 10 },
  end: { x: 50, y: 50 },
};

// ✅ Mock marquee store
vi.mock("../../src/editor/selection/marqueeStore", () => {
  return {
    marqueeSubscribe: () => () => {}, // no-op unsubscribe
    marqueeGetSnapshot: () => SNAPSHOT,
  };
});

describe("MarqueeOverlay", () => {
  it("renders rectangle", () => {
    const { container } = render(<MarqueeOverlay />);

    const div = container.firstChild;

    expect(div).toBeTruthy();

    // width = 50 - 10
    expect(div.style.width).toBe("40px");

    // height = 50 - 10
    expect(div.style.height).toBe("40px");

    expect(div.style.left).toBe("10px");
    expect(div.style.top).toBe("10px");
  });
});
