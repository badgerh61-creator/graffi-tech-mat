import React, { useMemo, useRef } from "react";
import { useSelection } from "../selection/selectionStore";
import { useActiveDecal } from "../decals/activeDecalStore";
import { useDecalPlacement } from "../decals/decalPlacementStore";
import { useConstraintViolations } from "../constraints/constraintViolationStore";
import { computeInspectorSections } from "./inspectorContext";
import InspectorSummarySection from "./InspectorSummarySection";

import MaterialSlotInspectorPanel from "../materials/MaterialSlotInspectorPanel";
import PaintLibraryPanel from "../materials/PaintLibraryPanel";
import DecalPlacementPanel from "../decals/DecalPlacementPanel";
import VariantSetsPanel from "../variants/VariantSetsPanel";
import ConstraintViolationsPanel from "../constraints/ConstraintViolationsPanel";
import ObjectActionsPanel from "../outliner/ObjectActionsPanel";

// ✅ NEW — Tier 7.61
import PivotOriginPanel from "../transform/PivotOriginPanel";

function Section({ title, children }) {
  return (
    <div className="space-y-2">
      <div className="text-xs font-semibold uppercase opacity-60">
        {title}
      </div>
      {children}
    </div>
  );
}

export default function UnifiedInspectorPanel({
  snapshot,
  toolsEnabled,
  lockState,
  onCommitTool,
  viewerApiRef, // ✅ pass from StudioEditor (important for pivot presets)
}) {
  const { selectedId } = useSelection();
  const { decalId: activeDecalId } = useActiveDecal();
  const { placement } = useDecalPlacement();
  const { violations } = useConstraintViolations();

  const { kind, sections } = useMemo(
    () =>
      computeInspectorSections({
        selectedId,
        activeDecalId,
        placementEnabled: !!placement?.enabled,
        violations,
      }),
    [selectedId, activeDecalId, placement?.enabled, violations]
  );

  return (
    <div className="border rounded p-3 space-y-4">
      <div className="text-sm font-semibold">Inspector</div>

      {/* ---------------- Summary ---------------- */}
      <Section title="Summary">
        <InspectorSummarySection
          selectedId={selectedId}
          activeDecalId={activeDecalId}
          selectionKind={kind}
          activeSnapshot={snapshot}
          toolsEnabled={toolsEnabled}
          lockState={lockState}
        />
      </Section>

      {/* ---------------- Transform ---------------- */}
      {sections.includes("transform") ? (
        <Section title="Transform">
          <ObjectActionsPanel
            canEdit={toolsEnabled}
            onCommitTool={onCommitTool}
          />
        </Section>
      ) : null}

      {/* ✅ NEW — Pivot (Tier 7.61) */}
      {sections.includes("transform") ? (
        <Section title="Pivot / Origin">
          <PivotOriginPanel
            snapshot={snapshot}
            canEdit={toolsEnabled}
            onCommitTool={onCommitTool}
            onRequestPivotPreset={(preset, objectId) => {
              const pivot =
                viewerApiRef?.current?.getPivotPresetForObject?.(
                  objectId,
                  preset
                );

              if (!pivot) return;

              onCommitTool?.({
                tool: "SCENE_SET_OBJECT_PIVOT_PRESET",
                station: "geometry",
                payload: {
                  object_id: objectId,
                  preset,
                  pivot,
                },
              });
            }}
          />
        </Section>
      ) : null}

      {/* ---------------- Materials ---------------- */}
      {sections.includes("materials") ? (
        <Section title="Materials">
          <MaterialSlotInspectorPanel
            snapshot={snapshot}
            canEdit={toolsEnabled}
            onCommitTool={onCommitTool}
          />
        </Section>
      ) : null}

      {/* ---------------- Paint ---------------- */}
      {sections.includes("paint") ? (
        <Section title="Paint">
          <PaintLibraryPanel
            snapshot={snapshot}
            canEdit={toolsEnabled}
            onCommitTool={onCommitTool}
          />
        </Section>
      ) : null}

      {/* ---------------- Decals ---------------- */}
      {sections.includes("decals") ? (
        <Section title="Decals">
          <DecalPlacementPanel />
        </Section>
      ) : null}

      {/* ---------------- Asset Info ---------------- */}
      {sections.includes("asset") ? (
        <Section title="Asset Info">
          <div className="border rounded p-3 text-xs opacity-70">
            Selection-driven asset info placeholder for Tier 7.59.
          </div>
        </Section>
      ) : null}

      {/* ---------------- Variants ---------------- */}
      {sections.includes("variants") ? (
        <Section title="Variants">
          <VariantSetsPanel
            snapshot={snapshot}
            canEdit={toolsEnabled}
            onCommitTool={onCommitTool}
          />
        </Section>
      ) : null}

      {/* ---------------- Constraints ---------------- */}
      {sections.includes("constraints") ? (
        <Section title="Constraints">
          <ConstraintViolationsPanel />
        </Section>
      ) : null}
    </div>
  );
}
