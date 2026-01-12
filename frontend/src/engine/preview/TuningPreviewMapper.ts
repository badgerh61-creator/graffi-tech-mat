export type TuningPreviewState = {
  suspension?: {
    visualRideHeightOffset: number
  }
  wheels?: {
    diameter: number
    width: number
    offset: number
  }
  brakes?: {
    style: string
  }
  engine?: {
    badge: string
  }
}

export function mapTuningToPreview(snapshot: any): TuningPreviewState {
  const tuning = snapshot?.tuning ?? {}

  return {
    suspension: tuning.suspension
      ? {
          visualRideHeightOffset:
            tuning.suspension.preset_id === "sport_low" ? -0.04 : 0,
        }
      : undefined,

    wheels: tuning.wheels
      ? {
          diameter: tuning.wheels.diameter,
          width: tuning.wheels.width,
          offset: tuning.wheels.offset,
        }
      : undefined,

    brakes: tuning.brakes
      ? {
          style: tuning.brakes.preset_id,
        }
      : undefined,

    engine: tuning.engine
      ? {
          badge: tuning.engine.preset_id,
        }
      : undefined,
  }
}

