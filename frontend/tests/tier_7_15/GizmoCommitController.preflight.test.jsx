import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";

// mocks...
vi.mock("../../src/editor/selection/selectionStore", () => ({
  useSelection: () => ({
    selectedId: null,
    primary: null,
    secondary: [],
    hovered: null,
    lastUpdatedAt: 0,
  }),
}));

vi.mock("../../src/editor/gizmo/TransformGizmo", () => ({
  default: ({ activeTargetId, enabled }) => (
    <div>
      <div data-testid="target">{activeTargetId ?? "none"}</div>
      <div data-testid="enabled">{String(!!enabled)}</div>
    </div>
  ),
}));

vi.mock("../../src/services/studio/toolExecutionAdapter", () => ({
  executeTool: vi.fn(async () => ({ ok: true, data: { new_snapshot_id: 2 } })),
}));

import GizmoCommitController from "../../src/editor/gizmo/GizmoCommitController";

describe("tier_7_15 GizmoCommitController preflight", () => {
  it("shows no target when selection.primary is null", () => {
    render(
      <GizmoCommitController
        activeSnapshot={{ id: 10, status: "draft" }}
        enabled={true}
        reasonDisabled={null}
        onApplied={() => {}}
        enablePreview={false}
      />
    );

    expect(screen.getByTestId("target").textContent).toBe("none");
    expect(screen.getByTestId("enabled").textContent).toBe("false");
  });
});
