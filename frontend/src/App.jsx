// src/App.jsx
import React from "react";
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

import { isAuthenticated } from "./utils/auth";

/* ---------------- AUTH GUARD ---------------- */
function RequireAuth({ children }) {
  return isAuthenticated()
    ? children
    : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ---------- AUTH ---------- */}
        <Route path="/login" element={<Login />} />

        {/* ---------- INVITES ---------- */}
        <Route
          path="/models/invites/:token/accept"
          element={<AcceptInvite />}
        />

        {/* ---------- STUDIO ---------- */}
        <Route
          path="/studio"
          element={
            <RequireAuth>
              <Studio />
            </RequireAuth>
          }
        />

        {/* ---------- ADMIN ---------- */}
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

        {/* ---------- FALLBACK ---------- */}
        <Route
          path="*"
          element={<Navigate to="/studio" replace />}
        />
      </Routes>
    </BrowserRouter>
  );
}

