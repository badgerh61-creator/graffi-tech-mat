import React from "react";
import { render } from "@testing-library/react";
import ConstraintPanel from "../../src/editor/panels/ConstraintPanel";

type Constraint = {
  id: string;
  type: string;
  description?: string;
  source?: string;
};

export function renderConstraintPanel({
  constraints = [],
}: {
  constraints?: Constraint[];
} = {}) {
  return render(<ConstraintPanel constraints={constraints} />);
}

