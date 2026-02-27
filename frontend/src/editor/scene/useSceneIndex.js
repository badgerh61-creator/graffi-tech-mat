import { useEffect, useMemo, useState } from "react";
import { fetchScene } from "../../services/studio/sceneApi";
import { clearSelection, useSelection } from "../selection/selectionStore";
import { isSelectionValidForSceneIndex, makeSceneRebindKey } from "./sceneSync";

export function useSceneIndex(snapshotId) {
  const { selectedId } = useSelection();

  const [sceneIndex, setSceneIndex] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const rebindKey = useMemo(() => makeSceneRebindKey(snapshotId), [snapshotId]);

  useEffect(() => {
    if (!snapshotId) {
      setSceneIndex(null);
      setError(null);
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    fetchScene(snapshotId)
      .then((data) => {
        if (cancelled) return;
        setSceneIndex(data);

        // enforce selection validity
        if (!isSelectionValidForSceneIndex(selectedId, data)) {
          clearSelection();
        }
      })
      .catch((e) => {
        if (cancelled) return;
        setError(String(e?.message || e));
        setSceneIndex(null);
      })
      .finally(() => {
        if (cancelled) return;
        setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // NOTE: selectionId included so selection validity is rechecked
  }, [snapshotId, selectedId]);

  return { sceneIndex, error, loading, rebindKey };
}
