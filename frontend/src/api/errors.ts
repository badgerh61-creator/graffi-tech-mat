export function normalizeApiError(error: any): string {
  if (error?.response?.data?.detail) {
    return error.response.data.detail;
  }

  if (typeof error?.message === "string") {
    return error.message;
  }

  return "Unexpected error occurred. Please try again.";
}

