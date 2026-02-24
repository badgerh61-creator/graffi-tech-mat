import { applyResolvedSelectionToStore } from "../../src/editor/selection/applyResolvedSelectionToStore";
import { selectionGetSnapshot, clearSelection } from "../../src/editor/selection/selectionStore";

test("applies resolved selection into unified store", () => {
  clearSelection();

  applyResolvedSelectionToStore({
    selected_target_ids: ["a", "b", "c"],
    active_target_id: "b",
    winner: "b",
  });

  const s = selectionGetSnapshot();
  expect(s.primary.id).toBe("b");
  expect(s.selectedId).toBe("b");

  const secondaryIds = s.secondary.map((x) => x.id).sort();
  expect(secondaryIds).toEqual(["a", "c"]);
});

test("clears selection when resolved is empty", () => {
  applyResolvedSelectionToStore({
    selected_target_ids: [],
    active_target_id: null,
    winner: null,
  });

  const s = selectionGetSnapshot();
  expect(s.primary).toBe(null);
  expect(s.selectedId).toBe(null);
  expect(s.secondary.length).toBe(0);
});
