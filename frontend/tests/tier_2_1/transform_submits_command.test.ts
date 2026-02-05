test("transform submits kernel command", async () => {
  mockKernelExecute();

  clickTransformButton();
  submitTransform({ x: 10 });

  expect(kernel.execute).toHaveBeenCalledWith(
    expect.objectContaining({
      tool: "translate",
      params: { x: 10 },
    })
  );
});

