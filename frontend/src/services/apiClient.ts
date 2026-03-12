import { API_BASE } from "../config/apiBase";

// frontend/src/services/apiClient.ts

import axios from "axios";

export const apiClient = axios.create({
  baseURL: API_BASE,
  withCredentials: false, // 🔴 IMPORTANT
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("graffi.access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

