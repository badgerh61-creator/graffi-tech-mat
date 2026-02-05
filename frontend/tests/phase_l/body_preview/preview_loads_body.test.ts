import { BodyPreviewController } from "@/state/preview/body/BodyPreviewController";

test("body preview loads body_state", () => {
  const controller = new BodyPreviewController();

  controller.load({
    body_state: {
      preset_id: "widebody_v1",
      parameters: { width: 1.2 },
    },
  });

  expect(controller.getState()).toEqual({
    presetId: "widebody_v1",
    parameters: { width: 1.2 },
  });
});

