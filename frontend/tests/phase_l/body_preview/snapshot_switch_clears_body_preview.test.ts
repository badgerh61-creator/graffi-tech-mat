import { BodyPreviewController } from "@/state/preview/body/BodyPreviewController";

test("snapshot switch clears body preview", () => {
  const controller = new BodyPreviewController();

  controller.load({
    body_state: {
      preset_id: "widebody_v1",
      parameters: {},
    },
  });

  controller.clear();

  expect(controller.getState()).toBeNull();
});

