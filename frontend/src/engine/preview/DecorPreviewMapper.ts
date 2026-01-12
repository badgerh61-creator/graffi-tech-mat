export function mapDecorToPreview(snapshot: any) {
  const decor = snapshot?.decor

  if (!decor || !Array.isArray(decor.decals)) {
    return {}
  }

  return {
    decals: decor.decals.map((d: any) => ({
      id: d.id,
      panel: d.panel,
      uv: d.uv,
    })),
  }
}

