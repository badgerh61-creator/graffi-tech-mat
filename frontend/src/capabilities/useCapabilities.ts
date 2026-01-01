useCapabilities.ts
import { Capability } from "./capability.types";
import { useCapabilityContext } from "./capabilityContext";

export function useCapabilities() {
  return useCapabilityContext();
}

export function useCapability(capability: Capability): boolean {
  const caps = useCapabilityContext();
  return Boolean(caps[capability]);
}
