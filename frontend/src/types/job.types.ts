// frontend/src/types/job.types.ts

export type JobStatus =
  | "queued"
  | "running"
  | "completed"
  | "failed";

export interface Job {
  id: string;
  type: string;
  status: JobStatus;
  progress: number; // 0–100
  error?: string;
  createdAt: string;
}

