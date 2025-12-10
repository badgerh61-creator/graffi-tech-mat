// src/store/assetStore.js
import { create } from "zustand";
import { nanoid } from "nanoid";

export const useAssetStore = create((set, get) => ({
  assets: [],

  addAssetFromFile: async (file) => {
    const id = nanoid();
    const ext = file.name.split(".").pop().toLowerCase();
    const mime = file.type || "application/octet-stream";
    const url = URL.createObjectURL(file);

    let thumbnailUrl = null;
    if (mime.startsWith("image/")) {
      thumbnailUrl = await get()._createThumb(file);
    }

    const type =
      mime.startsWith("image/")
        ? "image"
        : ["glb", "gltf", "fbx", "obj", "usdz"].includes(ext)
        ? "model"
        : ["hdr", "exr"].includes(ext)
        ? "hdri"
        : "file";

    const asset = {
      id,
      name: file.name,
      url,
      size: file.size,
      thumbnailUrl,
      type,
      meta: { ext, mime },
      createdAt: Date.now(),
    };

    set((s) => ({ assets: [...s.assets, asset] }));
    return asset;
  },

  removeAsset: (id) => {
    const asset = get().assets.find((x) => x.id === id);
    if (asset) {
      try {
        URL.revokeObjectURL(asset.url);
        if (asset.thumbnailUrl) URL.revokeObjectURL(asset.thumbnailUrl);
      } catch {}
    }
    set((s) => ({ assets: s.assets.filter((a) => a.id !== id) }));
  },

  _createThumb: async (file) => {
    const img = await new Promise((res, rej) => {
      const r = new FileReader();
      r.onload = () => {
        const im = new Image();
        im.onload = () => res(im);
        im.onerror = rej;
        im.src = r.result;
      };
      r.readAsDataURL(file);
    });

    const canvas = document.createElement("canvas");
    canvas.width = 160;
    canvas.height = 160;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, 160, 160);

    return await new Promise((res) =>
      canvas.toBlob((b) => res(URL.createObjectURL(b)), "image/webp")
    );
  },
}));
