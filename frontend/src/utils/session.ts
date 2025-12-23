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
 * Restore session on app boot
 * - returns true if authenticated
 * - returns false if user must login
 */
export async function restoreSession(): Promise<boolean> {
  const access = getAccessToken();
  const refresh = getRefreshToken();

  // Already logged in
  if (access) return true;

  // No way to restore
  if (!refresh) return false;

  try {
    const res = await axios.post(`${API_BASE}/refresh`, {
      refresh_token: refresh,
    });

    const { access_token, refresh_token } = res.data;

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

