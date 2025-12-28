// src/App.jsx
import React, { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "./pages/Login";
import Studio from "./pages/Studio";
import Admin from "./pages/Admin";
import AcceptInvite from "./pages/AcceptInvite";
import AdminRoute from "./routes/AdminRoute";

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
    let cancelled = false;

    async function restoreSession() {
      const refreshToken = getRefreshToken();

      if (!refreshToken) {
        if (!cancelled) setReady(true);
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });

        if (!res.ok) throw new Error("Refresh failed");

        const data = await res.json();
        setTokens(data.access_token, data.refresh_token);
      } catch {
        clearTokens();
      } finally {
        if (!cancelled) setReady(true);
      }
    }

    restoreSession();
    return () => {
      cancelled = true;
    };
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
          path="/models/invites/:token/accept"
          element={<AcceptInvite />}
        />

        <Route
          path="/studio"
          element={
            <RequireAuth>
              <Studio />
            </RequireAuth>
          }
        />

        <Route
          path="/admin"
          element={
            <RequireAuth>
              <AdminRoute>
                <Admin />
              </AdminRoute>
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

