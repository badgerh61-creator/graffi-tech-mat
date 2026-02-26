import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import SnapshotHistoryGraphPanel from "../../src/editor/history/SnapshotHistoryGraphPanel";
import { historyGetSnapshot } from "../../src/editor/history/historyStore";

// Force history endpoint to fail so fallback is used
vi.mock("../../src/editor/history/useSnapshotHistoryGraph", () => ({
  useSnapshotHistoryGraph: () => ({ data: null, err: new Error("no endpoint"), loading: false }),
}));

describe("SnapshotHistoryGraphPanel fallback", () => {
  it("renders local stack and navigates on click", () => {
    const s = historyGetSnapshot();
    s.stack = ["1", "2", "3"];
    s.cursor = 1;

    const onNavigate = vi.fn();

    render(<SnapshotHistoryGraphPanel activeSnapshotId={2} onNavigate={onNavigate} />);

    expect(screen.getByText("Linear (fallback)")).toBeTruthy();
    const btn3 = screen.getByText("3");
    fireEvent.click(btn3);

    expect(onNavigate).toHaveBeenCalledWith("3");
  });
});
