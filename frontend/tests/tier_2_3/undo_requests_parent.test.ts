import { screen, fireEvent, within } from "@testing-library/react";
import { cleanup } from "@testing-library/react";
import { renderEditor } from "../utils/renderEditor";
import { vi } from "vitest";

beforeEach(() => {
  cleanup();
});

test("undo requests parent snapshot", () => {
  const onNavigate = vi.fn();

  renderEditor({
    history: [
      { id: "s1" },
      { id: "s2", parentId: "s1" },
    ],
    activeSnapshotId: "s2",
    onNavigate,
  });

  const panel = screen.getByTestId("history-panel");
  fireEvent.click(within(panel).getByText("Undo"));

  expect(onNavigate).toHaveBeenCalledWith("s1");
});

