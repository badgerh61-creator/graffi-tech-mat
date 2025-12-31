import { create } from "zustand";
import { workspaceRegistry } from "../workspaces/_registry";
import type { WorkspaceDefinition } from "../workspaces/_types";

interface WorkspaceState {
  activeWorkspaceId: string;
  setActiveWorkspace: (id: string) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  activeWorkspaceId: "design",

  setActiveWorkspace: (id) =>
    set({ activeWorkspaceId: id }),
}));

/**
 * ✅ REQUIRED BY PanelHost
 * Returns the active workspace definition
 */
export function useActiveWorkspace(): WorkspaceDefinition | null {
  const activeWorkspaceId = useWorkspaceStore(
    (s) => s.activeWorkspaceId
  );

  return workspaceRegistry[activeWorkspaceId] ?? null;
}

