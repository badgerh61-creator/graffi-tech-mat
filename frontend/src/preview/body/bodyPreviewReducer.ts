import { BodyPreviewPayload, BodyPreviewState } from "./bodyPreviewTypes";

export function reduceBodyPreview(
  _prev: BodyPreviewState | null,
  payload: BodyPreviewPayload
): BodyPreviewState | null {
  if (!payload.body_state) return null;

  return {
    presetId: payload.body_state.preset_id,
    parameters: { ...payload.body_state.parameters },
  };
}

