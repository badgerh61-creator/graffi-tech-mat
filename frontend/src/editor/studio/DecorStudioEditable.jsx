// src/editor/studio/DecorStudioEditable.jsx

import React from "react";
import DecorStudio from "./DecorStudio";
import { useCapability } from "../../capabilities";

export default function DecorStudioEditable({ decor = [] }) {
  const canEdit = useCapability("decor.exterior.edit");

  return (
    <section aria-label="Decor Studio Editable">
      <header>
        <h2>Decor Studio</h2>
      </header>

      {canEdit && (
        <div>
          <button>Apply Material</button>
        </div>
      )}

      <DecorStudio decor={decor} />
    </section>
  );
}

