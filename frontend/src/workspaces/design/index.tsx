// frontend/src/workspaces/design/index.tsx

/**
 * Phase G+ rule:
 * Workspaces render ONLY the central canvas / engine surface.
 * - No panels
 * - No permission messaging
 * - No UI chrome
 *
 * Capability enforcement happens at:
 * - WorkspaceHost (view/edit)
 * - PanelHost (panel-level)
 */

export default function DesignWorkspace() {
  return (
    <div className="workspace-canvas">
      {/* Engine canvas / scene mount goes here */}
    </div>
  );
}

