// frontend/src/editor/panels/ConstraintPanel.jsx
import React from "react";

export default function ConstraintPanel({ constraints = [] }) {
  // Contract: if none exist => no UI at all
  if (!Array.isArray(constraints) || constraints.length === 0) return null;

  return (
    <section data-testid="constraints-panel">
      <h3>Active Constraints</h3>
      <ul>
        {constraints.map((c) => (
          <li key={c.id}>
            <strong data-readonly="true">{c.type}</strong>

            {c.description && <div>{c.description}</div>}
            {c.source && <small>{c.source}</small>}
          </li>
        ))}
      </ul>
    </section>
  );
}
