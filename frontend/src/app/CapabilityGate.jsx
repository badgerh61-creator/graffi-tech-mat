import { useCapabilities } from "../state/capabilityStore";

export default function CapabilityGate({ capability, children }) {
  const capabilities = useCapabilities();

  if (!capabilities.includes(capability)) {
    return null;
  }

  return children;
}

