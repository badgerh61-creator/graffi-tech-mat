// frontend/src/services/apiClient.ts

import axios from "axios";

export const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: false, // 🔴 IMPORTANT
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("graffi.access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

