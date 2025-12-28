// src/utils/inviteContext.js

const INVITE_CONTEXT_KEY = "invite_context";

export const setInviteContext = (context) => {
  localStorage.setItem(
    INVITE_CONTEXT_KEY,
    JSON.stringify(context)
  );
};

export const getInviteContext = () => {
  try {
    const raw = localStorage.getItem(INVITE_CONTEXT_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

export const clearInviteContext = () => {
  localStorage.removeItem(INVITE_CONTEXT_KEY);
};

