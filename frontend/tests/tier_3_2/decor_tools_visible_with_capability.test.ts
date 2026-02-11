import { renderDecorStudio } from "../utils/renderDecorStudio";
import { renderDecorStudio } from "../utils/renderDecorStudio";
import { screen } from "@testing-library/react";

test("decor tools visible when capability present", () => {
  renderDecorStudio({
    capabilities: ["decor.exterior.edit"],
  });

  expect(screen.getByText(/apply material/i)).toBeInTheDocument();
});

