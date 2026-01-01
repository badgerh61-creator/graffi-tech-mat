import { CapabilityMap } from "./capability.types";

/**
 * Role → capability mapping.
 * Immutable, explicit, namespaced.
 */
export const ROLE_CAPABILITIES = Object.freeze<
  Readonly<Record<string, CapabilityMap>>
>({
  viewer: Object.freeze({
    // global
    view: true,
    edit: false,
    upload: false,
    delete: false,

    // assets
    "assets.view": true,
    "assets.use": false,
  }),

  editor: Object.freeze({
    // global
    view: true,
    edit: true,
    upload: true,
    delete: false,

    // assets
    "assets.view": true,
    "assets.use": true,
  }),

  admin: Object.freeze({
    // global
    view: true,
    edit: true,
    upload: true,
    delete: true,
    admin: true,

    // assets
    "assets.view": true,
    "assets.use": true,
  }),
});

