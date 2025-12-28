// frontend/src/api/assets.ts

import api from "./client";

export const assetsApi = {
  upload(file: File) {
    const form = new FormData();

    // 🔴 THIS IS CRITICAL — key MUST be "file"
    form.append("file", file);

    return api.post("/upload/", form, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
};

