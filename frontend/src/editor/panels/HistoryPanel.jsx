// frontend/src/editor/panels/HistoryPanel.jsx
import React from "react";

export default function HistoryPanel({
  history = [],
  activeSnapshotId,
  onNavigate,
}) {
  if (!Array.isArray(history) || history.length === 0) return null;

  const activeId = activeSnapshotId != null ? String(activeSnapshotId) : null;

  // Normalize parent key (parent OR parentId)
  const parentMap = Object.fromEntries(
    history.map((s) => [String(s.id), s.parent ?? s.parentId ?? null])
  );

  const activeParent = activeId ? parentMap[activeId] : null;

  return (
    <div data-testid="history-panel">
      {/* Undo is always allowed if parent exists */}
      {activeParent && (
        <button onClick={() => onNavigate(activeParent)}>
          Undo
        </button>
      )}

      <ul>
        {history.map((s) => {
          const sid = String(s.id);
          const isActive = activeId != null && sid === activeId;

          return (
            <li
              key={sid}
              data-testid={`snapshot-${sid}`}
              className={isActive ? "active" : ""}
            >
              {sid}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
