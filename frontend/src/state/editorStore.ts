let activeWorkspace = "design";

export function getActiveWorkspace() {
  return activeWorkspace;
}

export function setActiveWorkspace(id: string) {
  activeWorkspace = id;
}

