export type DockZone = "left" | "right" | "bottom" | "center";

export interface EditorLayoutState {
  left: string[];
  right: string[];
  bottom: string[];
  center: string | null;
}

