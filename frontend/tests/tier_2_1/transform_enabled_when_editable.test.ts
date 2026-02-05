test("transform tool enabled for draft snapshot in editing mode", () => {
  renderEditor({
    snapshot: { status: "draft" },
    mode: "editing",
    station: "geometry",
  });

  expect(getTransformButton()).toBeEnabled();
});

