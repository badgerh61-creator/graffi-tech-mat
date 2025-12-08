// src/store/useStore.js
// small helpers for selectors if needed in future
export function pick(...keys) {
  return (state) => {
    const out = {};
    for (const k of keys) out[k] = state[k];
    return out;
  };
}
