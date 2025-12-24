import React from "react";
import { Navigate } from "react-router-dom";
import { getAccessToken } from "../utils/auth";

function decodeJwt(token) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return null;
  }
}

export default function AdminRoute({ children }) {
  const token = getAccessToken();
  const payload = token ? decodeJwt(token) : null;

  if (!payload || payload.role !== "admin") {
    return <Navigate to="/studio" replace />;
  }

  return children;
}

