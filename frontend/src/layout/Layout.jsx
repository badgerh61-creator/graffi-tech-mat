// src/layout/Layout.jsx

export default function Layout() {
  if (import.meta.env.DEV) {
    console.warn(
      "[DEPRECATED] Layout.jsx is legacy and must not be used for /studio."
    );
  }

  throw new Error(
    "Legacy Layout.jsx is disabled. Use EditorLayoutHost instead."
  );
}

