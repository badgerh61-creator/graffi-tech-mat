test("decor tools hidden without capability", () => {
  renderDecorStudio({
    capabilities: [],
  });

  expect(screen.queryByText(/apply material/i)).toBeNull();
});

