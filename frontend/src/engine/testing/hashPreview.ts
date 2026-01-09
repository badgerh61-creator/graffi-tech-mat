// frontend/src/engine/testing/hashPreview.ts

export function hashPreview(preview: { nodes: any[] }): string {
  if (!preview || !Array.isArray(preview.nodes)) {
    return "invalid-preview"
  }

  const stable = [...preview.nodes].sort((a, b) =>
    String(a.id).localeCompare(String(b.id))
  )

  return JSON.stringify(stable)
}

