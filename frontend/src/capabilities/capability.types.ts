// frontend/src/capabilities/capability.types.ts

export type Capability =
  // global
  | "view"
  | "edit"
  | "upload"
  | "delete"
  | "admin"

  // assets
  | "assets.view"
  | "assets.use";

export type CapabilityMap = Partial<Record<Capability, boolean>>;

