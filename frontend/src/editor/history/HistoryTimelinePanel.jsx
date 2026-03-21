// frontend/src/editor/history/HistoryTimelinePanel.jsx

import React from "react";
import { useHistory, jumpToSnapshot } from "./historyStore";

export default function HistoryTimelinePanel({
  onRestoreSnapshot,
}) {
  const { stack, cursor } = useHistory();

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">History Timeline</div>

      {!stack.length ? (
        <div className="text-xs opacity-60">No history yet</div>
      ) : (
        <div className="space-y-1 max-h-60 overflow-auto">
          {stack.map((id, i) => {
            const active = i === cursor;

            return (
              <button
                key={id}
                className={`w-full text-left border rounded p-2 text-xs ${
                  active ? "bg-gray-100" : ""
                }`}
                onClick={() => {
                  const snapId = jumpToSnapshot(id);
                  if (snapId) {
                    onRestoreSnapshot?.(snapId);
                  }
                }}
              >
                <div className="font-mono">#{id}</div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
