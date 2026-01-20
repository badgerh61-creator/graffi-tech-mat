export type GeometryCommand =
  | { command: "SET_PARAM"; param: string; value: number }
  | { command: "SEGMENT_PANEL"; surface_id: string; bounds: string };

