import { useKernel } from "../kernel/useKernel";

export default function TransformPanel({ snapshot }) {
  const kernel = useKernel();

  const canTransform =
    snapshot?.status === "draft" &&
    kernel.mode === "editing" &&
    kernel.station === "geometry" &&
    kernel.canUseTool("translate");

  const onSubmit = async (params) => {
    try {
      await kernel.execute({
        tool: "translate",
        params,
      });
    } catch (err) {
      kernel.reportError(err.message);
    }
  };

  return (
    <fieldset disabled={!canTransform}>
      <button>Translate</button>
      {/* param inputs stubbed */}
    </fieldset>
  );
}

