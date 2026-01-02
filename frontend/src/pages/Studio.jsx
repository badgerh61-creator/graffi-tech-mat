// frontend/src/pages/Studio.jsx
// 🚫 LEGACY STUDIO — DISABLED

export default function Studio() {
  if (import.meta.env.DEV) {
    console.error(
      "[FATAL] Legacy Studio.jsx mounted. This must not happen."
    );
  }

  throw new Error(
    "Legacy Studio.jsx is disabled. Use /studio with StudioEditor only."
  );
}

