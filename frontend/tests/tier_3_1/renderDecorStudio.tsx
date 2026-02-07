import React from "react";
import { render } from "@testing-library/react";
import DecorStudio from "@/editor/studio/DecorStudio";

export function renderDecorStudio({
  decor = [],
}: {
  decor?: any[];
}) {
  return render(<DecorStudio decor={decor} />);
}

