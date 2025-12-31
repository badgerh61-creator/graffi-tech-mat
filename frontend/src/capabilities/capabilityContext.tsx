import React, { createContext, useContext } from "react";
import { CapabilityMap } from "./capability.types";
import { ROLE_CAPABILITIES } from "./roleCapabilities";

export const CapabilityContext = createContext<CapabilityMap | null>(null);

export function CapabilityProvider({
  role,
  children,
}: {
  role: string;
  children: React.ReactNode;
}) {
  const capabilities = ROLE_CAPABILITIES[role] ?? {};

  return (
    <CapabilityContext.Provider value={capabilities}>
      {children}
    </CapabilityContext.Provider>
  );
}

export function useCapabilityContext(): CapabilityMap {
  const ctx = useContext(CapabilityContext);
  if (!ctx) {
    throw new Error("useCapabilityContext must be used within CapabilityProvider");
  }
  return ctx;
}

