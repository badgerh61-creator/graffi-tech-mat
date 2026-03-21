import React from "react"; 
import { render, screen } from "@testing-library/react";
import HistoryTimelinePanel from "../../src/editor/history/HistoryTimelinePanel";

test("renders history panel", () => {
  render(<HistoryTimelinePanel onRestoreSnapshot={() => {}} />);
  expect(screen.getByText("History Timeline")).toBeTruthy();
});
