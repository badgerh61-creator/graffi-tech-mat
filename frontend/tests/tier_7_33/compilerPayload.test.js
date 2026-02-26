test("APPLY_COMPONENT payload shape is canonical", () => {
  const payload = {
    tool: "APPLY_COMPONENT",
    station: "geometry",
    payload: {
      component_id: "cmp1",
      next_params: { delta_y: 0.25 },
      target_id: "vehicle-1::CarRoot",
    },
  };

  expect(payload.tool).toBe("APPLY_COMPONENT");
  expect(payload.payload.component_id).toBe("cmp1");
  expect(payload.payload.next_params.delta_y).toBe(0.25);
});
