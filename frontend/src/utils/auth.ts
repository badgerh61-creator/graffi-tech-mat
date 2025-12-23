const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

/* ================= GETTERS ================= */

export const getAccessToken = (): string | null =>
  localStorage.getItem(ACCESS_TOKEN_KEY);

export const getRefreshToken = (): string | null =>
  localStorage.getItem(REFRESH_TOKEN_KEY);

/* ================= SETTERS ================= */

export const setTokens = (
  accessToken: string,
  refreshToken?: string
) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
};

/* ================= CLEAR ================= */

export const clearTokens = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/* ================= JWT HELPERS ================= */

function decodeJwt(token: string): any | null {
  try {
    const payload = token.split(".")[1];
    return JSON.parse(atob(payload));
  } catch {
    return null;
  }
}

export const isAccessTokenExpired = (): boolean => {
  const token = getAccessToken();
  if (!token) return true;

  const decoded = decodeJwt(token);
  if (!decoded?.exp) return true;

  return Date.now() >= decoded.exp * 1000;
};

/* ================= AUTH STATE ================= */

export const isAuthenticated = (): boolean => {
  return !!getAccessToken() && !isAccessTokenExpired();
};

