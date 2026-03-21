export const SHORTCUTS = [
  { key: "g", action: "TRANSFORM_TRANSLATE" },
  { key: "r", action: "TRANSFORM_ROTATE" },
  { key: "s", action: "TRANSFORM_SCALE" },

  { key: "z", ctrl: true, action: "UNDO" },

  // ✅ BOTH redo styles
  { key: "z", ctrl: true, shift: true, action: "REDO" },
  { key: "y", ctrl: true, action: "REDO" },

  { key: "d", ctrl: true, action: "DUPLICATE" },

  { key: "escape", action: "CLEAR_SELECTION" },
];
