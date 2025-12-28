// src/api/invites.js
import { api } from "./client";

export const invitesApi = {
  accept: (token) => {
    return api.post(`/models/invites/${token}/accept`);
  },

  // 🔵 ADD: resend invite (safe if endpoint exists)
  resend: (inviteId) => {
    return api.post(`/models/invites/${inviteId}/resend`);
  },

  // 🔵 ADD: revoke invite
  revoke: (inviteId) => {
    return api.delete(`/models/invites/${inviteId}`);
  },
};

