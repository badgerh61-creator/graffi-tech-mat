import { normalizeRuns } from "../../src/editor/telemetry/multiChart";

test("normalizeRuns returns one series per artifact", () => {
  const runs = [
    { artifact_id: 2, curves: { time_s: [0, 1], speed_mps: [0, 2] } },
    { artifact_id: 1, curves: { time_s: [0, 1], speed_mps: [1, 3] } },
  ];

  const series = normalizeRuns(runs, "speed_mps");
  expect(series.length).toBe(2);
  expect(series[0].artifact_id).toBe(1); // sorted
  expect(series[0].points.length).toBe(2);
});
