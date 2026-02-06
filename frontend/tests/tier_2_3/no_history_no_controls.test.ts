import { screen } from "@testing-library/react";
import { cleanup } from "@testing-library/react";
import { renderEditor } from "../utils/renderEditor";

beforeEach(() => {
  cleanup();
});

test("snapshot history graph renders nodes", () => {
  renderEditor({
    history: [
      { id: "s1", parentId: null },
      { id: "s2", parentId: "s1" },
    ],
    activeSnapshotId: "s2",
  });

  expect(screen.getByText("s1")).toBeInTheDocument();
  expect(screen.getByText("s2")).toBeInTheDocument();
});

