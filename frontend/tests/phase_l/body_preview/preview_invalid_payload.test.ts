import { BodyPreviewController } from "@/preview/body/BodyPreviewController";

test("invalid body payload does not crash", () => {
  const controller = new BodyPreviewController();

  controller.load({});

  expect(controller.getState()).toBeNull();
});

