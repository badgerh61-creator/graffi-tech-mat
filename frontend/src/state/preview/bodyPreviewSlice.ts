import { BodyPreviewController } from "../../preview/body/BodyPreviewController";

export const bodyPreviewController = new BodyPreviewController();

export function loadBodyPreview(snapshotPayload: any) {
  bodyPreviewController.load(snapshotPayload);
}

export function clearBodyPreview() {
  bodyPreviewController.clear();
}

