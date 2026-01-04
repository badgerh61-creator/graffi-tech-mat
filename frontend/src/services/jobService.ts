// frontend/src/services/jobService.ts

import type { Job } from "../types/job.types";
import { apiClient } from "./apiClient";

/**
 * Phase H3 / Phase I.6 — read-only background jobs
 * Canonical adapter (array-safe)
 */
export async function fetchJobs(): Promise<Job[]> {
  const res = await apiClient.get<Job[]>("/jobs/");

  // 🔒 HARD CONTRACT GUARD
  // Backend returns a bare array — never `.items`
  if (Array.isArray(res.data)) {
    return res.data;
  }

  // Fail-safe: never let UI crash
  return [];
}


