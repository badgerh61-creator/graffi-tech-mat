import { toolPreflightGuard } from "../../src/editor/tools/toolPreflightGuard";
import type { SelectionState } from "../../src/editor/selection/selectionTypes";

function sel(primary: any): SelectionState {
  return {
    primary,
    secondary: [],
    hovered: null,
    lastUpdatedAt: 0,
  };
}

test("blocks when uiDisabled", () => {
  const r = toolPreflightGuard({
    selection: sel({ kind: "panel", id: "panel-1" }),
    uiDisabled: true,
    activeSnapshotId: 10,
  });

  expect(r.ok).toBe(false);
  if (!r.ok) expect(r.reason).toBe("ui_disabled");
});

test("blocks when no snapshot", () => {
  const r = toolPreflightGuard({
    selection: sel({ kind: "panel", id: "panel-1" }),
    uiDisabled: false,
    activeSnapshotId: null,
  });

  expect(r.ok).toBe(false);
  if (!r.ok) expect(r.reason).toBe("no_snapshot");
});

test("blocks when no selection", () => {
  const r = toolPreflightGuard({
    selection: sel(null),
    uiDisabled: false,
    activeSnapshotId: 10,
  });

  expect(r.ok).toBe(false);
  if (!r.ok) expect(r.reason).toBe("no_selection");
});

test("passes when selection + snapshot + enabled", () => {
  const r = toolPreflightGuard({
    selection: sel({ kind: "panel", id: "panel-1" }),
    uiDisabled: false,
    activeSnapshotId: 10,
  });

  expect(r.ok).toBe(true);
  if (r.ok) expect(r.target_id).toBe("panel-1");
});
