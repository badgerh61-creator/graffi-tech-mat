import { screen } from "@testing-library/react";
import { cleanup } from "@testing-library/react";
import { renderEditor } from "../utils/renderEditor";

beforeEach(() => {
  cleanup();
});

test("active snapshot is highlighted", () => {
  renderEditor({
    history: [
      { id: "s1", parentId: null },
      { id: "s2", parentId: "s1" },
    ],
    activeSnapshotId: "s2",
  });

  expect(screen.getByTestId("snapshot-s2")).toHaveClass("active");
});

