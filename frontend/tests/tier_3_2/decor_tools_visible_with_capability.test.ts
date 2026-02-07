test("decor tools visible when capability present", () => {
  renderDecorStudio({
    capabilities: ["canEditExteriorDecor"],
  });

  expect(screen.getByText(/apply material/i)).toBeInTheDocument();
});

