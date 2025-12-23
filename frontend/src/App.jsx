import React, { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "./pages/Login";
import Studio from "./pages/Studio";
import {
  isAuthenticated,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "./utils/auth";

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

/* ---------------- AUTH GUARD ---------------- */
function RequireAuth({ children }) {
  return isAuthenticated()
    ? children
    : <Navigate to="/login" replace />;
}

export default function App() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function restoreSession() {
      const refreshToken = getRefreshToken();

      // No refresh token → normal login flow
      if (!refreshToken) {
        setReady(true);
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            refresh_token: refreshToken,
          }),
        });

        if (!res.ok) {
          throw new Error("Refresh failed");
        }

        const data = await res.json();

        if (!data.access_token) {
          throw new Error("Invalid refresh response");
        }

        setTokens(data.access_token, data.refresh_token);
      } catch {
        clearTokens();
      } finally {
        setReady(true);
      }
    }

    restoreSession();
  }, []);

  if (!ready) {
    return (
      <div className="min-h-screen flex items-center justify-center text-slate-500">
        Restoring session…
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/studio"
          element={
            <RequireAuth>
              <Studio />
            </RequireAuth>
          }
        />

        <Route
          path="*"
          element={<Navigate to="/studio" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

