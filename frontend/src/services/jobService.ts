// frontend/src/services/jobService.ts

import type { Job } from "../types/job.types";
import { apiClient } from "./apiClient";

/**
 * Fetch async jobs (read-only)
 */
export async function fetchJobs(): Promise<Job[]> {
  const res = await apiClient.get("/jobs");
  return res.data.items;
}

