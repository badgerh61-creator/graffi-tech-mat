import { resolvePrimaryTarget } from "../../src/editor/selection/resolveTarget";

test("returns no_selection when primary is null", () => {
  const res = resolvePrimaryTarget({ primary: null });
  expect(res.ok).toBe(false);
  if (!res.ok) expect(res.reason).toBe("no_selection");
});

test("resolves primary id deterministically", () => {
  const res = resolvePrimaryTarget({ primary: { kind: "panel", id: "panel-1" } });
  expect(res.ok).toBe(true);
  if (res.ok) {
    expect(res.target_id).toBe("panel-1");
    expect(res.kind).toBe("panel");
  }
});
