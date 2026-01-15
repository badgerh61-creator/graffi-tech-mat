import { BodyPreviewController } from "@/preview/body/BodyPreviewController";

test("reload produces same body preview", () => {
  const controller = new BodyPreviewController();

  const payload = {
    body_state: {
      preset_id: "widebody_v1",
      parameters: { width: 1.2 },
    },
  };

  controller.load(payload);
  const first = controller.getState();

  controller.load(payload);
  const second = controller.getState();

  expect(first).toEqual(second);
});

