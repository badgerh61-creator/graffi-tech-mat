// tests/utils/renderDecorStudio.tsx

import React from "react";
import { render } from "@testing-library/react";
import { CapabilityProvider } from "../../src/capabilities";
import DecorStudioEditable from "../../src/editor/studio/DecorStudioEditable";

type Options = {
  capabilities?: string[];
};

export function renderDecorStudio({
  capabilities = [],
}: Options = {}) {
  // Map test capabilities → role
  // If edit capability present → use "editor"
  const role = capabilities.includes("decor.exterior.edit")
    ? "editor"
    : "viewer";

  return render(
    <CapabilityProvider role={role}>
      <DecorStudioEditable />
    </CapabilityProvider>
  );
}

