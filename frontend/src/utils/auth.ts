// src/utils/auth.js

import { resetSessionState } from "./session";

const ACCESS_TOKEN_KEY = "graffi.access_token";
const REFRESH_TOKEN_KEY = "graffi.refresh_token";

/* ================= GETTERS ================= */

export const getAccessToken = () =>
  localStorage.getItem(ACCESS_TOKEN_KEY);

export const getRefreshToken = () =>
  localStorage.getItem(REFRESH_TOKEN_KEY);

/* ================= SETTERS ================= */

export const setTokens = (accessToken, refreshToken) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);

  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
};

/* ================= CLEAR ================= */

export const clearTokens = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  resetSessionState(); // 🔒 F3.5 REQUIRED
};

/* ================= JWT HELPERS ================= */

function decodeJwt(token) {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

export const isAccessTokenExpired = () => {
  const token = getAccessToken();
  if (!token) return true;

  const decoded = decodeJwt(token);
  if (!decoded?.exp) return true;

  return Date.now() >= decoded.exp * 1000;
};

/* ================= AUTH STATE ================= */

export const isAuthenticated = () => {
  try {
    return !!getAccessToken() && !isAccessTokenExpired();
  } catch {
    return false;
  }
};

/* ================= USER DESCRIPTOR ================= */

export const getCurrentUser = () => {
  const token = getAccessToken();
  if (!token) return null;

  const decoded = decodeJwt(token);
  if (!decoded) return null;

  return {
    id: decoded.sub ? Number(decoded.sub) : null,
    isAdmin: !!decoded.is_admin,
    roles: decoded.roles ?? [],
    permissions: decoded.permissions ?? [],
  };
};

