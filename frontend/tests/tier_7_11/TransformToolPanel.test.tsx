import React from "react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, fireEvent, screen, act } from "@testing-library/react";

import TransformToolPanel from "../../src/editor/transform/TransformToolPanel";
import {
  clearSelection,
  setSelectedId,
} from "../../src/editor/selection/selectionStore";

describe("tier_7_11 TransformToolPanel", () => {
  beforeEach(() => {
    clearSelection();

    // Ensure getAccessToken() returns something
    localStorage.setItem("access_token", "TEST_TOKEN");

    (globalThis as any).fetch = vi.fn();
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

    (globalThis as any).fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ new_snapshot_id: 99 }),
    });

    render(<TransformToolPanel activeSnapshot={{ id: 10 }} disabled={false} />);

    const btn = screen.getByRole("button", { name: /execute/i });

    await act(async () => {
      fireEvent.click(btn);
      await Promise.resolve(); // flush microtasks
    });

    expect((globalThis as any).fetch).toHaveBeenCalledTimes(1);

    const [url, opts] = (globalThis as any).fetch.mock.calls[0];

    expect(String(url)).toContain("/tools/execute");

    const body = JSON.parse(opts.body);

    expect(body.snapshot_id).toBe(10);
    expect(body.payload.target_id).toBe("panel-1");
  });
});
