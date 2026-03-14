import React, { useMemo, useState } from "react";
import { buildOutlinerTree } from "./outlinerTree";
import {
  useMultiSelection,
  toggleMultiSelection,
  setPrimarySelection,
} from "../selection/multiSelectionStore";
import { syncPrimaryToSingleSelection } from "../selection/multiSelectionBridge";

function Row({ node, depth, canEdit, onCommitTool, allObjects }) {
  const [expanded, setExpanded] = useState(true);
  const { selectedIds, primaryId } = useMultiSelection();

  const parentableTargets = allObjects.filter((o) => o.id !== node.id);
  const isSelected = selectedIds.includes(node.id);
  const isPrimary = primaryId === node.id;

  function handleSelect(e) {
    if (e.shiftKey || e.ctrlKey || e.metaKey) {
      toggleMultiSelection(node.id, true);
      return;
    }

    setPrimarySelection(node.id);
    syncPrimaryToSingleSelection(node.id);
  }

  return (
    <div className="space-y-1">
      <div
        className={`border rounded p-2 flex items-center gap-2 ${
          isSelected ? "bg-gray-50" : ""
        } ${isPrimary ? "ring-1 ring-gray-300" : ""}`}
        style={{ marginLeft: `${depth * 16}px` }}
      >
        <button
          className="border rounded px-2 py-1 text-xs"
          onClick={() => setExpanded((v) => !v)}
        >
          {expanded ? "−" : "+"}
        </button>

        <button
          className="text-left flex-1"
          onClick={handleSelect}
        >
          <div className="text-sm font-semibold">
            {node.name || node.id}
          </div>
          <div className="text-[11px] opacity-60 font-mono">
            {node.id} · {node.kind}
          </div>
        </button>

        {node.parent_id ? (
          <button
            className="border rounded px-2 py-1 text-xs"
            disabled={!canEdit}
            onClick={() =>
              onCommitTool?.({
                tool: "SCENE_UNPARENT_OBJECT",
                station: "geometry",
                payload: { object_id: node.id },
              })
            }
          >
            Unparent
          </button>
        ) : null}
      </div>

      {expanded ? (
        <div
          className="border rounded p-2 space-y-2"
          style={{ marginLeft: `${depth * 16 + 16}px` }}
        >
          <div className="text-xs opacity-70">Parenting</div>

          <div className="flex items-center gap-2 flex-wrap">
            {parentableTargets.map((target) => (
              <button
                key={target.id}
                className="border rounded px-2 py-1 text-xs"
                disabled={!canEdit}
                onClick={() =>
                  onCommitTool?.({
                    tool: "SCENE_PARENT_OBJECT",
                    station: "geometry",
                    payload: {
                      object_id: node.id,
                      parent_id: target.id,
                    },
                  })
                }
              >
                Parent → {target.name || target.id}
              </button>
            ))}
          </div>
        </div>
      ) : null}

      {expanded && node.children?.length ? (
        <div className="space-y-1">
          {node.children.map((child) => (
            <Row
              key={child.id}
              node={child}
              depth={depth + 1}
              canEdit={canEdit}
              onCommitTool={onCommitTool}
              allObjects={allObjects}
            />
          ))}
        </div>
      ) : null}
    </div>
  );
}

export default function SceneOutlinerTreePanel({
  snapshot,
  canEdit,
  onCommitTool,
}) {
  const objects = snapshot?.body_state?.objects || [];
  const tree = useMemo(() => buildOutlinerTree(objects), [objects]);

  const [groupName, setGroupName] = useState("Group");

  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-semibold">Scene Hierarchy</div>

      <div className="flex items-center gap-2">
        <input
          className="border rounded px-2 py-1 text-sm"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          placeholder="Group name"
        />
        <button
          className="border rounded px-3 py-2 text-sm"
          disabled={!canEdit || !groupName.trim()}
          onClick={() =>
            onCommitTool?.({
              tool: "SCENE_CREATE_GROUP",
              station: "geometry",
              payload: { name: groupName.trim() },
            })
          }
        >
          Create Group
        </button>
      </div>

      {!tree.length ? (
        <div className="text-xs opacity-70">No scene objects.</div>
      ) : (
        <div className="space-y-2">
          {tree.map((node) => (
            <Row
              key={node.id}
              node={node}
              depth={0}
              canEdit={canEdit}
              onCommitTool={onCommitTool}
              allObjects={objects}
            />
          ))}
        </div>
      )}
    </div>
  );
}
