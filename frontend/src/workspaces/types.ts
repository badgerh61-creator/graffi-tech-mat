/**
 * PHASE J WORKSPACE TYPES (READ-ONLY)
 */

export type SnapshotStatus = "completed" | "failed" | "pending";

export interface RenderedSnapshot {
  id: string;
  imageUrl: string;
  status: SnapshotStatus;
  createdAt: string;
  engineVersion: string;
}

export interface SnapshotGroups {
  completed: RenderedSnapshot[];
  failed: RenderedSnapshot[];
  pending: RenderedSnapshot[];
}

export interface WorkspaceMeta {
  total: number;
}

export interface ProjectWorkspace {
  snapshots: SnapshotGroups;
  meta?: WorkspaceMeta;
}

