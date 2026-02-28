import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import StudioModeBar from "../../src/editor/modes/StudioModeBar";

vi.mock("../../src/utils/auth", () => ({
  getAccessToken: () => "T",
}));

describe("Tier 7.35 StudioModeBar", () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("shows READ when snapshot is completed", () => {
    render(<StudioModeBar activeSnapshot={{ id: 1, status: "completed" }} />);
    expect(screen.getByText(/READ/)).toBeTruthy();
  });

  it("calls start-edit and sets draft snapshot id", async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ mode: "edit", draft_snapshot_id: 99 }),
    });

    const onSet = vi.fn();
    render(
      <StudioModeBar
        activeSnapshot={{ id: 1, status: "completed" }}
        onSetActiveSnapshotId={onSet}
      />
    );

    fireEvent.click(screen.getByText("Enter Edit"));

    await waitFor(() => {
      expect(onSet).toHaveBeenCalledWith(99);
    });

    const [url] = global.fetch.mock.calls[0];
    expect(url).toContain("/snapshots/1/start-edit");
  });

  it("shows EDIT (DRAFT) when snapshot is draft", () => {
    render(<StudioModeBar activeSnapshot={{ id: 2, status: "draft" }} />);
    expect(screen.getByText(/EDIT \(DRAFT\)/)).toBeTruthy();
  });
});
