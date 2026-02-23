import React from "react";
import { describe, it, expect, beforeEach } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";

import ViewportSurface from "../../src/editor/viewport/ViewportSurface";
import {
  clearSelection,
  selectionGetSnapshot,
} from "../../src/editor/selection/selectionStore";

describe("tier_7_10 ViewportSurface", () => {
  beforeEach(() => {
    clearSelection();
  });

  it("selects target id on click", () => {
    render(<ViewportSurface disabled={false} />);

    const proxy = screen.getByText("Panel 1").closest("[data-target-id]");
    fireEvent.click(proxy!);

    expect(selectionGetSnapshot().selectedId).toBe("panel-1");
  });

  it("clears selection when clicking empty space", () => {
    render(<ViewportSurface disabled={false} />);

    const proxy = screen.getByText("Panel 1").closest("[data-target-id]");
    fireEvent.click(proxy!);
    expect(selectionGetSnapshot().selectedId).toBe("panel-1");

    const surface = screen.getByLabelText("viewport-surface");
    fireEvent.click(surface);

    expect(selectionGetSnapshot().selectedId).toBe(null);
  });

  it("does nothing when disabled", () => {
    render(<ViewportSurface disabled={true} />);

    const proxy = screen.getByText("Panel 1").closest("[data-target-id]");
    fireEvent.click(proxy!);

    expect(selectionGetSnapshot().selectedId).toBe(null);
  });
});
