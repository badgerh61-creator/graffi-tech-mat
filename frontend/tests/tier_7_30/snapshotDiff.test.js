import { summarizeSnapshotDiff } from "../../src/editor/history/snapshotDiff";

test("summarizes body arrays by id when possible", () => {
  const base = {
    id: 1,
    status: "draft",
    body_state: { panels: [{ id: "p1", a: 1 }] },
    decor_state: { x: 1 },
    tuning_state: {},
  };

  const target = {
    id: 2,
    parent_snapshot_id: 1,
    status: "draft",
    body_state: { panels: [{ id: "p1", a: 2 }, { id: "p2" }] },
    decor_state: { x: 2, y: 9 },
    tuning_state: {},
  };

  const d = summarizeSnapshotDiff(base, target);
  expect(d.body.panels.mode).toBe("id");
  expect(d.body.panels.added).toBe(1);   // p2
  expect(d.body.panels.changed).toBe(1); // p1 changed
  expect(d.decor.changed).toBe(1);       // x changed
  expect(d.decor.added).toBe(1);         // y added
});

test("status change is detected", () => {
  const base = { id: 1, status: "draft", body_state: {} };
  const target = { id: 2, parent_snapshot_id: 1, status: "completed", body_state: {} };
  const d = summarizeSnapshotDiff(base, target);
  expect(d.meta.statusChanged).toBe(true);
  expect(d.meta.fromStatus).toBe("draft");
  expect(d.meta.toStatus).toBe("completed");
});
