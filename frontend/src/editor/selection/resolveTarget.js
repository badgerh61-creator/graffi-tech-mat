export function resolvePrimaryTarget(sel) {
  if (!sel?.primary) return { ok: false, reason: "no_selection" };
  return { ok: true, target_id: sel.primary.id, kind: sel.primary.kind };
}
