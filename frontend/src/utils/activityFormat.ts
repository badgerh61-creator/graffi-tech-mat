export function formatActivity(event: any): string {
  switch (event.action) {
    case "model.invite.sent":
      return "Sent a collaboration invite";
    case "model.invite.accepted":
      return "Accepted a collaboration invite";
    case "model.collaborator.add":
      return "Added a collaborator";
    case "model.collaborator.remove":
      return "Removed a collaborator";
    case "model.create":
      return "Created a model";
    case "asset.processed":
      return "Asset processed successfully";
    case "asset.failed":
      return "Asset processing failed";
    default:
      return event.action;
  }
}

