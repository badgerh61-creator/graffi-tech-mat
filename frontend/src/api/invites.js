import { api } from "./client";

export const invitesApi = {
  accept: (token) => {
    return api.post(`/models/invites/${token}/accept`);
  },
};

