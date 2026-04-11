/**
 * Tier 7.76 — Attach gizmo to selected group
 */
export function attachGizmo(transformControls, group) {
  if (!transformControls) return;

  transformControls.detach();

  if (!group) return;

  transformControls.attach(group);
}
