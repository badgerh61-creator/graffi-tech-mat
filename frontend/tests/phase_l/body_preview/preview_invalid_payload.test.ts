import { BodyPreviewController } from "@/state/preview/body/BodyPreviewController";

test("invalid body payload does not crash", () => {
  const controller = new BodyPreviewController();

  controller.load({});

  expect(controller.getState()).toBeNull();
});

