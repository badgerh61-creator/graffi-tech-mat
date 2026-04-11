/**
 * Tier 7.77 — Gizmo hotkeys
 */

export function bindGizmoHotkeys(transformControls) {
  function onKeyDown(e) {
    if (!transformControls) return;

    switch (e.key.toLowerCase()) {
      case "w":
        transformControls.setMode("translate");
        break;

      case "e":
        transformControls.setMode("rotate");
        break;

      case "r":
        transformControls.setMode("scale");
        break;

      default:
        return;
    }

    e.preventDefault();
  }

  window.addEventListener("keydown", onKeyDown);

  return () => {
    window.removeEventListener("keydown", onKeyDown);
  };
}
