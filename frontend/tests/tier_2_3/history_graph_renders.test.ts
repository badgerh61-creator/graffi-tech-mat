import { screen } from "@testing-library/react";
import { renderEditor } from "../utils/renderEditor";

test("snapshot history graph renders nodes", () => {
  renderEditor({
    withHistory: true, // ✅ REQUIRED for Tier 2.3
    history: [
      { id: "s1", parent: null },
      { id: "s2", parent: "s1" },
    ],
    activeSnapshotId: "s2",
  });

  expect(screen.getByText("s1")).toBeInTheDocument();
  expect(screen.getByText("s2")).toBeInTheDocument();
});

