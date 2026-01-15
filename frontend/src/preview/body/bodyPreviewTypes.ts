export interface BodyPreviewState {
  presetId: string | null;
  parameters: Record<string, number>;
}

export interface BodyPreviewPayload {
  body_state?: {
    preset_id: string;
    parameters: Record<string, number>;
  } | null;
}

