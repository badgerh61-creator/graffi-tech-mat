import { normalizeSeries, toPolylinePoints } from "../../src/editor/telemetry/simpleChart.js";

test("normalizeSeries pairs points", () => {
  const pts = normalizeSeries([0, 1, 2], [10, 11, 12]);
  expect(pts.length).toBe(3);
  expect(pts[1]).toEqual({ x: 1, y: 11 });
});

test("toPolylinePoints returns string", () => {
  const pts = [{ x: 0, y: 0 }, { x: 1, y: 1 }];
  const s = toPolylinePoints(pts, 100, 50);
  expect(typeof s).toBe("string");
  expect(s.length).toBeGreaterThan(0);
});
