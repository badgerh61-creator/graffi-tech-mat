/**
 * Resolve whether selected id is legal for the current snapshot.
 * For now: allow any non-empty string (UI-only), but keep hook point.
 *
 * Later tiers can validate against a scene index.
 */
export function resolveSelectedTarget(activeSnapshot, selectedId) {
  if (!activeSnapshot?.id) return { targetId: null, reason: "no active snapshot" };
  if (!selectedId) return { targetId: null, reason: "nothing selected" };
  return { targetId: selectedId, reason: null };
}
