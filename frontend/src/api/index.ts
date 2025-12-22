import { api } from "./client";

/* ---------- AUTH ---------- */
export const authApi = {
  login: (email: string, password: string) =>
    api.post(
      "/login",
      new URLSearchParams({
        username: email,
        password,
      })
    ),
};

/* ---------- ASSETS ---------- */
export const assetsApi = {
  upload: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return api.post("/upload/", form);
  },
};

