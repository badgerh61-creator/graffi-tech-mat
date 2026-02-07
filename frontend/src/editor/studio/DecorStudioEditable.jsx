import React from "react";
import DecorStudio from "./DecorStudio";
import { DecorTools } from "./DecorTools";

export default function DecorStudioEditable({
  decor,
  canEdit,
}) {
  return (
    <section aria-label="Decor Studio Editable">
      <header>
        <h2>Decor Studio</h2>

        {/* Editing controls live OUTSIDE the renderer */}
        <DecorTools canEdit={canEdit} />
      </header>

      {/* Delegate read-only rendering */}
      <DecorStudio decor={decor} />
    </section>
  );
}

