import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import TransformToolPanel from "../../src/editor/transform/TransformToolPanel";

// Mock adapter so we can assert it is NOT called when blocked
const executeToolMock = vi.fn(async () => ({ ok: true, data: { new_snapshot_id: 1 } }));
vi.mock("../../src/services/studio/toolExecutionAdapter", () => ({
  executeTool: (...args) => executeToolMock(...args),
}));

// Mock selection store hook (component uses useSelection from selectionStore)
vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({
    primary: null,
    secondary: [],
    hovered: null,
    lastUpdatedAt: 0,
    selectedId: null,
  }),
}));

describe("tier_7_14 TransformToolPanel preflight", () => {
  beforeEach(() => {
    executeToolMock.mockClear();
  });

  it("blocks execute when no_selection", () => {
    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    const btn = screen.getByTestId("transform-execute");
    expect(btn.disabled).toBe(true);
    expect(btn.textContent.toLowerCase()).toContain("blocked");

    // ensure adapter not called
    expect(executeToolMock).not.toHaveBeenCalled();
  });
});
