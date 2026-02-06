import { screen, fireEvent } from "@testing-library/react";

test("redo requires explicit child selection", () => {
  renderEditor({
    history: [
      { id: "s1" },
      { id: "s2", parent: "s1" },
      { id: "s3", parent: "s1" },
    ],
    activeSnapshotId: "s1",
  });

  expect(screen.queryByText("Redo")).toBeNull();
});

