// frontend/src/workspaces/_registry.ts

import DesignWorkspace from "./design";
import { WorkspaceDefinition } from "./_types";

export const workspaceRegistry: Record<string, WorkspaceDefinition> = {
  design: {
    id: "design",
    title: "Design",
    allowedPanels: [
      "asset-browser",
      "engine-preview",
      "jobs", // ✅ Phase H3: async jobs visibility
    ],
  },
};

export const workspaceComponents: Record<string, any> = {
  design: DesignWorkspace,
};

