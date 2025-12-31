export type Capability =
  | "viewStudio"
  | "editWorkspace"
  | "useAssets"
  | "useDecor"
  | "useTuning"
  | "manageModels"
  | "adminAccess";

export type CapabilityMap = Partial<Record<Capability, boolean>>;

