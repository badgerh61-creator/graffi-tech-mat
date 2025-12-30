let capabilities: string[] = [];

export function setCapabilities(next: string[]) {
  capabilities = next;
}

export function useCapabilities() {
  return capabilities;
}

