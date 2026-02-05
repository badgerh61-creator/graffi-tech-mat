import { BodyPreviewController } from "@/state/preview/body/BodyPreviewController";

test("body preview is deterministic", () => {
  const c1 = new BodyPreviewController();
  const c2 = new BodyPreviewController();

  const payload = {
    body_state: {
      preset_id: "widebody_v1",
      parameters: { width: 1.2 },
    },
  };

  c1.load(payload);
  c2.load(payload);

  expect(c1.getState()).toEqual(c2.getState());
});

