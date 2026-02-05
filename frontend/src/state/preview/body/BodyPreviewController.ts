// src/state/preview/body/BodyPreviewController.ts

export type BodyPreviewState = {
  presetId: string;
  parameters: Record<string, number>;
};

export class BodyPreviewController {
  private state: BodyPreviewState | null = null;

  load(payload: unknown) {
    try {
      if (!payload || typeof payload !== "object") {
        this.state = null;
        return;
      }

      const root = payload as any;

      /**
       * Phase L canonical payload shapes:
       * 1) { snapshot: { body_state } }
       * 2) { body_state: { body } }
       * 3) { body_state }
       * 4) { body }
       */
      const bodyState =
        root.snapshot?.body_state ??
        root.body_state?.body ??
        root.body_state ??
        root.body ??
        null;

      if (!bodyState || typeof bodyState !== "object") {
        this.state = null;
        return;
      }

      // ✅ Canonical normalization (snake_case → camelCase)
      const presetId =
        typeof bodyState.presetId === "string"
          ? bodyState.presetId
          : typeof bodyState.preset_id === "string"
          ? bodyState.preset_id
          : null;

      if (!presetId) {
        this.state = null;
        return;
      }

      this.state = {
        presetId,
        parameters:
          typeof bodyState.parameters === "object" &&
          bodyState.parameters !== null
            ? bodyState.parameters
            : {},
      };
    } catch {
      this.state = null;
    }
  }

  clear() {
    this.state = null;
  }

  getState(): BodyPreviewState | null {
    return this.state;
  }
}

