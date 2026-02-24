// frontend/tests/tier_7_10/ViewportSurface.test.tsx
import React from "react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";

import ViewportSurface from "../../src/editor/viewport/ViewportSurface";
import {
  clearSelection,
  selectionGetSnapshot,
} from "../../src/editor/selection/selectionStore";

// ✅ Mock the async resolver used by Tier 7.18 ViewportSurface
vi.mock("../../src/editor/selection/resolveSelectionClient", () => {
  return {
    resolveSelectionRemote: vi.fn(async ({ hitCandidates, previousSelection }) => {
      const tid = hitCandidates?.[0]?.target_id ?? null;

      // Clicking empty space => clear selection (no modifiers case)
      if (!tid) {
        return { selected_target_ids: [], active_target_id: null, winner: null };
      }

      // Minimal deterministic mock: select the clicked target as the only selection
      return { selected_target_ids: [tid], active_target_id: tid, winner: tid };
    }),
  };
});

describe("tier_7_10 ViewportSurface", () => {
  beforeEach(() => {
    clearSelection();
  });

  it("selects target id on click", async () => {
    render(<ViewportSurface disabled={false} />);

    const proxy = screen.getByText("Panel 1").closest("[data-target-id]");
    fireEvent.click(proxy!);

    // wait a tick for async onClick -> resolveSelectionRemote -> applyResolvedSelectionToStore
    await Promise.resolve();

    expect(selectionGetSnapshot().selectedId).toBe("panel-1");
  });

  it("clears selection when clicking empty space", async () => {
    render(<ViewportSurface disabled={false} />);

    const proxy = screen.getByText("Panel 1").closest("[data-target-id]");
    fireEvent.click(proxy!);
    await Promise.resolve();
    expect(selectionGetSnapshot().selectedId).toBe("panel-1");

    const surface = screen.getByLabelText("viewport-surface");
    fireEvent.click(surface);

    await Promise.resolve();
    expect(selectionGetSnapshot().selectedId).toBe(null);
  });

  it("does nothing when disabled", async () => {
    render(<ViewportSurface disabled={true} />);

    const proxy = screen.getByText("Panel 1").closest("[data-target-id]");
    fireEvent.click(proxy!);

    await Promise.resolve();
    expect(selectionGetSnapshot().selectedId).toBe(null);
  });
});
