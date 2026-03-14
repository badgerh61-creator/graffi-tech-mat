export function detectSelectionKind({ selectedId, activeDecalId }) {
  if (activeDecalId) return "decal";
  if (!selectedId) return "none";
  if (String(selectedId).includes("::slot:")) return "slot";
  if (String(selectedId).includes("::")) return "mesh";
  return "object";
}

export function computeInspectorSections({
  selectedId,
  activeDecalId,
  placementEnabled,
  violations,
}) {
  const kind = detectSelectionKind({ selectedId, activeDecalId });

  const sections = ["summary"];

  if (kind === "object" || kind === "mesh" || kind === "slot") {
    sections.push("transform");
    sections.push("materials");
    sections.push("paint");
    sections.push("asset");
  }

  if (kind === "decal" || placementEnabled) {
    sections.push("decals");
  }

  sections.push("variants");

  if ((violations || []).length > 0) {
    sections.push("constraints");
  }

  return { kind, sections };
}
