import { useSyncExternalStore } from "react";

const state = {
  artifacts: [],      // array of artifact objects
  visibleCurves: {},  // curveName -> boolean
};

const listeners = new Set();
function emit() { for (const l of listeners) l(); }

export function telemetrySubscribe(l) {
  listeners.add(l);
  return () => listeners.delete(l);
}

export function telemetryGetSnapshot() {
  return state;
}

export function useTelemetry() {
  return useSyncExternalStore(
    telemetrySubscribe,
    telemetryGetSnapshot,
    telemetryGetSnapshot
  );
}

export function addArtifact(artifact) {
  if (!artifact?.artifact_id) return;

  // no duplicates
  if (state.artifacts.some((a) => a.artifact_id === artifact.artifact_id)) return;

  state.artifacts = [...state.artifacts, artifact].sort(
    (a, b) => a.artifact_id - b.artifact_id
  );

  // init curve visibility deterministically
  const curves = Object.keys(artifact.curves || {}).sort();
  for (const c of curves) {
    if (c === "time_s") continue;
    if (state.visibleCurves[c] === undefined) state.visibleCurves[c] = true;
  }

  emit();
}

export function removeArtifact(artifactId) {
  state.artifacts = state.artifacts.filter((a) => a.artifact_id !== artifactId);
  emit();
}

export function toggleCurve(curveName) {
  state.visibleCurves[curveName] = !state.visibleCurves[curveName];
  emit();
}

export function clearArtifacts() {
  state.artifacts = [];
  state.visibleCurves = {};
  emit();
}
