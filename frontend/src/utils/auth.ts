// src/utils/auth.js

import { resetSessionState } from "./session";

const ACCESS_TOKEN_KEY = "graffi.access_token";
const REFRESH_TOKEN_KEY = "graffi.refresh_token";
const USER_CACHE_KEY = "graffi.user";

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
  localStorage.removeItem(USER_CACHE_KEY); // 🔥 clear user too
  resetSessionState();
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

/* ================= USER (LEGACY — DO NOT TRUST FOR ROLE) ================= */

export const getCurrentUser = () => {
  const token = getAccessToken();
  if (!token) return null;

  const decoded = decodeJwt(token);
  if (!decoded) return null;

  return {
    id: decoded.sub ? Number(decoded.sub) : null,
  };
};

/* ================= 🔥 REAL USER (SOURCE OF TRUTH) ================= */

export const fetchCurrentUser = async () => {
  const token = getAccessToken();
  if (!token) return null;

  try {
    const res = await fetch("http://localhost:8000/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) throw new Error("Failed to fetch /me");

    const data = await res.json();

    console.log("🔥 USER FROM /me:", data);

    // ✅ cache for fast access
    localStorage.setItem(USER_CACHE_KEY, JSON.stringify(data));

    return data;
  } catch (err) {
    console.error("User fetch failed:", err);
    return null;
  }
};

/* ================= OPTIONAL CACHE ACCESS ================= */

export const getCachedUser = () => {
  try {
    const raw = localStorage.getItem(USER_CACHE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};
