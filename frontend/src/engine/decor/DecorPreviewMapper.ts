// frontend/src/engine/decor/DecorPreviewMapper.ts

type DecorDecalInstance = {
  instance_id: string
  asset_id: string
  panel: string
  uv: {
    x: number
    y: number
    scale: number
    rotation: number
  }
}

type DecorPreviewInput = {
  snapshotId: string
  decor: {
    decals: DecorDecalInstance[]
  }
}

type EngineNode = {
  id: string
  type: "decal"
  targetPanel: string
  transform: object
}

type DecorPreviewResult = {
  nodes: EngineNode[]
}

function isValidDecal(d: any): d is DecorDecalInstance {
  return (
    d &&
    typeof d.instance_id === "string" &&
    typeof d.asset_id === "string" &&
    typeof d.panel === "string" &&
    d.uv &&
    typeof d.uv.x === "number" &&
    typeof d.uv.y === "number" &&
    typeof d.uv.scale === "number" &&
    typeof d.uv.rotation === "number"
  )
}

export class DecorPreviewMapper {
  private nodes: EngineNode[] = []

  build(input: DecorPreviewInput): DecorPreviewResult {
    if (
      !input ||
      typeof input.snapshotId !== "string" ||
      !input.decor ||
      !Array.isArray(input.decor.decals)
    ) {
      throw new Error("Invalid decor preview payload")
    }

    // 🔑 Empty decor is VALID → clears preview
    for (const decal of input.decor.decals) {
      if (!isValidDecal(decal)) {
        throw new Error("Invalid decor decal entry")
      }
    }

    this.clear()

    const decals = [...input.decor.decals].sort((a, b) =>
      a.instance_id.localeCompare(b.instance_id)
    )

    this.nodes = decals.map(d => ({
      id: d.instance_id,
      type: "decal",
      targetPanel: d.panel,
      transform: d.uv,
    }))

    return { nodes: this.nodes }
  }

  clear() {
    this.nodes = []
  }

  currentNodes() {
    return this.nodes
  }
}

export function buildDecorPreview(
  input: DecorPreviewInput
): DecorPreviewResult {
  const mapper = new DecorPreviewMapper()
  return mapper.build(input)
}

