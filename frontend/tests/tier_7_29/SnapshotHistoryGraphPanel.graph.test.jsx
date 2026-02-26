import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import SnapshotHistoryGraphPanel from "../../src/editor/history/SnapshotHistoryGraphPanel";

vi.mock("../../src/editor/history/useSnapshotHistoryGraph", () => ({
  useSnapshotHistoryGraph: () => ({
    loading: false,
    err: null,
    data: {
      snapshot_id: 3,
      has_parent_links: true,
      nodes: [
        { id: 3, parent_snapshot_id: 2, children_ids: [] },
        { id: 2, parent_snapshot_id: 1, children_ids: [3, 99] },
        { id: 1, parent_snapshot_id: null, children_ids: [2] },
      ],
    },
  }),
}));

describe("SnapshotHistoryGraphPanel graph mode", () => {
  it("renders graph and navigates on node click", () => {
    const onNavigate = vi.fn();
    render(<SnapshotHistoryGraphPanel activeSnapshotId={3} onNavigate={onNavigate} />);

    expect(screen.getByText("Graph")).toBeTruthy();

    // click branch child 99
    const btn99 = screen.getByText("99");
    fireEvent.click(btn99);

    expect(onNavigate).toHaveBeenCalledWith(99);
  });
});
