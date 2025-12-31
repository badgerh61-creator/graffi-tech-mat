import DesignWorkspace from "./design";

import { WorkspaceDefinition } from "./_types";

export const workspaceRegistry: Record<string, WorkspaceDefinition> = {
  design: {
    id: "design",
    title: "Design",
    allowedPanels: ["asset-browser"],
  },
};

export const workspaceComponents: Record<string, any> = {
  design: DesignWorkspace,
};

