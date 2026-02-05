test("transform tool disabled when snapshot is completed", () => {
  renderEditor({
    snapshot: { status: "completed" },
  });

  expect(getTransformButton()).toBeDisabled();
});

