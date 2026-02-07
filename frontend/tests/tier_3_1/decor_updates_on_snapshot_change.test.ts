import {
  renderDecorStudio,
  rerenderDecorStudio,
} from "./helpers/renderDecorStudio";

import { screen } from "@testing-library/react";

test("decor updates when snapshot changes", () => {
  renderDecorStudio({
    decor: [{ id: "p1", name: "Blue" }],
  });

  rerenderDecorStudio({
    decor: [{ id: "p2", name: "Green" }],
  });

  expect(screen.getByText("Green")).toBeInTheDocument();
});

