export type SelectableKind = "panel" | "curve" | "surface" | "vertex" | "edge";

export type SelectionItem = {
  kind: SelectableKind;
  id: string;
};

export type SelectionState = {
  primary: SelectionItem | null;
  secondary: SelectionItem[];
  hovered: SelectionItem | null;
  lastUpdatedAt: number;
};
