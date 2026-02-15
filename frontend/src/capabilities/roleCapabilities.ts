// frontend/src/capabilities/roleCapabilities.ts

import { CapabilityMap } from "./capability.types";

export const ROLE_CAPABILITIES = Object.freeze<
  Readonly<Record<string, CapabilityMap>>
>({
  viewer: Object.freeze({
    view: true,
    edit: false,
    upload: false,
    delete: false,

    "assets.view": true,
    "assets.use": false,
    "engine.preview": true,
    "jobs.view": true,

    "engineering.assistant.use": false,
  }),

  editor: Object.freeze({
    view: true,
    edit: true,
    upload: true,
    delete: false,

    "assets.view": true,
    "assets.use": true,
    "engine.preview": true,
    "jobs.view": true,

    "decor.exterior.edit": true,

    "engineering.assistant.use": true,
  }),

  admin: Object.freeze({
    view: true,
    edit: true,
    upload: true,
    delete: true,
    admin: true,

    "assets.view": true,
    "assets.use": true,
    "engine.preview": true,
    "jobs.view": true,

    "decor.exterior.edit": true,

    "engineering.assistant.use": true,
  }),
});

