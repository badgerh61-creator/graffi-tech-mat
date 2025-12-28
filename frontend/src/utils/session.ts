// src/utils/session.ts

import axios from "axios";
import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from "./auth";

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000";

/**
 * In-memory guard to prevent multiple refresh attempts
 * per application boot.
 */
let refreshAttempted = false;

/**
 * Restore session on app boot
 * - returns true if authenticated
 * - returns false if user must login
 */
export async function restoreSession(): Promise<boolean> {
  const access = getAccessToken();
  const refresh = getRefreshToken();

  // Already logged in and valid
  if (access) return true;

  // No way to restore
  if (!refresh) return false;

  // 🔒 F3.5 GUARD: only one refresh attempt
  if (refreshAttempted) {
    return false;
  }

  refreshAttempted = true;

  try {
    const res = await axios.post(`${API_BASE}/refresh`, {
      refresh_token: refresh,
    });

    const { access_token, refresh_token } = res.data || {};

    if (!access_token || !refresh_token) {
      throw new Error("Invalid refresh response");
    }

    setTokens(access_token, refresh_token);
    return true;
  } catch {
    clearTokens();
    return false;
  }
}

/**
 * Reset session state (used on logout)
 */
export function resetSessionState() {
  refreshAttempted = false;
}

