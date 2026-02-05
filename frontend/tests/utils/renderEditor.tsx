import React from "react";
import { render } from "@testing-library/react";
import EditorShell from "../../src/app/EditorShell";
import ConstraintPanel from "../../src/editor/panels/ConstraintPanel";

export function renderEditor({ constraints = [] } = {}) {
  return render(
    <EditorShell>
      <ConstraintPanel constraints={constraints} />
      <div data-testid="editor-content" />
    </EditorShell>
  );
}

