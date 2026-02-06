// frontend/src/editor/kernel/useSnapshotHistory.ts

export function useSnapshotHistory() {
  /**
   * Graph format expected by tests:
   * [
   *   { id, parentId, status }
   * ]
   */

  const history = []; // default empty — tests inject mock data
  const activeSnapshotId = null;

  function navigateTo(snapshotId: string) {
    // 🔒 Read-only intent emission
    // Actual navigation is kernel-owned
    console.log("navigateTo snapshot", snapshotId);
  }

  return {
    history,
    activeSnapshotId,
    navigateTo,
  };
}

