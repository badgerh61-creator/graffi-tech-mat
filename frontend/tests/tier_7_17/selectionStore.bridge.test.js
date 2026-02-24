import {
  selectionGetSnapshot,
  clearSelection,
  setSelectedId,
  setPrimarySelection,
  clearTypedSelection,
} from "../../src/editor/selection/selectionStore";

test("setSelectedId bridges to primary", () => {
  clearSelection();
  setSelectedId("panel-1");

  const s = selectionGetSnapshot();
  expect(s.selectedId).toBe("panel-1");
  expect(s.primary.id).toBe("panel-1");
  expect(s.primary.kind).toBe("panel");
});

test("setPrimarySelection bridges to selectedId", () => {
  clearSelection();
  setPrimarySelection({ kind: "panel", id: "panel-2" });

  const s = selectionGetSnapshot();
  expect(s.primary.id).toBe("panel-2");
  expect(s.selectedId).toBe("panel-2");
});

test("clearSelection clears both v1 + v2", () => {
  setSelectedId("panel-1");
  clearSelection();

  const s = selectionGetSnapshot();
  expect(s.selectedId).toBe(null);
  expect(s.primary).toBe(null);
  expect(s.secondary).toEqual([]);
  expect(s.hovered).toBe(null);
});

test("clearTypedSelection clears v2 and legacy", () => {
  setPrimarySelection({ kind: "panel", id: "panel-1" });
  clearTypedSelection();

  const s = selectionGetSnapshot();
  expect(s.primary).toBe(null);
  expect(s.selectedId).toBe(null);
});
