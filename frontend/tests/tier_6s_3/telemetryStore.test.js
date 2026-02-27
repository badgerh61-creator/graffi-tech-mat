import { addArtifact, telemetryGetSnapshot, clearArtifacts } from "../../src/editor/telemetry/telemetryStore";

test("artifacts are sorted deterministically by artifact_id", () => {
  clearArtifacts();

  addArtifact({ artifact_id: 5, curves: { time_s: [], speed_mps: [] } });
  addArtifact({ artifact_id: 1, curves: { time_s: [], speed_mps: [] } });

  const s = telemetryGetSnapshot();
  expect(s.artifacts[0].artifact_id).toBe(1);
  expect(s.artifacts[1].artifact_id).toBe(5);
});
