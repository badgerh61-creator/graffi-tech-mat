test("UI state unchanged after rejection", async () => {
  const before = getSnapshotId();

  mockKernelReject("invalid operation");
  submitTransform({ x: 5 });

  expect(getSnapshotId()).toBe(before);
});

