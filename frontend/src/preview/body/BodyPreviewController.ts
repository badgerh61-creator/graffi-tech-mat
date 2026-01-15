import { reduceBodyPreview } from "./bodyPreviewReducer";
import { BodyPreviewPayload, BodyPreviewState } from "./bodyPreviewTypes";

export class BodyPreviewController {
  private state: BodyPreviewState | null = null;

  load(payload: BodyPreviewPayload) {
    this.state = reduceBodyPreview(this.state, payload);
  }

  clear() {
    this.state = null;
  }

  getState(): BodyPreviewState | null {
    return this.state;
  }
}

