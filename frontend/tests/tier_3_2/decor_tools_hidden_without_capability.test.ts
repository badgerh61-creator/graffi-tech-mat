import { renderDecorStudio } from "../utils/renderDecorStudio";
import { screen } from "@testing-library/react";

test("decor tools hidden without capability", () => {
  renderDecorStudio({
    capabilities: [],
  });

  expect(screen.queryByText(/apply material/i)).toBeNull();
});

