import { selectPrimaryById, clearAllSelection } from "../../src/editor/selection/selectionBridge";
import { selectionGetSnapshot } from "../../src/editor/selection/selectionStore";

test("selectPrimaryById sets typed primary and legacy selectedId", () => {
  clearAllSelection();

  selectPrimaryById({ kind: "panel", id: "panel-1" });

  const s = selectionGetSnapshot();

  // v2 typed (inside unified store)
  expect(s.primary?.id).toBe("panel-1");
  expect(s.primary?.kind).toBe("panel");

  // v1 legacy bridge
  expect(s.selectedId).toBe("panel-1");
});

test("clearAllSelection clears typed and legacy", () => {
  selectPrimaryById({ kind: "panel", id: "panel-1" });
  clearAllSelection();

  const s = selectionGetSnapshot();
  expect(s.primary).toBe(null);
  expect(s.selectedId).toBe(null);
});
