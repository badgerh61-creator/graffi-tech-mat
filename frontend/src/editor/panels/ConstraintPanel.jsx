// src/editor/panels/ConstraintPanel.jsx
import React from "react";

export default function ConstraintPanel({ constraints = [] }) {
  if (!constraints.length) return null;

  return (
    <section>
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

