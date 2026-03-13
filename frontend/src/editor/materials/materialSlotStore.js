import { useSyncExternalStore } from "react";

const state = {
  slotsByTarget: {},
};

const listeners = new Set();
const emit = () => listeners.forEach((l) => l());

export function setMaterialSlotsForTarget(targetId, slots) {
  if (!targetId) return;
  state.slotsByTarget = {
    ...state.slotsByTarget,
    [String(targetId)]: Array.isArray(slots) ? slots : [],
  };
  emit();
}

export function clearMaterialSlots() {
  state.slotsByTarget = {};
  emit();
}

export function materialSlotGetSnapshot() {
  return state;
}

export function materialSlotSubscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useMaterialSlots() {
  return useSyncExternalStore(
    materialSlotSubscribe,
    materialSlotGetSnapshot,
    materialSlotGetSnapshot
  );
}
