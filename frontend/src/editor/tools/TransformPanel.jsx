import { useState } from "react";
import { useKernel } from "../kernel/useKernel";

export default function TransformPanel({ snapshot }) {
  const kernel = useKernel();

  const [axisLock, setAxisLock] = useState("xyz");

  const canTransform =
    snapshot?.status === "draft" &&
    kernel.mode === "editing" &&
    kernel.station === "geometry" &&
    kernel.canUseTool("translate");

  const onSubmit = async () => {
    try {
      await kernel.execute({
        tool: "translate",
        params: {
          x: 10,
          y: 0,
          z: 0,

          // Tier 7.4 axis locks
          axis_lock: axisLock,
          drag_source: "panel",
        },
      });
    } catch (err) {
      kernel.reportError(err.message);
    }
  };

  return (
    <fieldset disabled={!canTransform}>
      <legend>Transform</legend>

      <button type="button" onClick={onSubmit}>
        Translate
      </button>

      <div style={{ marginTop: 10 }}>
        <label>
          Axis
          <select
            value={axisLock}
            onChange={(e) => setAxisLock(e.target.value)}
          >
            <option value="x">X</option>
            <option value="y">Y</option>
            <option value="z">Z</option>
            <option value="xy">XY</option>
            <option value="xz">XZ</option>
            <option value="yz">YZ</option>
            <option value="xyz">XYZ</option>
          </select>
        </label>
      </div>
    </fieldset>
  );
}
