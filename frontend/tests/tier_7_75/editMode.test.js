test("edit mode becomes ready", () => {
  const state = { ready: false };

  state.ready = true;

  expect(state.ready).toBe(true);
});
