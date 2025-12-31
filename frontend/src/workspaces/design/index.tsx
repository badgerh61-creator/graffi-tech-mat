// frontend/src/workspaces/design/index.tsx

import { useCapability } from "../../capabilities/useCapabilities";

export default function DesignWorkspace() {
  const canView = useCapability("design.view");

  // 🔐 GLOBAL + DOMAIN EDIT GATE (minimal alignment)
  const canEdit =
    useCapability("edit") &&
    useCapability("design.edit");

  if (!canView) {
    return (
      <div className="workspace design-workspace design--disabled">
        <h2>Design Workspace</h2>
        <p>You do not have permission to access this workspace.</p>
      </div>
    );
  }

  return (
    <div
      className={`workspace design-workspace ${
        canEdit ? "design--editable" : "design--read-only"
      }`}
    >
      <h2>Design Workspace</h2>

      {!canEdit && (
        <p className="workspace-readonly-hint">
          Read-only mode — editing tools are disabled.
        </p>
      )}

      {canEdit ? (
        <p>Design tools enabled.</p>
      ) : (
        <p>Previewing design state.</p>
      )}
    </div>
  );
}

