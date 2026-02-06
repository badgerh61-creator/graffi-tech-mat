// tests/utils/renderEditor.tsx

// NOTE:
// withHistory=true is ONLY for Tier 2.3+ tests.
// Do not enable for earlier phases.

import React from "react";
import { render } from "@testing-library/react";
import EditorShell from "../../src/app/EditorShell";
import ConstraintPanel from "../../src/editor/panels/ConstraintPanel";

type RenderEditorOptions = {
  constraints?: any[];
  withHistory?: boolean;

  // 🆕 Tier 2.3 injection
  history?: any[];
  activeSnapshotId?: string | null;
  onNavigate?: (id: string) => void;
};

export function renderEditor({
  constraints = [],
  withHistory = false,
  history,
  activeSnapshotId,
  onNavigate,
}: RenderEditorOptions = {}) {
  return render(
    <EditorShell
      history={history}
      activeSnapshotId={activeSnapshotId}
      onNavigate={onNavigate}
    >
      {/* 🔒 Legacy behavior */}
      {!withHistory && (
        <ConstraintPanel constraints={constraints} />
      )}

      <div data-testid="editor-content" />
    </EditorShell>
  );
}

