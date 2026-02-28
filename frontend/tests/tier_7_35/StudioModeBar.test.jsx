// tests/tier_7_35/StudioModeBar.test.jsx
import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, fireEvent, screen, waitFor } from "@testing-library/react";

import StudioModeBar from "../../src/editor/modes/StudioModeBar";

// ✅ Mock API module (best: avoids fetch/res.ok issues entirely)
vi.mock("../../src/services/studio/draftWorkspaceApi", () => {
  return {
    startEdit: vi.fn(async () => ({ draft_snapshot_id: 2 })),
    completeDraft: vi.fn(async () => ({ completed_snapshot_id: 99 })),
    discardDraft: vi.fn(async () => ({ parent_snapshot_id: 99 })),
  };
});

describe("Tier 7.35 StudioModeBar", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("Enter Edit calls onSetActiveSnapshotId with draft_snapshot_id", async () => {
    const onSet = vi.fn();

    render(
      <StudioModeBar
        activeSnapshot={{ id: 1, status: "completed" }}
        onSetActiveSnapshotId={onSet}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /enter edit/i }));

    await waitFor(() => {
      expect(onSet).toHaveBeenCalledWith(2);
    });
  });

  it("Complete Draft calls onSetActiveSnapshotId with completed_snapshot_id", async () => {
    const onSet = vi.fn();

    render(
      <StudioModeBar
        activeSnapshot={{ id: 2, status: "draft" }}
        onSetActiveSnapshotId={onSet}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /complete draft/i }));

    await waitFor(() => {
      expect(onSet).toHaveBeenCalledWith(99);
    });
  });

  it("Discard Draft calls onSetActiveSnapshotId with parent_snapshot_id", async () => {
    const onSet = vi.fn();

    render(
      <StudioModeBar
        activeSnapshot={{ id: 2, status: "draft" }}
        onSetActiveSnapshotId={onSet}
      />
    );

    fireEvent.click(screen.getByRole("button", { name: /discard draft/i }));

    await waitFor(() => {
      expect(onSet).toHaveBeenCalledWith(99);
    });
  });
});
