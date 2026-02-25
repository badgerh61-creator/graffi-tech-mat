import React from "react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, fireEvent, screen, act } from "@testing-library/react";

import TransformToolPanel from "../../src/editor/transform/TransformToolPanel";
import {
  clearSelection,
  setSelectedId,
} from "../../src/editor/selection/selectionStore";

// ✅ Tier 7.12: mock the adapter so Tier 7.11 doesn't depend on network call count/endpoints
vi.mock("../../src/services/studio/toolExecutionAdapter", () => ({
  executeTool: vi.fn(async ({ payload }: any) => ({
    ok: true,
    data: { new_snapshot_id: 99, echoed_target_id: payload?.target_id },
  })),
}));

import { executeTool } from "../../src/services/studio/toolExecutionAdapter";

describe("tier_7_11 TransformToolPanel", () => {
  beforeEach(() => {
    clearSelection();

    // no longer required, but harmless if other tests rely on it
    localStorage.setItem("access_token", "TEST_TOKEN");

    // keep a fetch stub around in case some other import triggers it
    (globalThis as any).fetch = vi.fn();

    vi.clearAllMocks();
  });

  it("blocks execution when no selection", () => {
    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    const btn = screen.getByRole("button", { name: /blocked/i });

    expect(btn).toBeDisabled();
    expect(btn.textContent?.toLowerCase()).toContain("select");
  });

  it("enables execution when selection exists", () => {
    setSelectedId("panel-1");

    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    const btn = screen.getByRole("button", { name: /execute/i });

    expect(btn).not.toBeDisabled();
  });

  it("sends target_id from selection store", async () => {
    setSelectedId("panel-1");

    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    const btn = screen.getByRole("button", { name: /execute/i });

    await act(async () => {
      fireEvent.click(btn);
      await Promise.resolve(); // flush microtasks
    });

    // ✅ We assert adapter called once (stable even if adapter uses 2-3 fetches internally)
    expect(executeTool).toHaveBeenCalledTimes(1);

    const args = (executeTool as any).mock.calls[0][0];

    expect(args.snapshotId).toBe(10);
    expect(args.station).toBe("geometry");
    expect(args.tool).toBe("TRANSLATE");
    expect(args.payload.target_id).toBe("panel-1");
  });
});

