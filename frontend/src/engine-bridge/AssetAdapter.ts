import { AssetRef } from "../../../engine/assets/AssetRef";

let attachedAssets: AssetRef[] = [];

export const AssetAdapter = {
  attach(ref: AssetRef) {
    attachedAssets.push(ref);
  },

  list(): AssetRef[] {
    return attachedAssets;
  },

  clear() {
    attachedAssets = [];
  },
};

