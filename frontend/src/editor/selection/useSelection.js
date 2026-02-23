import { useState } from "react";

export function useSelection() {
  const [selectedId, setSelectedId] = useState(null);

  return {
    selectedId,
    select: (id) => setSelectedId(id),
    clear: () => setSelectedId(null),
  };
}
