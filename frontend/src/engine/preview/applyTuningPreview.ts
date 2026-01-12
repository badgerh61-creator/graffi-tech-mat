import { TuningPreviewState } from "./TuningPreviewMapper"

export function applyTuningPreview(
  preview: TuningPreviewState,
  engine: any,
) {
  // Visual-only application
  // No physics, no mutation persistence

  if (preview.wheels) {
    engine.preview?.setWheelAppearance?.(preview.wheels)
  }

  if (preview.suspension) {
    engine.preview?.setRideHeightHint?.(
      preview.suspension.visualRideHeightOffset,
    )
  }

  if (preview.brakes) {
    engine.preview?.setBrakeStyle?.(preview.brakes.style)
  }

  if (preview.engine) {
    engine.preview?.setEngineBadge?.(preview.engine.badge)
  }
}

