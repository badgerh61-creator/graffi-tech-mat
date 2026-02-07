import { renderDecorStudio } from "./renderDecorStudio";
import { screen } from "@testing-library/react";

test("decor items grouped by domain", () => {
  renderDecorStudio({
    decor: [
      { id: "p1", domain: "exterior.paint", name: "Red" },
      { id: "s1", domain: "interior.seats", name: "Cloth" },
    ],
  });

  expect(screen.getByText(/Exterior Paint/i)).toBeInTheDocument();
  expect(screen.getByText(/Interior Seats/i)).toBeInTheDocument();
});

