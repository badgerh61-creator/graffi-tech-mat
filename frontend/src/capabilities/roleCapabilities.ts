import { CapabilityMap } from "./capability.types";

/**
 * Role → capability mapping.
 * This is immutable and must never be modified at runtime.
 */
export const ROLE_CAPABILITIES = Object.freeze<
  Readonly<Record<string, CapabilityMap>>
>({
  viewer: Object.freeze({
    view: true,
    edit: false,
    upload: false,
    delete: false,
  }),

  editor: Object.freeze({
    view: true,
    edit: true,
    upload: true,
    delete: false,
  }),

  admin: Object.freeze({
    view: true,
    edit: true,
    upload: true,
    delete: true,
    admin: true,
  }),
});

