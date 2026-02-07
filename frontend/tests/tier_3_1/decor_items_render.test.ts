import { renderDecorStudio } from "./renderDecorStudio";
import { screen } from "@testing-library/react";

test("decor items render from snapshot", () => {
  renderDecorStudio({
    decor: [
      {
        id: "paint-1",
        domain: "exterior.paint",
        name: "Midnight Blue",
      },
    ],
  });

  expect(screen.getByText("Midnight Blue")).toBeInTheDocument();
});

