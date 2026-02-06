// frontend/src/editor/panels/HistoryPanel.jsx
import React from "react";

export default function HistoryPanel({
  history = [],
  activeSnapshotId,
  onNavigate,
}) {
  if (!history.length) return null;

  // Normalize parent key (parent OR parentId)
  const parentMap = Object.fromEntries(
    history.map((s) => [s.id, s.parent ?? s.parentId ?? null])
  );

  const activeParent = parentMap[activeSnapshotId];

  return (
    <div data-testid="history-panel">
      {/* Undo is always allowed if parent exists */}
      {activeParent && (
        <button onClick={() => onNavigate(activeParent)}>
          Undo
        </button>
      )}

      <ul>
        {history.map((s) => (
          <li
            key={s.id}
            data-testid={`snapshot-${s.id}`}
            className={s.id === activeSnapshotId ? "active" : ""}
          >
            {s.id}
          </li>
        ))}
      </ul>
    </div>
  );
}

