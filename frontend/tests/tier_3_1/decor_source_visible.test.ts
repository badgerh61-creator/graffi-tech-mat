import { renderDecorStudio } from "./renderDecorStudio";
import { screen } from "@testing-library/react";

test("decor source metadata shown", () => {
  renderDecorStudio({
    decor: [
      {
        id: "d1",
        name: "Matatu Stripe",
        source: "culture-pack:kenya",
      },
    ],
  });

  expect(screen.getByText(/kenya/i)).toBeInTheDocument();
});

